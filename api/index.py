"""
OSRS Guru RAG API v2.0 — 三层架构
=================================
Layer 1: 本地 115 篇攻略 TF-IDF 检索
Layer 2: OSRS Wiki API 实时数据补充
Layer 3: DeepSeek V4 Flash (主) + Groq/Llama3 (备) 双模型生成

端点:
    GET /rag-api/search?q=<question>
    返回: {"answer": "...", "source": "osrsguru_rag|osrs_wiki|deepseek|gpt4o"}

本地开发: uvicorn api.index:app --reload --port 8000
"""

import json
import os
import re
import math
import numpy as np
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

# ============================================================
# 配置
# ============================================================
DATA_DIR = Path(__file__).parent.parent / "data"

# --- DeepSeek (主模型) ---
DEEPSEEK_API_KEY = os.environ.get(
    "DEEPSEEK_API_KEY",
    "sk-c08d3179018b44d7b150f54af4a82b1b",
)
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-v4-flash"

# --- Groq/Llama3 (备用模型，美国节点，免费) ---
GROQ_API_KEY = os.environ.get(
    "GROQ_API_KEY",
    "",
)
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "llama-3.3-70b-versatile"

# --- OSRS Wiki ---
WIKI_API_BASE = "https://oldschool.runescape.wiki/api.php"
WIKI_HEADERS = {"User-Agent": "OSRSGuru-RAG/2.0 (contact@osrsguru.com)"}

# --- 检索配置 ---
TOP_K = 5
MIN_SIMILARITY = 0.05
WIKI_TRIGGER_THRESHOLD = 0.15  # RAG 最高分低于此值时触发 Wiki 查询

