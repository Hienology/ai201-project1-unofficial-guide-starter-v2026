# Spot-check — criterion 4

Ten of the 94 chunks, drawn by `review_chunks.py::write_spotcheck` with `random.Random(201)` so the draw can't be re-rolled.

For each one, read the chunk and Claude's marks for checks 1 and 3. Put
**Y** in `Agree: [ ]` if you agree with both marks, **N** if you disagree
with either, and a few words on why after an N.

- **1 Answerable alone** — Using only this chunk, someone could give a factually correct answer to a question about its topic (for a chunk covering several towns: a question about any one of them).
- **3 One line of ideas** — Every sentence serves the topic named in its heading.

### S1 · A4 · guide_brightwater.md#3

> Brightwater > Eat and drink: The riverside strip has six or seven places aimed squarely at visitors and priced accordingly. Two streets back, on Corry Lane, the same food costs about a third less. The Tuesday market sets up in the square from 7am and is finished by 1pm. Most kitchens in town stop serving at 9pm, earlier than visitors expect, and on Sundays many close entirely.

Claude: check 1: Y · check 3: Y

Agree: [Y]

### S2 · B20 · guide_walking.md#1

> Walking in the region > Moderate, with hills: The **Corry Vale circuit** takes in three of the four villages, about nine miles with 500 metres of ascent. The footpath network in the valley is dense and well marked. Several paths become genuinely boggy rather than merely wet outside May to September.
>
> **Givens Mill** to Brightwater along the river is three hours one way, easy underfoot, and the return needs a weekday bus.

Claude: check 1: Y · check 3: N (the Givens Mill–Brightwater walk is 'easy underfoot' along a river, not a walk with hills, and it already appears under 'Easy, on good surfaces')

Agree: [Y]

### S3 · A32 · guide_givens_mill.md#7

> Givens Mill > Practical notes: Cash is still useful at the market and in smaller places, though cards are accepted almost everywhere now. Mobile coverage is good in the centre and patchy on the outskirts. The nearest full hospital is in Brightwater; there is a minor injuries unit locally with limited hours.

Claude: check 1: Y (Y on cash and mobile coverage; its hospital line (nearest full hospital in Brightwater) contradicts guide_accessibility.md, which says Marchwood) · check 3: Y

Agree: [N] — nothing worth answering from. Incoherent theme: cash and cards -> mobile coverage -> full hospital and medical centres; more like things to take notice of, or something inconvenient, than an answer to a specific question.

### S4 · A44 · guide_kestrelford.md#3

> Kestrelford > Eat and drink: Four pubs, two cafés, and a bakery that sells out by 11am. The pubs serve food between 12 and 2 and again between 6 and 8:30, and outside those windows there is nowhere to eat at all. The bakery is the reason most people come back.

Claude: check 1: Y · check 3: Y

Agree: [Y]

### S5 · B1 · guide_accessibility.md#0

> Getting around the region with limited mobility > Overview: An honest assessment rather than a promotional one. Some of these places are difficult and it is better to know in advance.

Claude: check 1: N (no facts about any place — it describes the guide's own approach, so there is nothing to answer a question from) · check 3: Y

Agree: [Y]

### S6 · A27 · guide_givens_mill.md#2

> Givens Mill > Getting around: Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.

Claude: check 1: Y · check 3: Y

Agree: [Y]

### S7 · A72 · guide_thornby_wells.md#7

> Thornby Wells > Practical notes: Cash is still useful at the market and in smaller places, though cards are accepted almost everywhere now. Mobile coverage is good in the centre and patchy on the outskirts. The nearest full hospital is in Brightwater; there is a minor injuries unit locally with limited hours.

Claude: check 1: Y (Y on cash and mobile coverage; its hospital line (nearest full hospital in Brightwater) contradicts guide_accessibility.md, which says Marchwood) · check 3: Y

Agree: [N] — nothing worth answering from. Incoherent theme: cash and cards -> mobile coverage -> full hospital and medical centres; more like things to take notice of, or something inconvenient, than an answer to a specific question.

### S8 · A71 · guide_thornby_wells.md#6

> Thornby Wells > When to go: Year-round, genuinely. The gardens are best in May and June. The concert season runs September to April, which makes this the region's most reliable winter destination after Marchwood.

Claude: check 1: Y · check 3: Y

Agree: [Y]

### S9 · A70 · guide_thornby_wells.md#5

> Thornby Wells > Where to stay: Two large hotels from the spa period, both faded in a way some people find charming, and several small guesthouses. Prices are moderate and stable year-round.

Claude: check 1: Y · check 3: Y

Agree: [Y]

### S10 · A51 · guide_marchwood.md#2

> Marchwood > Getting around: A tram network of four lines, running every 8 minutes on weekdays and every 15 at weekends, until midnight. A day ticket costs less than two single fares and nobody tells you this at the machine. The centre is walkable but the interesting districts are not adjacent to each other.

Claude: check 1: Y · check 3: Y

Agree: [Y]

---

## Also checked by the student: checks 2, 4 and 5

Not part of the audit above — these three are marked by `review_chunks.py`, not
by Claude — but re-read by hand on the same ten chunks:

- **Check 2:** all ten pass. S2 has two paragraphs, and the second doesn't
  start with "Guide > Section".
- **Check 4:** S5 has nothing concrete. S3 and S7 are completely similar, with
  nothing noticeable beyond "a" and "cards".
- **Check 5:** S3 and S7 follow the same structure and read the same, though
  they come from different guides.

The script's marks on these ten, for comparison: check 2 Y on all ten; check 4
N on S3, S5 and S7; check 5 N on S3 and S7.
