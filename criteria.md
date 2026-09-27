# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** 3 of 5 would only be average; I want good, and 4 of 5 is
the minimum I'd call good.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** Naming the source has to happen every time, not four
times in five. The person reading an answer is either not going to search
fourteen guides to check it, or doesn't know where to look — an answer with no
source leaves them nothing to check it against.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:** When I set the cutoff, the two groups didn't overlap: my
five questions' best distances ran 0.292–0.604 and the five out-of-scope ones
0.818–0.968. I put the cutoff at 0.56, below that gap on purpose, because my
rule is that when retrieval misses, the system should honestly say no. Q2
(0.604) is the one question whose answer isn't in its top five chunks, so 0.56
refuses it, while Q4 (0.517), whose answer was retrieved, still gets through;
0.56 is the middle of those two.

---

## 4. Chunks can answer a question on their own

Every chunk `chunker.py::split_documents` produces is scored on five yes/no
checks, and passes at **4 or more of 5**:

| # | Check | Marked by |
| --- | --- | --- |
| 1 | **Answerable alone** — using only this chunk, someone could give a factually correct answer to a question about its topic (for a chunk covering several towns: a question about any one of them) | Claude, with a reason for every N |
| 2 | **Whole unit** — it starts with "Guide > Section:" and ends at the end of a sentence | `review_chunks.py` |
| 3 | **One line of ideas** — every sentence serves the topic named in its heading | Claude, with a reason for every N |
| 4 | **Concrete** — it contains a digit, a number written as a word (two to twenty, thirty, forty, fifty, hundred, thousand), a day or a month | `review_chunks.py` |
| 5 | **Not repeated** — its text is not a near-copy (90% or more the same) of another chunk's | `review_chunks.py` |

At least **60 of the 72** town-guide chunks and at least **15 of the 22**
cross-cutting-guide chunks pass. Both parts have to hold.

Claude's marks for checks 1 and 3 are audited: I check ten chunks drawn at
random (seed 201) and record how many I agree with in
`results/chunk_spotcheck.md`. The full sheet is `results/chunk_review.md`.

**Why this target:** I think of the system as a student doing a
reading-comprehension exercise. Work that stays inside one section of one
passage — a town guide's chunk, one town and one topic — needs no connecting,
verifying or analysing, so it's the easier task and I expect the higher score
(60 of 72). A cross-cutting chunk puts several towns under one theme, which is
the more complex, demanding task, so I expect a lower score there (15 of 22).

---

## 5. Answers are factual, precisely sourced, and concise

At least **4 of my 5** test questions get an answer that passes, **in every
run**. An answer passes only if it clears three checks, in this order:

1. **Factual** — it contains the question's `expects` phrase from
   `questions.py`.
2. **Precise** — every file it names is one listed for that question below.
   Naming no file doesn't fail this check; criterion 2 covers that.
3. **Concise** — it is at most **80 words per fact the question needs**: 80
   words for questions 1–3, which need one fact each, and 160 for questions
   4–5, which need two.

| Question | Files that count as a correct reference | Facts needed |
| --- | --- | --- |
| 1. Givens Mill tearoom | `guide_givens_mill.md` | 1 |
| 2. Cheapest train tickets | `guide_regional_transport.md` | 1 |
| 3. Halden Bay coastal path | `guide_halden_bay.md`, `guide_walking.md`, `guide_regional_transport.md` | 1 |
| 4. Best town in winter | `guide_marchwood.md`, `guide_thornby_wells.md` | 2 |
| 5. Nearest full hospital | `guide_accessibility.md`, which must be named; any of the nine town guides may be named alongside it | 2 |

A fact is one claim that can be checked against the documents on its own; two
claims are separate facts if one could be true while the other is false. The
facts each question needs were counted from the answer key in `README.md`
before any answers existed.

**Why this target:** 4 of 5 for the same reason as criterion 1: 3 of 5 would
only be average, and 4 is the minimum I'd call good. The chunks an answer is
built from run to about 50–70 words, so 80 words is generous for a one-fact
answer, and 160 covers the ones that need two. Generous on purpose: now and
then the sentence that holds the answer is long and dense with information,
and a correct answer shouldn't fail for quoting it.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
