"""
What counts as a correct answer, written down as code.

`run_eval.py` finds this file on its own and calls `judge` once per answer, so
the Run columns in its table carry criterion 5's verdict — the criterion about
whether the answer is actually right. Criteria 1 and 2 come from the same checks,
added up per run by `summarize_run.py`.

Every rule here is plain text matching, on purpose. Nothing in this file asks a
model whether an answer is good: the system under test is a model, and grading
it with another one would make the grade as uncertain as the thing it grades.
The price is that a correct answer worded differently from the `expects` phrase
("seven days before" for "a week ahead") fails. `summarize_run.py` lists every
such answer for a person to read rather than deciding it here.

The rules come from criteria.md:

  Criterion 2  every answer names at least one source file. A refusal counts
               as an answer, so a refusal that names no file fails.
  Criterion 5  an answer passes only if it clears three checks, in order:
                 factual  — contains the question's `expects` phrase
                 precise  — every file it names is allowed for that question
                            (naming none is fine here; criterion 2 covers it)
                 concise  — at most 80 words per fact the question needs
               A refusal never contains the `expects` phrase, so it fails.
"""

import re

WORDS_PER_FACT = 80

# Criterion 5's table, from criteria.md: the files that count as a correct
# reference for each question, the one that must be among them (if any), and how
# many facts a correct answer needs.
TOWN_GUIDES = [
    f"guide_{town}.md"
    for town in ("brightwater", "corry_vale", "elder_ness", "givens_mill",
                 "halden_bay", "kestrelford", "marchwood", "pellew_sands",
                 "thornby_wells")
]

RULES = {
    "Which day of the week is the Givens Mill tearoom closed?": {
        "allowed": ["guide_givens_mill.md"], "required": None, "facts": 1,
    },
    "How far ahead should I book train tickets to get the cheapest fare?": {
        "allowed": ["guide_regional_transport.md"], "required": None, "facts": 1,
    },
    "When does the Halden Bay coastal path get closed?": {
        "allowed": ["guide_halden_bay.md", "guide_walking.md",
                    "guide_regional_transport.md"],
        "required": None, "facts": 1,
    },
    "Which town is the best place to visit in winter?": {
        "allowed": ["guide_marchwood.md", "guide_thornby_wells.md"],
        "required": None, "facts": 2,
    },
    "Where is the nearest full hospital?": {
        "allowed": ["guide_accessibility.md", *TOWN_GUIDES],
        "required": "guide_accessibility.md", "facts": 2,
    },
}

_FILE = re.compile(r"(?<![\w-])[\w-]+\.(?:md|txt)\b")
_REFUSAL = re.compile(
    r"\b(?:don't|do not|doesn't|does not|not) (?:have )?enough information\b",
    re.IGNORECASE,
)


def contains_phrase(text: str, phrase: str) -> bool:
    """
    Does `text` contain `phrase` as whole words, ignoring capitals?

    "Tuesdays" and "TUESDAY" match `Tuesday`, and "High winds" matches
    `high wind`, but "Tuesdayish" and "highwind" don't. Capitals are ignored
    because none of this project's phrases changes meaning with them — a plain
    match can't tell Drinkwater the surname from drinkwater the typo, so a
    phrase where that mattered would need a person to read it.
    """
    words = [re.escape(w) for w in phrase.split()]
    pattern = r"(?<![A-Za-z0-9])" + r"\s+".join(words) + r"s?(?![A-Za-z0-9])"
    return re.search(pattern, text, re.IGNORECASE) is not None


def files_named(answer: str) -> list[str]:
    """Every source file the answer mentions, in order, without repeats."""
    return list(dict.fromkeys(_FILE.findall(answer)))


def is_refusal(answer: str) -> bool:
    """The gate's refusal, or the model saying the same thing in its own words."""
    return _REFUSAL.search(answer) is not None


def retrieval_has_answer(expects: str, results) -> bool:
    """Criterion 1: does any retrieved chunk contain the `expects` phrase?"""
    return any(contains_phrase(r.text, expects) for r in results)


def names_a_source(answer: str) -> bool:
    """Criterion 2: does the answer name at least one file?"""
    return bool(files_named(answer))


def check_answer(question: str, expects: str, answer: str) -> dict:
    """Criterion 5's three checks for one answer, and which one failed first."""
    rule = RULES[question]
    files = files_named(answer)
    words = len(answer.split())
    limit = WORDS_PER_FACT * rule["facts"]

    factual = contains_phrase(answer, expects)
    precise = all(f in rule["allowed"] for f in files) and (
        rule["required"] is None or not files or rule["required"] in files
    )
    concise = words <= limit

    first_failure = next(
        (name for name, ok in (("factual", factual), ("precise", precise),
                               ("concise", concise)) if not ok),
        None,
    )
    return {
        "factual": factual,
        "precise": precise,
        "concise": concise,
        "passed": first_failure is None,
        "first_failure": first_failure,
        "files": files,
        "words": words,
        "limit": limit,
        "refusal": is_refusal(answer),
    }


def judge(question: str, expects: str, answer: str, results) -> bool:
    """Criterion 5: is this answer factual, precisely sourced and concise?"""
    return check_answer(question, expects, answer)["passed"]
