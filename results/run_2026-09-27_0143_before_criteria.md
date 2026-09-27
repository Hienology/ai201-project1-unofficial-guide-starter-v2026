# Criteria — run_2026-09-27_0143_before

- Produced by: `summarize_run.py::summarize`, from `results/run_2026-09-27_0143_before.md`, with the checks in `scorer.py`
- Criteria 1, 3 and 4 are deterministic, so the same number fills every run column.
- Criterion 4 is town guides · cross-cutting guides.
- The verdict is left blank: MET or MISSED is the student's call.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1. Retrieved chunk contains the answer | 4 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | |
| 2. Every answer names a source | 5 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | |
| 4. Chunks can answer a question on their own | 60 of 72 and 15 of 22 | 63 of 72 · 21 of 22 | 63 of 72 · 21 of 22 | 63 of 72 · 21 of 22 | |
| 5. Answers are factual, precise and concise | 4 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | |

## Every answer

Criterion 1 is per question; the rest are per answer. Criterion 5 stops at
the first check that fails: factual, then precise, then concise.

| Question | Run | 1 Retrieved | 2 Names a file | 5 Factual | 5 Precise | 5 Words | Refusal | 5 Pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | 1 | yes | yes | yes | yes | 11/80 | no | yes |
| Q1 | 2 | yes | yes | yes | yes | 11/80 | no | yes |
| Q1 | 3 | yes | yes | yes | yes | 9/80 | no | yes |
| Q2 | 1 | **no** | **no** | **no** | yes | 7/80 | yes | **no** |
| Q2 | 2 | **no** | **no** | **no** | yes | 7/80 | yes | **no** |
| Q2 | 3 | **no** | **no** | **no** | yes | 7/80 | yes | **no** |
| Q3 | 1 | yes | yes | yes | yes | 23/80 | no | yes |
| Q3 | 2 | yes | yes | yes | yes | 23/80 | no | yes |
| Q3 | 3 | yes | yes | yes | yes | 23/80 | no | yes |
| Q4 | 1 | yes | yes | yes | yes | 37/160 | no | yes |
| Q4 | 2 | yes | yes | yes | yes | 46/160 | no | yes |
| Q4 | 3 | yes | yes | yes | yes | 39/160 | no | yes |
| Q5 | 1 | yes | yes | yes | yes | 26/160 | no | yes |
| Q5 | 2 | yes | yes | yes | yes | 26/160 | no | yes |
| Q5 | 3 | yes | yes | yes | yes | 25/160 | no | yes |

Questions: Q1 Which day of the week is the Givens Mill tearoom closed? · Q2 How far ahead should I book train tickets to get the cheapest fare? · Q3 When does the Halden Bay coastal path get closed? · Q4 Which town is the best place to visit in winter? · Q5 Where is the nearest full hospital?

## For a person to read

Nothing: every answer either matched its phrase or was a refusal.
