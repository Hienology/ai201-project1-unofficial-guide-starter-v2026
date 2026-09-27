#!/usr/bin/env python3
"""
The measurement for criterion 4: five checks on every chunk, and a count.

    python review_chunks.py              write results/chunk_review.md
    python review_chunks.py --spotcheck  write results/chunk_spotcheck.md, once
    python review_chunks.py --count      count passes and spot-check agreement

Criterion 4 scores every chunk `chunker.py::split_documents` makes on five
yes/no checks and passes it at 4 or more. Checks 2, 4 and 5 are mechanical,
and this script marks them. Checks 1 and 3 need reading — is the chunk
answerable on its own, does every sentence serve its heading — and those were
marked by Claude against the same rubric, with a reason for every N, in
results/chunk_judgments.json. This script never makes a judgment call; it
copies those marks in.

The spot-check is the student's half: ten chunks drawn at random with a fixed
seed, so the draw can't be re-rolled, each showing Claude's two marks to agree
or disagree with. The agreement is reported next to the count.

Chunking is deterministic, so one sheet is the measurement for all three runs
in unit 2. Each judgment is stored with a fingerprint of the chunk's text; if
the chunker changes, marks for chunks whose text changed are dropped rather
than silently reused.
"""

import argparse
import difflib
import hashlib
import json
import os
import random
import re
import sys

import config

# The five guides that cut across towns rather than describing one. Named
# explicitly: guessing it from the headings would be one more thing to trust.
CROSS_CUTTING = {
    "guide_accessibility.md",
    "guide_eating.md",
    "guide_regional_transport.md",
    "guide_seasons.md",
    "guide_walking.md",
}

CHECKS = {
    "1": ("Answerable alone", "Claude",
          "Using only this chunk, someone could give a factually correct answer "
          "to a question about its topic (for a chunk covering several towns: a "
          "question about any one of them)."),
    "2": ("Whole unit", "script",
          'It starts with "Guide > Section:" and ends at the end of a sentence.'),
    "3": ("One line of ideas", "Claude",
          "Every sentence serves the topic named in its heading."),
    "4": ("Concrete", "script",
          "It contains a digit, a number written as a word (two to twenty, "
          "thirty, forty, fifty, hundred, thousand), a day or a month."),
    "5": ("Not repeated", "script",
          "Its text is not a near-copy (90% or more the same) of another chunk's."),
}

PASS_MARK = 4
SPOTCHECK_SIZE = 10
SPOTCHECK_SEED = 201

SHEET = config.RESULTS_DIR / "chunk_review.md"
SPOTCHECK = config.RESULTS_DIR / "chunk_spotcheck.md"
JUDGMENTS = config.RESULTS_DIR / "chunk_judgments.json"

PREFIX = re.compile(r"^[^\n>]+ > [^\n:]+: ")
NUMBER_WORDS = re.compile(
    r"\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
    r"fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|"
    r"fifty|hundred|thousand)\b",
    re.IGNORECASE,
)
# Days and months are matched case-sensitively, so the verb "may" isn't May.
CALENDAR = re.compile(
    r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|January|"
    r"February|March|April|May|June|July|August|September|October|November|"
    r"December)s?\b"
)


def _body(text: str) -> str:
    return PREFIX.sub("", text, count=1)


def fingerprint(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]


def mechanical_checks(chunks) -> dict[str, dict[str, tuple[str, str]]]:
    """Checks 2, 4 and 5 for every chunk, as {label: {check: (mark, reason)}}."""
    bodies = {c.label: _body(c.text) for c in chunks}
    copies: dict[str, list[str]] = {c.label: [] for c in chunks}
    labels = list(bodies)
    for i, a in enumerate(labels):
        for b in labels[i + 1 :]:
            matcher = difflib.SequenceMatcher(None, bodies[a], bodies[b])
            if matcher.quick_ratio() >= 0.9 and matcher.ratio() >= 0.9:
                copies[a].append(b)
                copies[b].append(a)

    marks = {}
    for c in chunks:
        body = bodies[c.label]
        whole = bool(PREFIX.match(c.text)) and c.text.rstrip().endswith((".", "!", "?"))
        concrete = bool(re.search(r"\d", body) or NUMBER_WORDS.search(body)
                        or CALENDAR.search(body))
        others = copies[c.label]
        marks[c.label] = {
            "2": ("Y", "") if whole else ("N", "doesn't start with a label or end a sentence"),
            "4": ("Y", "") if concrete else ("N", "no number, day or month in it"),
            "5": ("Y", "") if not others else (
                "N", f"near-copy of {others[0]}"
                + (f" and {len(others) - 1} others" if len(others) > 1 else "")),
        }
    return marks


