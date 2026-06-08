"""
OSRS Guru RAG Indexer
解析所有攻略 HTML 文件，提取文本内容，构建 TF-IDF 向量索引和稠密向量嵌入。
供 Vercel RAG API 使用。

用法:
    python rag_indexer.py              # 完整索引（TF-IDF + dense embeddings）
    python rag_indexer.py --tfidf-only # 仅 TF-IDF（轻量，适合 Vercel）
"""

import os
import re
import json
import pickle
import argparse
import numpy as np
from pathlib import Path
from html.parser import HTMLParser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ========== 配置 ==========
GUIDES_DIR = Path(__file__).parent / "guides"
DATA_DIR = Path(__file__).parent / "data"
CHUNK_SIZE = 500       # 每个 chunk 的字符数
CHUNK_OVERLAP = 100    # chunk 之间的重叠字符数
TOP_N_KEYWORDS = 2000  # TF-IDF 最大特征数


class HTMLTextExtractor(HTMLParser):
    """从 HTML 中提取纯文本，跳过脚本/样式/导航等非内容标签"""

    SKIP_TAGS = {'script', 'style', 'nav', 'header', 'footer', 'noscript', 'code', 'pre'}
    INLINE_TAGS = {'a', 'span', 'strong', 'em', 'b', 'i', 'u', 'code', 'small', 'mark', 'sub', 'sup'}

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_depth = 0
        self.inline_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
        elif tag in self.INLINE_TAGS:
            self.inline_depth += 1
        elif self.skip_depth == 0:
            self.text_parts.append(' ')

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self.skip_depth > 0:
            self.skip_depth -= 1
        elif tag in self.INLINE_TAGS and self.inline_depth > 0:
            self.inline_depth -= 1
        elif tag in {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'tr', 'div', 'section', 'article'}:
            if self.skip_depth == 0:
                self.text_parts.append('\n')

    def handle_data(self, data):
        if self.skip_depth == 0:
            text = data.strip()
            if text:
                self.text_parts.append(text)
                self.text_parts.append(' ')

    def get_text(self) -> str:
        raw = ''.join(self.text_parts)
        # 清理多余空白
        raw = re.sub(r'\n\s*\n', '\n\n', raw)
        raw = re.sub(r' {2,}', ' ', raw)
        raw = re.sub(r'\n +', '\n', raw)
        return raw.strip()


def extract_faq_from_html(html_content: str) -> list[dict]:
    """提取 FAQPage 结构化数据中的 Q&A"""
    faqs = []
    # 匹配 JSON-LD 中的 FAQPage
    pattern = r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>'
    for match in re.finditer(pattern, html_content, re.DOTALL):
        try:
            data = json.loads(match.group(1))
            if isinstance(data, dict) and data.get('@type') == 'FAQPage':
                for item in data.get('mainEntity', []):
                    q = item.get('name', '')
                    a = item.get('acceptedAnswer', {}).get('text', '')
                    if q and a:
                        faqs.append({'question': q, 'answer': a})
            # 处理 @graph 格式
            elif isinstance(data, dict) and '@graph' in data:
                for node in data['@graph']:
                    if node.get('@type') == 'FAQPage':
                        for item in node.get('mainEntity', []):
                            q = item.get('name', '')
                            a = item.get('acceptedAnswer', {}).get('text', '')
                            if q and a:
                                faqs.append({'question': q, 'answer': a})
        except (json.JSONDecodeError, KeyError):
            continue
    return faqs


