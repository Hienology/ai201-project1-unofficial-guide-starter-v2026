#!/usr/bin/env python3
"""
Turn one `run_eval.py` log into the per-criterion run log the README asks for.

    python summarize_run.py                         the newest results/run_*.md
    python summarize_run.py results/run_..._before.md

`run_eval.py` writes one row per *question*. The README's run log is one row per
*criterion*, and this does that adding up, using the same checks as `judge` in
scorer.py. It writes `<log>_criteria.md` next to the log.

Where each number comes from:

  1  retrieval, re-run here for each question. Retrieval is deterministic, so
     it's the same in every run, like criterion 3.
  2  the answers in the log: does each name a file?
  3  the log's own out-of-scope section, one deterministic pass.
  4  `review_chunks.py`'s count. Chunking is deterministic too.
  5  the answers in the log, through `scorer.check_answer`.

It fills in numbers, not verdicts. MET or MISSED is the student's call.
Answers a text match can't be trusted on — the wrong phrase but not a refusal,
which is where a correct paraphrase would land — are listed at the end for a
person to read.
"""

import argparse
import os
import re
import sys
from pathlib import Path

import config
import questions as qs
import scorer

TARGETS = {
    "1": ("Retrieved chunk contains the answer", "4 of 5"),
    "2": ("Every answer names a source", "5 of 5"),
    "3": ("Gate stops out-of-corpus questions", "4 of 5"),
    "4": ("Chunks can answer a question on their own", "60 of 72 and 15 of 22"),
    "5": ("Answers are factual, precise and concise", "4 of 5"),
}

ENTRY = re.compile(
    r"^### (?P<question>[^\n]+) — run (?P<run>\d+)\n\n"
    r"- Best distance: (?P<distance>[\d.]+) \((?P<gate>passed|refused by) the gate\)\n"
    r"- Sources retrieved: (?P<sources>[^\n]*)\n\n"
    r"```\n(?P<answer>.*?)\n```",
    re.M | re.S,
)


def parse_log(text: str) -> dict:
    top_k = re.search(r"top-k: (\d+)", text)
    variant = re.search(r"index variant `([^`]+)`", text)
    corpus = re.search(r"- Corpus: `([^`]+)`", text)
    refused = re.search(r"Refused (\d+) of (\d+)\.", text)
    entries = [
        {**m.groupdict(), "run": int(m["run"]), "distance": float(m["distance"])}
        for m in ENTRY.finditer(text)
    ]
    if not entries:
        sys.exit("Found no answers in that log. Is it a run_eval.py log?")
    return {
        "top_k": int(top_k[1]) if top_k else config.TOP_K,
        "variant": variant[1] if variant else "default",
        "corpus": corpus[1] if corpus else config.CORPUS,
        "refused": (int(refused[1]), int(refused[2])) if refused else None,
        "entries": entries,
    }


