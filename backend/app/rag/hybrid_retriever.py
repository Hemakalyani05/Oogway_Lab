"""
Hybrid RAG Retriever combining Dense Cosine Vector Similarity and BM25 Sparse Keyword Ranking via Reciprocal Rank Fusion (RRF).
"""
import math
import re
from typing import List, Dict, Any, Optional

from app.rag.embeddings import FastLocalEmbedder, cosine_similarity
from app.core.logging import logger


class BM25Retriever:
    """Lightweight pure-python BM25 keyword ranker."""
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus: List[Dict[str, Any]] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_freqs: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b\w+\b', text.lower())

    def index(self, documents: List[Dict[str, Any]]):
        self.corpus = documents
        self.doc_lengths = []
        self.doc_freqs = {}
        num_docs = len(documents)

        if num_docs == 0:
            return

        for doc in documents:
            tokens = self._tokenize(doc["content"])
            self.doc_lengths.append(len(tokens))
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.doc_freqs[token] = self.doc_freqs.get(token, 0) + 1

        self.avg_doc_len = sum(self.doc_lengths) / max(num_docs, 1)

        # Calculate IDF
        for token, df in self.doc_freqs.items():
            self.idf[token] = math.log((num_docs - df + 0.5) / (df + 0.5) + 1.0)

    def score(self, query: str) -> List[float]:
        query_tokens = self._tokenize(query)
        scores = [0.0] * len(self.corpus)

        for i, doc in enumerate(self.corpus):
            tokens = self._tokenize(doc["content"])
            doc_len = self.doc_lengths[i]
            token_counts: Dict[str, int] = {}
            for t in tokens:
                token_counts[t] = token_counts.get(t, 0) + 1

            doc_score = 0.0
            for qt in query_tokens:
                if qt in token_counts:
                    freq = token_counts[qt]
                    idf = self.idf.get(qt, 0.1)
                    numerator = freq * (self.k1 + 1)
                    denominator = freq + self.k1 * (1 - self.b + self.b * (doc_len / max(self.avg_doc_len, 1.0)))
                    doc_score += idf * (numerator / max(denominator, 1e-6))
            scores[i] = doc_score

        return scores


class HybridRetriever:
    """
    Hybrid Retriever integrating Dense vector embeddings and BM25 sparse keyword ranking
    with Reciprocal Rank Fusion (RRF).
    """
    def __init__(self):
        self.embedder = FastLocalEmbedder()
        self.bm25 = BM25Retriever()
        self.documents: List[Dict[str, Any]] = []
        self.embeddings: List[List[float]] = []

    def load_documents(self, documents: List[Dict[str, Any]]):
        self.documents = documents
        logger.info(f"Indexing {len(documents)} transcript chunks into Hybrid Retriever...")
        self.bm25.index(documents)
        self.embeddings = [self.embedder.embed_text(d["content"]) for d in documents]
        logger.info("Hybrid index build complete.")

    def search(self, query: str, top_k: int = 5, rrf_k: int = 60) -> List[Dict[str, Any]]:
        if not self.documents:
            return []

        # 1. BM25 Sparse Ranking
        bm25_scores = self.bm25.score(query)
        bm25_ranked_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)

        # 2. Dense Vector Ranking
        query_vec = self.embedder.embed_text(query)
        dense_scores = [cosine_similarity(query_vec, doc_vec) for doc_vec in self.embeddings]
        dense_ranked_indices = sorted(range(len(dense_scores)), key=lambda i: dense_scores[i], reverse=True)

        # 3. Reciprocal Rank Fusion (RRF)
        rrf_scores: Dict[int, float] = {}

        for rank, idx in enumerate(bm25_ranked_indices[:top_k * 3]):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + (1.0 / (rrf_k + rank + 1))

        for rank, idx in enumerate(dense_ranked_indices[:top_k * 3]):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + (1.0 / (rrf_k + rank + 1))

        # Sort by final fused RRF score
        sorted_indices = sorted(rrf_scores.keys(), key=lambda idx: rrf_scores[idx], reverse=True)

        results = []
        for idx in sorted_indices[:top_k]:
            doc = dict(self.documents[idx])
            doc["score"] = round(rrf_scores[idx], 4)
            doc["dense_similarity"] = round(dense_scores[idx], 4)
            doc["bm25_score"] = round(bm25_scores[idx], 4)
            results.append(doc)

        return results


# Global singleton instance
hybrid_retriever = HybridRetriever()
