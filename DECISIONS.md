# Decision log

Your methods section, in your own words.
About one to two pages in total.

Answer these as you go, not the night before it is due.
Each answer is easier to write while the decision is still fresh, and prompt 1 only works if you write it before you see your own-corpus numbers.
Specifics beat polish: a short, honest answer with a number in it is worth more than a long vague one.

Each prompt ends with a marker line.
Replace that line with your answer.
`uv run p2 check` reports a marker as unfinished work, and `uv run p2 check --final` fails while any marker is left, so a finished log is part of being done.

Please do not let the agent write these for you.
These answers are about what you chose and what you knew, and the agent cannot know that.
Prompt 3 in particular only works in your own words.

---

## 1. Why this corpus, and what you expected

Why did you pick the corpus you used in stage 2, and why does it belong to a field or a question you care about?
Then say what you expected before you measured anything: which of `bm25`, `dense`, `hybrid` and `rerank` do you think will win on it, and which will do worst, and why?

Commit this answer before your first `uv run p2 score` on the own corpus.
Git history then shows that the expectation came first, which is what lets it be wrong in a way that teaches you something.
If you were surprised later, say so in prompt 4 or in EVAL.md; do not come back and rewrite this one.

I chose this corpus because it is specific to Colorado and a topic that interests me. Because it is government data it is public domain so it works well for this project. I expect rerank to do the best because I expect this corpus to have multiple matches for each query on hybrid thus reranking them should show improvement. I expect dense to do the worst because there will be a lot of context overlap due to the narrow scope of the corpus.

---

## 2. A fork in the road

Name one real design choice where you could have gone two ways: the chunk size, the embedding model, how the two systems are fused, how many documents the reranker sees, a sentence in `prompts/answer.txt`, how you cleaned the corpus.

Say which you picked, what the alternative was, and what you gave up by not taking it.
If you measured both, give both numbers.
If you rejected the alternative without measuring it, say why that was a fair call, and what it cost you in time, tokens or complexity.

"There was no alternative" is not an answer.
Find the fork.

I chose to increase the character limit from 2000 to 6000 characters in order to give a more robust test of the reranker. This will have a higher cost of tokens but it is worth testing. It improves from 13% but doesn’t take too much of the document. I gave up the cheaper cost and potentially more accurate response of the best chunk.

---

## 3. Where you overruled the agent

One time Claude suggested, wrote or claimed something and you did not take it.
It might be a relevance judgment you disagreed with, a retriever it called finished when a run file showed otherwise, a number it summarized wrongly, or a license it said was fine.

What did it do?
How did you notice?
What did you do instead?

If it genuinely never happened, say so plainly, and then say what you would have had to check in order to notice.
Being honest here costs you far less than a story you cannot defend when you record your video.

One step where I kept some oversight on the agent was during the drafting of the claude written queries when claude was identifying the best matches for each query. For the most part claude did well identifying matches however one example where I had to override claude was with the following query. The original query read "When were the monitoring wells on the east side of the Uncompahgre River built?", however upon reviewing the evidence the wells were built in two phases as two separate times. Leaving the query as is was vague and did not have a clear right answer, simply updating the phrasing to say completed narrowed the scope of the question so that the intended section is the one that quotes well completion rather than construction phases.

---

## 4. A number you do not trust

Pick one number in `EVAL.md` that you do not fully trust, and say why.
It could be a mean over a small query class, a difference whose interval includes zero, a verified share of 100%, a score on a gold set you wrote yourself, or a result you got only once.

What would have to be true for you to trust it?
Did you do anything to test it, and what did that show?

The number I don't trust is the number for comparing the scores between the Claude queries and the hand written queries to determine if the model-written queries favor key word search due to their construction method. The most useful single number for this is in column Claude minus hand in the MRR@10 row since this stat is what was used for comparisons across the project. The score was +0.038 with bm25 trails dense by slightly less on the claude queries but not enough to be distinguishable. It is hard to trust this number because of how few hand written queries there are relative to the number of claude queries, which leaves us with a very wide interval relative to the score. In order to trust it better having an equal number of claude and hand queries would help to ensure a more fair reading. I was not able to test this as I didn't have time to write and run more hand queries but this would be a good future step.

---

## 5. What is still wrong

One thing in your system, your corpus or your gold set that is not right, not finished, or that you do not fully understand.

What would you do next, and how would you find out whether it matters?
Name the file, the query or the document where someone could look.

The biggest piece that I would change or work on next would be something I have mentioned several times which is raising the 6,000 character limit for rerank. Having this limit prevented rerank from having the full context when ranking selections which hurt on queries where the most relevant data falls beyond this limit in the document, this can be seen by inspecting OWN_PASSAGE_CHARS in p2/retrievers/rerank.py as well as the results in the EVAL.md section 6 table. One interesting way to address this would be rather than just raw raising the limit to keep the limit the same but instead dynamically give rerank the 6,000 character chunk that was deemed most relevant by the other systems. A quick test to see improvement would be to run the change on the 8 queries whose answers sit beyond character 6,000 and check that rank improves for rerank. Finally in order to validate whether this change had the result I expected I would need to rerun all 55 queries and then recompare rerank and hybrid to see if this was able to improve rerank enough to have a distinguishable improvement. A potential risk of this is that if hybrid's chunk that was determined to be the most relevant is not the correct chunk the same issue would repeat and rerank would likely not rank this highly.