def load_judgments(chunks) -> dict[str, dict[str, tuple[str, str]]]:
    """Claude's marks for checks 1 and 3, kept only where the chunk is unchanged."""
    if not JUDGMENTS.exists():
        return {}
    stored = json.loads(JUDGMENTS.read_text(encoding="utf-8"))["marks"]
    current = {c.label: fingerprint(c.text) for c in chunks}
    kept, stale = {}, []
    for label, entry in stored.items():
        if current.get(label) != entry["fingerprint"]:
            stale.append(label)
            continue
        kept[label] = {k: tuple(entry[k]) for k in ("1", "3")}
    if stale:
        print(f"Dropped {len(stale)} judgment(s) whose chunk text changed: "
              + ", ".join(stale[:5]) + (" …" if len(stale) > 5 else ""),
              file=sys.stderr)
    return kept


def score_all(corpus: str):
    """Every chunk with its part, its five marks and its score."""
    from ingest import load_documents
    from chunker import split_documents

    chunks = split_documents(load_documents(corpus))
    mechanical = mechanical_checks(chunks)
    judged = load_judgments(chunks)

    rows = []
    counters = {"A": 0, "B": 0}
    for c in chunks:
        part = "B" if c.source in CROSS_CUTTING else "A"
        counters[part] += 1
        marks = {**mechanical[c.label], **judged.get(c.label, {})}
        complete = all(k in marks for k in CHECKS)
        score = sum(marks[k][0] == "Y" for k in CHECKS if k in marks)
        rows.append({
            "id": f"{part}{counters[part]}",
            "part": part,
            "chunk": c,
            "marks": marks,
            "score": score,
            "complete": complete,
            "passed": complete and score >= PASS_MARK,
        })
    return rows


def _marks_line(row) -> str:
    cells = [f"{k} {row['marks'][k][0] if k in row['marks'] else '–'}" for k in CHECKS]
    verdict = ("**pass**" if row["passed"] else "**fail**") if row["complete"] else "unmarked"
    return f"Checks: {' · '.join(cells)} — {row['score']}/5, {verdict}"


def _reasons(row) -> list[str]:
    return [f"- {k} {CHECKS[k][0]}: {reason}"
            for k, (mark, reason) in sorted(row["marks"].items())
            if mark == "N" or reason]


def write_sheet(rows, corpus: str) -> None:
    lines = [
        "# Chunk review — criterion 4",
        "",
        f"- Produced by: `review_chunks.py::write_sheet`, chunks from "
        f"`{rows[0]['chunk'].produced_by}`, corpus `{corpus}`",
        f"- Checks 2, 4 and 5 marked by this script. Checks 1 and 3 marked by "
        f"Claude (`{os.path.relpath(JUDGMENTS, config.ROOT)}`), audited in "
        f"`{os.path.relpath(SPOTCHECK, config.ROOT)}`.",
        f"- A chunk passes at {PASS_MARK} or more of 5.",
        "",
        "| # | Check | Marked by |",
        "|---|---|---|",
    ]
    lines += [f"| {k} | **{name}** — {rule} | {who} |" for k, (name, who, rule) in CHECKS.items()]

    for part, name in (("A", "town guides"), ("B", "cross-cutting guides")):
        group = [r for r in rows if r["part"] == part]
        passed = sum(r["passed"] for r in group)
        lines += ["", f"## Part {part} — {name}: {passed} of {len(group)} pass"]
        for row in group:
            quoted = row["chunk"].text.replace("\n\n", "\n>\n> ")
            lines += ["", f"### {row['id']} · {row['chunk'].label}", "", f"> {quoted}",
                      "", _marks_line(row)]
            reasons = _reasons(row)
            if reasons:
                lines += [""] + reasons

    SHEET.parent.mkdir(exist_ok=True)
    SHEET.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {os.path.relpath(SHEET, config.ROOT)}")


