"""
OSRS Guru RAG Indexer — ChromaDB内置Embedding
向量化 115 篇攻略 → ChromaDB
运行: python rag_indexer.py
"""

import os, re
from pathlib import Path
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

load_dotenv()

GUIDES_DIR = Path(os.getenv("GUIDES_DIR", "C:/Users/Lenovo/osrs-guide-site/guides"))
CHROMA_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"))

# 使用 ChromaDB 内置免费 embedding (all-MiniLM-L6-v2, 无需API key)
# pip install chromadb 自带，首次运行自动下载模型 (~80MB)
from chromadb.utils import embedding_functions
ef = embedding_functions.DefaultEmbeddingFunction()
def get_emb(text): return ef([text])[0].tolist()

def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    # 移除 HTML 标签
    for selector in ["header","footer","nav","script","style",
                     ".support-card",".inline-support-hint",".breadcrumb",
                     ".article-meta",".site-header",".site-footer"]:
        for el in soup.select(selector):
            if el: el.decompose()
    text = soup.get_text(separator="\n")
    text = re.sub(r'\n{3,}','\n\n',text).strip()
    text = re.sub(r'[ \t]+',' ',text)
    return text[:3000]

def index_all_guides():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    try: client.delete_collection("osrs_guides")
    except: pass

    collection = client.create_collection(
        name="osrs_guides", metadata={"description":"OSRS Guru Guides"})

    files = sorted(GUIDES_DIR.glob("*.html"))
    print(f"Found {len(files)} guides")

    docs, ids, metas, embs = [], [], [], []
    for i, f in enumerate(files):
        try:
            text = extract_text(f.read_text(encoding="utf-8"))
            if len(text) < 300: continue
            print(f"  [{i+1}/{len(files)}] {f.name}")
            emb = get_emb(text)
            docs.append(text); ids.append(f.stem); metas.append({"file": f.name}); embs.append(emb)
        except Exception as e:
            print(f"  skip {f.name}: {e}")

    print(f"\nStoring {len(docs)} docs...")
    for i in range(0, len(docs), 50):
        end = min(i+50, len(docs))
        collection.add(documents=docs[i:end], embeddings=embs[i:end], ids=ids[i:end], metadatas=metas[i:end])
        print(f"  {end}/{len(docs)}")

    print(f"Done! {collection.count()} guides indexed")

if __name__ == "__main__":
    index_all_guides()
