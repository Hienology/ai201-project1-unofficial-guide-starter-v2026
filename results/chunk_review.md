# Chunk review — criterion 4

- Produced by: `review_chunks.py::write_sheet`, chunks from `chunker.py::split_documents`, corpus `city_guides`
- Checks 2, 4 and 5 marked by this script. Checks 1 and 3 marked by Claude (`results/chunk_judgments.json`), audited in `results/chunk_spotcheck.md`.
- A chunk passes at 4 or more of 5.

| # | Check | Marked by |
|---|---|---|
| 1 | **Answerable alone** — Using only this chunk, someone could give a factually correct answer to a question about its topic (for a chunk covering several towns: a question about any one of them). | Claude |
| 2 | **Whole unit** — It starts with "Guide > Section:" and ends at the end of a sentence. | script |
| 3 | **One line of ideas** — Every sentence serves the topic named in its heading. | Claude |
| 4 | **Concrete** — It contains a digit, a number written as a word (two to twenty, thirty, forty, fifty, hundred, thousand), a day or a month. | script |
| 5 | **Not repeated** — Its text is not a near-copy (90% or more the same) of another chunk's. | script |

## Part A — town guides: 0 of 72 pass

### A1 · guide_brightwater.md#0

> Brightwater > Overview: Brightwater is a river town of about 40,000 people, roughly doubling in term time. It grew around a mill that closed in 1974 and spent twenty years working out what to be instead. The answer turned out to be the university.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A2 · guide_brightwater.md#1

> Brightwater > Getting there: The train runs to the regional hub eleven times a day on weekdays and six times on Sundays, taking 50 minutes. The station is a 15-minute walk from campus, or the shuttle meets the four busiest arrivals. Long-distance coaches stop on Verrill Street rather than at the station, which catches people out. There is no airport; the nearest is 90 minutes by road.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A3 · guide_brightwater.md#2

> Brightwater > Getting around: The town is walkable end to end in about 35 minutes. The local bus runs two routes on a 30-minute headway until 7pm and stops entirely on Sundays. Cycling is easy along the river path and unpleasant on Mill Road, which has no shoulder. Taxis exist but must be phoned; they do not circulate looking for fares.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A4 · guide_brightwater.md#3

> Brightwater > Eat and drink: The riverside strip has six or seven places aimed squarely at visitors and priced accordingly. Two streets back, on Corry Lane, the same food costs about a third less. The Tuesday market sets up in the square from 7am and is finished by 1pm. Most kitchens in town stop serving at 9pm, earlier than visitors expect, and on Sundays many close entirely.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A5 · guide_brightwater.md#4

> Brightwater > What to see: The mill building itself is now a museum and is genuinely good, particularly the section on what happened to the town after it closed. Allow 90 minutes. The river walk runs four miles upstream to a weir and is the thing most people remember. The cathedral is small and 14th century and takes 20 minutes.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A6 · guide_brightwater.md#5

> Brightwater > Where to stay: Accommodation is thin and expensive during graduation week and in early September. Outside those windows there is more supply than demand. The two hotels on the riverside are the obvious choice and the guesthouses on Corry Lane are better value.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A7 · guide_brightwater.md#6

> Brightwater > When to go: May and June are the best months — long days, everything open, and the students largely gone. July and August are quiet to the point of being dull. Late September through November the town is at its busiest. Winter is cold and several riverside businesses close entirely from January to March.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A8 · guide_brightwater.md#7

> Brightwater > Practical notes: Cash is still useful at the market and in smaller places, though cards are accepted almost everywhere now. Mobile coverage is good in the centre and patchy on the outskirts. The nearest full hospital is in Brightwater; there is a minor injuries unit locally with limited hours.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 N — 1/5, unmarked

- 4 Concrete: no number, day or month in it
- 5 Not repeated: near-copy of guide_corry_vale.md#7 and 7 others

### A9 · guide_corry_vale.md#0

