# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

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
|---|---|---|---|---|
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

```
Getting around the region with limited mobility > Overview: An honest assessment rather than a promotional one. Some of these places are difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
Corry Vale > Where to stay: Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
Givens Mill > Getting around: Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
Kestrelford > What to see: The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
Pellew Sands > When to go: June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```

## Sample Answer

Produced by `python app.py ask "Where is the nearest full hospital?"` at cutoff
0.56, copied unedited. The full run, including the exact prompt the model was
sent (`--show-prompt`), is in `results/milestone4_sample_answer.txt`.

**Question:** Where is the nearest full hospital?

**Answer:**

```
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
|---|---|---|---|
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
correct, precise, concise, coherent — into a five-check rubric, which I
approved before anything was marked. A script marks the three mechanical
checks; Claude marked the two that need reading, 188 marks in all, 3 of them
N, each with a reason. I audited ten chunks drawn at random with a fixed seed
and agreed on 8. I disagreed on two copies of the repeated "Practical notes"
paragraph: Claude called them answerable on their own because you could ask
whether cash is useful, but to me they jump from cash to mobile coverage to
hospitals and answer no specific question. That disagreement showed check 1's
wording can be read two ways, which I'm leaving on record for Unit 2 rather
than rewording after the count.

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

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