# ============================================================
# FastAPI 应用
# ============================================================
app = FastAPI(
    title="OSRS Guru RAG API",
    description="Three-layer RAG: Local Guides + OSRS Wiki + DeepSeek/Groq",
    version="2.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 全局状态
# ============================================================
chunks: list[dict] = []
vocab: dict[str, dict] = {}
tfidf_matrix: np.ndarray = None
index_loaded = False


# ============================================================
# Layer 1: 本地 TF-IDF 检索
# ============================================================

def _tokenize(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    words = [w for w in text.split() if len(w) > 1]
    tokens = words.copy()
    for i in range(len(words) - 1):
        tokens.append(f"{words[i]} {words[i+1]}")
    return tokens


def _tfidf_query_vector(query: str) -> np.ndarray:
    n_features = len(vocab)
    vec = np.zeros(n_features, dtype=np.float32)
    tokens = _tokenize(query)
    tf = {}
    for t in tokens:
        if t in vocab:
            tf[t] = tf.get(t, 0) + 1
    if not tf:
        return vec
    for term, count in tf.items():
        entry = vocab[term]
        idx = entry["index"]
        tf_val = 1 + math.log(count) if count > 0 else 0
        vec[idx] = tf_val * entry["idf"]
    norm = np.linalg.norm(vec)
    if norm > 1e-10:
        vec = vec / norm
    return vec


def _cosine_similarity(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return np.dot(matrix, query_vec)


def load_index():
    global chunks, vocab, tfidf_matrix, index_loaded
    if index_loaded:
        return
    try:
        chunks_path = DATA_DIR / "chunks.json"
        if not chunks_path.exists():
            raise FileNotFoundError(f"chunks.json not found. Run: python rag_indexer.py")
        with open(chunks_path, 'r', encoding='utf-8') as f:
            chunks.clear()
            chunks.extend(json.load(f))

        vocab_path = DATA_DIR / "vocab.json"
        if not vocab_path.exists():
            raise FileNotFoundError("vocab.json not found. Re-run rag_indexer.py.")
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab.clear()
            vocab.update(json.load(f))

        for ext in [".npz", ".npy"]:
            matrix_path = DATA_DIR / f"tfidf_matrix{ext}"
            if matrix_path.exists():
                break
        else:
            raise FileNotFoundError("tfidf_matrix.npz not found.")
        loaded = np.load(matrix_path)
        if hasattr(loaded, 'files'):
            tfidf_matrix = loaded[loaded.files[0]]
        else:
            tfidf_matrix = loaded

        index_loaded = True
        print(f"[OK] Index loaded: {len(chunks)} chunks, {len(vocab)} terms, matrix {tfidf_matrix.shape}")
    except Exception as e:
        print(f"[ERR] Failed to load index: {e}")
        raise


# ============================================================
# Layer 2: OSRS Wiki API
# ============================================================

async def _search_wiki(query: str, limit: int = 3) -> list[dict]:
    """搜索 OSRS Wiki"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                WIKI_API_BASE,
                params={
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "format": "json",
                    "srlimit": limit,
                },
                headers=WIKI_HEADERS,
            )
            data = resp.json()
            return [
                {"title": r["title"], "snippet": r.get("snippet", "")}
                for r in data.get("query", {}).get("search", [])
            ]
    except Exception as e:
        print(f"[WIKI] Search error: {e}")
        return []


async def _get_wiki_page(title: str) -> str | None:
    """获取 Wiki 页面正文"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                WIKI_API_BASE,
                params={
                    "action": "query",
                    "prop": "extracts",
                    "exintro": 1,
                    "explaintext": 1,
                    "titles": title,
                    "format": "json",
                },
                headers=WIKI_HEADERS,
            )
            data = resp.json()
            pages = data.get("query", {}).get("pages", {})
            for page_id, page in pages.items():
                if page_id != "-1":
                    return page.get("extract", "")
            return None
    except Exception as e:
        print(f"[WIKI] Page fetch error: {e}")
        return None


async def _query_wiki_layer(query: str) -> str | None:
    """Layer 2 完整流程：搜索 Wiki → 获取页面 → 返回正文"""
    results = await _search_wiki(query, limit=3)
    if not results:
        return None
    # 取最佳匹配页面的完整内容
    for r in results[:2]:
        content = await _get_wiki_page(r["title"])
        if content and len(content) > 100:
            header = f"[Source: OSRS Wiki — {r['title']}]"
            return f"{header}\n{content[:800]}"
    # 如果拿不到完整页面，用 snippet
    snippets = "\n".join([
        f"[Wiki: {r['title']}] {re.sub(r'<[^>]+>', '', r['snippet'])}"
        for r in results
    ])
    return snippets if snippets else None


# ============================================================
# Layer 3: 双模型生成 (DeepSeek 主 + GPT-4o-mini 备)
# ============================================================

async def _call_llm(
    context: str,
    question: str,
    model: str,
    api_key: str,
    base_url: str,
) -> str:
    """通用 LLM 调用"""
    system_prompt = (
        "You are OSRS Guru AI, the AI assistant for osrsguru.com — "
        "the best Old School RuneScape guide site.\n\n"
        "RULES:\n"
        "1. Answer using the provided context. If it's from OSRS Wiki, cite it.\n"
        "2. Keep answers CONCISE (150-300 words) and ACTIONABLE. Use bullet points.\n"
        "3. Use OSRS terms correctly (gp, Ranged, Defence, PK, PvM, etc.).\n"
        "4. Mention specific guide or wiki page names when referencing.\n"
        "5. Be friendly — OSRS players appreciate the grind!"
    )

    user_prompt = (
        f"Knowledge Base Context:\n{context}\n\n"
        f"Player Question: {question}\n\n"
        f"Answer based on the context above:"
    )

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.3,
                "max_tokens": 600,
            },
        )
        if response.status_code != 200:
            raise Exception(f"LLM API {response.status_code}: {response.text[:200]}")
        data = response.json()
        return data["choices"][0]["message"]["content"]


async def _call_deepseek(context: str, question: str) -> str:
    """Layer 3a: DeepSeek (主模型)"""
    return await _call_llm(
        context, question,
        model=DEEPSEEK_MODEL,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
    )


async def _call_groq(context: str, question: str) -> str:
    """Layer 3b: Groq/Llama3 (备用模型，美国节点，免费)"""
    return await _call_llm(
        context, question,
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL,
    )


# ============================================================
# 三层融合主搜索端点
# ============================================================