> Corry Vale > Overview: Corry Vale is not a town but a valley containing four villages strung along eleven miles of road. Visitors treat it as one destination and locals emphatically do not. The largest village has 900 people and the smallest has 140.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A10 · guide_corry_vale.md#1

> Corry Vale > Getting there: There is no public transport into the valley beyond a school bus that will carry passengers if there is room. Driving from Brightwater takes 35 minutes on a good road as far as the valley mouth and then 20 more on a poor one. Cycling in is a serious undertaking; the road climbs 400 metres in the first four miles.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A11 · guide_corry_vale.md#2

> Corry Vale > Getting around: Nothing within the valley is walkable from anything else — the villages are two to four miles apart. There is one taxi, based in the largest village, and it must be booked a day ahead. Most visitors drive between villages and walk the footpaths in between.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A12 · guide_corry_vale.md#3

> Corry Vale > Eat and drink: One pub in the largest village serves food seven days a week. A second, in the third village, opens Thursday to Sunday. There is a farm shop at the valley mouth that sells bread, cheese and little else, and it closes at 4pm. Bring supplies; this is not a place with options.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A13 · guide_corry_vale.md#4

> Corry Vale > What to see: The valley itself is the attraction. The footpath network is dense and well marked, and a circuit taking in three of the four villages is about nine miles with 500 metres of ascent. The chapel in the second village is 12th century and always unlocked.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A14 · guide_corry_vale.md#5

> Corry Vale > Where to stay: Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A15 · guide_corry_vale.md#6

> Corry Vale > When to go: May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths become genuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A16 · guide_corry_vale.md#7

> Corry Vale > Practical notes: Cash is still useful at the market and in smaller places, though cards are accepted almost everywhere now. Mobile coverage is good in the centre and patchy on the outskirts. The nearest full hospital is in Brightwater; there is a minor injuries unit locally with limited hours.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 N — 1/5, unmarked

- 4 Concrete: no number, day or month in it
- 5 Not repeated: near-copy of guide_brightwater.md#7 and 7 others

### A17 · guide_elder_ness.md#0

> Elder Ness > Overview: Elder Ness is a headland with a village of 300 on it, a lighthouse, a bird observatory, and very little else. People come for one of three reasons — birds, walking, or a deliberate absence of things to do.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A18 · guide_elder_ness.md#1

> Elder Ness > Getting there: A single road in, which floods at the highest spring tides roughly six times a year for about two hours either side of high water. Tide tables are posted at the turning and are worth reading. No public transport of any kind. Nearest station is Pellew Sands, 40 minutes by road.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A19 · guide_elder_ness.md#2

> Elder Ness > Getting around: On foot. The village is one street. The lighthouse is a 25-minute walk along the shingle, which is harder going than the distance suggests. There is one car park at the village and parking anywhere else on the headland is prohibited and enforced.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A20 · guide_elder_ness.md#3

> Elder Ness > Eat and drink: One pub, serving food 12 to 2 and 6 to 8, closed Mondays. A shop that sells basics and closes at 5pm and all day Sunday. That is the complete list. Visitors staying more than a night bring food with them.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A21 · guide_elder_ness.md#4

> Elder Ness > What to see: The bird observatory takes day visitors and the wardens are generous with their time; spring and autumn migration are the reasons to come. The lighthouse is not open to the public but the walk to it is the point. The shingle beach is dramatic and swimming is genuinely dangerous — there is a strong offshore current and no lifeguard.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 Y — 2/5, unmarked

- 4 Concrete: no number, day or month in it

### A22 · guide_elder_ness.md#5

> Elder Ness > Where to stay: The pub has four rooms and the observatory has dormitory accommodation for members and their guests. Both book up entirely for the migration seasons a year ahead. There is nothing else.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A23 · guide_elder_ness.md#6

> Elder Ness > When to go: April to May and September to October for birds, which is what most visitors come for. Midsummer is pleasant and quiet. Winter is severe, the road floods more often, and the pub reduces to weekends only.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A24 · guide_elder_ness.md#7

