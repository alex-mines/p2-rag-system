"""Rerank: ask Claude to reorder the top 20 of hybrid (bm25 + dense, RRF), one claude -p call per query.

Ported from the 13 lab's pipeline.py (rerank_one, RERANK_SCHEMA, command_rerank):
- the first stage's top 20 go to Claude as numbered passages, each cut to PASSAGE_CHARS characters;
- the reply is forced into {"order": [20 integers]} and must be each of 1 to 20 once, else the
  first-stage order is kept for that query (a warning goes to stderr);
- results below the 20 keep their first-stage order underneath. The reranker can only reorder its 20
  candidates, so a relevant document outside them is not rescued.

Changes from the lab: the schema also bounds each number to 1..20 (the lab's only fixed the count); the
prompt describes 30 CFR sections and the brief's relevance rule instead of help-center articles; the
call goes through p2.claude.call, which caches replies and records tokens in the trace; and
search_chunks reranks the first stage's top 20 chunks the same way, for `p2 answer`.
"""

import sys

from p2 import claude, retrievers

NEEDS_CLAUDE = True

FIRST_STAGE = "hybrid"
CANDIDATES = 20
PASSAGE_CHARS = 2000
OWN_PASSAGE_CHARS = 6000  # own corpus: documents are 5-page parts of about 15,000 characters. Known flaw: for 8 of 55 queries (h09, h10, c12, c13, c17, c27, c38, c41) the answer sits past character 6,000 in every relevant part, so the reranker cannot see it; 6 of the 7 queries where rerank ranks below hybrid are among them. A 12,000 character trial on those 8 raised their MRR@10 from 0.480 to 0.812 (scratch run, not committed).

SCHEMA = {
    "type": "object",
    "properties": {
        "order": {
            "type": "array",
            "items": {"type": "integer", "minimum": 1, "maximum": CANDIDATES},
            "minItems": CANDIDATES,
            "maxItems": CANDIDATES,
        }
    },
    "required": ["order"],
}

PROMPT = """Below are {n} passages from the US federal mine safety and health regulations (30 CFR), numbered 1 to {n}, and a search query.
A passage is relevant when it states the requirement the query asks about. When the query does not name a kind of mine, the parallel sections in parts 56, 57, 75 and 77 that state the same rule are all relevant. A passage that only cross-references the requirement is not relevant.
Order the passages from the most relevant to the least relevant.
Reply with all {n} passage numbers, each exactly once, best first.

Query: {query}

{passages}"""

# The own corpus (USGS reports on Colorado water): the relevance rule is the student's, also used for the gold set.
OWN_PROMPT = """Below are {n} passages from U.S. Geological Survey reports on Colorado water resources, numbered 1 to {n}, and a search query.
Relevance rule: the relevant section should give a reader all of the supporting evidence needed to justify the claim made in answer to the question posed. The reader should be able to look at a portion of the text and say yes this connects to my question directly.
Order the passages from the most relevant to the least relevant.
Reply with all {n} passage numbers, each exactly once, best first.

Query: {query}

{passages}"""


def rerank(cfg, query: str, candidates: list[tuple[str, str]], corpus_name: str = "shared") -> list[int]:
    """Indexes into `candidates` (id, text), best first; the original order if the reply is unusable."""
    n = len(candidates)
    keep = list(range(n))
    chars = OWN_PASSAGE_CHARS if corpus_name == "own" else PASSAGE_CHARS
    passages = "\n\n".join(f"[{i}] {text[:chars]}" for i, (_id, text) in enumerate(candidates, 1))
    prompt = OWN_PROMPT if corpus_name == "own" else PROMPT
    reply = claude.call(prompt.format(n=n, query=query, passages=passages), schema(n), model=cfg.model, cache_dir=claude.cache_folder(cfg))
    if reply.error:
        print(f"rerank: {reply.error}; kept the first-stage order for: {query[:60]}", file=sys.stderr)
        return keep
    order = reply.output.get("order")
    if not isinstance(order, list) or sorted(order) != list(range(1, n + 1)):
        print(f"rerank: the reply was not each of 1 to {n} once; kept the first-stage order for: {query[:60]}", file=sys.stderr)
        return keep
    return [i - 1 for i in order]


def schema(n: int) -> dict:
    if n == CANDIDATES:
        return SCHEMA
    items = {"type": "integer", "minimum": 1, "maximum": n}
    return {"type": "object", "properties": {"order": {"type": "array", "items": items, "minItems": n, "maxItems": n}}, "required": ["order"]}


def lift(reranked: list[str], rest: list[str]) -> list[tuple[str, float]]:
    """Ids best first with strictly falling scores 1/rank, so the order is exactly the one given."""
    return [(item, 1.0 / rank) for rank, item in enumerate(reranked + rest, 1)]


class Rerank:
    model = None

    def __init__(self, corpus, cfg):
        self.corpus = corpus
        self.cfg = cfg
        self.first = retrievers.build(FIRST_STAGE, corpus, cfg)
        self.chunk_text = {c.id: c.text for c in self.first.parts[0].chunks}
        self.model = cfg.model

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        first = [d for d, _ in self.first.search(text, max(k, CANDIDATES))]
        top, rest = first[:CANDIDATES], first[CANDIDATES:]
        if top:
            top = [top[i] for i in rerank(self.cfg, text, [(d, self.corpus.docs[d].text) for d in top], self.corpus.name)]
        return lift(top, rest)[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        first = [c for c, _ in self.first.search_chunks(text, max(k, CANDIDATES))]
        top, rest = first[:CANDIDATES], first[CANDIDATES:]
        if top:
            top = [top[i] for i in rerank(self.cfg, text, [(c, self.chunk_text[c]) for c in top], self.corpus.name)]
        return lift(top, rest)[:k]


def build(corpus, cfg):
    return Rerank(corpus, cfg)
