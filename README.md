# The Unofficial Guide

**Hien Vo** — corpus: `city_guides`

---

# Unit 1

## What This Does

The Unofficial Guide answers travel questions about a fictional region using
only fourteen guides from the `city_guides` corpus: nine town guides (Halden
Bay, Brightwater, Marchwood and others) and five that cut across all of them
(eating, walking, regional transport, seasons, accessibility). It handles
specific, practical questions — when somewhere is open or closed, how to get
there without a car, where to eat or stay, when to visit, how easy a town is to
get around. For each question it finds the closest guide sections, refuses
with "I don't have enough information about that" when nothing is close
enough, and otherwise has Gemini answer from those sections alone, naming the
files it used.

## Test Questions and Answer Key

The five questions in `questions.py`, in the same order `run_eval.py` runs
them, with where each answer actually lives in the corpus. To judge a generated
answer, compare it against the quoted sentence: a correct answer contains the
**expects** phrase.

| # | Question | Correct answer contains | Where the answer is | The sentence it comes from |
| --- | --- | --- | --- | --- |
| 1 | Which day of the week is the Givens Mill tearoom closed? | `Tuesday` | [guide_givens_mill.md › Eat and drink](corpora/city_guides/documents/guide_givens_mill.md#eat-and-drink) (line 15) | "A tearoom attached to the mill, open 10 to 4 daily except **Tuesdays**…" |
| 2 | How far ahead should I book train tickets to get the cheapest fare? | `a week ahead` | [guide_regional_transport.md › The railway](corpora/city_guides/documents/guide_regional_transport.md#the-railway) (lines 9–10) | "Tickets are cheaper booked the day before than on the day, and considerably cheaper than that booked **a week ahead**." *"The day before" is in the same sentence and is the wrong answer.* |
| 3 | When does the Halden Bay coastal path get closed? | `high wind` | [guide_halden_bay.md › When to go](corpora/city_guides/documents/guide_halden_bay.md#when-to-go) (line 27). Also [guide_walking.md › Serious, and weather-dependent](corpora/city_guides/documents/guide_walking.md#serious-and-weather-dependent) (lines 30–31) and [guide_regional_transport.md › Walking and cycling](corpora/city_guides/documents/guide_regional_transport.md#walking-and-cycling) (line 41) | "The coastal path is genuinely dangerous in **high wind** and gets shut." |
| 4 | Which town is the best place to visit in winter? | `Marchwood` | [guide_marchwood.md › When to go](corpora/city_guides/documents/guide_marchwood.md#when-to-go) (line 27), backed up by [guide_thornby_wells.md › When to go](corpora/city_guides/documents/guide_thornby_wells.md#when-to-go) (line 27) | "This is the one place in the region that works in winter…" and "…the region's most reliable winter destination after **Marchwood**." *Thornby Wells is second, not first.* |
| 5 | Where is the nearest full hospital? | `Marchwood` | [guide_accessibility.md › Practical](corpora/city_guides/documents/guide_accessibility.md#practical) (line 45). **Contradicted** by the "Practical notes" paragraph repeated in all 9 town guides, e.g. [guide_halden_bay.md › Practical notes](corpora/city_guides/documents/guide_halden_bay.md#practical-notes) (line 33) | "The nearest full hospital is in **Marchwood**. Brightwater has a hospital…" versus the town guides' "The nearest full hospital is in Brightwater…" *An answer of "Brightwater" is the one the repeated paragraph produces; see the comment in `questions.py`.* |

The five `OUT_OF_SCOPE` questions at the bottom of `questions.py` have no
answer anywhere in the corpus. The correct result for each is the refusal:
"I don't have enough information about that."

## Chunking Strategy

**Chunk size:** one `##` section per chunk, not a character count — 183 to 758
characters, a median of 47 words. A section over 1,000 characters would be cut
into windows, but no section in this corpus is that long (the longest is 691).

**Overlap:** none between sections. Instead, every chunk starts with
`{guide title} > {section heading}:`. (The 1,000-character windows would
overlap by 100, but they never fire here.)

Every guide is real markdown: a `#` title, then `##` sections such as "Getting
there", "Eat and drink" and "When to go", and each section is one
self-contained idea of 158 to 691 characters. The headings already mark
where one idea ends and the next begins, so they are the cut.

The starter's fixed 800-character chunker ignored them. It made 51 chunks that
ran across section boundaries and started and ended mid-word — one began
"urs" (the tail of "Opening hours"), another ended "stop serving at 9p", and
the shortest was just "d Sundays and after 5pm." Splitting on headings makes
94 chunks (84 sections plus 10 intro paragraphs) with no text lost.

The prefix does the job overlap usually does. A section read on its own often
doesn't say which town it's about — "Buses run four times a day" — and the
prefix puts that back without copying text from the neighbouring section.

The known weak spot is the five cross-cutting guides, where one section puts
several towns under one theme ("Difficult" covers four towns). Splitting on the
heading is still right, but those chunks are broader, which is why criterion 4
sets a lower bar for them (15 of 22) than for the town guides (60 of 72). The
function is `chunker.py::split_documents`; the starter's version is kept as
`chunker.py::fallback_split` for comparison.

## Sample Chunks

Printed by `python app.py chunks -n 5`, which samples evenly across all 94
chunks, and copied across unedited.

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```text
Getting around the region with limited mobility > Overview: An honest assessment rather than a promotional one. Some of these places are difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```text
Corry Vale > Where to stay: Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```text
Givens Mill > Getting around: Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```text
Kestrelford > What to see: The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```text
Pellew Sands > When to go: June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```

## Sample Answer

Produced by `python app.py ask "Where is the nearest full hospital?"` at cutoff
0.56, copied unedited. The full run, including the exact prompt the model was
sent (`--show-prompt`), is in `results/milestone4_sample_answer.txt`.

**Question:** Where is the nearest full hospital?

**Answer:**

```text
  (best distance 0.346, cutoff 0.56)

Based on `guide_accessibility.md`, the nearest full hospital is in Marchwood. (However, the town-specific guides `guide_givens_mill.md`, `guide_kestrelford.md`, `guide_halden_bay.md`, and `guide_marchwood.md` state that the nearest full hospital is in Brightwater.)

Sources retrieved: guide_accessibility.md, guide_givens_mill.md, guide_halden_bay.md, guide_kestrelford.md, guide_marchwood.md
```

**My relevance cutoff:** 0.56 (`THRESHOLD` in `config.py`)

The two groups don't overlap. My five questions' best distances run
0.292–0.604; the five out-of-scope ones run 0.818–0.968. The course's method
puts the cutoff in that gap, but I put it **below** the gap on purpose,
because my rule is that when retrieval misses, the system should honestly say
no:

- **Q2 (0.604)** is the one question whose answer isn't in its top five
  chunks. The chunk that answers it ranks 11th (distance 0.731); the top hit
  is Marchwood's tram-ticket section, which shares the words *ticket* and
  *fare*. At 0.56 the gate refuses it instead of handing the model five chunks
  that don't contain the answer.
- **Q4 (0.517)** has its answer at ranks 3 and 4, so it should get through.
- 0.56 is the middle of those two, leaving about 0.04 either side. 0.6 would
  also have refused Q2, but by only 0.004.

What the gate can't do: distance measures how close the *topic* is, not
whether the answer exists. Questions this corpus can't answer but that sound
like it can — vegetarian restaurants in Kestrelford (0.371), the last
Marchwood airport bus (0.377) — sit as close as my real questions and pass any
sensible cutoff. For those, the only guard is the grounding instruction in
`generate.py`.

Raw output: `results/milestone4_retrieval.txt`, from `python app.py retrieve`.

| Question | In corpus? | Best distance | At 0.56 |
| --- | --- | --- | --- |
| When does the Halden Bay coastal path get closed? | yes | 0.292 | answered |
| Where is the nearest full hospital? | yes | 0.346 | answered |
| Which day of the week is the Givens Mill tearoom closed? | yes | 0.379 | answered |
| Which town is the best place to visit in winter? | yes | 0.517 | answered |
| How far ahead should I book train tickets to get the cheapest fare? | yes | 0.604 | **refused** |
| What is the capital of Mongolia? | no | 0.818 | refused |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.843 | refused |
| How do I write a for loop in Rust? | no | 0.852 | refused |
| How do I change the oil in a diesel engine? | no | 0.884 | refused |
| Who won the 1994 World Cup? | no | 0.968 | refused |

## How I Used AI

**1. Choosing the test questions.** I asked Claude for ten candidate
questions spread across the kinds of source this corpus has — a town guide
only, a cross-cutting guide only, both, several documents together, and
documents that contradict each other — each with a prediction of how close
retrieval would get and whether the answer would come back. I picked five. I
wanted to reword the hospital question to say "medical center"; Claude pointed
out that phrase appears nowhere in the corpus and would add a vocabulary gap on
top of the contradiction I was trying to test, so I kept "full hospital" and
chose Marchwood as the correct answer. When I measured in Milestone 4, two of
the predictions were wrong: the train-ticket question it called easy was my
worst (the chunk that answers it ranked 11th, at 0.731), and the hospital
question it expected to miss put the right chunk first (0.346).

**2. Marking the chunks for criterion 4.** Reading all 94 chunks by hand
wasn't practical, so Claude turned the standards I'd given it — factually
correct, precise, concise, coherent — into a five-check (scored 1-5) rubric, which I approved before anything was marked. A script marks the three mechanical checks; Claude marked the two that need reading, 188 marks in all, 3 of them
N, each with a reason. I audited ten chunks drawn at random with a fixed seed
and agreed on 8. I disagreed on two copies of the repeated "Practical notes"
paragraph: Claude called them answerable on their own because you could ask
whether cash is useful, but to me they jump from cash to mobile coverage to
hospitals and answer no specific question. That disagreement showed check 1's
wording can be read two ways, which I'm leaving on record for Unit 2 rather
than rewording after the count.

### In unit 2

**3. Keeping the two models apart.** Gemini writes the answers being tested,
and Claude was helping me build and check the system, so I told Claude I
didn't want the two mixed up. We set a rule before any results existed: the
scorer is plain text matching (`scorer.py`), and Claude builds the tools but
never decides whether an answer is right. Where a text match can't be trusted,
`summarize_run.py` lists the answer for me instead. That's how the three Q4
answers after the fix came to me: they don't contain "Marchwood", and I read
them and kept the fails, because the seasons guide they drew on compares no
towns at all.

**4. The diagnosis started from my question.** I asked Claude for possible
causes at different stages, unranked, and it brought one measured check per
stage. What decided it for me was a question I asked on looking at the answer
chunk: why is the railway line and its timetable in front of the ticket
prices, when the question only asks about tickets? That is the mechanism —
two ideas under one heading, one embedding for both — and Claude then showed
the tickets paragraph on its own sits at 0.545 where the whole chunk is at
0.731. When I suggested testing different chunk sizes against the same
measures, it ran six, and warned me that picking the winner on my five
questions would be tuning to the test; the table went in as evidence for the
diagnosis, not as a way to choose.

**5. Asking Claude to pick the one fix — and to show its work.** I asked it to
choose, and to write up the other two with measurements rather than opinions.
It picked paragraph chunking because it was the only candidate acting at the
stage I'd diagnosed, and simulated the other two without changing the system:
hybrid search got Q2's answer into the top five but the gate still refused it,
and a helpful refusal would have pointed Q2 to three wrong files. The after
run then showed exactly the trade its comparison had predicted — Q2 fixed, Q4
broken. What I changed: I checked its after-run work where it needed a
person, auditing ten re-marked chunks (agreeing on 8) and judging Q4's flagged
answers myself.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

`python run_eval.py --label before`: five questions, three runs each, caching
off, cutoff 0.56, top-k 5. The run log is
`results/run_2026-09-27_0143_before.md` (`run_eval.py::main`, criterion 5
scored by `scorer.py::judge`), and this table was added up from it by
`summarize_run.py::summarize` into `results/run_2026-09-27_0143_before_criteria.md`.
Criteria 1, 3 and 4 are deterministic, so the same number fills every run
column. Criterion 4 is town-guide chunks · cross-cutting chunks.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1. Retrieved chunk contains the answer | 4 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | **MISSED** |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunks can answer a question on their own | 60 of 72 and 15 of 22 | 63 · 21 | 63 · 21 | 63 · 21 | MET |
| 5. Answers are factual, precise and concise | 4 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | MET |

**Criteria 1, 2 and 5 — the five answers from run 1**, copied unedited from
the run log. Produced by `run_eval.py::run_once`: `gate.py::check` refused
Q2, and `generate.py::answer_from_chunks` wrote the other four. Runs 2 and 3
are in the log.

```text
Q1  Which day of the week is the Givens Mill tearoom closed?
The Givens Mill tearoom is closed on Tuesdays, according to guide_givens_mill.md.

Q2  How far ahead should I book train tickets to get the cheapest fare?  (best distance 0.604, refused by the gate)
I don't have enough information about that.

Q3  When does the Halden Bay coastal path get closed?
The Halden Bay coastal path gets closed when there is high wind, as it is genuinely dangerous in those conditions (`guide_halden_bay.md` and `guide_walking.md`).

Q4  Which town is the best place to visit in winter?
Marchwood is the one place in the region that works in winter, since almost everything is indoors and nothing closes seasonally (guide_marchwood.md). Additionally, Thornby Wells is noted as the region's most reliable winter destination after Marchwood (guide_thornby_wells.md).

Q5  Where is the nearest full hospital?
According to `guide_accessibility.md`, the nearest full hospital is in Marchwood. (However, the other documents—`guide_givens_mill.md`, `guide_kestrelford.md`, `guide_halden_bay.md`, and `guide_marchwood.md`—state that the nearest full hospital is in Brightwater.)
```

**Criterion 1 — what retrieval returned for Q2**, the one question whose top
five don't contain the answer. Produced by `store.py::search`, via
`python app.py retrieve`; full output in `results/milestone4_retrieval.txt`.
The chunk that answers it, `guide_regional_transport.md#0`, ranks 11th at
0.731.

```text
#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.6042     guide_marchwood.md               Marchwood > Getting around: A tram network of four l...
2   0.6252     guide_kestrelford.md             Kestrelford > When to go: Late spring and early autu...
3   0.6877     guide_eating.md                  Eating across the region > Markets: Kestrelford's Sa...
4   0.6940     guide_marchwood.md               Marchwood > Getting there: Every railway line in the...
5   0.6952     guide_givens_mill.md             Givens Mill > When to go: The mill runs March to Nov...
```

**Criterion 3 — the gate on the out-of-scope questions**, from the run log.
Produced by `run_eval.py::check_out_of_scope`, cutoff 0.56. Refused 5 of 5.

| Out-of-scope question | Best distance | Gate |
| --- | --- | --- |
| What is the capital of Mongolia? | 0.818 | refused |
| How do I change the oil in a diesel engine? | 0.884 | refused |
| Who won the 1994 World Cup? | 0.968 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.843 | refused |
| How do I write a for loop in Rust? | 0.852 | refused |

**Criterion 4 — the chunk review.** Produced by `review_chunks.py::count`
(`python review_chunks.py --count`); every mark and reason is in
`results/chunk_review.md`.

```text
Part A (town guides): 63 of 72 pass at 4+ of 5
Part B (cross-cutting guides): 21 of 22 pass at 4+ of 5
Spot-check: you agreed with Claude on 8 of 10
```

## Verdicts

Against the targets I wrote in unit 1, unchanged. A criterion is met only if
the target holds in every run.

| # | Criterion | Verdict | How I decided |
| --- | --- | --- | --- |
| 1 | Retrieved chunk contains the answer | MET | 4 of 5 in every run, exactly the target. The one miss is Q2 every time — the chunk that answers it ranks 11th, outside the top five — so there's no margin: one more miss in any run would make this a miss. |
| 2 | Every answer names a source | **MISSED** | 4 of 5 in every run against 5 of 5. The only answer with no source is Q2's: the gate refuses it at my 0.56 cutoff, and that refusal is a fixed sentence that names no file. Retrieval and the gate are deterministic, so as the system stands this can't reach 5 of 5. |
| 3 | Gate stops out-of-corpus questions | MET | 5 of 5 in every run, above the 4 of 5 target. But the five questions were never close: their best distances ran 0.818 and up against a 0.56 cutoff, so this barely tested the gate. On-topic questions the corpus can't answer (0.37–0.59 in my Milestone 4 probes) would all get past it. |
| 4 | Chunks can answer a question on their own | MET | 63 of 72 town-guide chunks and 21 of 22 cross-cutting chunks pass, against 60 and 15; chunking is deterministic, so it's the same in every run. The nine failures are the repeated "Practical notes" paragraph. I agreed with 8 of Claude's 10 audited marks, and the two I disagreed on showed check 1 can be read two ways. |
| 5 | Answers are factual, precise and concise | MET | 4 of 5 in every run, exactly the target. Again the only failure is Q2, whose refusal can't contain "a week ahead". The other four were factual and named only allowed files, and the longest was 46 words of a 160 limit, so "concise" was never really tested. |

## Diagnoses

**Criterion 2 (missed) — stage: chunking.** Q2 asks how far ahead to book
train tickets. The answer is in `guide_regional_transport.md` under
`## The railway`, but that one heading holds two ideas: a paragraph on the
line and its timetable, then a paragraph on ticket prices. My chunker cuts on
`##` headings, so both paragraphs became one chunk with one embedding, and the
timetable half pulls it away from a ticket question. The chunk as indexed is
0.731 from Q2; the tickets paragraph on its own would be 0.545, the timetable
paragraph 0.775. So the chunk ranks 11th, and only the top five reach the
model (`TOP_K = 5`, the starter's default). The best distance left is the
Marchwood tram-ticket chunk at 0.604, the 0.56 gate refuses the question, and
the gate's refusal names no file — which is the criterion 2 miss.

It's before generation, not in it: the answer isn't in any of Q2's five
retrieved chunks, so the model never had a chance. My chunking assumption —
one heading, one idea — holds for most of the 84 sections, and this one breaks
it. It even passed criterion 4: the tickets paragraph belongs under "The
railway", so the chunk is coherent by its heading while still being hard to
find for a narrow question.

**The pattern.** This is one problem, not three. The same Q2 failure is the
only miss behind criteria 1 and 5 as well, which is why both sit exactly on
target with no margin.

**Evidence.**

- `results/diagnosis_q2.txt` (`diagnose_q2.py`) — one check per stage. The
  tickets paragraph alone is 0.545 against 0.731 for the whole chunk
  (chunking). Rewording Q2 in the chunk's own terms moved it to 8th but further
  away, 0.761, so wording alone doesn't explain it (embedding). A keyword
  ranking (BM25) puts the chunk 2nd instead of 11th (retrieval) — a second
  route to the same chunk, not the cause.
- `results/chunking_comparison.txt` (`compare_chunkings.py`) — six ways of
  cutting the same guides, scored the same way. Cutting by paragraph moves Q2
  from 11th to 1st at 0.545, under the cutoff; but it also moves Q4's answer
  from 3rd to 6th, because four of the newly split cross-cutting paragraphs —
  two about winter, two about Thornby Wells being easy to get around — get
  sharper and crowd it out. No chunk size wins everywhere: coarser chunks blur,
  finer ones lose context.

## The Improvement

**What I changed:** one thing. `chunker.py::split_documents` now cuts each
`##` section into its paragraphs, and every paragraph keeps the
`Guide > Section:` prefix (commit `dd8a7a1`). The unit 1 version is kept as
`chunker.py::split_by_section`. The prompt, the 0.56 cutoff, top-k 5 and the
embedding model are unchanged. That makes 115 chunks instead of 94: all 72
town-guide chunks are identical to before, and the 22 cross-cutting chunks
became 43.

**Why I picked it:** the diagnosis puts the criterion 2 miss in chunking — Q2's
answer shares the railway section's chunk with the timetable, which pulls it
down to 11th — so the fix gives each idea its own chunk; the comparison
predicted it would move Q2 to 1st at 0.545, under the cutoff.

### The two alternatives, measured

Both simulated on the unit 1 system, in memory, with nothing in the pipeline
changed: `simulate_alternatives.py`, output in `results/alternatives.txt`.

**B. Hybrid search** — blend the meaning ranking with a BM25 keyword ranking
(reciprocal rank fusion) and keep the top five. It does what retrieval can:
Q2's answer enters its top five, because BM25 ranks that chunk 2nd. But the
gate still judges the best *meaning-based* distance among the five, which for
Q2 is 0.625, over the 0.56 cutoff — so Q2 is still refused, the refusal still
names no file, and criterion 2 stays at 4 of 5. Making it count would take a
second change, a gate that understands fused scores with a new cutoff to
calibrate, which unit 2 doesn't allow. And it acts at retrieval, not at the
chunking stage the diagnosis points to.

**C. Helpful refusal** — when the gate refuses, restate the question, say the
answer isn't there, and point to the files of the closest chunks. It would
lift criterion 2 to 5 of 5, since the refusal would name files. But for Q2
those files are `guide_marchwood.md`, `guide_kestrelford.md` and
`guide_eating.md` — none of them the one with the answer,
`guide_regional_transport.md` — and it would send "What is the capital of
Mongolia?" to Corry Vale. It treats the symptom, a refusal with no source, and
leaves the cause, a buried answer, in place; its pointers would need their own
cutoff before they stopped misleading. It's still how I'd want a refusal to
read, so it's first on my list of next steps.

### Run Log — After

`python run_eval.py --label after`: the same five questions, three runs each,
caching off, cutoff 0.56, top-k 5. The run log is
`results/run_2026-09-27_1734_after.md`, added up by `summarize_run.py::summarize`
into `results/run_2026-09-27_1734_after_criteria.md`. Criterion 4 was
re-measured on the new chunks (`results/chunk_review_after.md`): Part B now
has 43 chunks, not 22, and 42 of them pass, which clears the original target
whether "15 of 22" is read as a count or as a share (68% of 43 is 30).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1. Retrieved chunk contains the answer | 4 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunks can answer a question on their own | 60 of 72 and 15 of 22 | 63 · 42 of 43 | 63 · 42 of 43 | 63 · 42 of 43 | MET |
| 5. Answers are factual, precise and concise | 4 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | MET |

**The two questions that changed, run 1**, copied unedited from the run log
(`run_eval.py::run_once`, answers by `generate.py::answer_from_chunks`). The
other three answered as before; all fifteen answers are in the log.

```text
Q2  How far ahead should I book train tickets to get the cheapest fare?  (best distance 0.545, passed the gate)
Train tickets are considerably cheaper when booked a week ahead compared to booking them the day before. 

Source: guide_regional_transport.md

Q4  Which town is the best place to visit in winter?  (best distance 0.535, passed the gate)
Based on the provided documents, there is no mention of which town is the "best" place to visit in winter. However, the documents state that Brightwater carries on during the winter because the university keeps it occupied, while Halden Bay largely closes and Kestrelford can be cut off by snow (guide_seasons.md).
```

**Criterion 4 after the change**, from `review_chunks.py::count`
(`python review_chunks.py --label after --count`):

```text
Part A (town guides): 63 of 72 pass at 4+ of 5
Part B (cross-cutting guides): 42 of 43 pass at 4+ of 5
Spot-check: you agreed with Claude on 8 of 10
```

The new spot-check (`results/chunk_spotcheck_after.md`, same seed) drew ten
chunks from the 115. I disagreed on S3, a copy of the repeated "Practical
notes" paragraph, for the same reason as the first time, and on S5, the
accessibility guide's intro, which doesn't suit an Overview — the same chunk
and the same marks I agreed with in the first spot-check.

`summarize_run.py` flagged all three Q4 answers for a person to read, since
none contains "Marchwood" and none is a refusal. I read them: they're honest
about what they were given — `guide_seasons.md` compares no towns, so nothing
in it can say which one is best — but they aren't the answer. Thornby Wells is
the region's most reliable winter destination "after Marchwood", so Marchwood
is first. The scorer's fails stand.

**Did it help?** Yes, for the criterion it was aimed at — and it cost another
question. Criterion 2 went from 4 of 5 in every run to 5 of 5 in every run:
Q2's tickets paragraph now ranks 1st at 0.545, passes the gate, and every
answer names `guide_regional_transport.md`. Criteria 1 and 5 stayed at 4 of
5, but the miss moved from Q2 to Q4. Splitting the cross-cutting sections made
their paragraphs sharper; four of the new ones — two about winter, two about
Thornby Wells being easy to get around — now sit in Q4's top five (best
0.535), and the chunks that name Marchwood fell to 6th and below. With them gone, the
model said the documents don't name a best winter town and summarised
`guide_seasons.md` instead — honest, but not the answer. Criterion 3 didn't
move (5 of 5, nearest out-of-scope still 0.818), and criterion 4's
cross-cutting part rose from 21 of 22 to 42 of 43. The paragraphs also sit
closer to the questions they answer: Q3's best distance fell from 0.292 to
0.195 and Q5's from 0.346 to 0.279.

So one criterion fixed and none pushed below target, but the system's single
failing question is now Q4 instead of Q2. I know it was the chunker because
the before and after runs differ only in that one commit, and the same
`scorer.py` produced both tables.

## What's Still Broken

No criterion is missed after the fix. That isn't the same as nothing being
broken.

**Q4 now fails, in every run.** Splitting the cross-cutting sections made
their paragraphs sharper, and four of the new ones — two about winter, two
about Thornby Wells being easy to get around — now sit in Q4's top five (best
distance 0.535), pushing the two chunks that name Marchwood down to 6th and
below. With nothing in front of it that compares towns, the model says the
documents don't name a best winter town. Criteria 1 and 5 hold at 4 of 5 only
because Q4 is the single miss — the same zero margin Q2 used to cause. The
system still has one failing question; it's just a different one.

What I'd do next, and why I stopped:

1. **Short, helpful refusals** — the behaviour I asked for in Step 9, before
   any results. When the answer isn't in what was retrieved, say so in one
   line and name where to look, then stop. The after-run Q4 answers did the
   first half and then kept summarising the seasons guide; the gate's refusal
   does neither. The simulation in `results/alternatives.txt` says the
   pointers need their own cutoff first: for Q2 they'd have pointed to three
   files, none of them the right one.
2. **A retrieval change aimed at Q4** — top-k 6, or hybrid search. With
   paragraph chunks, Thornby Wells › When to go sits 6th at 0.575, so top-k 6
   would put a Marchwood-naming chunk in front of the model without touching
   the gate; hybrid search brought Q2's answer into its top five in
   simulation. Neither is tested, and either could break something else, so
   each needs its own before-and-after run.

I stopped because unit 2 allows one change, and I spent it on the stage my
diagnosis pointed to. A second change in the same run would have made the
before-and-after comparison impossible to read.

**Refusals are either bare or long-winded.** The gate's refusal is a fixed
sentence that names no file — that's what missed criterion 2 before the fix.
The model's own refusals (the Milestone 4 probe, Q4 after the fix) name files
but go on for a paragraph. Neither restates the question or says which part of
it the documents don't cover.

**The corpus contradicts itself, and the system just repeats it.** The
hospital conflict is handled, because Q5 was built to test it and the model
reports both sides. Others aren't: Marchwood's guide says trains to
Brightwater run "every 40 minutes until 11pm" where Brightwater's and the
transport guide say eleven a day, and the walking guide gives Corry Vale's
"not gritted above the second village" to Kestrelford. Nothing in the pipeline
notices a contradiction; an answer built from one of those chunks states it as
fact.

**The gate only catches questions from another world.** Criterion 3 is 5 of
5, but its out-of-scope questions sat at 0.818 and up. Questions the corpus
can't answer but sounds like it could — vegetarian restaurants in Kestrelford
(0.371), the last Marchwood airport bus (0.377) — pass the gate at any
sensible cutoff, and only the prompt stands between them and a guess.

## What I'd Do Differently

### The criteria I'd write differently

1. **Criterion 4, check 1 ("answerable alone").** I wrote "a question about
   its topic", and it reads two ways: *any* single question (Claude's reading —
   "is cash useful here?") or a *specific* question the chunk as a whole
   answers (mine). That's why I disagreed with Claude on the "Practical notes"
   chunks in both audits. I'd write: "Using only this chunk, someone could
   correctly answer one specific question about its heading."
2. **Criterion 4, check 3 ("one line of ideas").** I judged the same chunk —
   the accessibility guide's intro, with the same marks — differently in the
   two audits: I agreed the first time and disagreed the second. A check I
   can't answer the same way twice isn't measuring anything. I'd define
   "serves its heading" with one example that passes and one that fails, or
   drop the check.
3. **Criterion 4, check 4 ("concrete").** Counting digits, number words, days
   and months missed chunks that are full of facts without a number in them —
   Elder Ness › What to see ("spring and autumn migration") fails it. I'd count
   named places and seasons too.
4. **Criterion 4's targets.** 60 of 72 and 15 of 22 were what I expected, not
   what good looks like; ideally both would be 90–100%. I only asked about that
   after I'd seen the count, when raising them would have been moving the
   goalposts the other way, so they stayed. And "15 of 22" stopped fitting as
   soon as the chunk count changed to 43 — I'd write it as a share.
5. **Criterion 3.** Questions from another world (Mongolia, Rust) were never
   close to the cutoff, so 5 of 5 tested almost nothing. I'd use near misses —
   questions about these towns the guides can't answer — and measure the whole
   system's refusal, gate and prompt together, because the gate alone can't
   catch them.
6. **Criterion 5's word limit.** 80 words per fact was generous on purpose,
   but so generous it never came close: the longest answer in either run was
   54 words. I'd set it near 40.
7. **Criteria 1 and 5, and the questions behind them.** "4 of 5" because 3 of
   5 felt average — but with only five questions, one hard question decided
   both criteria, before the fix and after it. I'd write ten or more. And I'd
   pick `expects` phrases that appear only in the answer: "Tuesday" is also in
   two chunks about Brightwater's Tuesday market, "a week ahead" in two about
   booking Sunday lunch, and "Marchwood" in 17 of 115 chunks, so criterion 1's
   text match could pass on the wrong chunk. None did, but nothing stopped it.

### What was hard, and what I'd change about how I worked

- **Two projects in one weekend.** I joined the course at the start of unit 2,
  so project 1 and project 2 had to be built in order, in the same repo, with
  the link due Monday and everything due Wednesday.
- **Judging answers without reading the whole corpus.** At first I couldn't
  see how I could give real input on documents I hadn't read. The answer key
  at the top of this README — each question, the section that answers it, and
  the exact sentence — is what made it possible: I compared answers to one
  row, not to fourteen guides. But I'd still read one town guide and one
  cross-cutting guide first next time. I only saw the "two ideas under one
  heading" problem when I looked at the railway chunk myself.
- **Two AI models in one project.** Gemini writes the answers and Claude was
  helping me build and check the system, and I was worried the two would get
  mixed up. The rule that fixed it: Gemini is the system under test, the
  scorer is plain text matching, and Claude never decides whether an answer is
  right — where a match can't be trusted, the answer is shown to me.
- **Thinking in hyperparameters.** I kept wanting to tune numbers until they
  looked right. The lesson was about timing: a target is written and committed
  before the measurement and never moved. I nearly broke that twice — asking
  about 90% chunk targets after the count, and proposing a 0.61 cutoff, which
  would have let through the very question my rule said to refuse.
- **Numbers I couldn't picture.** Distances meant nothing to me until I saw
  them next to questions: an unanswerable question about vegetarian
  restaurants in Kestrelford (0.371) sits closer than my real tearoom question
  (0.379). That's when it clicked that distance measures topic, not whether the
  answer exists.
- **Marking 94 chunks by hand.** It wasn't realistic, so Claude marked the
  judgment checks against my rubric and I audited ten at random, twice. It
  worked, but the audits showed my own checks weren't as clear as I'd thought.
- **Defaults I never chose.** I only asked where "top 5" came from in the
  diagnosis step. Next time I'd list every inherited default at the start —
  top-k, the embedding model, the prompt — and decide which ones I'm actually
  choosing.
