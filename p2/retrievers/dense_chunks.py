"""Ablation of dense: chunks of 600 words with 100 words of overlap (dense uses [chunking] in p2.toml: 300 and 50).

Everything else is dense: bge-small-en-v1.5, cosine similarity, a document scores its best chunk.
The model truncates its input at 512 tokens, so about the first 365 words of each chunk are embedded.
"""

from p2.retrievers import dense

NEEDS_CLAUDE = False
BASE = "dense"

CHUNK_WORDS = 600
CHUNK_OVERLAP = 100


def build(corpus, cfg):
    return dense.Dense(corpus, cfg.replace(chunk_words=CHUNK_WORDS, chunk_overlap=CHUNK_OVERLAP))