def write_spotcheck(rows) -> None:
    drawn = random.Random(SPOTCHECK_SEED).sample(rows, SPOTCHECK_SIZE)
    lines = [
        "# Spot-check — criterion 4",
        "",
        f"Ten of the {len(rows)} chunks, drawn by `review_chunks.py::write_spotcheck` "
        f"with `random.Random({SPOTCHECK_SEED})` so the draw can't be re-rolled.",
        "",
        "For each one, read the chunk and Claude's marks for checks 1 and 3. Put",
        "**Y** in `Agree: [ ]` if you agree with both marks, **N** if you disagree",
        "with either, and a few words on why after an N.",
        "",
        f"- **1 {CHECKS['1'][0]}** — {CHECKS['1'][2]}",
        f"- **3 {CHECKS['3'][0]}** — {CHECKS['3'][2]}",
    ]
    for n, row in enumerate(drawn, 1):
        quoted = row["chunk"].text.replace("\n\n", "\n>\n> ")
        claude = " · ".join(
            f"check {k}: {row['marks'][k][0]}" + (f" ({row['marks'][k][1]})" if row["marks"][k][1] else "")
            if k in row["marks"] else f"check {k}: unmarked"
            for k in ("1", "3")
        )
        lines += ["", f"### S{n} · {row['id']} · {row['chunk'].label}", "", f"> {quoted}",
                  "", f"Claude: {claude}", "", "Agree: [ ]"]

    SPOTCHECK.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {os.path.relpath(SPOTCHECK, config.ROOT)} ({SPOTCHECK_SIZE} chunks)")


def count(rows) -> None:
    for part, name in (("A", "town guides"), ("B", "cross-cutting guides")):
        group = [r for r in rows if r["part"] == part]
        unmarked = sum(not r["complete"] for r in group)
        print(f"Part {part} ({name}): {sum(r['passed'] for r in group)} of {len(group)} "
              f"pass at {PASS_MARK}+ of 5" + (f"  ({unmarked} not fully marked)" if unmarked else ""))

    failing = [r for r in rows if r["complete"] and not r["passed"]]
    if failing:
        print("\nFailing chunks:")
        for r in failing:
            noes = "; ".join(f"{k} {reason or 'N'}" for k, (mark, reason) in sorted(r["marks"].items())
                             if mark == "N")
            print(f"  {r['id']} {r['chunk'].label} — {r['score']}/5: {noes}")

    if SPOTCHECK.exists():
        answers = re.findall(r"^Agree: \[(.*?)\]", SPOTCHECK.read_text(encoding="utf-8"), re.M)
        agreed = sum(a.strip().upper() == "Y" for a in answers)
        blank = sum(a.strip().upper() not in {"Y", "N"} for a in answers)
        print(f"\nSpot-check: you agreed with Claude on {agreed} of {len(answers)}"
              + (f" ({blank} still blank)" if blank else ""))


def main():
    parser = argparse.ArgumentParser(description="Criterion 4's chunk review.")
    parser.add_argument("--count", action="store_true", help="count passes and spot-check agreement")
    parser.add_argument("--spotcheck", action="store_true", help="write the spot-check sheet")
    parser.add_argument("--corpus", default=None)
    parser.add_argument("--force", action="store_true", help="overwrite an existing spot-check")
    args = parser.parse_args()

    corpus = args.corpus or config.CORPUS
    rows = score_all(corpus)

    if args.count:
        count(rows)
    elif args.spotcheck:
        if SPOTCHECK.exists() and not args.force:
            sys.exit(f"{os.path.relpath(SPOTCHECK, config.ROOT)} already exists and may "
                     f"have your answers in it. Use --force to start over.")
        write_spotcheck(rows)
    else:
        write_sheet(rows, corpus)


if __name__ == "__main__":
    main()
