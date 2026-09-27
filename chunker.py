"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below cuts on the guides' own `##` headings: one section, one
chunk, each prefixed with the guide's title and the section's heading. The
starter's version cut every document into fixed 800-character pieces, which on
city_guides meant 51 chunks that started and ended mid-word ("urs", "9p") and
ran straight across section boundaries. That version is `fallback_split`.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _sections(doc: Document) -> tuple[str, list[tuple[str, str]]]:
    """
    Break one markdown guide into its title and (heading, body) sections.

    Text between the `#` title and the first `##` is the guide's intro; it
    becomes its own section called "Overview". Hard line wraps inside a
    paragraph are joined up, since they are formatting, not meaning.
    """
    lines = doc.text.split("\n")
    if lines and lines[0].startswith("# "):
        title, body = lines[0][2:].strip(), "\n".join(lines[1:])
    else:
        title, body = doc.source.rsplit(".", 1)[0], doc.text

    parts = re.split(r"(?m)^## ", body)
    raw = [("Overview", parts[0])]
    for part in parts[1:]:
        heading, _, text = part.partition("\n")
        raw.append((heading.strip(), text))

    sections = []
    for heading, text in raw:
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text.strip())
        if text:
            sections.append((heading, text))
    return title, sections


def _windows(text: str, size: int, overlap: int) -> list[str]:
    """The safety net for a section too long to be one idea. Unused on city_guides."""
    if len(text) <= size:
        return [text]
    pieces, start = [], 0
    while True:
        pieces.append(text[start : start + size])
        if start + size >= len(text):
            return pieces
        start += size - overlap


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split each guide on its `##` headings: one section, one chunk.

    Every city_guides document is a `#` title followed by labelled sections
    ("Getting there", "Eat and drink", "When to go"), and each section is one
    self-contained idea of 158 to 691 characters. The headings already
    mark where one thought ends and the next begins, so they are the cut.

    Each chunk starts with "{title} > {heading}: ". A section read on its own
    often doesn't say which town it's about — "Buses run four times a day" —
    and the prefix puts that back without copying text from its neighbours,
    which is the job overlap does in a fixed-size chunker.

    A section longer than config.SECTION_MAX_CHARS is windowed with
    config.SECTION_OVERLAP so no chunk carries several unrelated ideas.
    """
    chunks: list[Chunk] = []
    for doc in documents:
        title, sections = _sections(doc)
        index = 0
        for heading, text in sections:
            for piece in _windows(text, config.SECTION_MAX_CHARS, config.SECTION_OVERLAP):
                chunks.append(
                    Chunk(
                        text=f"{title} > {heading}: {piece}",
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
