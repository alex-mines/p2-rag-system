"""Hybrid retrieval: reciprocal rank fusion (RRF, k = 60) of bm25 and dense.

Ported from the 13 lab's pipeline.py (rrf, command_fuse). Each document scores the sum of
1 / (K + rank) over the two rankings, ranks counted from 1, and the fused documents are ordered by
that score, equal scores in document id order.

Both systems are asked for every document, not their top 10: a document 11th in both lists can
belong in the fused top 10. search_chunks fuses the chunk rankings the same way, for `p2 answer`.
"""

from p2 import retrievers
from p2.runfile import order

NEEDS_CLAUDE = False

K = 60
PARTS = ("bm25", "dense")


def fuse(rankings: list[list[tuple[str, float]]]) -> list[tuple[str, float]]:
    """RRF over full rankings, each a list of (id, score) best first."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, (item, _score) in enumerate(ranking, 1):
            scores[item] = scores.get(item, 0.0) + 1.0 / (K + rank)
    return order(scores.items())


class Hybrid:
    def __init__(self, corpus, cfg):
        self.parts = [retrievers.build(name, corpus, cfg) for name in PARTS]
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(self.parts[0].chunks)

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        return fuse([p.search(text, self.n_docs) for p in self.parts])[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        return fuse([p.search_chunks(text, self.n_chunks) for p in self.parts])[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