> Elder Ness > Practical notes: Cash is still useful at the market and in smaller places, though cards are accepted almost everywhere now. Mobile coverage is good in the centre and patchy on the outskirts. The nearest full hospital is in Brightwater; there is a minor injuries unit locally with limited hours.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 N — 1/5, unmarked

- 4 Concrete: no number, day or month in it
- 5 Not repeated: near-copy of guide_brightwater.md#7 and 7 others

### A25 · guide_givens_mill.md#0

> Givens Mill > Overview: Givens Mill is a village of 700 built around a working watermill that still grinds flour commercially. It is the sort of place people visit for an afternoon and then talk about for longer than the visit lasted.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A26 · guide_givens_mill.md#1

> Givens Mill > Getting there: No station and no bus on Sundays; four buses a day from Brightwater on weekdays, taking 30 minutes. Driving is 20 minutes. The village car park holds about forty cars and is full by 11am on summer Saturdays.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A27 · guide_givens_mill.md#2

> Givens Mill > Getting around: Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A28 · guide_givens_mill.md#3

> Givens Mill > Eat and drink: A tearoom attached to the mill, open 10 to 4 daily except Tuesdays, which sells bread made from the flour ground twenty metres away and is the reason most people come. One pub, food served lunchtimes and Thursday to Saturday evenings.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A29 · guide_givens_mill.md#4

> Givens Mill > What to see: The mill runs tours on the hour from 11 to 3 and the machinery is operating during them, which is loud and much more impressive than a static exhibit. The church has a Saxon doorway. The river walk downstream reaches Brightwater in about three hours.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A30 · guide_givens_mill.md#5

> Givens Mill > Where to stay: Nothing in the village itself. The nearest rooms are in Brightwater, which is close enough that this is not really a problem — most people come for a half day.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 Y — 2/5, unmarked

- 4 Concrete: no number, day or month in it

### A31 · guide_givens_mill.md#6

> Givens Mill > When to go: The mill runs March to November and is closed entirely in winter. Late spring is the best time. Summer Saturdays are busy enough that the car park becomes the limiting factor; come on a weekday if you can.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A32 · guide_givens_mill.md#7

> Givens Mill > Practical notes: Cash is still useful at the market and in smaller places, though cards are accepted almost everywhere now. Mobile coverage is good in the centre and patchy on the outskirts. The nearest full hospital is in Brightwater; there is a minor injuries unit locally with limited hours.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 N — 1/5, unmarked

- 4 Concrete: no number, day or month in it
- 5 Not repeated: near-copy of guide_brightwater.md#7 and 7 others

### A33 · guide_halden_bay.md#0

> Halden Bay > Overview: Halden Bay is a working fishing port of 8,000 that has picked up a second life as a weekend destination. The two economies sit somewhat awkwardly beside each other and the town is candid about it.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A34 · guide_halden_bay.md#1

> Halden Bay > Getting there: The coast road is the only approach and it is slow — 40 minutes for 22 miles, with the last stretch cut into the cliff. Buses run four times a day. Parking in the town itself is limited to two small lots that fill by 10am on summer weekends; the overflow lot is a 12-minute walk up a hill.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A35 · guide_halden_bay.md#2

> Halden Bay > Getting around: The town is small enough to cross in fifteen minutes but is built on three levels connected by stepped lanes, which makes it hard going with luggage or a pushchair. The harbour front is level; everything above it is not.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A36 · guide_halden_bay.md#3

> Halden Bay > Eat and drink: Seafood, unsurprisingly, and it is genuinely fresh — the boats land in the early morning and the two harbour restaurants buy directly. Prices on the harbour front are roughly double those on Fell Street, one level up, for comparable food. Everything closes by 9pm and much of it closes entirely from November to February.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A37 · guide_halden_bay.md#4

> Halden Bay > What to see: The harbour at 6am when the boats come in is the thing worth setting an alarm for. The coastal path runs in both directions, north to a lighthouse in about two hours and south along the cliffs for as far as you want. The small museum on Fell Street covers the fishing industry and takes 40 minutes.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A38 · guide_halden_bay.md#5

