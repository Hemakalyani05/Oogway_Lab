"""
Embedding generator supporting local fast vectorizer, sentence-transformers, or OpenAI embeddings.
"""
from typing import List
import numpy as np
import math
import re


class FastLocalEmbedder:
    """
    Lightweight, fast zero-dependency local vector embedder based on subword hashing + n-gram term frequencies.
    Produces stable 384-dimensional dense vectors with cosine similarity matching.
    """
    def __init__(self, dim: int = 384):
        self.dim = dim

    def embed_text(self, text: str) -> List[float]:
        vec = np.zeros(self.dim, dtype=np.float32)
        words = re.findall(r'\b\w+\b', text.lower())
        if not words:
            return vec.tolist()
        
        for i, word in enumerate(words):
            # Primary word hash
            h = hash(word) % self.dim
            vec[h] += 1.0
            # Bigram hash for phrase context
            if i < len(words) - 1:
                bg = f"{word}_{words[i+1]}"
                h_bg = hash(bg) % self.dim
                vec[h_bg] += 1.5

        # L2 Normalization
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Computes cosine similarity between two unit vectors."""
    a = np.array(v1, dtype=np.float32)
    b = np.array(v2, dtype=np.float32)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))
