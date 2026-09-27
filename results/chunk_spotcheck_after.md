# Spot-check — criterion 4

Ten of the 115 chunks, drawn by `review_chunks.py::write_spotcheck` with `random.Random(201)` so the draw can't be re-rolled.

For each one, read the chunk and Claude's marks for checks 1 and 3. Put
**Y** in `Agree: [ ]` if you agree with both marks, **N** if you disagree
with either, and a few words on why after an N.

- **1 Answerable alone** — Using only this chunk, someone could give a factually correct answer to a question about its topic (for a chunk covering several towns: a question about any one of them).
- **3 One line of ideas** — Every sentence serves the topic named in its heading.

### S1 · B9 · guide_accessibility.md#8

> Getting around the region with limited mobility > Difficult: **Corry Vale** has no public transport, villages two to four miles apart, and footpaths rather than pavements. **Elder Ness** is shingle and a single street.

Claude: check 1: Y · check 3: Y

Agree: [Y]

### S2 · B28 · guide_seasons.md#1

> When to visit the region > Spring, March to May: The Kestrelford Saturday market builds back to full size through April.

Claude: check 1: Y · check 3: Y

Agree: [Y] — the Kestrelford market building back through April fits a question about what's on in the region from March to May.

### S3 · A24 · guide_elder_ness.md#7

> Elder Ness > Practical notes: Cash is still useful at the market and in smaller places, though cards are accepted almost everywhere now. Mobile coverage is good in the centre and patchy on the outskirts. The nearest full hospital is in Brightwater; there is a minor injuries unit locally with limited hours.

Claude: check 1: Y (Y on cash; Elder Ness has no market or centre (it is one street), and the hospital line contradicts guide_accessibility.md (Marchwood)) · check 3: Y

Agree: [N] — the same as in the first spot-check: nothing worth answering from; it jumps from cash to mobile coverage to hospitals.

### S4 · A36 · guide_halden_bay.md#3

> Halden Bay > Eat and drink: Seafood, unsurprisingly, and it is genuinely fresh — the boats land in the early morning and the two harbour restaurants buy directly. Prices on the harbour front are roughly double those on Fell Street, one level up, for comparable food. Everything closes by 9pm and much of it closes entirely from November to February.

Claude: check 1: Y · check 3: Y

Agree: [Y]

### S5 · B1 · guide_accessibility.md#0

> Getting around the region with limited mobility > Overview: An honest assessment rather than a promotional one. Some of these places are difficult and it is better to know in advance.

Claude: check 1: N (no facts about any place — it describes the guide's own approach, so there is nothing to answer a question from) · check 3: Y

Agree: [N] — incoherent: "An honest assessment rather than a promotional one" describes the guide, not the region, and I can't see why it suits an Overview (check 3).

### S6 · A66 · guide_thornby_wells.md#1

> Thornby Wells > Getting there: On the Marchwood line, 25 minutes from the hub, with trains every hour and every two hours on Sundays. The station is in the centre. Driving from Brightwater is 45 minutes on good roads. Parking is free for two hours everywhere in town, which is unusual and generous.

Claude: check 1: Y · check 3: Y

Agree: [Y]

### S7 · A19 · guide_elder_ness.md#2

> Elder Ness > Getting around: On foot. The village is one street. The lighthouse is a 25-minute walk along the shingle, which is harder going than the distance suggests. There is one car park at the village and parking anywhere else on the headland is prohibited and enforced.

Claude: check 1: Y · check 3: Y

Agree: [Y]

### S8 · B33 · guide_seasons.md#6

> When to visit the region > Winter, December to February: Brightwater carries on, since the university keeps it occupied. Halden Bay largely closes. Kestrelford's approach road is difficult in snow and the town is cut off for a day or two most winters.

Claude: check 1: Y · check 3: Y

Agree: [ ]

### S9 · B26 · guide_regional_transport.md#7

> Getting around the region > Walking and cycling: Cycling is pleasant on the river path and the trackbed, and unpleasant on Mill Road and the coast road, neither of which has a shoulder.

Claude: check 1: Y · check 3: Y

Agree: [Y]

### S10 · B25 · guide_regional_transport.md#6

> Getting around the region > Walking and cycling: The river path from Brightwater runs four miles upstream on a good surface. The old railway trackbed from Kestrelford runs six miles on an easy gradient and is the best walking in the region for the effort involved. The coastal path from Halden Bay is more serious — exposed, and closed in high wind.

Claude: check 1: Y · check 3: Y

Agree: [Y]
