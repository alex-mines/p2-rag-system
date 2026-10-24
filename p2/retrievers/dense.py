"""Dense retrieval: embed every chunk once with bge-small-en-v1.5, embed the query, rank chunks by cosine similarity.

Ported from the 12 lab's retrieve.py (load_bge, cached_doc_vectors, dense_rankings): vectors have length 1,
so one matrix product gives every cosine similarity. The lab embedded whole articles; here the unit is the
chunk from [chunking] in p2.toml, and ChunkScorer lifts chunk scores to documents (a document scores its best chunk).

The model is bge-small-en-v1.5 unless p2.toml has a [dense] table with model = "..." (potion: embed.POTION).
No query instruction prefix, as in the lab's default bge arm.
"""

from p2 import embed
from p2.retrievers import ChunkScorer

NEEDS_CLAUDE = False


class Dense(ChunkScorer):
    def __init__(self, corpus, cfg):
        super().__init__(corpus, cfg)
        self.model = cfg.table("dense").get("model", embed.BGE)
        self.embedder = embed.load(self.model)
        self.vectors = embed.doc_vectors(self.embedder, [c.text for c in self.chunks], cfg.root)

    def score_chunks(self, text: str) -> list[float]:
        if not len(self.vectors):
            return []
        query = self.embedder.encode([text])[0]
        return (self.vectors @ query).tolist()


def build(corpus, cfg):
    return Dense(corpus, cfg)
