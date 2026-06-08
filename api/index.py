"""
OSRS Guru RAG API
Vercel serverless FastAPI 应用，为 OSRS AI 问答浮窗提供后端服务。
纯 numpy 实现 TF-IDF 检索（无需 scikit-learn），轻量部署。

端点:
    GET /api/rag-api/search?q=<question>
    返回: {"answer": "...", "source": "osrsguru_rag"}

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

# ========== 配置 ==========
DATA_DIR = Path(__file__).parent.parent / "data"
DEEPSEEK_API_KEY = os.environ.get(
    "DEEPSEEK_API_KEY",
    "sk-c08d3179018b44d7b150f54af4a82b1b",
)
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

TOP_K = 5
MIN_SIMILARITY = 0.05
TOP_N_TERMS = 50  # 查询时每词取 top-N 最重要 term

# ========== FastAPI 应用 ==========
app = FastAPI(
    title="OSRS Guru RAG API",
    description="RAG API for osrsguru.com AI Q&A Widget",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 全局状态 ==========
chunks: list[dict] = []
vocab: dict[str, dict] = {}       # {word: {idf, index}}
tfidf_matrix: np.ndarray = None   # (n_chunks, n_features) float32
index_loaded = False


def _tokenize(text: str) -> list[str]:
    """简单分词（与 sklearn TfidfVectorizer 默认行为一致：1-2 gram）"""
    text = text.lower()
    # 保留字母数字和空格
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    words = [w for w in text.split() if len(w) > 1]
    # Unigrams + bigrams
    tokens = words.copy()
    for i in range(len(words) - 1):
        tokens.append(f"{words[i]} {words[i+1]}")
    return tokens


def _tfidf_query_vector(query: str) -> np.ndarray:
    """
    纯 numpy 实现 TF-IDF 查询向量。
    不需要 sklearn — 用 vocab.json 中的 IDF 值。
    """
    n_features = len(vocab)
    vec = np.zeros(n_features, dtype=np.float32)
    tokens = _tokenize(query)

    # 计算词频 (TF)
    tf = {}
    for t in tokens:
        if t in vocab:
            tf[t] = tf.get(t, 0) + 1

    if not tf:
        return vec

    # TF-IDF = TF * IDF（与 indexer 的 sublinear_tf=False 保持一致）
    for term, count in tf.items():
        entry = vocab[term]
        idx = entry["index"]
        # 对查询也应用 sublinear TF
        tf_val = 1 + math.log(count) if count > 0 else 0
        vec[idx] = tf_val * entry["idf"]

    # L2 归一化
    norm = np.linalg.norm(vec)
    if norm > 1e-10:
        vec = vec / norm

    return vec


def _cosine_similarity(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """纯 numpy 余弦相似度"""
    # matrix 已 L2 归一化 (sklearn 默认)，query_vec 也已归一化
    # 直接点积即得余弦相似度
    return np.dot(matrix, query_vec)


def load_index():
    """加载预计算的索引数据（无需 sklearn）"""
    global chunks, vocab, tfidf_matrix, index_loaded

    if index_loaded:
        return

    try:
        # 加载 chunks
        chunks_path = DATA_DIR / "chunks.json"
        if not chunks_path.exists():
            raise FileNotFoundError(
                f"chunks.json not found at {chunks_path}. "
                f"Run: python rag_indexer.py"
            )
        with open(chunks_path, 'r', encoding='utf-8') as f:
            chunks.clear()
            chunks.extend(json.load(f))

        # 加载词表
        vocab_path = DATA_DIR / "vocab.json"
        if not vocab_path.exists():
            raise FileNotFoundError(
                f"vocab.json not found. Re-run rag_indexer.py to generate it."
            )
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab.clear()
            vocab.update(json.load(f))

        # 加载 TF-IDF matrix (支持 .npz 和 .npy)
        for ext in [".npz", ".npy"]:
            matrix_path = DATA_DIR / f"tfidf_matrix{ext}"
            if matrix_path.exists():
                break
        else:
            raise FileNotFoundError("tfidf_matrix.npz not found.")
        loaded = np.load(matrix_path)
        if hasattr(loaded, 'files'):
            tfidf_matrix = loaded[loaded.files[0]]  # npz format
        else:
            tfidf_matrix = loaded  # npy format

        index_loaded = True
        print(
            f"[OK] Index loaded: {len(chunks)} chunks, "
            f"{len(vocab)} vocab terms, "
            f"matrix {tfidf_matrix.shape}"
        )

    except Exception as e:
        print(f"[ERR] Failed to load index: {e}")
        raise


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
        "version": "1.1.0",
    }


@app.get("/rag-api/search")
@app.get("/api/rag-api/search")
async def search(q: str = Query(..., min_length=1, max_length=500, description="Player question")):
    """
    主搜索端点：
    1. 纯 numpy TF-IDF 检索最相关 chunks
    2. 上下文传递给 DeepSeek API 生成回答
    """
    if not index_loaded:
        try:
            load_index()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Index unavailable: {e}")

    query = q.strip()
    if not query:
        return {
            "answer": "Ask me anything about Old School RuneScape!",
            "source": "system",
        }

    # ===== Step 1: TF-IDF 检索 =====
    try:
        query_vec = _tfidf_query_vector(query)
        similarities = _cosine_similarity(query_vec, tfidf_matrix)

        # Top-K
        top_indices = np.argsort(similarities)[-TOP_K:][::-1]

        # 过滤
        relevant = [
            (int(i), float(similarities[i]))
            for i in top_indices
            if float(similarities[i]) > MIN_SIMILARITY
        ]

        if not relevant:
            return {
                "answer": (
                    "I couldn't find relevant info about that in our OSRS guides. "
                    "Try asking about skills, bosses, quests, or money-making — "
                    "check osrsguru.com for the latest guides!"
                ),
                "source": "system",
            }

        # 构建上下文
        context_parts = []
        for i, sim in relevant:
            chunk = chunks[i]
            context_parts.append(f"[Guide: {chunk['title']}]\n{chunk['text']}")
        context = "\n\n---\n\n".join(context_parts)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {e}")

    # ===== Step 2: 调用 DeepSeek 生成回答 =====
    try:
        answer = await _call_deepseek(context, query)
        return {
            "answer": answer,
            "source": "osrsguru_rag",
            "chunks_used": len(relevant),
        }
    except Exception as e:
        print(f"DeepSeek API error: {e}")
        # Fallback: 返回最匹配的原文片段
        best = context_parts[0] if context_parts else "No info found."
        return {
            "answer": (
                f"⚠️ AI is temporarily unavailable. "
                f"Here's the most relevant guide snippet:\n\n{best[:500]}..."
            ),
            "source": "osrsguru_fallback",
        }


async def _call_deepseek(context: str, question: str) -> str:
    """调用 DeepSeek API (OpenAI-compatible)"""
    system_prompt = (
        "You are OSRS Guru AI, the AI assistant for osrsguru.com — "
        "the best Old School RuneScape guide site.\n\n"
        "RULES:\n"
        "1. Answer ONLY from the provided context. No outside knowledge.\n"
        "2. If context lacks the answer, say: 'I don't have enough info on that "
        "yet. Check osrsguru.com for the latest guides!'\n"
        "3. Keep answers CONCISE (150-300 words) and ACTIONABLE.\n"
        "4. Use OSRS terms correctly (gp, Ranged, Defence, PK, PvM, etc.).\n"
        "5. Mention the guide title(s) you reference.\n"
        "6. Be friendly — OSRS players appreciate the grind!"
    )

    user_prompt = (
        f"OSRS Guru Knowledge Base:\n{context}\n\n"
        f"Player Question: {question}\n\n"
        f"Answer based on the guides above:"
    )

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": DEEPSEEK_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.3,
                "max_tokens": 600,
            },
        )

        if response.status_code != 200:
            raise Exception(
                f"DeepSeek API {response.status_code}: {response.text[:200]}"
            )

        data = response.json()
        return data["choices"][0]["message"]["content"]
