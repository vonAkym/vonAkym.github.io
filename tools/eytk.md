# Everything you need to know: MyMakanRoute

A study guide for the supervisor meeting. It covers the project end to end: what it is, how each part works, the numbers, the technical terms, and answers to likely questions.

Every fact here comes from the code and the project docs (`PLAN.md`, `FEASIBILITY.md`, `erd.md`, `architecture.md`, `CLAUDE.md`) as of 5 Nov 2026. Where something is planned rather than built, it says so.

**How to use it:** read sections 1 to 3 first; they are enough to answer most questions. Then read the part you feel least sure about. Section 15 has likely questions with short answers, section 16 has the numbers on one card, and section 17 is an A to Z glossary.

---

## 1. The project in 30 seconds

> MyMakanRoute is a food hopping and food discovery planner for Penang. It helps tourists and locals find **hidden gems**: food places that are well rated but not yet well known. The user picks a few places, and the app plans the **shortest walking route** between them. The route planner uses **Dijkstra's algorithm** on a real OpenStreetMap road network to get the walking times, and **Ant Colony Optimisation** to choose the visiting order.

- **Course:** CAT405 Final Year Project, School of Computer Sciences, USM, Intelligent Computing major.
- **Area covered so far:** George Town to Gelugor/USM (bounding box 5.33 to 5.46 N, 100.27 to 100.345 E).
- **Status:** the proposed work is feasible. All four modules run end to end. Two gaps remain: **real ratings** and **real user accounts**.

**Why "Intelligent Computing"?** The route planner uses Ant Colony Optimisation, a nature-inspired optimisation method (swarm intelligence). That is the intelligent computing part.

---

## 2. Modules and submodules (fixed from the proposal)

4 modules, 13 submodules. These names never change.

| Module | Submodules | Status |
| --- | --- | --- |
| **User Management** | Registration, Login, Profile and Preference Setup | Partial (web screens in demo mode) |
| **Food Discovery** | Food Place Searching, Hidden Gem Highlighting, Food Place Visualisation | Built |
| **Food Hopping** | Itinerary Planner, Route Planner, Itinerary Review and Customisation, Past Food Hopping Visualisation | Route Planner built; the other 3 partial |
| **Food Stalls Analytics** | Food Places Visualisation, Food Places Analysis, Food Place Suggestion | Built |

- **Built (7):** has a server part (API), a web page, and automated tests.
- **Partial (6):** the web screen works, but in **demo mode**: login does not check a real password, and data is kept in the browser (localStorage). The database tables are ready. The real server part comes in **Phase 2B**.
- **Filtering** (halal, budget, cuisine, dietary, open now) is **not a module**. It is part of Food Discovery and Food Hopping.

---

## 3. How the whole system works (end to end)

### 3.1 The three layers

| Layer | What it is | Technology |
| --- | --- | --- |
| **Presentation** (what the user sees) | Web app in the browser. Mobile app planned | React + Vite (web); React Native + Expo (mobile, planned) |
| **Application** (the logic) | Backend API: one server program that all apps talk to | Node.js + Express (JavaScript) |
| **Data** (what is stored) | Database of places, users and trips | Supabase: PostgreSQL + PostGIS |

**External data:** OpenStreetMap gives us the food places and the road network. Google Places ratings are planned.

The apps **never talk to the database directly**. They call our backend API, and only the backend talks to the database. This keeps database passwords off the user's device and keeps all rules in one place.

### 3.2 What happens when a user plans a trip (step by step)

1. The user opens the web app and chooses a location (for example Komtar).
2. The web app calls `GET /api/discovery/places?lat=..&lng=..&radius=1500`.
3. The backend runs a **PostGIS** query: "all places within 1,500 m of this point, with their distance".
4. The backend applies the **hidden gem rule** to every place and **ranks** them: Hidden Gems first, then Popular, then unlabelled; nearest first within each group.
5. The web app shows the list and a **Leaflet** map with labels.
6. The user adds 2 to 10 places to the trip and presses **Plan route**.
7. The web app calls `POST /api/hopping/route` with the place IDs and travel mode (walking or driving).
8. The backend:
   1. loads the places from the database;
   2. **snaps** each place to its nearest road node;
   3. runs **Dijkstra** from each place to build a **time matrix** (walking time between every pair);
   4. runs **ACO** on the matrix to choose the visiting order;
   5. also runs **nearest neighbour** and **brute force** (up to 8 stops) for comparison;
   6. builds the **legs** (time, distance, and the road path to draw on the map).
9. The web app draws the route on the map and shows total minutes, metres, and the comparison card.
10. The user can reorder or remove stops, plan again, and save the trip (saved in the browser for now; on the server from Phase 2B).

### 3.3 The tech stack, and why each was chosen