@app.on_event("startup")
async def startup():
    try:
        load_index()
    except Exception as e:
        print(f"WARNING: Index not loaded: {e}")


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "index_loaded": index_loaded,
        "num_chunks": len(chunks) if index_loaded else 0,
        "vocab_size": len(vocab) if index_loaded else 0,
        "groq_configured": bool(GROQ_API_KEY),
        "version": "2.1.0",
    }


@app.get("/rag-api/search")
@app.get("/api/rag-api/search")
async def search(q: str = Query(..., min_length=1, max_length=500, description="Player question")):
    """
    三层架构融合搜索:
    1. Layer 1: TF-IDF 检索本地攻略
    2. Layer 2: RAG 弱时自动查 OSRS Wiki
    3. Layer 3: DeepSeek 生成 → 失败则 GPT-4o-mini 兜底
    """
    if not index_loaded:
        try:
            load_index()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Index unavailable: {e}")

    query = q.strip()
    if not query:
        return {"answer": "Ask me anything about Old School RuneScape!", "source": "system"}

    # ===== Layer 1: 本地 RAG 检索 =====
    wiki_context = None
    rag_context = ""
    max_similarity = 0.0

    try:
        query_vec = _tfidf_query_vector(query)
        similarities = _cosine_similarity(query_vec, tfidf_matrix)
        top_indices = np.argsort(similarities)[-TOP_K:][::-1]

        relevant = [
            (int(i), float(similarities[i]))
            for i in top_indices
            if float(similarities[i]) > MIN_SIMILARITY
        ]

        if relevant:
            max_similarity = max(s for _, s in relevant)
            context_parts = []
            for i, sim in relevant:
                chunk = chunks[i]
                context_parts.append(
                    f"[Guide: {chunk['title']}]\n{chunk['text']}"
                )
            rag_context = "\n\n---\n\n".join(context_parts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {e}")

    # ===== Layer 2: OSRS Wiki 实时补充（始终并行查询） =====
    # Wiki 查询很快 (<1s)，始终补充以提升回答完整度
    wiki_context = await _query_wiki_layer(query)

    # ===== 合并上下文 =====
    if rag_context and wiki_context:
        # 两者都有：攻略为主，Wiki 补充
        combined_context = (
            f"=== OSRS Guru Guides ===\n{rag_context}\n\n"
            f"=== OSRS Wiki (supplementary) ===\n{wiki_context}"
        )
    elif rag_context:
        combined_context = rag_context
    elif wiki_context:
        combined_context = wiki_context
    else:
        return {
            "answer": (
                "I couldn't find relevant info about that. "
                "Try asking about OSRS skills, bosses, quests, or money-making — "
                "check osrsguru.com for the latest guides!"
            ),
            "source": "system",
        }

    # ===== Layer 3: 双模型生成 =====
    # 判断来源类型
    if rag_context and wiki_context:
        source = "osrsguru_wiki"
    elif rag_context:
        source = "osrsguru_rag"
    else:
        source = "osrs_wiki"

    # 尝试 DeepSeek（主模型）
    try:
        answer = await _call_deepseek(combined_context, query)
        return {
            "answer": answer,
            "source": source,
            "model": "deepseek",
            "chunks_used": len(relevant) if rag_context else 0,
            "wiki_used": bool(wiki_context),
        }
    except Exception as e:
        print(f"[LLM] DeepSeek failed: {e}, trying GPT-4o-mini...")

    # DeepSeek 失败，尝试 Groq（美国备用）
    if GROQ_API_KEY:
        try:
            answer = await _call_groq(combined_context, query)
            return {
                "answer": answer,
                "source": source,
                "model": "groq-llama3",
                "chunks_used": len(relevant) if rag_context else 0,
                "wiki_used": bool(wiki_context),
            }
        except Exception as e:
            print(f"[LLM] Groq also failed: {e}")

    # 两个模型都失败了，返回原文
    fallback_text = rag_context or wiki_context or "No info found."
    return {
        "answer": (
            f"⚠️ AI services are temporarily unavailable. "
            f"Here's the most relevant info:\n\n{fallback_text[:500]}..."
        ),
        "source": "osrsguru_fallback",
    }