> Halden Bay > Where to stay: Almost entirely holiday lets rather than hotels, which means minimum stays of two or three nights in summer. There is one inn on the harbour. Prices roughly halve outside July and August.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A39 · guide_halden_bay.md#6

> Halden Bay > When to go: June and September are the sweet spot. July and August are busy enough that the parking problem becomes the defining feature of the visit. Winter is dramatic and largely closed. The coastal path is genuinely dangerous in high wind and gets shut.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A40 · guide_halden_bay.md#7

> Halden Bay > Practical notes: Cash is still useful at the market and in smaller places, though cards are accepted almost everywhere now. Mobile coverage is good in the centre and patchy on the outskirts. The nearest full hospital is in Brightwater; there is a minor injuries unit locally with limited hours.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 N — 1/5, unmarked

- 4 Concrete: no number, day or month in it
- 5 Not repeated: near-copy of guide_brightwater.md#7 and 7 others

### A41 · guide_kestrelford.md#0

> Kestrelford > Overview: Kestrelford is a hill town of 12,000, an hour inland from Brightwater. It has been a market town since the 1200s and the street plan has not meaningfully changed since. This is charming on foot and difficult in a car.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A42 · guide_kestrelford.md#1

> Kestrelford > Getting there: No railway station; the line was closed in 1963 and the trackbed is now a walking route. Buses run from Brightwater roughly hourly on weekdays, every two hours on Saturdays, and not at all on Sundays. Driving takes 55 minutes and the last eight are on a single-track road with passing places.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A43 · guide_kestrelford.md#2

> Kestrelford > Getting around: Everything is within a ten-minute walk of the market square. The town is built on a slope and the walk up from the lower car park is steeper than it looks on a map. There is no local bus service within the town itself.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A44 · guide_kestrelford.md#3

> Kestrelford > Eat and drink: Four pubs, two cafés, and a bakery that sells out by 11am. The pubs serve food between 12 and 2 and again between 6 and 8:30, and outside those windows there is nowhere to eat at all. The bakery is the reason most people come back.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A45 · guide_kestrelford.md#4

> Kestrelford > What to see: The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A46 · guide_kestrelford.md#5

> Kestrelford > Where to stay: Two inns on the square and a handful of rooms above the pubs. Booking ahead matters between May and September and not at all otherwise. There is no accommodation of any kind within four miles of the town in either direction.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A47 · guide_kestrelford.md#6

> Kestrelford > When to go: Late spring and early autumn. The Saturday market runs year-round but is much reduced from November to February. August is busy with walkers. The single-track approach road is genuinely difficult in snow and the town can be cut off for a day or two most winters.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A48 · guide_kestrelford.md#7

> Kestrelford > Practical notes: Cash is still useful at the market and in smaller places, though cards are accepted almost everywhere now. Mobile coverage is good in the centre and patchy on the outskirts. The nearest full hospital is in Brightwater; there is a minor injuries unit locally with limited hours.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 N — 1/5, unmarked

- 4 Concrete: no number, day or month in it
- 5 Not repeated: near-copy of guide_brightwater.md#7 and 7 others

### A49 · guide_marchwood.md#0

> Marchwood > Overview: Marchwood is the regional hub — 180,000 people, the junction everyone changes trains at, and a city most visitors pass through rather than stop in. That is a mistake, though an understandable one, since almost nothing of interest is near the station.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A50 · guide_marchwood.md#1

> Marchwood > Getting there: Every railway line in the region meets here, which is the city's defining feature. Trains to Brightwater run every 40 minutes until 11pm. The airport is 20 minutes out by a dedicated bus that runs every 15 minutes and costs more than the equivalent taxi shared between three people.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A51 · guide_marchwood.md#2

> Marchwood > Getting around: A tram network of four lines, running every 8 minutes on weekdays and every 15 at weekends, until midnight. A day ticket costs less than two single fares and nobody tells you this at the machine. The centre is walkable but the interesting districts are not adjacent to each other.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A52 · guide_marchwood.md#3