| Part | Choice | Why |
| --- | --- | --- |
| Backend language | JavaScript (Node.js 20+) | Same language as the web and mobile apps; one language for the whole project |
| Web framework | Express 4 | The most common and simplest Node.js web framework |
| Database | PostgreSQL + PostGIS | Real SQL database; PostGIS handles map distances ("within 1.5 km") efficiently |
| Hosting | Supabase (Singapore region) | Free hosted PostgreSQL with PostGIS and a built-in login service (Supabase Auth) |
| Database access | `pg` library with plain SQL | Same code runs on Supabase, a laptop or a test server; easier to explain than a heavy tool |
| Input checking | zod | One readable rule set per request; clear error messages |
| Security headers | helmet, cors | Standard protections in one line each |
| Web app | React 19 + Vite | Most popular UI library; Vite is a fast development server |
| Maps (web) | Leaflet + react-leaflet with OpenStreetMap tiles | Free, no API key |
| Charts (web) | Recharts | Simple React charts |
| Mobile (planned) | React Native + Expo | Reuses React knowledge; Expo Go runs on a real phone easily |
| Tests | Jest + Supertest (backend), Vitest (web) | Standard tools; Supertest calls the API without starting a server |

---

## 4. The backend (code structure)

### 4.1 Folders

```
backend/src/
  app.js          builds the Express app (tests use this)
  index.js        starts the server on port 3000
  config/         reads settings from .env and checks them with zod
  lib/            db.js (database connection pool), response.js (standard answers, AppError)
  middleware/     validate.js, errorHandler.js, notFound.js
  modules/
    food-discovery/        search, hidden gem rule, opening hours
    food-hopping/          travel graph, Dijkstra, ACO, baselines
    food-stalls-analytics/ overview and findings
    user-management/       empty (Phase 2B)
backend/db/migrations/     001 to 004 .sql files
backend/db/seeds/          55 SAMPLE places
backend/scripts/           import-osm.js, build-road-graph.js, feasibility.js
```

Each module has the same four files:

- **routes:** the URLs, and the input rules for each URL.
- **controller:** reads the request and sends the response.
- **service:** the actual logic.
- **model:** the SQL queries.

This is a **layered** design (similar to MVC). Each file has one job, so it is easy to test and explain.

### 4.2 API endpoints (built)

| Method and path | Submodule | What it does |
| --- | --- | --- |
| `GET /health`, `GET /health/db` | (checks) | Is the server up? Can it reach the database? |
| `GET /api/discovery/places` | Food Place Searching + Hidden Gem Highlighting | Search by location and radius, with filters; labelled and ranked |
| `GET /api/discovery/places/:id` | Food Place Visualisation | One place's details |
| `POST /api/hopping/route` | Route Planner | Plan the best visiting order and route |
| `GET /api/analytics/overview` | Food Places Visualisation, Analysis, Suggestion | Chart data, written findings, suggested places |

**Search filters:** `lat`, `lng`, `radius` (100 to 5,000 m, default 1,500), `halal`, `maxPrice` (1 to 4), `cuisine`, `dietary`, `openNow`, `label`, `limit` (1 to 100, default 50).

**Route request:** `{ placeIds (2 to 10, no repeats), travelMode ("walking" or "driving", default walking), startPlaceId (optional, must be one of the places), seed (optional) }`.

**Planned (Phase 2B):** `/api/auth/register`, `/api/auth/login`, `/api/auth/refresh`, profile and preferences, and itinerary (save, edit, list) endpoints.

### 4.3 API design rules

- **REST API:** each URL is a "resource" (places, routes), and the HTTP method says what to do (GET reads, POST creates or computes).
- **JSON:** the text format all data is sent in.
- **Same answer shape everywhere:**
  - Success: `{ "success": true, "data": { ... } }`
  - Failure: `{ "success": false, "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }`
- **Validation:** every request is checked with a zod schema **before** the logic runs. Bad input gives HTTP **400** `VALIDATION_ERROR`.
- **Errors:**
  - Expected problems throw an `AppError`, for example 404 `NOT_FOUND`.
  - Anything unexpected becomes 500 `INTERNAL_ERROR`, with **no stack trace or SQL shown** to the user. The details go to the server log only.
- **Parameterised SQL** (`$1, $2`): user input is never pasted into SQL text, which prevents **SQL injection**.

---

## 5. Database and Supabase

### 5.1 What Supabase is

**Supabase** is a hosted service that gives us a **PostgreSQL** database (with the **PostGIS** add-on) in the cloud, plus an optional login service (**Supabase Auth**). Our project is in the **Singapore** region (close to Malaysia, so it is fast). We use the free tier.

**How the app uses it:** only our backend connects, with the `pg` library and a connection string (`DATABASE_URL`) kept in `backend/.env`. That file is never committed to Git.

### 5.2 The 6 tables

| Table | What it holds | Used by the API today? |
| --- | --- | --- |
| `places` | Every food place: name, cuisine, area, location (map point), halal, price level, rating, review count, opening hours, source, sample flag | **Yes** |
| `profiles` | One row per user: display name, role (user or admin). id = Supabase Auth user id | Not yet (2B) |
| `preferences` | A user's default filters: halal only, max price, cuisines, dietary | Not yet (2B) |
| `itineraries` | Saved trips: title, travel mode, total time and distance | Not yet (2B) |
| `itinerary_stops` | The ordered stops of each trip (links a trip to places) | Not yet (2B) |
| `schema_migrations` | Which migration files have been applied | Yes (by the migration runner) |

**Relationships (as in the ERD):**

- One profile **has** zero or one preferences row (1 to 1). `preferences.user_id` is both the PK and the FK.
- One profile **owns** zero or many itineraries (1 to many).
- One itinerary **contains** zero or many stops (1 to many).
- One place can be **visited in** zero or many stops (1 to many).