def summarize(path: Path) -> str:
    from store import search
    import review_chunks

    log = parse_log(path.read_text(encoding="utf-8"))
    items = qs.answered()
    expects = {q["question"]: q["expects"] for q in items}
    short = {q["question"]: f"Q{i}" for i, q in enumerate(items, 1)}
    runs = sorted({e["run"] for e in log["entries"]})

    missing = [q for q in expects if q not in scorer.RULES]
    if missing:
        sys.exit(f"scorer.RULES has no rule for: {missing}")

    # Criterion 1: retrieval, which doesn't change between runs.
    retrieved = {
        q: scorer.retrieval_has_answer(
            e, search(q, top_k=log["top_k"], corpus=log["corpus"], variant=log["variant"])
        )
        for q, e in expects.items()
    }

    # Criterion 4: the chunk review.
    rows = review_chunks.score_all(log["corpus"])
    parts = {p: [r for r in rows if r["part"] == p] for p in ("A", "B")}
    c4 = " · ".join(f"{sum(r['passed'] for r in g)} of {len(g)}" for g in parts.values())

    checked = []
    for e in log["entries"]:
        result = scorer.check_answer(e["question"], expects[e["question"]], e["answer"])
        checked.append({**e, **result, "named": scorer.names_a_source(e["answer"])})

    def per_run(key):
        return [f"{sum(c[key] for c in checked if c['run'] == r)} of "
                f"{sum(1 for c in checked if c['run'] == r)}" for r in runs]

    c1 = f"{sum(retrieved.values())} of {len(retrieved)}"
    c3 = f"{log['refused'][0]} of {log['refused'][1]}" if log["refused"] else "—"
    cells = {
        "1": [c1] * len(runs),
        "2": per_run("named"),
        "3": [c3] * len(runs),
        "4": [c4] * len(runs),
        "5": per_run("passed"),
    }

    run_heads = " | ".join(f"Run {r}" for r in runs)
    lines = [
        f"# Criteria — {path.stem}",
        "",
        f"- Produced by: `summarize_run.py::summarize`, from `{os.path.relpath(path, config.ROOT)}`, "
        f"with the checks in `scorer.py`",
        f"- Criteria 1, 3 and 4 are deterministic, so the same number fills every run column.",
        f"- Criterion 4 is town guides · cross-cutting guides.",
        "- The verdict is left blank: MET or MISSED is the student's call.",
        "",
        f"| Criterion | Target | {run_heads} | Verdict |",
        "| " + " | ".join("---" for _ in range(len(runs) + 3)) + " |",
    ]
    for k, (name, target) in TARGETS.items():
        lines.append(f"| {k}. {name} | {target} | {' | '.join(cells[k])} | |")

    lines += [
        "",
        "## Every answer",
        "",
        "Criterion 1 is per question; the rest are per answer. Criterion 5 stops at",
        "the first check that fails: factual, then precise, then concise.",
        "",
        "| Question | Run | 1 Retrieved | 2 Names a file | 5 Factual | 5 Precise | 5 Words | Refusal | 5 Pass |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    yn = {True: "yes", False: "**no**"}
    for c in checked:
        lines.append(
            f"| {short[c['question']]} | {c['run']} | {yn[retrieved[c['question']]]} | "
            f"{yn[c['named']]} | {yn[c['factual']]} | {yn[c['precise']]} | "
            f"{c['words']}/{c['limit']} | {'yes' if c['refusal'] else 'no'} | {yn[c['passed']]} |"
        )

    lines += ["", "Questions: " + " · ".join(f"{s} {q}" for q, s in short.items())]

    look = [c for c in checked if not c["factual"] and not c["refusal"]]
    wrong_files = [c for c in checked if c["factual"] and not c["precise"]]
    lines += ["", "## For a person to read", ""]
    if not look and not wrong_files:
        lines.append("Nothing: every answer either matched its phrase or was a refusal.")
    for c in look:
        lines += [
            f"**{short[c['question']]} run {c['run']}** — no `{expects[c['question']]}` "
            f"and not a refusal. A correct paraphrase would land here.",
            "", "```text", c["answer"], "```", "",
        ]
    for c in wrong_files:
        allowed = scorer.RULES[c["question"]]
        lines += [
            f"**{short[c['question']]} run {c['run']}** — right phrase, but names "
            f"{', '.join(c['files'])}; allowed: {', '.join(allowed['allowed'][:3])}"
            f"{' …' if len(allowed['allowed']) > 3 else ''}"
            + (f" (must include {allowed['required']})" if allowed["required"] else ""),
            "",
        ]
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Per-criterion run log from a run_eval.py log.")
    parser.add_argument("log", nargs="?", type=Path, help="a results/run_*.md file")
    args = parser.parse_args()

    if args.log:
        path = args.log if args.log.is_absolute() else config.ROOT / args.log
    else:
        logs = sorted(p for p in config.RESULTS_DIR.glob("run_*.md")
                      if not p.stem.endswith("_criteria"))
        if not logs:
            sys.exit("No results/run_*.md yet. Run `python run_eval.py --label before` first.")
        path = logs[-1]

    report = summarize(path)
    out = path.with_name(f"{path.stem}_criteria.md")
    out.write_text(report, encoding="utf-8")
    print(report)
    print(f"Wrote {os.path.relpath(out, config.ROOT)}")


if __name__ == "__main__":
    main()
