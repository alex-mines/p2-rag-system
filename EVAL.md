# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.

**dense.** Embedding model: `BAAI/bge-small-en-v1.5` through fastembed (`p2.embed.load`), no query instruction prefix.
Documents are split into 300-word chunks with 50 words of overlap (`[chunking]` in `p2.toml`), each chunk is embedded once and the vectors are cached, and the query is embedded the same way.
Chunks are ranked by cosine similarity with an exact numpy search, and a document scores its best chunk.
Changes from the 12 lab: the lab embedded whole articles and this embeds chunks, and the vector cache is keyed by chunk text.
bge-small was selected over potion-retrieval because while bge is slower and has a higher cost it includes the context around a word so a word's vector changes with the words around it

**hybrid.** Reciprocal rank fusion (RRF) of `bm25` and `dense`: a document scores the sum of 1 / (60 + rank) over its rank in each of the two systems, ranks counted from 1, and documents are ordered by that score with ties in document id order.
Each system is asked for a ranking of every document in the corpus, not its top 10, so a document ranked 11th by both can still reach the fused top 10.
Both parts are the same `bm25` and `dense` as above, so the documents are scored from the same 300-word chunks, and the fusion happens at the document level.
Changes from the 13 lab: the lab fused whole-article rankings, and here the inputs are chunk-based document rankings, with `bm25` using the `codes` tokenizer from `p2.toml`; `k = 60` and the fusion formula are the lab's.
The system also has a `search_chunks` that fuses the chunk rankings the same way, for `p2 answer`. 
Bm25 and dense were fused because they work well together to cover for eachothers' weaknesses.