> Marchwood > Eat and drink: The best eating is in the Northgate district, a 12-minute tram ride from the station, where about thirty restaurants sit within four streets. The area immediately around the station is uniformly poor and expensive. Marchwood keeps later hours than anywhere else in the region — kitchens serve until 10:30pm, and until midnight on Fridays and Saturdays.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A53 · guide_marchwood.md#4

> Marchwood > What to see: The city museum is free and genuinely excellent, particularly the industrial floor. The covered market has operated since 1863 and is at its best on a weekday morning. The canal walk from Northgate to the old lock is 40 minutes and is the thing residents recommend when asked.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A54 · guide_marchwood.md#5

> Marchwood > Where to stay: Plentiful and, outside conference weeks, cheap. Northgate is the district worth staying in. Station-area hotels are convenient for an early train and dispiriting for anything else.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 Y — 2/5, unmarked

- 4 Concrete: no number, day or month in it

### A55 · guide_marchwood.md#6

> Marchwood > When to go: Any time. This is the one place in the region that works in winter, since almost everything is indoors and nothing closes seasonally. Conference weeks in March and October fill the hotels and double the prices; check before booking.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A56 · guide_marchwood.md#7

> Marchwood > Practical notes: Cash is still useful at the market and in smaller places, though cards are accepted almost everywhere now. Mobile coverage is good in the centre and patchy on the outskirts. The nearest full hospital is in Brightwater; there is a minor injuries unit locally with limited hours.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 N — 1/5, unmarked

- 4 Concrete: no number, day or month in it
- 5 Not repeated: near-copy of guide_brightwater.md#7 and 7 others

### A57 · guide_pellew_sands.md#0

> Pellew Sands > Overview: Pellew Sands is a Victorian seaside resort that has been through three distinct lives: fashionable, then neglected, and now something in between. The architecture is from the first period and much of the infrastructure from the second.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A58 · guide_pellew_sands.md#1

> Pellew Sands > Getting there: The branch line runs from the regional hub in 70 minutes, seven times a day, and the station is on the seafront, which is rare and pleasant. Driving is 50 minutes from Brightwater. Seafront parking is metered and expensive; the free lot behind the station is a four-minute walk and almost always has space.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A59 · guide_pellew_sands.md#2

> Pellew Sands > Getting around: The seafront runs two miles and is flat the whole way. Everything of interest is on it or one street back. A land train runs the length of the promenade between Easter and September, hourly, and is aimed at children but used by everyone.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A60 · guide_pellew_sands.md#3

> Pellew Sands > Eat and drink: The seafront is chips and ice cream, done well and without pretence. The better cooking is on Marine Terrace, one street back, where four or five places are genuinely good and roughly half the seafront price. Sunday evening is difficult — most kitchens close.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A61 · guide_pellew_sands.md#4

> Pellew Sands > What to see: The pier is 1890s, was partly destroyed by fire in 1978, and the surviving half is open and free. The municipal gardens behind the seafront are better than they sound. The beach is two miles of hard sand and is genuinely excellent at low tide and unremarkable at high.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A62 · guide_pellew_sands.md#5

> Pellew Sands > Where to stay: A great deal of accommodation, most of it dating from the resort's first period and varying wildly in how well it has been maintained. Prices are low outside July and August. The seafront hotels are noisier than the Marine Terrace guesthouses.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A63 · guide_pellew_sands.md#6

> Pellew Sands > When to go: June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A64 · guide_pellew_sands.md#7

> Pellew Sands > Practical notes: Cash is still useful at the market and in smaller places, though cards are accepted almost everywhere now. Mobile coverage is good in the centre and patchy on the outskirts. The nearest full hospital is in Brightwater; there is a minor injuries unit locally with limited hours.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 N — 1/5, unmarked

- 4 Concrete: no number, day or month in it
- 5 Not repeated: near-copy of guide_brightwater.md#7 and 7 others

### A65 · guide_thornby_wells.md#0

