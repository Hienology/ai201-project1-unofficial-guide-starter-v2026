#!/usr/bin/env python3
"""
Six ways to cut the same fourteen guides, scored by the same standards.

    python compare_chunkings.py      prints the table and writes results/chunking_comparison.txt

Evidence for the diagnosis, not a change to the system: every strategy is
embedded in memory and nothing touches the index. For each one it reports,
per test question, the rank of the first chunk containing the `expects`
phrase (the same `scorer.contains_phrase` check criterion 1 uses), how many
answers land in the top k the model sees, how many questions would pass the
0.56 gate, and how close the nearest out-of-scope question gets.

Choosing a strategy because it tops this table would be fitting it to five
questions. The table is here to show the trade-off — coarser chunks carry
more context but blur, finer ones are sharp but thin — and to check the
diagnosis: splitting the railway section's two paragraphs is what moves Q2.
"""

import io
import re
import statistics
from contextlib import redirect_stdout

import numpy as np

import config
import questions as qs
import scorer
from chunker import _sections, fallback_split, split_documents
from ingest import load_documents
from store import embed


def paragraph_chunks(docs) -> list[str]:
    """Each paragraph of each section, with the section's prefix."""
    out = []
    for doc in docs:
        title, sections = _sections(doc)
        for heading, body in sections:
            out += [f"{title} > {heading}: {p.strip()}" for p in body.split("\n\n") if p.strip()]
    return out


def sentence_chunks(docs) -> list[str]:
    """Each sentence of each section, with the section's prefix."""
    out = []
    for doc in docs:
        title, sections = _sections(doc)
        for heading, body in sections:
            for p in body.split("\n\n"):
                out += [f"{title} > {heading}: {s}"
                        for s in re.split(r"(?<=[.!?])\s+", p.strip()) if s]
    return out


def unit(vectors) -> np.ndarray:
    v = np.array(vectors)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def report() -> None:
    docs = load_documents()
    strategies = {
        "whole guide": [d.text for d in docs],
        "fixed 800 (starter)": [c.text for c in fallback_split(docs, 800, 120)],
        "fixed 400": [c.text for c in fallback_split(docs, 400, 60)],
        "## section (in use)": [c.text for c in split_documents(docs)],
        "paragraph": paragraph_chunks(docs),
        "sentence": sentence_chunks(docs),
    }
    items = qs.answered()
    questions = [q["question"] for q in items] + qs.OUT_OF_SCOPE
    qv = unit(embed(questions))
    k, cutoff = config.TOP_K, config.THRESHOLD

    print(f"Top-k {k}, cutoff {cutoff}. Rank = position of the first chunk containing the")
    print("question's expects phrase. Q1 tearoom · Q2 tickets · Q3 coastal path · Q4 winter · Q5 hospital.\n")
    print(f"{'strategy':<21}{'chunks':>7}{'median words':>14}   {'Q1':>3}{'Q2':>4}{'Q3':>4}{'Q4':>4}{'Q5':>4}"
          f"   {'in top ' + str(k):>9}   {'pass gate':>9}   {'nearest out-of-scope':>20}")
    details = {}
    for name, texts in strategies.items():
        distances = 1 - qv @ unit(embed(texts)).T
        ranks, passed = [], 0
        for i, item in enumerate(items):
            order = np.argsort(distances[i])
            ranks.append(next(n for n, j in enumerate(order, 1)
                              if scorer.contains_phrase(texts[j], item["expects"])))
            passed += distances[i].min() < cutoff
        in_top = sum(r <= k for r in ranks)
        words = statistics.median(len(t.split()) for t in texts)
        print(f"{name:<21}{len(texts):>7}{words:>14.0f}   " + "".join(f"{r:>4}" for r in ranks)[1:]
              + f"   {in_top:>5} of 5   {passed:>5} of 5   {distances[len(items):].min():>20.3f}")
        details[name] = (texts, distances)

    for name in ("## section (in use)", "paragraph"):
        texts, distances = details[name]
        for i in (1, 3):  # Q2 and Q4
            print(f"\nTop {k + 1} for Q{i + 1} with {name} chunks:")
            for n, j in enumerate(np.argsort(distances[i])[: k + 1], 1):
                has = "✓" if scorer.contains_phrase(texts[j], items[i]["expects"]) else " "
                print(f"  {n} {has} {distances[i][j]:.3f}  {texts[j][:88]}")


def main():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        report()
    text = buffer.getvalue()
    print(text, end="")
    out = config.RESULTS_DIR / "chunking_comparison.txt"
    out.write_text(text, encoding="utf-8")
    print(f"\nWrote {out.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
