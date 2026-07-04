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
async def call_deepseek(prompt: str, game: str = "osrs") -> str:
    """根据游戏选择系统提示词"""
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        )
        # 根据游戏选择系统提示
        system_prompts = {
            "osrs": "You are an OSRS (Old School RuneScape) expert assistant. Answer accurately, concisely, based on game facts. Use English.",
            "crimson-desert": "You are a Crimson Desert (2026 action RPG by Pearl Abyss) expert assistant. Answer accurately about combat, quests, weapons, skills, bosses. Use English.",
            "windrose": "You are a Windrose (2026 pirate survival game) expert assistant. Answer accurately about survival, ship combat, crafting, exploration, bosses. Use English.",
        }
        system_content = system_prompts.get(game, system_prompts["osrs"])

        resp = await client.chat.completions.create(
            model=os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash"),
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ], max_tokens=500, temperature=0.3
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        print(f"DeepSeek error: {e}")
        return ""

async def call_gpt4o_mini(prompt: str) -> str:
    return ""

# ============================================================
# Core RAG Query — 三层融合
# ============================================================
async def rag_query(question: str, game: str = "osrs") -> dict:
    """多游戏支持：OSRS用Wiki+DeepSeek，CD/WR直接用DeepSeek"""
    source = "unknown"
    answer = ""

    # 非OSRS游戏：跳过Wiki，直接用DeepSeek
    if game and game != "osrs":
        try:
            ds_answer = await call_deepseek(question, game)
            if ds_answer:
                return {"answer": ds_answer, "source": "deepseek", "game": game}
        except Exception as e:
            print(f"DeepSeek error for {game}: {e}")
        return {
            "answer": f"Sorry, I could not find an answer about {game}. Please browse osrsguru.com/guides/{game}/ for guides.",
            "source": "fallback",
            "game": game
        }

    # OSRS：Layer 1: OSRS Wiki API
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
        ds_answer = await call_deepseek(question, "osrs")
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
async def search(q: str = Query(..., description="搜索问题"), game: Optional[str] = Query(None, description="游戏类型: osrs/crimson-desert/windrose")):
    result = await rag_query(q, game or "osrs")
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
# Payment Verification — PayPal Subscription Check
# ============================================================
PAYPAL_API = os.getenv("PAYPAL_API", "https://api-m.paypal.com")  # sandbox: api-m.sandbox.paypal.com
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "")
PAYPAL_TOKEN_CACHE = {"token": None, "expires_at": 0}

async def get_paypal_token() -> Optional[str]:
    """Get PayPal OAuth 2.0 access token."""
    now = __import__("time").time()
    if PAYPAL_TOKEN_CACHE["token"] and now < PAYPAL_TOKEN_CACHE["expires_at"]:
        return PAYPAL_TOKEN_CACHE["token"]
    if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
        return None
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{PAYPAL_API}/v1/oauth2/token",
                data={"grant_type": "client_credentials"},
                auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET),
                headers={"Accept": "application/json"}
            )
            if resp.status_code == 200:
                data = resp.json()
                PAYPAL_TOKEN_CACHE["token"] = data["access_token"]
                PAYPAL_TOKEN_CACHE["expires_at"] = now + data.get("expires_in", 30000) - 60
                return data["access_token"]
    except Exception as e:
        print(f"PayPal token error: {e}")
    return None

@app.get("/api/payment/verify/{subscription_id}")
async def verify_paypal_subscription(subscription_id: str):
    """
    Verify PayPal subscription status via PayPal REST API.
    Returns: { verified: bool, status: str, subscription_id: str }
    """
    # Return pending if no PayPal credentials configured
    token = await get_paypal_token()
    if not token:
        return JSONResponse({
            "verified": False,
            "status": "unconfigured",
            "subscription_id": subscription_id,
            "message": "Payment verification not configured yet. Contact support@osrsguru.com"
        }, status_code=200)

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                f"{PAYPAL_API}/v1/billing/subscriptions/{subscription_id}",
                headers={"Authorization": f"Bearer {token}", "Accept": "application/json"}
            )
            if resp.status_code == 200:
                data = resp.json()
                status = data.get("status", "").lower()  # ACTIVE, APPROVAL_PENDING, CANCELLED, etc.
                is_active = status in ("active", "approved")
                return {
                    "verified": is_active,
                    "status": status,
                    "subscription_id": subscription_id,
                    "plan_id": data.get("plan_id", ""),
                    "start_time": data.get("start_time", ""),
                    "next_billing_time": data.get("billing_info", {}).get("next_billing_time", ""),
                    "payer_email": data.get("subscriber", {}).get("email_address", "")
                }
            elif resp.status_code == 404:
                return {"verified": False, "status": "not_found", "subscription_id": subscription_id}
            else:
                return {"verified": False, "status": "error", "subscription_id": subscription_id,
                        "paypal_code": resp.status_code}
    except Exception as e:
        return {"verified": False, "status": "error", "subscription_id": subscription_id,
                "message": str(e)}

# ============================================================
# Run: uvicorn main:app --host 0.0.0.0 --port 8000
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