> Thornby Wells > Overview: Thornby Wells was a spa town for about ninety years and has spent the century since being a comfortable small town of 6,000 that happens to have unusually grand architecture for its size.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A66 · guide_thornby_wells.md#1

> Thornby Wells > Getting there: On the Marchwood line, 25 minutes from the hub, with trains every hour and every two hours on Sundays. The station is in the centre. Driving from Brightwater is 45 minutes on good roads. Parking is free for two hours everywhere in town, which is unusual and generous.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A67 · guide_thornby_wells.md#2

> Thornby Wells > Getting around: Flat and compact — 15 minutes end to end. The pump room, the gardens, and the main shopping street are within three minutes of each other. No local transport and none needed.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A68 · guide_thornby_wells.md#3

> Thornby Wells > Eat and drink: Better than a town this size has any right to be, a legacy of the spa era. Four places on Pump Street are genuinely good and the prices are Marchwood prices rather than village prices. Sunday lunch is the local institution and needs booking a week ahead.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A69 · guide_thornby_wells.md#4

> Thornby Wells > What to see: The pump room is open, free, and you can still drink the water, which tastes bad in an interesting way. The gardens behind it are formal, well kept, and open until dusk. The assembly rooms host concerts most weekends and tickets are rarely sold out.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 Y — 2/5, unmarked

- 4 Concrete: no number, day or month in it

### A70 · guide_thornby_wells.md#5

> Thornby Wells > Where to stay: Two large hotels from the spa period, both faded in a way some people find charming, and several small guesthouses. Prices are moderate and stable year-round.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A71 · guide_thornby_wells.md#6

> Thornby Wells > When to go: Year-round, genuinely. The gardens are best in May and June. The concert season runs September to April, which makes this the region's most reliable winter destination after Marchwood.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### A72 · guide_thornby_wells.md#7

> Thornby Wells > Practical notes: Cash is still useful at the market and in smaller places, though cards are accepted almost everywhere now. Mobile coverage is good in the centre and patchy on the outskirts. The nearest full hospital is in Brightwater; there is a minor injuries unit locally with limited hours.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 N — 1/5, unmarked

- 4 Concrete: no number, day or month in it
- 5 Not repeated: near-copy of guide_brightwater.md#7 and 7 others

## Part B — cross-cutting guides: 0 of 22 pass

### B1 · guide_accessibility.md#0

> Getting around the region with limited mobility > Overview: An honest assessment rather than a promotional one. Some of these places are difficult and it is better to know in advance.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 Y — 2/5, unmarked

- 4 Concrete: no number, day or month in it

### B2 · guide_accessibility.md#1

> Getting around the region with limited mobility > Straightforward: **Thornby Wells** is the easiest town in the region. It is flat, compact, and everything is within three minutes of everything else. Parking is free for two hours anywhere in town and the station is central. The pump room and gardens are level throughout.
>
> **Marchwood** has a modern tram network with level boarding on all four lines, running every 8 minutes on weekdays. The city museum and covered market are both step-free. The distances between districts are the main consideration.
>
> **Brightwater** is level along the river and through the centre. The mill museum is step-free. The station is a 15-minute walk from campus on flat ground, or the shuttle meets the four busiest arrivals.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B3 · guide_accessibility.md#2

> Getting around the region with limited mobility > Mixed: **Pellew Sands** has a two-mile seafront that is flat the whole way, and everything of interest is on it or one street back. The land train runs the length of the promenade hourly between Easter and September. The beach itself is hard sand and manageable at low tide.
>
> **Givens Mill** is one flat street along the river. The mill tour involves stairs and the machinery floor is not accessible; the tearoom and riverside are.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B4 · guide_accessibility.md#3

> Getting around the region with limited mobility > Difficult: **Kestrelford** is built on a slope and the walk up from the lower car park is steeper than it looks on a map. There is no transport within the town.
>
> **Halden Bay** is built on three levels connected by stepped lanes. The harbour front is level; everything above it is not. This is hard going with luggage or a pushchair, let alone a wheelchair.
>
> **Corry Vale** has no public transport, villages two to four miles apart, and footpaths rather than pavements. **Elder Ness** is shingle and a single street.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B5 · guide_accessibility.md#4

