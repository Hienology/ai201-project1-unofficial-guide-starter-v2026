#!/usr/bin/env python3
"""
The measurement for criterion 4: a review sheet of every chunk, and a count.

    python review_chunks.py            write results/chunk_review.md
    python review_chunks.py --count    add up the marks you've filled in

The sheet lists every chunk `chunker.py::split_documents` makes, in two parts —
town guides and cross-cutting guides — because criterion 4 sets a separate
target for each. Every entry ends in `Pass: [ ]`, and you put Y or N inside the
brackets.

Deciding each mark is yours. This script only lays the chunks out and adds up
what you wrote, so the count is exactly your judgment and nobody else's.

Chunking is deterministic, so one filled-in sheet is the measurement for all
three runs in unit 2. If a unit 2 fix changes the chunker, write a fresh sheet
with `--sheet results/chunk_review_after.md` and fill that in too.
"""

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

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

PASS_RULE = (
    "**Y** = using only this chunk, someone could give a factually correct "
    "answer to a question about its topic (for a chunk covering several "
    "towns: a question about any one of them). **N** = they couldn't."
)

DEFAULT_SHEET = config.RESULTS_DIR / "chunk_review.md"


def write_sheet(path: Path, corpus: str) -> None:
    from ingest import load_documents
    from chunker import split_documents

    chunks = split_documents(load_documents(corpus))
    parts = [
        ("A", "town guides", [c for c in chunks if c.source not in CROSS_CUTTING]),
        ("B", "cross-cutting guides", [c for c in chunks if c.source in CROSS_CUTTING]),
    ]

    lines = [
        "# Chunk review — criterion 4",
        "",
        f"- Produced by: `review_chunks.py::write_sheet`, chunks from "
        f"`{chunks[0].produced_by}`",
        f"- Corpus: `{corpus}`, {len(chunks)} chunks",
        f"- Written: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"**Pass rule:** {PASS_RULE}",
        "",
        "Mark every `Pass: [ ]` as `[Y]` or `[N]`. A reason after it on the same",
        "line is optional, but worth writing for every N — unit 2's diagnoses",
        "start from them. Count with `python review_chunks.py --count`.",
    ]

    for letter, name, group in parts:
        lines += ["", f"## Part {letter} — {name} ({len(group)} chunks)"]
        for n, chunk in enumerate(group, 1):
            quoted = chunk.text.replace("\n\n", "\n>\n> ")
            lines += [
                "",
                f"### {letter}{n} · {chunk.label}",
                "",
                f"> {quoted}",
                "",
                "Pass: [ ]",
            ]

    path.parent.mkdir(exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {os.path.relpath(path, config.ROOT)}: " + ", ".join(
        f"Part {letter} {len(group)} {name}" for letter, name, group in parts
    ))


def count_sheet(path: Path) -> None:
    """Add up the Y/N marks, part by part, and list every N with its reason."""
    part = None
    entry = None
    tallies: dict[str, dict[str, int]] = {}
    names: dict[str, str] = {}
    noes: list[str] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if heading := re.match(r"## Part (\w) — (.+) \(", line):
            part = heading.group(1)
            names[part] = heading.group(2)
            tallies[part] = {"Y": 0, "N": 0, "unmarked": 0}
        elif line.startswith("### "):
            entry = line[4:]
        elif mark := re.match(r"Pass: \[(.*?)\](.*)", line):
            value = mark.group(1).strip().upper()
            key = value if value in {"Y", "N"} else "unmarked"
            tallies[part][key] += 1
            if key == "N":
                reason = mark.group(2).strip(" —-:")
                noes.append(f"  {entry}{f' — {reason}' if reason else ''}")

    for part, t in tallies.items():
        total = sum(t.values())
        print(f"Part {part} ({names[part]}): {t['Y']} of {total} marked Y  "
              f"({t['N']} N, {t['unmarked']} unmarked)")

    if noes:
        print("\nMarked N:")
        print("\n".join(noes))

    if any(t["unmarked"] for t in tallies.values()):
        print("\nSome chunks are still unmarked — the count isn't final yet.")


def main():
    parser = argparse.ArgumentParser(description="Criterion 4's chunk review sheet.")
    parser.add_argument("--count", action="store_true", help="count a filled-in sheet")
    parser.add_argument("--sheet", type=Path, default=DEFAULT_SHEET)
    parser.add_argument("--corpus", default=None)
    parser.add_argument("--force", action="store_true", help="overwrite an existing sheet")
    args = parser.parse_args()

    sheet = args.sheet if args.sheet.is_absolute() else config.ROOT / args.sheet

    if args.count:
        if not sheet.exists():
            sys.exit(f"No sheet at {sheet}. Run without --count to write one.")
        count_sheet(sheet)
        return

    if sheet.exists() and not args.force:
        sys.exit(
            f"{os.path.relpath(sheet, config.ROOT)} already exists and may have your marks "
            f"in it. Use --count to count it, or --force to start over."
        )
    write_sheet(sheet, args.corpus or config.CORPUS)


if __name__ == "__main__":
    main()
