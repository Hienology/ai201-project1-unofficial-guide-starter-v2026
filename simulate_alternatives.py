#!/usr/bin/env python3
"""
The two fixes not picked in unit 2, simulated against the unit 1 system.

    python simulate_alternatives.py    prints the report and writes results/alternatives.txt

Unit 2 allows one change, and the one made was paragraph chunking. These are
the other two candidates, measured rather than guessed, on the system as it
was before the change: one chunk per `##` section (`split_by_section`), top 5,
the 0.56 gate. Everything runs in memory; nothing here changes the pipeline.

  B  hybrid search — blend the meaning ranking with a keyword ranking (BM25)
     by reciprocal rank fusion, keep the top 5, and let the gate judge them
     exactly as it does now: by the best meaning-based distance among them.
  C  helpful refusal — when the gate refuses, point the reader to the files
     of the three closest chunks instead of giving no source at all.
"""

import io
import re
from contextlib import redirect_stdout

import numpy as np

import config
import questions as qs
import scorer
from chunker import split_by_section
from ingest import load_documents
from store import embed

RRF_K = 60        # the usual constant for reciprocal rank fusion
POINT_TO = 3      # how many files a helpful refusal would suggest


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


def unit(vectors) -> np.ndarray:
    v = np.array(vectors)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def report() -> None:
    from rank_bm25 import BM25Okapi

    chunks = split_by_section(load_documents())
    texts = [c.text for c in chunks]
    cv = unit(embed(texts))
    bm25 = BM25Okapi([words(t) for t in texts])
    k, cutoff = config.TOP_K, config.THRESHOLD

    items = qs.answered()
    rows = [(f"Q{i}", q["question"], q["expects"]) for i, q in enumerate(items, 1)]
    rows += [(f"O{i}", q, None) for i, q in enumerate(qs.OUT_OF_SCOPE, 1)]
    qv = unit(embed([r[1] for r in rows]))

    print(f"Unit 1 system: {len(chunks)} section chunks, top {k}, gate cutoff {cutoff}.\n")
    print("B · HYBRID SEARCH — top 5 by reciprocal rank fusion of meaning and BM25 ranks;")
    print("    the gate still judges the best meaning-based distance among those five.")
    print(f"    {'':<4}{'answer in top 5':>30}   {'gate (best distance)':>30}")
    print(f"    {'':<4}{'today':>14}{'hybrid':>16}   {'today':>14}{'hybrid':>16}")
    refused_today = []
    for (name, question, expects), q in zip(rows, qv):
        dist = 1 - cv @ q
        sem_rank = {j: n for n, j in enumerate(np.argsort(dist), 1)}
        scores = bm25.get_scores(words(question))
        kw_rank = {j: n for n, j in enumerate(np.argsort(-scores), 1)}
        fused = sorted(range(len(chunks)),
                       key=lambda j: -(1 / (RRF_K + sem_rank[j]) + 1 / (RRF_K + kw_rank[j])))
        today, hybrid = list(np.argsort(dist)[:k]), fused[:k]

        def found(top):
            if expects is None:
                return "—"
            return "yes" if any(scorer.contains_phrase(texts[j], expects) for j in top) else "no"

        def gate(top):
            best = min(dist[j] for j in top)
            return f"{'pass' if best < cutoff else 'refused'} ({best:.3f})"

        print(f"    {name:<4}{found(today):>14}{found(hybrid):>16}   {gate(today):>14}{gate(hybrid):>16}")
        if min(dist[j] for j in today) >= cutoff:
            refused_today.append((name, question, expects, today))

    print("\nC · HELPFUL REFUSAL — for each question the gate refuses today, the files a")
    print(f"    refusal would point to (the {POINT_TO} closest chunks), and whether any holds the answer:")
    for name, question, expects, today in refused_today:
        files = list(dict.fromkeys(chunks[j].source for j in today))[:POINT_TO]
        if expects:
            # The answer key's files, not a phrase search: "a week ahead" also
            # turns up in the eating guide, about booking Sunday lunch.
            answer_files = scorer.RULES[question]["allowed"]
            holds = [f for f in files if f in answer_files]
            verdict = (f"answer file ({', '.join(answer_files)}) among them: "
                       f"{'yes' if holds else 'no'}")
        else:
            verdict = "no answer exists in the corpus"
        print(f"    {name}  {question}")
        print(f"        would point to: {', '.join(files)} — {verdict}")


def main():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        report()
    text = buffer.getvalue()
    print(text, end="")
    out = config.RESULTS_DIR / "alternatives.txt"
    out.write_text(text, encoding="utf-8")
    print(f"\nWrote {out.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