> Getting around the region with limited mobility > Practical: The nearest full hospital is in Marchwood. Brightwater has a hospital; Kestrelford, Halden Bay, Corry Vale, Givens Mill and Elder Ness have minor injuries units with limited hours or nothing at all.
>
> Mobile coverage is good in the town centres and patchy on the outskirts, and genuinely absent in parts of Corry Vale.

Checks: 1 – · 2 Y · 3 – · 4 N · 5 Y — 2/5, unmarked

- 4 Concrete: no number, day or month in it

### B6 · guide_eating.md#0

> Eating across the region > The pattern worth knowing: Almost everywhere in this region, the good cooking is one street back from wherever the visitors are. Brightwater's riverside strip is priced for people who walked there from the hotels; Corry Lane, two streets inland, serves comparable food for about a third less. Halden Bay's harbour front is roughly double Fell Street, one level up. Pellew Sands's seafront is chips and ice cream, and Marine Terrace behind it is where the actual restaurants are.
>
> Marchwood is the exception, in that the good district — Northgate — is a tram ride away rather than a street away, and the station area is uniformly poor.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B7 · guide_eating.md#1

> Eating across the region > Opening hours: This catches visitors out more than anything else. Outside Marchwood, kitchens across the region stop serving at 9pm and often earlier. Kestrelford's pubs serve 12 to 2 and 6 to 8:30 and there is nowhere to eat at all outside those windows. Elder Ness has one pub, closed Mondays.
>
> Sunday evening is the hardest meal to find anywhere except Marchwood and Thornby Wells.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B8 · guide_eating.md#2

> Eating across the region > Markets: Kestrelford's Saturday market has run since the 1400s and is the region's best, though much reduced from November to February. Brightwater's Tuesday market sets up at 7am in the square and is finished by 1pm. Marchwood's covered market has operated since 1863, runs six days a week, and is at its best on a weekday morning.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B9 · guide_eating.md#3

> Eating across the region > Local specifics: Halden Bay's seafood is genuinely fresh — the two harbour restaurants buy directly from boats that land in the early morning. Givens Mill's tearoom sells bread made from flour ground twenty metres away. Kestrelford's bakery sells out by 11am and is the reason a lot of people return. Thornby Wells does Sunday lunch as a local institution and it needs booking a week ahead.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B10 · guide_eating.md#4

> Eating across the region > Practical: Cash is still useful at markets and in the smaller villages. Corry Vale has a farm shop at the valley mouth selling bread and cheese and little else, closing at 4pm — bring supplies if you are staying there. Elder Ness has one shop, closed Sundays and after 5pm.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B11 · guide_regional_transport.md#0

> Getting around the region > The railway: The line runs along the river valley, connecting Brightwater to the regional hub in 50 minutes. Eleven services a day on weekdays, six on Sundays. The line north of Brightwater closed in 1963 and everything beyond it is bus or car.
>
> Tickets are cheaper booked the day before than on the day, and considerably cheaper than that booked a week ahead. There is no ticket office at Brightwater station outside weekday mornings; the machine on the platform takes cards only.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B12 · guide_regional_transport.md#1

> Getting around the region > Buses: Three operators run in the region and they do not accept each other's tickets, which is the single most common source of confusion for visitors. Services concentrate on weekday daytimes. Sunday service is minimal to non-existent outside the Brightwater town routes.
>
> The Kestrelford service is hourly on weekdays, two-hourly on Saturdays, and does not run on Sundays. The Halden Bay coast service runs four times daily year-round.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B13 · guide_regional_transport.md#2