**rerank.** A listwise reranker over the top 20 documents of `hybrid`: one `claude -p` call per query on Sonnet (`[claude]` in `p2.toml`) with no tools, so Claude sees only the prompt.
The 20 candidates are shown as numbered passages, each document cut to its first 2,000 characters, and Claude must reply with all 20 numbers, best first, in a JSON object forced by a schema.
Documents ranked 21 and below keep their `hybrid` order underneath the 20, so the reranker can only reorder its candidates and cannot bring back a relevant document that `hybrid` ranked below 20.
A reply that is not each of 1 to 20 exactly once keeps the `hybrid` order for that query and prints a warning; the replies are cached, and the tokens and seconds of every call are in `traces/shared-practice-rerank.jsonl`.
Changes from the 13 lab: the schema also bounds every number to 1 through 20 (the lab's fixed only how many numbers come back); passages are cut at 2,000 characters where the lab used 600, because these sections are longer than the lab's articles; and the prompt names 30 CFR and states the brief's relevance rule, that a section is relevant when it states the requirement the query asks about, that the parallel sections in parts 56, 57, 75 and 77 are all relevant when the query names no kind of mine, and that a section that only cross-references the requirement is not.
`search_chunks` reranks the top 20 chunks of `hybrid` the same way, for `p2 answer`.
The practice run took 20 calls, about 16,400 input tokens per call.
I reranked hybrid over dense because hybrid gives the reranker more options to work with since it retrieves texts from both dense and bm25.
I kept it at 20 candidates and 2,000 characters as a reasonable cost since the text has to be passed to Claude for rerank while still providing enough options to find a good match. The prompt carries the relevance rule to ensure that sections that are retained are directly relevant as well as balance sections that are relevant to different portions.

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.592 | 0.471 | 0.444 |
| rerank | 0.758 | 0.800 | 0.763 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.595 | 0.917 |
| dense | MRR@10 | 0.333 | 0.714 | 0.653 |
| dense | nDCG@10 | 0.211 | 0.593 | 0.661 |
| hybrid | Recall@10 | 0.500 | 0.405 | 0.917 |
| hybrid | MRR@10 | 0.514 | 0.154 | 0.792 |
| hybrid | nDCG@10 | 0.397 | 0.203 | 0.779 |
| rerank | Recall@10 | 0.714 | 0.595 | 1.000 |
| rerank | MRR@10 | 0.714 | 0.714 | 1.000 |
| rerank | nDCG@10 | 0.697 | 0.626 | 1.000 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.067 | [-0.350, +0.225] | 0.415 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.055 | [-0.225, +0.343] | 0.412 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.039 | [-0.302, +0.231] | 0.385 | not distinguishable |
| hybrid minus bm25 | Recall@10 | -0.033 | [-0.250, +0.192] | 0.324 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.036 | [-0.178, +0.084] | 0.193 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.075 | [-0.238, +0.075] | 0.228 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.033 | [-0.125, +0.192] | 0.231 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.091 | [-0.305, +0.110] | 0.300 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.036 | [-0.199, +0.113] | 0.227 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.133 | [-0.100, +0.358] | 0.340 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.293 | [+0.043, +0.533] | 0.353 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.244 | [+0.015, +0.461] | 0.326 | rerank higher |
| rerank minus dense | Recall@10 | +0.200 | [+0.050, +0.367] | 0.224 | rerank higher |
| rerank minus dense | MRR@10 | +0.237 | [+0.083, +0.408] | 0.239 | rerank higher |
| rerank minus dense | nDCG@10 | +0.283 | [+0.148, +0.430] | 0.207 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | 0.166 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | 0.246 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.319 | [+0.196, +0.446] | 0.180 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

Rerank is distinguishably better than the other three systems on MRR@10 and nDCG@10, however the comparisons between the other three systems are not significant enough to make any claims on. Based on the table for MDD the smallest gap falls between 0.2 and 0.4 for n=20. Bm25 performed as claimed, doing solid on the direct word matches but not finding any of the paraphrased matches. We cannot make any claim on hybrid as compared to bm25 and dense since the gap was below the threshold for significance. Rerank showed a significant improvement over the other three which supports the claim that it can improve the candidate list.

---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| hybrid | hybrid | 7 of 8 (88%) | [0.529, 0.978] | 1 of 8 (12%) | 4 of 4 (100%) | [0.510, 1.000] | 11 of 11 |
<!-- p2:end answers -->

Which system answered, and why that one?
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.

all three claims were built using hybrid in order to save tokens that rerank would have cost.

The quote for claim one is missing some of the context as the type of accident the 15 minute window is applicable for. The quotes for claim 3 and 5 respectively are both correct and relevant.

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

TODO: describe your corpus and its license basis.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

TODO: describe your gold set and your relevance rule.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.900 | 0.744 | 0.774 |
| dense | 0.923 | 0.791 | 0.785 |
| hybrid | 0.947 | 0.820 | 0.814 |
| rerank | 0.954 | 0.885 | 0.861 |
| ablation/dense_chunks | 0.878 | 0.744 | 0.739 |

55 judged queries; nDCG uses binary labels; a random ranking of the 209 documents would get recall@10 near 0.048.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | substance (n=19) | name (n=18) | paraphrase (n=18) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.972 | 0.722 |
| bm25 | MRR@10 | 0.895 | 0.803 | 0.525 |
| bm25 | nDCG@10 | 0.903 | 0.832 | 0.579 |
| dense | Recall@10 | 0.982 | 0.950 | 0.833 |
| dense | MRR@10 | 0.855 | 0.833 | 0.680 |
| dense | nDCG@10 | 0.855 | 0.823 | 0.673 |
| hybrid | Recall@10 | 1.000 | 0.950 | 0.889 |
| hybrid | MRR@10 | 0.925 | 0.894 | 0.636 |
| hybrid | nDCG@10 | 0.893 | 0.867 | 0.678 |
| rerank | Recall@10 | 0.965 | 0.961 | 0.935 |
| rerank | MRR@10 | 0.934 | 0.841 | 0.877 |
| rerank | nDCG@10 | 0.887 | 0.837 | 0.857 |
| ablation/dense_chunks | Recall@10 | 0.982 | 0.885 | 0.759 |
| ablation/dense_chunks | MRR@10 | 0.833 | 0.731 | 0.661 |
| ablation/dense_chunks | nDCG@10 | 0.862 | 0.732 | 0.618 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=10) | claude (n=45) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 0.900 | 0.900 | +0.000 | [-0.233, +0.167] | not distinguishable |
| bm25 | MRR@10 | 0.783 | 0.735 | +0.048 | [-0.210, +0.274] | not distinguishable |
| bm25 | nDCG@10 | 0.792 | 0.770 | +0.022 | [-0.208, +0.219] | not distinguishable |
| dense | Recall@10 | 0.950 | 0.917 | +0.033 | [-0.091, +0.131] | not distinguishable |
| dense | MRR@10 | 0.861 | 0.775 | +0.086 | [-0.133, +0.263] | not distinguishable |
| dense | nDCG@10 | 0.836 | 0.774 | +0.063 | [-0.099, +0.205] | not distinguishable |
| hybrid | Recall@10 | 1.000 | 0.936 | +0.064 | [+0.015, +0.130] | hand higher |
| hybrid | MRR@10 | 0.917 | 0.799 | +0.118 | [-0.080, +0.273] | not distinguishable |
| hybrid | nDCG@10 | 0.897 | 0.796 | +0.101 | [-0.049, +0.227] | not distinguishable |
| rerank | Recall@10 | 1.000 | 0.944 | +0.056 | [+0.016, +0.104] | hand higher |
| rerank | MRR@10 | 0.900 | 0.882 | +0.018 | [-0.137, +0.154] | not distinguishable |
| rerank | nDCG@10 | 0.909 | 0.850 | +0.059 | [-0.057, +0.169] | not distinguishable |
| ablation/dense_chunks | Recall@10 | 0.900 | 0.873 | +0.027 | [-0.128, +0.159] | not distinguishable |
| ablation/dense_chunks | MRR@10 | 0.698 | 0.754 | -0.056 | [-0.275, +0.159] | not distinguishable |
| ablation/dense_chunks | nDCG@10 | 0.727 | 0.742 | -0.015 | [-0.195, +0.155] | not distinguishable |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | -0.017 | -0.050 | +0.033 | [-0.174, +0.289] | not distinguishable |
| MRR@10 | -0.040 | -0.078 | +0.038 | [-0.188, +0.264] | not distinguishable |
| nDCG@10 | -0.004 | -0.044 | +0.040 | [-0.101, +0.180] | not distinguishable |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.82 (10 queries), claude 0.83 (45 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 10 hand and 45 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | +0.023 | [-0.053, +0.111] | 0.118 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.047 | [-0.061, +0.156] | 0.158 | not distinguishable |
| dense minus bm25 | nDCG@10 | +0.011 | [-0.068, +0.095] | 0.118 | not distinguishable |
| hybrid minus bm25 | Recall@10 | +0.047 | [-0.024, +0.127] | 0.110 | not distinguishable |
| hybrid minus bm25 | MRR@10 | +0.077 | [+0.012, +0.142] | 0.094 | hybrid higher |
| hybrid minus bm25 | nDCG@10 | +0.040 | [-0.014, +0.095] | 0.080 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.024 | [+0.000, +0.055] | 0.039 | not distinguishable |
| hybrid minus dense | MRR@10 | +0.030 | [-0.046, +0.102] | 0.108 | not distinguishable |
| hybrid minus dense | nDCG@10 | +0.029 | [-0.018, +0.073] | 0.067 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.054 | [-0.007, +0.127] | 0.096 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.141 | [+0.039, +0.246] | 0.149 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.087 | [+0.012, +0.168] | 0.114 | rerank higher |
| rerank minus dense | Recall@10 | +0.031 | [-0.015, +0.077] | 0.068 | not distinguishable |
| rerank minus dense | MRR@10 | +0.094 | [-0.009, +0.195] | 0.144 | not distinguishable |
| rerank minus dense | nDCG@10 | +0.076 | [+0.002, +0.148] | 0.104 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.007 | [-0.032, +0.046] | 0.056 | not distinguishable |
| rerank minus hybrid | MRR@10 | +0.065 | [-0.026, +0.158] | 0.130 | not distinguishable |
| rerank minus hybrid | nDCG@10 | +0.046 | [-0.019, +0.113] | 0.095 | not distinguishable |
| ablation/dense_chunks minus bm25 | Recall@10 | -0.022 | [-0.112, +0.075] | 0.135 | not distinguishable |
| ablation/dense_chunks minus bm25 | MRR@10 | -0.0003 | [-0.120, +0.121] | 0.174 | not distinguishable |
| ablation/dense_chunks minus bm25 | nDCG@10 | -0.034 | [-0.126, +0.059] | 0.132 | not distinguishable |
| ablation/dense_chunks minus dense | Recall@10 | -0.045 | [-0.094, -0.009] | 0.062 | dense higher |
| ablation/dense_chunks minus dense | MRR@10 | -0.047 | [-0.109, +0.012] | 0.087 | not distinguishable |
| ablation/dense_chunks minus dense | nDCG@10 | -0.046 | [-0.087, -0.008] | 0.056 | dense higher |
| ablation/dense_chunks minus hybrid | Recall@10 | -0.070 | [-0.124, -0.024] | 0.071 | hybrid higher |
| ablation/dense_chunks minus hybrid | MRR@10 | -0.077 | [-0.170, +0.017] | 0.134 | not distinguishable |
| ablation/dense_chunks minus hybrid | nDCG@10 | -0.075 | [-0.139, -0.014] | 0.090 | hybrid higher |
| ablation/dense_chunks minus rerank | Recall@10 | -0.076 | [-0.140, -0.016] | 0.090 | rerank higher |
| ablation/dense_chunks minus rerank | MRR@10 | -0.141 | [-0.239, -0.041] | 0.142 | rerank higher |
| ablation/dense_chunks minus rerank | nDCG@10 | -0.121 | [-0.194, -0.048] | 0.106 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

Using my gold-set and MRR@10 as the metric I can claim that hybrid outperforms bm25, rerank outperforms bm25, and rerank outperforms the ablation dense. For the large majority of systems and metrics hand and claude queries were not distinguishable with the exception of the hybrid and rerank performing better on Recall@10 on the hand queries. My prediction in DECISIONS.md prompt 1 did not hold, while rerank scored the best it was not distinguishable from hybrid, and I observed that dense outperformed bm25 but those two were not distinguishable either.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

I hypothesize that raising dense's chunk size from 300 to 600 words (overlap 100) will raise MRR@10 on my corpus above dense's 0.791, because increasing the context the model can see could reveal more necessary context to connect the paraphrased queries to the real answer. Even though the model truncates at 512 tokens this allows dense to take advantage of the full limit when it can.

<!-- p2:begin own-ablation -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| ablation/dense_chunks minus bm25 | Recall@10 | -0.022 | [-0.112, +0.075] | 0.135 | not distinguishable |
| ablation/dense_chunks minus bm25 | MRR@10 | -0.0003 | [-0.120, +0.121] | 0.174 | not distinguishable |
| ablation/dense_chunks minus bm25 | nDCG@10 | -0.034 | [-0.126, +0.059] | 0.132 | not distinguishable |
| ablation/dense_chunks minus dense | Recall@10 | -0.045 | [-0.094, -0.009] | 0.062 | dense higher |
| ablation/dense_chunks minus dense | MRR@10 | -0.047 | [-0.109, +0.012] | 0.087 | not distinguishable |
| ablation/dense_chunks minus dense | nDCG@10 | -0.046 | [-0.087, -0.008] | 0.056 | dense higher |
| ablation/dense_chunks minus hybrid | Recall@10 | -0.070 | [-0.124, -0.024] | 0.071 | hybrid higher |
| ablation/dense_chunks minus hybrid | MRR@10 | -0.077 | [-0.170, +0.017] | 0.134 | not distinguishable |
| ablation/dense_chunks minus hybrid | nDCG@10 | -0.075 | [-0.139, -0.014] | 0.090 | hybrid higher |
| ablation/dense_chunks minus rerank | Recall@10 | -0.076 | [-0.140, -0.016] | 0.090 | rerank higher |
| ablation/dense_chunks minus rerank | MRR@10 | -0.141 | [-0.239, -0.041] | 0.142 | rerank higher |
| ablation/dense_chunks minus rerank | nDCG@10 | -0.121 | [-0.194, -0.048] | 0.106 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
ablation/dense_chunks against dense (BASE = "dense" in p2/retrievers/dense_chunks.py): it helped 7 queries, hurt 10 and left 38 unchanged.

| Query | Class | Origin | dense RR | ablation/dense_chunks RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| c17 | substance | claude | 0.500 | 1.000 | +0.500 | helped |
| c19 | substance | claude | 0.500 | 1.000 | +0.500 | helped |
| c36 | paraphrase | claude | 0.500 | 1.000 | +0.500 | helped |
| c37 | paraphrase | claude | 0.167 | 0.333 | +0.167 | helped |
| c39 | paraphrase | claude | 0.125 | 0.250 | +0.125 | helped |
| c15 | substance | claude | 0.250 | 0.333 | +0.083 | helped |
| h03 | paraphrase | hand | 0.111 | 0.143 | +0.032 | helped |
| h05 | name | hand | 1.000 | 0.333 | -0.667 | hurt |
| c10 | name | claude | 1.000 | 0.500 | -0.500 | hurt |
| c23 | substance | claude | 1.000 | 0.500 | -0.500 | hurt |
| c24 | substance | claude | 1.000 | 0.500 | -0.500 | hurt |
| c38 | paraphrase | claude | 1.000 | 0.500 | -0.500 | hurt |
| h06 | substance | hand | 1.000 | 0.500 | -0.500 | hurt |
| h10 | name | hand | 1.000 | 0.500 | -0.500 | hurt |
| c41 | paraphrase | claude | 0.333 | 0.000 | -0.333 | hurt |
| c42 | paraphrase | claude | 0.500 | 0.167 | -0.333 | hurt |
| c09 | name | claude | 0.500 | 0.333 | -0.167 | hurt |

RR is the reciprocal rank of the first relevant document in the top 10 (0 when none is there), the per-query value behind MRR@10; the queries at the top of each list are the ones to read.
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

The change made was increasing the chunk size from 300 to 600 words and the overlap from 50 to 100, everything else was held constant, there is a truncation at 512 tokens which may prevent it from getting a full 600 word chunk. The result did not support my hypothesis, I expected an increase in performance but the observed result was a decrease in point score from 0.791 to 0.744 a difference of -0.047 which is not enough to be a distinguishable difference, additionally dense was distinguishably higher in Recall and nDCG. With my gold set in order to see an effect the MDD would be 0.087, a true difference larger than about 0.09 would have been detected 80% of the time. By inspecting the table we can see that the change helped on 7 queries but hurt 10 with 38 remaining the same. Top helped example and interpretation: c36 a paraphrase query asking for a list of measurable characteristics, more context means more characteristics this makes sense. Top hurt example and interpretation: h05 asks for a single statistic where additional context could accidentally tie another number to the answer rather than what the user was asking for.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|

TODO: add one row for each failure you analyzed, and write two or three sentences on the pattern you see across them.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

TODO: write the cross-corpus comparison.

---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-hybrid.jsonl | hybrid | 12 | 12 | 2 | 81,624 | 3,074 | 53.2 | 6,802 | 256 | 4.4 |
| traces/answers-hybrid.r1.jsonl | hybrid | 12 | 12 | 0 | 81,619 | 2,836 | 56.0 | 6,802 | 236 | 4.7 |
| traces/answers-hybrid.r2.jsonl | hybrid | 12 | 12 | 0 | 81,619 | 3,319 | 56.8 | 6,802 | 277 | 4.7 |
| traces/answers-hybrid.r3.jsonl | hybrid | 12 | 12 | 0 | 81,615 | 2,999 | 55.1 | 6,801 | 250 | 4.6 |
| traces/own-own-rerank.jsonl | rerank | 55 | 55 | 2 | 2,885,453 | 5,005 | 247.8 | 52,463 | 91 | 4.5 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 2 | 328,625 | 1,932 | 86.6 | 16,431 | 97 | 4.3 |
| traces/shared-practice-rerank.r1.jsonl | rerank | 20 | 20 | 0 | 358,219 | 2,221 | 92.6 | 17,911 | 111 | 4.6 |
| traces/shared-practice-rerank.r2.jsonl | rerank | 20 | 20 | 0 | 321,326 | 2,322 | 91.9 | 16,066 | 116 | 4.6 |
| traces/shared-practice-rerank.r3.jsonl | rerank | 20 | 20 | 0 | 353,892 | 2,241 | 91.7 | 17,695 | 112 | 4.6 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 1 | 706,952 | 4,902 | 236.4 | 17,674 | 123 | 5.9 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.293 | [-0.533, -0.043] | 16,431 | 4.3 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.237 | [-0.408, -0.083] | 16,431 | 4.3 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.329 | [-0.504, -0.164] | 16,431 | 4.3 | rerank higher |
| own: bm25 minus rerank | 55 | -0.141 | [-0.246, -0.039] | 52,463 | 4.5 | rerank higher |
| own: dense minus rerank | 55 | -0.094 | [-0.195, +0.009] | 52,463 | 4.5 | not distinguishable |
| own: hybrid minus rerank | 55 | -0.065 | [-0.158, +0.026] | 52,463 | 4.5 | not distinguishable |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-ablation-dense_chunks.jsonl | dense_chunks | 55 | 0.75 | 13.7 |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 55 | 0.14 | 2.6 |
| traces/retrieval/own-own-dense.jsonl | dense | 55 | 0.87 | 15.8 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 55 | 1.29 | 23.4 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.10 | 4.8 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.37 | 18.7 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.55 | 27.5 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.20 | 5.0 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.63 | 15.9 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 1.08 | 27.0 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

Write the five things here.

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
Repeated runs of rerank on shared/practice:

| Run | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| rerank.r1 | 0.758 | 0.800 | 0.757 |
| rerank.r2 | 0.758 | 0.800 | 0.755 |
| rerank.r3 | 0.758 | 0.800 | 0.754 |
| range (max minus min) | 0.000 | 0.000 | 0.003 |

| Comparison | Metric | Mean difference | 95% interval | Reading |
| --- | --- | ---: | ---: | --- |
| rerank.r1 minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | rerank.r1 higher |
| rerank.r2 minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | rerank.r2 higher |
| rerank.r3 minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | rerank.r3 higher |
| rerank.r1 minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | rerank.r1 higher |
| rerank.r2 minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | rerank.r2 higher |
| rerank.r3 minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | rerank.r3 higher |
| rerank.r1 minus hybrid | nDCG@10 | +0.314 | [+0.191, +0.440] | rerank.r1 higher |
| rerank.r2 minus hybrid | nDCG@10 | +0.311 | [+0.188, +0.439] | rerank.r2 higher |
| rerank.r3 minus hybrid | nDCG@10 | +0.311 | [+0.187, +0.438] | rerank.r3 higher |

Repeated answers shared/hybrid:

| File | Verified (in) | 95% interval | Declined (out) | 95% interval |
| --- | ---: | ---: | ---: | ---: |
| hybrid.r1 | 7 of 8 (88%) | [0.529, 0.978] | 4 of 4 (100%) | [0.510, 1.000] |
| hybrid.r2 | 7 of 8 (88%) | [0.529, 0.978] | 4 of 4 (100%) | [0.510, 1.000] |
| hybrid.r3 | 7 of 8 (88%) | [0.529, 0.978] | 4 of 4 (100%) | [0.510, 1.000] |
| range (max minus min) | 0.000 |  | 0.000 |  |

Each repeat answers the same questions, so the repeats are not independent trials and their counts are not pooled into one interval.
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

598E: write the repeats result here.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

598E: write the claim and its outcome here.
