"""
OSRS Guru RAG API — FastAPI Backend
三层架构: RAG知识库 → OSRS Wiki API → DeepSeek/GPT-4o-mini
"""

import os
import json
import httpx
from pathlib import Path
from typing import Optional, List
from dotenv import load_dotenv

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

load_dotenv()

# ============================================================
# Config
# ============================================================
app = FastAPI(title="OSRS Guru RAG API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

GUIDES_DIR = Path(os.getenv("GUIDES_DIR", "../osrs-guide-site/guides"))
CHROMA_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"))
WIKI_API = "https://oldschool.runescape.wiki/api.php"
GE_API = "https://prices.runescape.wiki/api/v1/osrs"
WIKI_HEADERS = {"User-Agent": "OSRSGuru-RAG/1.0 (contact@osrsguru.com)"}

# ============================================================
# RAG Layer — ChromaDB 向量检索
# ============================================================
ef = None  # 延迟加载

def get_embedding_fn():
    global ef
    if ef is None:
        from chromadb.utils import embedding_functions
        ef = embedding_functions.DefaultEmbeddingFunction()
    return ef

def init_chroma():
    """延迟加载 ChromaDB"""
    import chromadb
    from chromadb.config import Settings
    return chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))

def get_rag_collection():
    client = init_chroma()
    return client.get_or_create_collection(
        name="osrs_guides",
        embedding_function=get_embedding_fn()
    )

def search_guides(query: str, n: int = 3) -> List[str]:
    """RAG 检索：ChromaDB 内置 embedding → 向量搜索"""
    try:
        collection = get_rag_collection()
        results = collection.query(query_texts=[query], n_results=n)
        return results.get("documents", [[]])[0] if results else []
    except Exception:
        return []

# ============================================================
# Layer 2 — OSRS Wiki API
# ============================================================
WIKI_CACHE = {}

async def search_wiki(query: str, limit: int = 3):
    if query in WIKI_CACHE:
        return WIKI_CACHE[query]
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(WIKI_API, params={
            "action": "query", "list": "search", "srsearch": query,
            "format": "json", "srlimit": limit
        }, headers=WIKI_HEADERS)
        data = resp.json()
        results = [{"title": r["title"], "snippet": r.get("snippet","")}
                   for r in data.get("query",{}).get("search",[])]
        WIKI_CACHE[query] = results
        return results

async def get_wiki_page(title: str) -> Optional[str]:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(WIKI_API, params={
            "action": "query", "prop": "extracts", "exintro": 1,
            "explaintext": 1, "titles": title, "format": "json"
        }, headers=WIKI_HEADERS)
        pages = resp.json().get("query",{}).get("pages",{})
        return next((p.get("extract","") for p in pages.values()), None)

async def search_item_price(item_name: str) -> Optional[dict]:
    """GE实时价格查询"""
    async with httpx.AsyncClient(timeout=15) as client:
        mapping_resp = await client.get(f"{GE_API}/mapping", headers=WIKI_HEADERS)
        mapping = {i["id"]: i["name"] for i in mapping_resp.json()}
        price_resp = await client.get(f"{GE_API}/latest", headers=WIKI_HEADERS)
        prices = price_resp.json().get("data", {})
    for item_id, name in mapping.items():
        if item_name.lower() in name.lower() and item_id in prices:
            return {
                "name": name, "buy_price": prices[item_id].get("low", 0),
                "sell_price": prices[item_id].get("high", 0),
                "item_id": item_id
            }
    return None

# ============================================================
# Layer 3 — LLM Fallback (DeepSeek + GPT-4o-mini)
# ============================================================
async def call_deepseek(prompt: str) -> str:
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        )
        resp = await client.chat.completions.create(
            model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            messages=[
                {"role": "system", "content": "你是OSRS专家助手。回答要精确、简洁、基于游戏事实。用英文回答。"},
                {"role": "user", "content": prompt}
            ], max_tokens=500, temperature=0.3
        )
        return resp.choices[0].message.content or ""
    except Exception:
        return ""

async def call_gpt4o_mini(prompt: str) -> str:
    return ""

# ============================================================
# Core RAG Query — 三层融合
# ============================================================
async def rag_query(question: str) -> dict:
    """Vercel-optimized: Wiki API → DeepSeek (skips heavy ChromaDB for serverless)"""
    source = "unknown"
    answer = ""

    # Layer 1: OSRS Wiki API (fast, no model needed)
    try:
        wiki_results = await search_wiki(question)
        if wiki_results:
            page = await get_wiki_page(wiki_results[0]["title"])
            if page and len(page) > 100:
                return {
                    "answer": page[:800],
                    "source": "osrs_wiki",
                    "wiki_title": wiki_results[0]["title"]
                }
    except Exception:
        pass

    # Layer 2: DeepSeek AI Fallback
    try:
        ds_answer = await call_deepseek(question)
        if ds_answer:
            return {"answer": ds_answer, "source": "deepseek"}
    except Exception:
        pass

    return {"answer": "Sorry, I could not find an answer. Please browse osrsguru.com for guides.", "source": "fallback"}

# ============================================================
# API Endpoints
# ============================================================
class SearchResponse(BaseModel):
    answer: str
    source: str
    wiki_title: Optional[str] = None

@app.get("/")
async def root():
    return {"service": "OSRS Guru RAG API", "version": "1.0", "status": "running"}

@app.get("/rag-api/search")
async def search(q: str = Query(..., description="搜索问题")):
    result = await rag_query(q)
    return result

@app.get("/rag-api/price")
async def price(item: str = Query(..., description="物品名称")):
    result = await search_item_price(item)
    if result:
        return {"found": True, **result}
    return {"found": False, "message": f"未找到 {item} 的价格"}

@app.get("/rag-api/health")
async def health():
    return {"status": "ok", "guides_indexed": get_rag_collection().count() if CHROMA_DIR.exists() else 0}

# ============================================================
# Run: uvicorn main:app --host 0.0.0.0 --port 8000
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