def extract_guide_content(filepath: Path) -> dict:
    """解析单个攻略文件，返回结构化数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 提取标题
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    title = title_match.group(1) if title_match else filepath.stem
    # 清理标题（移除 "| OSRS Guru" 等后缀）
    title = re.sub(r'\s*[|–—\-]\s*OSRS Guru.*$', '', title).strip()

    # 提取 meta description
    desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
    description = desc_match.group(1) if desc_match else ''

    # 提取正文
    extractor = HTMLTextExtractor()
    extractor.feed(html)
    text = extractor.get_text()

    # 提取 FAQ
    faqs = extract_faq_from_html(html)

    # 提取类别标签（从面包屑导航中提取）
    category = 'general'
    breadcrumb_match = re.search(
        r'breadcrumb[^>]*>.*?<a[^>]*href="[^"]*">([^<]+)</a>\s*/\s*<a[^>]*href="[^"]*">([^<]+)</a>',
        html
    )
    if breadcrumb_match:
        crumb = breadcrumb_match.group(2).lower()
        if 'boss' in crumb:
            category = 'boss'
        elif 'money' in crumb:
            category = 'money-making'
        elif 'quest' in crumb:
            category = 'quest'
        elif 'skill' in crumb or 'training' in crumb:
            category = 'skill-training'

    # 备用：从标题推断
    if category == 'general':
        title_lower = title.lower()
        if 'boss' in title_lower or 'fight caves' in title_lower or 'jad' in title_lower:
            category = 'boss'
        elif 'money' in title_lower or 'gp' in title_lower or 'flipping' in title_lower:
            category = 'money-making'
        elif 'quest' in title_lower:
            category = 'quest'
        elif '1-99' in title_lower or 'training' in title_lower or 'guide' in title_lower:
            category = 'skill-training'

    return {
        'title': title,
        'description': description,
        'text': text,
        'faqs': faqs,
        'category': category,
        'filename': filepath.name,
        'url': f'https://osrsguru.com/guides/{filepath.name}',
    }


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """将长文本分割为重叠的 chunks"""
    if len(text) <= chunk_size:
        return [text] if text.strip() else []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # 尝试在句子边界处截断
        if end < len(text):
            # 寻找最近的句号、问号、感叹号或换行
            for sep in ['. ', '? ', '! ', '\n', ' ']:
                last_sep = chunk.rfind(sep)
                if last_sep > chunk_size * 0.6:  # 至少保留 60%
                    end = start + last_sep + 1
                    chunk = text[start:end]
                    break

        chunk = chunk.strip()
        if chunk and len(chunk) > 50:  # 忽略太短的 chunk
            chunks.append(chunk)

        start = end - overlap
        if start >= len(text):
            break

    return chunks


def build_index(tfidf_only: bool = False):
    """主索引构建函数"""
    print("=" * 60)
    print("OSRS Guru RAG Indexer")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # ========== 第一步：解析所有攻略 ==========
    print("\n[1/4] Parsing guide HTML files...")
    guide_files = sorted(GUIDES_DIR.glob("*.html"))
    print(f"  Found {len(guide_files)} HTML files")

    all_chunks = []
    faq_count = 0

    for i, filepath in enumerate(guide_files):
        try:
            guide = extract_guide_content(filepath)
            text = guide['text']

            if not text or len(text) < 100:
                print(f"  [SKIP] {filepath.name} (too little content: {len(text)} chars)")
                continue

            # 为正文分块
            text_chunks = chunk_text(text)
            for j, chunk in enumerate(text_chunks):
                all_chunks.append({
                    'text': chunk,
                    'title': guide['title'],
                    'url': guide['url'],
                    'category': guide['category'],
                    'chunk_index': j,
                    'type': 'content',
                })

            # 添加 FAQ 作为独立 chunks（高质量 Q&A 对）
            for faq in guide['faqs']:
                all_chunks.append({
                    'text': f"Q: {faq['question']}\nA: {faq['answer']}",
                    'title': guide['title'],
                    'url': guide['url'],
                    'category': guide['category'],
                    'chunk_index': -1,
                    'type': 'faq',
                })
                faq_count += 1

            if (i + 1) % 20 == 0:
                print(f"  Processed {i + 1}/{len(guide_files)} files...")
        except Exception as e:
            print(f"  [ERR] {filepath.name}: {e}")

    print(f"  [OK] Parsed {len(guide_files)} files -> {len(all_chunks)} chunks ({faq_count} FAQ pairs)")

    # ========== 第二步：构建 TF-IDF ==========
    print("\n[2/4] Building TF-IDF vectorizer...")
    texts = [c['text'] for c in all_chunks]

    vectorizer = TfidfVectorizer(
        max_features=TOP_N_KEYWORDS,
        stop_words='english',
        ngram_range=(1, 2),
        sublinear_tf=True,
    )
    tfidf_matrix = vectorizer.fit_transform(texts)
    print(f"  [OK] TF-IDF matrix: {tfidf_matrix.shape[0]} chunks x {tfidf_matrix.shape[1]} features")

    # ========== 第三步：保存数据 ==========
    print("\n[3/4] Saving index data...")

    # 保存 chunks
    chunks_path = DATA_DIR / "chunks.json"
    with open(chunks_path, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    print(f"  [OK] Saved {len(all_chunks)} chunks -> {chunks_path}")

    # 保存 TF-IDF vectorizer
    vectorizer_path = DATA_DIR / "tfidf_vectorizer.pkl"
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"  [OK] Saved TF-IDF vectorizer -> {vectorizer_path}")

    # 保存 TF-IDF matrix (sparse → dense for Vercel compatibility)
    matrix_path = DATA_DIR / "tfidf_matrix.npz"
    tfidf_dense = tfidf_matrix.toarray().astype(np.float16)
    np.savez_compressed(matrix_path, matrix=tfidf_dense)
    print(f"  [OK] Saved TF-IDF matrix ({tfidf_dense.shape}) -> {matrix_path}")

    # 保存词表（供 Vercel API 无需 sklearn 即可做 TF-IDF 查询）
    vocab_path = DATA_DIR / "vocab.json"
    vocab_data = {
        word: {"idf": float(vectorizer.idf_[idx]), "index": int(idx)}
        for word, idx in vectorizer.vocabulary_.items()
    }
    with open(vocab_path, 'w', encoding='utf-8') as f:
        json.dump(vocab_data, f, ensure_ascii=False)
    print(f"  [OK] Saved vocabulary ({len(vocab_data)} terms) -> {vocab_path}")

    # 保存元数据
    meta = {
        'num_guides': len(guide_files),
        'num_chunks': len(all_chunks),
        'num_faqs': faq_count,
        'chunk_size': CHUNK_SIZE,
        'chunk_overlap': CHUNK_OVERLAP,
        'tfidf_features': TOP_N_KEYWORDS,
        'categories': list(set(c['category'] for c in all_chunks)),
    }
    with open(DATA_DIR / "meta.json", 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"  [OK] Saved metadata -> {DATA_DIR / 'meta.json'}")

    # ========== 第四步：构建稠密向量嵌入（可选） ==========
    if not tfidf_only:
        print("\n[4/4] Building dense embeddings with sentence-transformers...")
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
            emb_path = DATA_DIR / "embeddings.npy"
            np.save(emb_path, embeddings)
            print(f"  [OK] Saved dense embeddings ({embeddings.shape}) -> {emb_path}")
        except Exception as e:
            print(f"  [WARN] Dense embeddings failed (will use TF-IDF only): {e}")
    else:
        print("\n[4/4] Skipping dense embeddings (--tfidf-only)")

    # ========== 汇总 ==========
    print("\n" + "=" * 60)
    print("INDEXING COMPLETE")
    print("=" * 60)
    print(f"  Guides processed:  {len(guide_files)}")
    print(f"  Total chunks:      {len(all_chunks)}")
    print(f"  FAQ pairs:         {faq_count}")
    print(f"  Categories:        {meta['categories']}")
    print(f"  TF-IDF dims:       {tfidf_matrix.shape}")
    print(f"  Data saved to:     {DATA_DIR}")
    print("\n  Next: deploy api/ to Vercel, or run locally with:")
    print("    uvicorn api.index:app --reload --port 8000")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OSRS Guru RAG Indexer')
    parser.add_argument('--tfidf-only', action='store_true', help='Skip dense embeddings, build TF-IDF only')
    args = parser.parse_args()
    build_index(tfidf_only=args.tfidf_only)