> Getting around the region > Driving: Roads are good between the towns and poor on the approaches to both Kestrelford and Halden Bay. The Kestrelford approach is single-track with passing places for the final eight minutes. The Halden Bay coast road is cut into the cliff and is slow rather than difficult.
>
> Parking is the constraint rather than driving. Both Halden Bay lots fill by 10am on summer weekends. Kestrelford's lower car park is free and involves a steep walk up.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B14 · guide_regional_transport.md#3

> Getting around the region > Walking and cycling: The river path from Brightwater runs four miles upstream on a good surface. The old railway trackbed from Kestrelford runs six miles on an easy gradient and is the best walking in the region for the effort involved. The coastal path from Halden Bay is more serious — exposed, and closed in high wind.
>
> Cycling is pleasant on the river path and the trackbed, and unpleasant on Mill Road and the coast road, neither of which has a shoulder.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B15 · guide_seasons.md#0

> When to visit the region > Spring, March to May: Days lengthen quickly and businesses that closed for winter reopen through March and April. By May everything is open and the weather is reliable enough to plan around. Late May is arguably the best week of the year in Brightwater — long days, everything running, and the students gone.
>
> The Kestrelford Saturday market builds back to full size through April.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B16 · guide_seasons.md#1

> When to visit the region > Summer, June to August: June is excellent everywhere. July and August split: Halden Bay becomes very busy and the parking problem dominates, Kestrelford fills with walkers, and Brightwater goes quiet to the point of dullness with the university empty.
>
> If you are going to Halden Bay in August, arrive before 10am or plan to use the overflow lot.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B17 · guide_seasons.md#2

> When to visit the region > Autumn, September to November: September is the other sweet spot — warm, quiet, and everything still open. From late September Brightwater is at its busiest as term starts, and accommodation there becomes hard to find and expensive.
>
> By November the coastal businesses begin closing and the days are short.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B18 · guide_seasons.md#3

> When to visit the region > Winter, December to February: Brightwater carries on, since the university keeps it occupied. Halden Bay largely closes. Kestrelford's approach road is difficult in snow and the town is cut off for a day or two most winters.
>
> The coastal path is dramatic and frequently shut. Several riverside businesses in Brightwater close entirely from January to March.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B19 · guide_walking.md#0

> Walking in the region > Easy, on good surfaces: The **Brightwater river path** runs four miles upstream from the town to a weir, on a made surface, flat throughout. It is the most-walked route in the region and deservedly so. Continuing downstream from Givens Mill reaches Brightwater in about three hours.
>
> The **Kestrelford trackbed** follows the railway line closed in 1963 for six miles to the next village. Easy gradient, good surface, and the best walking in the region for the effort involved.
>
> **Thornby Wells** has flat, formal gardens and level streets — the region's most accessible town on foot.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B20 · guide_walking.md#1

> Walking in the region > Moderate, with hills: The **Corry Vale circuit** takes in three of the four villages, about nine miles with 500 metres of ascent. The footpath network in the valley is dense and well marked. Several paths become genuinely boggy rather than merely wet outside May to September.
>
> **Givens Mill** to Brightwater along the river is three hours one way, easy underfoot, and the return needs a weekday bus.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B21 · guide_walking.md#2

> Walking in the region > Serious, and weather-dependent: The **Halden Bay coastal path** runs north to a lighthouse in about two hours and south along the cliffs indefinitely. It is exposed, and it is closed in high wind — this is enforced and the closures are not advisory.
>
> The **Elder Ness shingle** walk to the lighthouse is only 25 minutes but shingle is much harder going than the distance suggests. The single access road to the headland floods at the highest spring tides, about six times a year, for roughly two hours either side of high water.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked

### B22 · guide_walking.md#3

> Walking in the region > Seasonal notes: Add four minutes to any Brightwater walking estimate in winter; the path past the pond ices over and people take the long way round. Boots with real tread matter more here than any other equipment. Paths are cleared by 7am on weekdays and considerably later at weekends.
>
> The Kestrelford approach road is not gritted above the second village and is impassable in snow, which can cut the town off for a day or two most winters.

Checks: 1 – · 2 Y · 3 – · 4 Y · 5 Y — 3/5, unmarked
