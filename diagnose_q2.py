#!/usr/bin/env python3
"""
Why does Q2 miss? Three checks, one per possible cause, for the diagnosis.

    python diagnose_q2.py        prints the report and writes results/diagnosis_q2.txt

Q2 ("How far ahead should I book train tickets to get the cheapest fare?") is
the one question whose answer isn't in its top five chunks, and the reason
criterion 2 is missed. The course's quick test puts the problem before
generation, so each check here looks at an earlier stage, and none of them
changes the system:

  A  chunking   — the railway chunk holds two ideas. How close is each half?
  B  embedding  — does the question share words with the answer chunk, and
                  does asking in the chunk's own words move it?
  C  retrieval  — where would a keyword ranking (BM25) put the answer chunk?

No model calls. The checks are ordered by pipeline stage, not by likelihood.

It diagnoses the unit 1 system — one chunk per `##` section, from
`chunker.py::split_by_section` — and ranks those chunks in memory rather than
through the index, so the evidence still reproduces after unit 2 re-chunks.
"""

import io
import math
import re
from contextlib import redirect_stdout
from types import SimpleNamespace

import config
from chunker import split_by_section
from ingest import load_documents
from store import embed

QUESTION = "How far ahead should I book train tickets to get the cheapest fare?"
ANSWER_LABEL = "guide_regional_transport.md#0"
REWORDED = "How far ahead should I book railway tickets to get them cheaper?"
STOPWORDS = {"how", "far", "should", "i", "to", "get", "the", "a", "an", "them"}


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


def distance(a: str, b: str) -> float:
    """Cosine distance, the same measure the index uses."""
    va, vb = embed([a, b])
    dot = sum(x * y for x, y in zip(va, vb))
    return 1 - dot / (math.sqrt(sum(x * x for x in va)) * math.sqrt(sum(y * y for y in vb)))


def search(question: str, chunks, vectors) -> list:
    """Every chunk nearest-first, like `store.search`, but over `chunks` in memory."""
    (q,) = embed([question])
    qn = math.sqrt(sum(x * x for x in q))
    scored = []
    for c, v in zip(chunks, vectors):
        cos = sum(x * y for x, y in zip(q, v)) / (qn * math.sqrt(sum(y * y for y in v)))
        scored.append(SimpleNamespace(label=c.label, text=c.text, distance=1 - cos))
    return sorted(scored, key=lambda r: r.distance)


def rank_of(label: str, results) -> tuple[int, float]:
    for n, r in enumerate(results, 1):
        if r.label == label:
            return n, r.distance
    raise LookupError(label)


def report() -> None:
    chunks = split_by_section(load_documents())
    vectors = embed([c.text for c in chunks])
    answer = next(c for c in chunks if c.label == ANSWER_LABEL)
    ranked = search(QUESTION, chunks, vectors)
    top = ranked[0]
    rank, dist = rank_of(ANSWER_LABEL, ranked)

    print(f"Q2: {QUESTION}")
    print(f"Answer chunk {ANSWER_LABEL} ranks {rank} of {len(chunks)} at {dist:.3f}; "
          f"top-k is {config.TOP_K}, cutoff {config.THRESHOLD}.")
    print(f"Top hit: {top.label} at {top.distance:.3f}.\n")

    prefix, body = answer.text.split(": ", 1)
    first, second = body.split("\n\n", 1)
    print("A · CHUNKING — the answer chunk's two paragraphs, each with the same prefix:")
    print(f"    whole chunk, as indexed      {distance(QUESTION, answer.text):.3f}")
    print(f"    line and timetable paragraph {distance(QUESTION, f'{prefix}: {first}'):.3f}")
    print(f"    tickets paragraph alone      {distance(QUESTION, f'{prefix}: {second}'):.3f}")
    print(f"    (today's top hit is {top.distance:.3f}; the cutoff is {config.THRESHOLD})\n")

    q_words = sorted(set(words(QUESTION)) - STOPWORDS)
    a_words, t_words = set(words(answer.text)), set(words(top.text))
    print("B · EMBEDDING — the question's content words, as exact words:")
    for w in q_words:
        print(f"    {w:<9} answer chunk: {'yes' if w in a_words else 'no ':<4} top hit: {'yes' if w in t_words else 'no'}")
    print("    (close forms: the answer chunk has 'booked' and 'cheaper'; "
          "the top hit has 'ticket' and 'fares')")
    r2, d2 = rank_of(ANSWER_LABEL, search(REWORDED, chunks, vectors))
    print(f"    reworded in the chunk's own terms: \"{REWORDED}\"")
    print(f"    → answer chunk ranks {r2} at {d2:.3f} (was {rank}, {dist:.3f})\n")

    from rank_bm25 import BM25Okapi
    bm25 = BM25Okapi([words(c.text) for c in chunks])
    scores = bm25.get_scores(words(QUESTION))
    order = sorted(range(len(chunks)), key=lambda i: -scores[i])
    brank = next(n for n, i in enumerate(order, 1) if chunks[i].label == ANSWER_LABEL)
    print("C · RETRIEVAL — the same 94 chunks ranked by keywords (BM25, rank_bm25) instead of meaning:")
    print(f"    answer chunk ranks {brank} of {len(chunks)} (by meaning: {rank})")
    print("    BM25 top 3: " + " · ".join(chunks[i].label for i in order[:3]))


def main():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        report()
    text = buffer.getvalue()
    print(text, end="")
    out = config.RESULTS_DIR / "diagnosis_q2.txt"
    out.write_text(text, encoding="utf-8")
    print(f"\nWrote {out.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