`itinerary_stops` is a **junction table**. It turns the many-to-many link between itineraries and places into two one-to-many links, and it also stores the **position** (order) of each stop.

### 5.3 Key database ideas

- **Primary key (PK):** the column that identifies each row (we use `uuid`, a long random id).
- **Foreign key (FK):** a column pointing to another table's PK. `on delete cascade` means deleting a user also deletes their trips.
- **Unique key (UK):** `osm_id` must not repeat, so re-running the import updates places instead of duplicating them.
- **`geography(Point, 4326)`:** the location type. 4326 is the standard GPS coordinate system (latitude and longitude, as used by phones).
- **GiST index:** a spatial index that makes "within N metres" searches fast without checking every row.
- **The search query:** `ST_DWithin(location, point, radius)` finds places within the radius, and `ST_Distance` gives each distance in metres.
- **Migrations:** numbered SQL files (001 to 004) that build the database. Running them in order rebuilds the same database anywhere. A small runner (`migrate.js`) records applied files in `schema_migrations`, so running it twice applies nothing new.
  - 001: places
  - 002: users (profiles, preferences)
  - 003: itineraries
  - 004: lock down the public API
- **Normalisation:** each fact is stored once (a place's data lives only in `places`; stops only point to it). This avoids copies that can disagree.

### 5.4 Database security

- **Row Level Security (RLS)** is switched on for every table. RLS means rules decide which rows a database user may see.
  - `places` has one read-only rule.
  - The other tables have no rules, so the public sees nothing in them.
- Supabase automatically publishes tables through a public REST API. **Migration 004 revokes** (takes away) write rights from Supabase's public roles (`anon`, `authenticated`) and blocks the private tables.
- Our backend connects as the table owner, so these rules do not limit it.
- We do **not** use the powerful `service_role` key in the app.
- There is no foreign key to Supabase's internal `auth.users` table, on purpose: the same migrations then also run on a plain PostgreSQL test database.

---

## 6. The data

### 6.1 Where it comes from

| Data | Source | How much | Where it is stored |
| --- | --- | --- | --- |
| Food places | **OpenStreetMap (OSM)**, a free world map made by volunteers. Tags used: restaurant, fast_food, food_court, cafe | 1,298 raw elements; 1,241 have a name and are imported | Supabase `places` table |
| Sample places | 55 of those real OSM places, with **invented** ratings, reviews, price, halal, hours and dietary tags | 55 | Supabase `places` (`source='sample'`, `is_sample=true`) |
| Road network | OSM roads for the same area | **26,689 nodes, 34,732 edges** | File `data/road-graph-penang.json` (about 2.5 MB), loaded into the backend's memory |

**Total in the database: 1,241 places** = 1,186 stored as OSM places + 55 kept as SAMPLE rows.

**How it is downloaded:** through the **Overpass API**, a public service for querying OSM data. The scripts try several Overpass servers and save **snapshots** in `data/`, so a busy server cannot break the demo.

**Why the road network is a file, not in Supabase:** the route planner reads the whole network on every route request. Keeping it in memory is much faster than querying the database each time, and it is loaded only once (about 0.2 s).

### 6.2 What OSM has and does not have

| | OSM (1,186 places) | SAMPLE (55) |
| --- | ---: | ---: |
| Name | 100% | 100% |
| Cuisine | 45.4% | 100% |
| Opening hours | 23.2% | 100% |
| Halal tag | **2.3%** | 100% |
| Rating | **0%** | 100% |

**Key finding:** OSM is good for **where** places are, but weak on **what they are like**. It has **no ratings at all**, so the hidden gem rule cannot run on OSM data alone. That is why the 55 SAMPLE places exist, and why real Google ratings are the next step.

**Be honest about it:** sample ratings are **invented**. Any result based on ratings shows that the **method works**, not facts about real Penang food.

### 6.3 Opening hours ("open now")

- Stored as JSON, for example `{"mon":[["08:00","15:00"],["18:00","22:00"]], ...}`. A missing day means closed.
- The check uses **Malaysian time** and handles ranges past midnight (for example 18:00 to 02:00).
- Places **without structured hours count as not open**, because we cannot promise they are. The raw OSM text is kept under `"osm"` but not used by the filter.

---

## 7. Hidden gem rule (Hidden Gem Highlighting)

**The idea:** a hidden gem is "well liked, but not many people know it yet". So it needs a **high rating** and **few reviews**.

| Label | Rule (defaults, changeable in config) |
| --- | --- |
| **Hidden Gem** | rating **≥ 4.3** and **1 to 100** reviews |
| **Popular** | **more than 100** reviews, whatever the rating |
| **No label** | everything else: no rating, 0 reviews, or few reviews with a lower rating |

- **Code:** `labelHiddenGem()` in `food-discovery/hiddenGem.js`. It is a **pure function** (same input always gives the same output, no database), so it is easy to unit test.
- **Ranking** (`rankFoodPlaces()`):
  1. Hidden Gems first, then Popular, then no label.
  2. Within each group, nearest first.
  3. A higher rating breaks ties.
- **Result on the 55 sample places:** 14 Hidden Gems, 35 Popular, 6 no label.
- **Komtar example (1.5 km):** 704 places found. The top 5 are all Hidden Gems, nearest first: Sister Yao's Char Koay Kak at 275 m, then Muscle Man Char Koay Kak, VR Pinxin Vegan, Hot Bowl White Curry Mee and Tok Tok Mee.
- **Sensitivity test:** at rating 4.0 there are 16 gems; at 4.5 there are 7; at the current 4.3 there are 14. The ≤ 100 and ≤ 200 review limits give the same count because no sample place has 101 to 200 reviews. That is a gap in the sample data, which real Google data will fix.

**Why 4.3 and 100?** These are reasonable starting values: 4.3 is clearly above average on most review sites, and 100 reviews separates "known locally" from "famous". They are configurable, and real Google data (step 2.9a) will show where they should sit.

---

## 8. Route planner (Food Hopping): the core algorithm

This is the most technical part. Learn the four steps in order: **graph → snap → Dijkstra → ACO**.

### 8.1 The road graph

- A **graph** is a set of **nodes** (points) linked by **edges** (connections).
- In our road graph:
  - a **node** is a junction or a road end (a **road node**);
  - an **edge** is a piece of road between two nodes, with a **length** and a **travel time**.
- Built from OSM by `npm run build:road-graph`: 26,689 nodes and 34,732 edges.
- **Connectivity:** 99% of usable walking nodes are in one connected part, so almost every place can reach every other.
- **Walking vs driving:**
  - Walking: 1.4 m/s (about 5 km/h), and people may walk **both ways** on one-way streets.
  - Driving: speed depends on road type (motorway 70 km/h, primary 40 km/h, residential 20 km/h, ...), and one-way streets are respected.
  - These speeds are **assumptions**, not measurements.

### 8.2 Snapping

- Places are not exactly on a road node, so each place is **snapped** to its **nearest road node** in the main connected part. That way a place is never stuck on an isolated road piece such as a car park.
- A **grid index** (squares of about 220 m) makes the nearest-node search fast: it checks only nearby squares, not all 26,689 nodes.
- A place more than 1 km from any road cannot be routed.
- **Fallback:** if the road file is missing, a simple graph is used instead. Each place links to its 4 nearest places, with road distance estimated as straight line × 1.3.

### 8.3 Dijkstra's algorithm (travel times)

- **What it does:** finds the **quickest path** from one node to every other node in a graph with non-negative edge weights.
- **How:**
  1. Keep a "frontier" of nodes ordered by best known time.
  2. Always settle (finalise) the closest unsettled node next.
  3. **Relax** its edges: "is going through this node quicker than what I knew?"
  4. Because times are never negative, a settled node's time is final.
- **Our implementation** uses a **binary min-heap** (a **priority queue**) to always get the closest node quickly. Complexity: **O((V + E) log V)**, where V is nodes and E is edges.
- **Time matrix:** we run Dijkstra **once per stop** to get the travel time between **every pair of stops**. For 10 stops that is a 10 × 10 table. This took about **46 ms** for 10 stops.

### 8.4 The visiting order problem (a small TSP)

- **The question:** given the time matrix, in what **order** should we visit the stops so the total time is smallest?
- This is the **Travelling Salesman Problem (TSP)**, a classic **NP-hard** problem: no known method solves large cases exactly and quickly.
- Our routes are **open**: they start at the first (or chosen) stop, visit each stop once, and **do not return**. This is called an **open TSP** or **shortest Hamiltonian path**.
- Number of possible orders for n stops with a fixed start: **(n − 1)!**
  - 8 stops: 7! = 5,040
  - 10 stops: 9! = 362,880
  - 13 stops: 12! = 479,001,600
  - 15 stops: 14! ≈ 87 billion

### 8.5 The three ways we solve it

| Method | How it works | Good | Bad |
| --- | --- | --- | --- |
| **Brute force** (with pruning) | Try every order; cut a branch as soon as it is already slower than the best found | Always optimal (**ground truth**) | Grows as (n−1)!; the API limits it to 8 stops |
| **Nearest neighbour** | Always go to the closest unvisited stop (**greedy**) | Very fast (about 0.01 ms) | Often not optimal: about 9% longer at 8 to 10 stops |
| **Ant Colony Optimisation (ACO)** | Simulated ants build orders, guided by distance and pheromone (below) | Near-optimal; cost grows only **polynomially** | A **heuristic**: usually, but not always, optimal |

**ACO is what the app uses.** The other two are for comparison, and the web app shows all three on the comparison card.

### 8.6 Ant Colony Optimisation, step by step

**The inspiration:** real ants find short paths to food by leaving **pheromone** (a scent). Shorter paths get walked more often, so they collect more pheromone, and more ants follow them. This is **swarm intelligence**: simple agents together find a good solution.

**Each round (iteration):**

1. **Build orders.** Every ant builds a full order from the start stop. At each step it picks the next unvisited stop **at random**, but with a probability proportional to
   **pheromone^α × (1 / time)^β**.
   - **Pheromone (τ, tau):** learned experience, meaning "this move was part of good orders before".
   - **Heuristic (η, eta) = 1 / time:** closer stops are more attractive.
   - **α (alpha) = 1:** weight of pheromone. **β (beta) = 2:** weight of closeness.
   - The random pick is a **roulette wheel selection**: a bigger weight means a bigger slice of the wheel.
2. **Evaporate.** Every pheromone trail loses a share: × (1 − ρ), with **ρ (rho) = 0.5**. Old information fades, so bad early choices are forgotten.
3. **Deposit.** Each ant adds **q / L** on every move of its order, where L is its total time (q = 1). Shorter orders add more.
   - **Elitist deposit:** the **best order so far** gets an extra deposit. This helps the colony converge on it.
4. **Trail limits (MAX-MIN).** Pheromone is kept between **τmin and τmax** (τmin = 0.2 × τmax). No move becomes impossible, so the ants keep exploring a little instead of all copying the first good order (this avoids **premature convergence** or **stagnation**).

**Stop:** after **200 iterations**, or earlier if there has been no better order for **100 rounds**.

**Other settings:**

- **Number of ants:** max(10, 2 × stops).
- **Starting pheromone τ0** = ants × q / (length of the nearest-neighbour order). This keeps it on the same scale as later deposits.
- **Seeded random numbers** (mulberry32, seed 42): the same input always gives the same route. That makes tests and the demo **repeatable**.
- **Cost:** about iterations × ants × n² operations, which is **polynomial** rather than factorial.

### 8.7 "Improved" vs "textbook" ACO

- **Textbook ACO:** the original **Ant System** (Dorigo, Maniezzo & Colorni, 1996) with β = 3, no elitist deposit and no trail limits.
- **Our improved ACO** adds:
  - the **elitist deposit** (idea from the Elitist Ant System);
  - **trail limits** (idea from the **MAX-MIN Ant System**, Stützle & Hoos);
  - β = 2.
- **Result:**
  - Both are always optimal at 4 to 6 stops.
  - At 8 stops: improved 100% optimal vs textbook 60%.
  - At 10 stops: improved 90% vs textbook 70%; worst gap 2.03% vs 4.48%.

### 8.8 Results (feasibility study, 5 Nov 2026)

- **Method:**
  - walking;
  - 4, 6, 8 and 10 stops, with **10 random trips per size**;
  - places from 42 sample places in George Town, Pulau Tikus, Jelutong and Gurney;
  - seeded trips (seed 2026 + n) and seeded ACO (seed 42);
  - brute force used as ground truth (raised to 10 stops for this study).
- **Improved ACO found the exact optimum in 39 of 40 trips (97.5%).**
  - The one miss was at 10 stops, 2.03% longer.
  - At 8 to 10 stops, nearest neighbour was optimal in only 3 of 20 trips and **about 9% longer** on average.
- **Speed:** a 10-stop plan takes about **46 ms (Dijkstra) + 7 ms (ACO)**, well under 0.1 s.
- **Demo route:** 6 stops in George Town, **17.9 min, 1,505 m**. Nearest neighbour gave 19.3 min (about 8% longer).
- **Optimality gap** = (method − optimum) / optimum × 100. **Opt%** = share of trips where the method found the optimum.

**Be honest:** these are **indicative**: 10 trips per size and one ACO seed. A larger test is planned: 50+ trips, several seeds, 12 to 20 stops.

### 8.9 "Why ACO if brute force is faster?" (very likely question)

- For **10 stops or fewer**, brute force with pruning is exact and fast (2.9 ms at 10 stops vs 7.26 ms for ACO). That is why it is used as **ground truth**.
- But the number of orders grows **factorially**: 479 million at 13 stops, 87 billion at 15. Pruning helps but does not stop that growth.
- ACO grows only **polynomially**, so it scales to longer trips and multi-day trips.
- ACO is also the **Intelligent Computing** component of the project.
- Next step: test 12 to 20 stops, where brute force is no longer practical. A possible extra baseline there is nearest neighbour + **2-opt** (a simple local improvement that swaps pairs of edges).

---

## 9. Food Stalls Analytics

`GET /api/analytics/overview` uses the **rated places** (currently the 55 SAMPLE places):

- **Food Places Visualisation:** totals, counts by area and cuisine, label counts, and points for a scatter chart (rating vs review count).
- **Food Places Analysis:** written **findings** sentences generated by the backend, for example "George Town has the highest average rating among areas with at least 3 rated places". Groups need at least 3 places, so one lucky place cannot top a list.
- **Food Place Suggestion:** the best rated Hidden Gems. With equal ratings, fewer reviews (less known) comes first.
- **Current numbers (sample):** average rating 4.18; 20 halal places (36%); Hidden Gems average 4.5 stars from about 66 reviews, while Popular places average 4.2 from about 1,226.

**Be honest:** these show the pipeline works; they are not claims about Penang food, because the ratings are invented.

---

## 10. The web app

- **Pages:** Landing (`/`), Discover (`/discover`), Trip (`/trip`), My Trips (`/trips`), Analytics (`/analytics`), Login, Register, Profile.
- **Map:** Leaflet with OpenStreetMap tiles; places shown with label badges, routes drawn along real roads.
- **Charts:** Recharts on the Analytics page.
- **State:**
  - `TripBasketContext` holds the places chosen for a trip.
  - `AuthContext` holds the **demo** user.
  - Saved trips and preferences are in **localStorage** (browser storage) until Phase 2B.
- **Design:** dark charcoal and orange landing page. Restyling the other pages to match is planned.
- **SAMPLE data is labelled** in the app, so nobody mistakes invented ratings for real ones.

---

## 11. Login and accounts (planned, Phase 2B)

- **Supabase Auth** will store emails and passwords. Passwords are **hashed** (stored as a scrambled, one-way value), so even we cannot read them.
- Our backend gets `/api/auth/register`, `/login` and `/refresh`, which call Supabase Auth. The apps only ever talk to our backend and never hold a Supabase key.
- After login, the user gets a **JWT** (JSON Web Token): a signed piece of text sent with each request to prove who they are. An `auth` **middleware** checks it on protected routes.
- **Why Supabase Auth instead of our own login?** Password storage is easy to get wrong. Supabase handles hashing, tokens and resets securely, and our backend still owns the Registration and Login submodules.

---

## 12. Security (what is already done)

| Risk | What we do |
| --- | --- |
| Secrets leaking | `.env` is never committed; `.env.example` has placeholders only; the old key is to be rotated |
| SQL injection | Parameterised queries only (`$1, $2`) |
| Bad input | zod validation on every request (400 on failure); body size limit 100 KB |
| Leaking internals | The error handler hides stack traces and SQL (500 `INTERNAL_ERROR`) |
| Public database access | RLS on every table; migration 004 revokes public write rights |
| Browser attacks | **helmet** sets safe HTTP headers; **CORS** allows only our web app's address |
| Powerful keys | The app never uses the Supabase `service_role` key |

- **CORS (Cross-Origin Resource Sharing):** browser rules about which websites may call our API.
- **Planned (Phase 3):** rate limiting on login (slows password guessing), `npm audit`, and a full security review.

---

## 13. Testing and quality

- **Unit tests** check one function alone (for example the hidden gem rule, Dijkstra on a small hand-drawn graph with known answers, ACO matching brute force on small cases).
- **API tests** (Supertest) call the endpoints and check the answers, including bad input.
- **Tests need no database, internet or secrets:** the database is replaced by a **mock** (a fake).
- **Count:** 277 backend tests and 93 web tests, all passing on the laptop.
- **Lint and format:** ESLint (finds mistakes) and Prettier (one code style).
- **Planned (Phase 3):** **CI** with GitHub Actions. GitHub will run lint and tests automatically on every push, with a throwaway PostGIS database.
- **Reproducible results:** `npm run feasibility` regenerates every number in the feasibility report (seeded, so the results are the same each run).

**How we work (Git):** one branch per phase, merged to `main` after tests pass and the review finds no must-fix items. Phase 1 is on `main`. The feasibility work is on `feature/feasibility-core`, not merged yet.

---

## 14. Risks, limitations and the plan

### 14.1 Limitations (say them before he finds them)

| Limitation | Effect | Plan |
| --- | --- | --- |
| Sample ratings are invented | Gem and analytics results show the method only | Google ratings for the 55 (step 2.9a); user ratings later |
| Halal tags in OSM: 2.3% | The halal filter misses untagged halal places | Google data, manual checks, user reports; show "halal unknown" honestly |
| Login is demo mode; trips saved in the browser | No real accounts; trips lost if browser data is cleared | Supabase Auth and the itinerary API (2B) |
| Fixed walking speed; assumed driving speeds | Times are estimates (no traffic, crossings, waiting) | Say so in the app; compare a few legs with a map service |
| Snapping to the nearest node | Small error at each end of a leg | Report the snap distance (already in the API); snap to road segments later |
| Benchmark is small | 10 trips per size, one seed | 50+ trips, several seeds, 12 to 20 stops (Phase 3) |
| Supabase free tier pauses when idle | The demo could fail | Open the dashboard before demos |
| No CI yet | Mistakes caught later | GitHub Actions (Phase 3) |
| Landing photos supplied by the student | Licence not confirmed | Confirm before any public release |

### 14.2 The plan (dates after today are proposed)

| When | What |
| --- | --- |
| Done (3 to 5 Nov) | **Phase 1:** database, migrations, sample data, project setup |
| Done (4 to 6 Nov) | **Phase 2A:** search, hidden gems, route planner, analytics, web prototype, feasibility study |
| About 7 to 11 Nov | **Step 2.9a:** Google Places ratings for the 55 sample places. Match only if names are similar and positions within about 100 m; report the match rate |
| About 11 to 21 Nov | **Phase 2B:** Supabase Auth login, profile and preferences, save, edit and list trips on the server |
| About 21 Nov to 1 Dec | **Phase 2C:** restyle all web pages, connect them to the new API |
| About 1 to 11 Dec | **Phase 2D:** React Native mobile app with the same features |
| About 11 to 25 Dec | **Phase 3:** CI, security review, larger route test (12 to 20 stops) |

**End goal:** a web and mobile app with all 13 submodules working, real ratings and user accounts.

**Google ratings note:** Google's terms only allow the **place ID** to be stored permanently, so ratings are refreshed by re-running the script.

---

## 15. Likely questions and short answers

**About the idea**

- **What problem does it solve?** Tourists find only the famous places; good small stalls are hard to find, and visiting several places in a good order is hard to plan. MyMakanRoute finds hidden gems and plans the shortest route between them.
- **Who are the users?** Tourists and locals in Penang (Guest and Registered user), plus an Admin who updates the place data.
- **How is it different from Google Maps?** Google Maps lists places and routes one destination at a time. We **label hidden gems** (high rating, few reviews) and **optimise the order** of several stops in one trip.

**About data**

- **Where does the data come from?** OpenStreetMap for places and roads; Google Places ratings next.
- **Are the ratings real?** No. The 55 sample places have invented ratings, clearly marked SAMPLE. They prove the method works. Real Google ratings are the next step.
- **Why not scrape Google or TripAdvisor?** It breaks their terms of service. We use the official Google Places API instead.
- **Why only 2.3% halal?** OSM volunteers rarely tag halal. We show "halal unknown" honestly and plan better sources.

**About the algorithms**

- **What is Dijkstra used for?** To get the walking time between every pair of chosen places along real roads (the time matrix).
- **Why not straight-line distance?** Roads are not straight. Real road times give realistic routes (straight line × 1.3 is only the fallback).
- **What is ACO used for?** To choose the order of the stops, using the time matrix.
- **Why ACO and not a genetic algorithm?** Both are valid metaheuristics. ACO was designed for path and ordering problems like the TSP, builds solutions step by step along edges, and fits a route planner naturally.
- **Is ACO always optimal?** No, it is a heuristic. In our test it found the optimum in 39 of 40 trips; the one miss was 2.03% longer.
- **How do you know the optimum?** Brute force tries every order, so it is exact. We used it as ground truth up to 10 stops.
- **Why open routes?** Food hopping usually ends at the last stop; people don't need to walk back to the start. A round trip can be added as an option.
- **What are α, β, ρ?** α = weight of pheromone (experience), β = weight of closeness, ρ = evaporation rate (how fast old pheromone fades).
- **Why seed 42?** A fixed seed makes results repeatable for tests and the demo. Several seeds will be tested in the larger evaluation.
- **What is the time complexity?**
  - Dijkstra with a heap: O((V + E) log V) per stop.
  - ACO: about O(iterations × ants × n²).
  - Brute force: O((n − 1)!).

**About the system**

- **Why Supabase?** Free hosted PostgreSQL with PostGIS, plus a built-in secure login service.
- **Why is the road network not in the database?** It is used on every route request; keeping it in memory is faster. It loads once in about 0.2 s.
- **Why a backend at all? Why not call Supabase from the app?** To keep secrets off the device, keep all rules and algorithms in one place, and let web and mobile share the same API.
- **How do you keep the database safe?** RLS on, public rights revoked, parameterised SQL, no service_role key in the app, secrets only in `.env`.
- **How do you test it?** 277 backend and 93 web automated tests, with a mocked database; brute force checks ACO; results are seeded and reproducible.

**About progress and plan**

- **What is done?** 7 of 13 submodules fully built; 6 partial (screens work in demo mode). All four modules run end to end.
- **What is the biggest risk?** Real ratings. The hidden gem idea depends on them, and OSM has none.
- **Is the timeline realistic?** The hardest parts (data, route planner, hidden gem rule) are done. What remains is mostly standard features: login, saving and screens.

---

## 16. Numbers card (memorise these)

| Number | What it is |
| ---: | --- |
| 4 / 13 | modules / submodules |
| 7 / 6 | submodules built / partial |
| 1,241 | places in the database (1,186 OSM + 55 SAMPLE) |
| 1,298 → 1,241 | raw OSM elements → named and imported (95.6%) |
| 26,689 / 34,732 | road nodes / road edges |
| 99% | walking nodes in the main connected part |
| 6 | database tables |
| 0% / 2.3% / 23.2% / 45.4% | OSM places with rating / halal / opening hours / cuisine |
| 4.3 and 1–100 | hidden gem: min rating and review range |
| 14 / 35 / 6 | Hidden Gem / Popular / no label (55 sample places) |
| 704 | places within 1.5 km of Komtar |
| 39 of 40 (97.5%) | trips where improved ACO found the optimum |
| 2.03% | worst ACO gap (one 10-stop trip) |
| about 9% | how much longer nearest neighbour is at 8–10 stops |
| 46 ms + 7 ms | Dijkstra + ACO time for 10 stops |
| 17.9 min, 1,505 m | 6-stop demo route (nearest neighbour 19.3 min) |
| 1.4 m/s | walking speed (about 5 km/h) |
| 200 / 100 / 42 | ACO max iterations / early-stop rounds / seed |
| α 1, β 2, ρ 0.5 | ACO weights and evaporation |
| 2 to 10 | stops allowed per route; brute force up to 8 in the API |
| 100 to 5,000 m | search radius range (default 1,500) |
| 277 / 93 | backend / web tests, all passing |

---

## 17. Glossary (A to Z)

- **ACO (Ant Colony Optimisation):** a swarm intelligence method where simulated ants build solutions guided by pheromone and closeness.
- **Adjacency list:** for each node, the list of nodes it connects to directly (how the graph is stored in memory).
- **Ant System:** the original ACO by Dorigo et al. (1996); our "textbook" baseline.
- **API (Application Programming Interface):** the server program the apps talk to, through fixed URLs.
- **AppError:** our error type for expected problems (for example 404), turned into a clean JSON answer.
- **Baseline:** a simple method used for comparison (nearest neighbour, brute force).
- **Binary min-heap:** a structure that always gives back the smallest item quickly; used as Dijkstra's priority queue.
- **Bounding box (bbox):** the rectangle of map area we cover (5.33 to 5.46 N, 100.27 to 100.345 E).
- **Brute force:** trying every possible answer; exact but slow for large inputs.
- **CI (Continuous Integration):** automatic lint and tests on every push (GitHub Actions, planned).
- **Connected component:** a group of nodes that can all reach each other.
- **Controller / Service / Model:** request handling / business logic / SQL queries (our layered structure).
- **CORS:** browser rules about which websites may call our API.
- **Dijkstra's algorithm:** finds the shortest (quickest) path in a graph with non-negative weights.
- **Edge:** a connection between two nodes; here a piece of road with a length and time.
- **Elitist deposit:** extra pheromone on the best order found so far.
- **Evaporation (ρ):** pheromone fading each round, so old choices are forgotten.
- **Express:** the Node.js web framework our backend uses.
- **Foreign key (FK):** a column linking to another table's primary key.
- **GiST index:** a spatial index for fast location searches in PostGIS.
- **Graph:** nodes connected by edges.
- **Greedy algorithm:** always takes the best-looking next step (nearest neighbour); fast but not always optimal.
- **Haversine / great-circle distance:** straight-line distance on the Earth's surface between two GPS points.
- **Heuristic (in ACO, η = 1/time):** a rule of thumb; prefer closer stops.
- **Heuristic method:** a method that usually finds a good answer but does not guarantee the best.
- **Hidden gem:** a place with rating ≥ 4.3 and 1 to 100 reviews.
- **JSON:** the text format data is sent in.
- **JWT (JSON Web Token):** a signed token proving who the user is after login (planned).
- **Leaflet:** the free map library used in the web app.
- **localStorage:** storage inside the browser; used for demo-mode data.
- **MAX-MIN Ant System (MMAS):** an ACO variant that keeps pheromone between limits to avoid stagnation.
- **Metaheuristic:** a general strategy for searching for good solutions (ACO, genetic algorithms, simulated annealing).
- **Middleware:** code that runs before or after each request (validation, error handling, auth).
- **Migration:** a numbered SQL file that changes the database structure.
- **Mock:** a fake replacement (for example of the database) used in tests.
- **Nearest neighbour:** greedy routing; always go to the closest unvisited stop.
- **Node:** a point in a graph; here a road junction or road end (a road node).
- **NP-hard:** a class of problems with no known fast exact method for large inputs (the TSP is one).
- **Open route:** visits every stop once, does not return to the start.
- **Optimality gap:** how much longer than the optimum a route is, in percent.
- **OSM (OpenStreetMap):** a free world map made by volunteers; our source for places and roads.
- **Overpass API:** a public service for downloading OSM data.
- **Parameterised query:** SQL with placeholders ($1, $2) so user input cannot change the query (prevents SQL injection).
- **Pheromone (τ):** in ACO, the learned value of a move; more for moves in short orders.
- **PostGIS:** a PostgreSQL add-on for map locations and distances.
- **PostgreSQL:** an open-source relational (SQL) database.
- **Primary key (PK):** the column that uniquely identifies each row.
- **Priority queue:** a queue that always gives back the most urgent (smallest) item first.
- **Pruning:** stopping a search branch early because it cannot beat the best answer so far.
- **Pure function:** same input always gives the same output, with no side effects; easy to test.
- **React / React Native:** UI libraries for web / mobile apps.
- **REST:** an API style where URLs are resources and HTTP methods (GET, POST) are actions.
- **RLS (Row Level Security):** database rules about which rows a user may see.
- **Roulette wheel selection:** random choice where bigger weights get a bigger chance.
- **Seed (random):** a starting number that makes "random" results repeatable.
- **Snapping:** matching a place to its nearest road node.
- **SRID 4326 (WGS 84):** the standard GPS coordinate system.
- **Stagnation:** when all ants keep building the same order and stop exploring.
- **Supabase:** hosted PostgreSQL + PostGIS + login service.
- **Supabase Auth:** Supabase's login service (planned for Phase 2B).
- **Swarm intelligence:** many simple agents together producing smart behaviour (ants, bees, birds).
- **Time matrix:** a table of travel times between every pair of chosen stops.
- **TSP (Travelling Salesman Problem):** find the shortest order to visit all points.
- **Unit test / API test:** a test of one function / of a whole endpoint.
- **UUID:** a long random unique id used as a primary key.
- **Vite:** a fast development server and build tool for the web app.
- **zod:** the library that checks request input against rules.

---

## 18. Things not to overclaim

- Do **not** say the ratings or analytics findings are real; they are invented SAMPLE data.
- Do **not** say login or saved trips work on the server yet; they are demo mode until Phase 2B.
- Do **not** say ACO is always optimal; it is a heuristic (39 of 40 in a small test).
- Do **not** say ACO is faster than brute force at 10 stops; it is not. The case for ACO is **scalability** for longer trips, and it is the intelligent computing part.
- Do **not** say walking times are exact; speeds are assumptions.
- Do **not** say the benchmark is final; it is indicative, and a larger one is planned.
- The mobile app is **planned**, not started.

If you don't know an answer, say: "I have not tested that yet; I will check and add it to the next report." That is a strong answer in a feasibility meeting.
