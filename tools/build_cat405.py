#!/usr/bin/env python3
"""CAT405 Final Year Project notes page. There are no lecture slides: the source is the owner's own project folder
(CAT405/DEVELOPMENT/MyMakanRoute: README, CLAUDE.md, docs/PLAN, FEASIBILITY, architecture, erd, module-status,
the presentation study guide, and the backend / web source). `.env` and `.mcp.json` were never read.
Content rules: only what is in those files; anything that is my own sum, reading or link is labelled on the page.
Diagrams are redrawn as inline SVG (the project's own PNG diagrams are not copied).

Six topics (one story of the project): 1 the idea and the plan, 2 the data, 3 hidden gems and search,
4 the route planner, 5 the proof (feasibility), 6 the application (backend and web).
Extra sections: #eytk (the owner's own study guide, tools/eytk.md, converted), #status (status, risks, next steps) and #meeting (supervisor meeting preparation)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
from notes_lib import mindmap, terms, psn, qa, week, E

OUT = os.path.join(ROOT, 'cat405')
os.makedirs(OUT, exist_ok=True)

# ====================================================================== tiny SVG helpers (same idea as build_cmt323.py)
def svg(w, h, inner, label, uid):
    return (f'<div class="dgw" tabindex="0" role="group" aria-label="Scrollable diagram">'
            f'<svg class="dg" viewBox="0 0 {w} {h}" role="img" aria-label="{E(label)}" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><marker id="ah{uid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path class="ah" d="M0 0L10 5L0 10z"/></marker>'
            f'<marker id="af{uid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path class="ah fb" d="M0 0L10 5L0 10z"/></marker></defs>'
            f'{inner}</svg></div>')


def box(x, y, w, h, lines, cls='bx', bold=True, small_rest=False):
    on = ' ton' if cls == 'bxs' else ''
    out = f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>'
    n, lh = len(lines), 19
    y0 = y + h / 2 - (n - 1) * lh / 2 + 5
    for i, line in enumerate(lines):
        c = 'tb' if (bold and i == 0) else ('ts' if small_rest else '')
        out += f'<text class="{c}{on}" x="{x + w / 2}" y="{y0 + i * lh:.1f}" text-anchor="middle">{E(line)}</text>'
    return out


def txt(x, y, s, cls='', anchor='middle'):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{E(s)}</text>'


def arr(x1, y1, x2, y2, uid, dash=False, fb=False, both=False):
    cls = 'ln' + (' dash' if dash else '') + (' fb' if fb else '')
    m = 'af' if fb else 'ah'
    start = f' marker-start="url(#{m}{uid})"' if both else ''
    return f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#{m}{uid})"{start}/>'


def ln(x1, y1, x2, y2, dash=False):
    return f'<line class="ln{" dash" if dash else ""}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'


def bus(uid, left, mid, right, label, tag_in, tag_out):
    """left boxes -> middle box -> right boxes (used for event-driven and publish-subscribe)."""
    h = 56
    n = max(len(left), len(right))
    H = 40 + n * 74
    cy = H / 2
    inner = ''
    for i, nm in enumerate(left):
        y = 24 + i * 74 + (n - len(left)) * 37
        inner += box(20, y, 170, h, nm) + arr(190, y + h / 2, 275, cy, uid)
    for i, nm in enumerate(right):
        y = 24 + i * 74 + (n - len(right)) * 37
        inner += box(510, y, 170, h, nm) + arr(425, cy, 510, y + h / 2, uid)
    inner += box(275, cy - 48, 150, 96, mid, 'bxs')
    inner += txt(232, cy - 62 if False else 16, tag_in, 'ts') + txt(468, 16, tag_out, 'ts')
    return svg(700, H, inner, label, uid)



# ====================================================================== mind maps
MAPS = {
1: mindmap('MyMakanRoute',
  [('What it is', ['Food hopping planner', 'Starts with Penang', 'Finds hidden gems', 'Plans a multi-stop trip']),
   ('Who uses it', ['Tourists and locals', 'Guest and registered user', 'Admin updates place data']),
   ('Why Intelligent Computing', ['Ant Colony Optimisation', 'Swarm intelligence', 'Picks the visiting order'])],
  [('4 modules, 13 submodules', ['User Management', 'Food Discovery', 'Food Hopping', 'Food Stalls Analytics', 'Names fixed by the proposal']),
   ('Phases', ['1 Foundation (done)', '2A Core backend and web', '2B Real login and trips', '2C Web, 2D Mobile', '3 CI, security, bigger test']),
   ('How it is built', ['One branch per phase', 'Commit only when tests pass', 'No push without the student', 'Never document unbuilt work'])],
  'Mind map of Topic 1: what MyMakanRoute is, its modules, phases and way of working'),
2: mindmap('The Data',
  [('Where it comes from', ['OpenStreetMap places', 'OpenStreetMap roads', 'Overpass API, saved snapshots', '55 SAMPLE places']),
   ('What OSM lacks', ['0% ratings', '2.3% halal tag', '23.2% opening hours', '45.4% cuisine']),
   ('Honest rule', ['Sample ratings are invented', 'Marked SAMPLE everywhere', 'Shows the method works'])],
  [('Database', ['Supabase PostgreSQL', 'PostGIS for map distance', 'Six tables', 'Plain SQL with pg']),
   ('Migrations', ['001 places', '002 profiles, preferences', '003 itineraries and stops', '004 lock down public access']),
   ('Road graph', ['26,689 nodes', '34,732 edges', 'A file, loaded into memory', '99% walking nodes connected'])],
  'Mind map of Topic 2: the data sources, what is missing, the database and the road graph'),
3: mindmap('Hidden Gems and Search',
  [('Search', ['Location and radius', 'PostGIS ST_DWithin', 'GiST spatial index', 'Radius 100 to 5,000 m']),
   ('Filters', ['Halal, price, cuisine', 'Dietary tags', 'Open now', 'Label']),
   ('Open now', ['Malaysian time zone', 'Past-midnight ranges', 'No hours counts as closed'])],
  [('Hidden gem rule', ['Rating 4.3 or more', '1 to 100 reviews', 'Popular: over 100 reviews', 'Otherwise no label']),
   ('Ranking', ['Gems first', 'Then Popular, then none', 'Nearest first in a group', 'Rating breaks ties']),
   ('Test of the rule', ['Sensitivity table', '14 gems at the default', 'Gap: no 101 to 200 reviews'])],
  'Mind map of Topic 3: searching, filters, the hidden gem rule and ranking'),
4: mindmap('The Route Planner',
  [('Step 1: the graph', ['Nodes are junctions', 'Edges are road pieces', 'Walk 1.4 m/s', 'Driving speed by road type']),
   ('Step 2: snapping', ['Place to nearest road node', 'Grid of about 220 m', 'Over 1 km: cannot route']),
   ('Step 3: Dijkstra', ['Quickest path from a stop', 'Binary min-heap', 'One run per stop', 'Gives the time matrix'])],
  [('Step 4: the order', ['Open TSP, NP-hard', '(n-1)! possible orders', 'Brute force: exact', 'Nearest neighbour: greedy']),
   ('Ant Colony Optimisation', ['Ants build orders', 'Pheromone and closeness', 'Evaporate, then deposit', 'Seeded: repeatable']),
   ('Improved vs textbook', ['Elitist deposit', 'MAX-MIN trail limits', 'Beta 2 instead of 3'])],
  'Mind map of Topic 4: the graph, snapping, Dijkstra and the three ways to choose the order'),
5: mindmap('The Proof',
  [('Method', ['Walking, 42 sample places', '4, 6, 8, 10 stops', '10 random trips per size', 'Brute force = the optimum']),
   ('Results', ['ACO optimal in 39 of 40', 'Worst gap 2.03%', 'Nearest neighbour about 9% longer', '46 ms + 7 ms for 10 stops']),
   ('Worked example', ['6 stops in George Town', '17.9 min, 1,505 m', 'Nearest neighbour 19.3 min'])],
  [('Honest points', ['Only 10 trips per size', 'One ACO seed', 'Sample ratings invented', 'Brute force is faster at 10']),
   ('Why still ACO', ['Orders grow factorially', '13 stops: 479 million', 'ACO grows polynomially', 'The intelligent part']),
   ('Next test', ['50+ trips, several seeds', '12 to 20 stops', 'Maybe 2-opt baseline'])],
  'Mind map of Topic 5: the feasibility study, its results and its limits'),
6: mindmap('The Application',
  [('Three layers', ['Web and mobile apps', 'Express API (logic)', 'PostgreSQL data', 'Apps never touch the database']),
   ('Inside a module', ['Routes: URLs and checks', 'Controller: request and reply', 'Service: the logic', 'Model: parameterised SQL']),
   ('API rules', ['REST and JSON', 'Same reply shape always', 'zod checks every request', 'No internals in errors'])],
  [('Web app', ['React 19 and Vite', 'Leaflet map, Recharts', 'Trip basket, max 10 stops', 'Demo mode until 2B']),
   ('Security', ['Parameterised SQL', 'RLS on every table', 'helmet and CORS', 'No service_role key']),
   ('Testing', ['Jest, Supertest, Vitest', 'Mocked database', 'Seeded, reproducible', 'CI planned in Phase 3'])],
  'Mind map of Topic 6: layers, module structure, API rules, web app, security and testing'),
}

# ====================================================================== visuals
d_layers = svg(700, 300,
    box(20, 14, 660, 64, ['Presentation layer', 'React + Vite web app (built).  React Native + Expo mobile app (planned, folder empty).'], small_rest=True)
    + arr(350, 78, 350, 108, 'ly', both=True)
    + box(20, 108, 660, 64, ['Application layer: backend API', 'Node.js + Express 4. All rules and algorithms live here (Dijkstra, ACO, hidden gem rule).'], 'bxs', small_rest=True)
    + arr(350, 172, 350, 202, 'ly', both=True)
    + box(20, 202, 660, 64, ['Data layer', 'Supabase: PostgreSQL + PostGIS (places, users, trips).  Road graph kept in memory from a file.'], small_rest=True)
    + txt(350, 290, 'Redrawn from docs/architecture.md. The apps never call the database; only the backend does.', 'ts'),
    'Redrawn: the three layers of MyMakanRoute and what sits in each', 'ly')

d_erd = svg(700, 285,
    box(20, 16, 150, 70, ['profiles', 'id, display_name, role'], small_rest=True)
    + box(260, 16, 170, 70, ['itineraries', 'title, mode, total time'], small_rest=True)
    + box(520, 16, 160, 70, ['itinerary_stops', 'position, place_id'], small_rest=True)
    + box(520, 150, 160, 70, ['places', 'location, rating, halal'], 'bxs', small_rest=True)
    + box(20, 150, 150, 70, ['preferences', 'halal, price, cuisines'], small_rest=True)
    + arr(170, 51, 260, 51, 'er') + arr(430, 51, 520, 51, 'er') + arr(600, 86, 600, 150, 'er') + arr(95, 86, 95, 150, 'er')
    + txt(215, 42, 'owns', 'ts') + txt(475, 42, 'contains', 'ts') + txt(640, 124, 'visited in', 'ts') + txt(130, 124, 'has one', 'ts')
    + txt(350, 252, 'Redrawn from docs/erd.md. All arrows are one-to-many except profiles to preferences (one-to-one).', 'ts')
    + txt(350, 273, 'Only places is used by the API today; the other tables are ready for Phase 2B.', 'ts'),
    'Redrawn: the entity relationship diagram of the six-table database', 'er')

d_gem = svg(700, 250,
    box(20, 95, 170, 60, ['A food place', 'rating and reviews'], small_rest=True)
    + arr(190, 125, 250, 125, 'gm')
    + box(250, 95, 190, 60, ['Has a rating and', 'at least 1 review?'], 'bxs', bold=False)
    + arr(440, 125, 500, 52, 'gm') + arr(440, 125, 500, 125, 'gm') + arr(440, 125, 500, 205, 'gm')
    + box(490, 22, 200, 60, ['Hidden Gem', 'rating 4.3+, 1 to 100 reviews'], small_rest=True)
    + box(500, 95, 180, 60, ['Popular', 'more than 100 reviews'], small_rest=True)
    + box(500, 175, 180, 60, ['No label', 'everything else'], small_rest=True)
    + txt(250, 60, 'No rating or 0 reviews: no label', 'ts', 'start')
    + txt(350, 247, 'Redrawn from docs/FEASIBILITY.md and hiddenGem.js. Thresholds are settings, not fixed code.', 'ts'),
    'Redrawn: the hidden gem decision rule', 'gm')

d_route = svg(700, 130,
    box(10, 30, 120, 66, ['Road graph', '26,689 nodes'], small_rest=True) + arr(130, 63, 160, 63, 'rt')
    + box(160, 30, 120, 66, ['Snap', 'place to node'], small_rest=True) + arr(280, 63, 310, 63, 'rt')
    + box(310, 30, 120, 66, ['Dijkstra', 'time matrix'], small_rest=True) + arr(430, 63, 460, 63, 'rt')
    + box(460, 30, 120, 66, ['ACO', 'visiting order'], 'bxs', small_rest=True) + arr(580, 63, 600, 63, 'rt')
    + box(600, 30, 92, 66, ['Legs', 'path to draw'], small_rest=True),
    'Redrawn: the five stages of the route planner', 'rt')

d_aco = svg(700, 130,
    box(10, 30, 150, 66, ['1. Build orders', 'ants pick next stop'], small_rest=True) + arr(160, 63, 190, 63, 'ac')
    + box(190, 30, 150, 66, ['2. Evaporate', 'x (1 - rho)'], small_rest=True) + arr(340, 63, 370, 63, 'ac')
    + box(370, 30, 150, 66, ['3. Deposit', 'q / L, plus elitist'], small_rest=True) + arr(520, 63, 550, 63, 'ac')
    + box(550, 30, 140, 66, ['4. Trail limits', 'MAX-MIN, then repeat'], 'bxs', small_rest=True)
    + txt(350, 120, 'One round. Up to 200 rounds; stop early after 100 rounds with no better order.', 'ts'),
    'Redrawn: one round of the improved Ant Colony Optimisation', 'ac')

d_flow = svg(700, 130,
    box(10, 30, 120, 66, ['Pick a place', 'e.g. Komtar'], small_rest=True) + arr(130, 63, 155, 63, 'fl')
    + box(155, 30, 120, 66, ['Browse', 'gems first'], small_rest=True) + arr(275, 63, 300, 63, 'fl')
    + box(300, 30, 120, 66, ['Add 2 to 10', 'places'], small_rest=True) + arr(420, 63, 445, 63, 'fl')
    + box(445, 30, 120, 66, ['Plan route', 'walk or drive'], 'bxs', small_rest=True) + arr(565, 63, 590, 63, 'fl')
    + box(590, 30, 100, 66, ['Save trip', 'needs login'], small_rest=True)
    + txt(350, 120, 'Redrawn from docs/user-flow.md (planned path). If unhappy with the route, reorder or remove stops and plan again.', 'ts'),
    'Redrawn: the planned user flow from choosing a place to saving a trip', 'fl')

def bars(rows, uid, label):
    """rows: (name, pct 0-100, note). Horizontal bars, redrawn from the results table."""
    H = 20 + len(rows) * 38
    inner = ''
    for i, (nm, pct, note) in enumerate(rows):
        y = 12 + i * 38
        inner += txt(212, y + 19, nm, 'ts', 'end') + f'<rect class="bx" x="222" y="{y}" width="320" height="26" rx="8"/>'
        inner += f'<rect class="bxs" x="222" y="{y}" width="{3.2 * pct:.0f}" height="26" rx="8"/>'
        inner += txt(550, y + 19, note, 'ts', 'start')
    return svg(700, H, inner, label, uid)

d_bars = bars([('Improved ACO, 4 stops', 100, '100%'), ('Improved ACO, 6 stops', 100, '100%'), ('Improved ACO, 8 stops', 100, '100%'), ('Improved ACO, 10 stops', 90, '90%'),
               ('Textbook ACO, 8 stops', 60, '60%'), ('Textbook ACO, 10 stops', 70, '70%'),
               ('Nearest neighbour, 8 stops', 10, '10%'), ('Nearest neighbour, 10 stops', 20, '20%')],
              'bs', 'Redrawn bar chart: share of 10 trips in which each method found the exact optimum, by number of stops')

NOTE = '<p class="small"><b>Source note:</b> there are no slides for CAT405. Everything below comes from the owner&rsquo;s own project folder (README, plan, feasibility report, architecture notes, ERD, module status, code). Sums, readings and links I added are marked &ldquo;my own&rdquo;.</p>'

# ---------------------------------------------------------------- topic 1
w1_vis = f'''{NOTE}
  <h3>The project in 30 seconds</h3>
  <p class="small">MyMakanRoute is a <b>food hopping and food discovery planner</b>, starting with Penang. It helps tourists and locals find <b>hidden gems</b>: food places that are well rated but not yet well known. The user picks a few places and the app plans the shortest walking route between them. Dijkstra&rsquo;s algorithm on a real OpenStreetMap road network gives the walking times, and Ant Colony Optimisation chooses the visiting order. It is a CAT405 final year project in the Intelligent Computing major; the nature-inspired ACO is the &ldquo;intelligent computing&rdquo; part.</p>
  <h3>The user&rsquo;s path</h3>
  {d_flow}
  <h3>Four modules, thirteen submodules (names fixed by the proposal)</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Module</th><th>Submodules</th><th>Status on 5 Nov 2026</th></tr></thead><tbody>
  <tr><th>User Management</th><td>Registration, Login, Profile and Preference Setup</td><td>Partial: web screens in demo mode</td></tr>
  <tr><th>Food Discovery</th><td>Food Place Searching, Hidden Gem Highlighting, Food Place Visualisation</td><td>Built</td></tr>
  <tr><th>Food Hopping</th><td>Itinerary Planner, Route Planner, Itinerary Review and Customisation, Past Food Hopping Visualisation</td><td>Route Planner built; the other three partial</td></tr>
  <tr><th>Food Stalls Analytics</th><td>Food Places Visualisation, Food Places Analysis, Food Place Suggestion</td><td>Built</td></tr></tbody></table></div>
  <p class="small"><b>Built (7)</b> means a server part (API), a web page and automated tests. <b>Partial (6)</b> means the web screen works in <b>demo mode</b> (login does not check a real password; data sits in the browser) while the database tables are ready. Filtering (halal, budget, cuisine, dietary, open now) is <b>not</b> a module: it lives inside Food Discovery and Food Hopping.</p>
  <h3>The plan, phase by phase</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Phase</th><th>What</th><th>When (later dates are proposals)</th></tr></thead><tbody>
  <tr><th>1 Foundation</th><td>Database, migrations, sample data, project setup</td><td>Done, 3 to 5 Nov</td></tr>
  <tr><th>2A Core</th><td>Search, hidden gems, route planner, analytics, web prototype, feasibility study</td><td>Built, under review</td></tr>
  <tr><th>Step 2.9a</th><td>Google Places ratings for the 55 sample places</td><td>About 7 to 11 Nov</td></tr>
  <tr><th>2B Real accounts</th><td>Supabase Auth login, profile, preferences, saved trips on the server</td><td>About 11 to 21 Nov</td></tr>
  <tr><th>2C Web</th><td>Restyle all pages, connect to the new API</td><td>About 21 Nov to 1 Dec</td></tr>
  <tr><th>2D Mobile</th><td>React Native app with the same features</td><td>About 1 to 11 Dec</td></tr>
  <tr><th>3 Finish</th><td>CI, security review, larger route test (12 to 20 stops)</td><td>About 11 to 25 Dec</td></tr></tbody></table></div>
  <h3>Decisions fixed in the plan (3 Nov)</h3>
  <ul class="chips-row"><li>Login goes through Supabase Auth, called by our own backend; apps never hold a Supabase key</li><li>Hidden gem has three labels</li><li>Plain SQL with <code>pg</code>, no heavy ORM</li><li>A tiny home-made migration runner</li><li>Seed data uses real OSM names with invented values, marked SAMPLE</li><li>Road graph from OSM; walking by default</li><li>Open route (no return to the start)</li><li>JavaScript, not TypeScript</li></ul>
  <h3>How the work is run</h3>
  <p class="small">The repo defines helper agents for Claude Code (planner, code-writer, tester, code-reviewer, security-reviewer, docs-writer). The rules in the project&rsquo;s own guide: one branch per phase, commit only when tests pass, never push without the student&rsquo;s say-so, and never document a feature that is not built.</p>
'''
w1_terms = terms([
 ('Food hopping', 'Visiting several food places in one trip.'),
 ('Hidden gem', 'A place with a high rating but few reviews, so not yet well known.'),
 ('Module / submodule', 'The proposal&rsquo;s fixed building blocks: 4 modules, 13 submodules. The names never change.'),
 ('Demo mode', 'A screen that works, but with fake login and data kept in the browser (localStorage), until the real server part is built.'),
 ('Phase', 'A chunk of work on its own Git branch, merged to <code>main</code> after tests pass.'),
 ('Intelligent Computing', 'The student&rsquo;s major. Here it shows up as Ant Colony Optimisation, a swarm intelligence method.'),
])
w1_boss = ''.join([
 qa('What problem does MyMakanRoute solve, and how is it different from Google Maps?',
  '<p>Tourists tend to find only the famous places, good small stalls are hard to find, and ordering several stops well is hard. It <b>labels hidden gems</b> (high rating, few reviews) and <b>optimises the order of several stops</b> in one trip. Google Maps lists places and routes one destination at a time.</p>', 1),
 qa('Name the four modules and say how many submodules are built.',
  '<p>User Management, Food Discovery, Food Hopping, Food Stalls Analytics: 13 submodules. <b>7 built</b>, <b>6 partial</b> (demo mode or browser only). Both counts are from the project&rsquo;s module-status file.</p>', 2),
 qa('Why is filtering not a module?',
  '<p>It was not in the proposal&rsquo;s module list. It is a feature inside Food Discovery and Food Hopping. The module names are fixed, so it was not promoted to one.</p>', 3),
 qa('What does &ldquo;Intelligent Computing&rdquo; mean for this project?',
  '<p>The route planner picks the visiting order with <b>Ant Colony Optimisation</b>, a swarm-intelligence (nature-inspired) method.</p>', 4),
])

# ---------------------------------------------------------------- topic 2
w2_vis = f'''{NOTE}
  <h3>Where the data comes from</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Data</th><th>Source</th><th>How much</th><th>Stored in</th></tr></thead><tbody>
  <tr><th>Food places</th><td>OpenStreetMap (OSM), tags restaurant, fast_food, food_court, cafe</td><td>1,298 raw elements; 1,241 named and imported (95.6%)</td><td>Supabase <code>places</code> table</td></tr>
  <tr><th>Sample places</th><td>55 of those real OSM places with <b>invented</b> ratings, reviews, price, halal, hours and dietary tags</td><td>55</td><td><code>places</code>, flagged <code>is_sample</code></td></tr>
  <tr><th>Road network</th><td>OSM roads, same area</td><td>26,689 nodes, 34,732 edges</td><td>File <code>data/road-graph-penang.json</code> (about 2.5 MB), loaded into memory</td></tr></tbody></table></div>
  <p class="small">The database holds <b>1,241 places</b> = 1,186 OSM rows + 55 SAMPLE rows. The area is the box 5.33 to 5.46 N, 100.27 to 100.345 E (Gelugor/USM to George Town). Data is fetched from the <b>Overpass API</b>; the scripts retry several servers and save a snapshot in <code>data/</code> so a busy server cannot break a demo. The road network is a file because the route planner reads all of it on every request; it loads once in about 0.2 s.</p>
  <h3>What OSM has, and what it does not</h3>
  <div class="tbl-wrap"><table><thead><tr><th></th><th>OSM (1,186)</th><th>SAMPLE (55)</th></tr></thead><tbody>
  <tr><th>Name</th><td>100%</td><td>100%</td></tr><tr><th>Cuisine</th><td>45.4%</td><td>100%</td></tr><tr><th>Opening hours</th><td>23.2%</td><td>100%</td></tr><tr><th>Halal tag</th><td><b>2.3%</b></td><td>100%</td></tr><tr><th>Rating</th><td><b>0%</b></td><td>100%</td></tr></tbody></table></div>
  <p class="small"><b>The key finding:</b> OSM is good for <i>where</i> places are and weak on <i>what they are like</i>. With no ratings at all, the hidden gem rule cannot run on OSM alone. That is why the SAMPLE places exist and why real Google ratings are the next step. Be honest: sample ratings are invented, so results built on them show that the <b>method</b> works, not facts about Penang food.</p>
  <p class="small"><i>My own note:</i> the plan file quotes slightly different percentages (97% named, 42% cuisine, 25% hours, 2% halal) for the raw snapshot; the feasibility report quotes the figures above for the imported rows. This page uses the feasibility figures.</p>
  <h3>The database</h3>
  {d_erd}
  <div class="tbl-wrap"><table><thead><tr><th>Table</th><th>Holds</th><th>Used by the API today?</th></tr></thead><tbody>
  <tr><th>places</th><td>Name, cuisine, area, location (map point), halal, price level, rating, review count, opening hours, source, sample flag</td><td>Yes</td></tr>
  <tr><th>profiles</th><td>One row per user: display name, role (user or admin)</td><td>Not yet (2B)</td></tr>
  <tr><th>preferences</th><td>Default filters: halal only, max price, cuisines, dietary</td><td>Not yet (2B)</td></tr>
  <tr><th>itineraries</th><td>Saved trips: title, travel mode, totals</td><td>Not yet (2B)</td></tr>
  <tr><th>itinerary_stops</th><td>The ordered stops of each trip (junction table with a <code>position</code>)</td><td>Not yet (2B)</td></tr>
  <tr><th>schema_migrations</th><td>Which migration files have run</td><td>By the migration runner</td></tr></tbody></table></div>
  <h3>Migrations: building the database the same way everywhere</h3>
  <ul class="chips-row"><li>001: places, PostGIS, a <code>nearby_places()</code> function (not used by the API)</li><li>002: profiles and preferences</li><li>003: itineraries and stops, with a deferrable unique (trip, position)</li><li>004: revoke Supabase public rights, switch on RLS</li></ul>
  <p class="small"><code>migrate.js</code> runs the numbered SQL files in order, each in a transaction, and records them in <code>schema_migrations</code>, so running it twice applies nothing new. <code>seed.js</code> checks the data with zod and upserts by <code>osm_id</code>; the OSM import never overwrites SAMPLE rows. There is deliberately <b>no foreign key to Supabase&rsquo;s own auth table</b>, so the same migrations also run on a plain PostgreSQL test database.</p>
  <h3>Database security</h3>
  <p class="small"><b>Row Level Security</b> is on for every table: <code>places</code> has one read-only rule, the others have none, so the public sees nothing in them. Supabase publishes tables through a public REST API automatically, so migration 004 revokes write rights from its <code>anon</code> and <code>authenticated</code> roles. Our backend connects as the table owner, so these rules do not limit it. The powerful <code>service_role</code> key is never used in the app.</p>
'''
w2_terms = terms([
 ('OpenStreetMap (OSM)', 'A free world map made by volunteers; the source of places and roads.'),
 ('Overpass API', 'A public service for downloading OSM data.'),
 ('Supabase', 'Hosted PostgreSQL + PostGIS + a login service (Supabase Auth). Our project is in the Singapore region, free tier.'),
 ('PostGIS', 'A PostgreSQL add-on for map locations and distances.'),
 ('geography(Point, 4326)', 'The location column type; 4326 is the standard GPS coordinate system.'),
 ('GiST index', 'A spatial index that makes &ldquo;within N metres&rdquo; fast without checking every row.'),
 ('Primary key / foreign key', 'The column that identifies a row / a column that points to another table&rsquo;s primary key.'),
 ('Junction table', 'Turns a many-to-many link into two one-to-many links and stores the order (<code>itinerary_stops</code>).'),
 ('Migration', 'A numbered SQL file that changes the database structure.'),
 ('RLS', 'Row Level Security: database rules about which rows a user may see.'),
 ('SAMPLE data', 'Real OSM place names with invented ratings and tags, marked so nobody mistakes them for real.'),
])
w2_boss = ''.join([
 qa('Why does the project need 55 SAMPLE places?',
  '<p>OSM has <b>no ratings</b> (0%), and the hidden gem rule needs a rating and a review count. The SAMPLE rows give the rule something to run on so the whole pipeline can be tested. Real Google ratings for those 55 are planned (step 2.9a).</p>', 1),
 qa('Why is the road network a file and not in Supabase?',
  '<p>The route planner reads the whole network on every request. Memory is much faster than querying the database each time, and it loads only once (about 0.2 s).</p>', 2),
 qa('Why is there no foreign key to the Supabase auth table?',
  '<p>So the same migrations also run on a plain PostgreSQL test database. The profile id simply equals the Supabase Auth user id.</p>', 3),
 qa('How is the database kept safe?',
  '<p>RLS on every table, public write rights revoked (migration 004), parameterised SQL, no <code>service_role</code> key in the app, secrets only in a <code>.env</code> file that is never committed.</p>', 4),
 qa('Why only 2.3% halal?',
  '<p>OSM volunteers rarely tag halal. The app should show &ldquo;halal unknown&rdquo; honestly; better sources (Google data, manual checks, user reports) are planned.</p>', 5),
])

# ---------------------------------------------------------------- topic 3
w3_vis = f'''{NOTE}
  <h3>The idea</h3>
  <p class="small">A hidden gem is &ldquo;well liked, but not many people know it yet&rdquo;, so it needs a <b>high rating</b> and <b>few reviews</b>.</p>
  {d_gem}
  <div class="tbl-wrap"><table><thead><tr><th>Label</th><th>Rule (defaults; set in config)</th></tr></thead><tbody>
  <tr><th>Hidden Gem</th><td>rating &ge; 4.3 and 1 to 100 reviews</td></tr><tr><th>Popular</th><td>more than 100 reviews, whatever the rating</td></tr>
  <tr><th>No label</th><td>no rating, 0 reviews, or few reviews with a lower rating</td></tr></tbody></table></div>
  <p class="small">In code this is <code>labelHiddenGem()</code>, a <b>pure function</b> (same input, same output, no database), so it is easy to unit test. The thresholds come from settings (<code>HIDDEN_GEM_MIN_RATING</code>, <code>HIDDEN_GEM_MAX_REVIEWS</code>, <code>POPULAR_MIN_REVIEWS</code>). Why 4.3 and 100? They are starting values: 4.3 is clearly above average on most review sites and 100 reviews separates &ldquo;known locally&rdquo; from &ldquo;famous&rdquo;. Real Google data will show where they should sit.</p>
  <h3>Ranking</h3>
  <ol class="five"><li>Hidden Gems first, then Popular, then unlabelled.</li><li>Inside each group, nearest first.</li><li>A higher rating breaks ties.</li></ol>
  <h3>Result on the 55 sample places</h3>
  <p class="small">14 Hidden Gems, 35 Popular, 6 with no label. <i>(My own check: 14 + 35 + 6 = 55.)</i> Sensitivity test of the thresholds (number of gems):</p>
  <div class="tbl-wrap"><table><thead><tr><th>Minimum rating</th><th>reviews &le; 50</th><th>reviews &le; 100</th><th>reviews &le; 200</th></tr></thead><tbody>
  <tr><th>4.0</th><td>6</td><td>16</td><td>16</td></tr><tr><th>4.3 (default)</th><td>6</td><td><b>14</b></td><td>14</td></tr><tr><th>4.5</th><td>4</td><td>7</td><td>7</td></tr></tbody></table></div>
  <p class="small">The &le; 100 and &le; 200 columns match because no sample place has 101 to 200 reviews. That is a gap in the sample data that real data should fill.</p>
  <h3>Searching</h3>
  <p class="small"><code>GET /api/discovery/places</code> takes <code>lat</code>, <code>lng</code>, <code>radius</code> (100 to 5,000 m, default 1,500), <code>halal</code>, <code>maxPrice</code> (1 to 4), <code>cuisine</code>, <code>dietary</code>, <code>openNow</code>, <code>label</code> and <code>limit</code> (1 to 100, default 50). PostGIS <code>ST_DWithin</code> finds places inside the radius, using a GiST index. Halal keeps only places marked halal; <code>maxPrice</code> means price level at most n; cuisine matches any of the given words (with <code>%</code> and <code>_</code> escaped); dietary needs all the given tags. <code>openNow</code> and <code>label</code> are applied in JavaScript afterwards. The reply carries a <code>note</code> when sample data is present.</p>
  <h3>&ldquo;Open now&rdquo;</h3>
  <ul class="chips-row"><li>Hours are stored as JSON per day, e.g. morning and evening ranges</li><li>Checked in Malaysian time</li><li>Ranges past midnight work (18:00 to 02:00)</li><li>A closing time of 23:59 counts as 24:00</li><li>No structured hours = counted as not open</li></ul>
  <h3>Worked example: Komtar, 1.5 km</h3>
  <p class="small">704 places found: 7 Hidden Gems, 19 Popular, 678 with no label. The top five are all gems, nearest first: Sister Yao&rsquo;s Char Koay Kak (275 m), Muscle Man Char Koay Kak (394 m), VR Pinxin Vegan (489 m), Hot Bowl White Curry Mee (649 m), Tok Tok Mee Bamboo Noodles (736 m). With halal only: 17 places (2 gems, 4 Popular, 11 none). <i>(Most of the 704 are plain OSM rows with no rating, which is why so few get a label.)</i></p>
'''
w3_terms = terms([
 ('Hidden gem', 'Rating at least 4.3 and 1 to 100 reviews (defaults).'),
 ('Popular', 'More than 100 reviews.'),
 ('Pure function', 'Same input always gives the same output, with no side effects; easy to test.'),
 ('ST_DWithin', 'The PostGIS test &ldquo;is this point within N metres of that point?&rdquo;'),
 ('Sensitivity test', 'Change a threshold and see how the result changes, to check the rule is not fragile.'),
 ('Parameterised query', 'SQL with placeholders (<code>$1, $2</code>) so user input cannot change the query.'),
])
w3_boss = ''.join([
 qa('State the hidden gem rule and how places are ranked.',
  '<p>Gem: rating &ge; 4.3 and 1 to 100 reviews. Popular: over 100 reviews. Otherwise no label. Rank gems first, then Popular, then none; nearest first inside each group; higher rating breaks ties.</p>', 1),
 qa('Why those thresholds?',
  '<p>They are reasonable starting values (4.3 is clearly above average; 100 reviews separates known locally from famous) and they are settings. The sensitivity table shows the effect of changing them, and real Google data will show where they should sit.</p>', 2),
 qa('Why do the &le; 100 and &le; 200 columns match in the sensitivity table?',
  '<p>No sample place has between 101 and 200 reviews. It is a limit of the sample data, not of the rule.</p>', 3),
 qa('Why does Komtar show only 7 gems among 704 places?',
  '<p>My reading: most of the 704 are OSM rows with no rating, and a place with no rating gets no label. Only the sample places can be labelled for now.</p>', 4),
 qa('Why are places with no opening hours not &ldquo;open now&rdquo;?',
  '<p>The app cannot promise they are open, so it does not claim it. The raw OSM text is kept but not used by the filter.</p>', 5),
])

# ---------------------------------------------------------------- topic 4
w4_vis = f'''{NOTE}
  <h3>Four steps, in order: graph, snap, Dijkstra, ACO</h3>
  {d_route}
  <p class="small"><code>POST /api/hopping/route</code> takes 2 to 10 unique place ids, a travel mode (walking or driving, default walking), an optional start place and an optional seed. It returns the visiting order, the legs (time, distance and the road path to draw), the totals, a comparison of three methods and the algorithm settings.</p>
  <h3>1. The road graph</h3>
  <p class="small">A <b>graph</b> is nodes joined by edges. Here a node is a junction or road end and an edge is a piece of road with a length and a travel time. It is built from OSM by <code>build-road-graph.js</code> (26,689 nodes, 34,732 edges); 99% of usable walking nodes sit in one connected part (26,208 of 26,478), and 97.7% for driving (22,918 of 23,448). <b>Walking</b> is 1.4 m/s and allowed both ways on one-way streets. <b>Driving</b> speed depends on road type (for example residential 20 km/h, primary 40, motorway 70) and respects one-way streets. These speeds are <b>assumptions</b>, not measurements.</p>
  <h3>2. Snapping</h3>
  <p class="small">A place is not exactly on a road node, so it is <b>snapped</b> to the nearest node in the main connected part (so it never lands on an isolated piece such as a car park). A grid of about 220 m squares keeps the search fast; a place more than 1 km from any road cannot be routed (error 422 <code>PLACE_NOT_ON_ROAD_GRAPH</code>). If the road file is missing, a fallback links each place to its 4 nearest places with straight-line distance &times; 1.3.</p>
  <h3>3. Dijkstra&rsquo;s algorithm</h3>
  <p class="small">Finds the quickest path from one node to all others when no edge is negative. Keep a frontier ordered by best known time; always settle the closest unsettled node; <b>relax</b> its edges (&ldquo;is going through here quicker?&rdquo;). Because times are never negative, a settled node&rsquo;s time is final. The code uses a binary min-heap (priority queue), cost <b>O((V + E) log V)</b>, and stops early once all wanted stops are settled. It runs <b>once per stop</b> to build the <b>time matrix</b>: the walking time between every pair (10 &times; 10 for 10 stops, about 46 ms). If any pair is unreachable the API answers 422 <code>ROUTE_UNREACHABLE</code>.</p>
  <h3>4. The visiting order: a small TSP</h3>
  <p class="small">Given the time matrix, which order has the smallest total time? That is the <b>Travelling Salesman Problem</b>, NP-hard. Routes here are <b>open</b> (start at the first or chosen stop, visit each once, do not return). With a fixed start there are <b>(n &minus; 1)!</b> orders:</p>
  <div class="tbl-wrap"><table><thead><tr><th>Stops</th><th>8</th><th>10</th><th>13</th><th>15</th></tr></thead><tbody><tr><th>Orders</th><td>7! = 5,040</td><td>9! = 362,880</td><td>12! = 479,001,600</td><td>14! &approx; 87 billion</td></tr></tbody></table></div>
  <div class="tbl-wrap"><table><thead><tr><th>Method</th><th>How</th><th>Good</th><th>Bad</th></tr></thead><tbody>
  <tr><th>Brute force (with pruning)</th><td>Try every order; drop a branch once it is already slower than the best</td><td>Always optimal: the ground truth</td><td>Grows as (n&minus;1)!; the API limits it to 8 stops</td></tr>
  <tr><th>Nearest neighbour</th><td>Always go to the closest unvisited stop (greedy)</td><td>Very fast (about 0.01 ms)</td><td>About 9% longer at 8 to 10 stops</td></tr>
  <tr><th>Ant Colony Optimisation</th><td>Simulated ants build orders guided by pheromone and closeness</td><td>Near-optimal; cost grows only polynomially</td><td>A heuristic: usually, not always, optimal</td></tr></tbody></table></div>
  <h3>Ant Colony Optimisation, round by round</h3>
  <p class="small">Real ants find short paths by leaving <b>pheromone</b>; shorter paths get walked more and collect more. Simple agents together find a good answer: <b>swarm intelligence</b>.</p>
  {d_aco}
  <ol class="five">
   <li><b>Build orders.</b> Each ant builds a full order from the start. At each step it picks the next unvisited stop <i>at random</i> with weight <b>pheromone<sup>&alpha;</sup> &times; (1/time)<sup>&beta;</sup></b> (roulette-wheel selection). &alpha; = 1 weighs experience; &beta; = 2 weighs closeness.</li>
   <li><b>Evaporate.</b> Every trail times (1 &minus; &rho;), &rho; = 0.5, so old information fades.</li>
   <li><b>Deposit.</b> Each ant adds q / L on every move of its order (L = its total time, q = 1), so shorter orders add more. <b>Elitist:</b> the best order so far gets an extra deposit.</li>
   <li><b>Trail limits (MAX-MIN).</b> Pheromone stays between &tau;min and &tau;max (&tau;min = 0.2 &times; &tau;max), where &tau;max = (ants + 1) q / (&rho; &times; best time). No move becomes impossible, which avoids stagnation (all ants copying the first good order).</li></ol>
  <div class="tbl-wrap"><table><thead><tr><th>Setting</th><th>Default</th></tr></thead><tbody>
  <tr><th>Iterations / early stop</th><td>200 / after 100 rounds with no improvement</td></tr><tr><th>Ants</th><td>max(10, 2 &times; stops)</td></tr>
  <tr><th>Start pheromone &tau;0</th><td>ants &times; q / (length of the nearest-neighbour order)</td></tr><tr><th>Random numbers</th><td>seeded (mulberry32, seed 42), so a route is repeatable</td></tr>
  <tr><th>Cost</th><td>about iterations &times; ants &times; n&sup2;: polynomial, not factorial</td></tr></tbody></table></div>
  <h3>&ldquo;Improved&rdquo; vs &ldquo;textbook&rdquo; ACO</h3>
  <p class="small"><b>Textbook</b> = the original Ant System (Dorigo, Maniezzo and Colorni, 1996) with &beta; = 3, no elitist deposit, no trail limits. <b>Improved</b> adds the elitist deposit (from the Elitist Ant System), MAX-MIN trail limits (from the MAX-MIN Ant System, St&uuml;tzle and Hoos) and &beta; = 2. Both are kept in the code so the comparison can be reproduced.</p>
'''
w4_terms = terms([
 ('Graph, node, edge', 'Points joined by connections; here junctions and road pieces.'),
 ('Snapping', 'Matching a place to its nearest road node.'),
 ('Dijkstra&rsquo;s algorithm', 'Quickest path from one node to all others when no edge is negative.'),
 ('Priority queue / min-heap', 'Always gives back the smallest item fast; used to pick the next node.'),
 ('Time matrix', 'A table of travel times between every pair of chosen stops.'),
 ('TSP, open TSP', 'Find the shortest order to visit all points. Open: no return to the start.'),
 ('NP-hard', 'No known fast exact method for large inputs.'),
 ('Heuristic / metaheuristic', 'A method that usually finds a good answer without a guarantee / a general search strategy such as ACO.'),
 ('Pheromone (&tau;), heuristic (&eta; = 1/time)', 'Learned value of a move / how attractive a closer stop is.'),
 ('&alpha;, &beta;, &rho;', 'Weight of pheromone, weight of closeness, evaporation rate.'),
 ('Elitist deposit', 'Extra pheromone on the best order found so far.'),
 ('MAX-MIN limits', 'Keep pheromone between a minimum and a maximum to avoid stagnation.'),
 ('Seed', 'A starting number that makes &ldquo;random&rdquo; results repeatable.'),
])
w4_boss = ''.join([
 qa('What is Dijkstra used for here, and why not straight-line distance?',
  '<p>To get the walking time between every pair of chosen places along real roads (the time matrix). Roads are not straight, so road times give realistic routes. Straight line &times; 1.3 is only the fallback when the road file is missing.</p>', 1),
 qa('Explain one round of ACO.',
  '<p>Ants build orders using pheromone and closeness; every trail evaporates by (1 &minus; &rho;); each ant deposits q/L on its moves and the best-so-far order gets an extra deposit; then pheromone is clamped between &tau;min and &tau;max. Repeat up to 200 times, or stop after 100 rounds without improvement.</p>', 2),
 qa('What do &alpha;, &beta; and &rho; do?',
  '<p>&alpha; = how much pheromone (experience) counts. &beta; = how much closeness counts. &rho; = how fast pheromone evaporates, so old choices fade.</p>', 3),
 qa('Why open routes?',
  '<p>Food hopping usually ends at the last stop; people do not need to walk back. A round trip could be added as an option.</p>', 4),
 qa('Why use a fixed seed?',
  '<p>The same input then gives the same route, which makes tests and the demo repeatable. Several seeds are planned for the larger evaluation.</p>', 5),
 qa('Give the time complexity of each method.',
  '<p>Dijkstra with a heap: O((V + E) log V) per stop. ACO: about O(iterations &times; ants &times; n&sup2;). Brute force: O((n &minus; 1)!).</p>', 6),
 qa('Work out how many orders 6 stops have if the start is fixed. <i>(my own sum)</i>',
  '<p>(6 &minus; 1)! = 5! = 5 &times; 4 &times; 3 &times; 2 &times; 1 = <b>120</b>.</p>', 7),
])

# ---------------------------------------------------------------- topic 5
w5_vis = f'''{NOTE}
  <h3>The question</h3>
  <p class="small">The supervisor asked whether the proposed work is feasible. The answer in the report: <b>yes</b>. All four modules run end to end, and two gaps remain: real ratings and real user accounts. The report&rsquo;s numbers can be regenerated with <code>npm run feasibility</code> (seeded, so the same each run).</p>
  <h3>Method</h3>
  <ul class="chips-row"><li>Walking mode</li><li>4, 6, 8 and 10 stops</li><li>10 random trips per size</li><li>Pool of 42 sample places (George Town, Pulau Tikus, Jelutong, Gurney)</li><li>Trips seeded 2026 + n; ACO seed 42</li><li>Brute force = the optimum (raised to 10 stops for this study)</li></ul>
  <p class="small"><b>Optimality gap</b> = (method &minus; optimum) / optimum &times; 100. <b>Opt%</b> = share of trips where the method found the optimum. One run on 5 Nov 2026 took 2.1 s.</p>
  <h3>Results</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Stops</th><th>Optimum (avg)</th><th>Improved ACO</th><th>Textbook ACO</th><th>Nearest neighbour</th></tr></thead><tbody>
  <tr><th>4</th><td>22.5 min</td><td>100% optimal</td><td>100%</td><td>90%, avg gap 1.04%</td></tr>
  <tr><th>6</th><td>30.1 min</td><td>100%</td><td>100%</td><td>70%, 1.52%</td></tr>
  <tr><th>8</th><td>50.6 min</td><td>100%, gap 0</td><td>60%, avg 0.65%, max 2.67%</td><td>10%, 9.21%</td></tr>
  <tr><th>10</th><td>62.6 min</td><td>90%, avg 0.2%, max 2.03%</td><td>70%, avg 1.0%, max 4.48%</td><td>20%, 9.14%</td></tr></tbody></table></div>
  {d_bars}
  <p class="small">Overall, improved ACO found the exact optimum in <b>39 of 40 trips</b> (97.5%), and 19 of 20 at 8 to 10 stops, where nearest neighbour managed 3 of 20. The one miss was a 10-stop trip, 2.03% longer. <i>(My own check: 10+10+10+9 = 39; the bar chart above is my redraw of the table.)</i></p>
  <h3>Speed</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Stops</th><th>4</th><th>6</th><th>8</th><th>10</th></tr></thead><tbody>
  <tr><th>Dijkstra matrix (avg)</th><td>5.84 ms</td><td>9.91 ms</td><td>18.43 ms</td><td>45.71 ms</td></tr>
  <tr><th>Improved ACO (avg)</th><td>1.74 ms</td><td>1.40 ms</td><td>3.16 ms</td><td>7.26 ms</td></tr></tbody></table></div>
  <p class="small">A 10-stop plan therefore takes about 46 ms + 7 ms, well under 0.1 s.</p>
  <h3>Worked example: a 6-stop George Town walk</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Leg</th><th>Walk</th></tr></thead><tbody>
  <tr><td>Tok Tok Mee &rarr; Tho Yuen Dim Sum</td><td>3.1 min, 257 m</td></tr><tr><td>&rarr; Hameediyah Tandoori House</td><td>1.5 min, 122 m</td></tr><tr><td>&rarr; Toh Soon Cafe</td><td>1.3 min, 110 m</td></tr>
  <tr><td>&rarr; Chulia Street Night Hawker Stalls</td><td>7.2 min, 609 m</td></tr><tr><td>&rarr; Ali Bubur Kacang</td><td>4.8 min, 407 m</td></tr><tr><th>Total</th><th>17.9 min, 1,505 m</th></tr></tbody></table></div>
  <p class="small">Nearest neighbour gave 19.3 min on the same stops, about 8% longer.</p>
  <h3>Be honest about it</h3>
  <ul class="traps"><li>The results are <b>indicative</b>: 10 trips per size and one ACO seed. A larger test (50+ trips, several seeds, 12 to 20 stops, maybe a nearest-neighbour + 2-opt baseline) is planned.</li>
  <li>At 10 stops <b>brute force is faster</b> than ACO (2.9 ms vs 7.26 ms). ACO is justified by <b>scalability</b>: orders grow factorially (479 million at 13 stops, 87 billion at 15) while ACO grows polynomially.</li>
  <li>ACO is a heuristic. It is not always optimal.</li>
  <li>Ratings behind the gem and analytics results are invented sample data.</li></ul>
  <h3>Analytics on the 55 rated sample places</h3>
  <p class="small"><code>GET /api/analytics/overview</code> returns chart data, generated written findings and suggested places. Average rating 4.18; 20 halal places (36%); best areas George Town 4.23 (28 places), Pulau Tikus 4.22 (6), Bayan Lepas 4.18 (4); best cuisine &ldquo;cafe&rdquo; 4.4; gems are 25% of the places. Gems average 4.5 stars from about 66 reviews, Popular places 4.2 from about 1,226. A group needs at least 3 rated places to be ranked, so one lucky place cannot top a list. Suggestions are the top 5 gems by rating, then fewer reviews. These show the pipeline works; they are not claims about Penang food.</p>
'''
w5_terms = terms([
 ('Feasibility study', 'A test of whether the proposed work can really be done, with evidence.'),
 ('Ground truth', 'The known-correct answer used to judge other methods (brute force here).'),
 ('Optimality gap', 'How much longer than the optimum a route is, in percent.'),
 ('Opt%', 'Share of trips where a method found the exact optimum.'),
 ('Indicative', 'Suggestive but not final, because the test is small.'),
 ('Scalability', 'How cost grows as the problem grows: factorial for brute force, polynomial for ACO.'),
 ('2-opt', 'A simple local improvement that swaps pairs of edges; a possible extra baseline.'),
])
w5_boss = ''.join([
 qa('Why use ACO if brute force is faster?',
  '<p>For 10 stops or fewer brute force with pruning is exact and fast (2.9 ms vs 7.26 ms), which is why it is the ground truth. But orders grow factorially (479 million at 13 stops, 87 billion at 15), and pruning does not stop that. ACO grows polynomially, so it scales to longer and multi-day trips. It is also the Intelligent Computing part. Next step: test 12 to 20 stops.</p>', 1),
 qa('How do you know the optimum?',
  '<p>Brute force tries every order, so it is exact. It was used as ground truth up to 10 stops.</p>', 2),
 qa('Is ACO always optimal?',
  '<p>No, it is a heuristic. In the test it found the optimum in 39 of 40 trips; the one miss was 2.03% longer.</p>', 3),
 qa('What is wrong with the evidence so far?',
  '<p>Only 10 trips per size, one ACO seed, up to 10 stops, and ratings are invented. The larger evaluation in Phase 3 is meant to fix the first three.</p>', 4),
 qa('Why is improved ACO better than textbook ACO here?',
  '<p>At 8 stops improved was 100% optimal against 60%; at 10 stops 90% against 70%, with a worst gap of 2.03% against 4.48%. The elitist deposit and MAX-MIN limits help it converge without stagnating. <i>(Small test: indicative only.)</i></p>', 5),
 qa('Calculate the optimality gap if a route takes 19.3 min and the optimum is 17.9 min. <i>(my own sum)</i>',
  '<p>(19.3 &minus; 17.9) / 17.9 &times; 100 = 1.4 / 17.9 &times; 100 &approx; <b>7.8%</b>, which the report rounds to about 8%.</p>', 6),
])

# ---------------------------------------------------------------- topic 6
w6_vis = f'''{NOTE}
  <h3>Three layers</h3>
  {d_layers}
  <p class="small">The apps never talk to the database. Only the backend does. That keeps database passwords off the user&rsquo;s device, keeps all rules in one place, and lets web and mobile share one API.</p>
  <h3>What happens when a user plans a trip</h3>
  <ol class="five"><li>The web app calls the search endpoint with a location and radius.</li><li>The backend runs the PostGIS query, applies the hidden gem rule and ranks the places.</li><li>The web app shows the list and a Leaflet map with labels.</li><li>The user adds 2 to 10 places and presses <b>Plan route</b>.</li><li>The backend loads the places, snaps them, runs Dijkstra for the time matrix, runs ACO (plus nearest neighbour and brute force for comparison), and builds the legs.</li><li>The web app draws the route and shows minutes, metres and the comparison card.</li></ol>
  <h3>Inside the backend</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Part</th><th>Job</th></tr></thead><tbody>
  <tr><th>routes</th><td>The URLs, and the zod input rules for each</td></tr><tr><th>controller</th><td>Reads the request, sends the reply</td></tr><tr><th>service</th><td>The actual logic</td></tr><tr><th>model</th><td>The SQL (parameterised)</td></tr></tbody></table></div>
  <p class="small">Each module folder (food-discovery, food-hopping, food-stalls-analytics) has these four files; user-management is empty until Phase 2B. Shared parts: <code>app.js</code> builds the Express app (tests use it), <code>index.js</code> is the only file that starts the server, <code>config/</code> reads and checks settings (when <code>NODE_ENV=test</code> it ignores <code>.env</code>), <code>lib/</code> holds the database pool and the reply helpers, and <code>middleware/</code> holds validation and error handling.</p>
  <h3>API rules</h3>
  <ul class="chips-row"><li>REST: URLs are resources, the method says what to do</li><li>JSON everywhere</li><li>Success: <code>{{success:true, data}}</code></li><li>Failure: <code>{{success:false, error:{{code, message, details}}}}</code></li><li>Bad input: 400 <code>VALIDATION_ERROR</code></li><li>Unexpected: 500 <code>INTERNAL_ERROR</code> with no stack trace or SQL</li><li>Body limit 100 KB</li></ul>
  <div class="tbl-wrap"><table><thead><tr><th>Endpoint</th><th>Submodule</th><th>Does</th></tr></thead><tbody>
  <tr><td><code>GET /health</code>, <code>/health/db</code></td><td>(checks)</td><td>Is the server up? Can it reach the database?</td></tr>
  <tr><td><code>GET /api/discovery/places</code></td><td>Searching + Hidden Gem Highlighting</td><td>Search, filter, label, rank</td></tr>
  <tr><td><code>GET /api/discovery/places/:id</code></td><td>Food Place Visualisation</td><td>One place&rsquo;s details</td></tr>
  <tr><td><code>POST /api/hopping/route</code></td><td>Route Planner</td><td>Best order and route</td></tr>
  <tr><td><code>GET /api/analytics/overview</code></td><td>Analytics (three submodules)</td><td>Charts, findings, suggestions</td></tr></tbody></table></div>
  <p class="small"><b>Planned (Phase 2B):</b> <code>/api/auth/register</code>, <code>/login</code>, <code>/refresh</code>, profile and preferences, and itinerary save, edit and list. The user will get a <b>JWT</b> (a signed token) sent with each request, and an auth middleware will check it. Supabase Auth hashes passwords, so even the team cannot read them.</p>
  <h3>The web app</h3>
  <p class="small">Pages: Landing, Discover, Trip, My Trips, Analytics, Login, Register, Profile, loaded lazily. A trip basket (context plus localStorage, max 10 stops) holds the chosen places; the route goes stale when stops, order or travel mode change. An <b>algorithm comparison card</b> shows ACO, nearest neighbour and brute force. Leaflet draws the map (OSM tiles, no key), Recharts the charts. Until Phase 2B, login, registration, profile and saved trips (max 50) live in browser localStorage and the password is only length-checked: <b>demo mode</b>. Sample data is labelled in the app.</p>
  <h3>Security: what is done</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Risk</th><th>What the project does</th></tr></thead><tbody>
  <tr><td>Secrets leaking</td><td><code>.env</code> never committed; the example file holds placeholders</td></tr><tr><td>SQL injection</td><td>Parameterised queries only</td></tr>
  <tr><td>Bad input</td><td>zod check on every request; body size limit</td></tr><tr><td>Leaking internals</td><td>Error handler hides stack traces and SQL</td></tr>
  <tr><td>Public database access</td><td>RLS on every table; migration 004</td></tr><tr><td>Browser attacks</td><td>helmet headers; CORS allows only the web app&rsquo;s address</td></tr>
  <tr><td>Powerful keys</td><td>No Supabase <code>service_role</code> key in the app</td></tr></tbody></table></div>
  <p class="small">Planned in Phase 3: login rate limiting, <code>npm audit</code>, a full security review.</p>
  <h3>Testing</h3>
  <p class="small">Unit tests check one function alone (the gem rule, Dijkstra on a small hand-drawn graph with known answers, ACO against brute force on small cases). API tests (Supertest) call endpoints, including bad input. Tests need no database, internet or secrets: the database is a mock. The study guide states <b>277 backend tests (Jest) and 93 web tests (Vitest)</b>; this page copies that figure from <code>docs/module-status.md</code> and has not re-run them. ESLint and Prettier handle style. CI with GitHub Actions is planned for Phase 3.</p>
'''
w6_terms = terms([
 ('Layered design', 'Each file has one job: routes, controller, service, model.'),
 ('REST / JSON', 'URLs as resources with GET/POST actions / the text format data travels in.'),
 ('zod', 'The library that checks request input against rules.'),
 ('AppError', 'The error type for expected problems, turned into a clean JSON reply.'),
 ('Middleware', 'Code that runs before or after each request (validation, errors, auth).'),
 ('helmet / CORS', 'Safe HTTP headers / browser rules about which sites may call the API.'),
 ('JWT', 'A signed token that proves who the user is after login (planned).'),
 ('Mock', 'A fake stand-in (for example for the database) used in tests.'),
 ('CI', 'Automatic lint and tests on every push (GitHub Actions, planned).'),
 ('localStorage', 'Browser storage, used for demo-mode data.'),
])
w6_boss = ''.join([
 qa('Why a backend at all? Why not call Supabase from the app?',
  '<p>To keep secrets off the device, keep all rules and algorithms in one place, and let web and mobile share one API.</p>', 1),
 qa('Walk through the four files of a backend module.',
  '<p>Routes: URLs and input rules. Controller: reads the request, sends the reply. Service: the logic. Model: the parameterised SQL.</p>', 2),
 qa('What does every API reply look like?',
  '<p>Success: <code>{success:true, data}</code>. Failure: <code>{success:false, error:{code, message, details}}</code>. Bad input gives 400, anything unexpected 500 with no internals shown.</p>', 3),
 qa('What is demo mode and when does it end?',
  '<p>Login, registration, profile and saved trips work on screen but live in the browser, and the password is only length-checked. It ends in Phase 2B, when Supabase Auth and the itinerary API are built.</p>', 4),
 qa('How do you test it without a database?',
  '<p>The database is replaced by a mock, so tests need no internet or secrets. Brute force checks ACO on small cases, and results are seeded so they repeat.</p>', 5),
 qa('List the security measures already in place.',
  '<p>Parameterised SQL, zod validation, hidden error details, RLS plus revoked public rights, helmet and CORS, no <code>service_role</code> key, secrets only in <code>.env</code>.</p>', 6),
])

# ====================================================================== story, status, meeting, cheat sheet, flashcards
story = [
 (1, 'The idea and the plan', 'Tourists find only the famous places, and ordering several stops well is hard.',
  'A food hopping planner with four modules that labels hidden gems and plans the route, built in phases.',
  'A hidden gem needs ratings. Where does the data come from?'),
 (2, 'The data', 'The planner needs places, ratings and roads.',
  'OpenStreetMap for places and roads in Supabase and a graph file, plus 55 SAMPLE places with invented ratings.',
  'Now the data exists. How do we decide which places are gems, and let users find them?'),
 (3, 'Hidden gems and search', 'A user wants well rated places nearby, not just famous ones.',
  'A radius search with filters, and a simple rule: rating 4.3 or more with 1 to 100 reviews.',
  'The user picks several places. In what order should they walk?'),
 (4, 'The route planner', 'Visiting n places has (n-1)! possible orders, and we need real walking times.',
  'Road graph, snapping, Dijkstra for times, and Ant Colony Optimisation for the order.',
  'Does it actually work, and is ACO any good?'),
 (5, 'The proof', 'The supervisor asked whether the proposed work is feasible.',
  'A seeded study: ACO found the optimum in 39 of 40 trips; nearest neighbour is about 9% longer.',
  'All of this has to live in an app other people can use, safely.'),
 (6, 'The application', 'Algorithms need an API, a web app, security and tests.',
  'Three layers, four-file modules, a React web app, RLS and zod, and automated tests.',
  'What is still missing: real ratings, real accounts, a bigger test and the mobile app (see Status).'),
]
story_html = '<ol class="story">' + ''.join(
    f'<li class="w{n}"><a href="#week-{n}"><span class="wk">Topic {n}</span><h3>{t}</h3>'
    f'<p><b>Problem</b>{p}</p><p><b>Fix</b>{s}</p><p class="but"><b>But then</b>{b}</p></a></li>' for n, t, p, s, b in story) + '</ol>'

numbers = [('4 / 13', 'modules / submodules'), ('7 / 6', 'submodules built / partial'), ('1,241', 'places in the database (1,186 OSM + 55 SAMPLE)'),
           ('1,298 to 1,241', 'raw OSM elements to named and imported (95.6%)'), ('26,689 / 34,732', 'road nodes / edges'), ('99%', 'walking nodes in the main connected part'),
           ('6', 'database tables'), ('0% / 2.3% / 23.2% / 45.4%', 'OSM places with rating / halal / opening hours / cuisine'),
           ('4.3 and 1 to 100', 'hidden gem: minimum rating and review range'), ('14 / 35 / 6', 'Hidden Gem / Popular / no label on the 55 samples'),
           ('704', 'places within 1.5 km of Komtar'), ('39 of 40', 'trips where improved ACO found the optimum (97.5%)'), ('2.03%', 'worst ACO gap, one 10-stop trip'),
           ('about 9%', 'how much longer nearest neighbour is at 8 to 10 stops'), ('46 ms + 7 ms', 'Dijkstra + ACO for 10 stops'),
           ('17.9 min, 1,505 m', 'the 6-stop demo route (nearest neighbour 19.3 min)'), ('1.4 m/s', 'walking speed (about 5 km/h)'),
           ('200 / 100 / 42', 'ACO max iterations / early-stop rounds / seed'), ('alpha 1, beta 2, rho 0.5', 'ACO weights and evaporation'),
           ('2 to 10', 'stops per route; brute force up to 8 in the API'), ('100 to 5,000 m', 'search radius range (default 1,500)'),
           ('277 / 93', 'backend / web tests (as stated in the module-status file)')]
numbers_html = '<ul class="nums">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in numbers) + '</ul>'
traps = [
 'Do <b>not</b> say the ratings or analytics findings are real: they are invented SAMPLE data.',
 'Do <b>not</b> say login or saved trips work on the server yet: they are demo mode until Phase 2B.',
 'Do <b>not</b> say ACO is always optimal: it is a heuristic (39 of 40 in a small test).',
 'Do <b>not</b> say ACO is faster than brute force at 10 stops. It is not. The case for ACO is <b>scalability</b>.',
 'Do <b>not</b> say walking times are exact: the speeds are assumptions.',
 'Do <b>not</b> say the benchmark is final: it is indicative.',
 'The mobile app is <b>planned</b>, not started.',
 'Filtering is <b>not</b> a module.',
 'If you do not know an answer, the study guide suggests: &ldquo;I have not tested that yet; I will check and add it to the next report.&rdquo;',
]
traps_html = '<ul class="traps">' + ''.join(f'<li>{t}</li>' for t in traps) + '</ul>'
cards = [
 ('What is MyMakanRoute?', 'A food hopping and discovery planner for Penang that labels hidden gems and plans the shortest walking route between chosen places.'),
 ('The four modules', 'User Management, Food Discovery, Food Hopping, Food Stalls Analytics (13 submodules).'),
 ('Built vs partial submodules', '7 built (API, web page, tests); 6 partial (demo mode or browser only).'),
 ('Three layers', 'Presentation (web, mobile), application (Express API), data (Supabase PostgreSQL + PostGIS).'),
 ('Where do places come from?', 'OpenStreetMap through the Overpass API; 1,241 imported; 55 are SAMPLE with invented values.'),
 ('Key finding about OSM', 'Good for where, weak on what: 0% ratings, 2.3% halal, 23.2% hours, 45.4% cuisine.'),
 ('Why is the road graph a file?', 'It is read on every route request; memory is faster than the database. Loads once in about 0.2 s.'),
 ('Road graph size', '26,689 nodes and 34,732 edges; 99% of walking nodes in the main component.'),
 ('What is RLS?', 'Row Level Security: database rules about which rows a user may see. On for every table.'),
 ('Hidden gem rule', 'Rating at least 4.3 and 1 to 100 reviews. Popular: over 100 reviews.'),
 ('Ranking order', 'Gems, then Popular, then none; nearest first in a group; higher rating breaks ties.'),
 ('Labels on the 55 samples', '14 Hidden Gems, 35 Popular, 6 no label.'),
 ('Search radius', '100 to 5,000 m, default 1,500, using PostGIS ST_DWithin and a GiST index.'),
 ('Open now rule', 'Malaysian time, past-midnight ranges handled, no structured hours counts as not open.'),
 ('Snapping', 'A place is matched to its nearest road node in the main component; over 1 km cannot be routed.'),
 ('Dijkstra in one line', 'Quickest path from a node, settling the closest node each time; with a heap, O((V+E) log V).'),
 ('Time matrix', 'Walking time between every pair of stops, one Dijkstra run per stop.'),
 ('Open TSP', 'Find the best order to visit all stops without returning to the start; (n-1)! orders.'),
 ('Brute force vs NN vs ACO', 'Exact but factorial / fast greedy, about 9% longer / near-optimal heuristic, polynomial.'),
 ('One ACO round', 'Build orders, evaporate, deposit (plus elitist), apply MAX-MIN limits.'),
 ('ACO settings', 'alpha 1, beta 2, rho 0.5, 200 iterations, stop after 100 without gain, seed 42.'),
 ('Improved vs textbook ACO', 'Improved adds elitist deposit, MAX-MIN limits and beta 2; textbook is the plain Ant System with beta 3.'),
 ('Feasibility result', 'Improved ACO optimal in 39 of 40 trips; worst gap 2.03%; NN about 9% longer at 8 to 10 stops.'),
 ('Why ACO if brute force is faster?', 'Orders grow factorially (479 million at 13 stops); ACO grows polynomially. It is the intelligent computing part.'),
 ('Biggest gap in the evidence', 'Only 10 trips per size and one seed; sample ratings are invented. Larger test planned.'),
 ('API reply shape', 'Success: {success:true, data}. Failure: {success:false, error:{code, message, details}}.'),
 ('Four backend files per module', 'routes, controller, service, model.'),
 ('Demo mode', 'Fake login and browser-only trips until Phase 2B adds Supabase Auth and the itinerary API.'),
 ('Biggest risk', 'Real ratings: the hidden gem idea depends on them and OSM has none.'),
]
cards_html = '<div class="cards" id="cards">' + ''.join(
    f'<button class="card" type="button" aria-pressed="false"><span class="front">{q}</span><span class="back">{a}</span></button>' for q, a in cards) + '</div>'
N_CARDS = len(cards)

weeks_html = ''.join([
 week(1, '', 'The idea and the plan', 'What MyMakanRoute is, its four modules, the phases and the way of working.',
      psn('Tourists find only the famous places, and ordering several stops well is hard.',
          'A food hopping planner in four modules that labels hidden gems and plans the route, built phase by phase.',
          'A hidden gem needs ratings. Where does the data come from?'), MAPS[1], w1_vis, w1_terms, w1_boss),
 week(2, '', 'The data', 'OpenStreetMap, the SAMPLE places, the database and the road graph.',
      psn('The planner needs places, ratings and roads.',
          'OSM for places and roads (Supabase plus a graph file) and 55 SAMPLE places with invented ratings.',
          'How do we decide which places are gems, and let users find them?'), MAPS[2], w2_vis, w2_terms, w2_boss),
 week(3, '', 'Hidden gems and search', 'The hidden gem rule, ranking, filters and the search endpoint.',
      psn('A user wants well rated places nearby, not just famous ones.',
          'Radius search with filters, plus rating 4.3 or more with 1 to 100 reviews as the gem rule.',
          'The user picks several places. In what order should they walk?'), MAPS[3], w3_vis, w3_terms, w3_boss),
 week(4, '', 'The route planner', 'Road graph, snapping, Dijkstra and three ways to choose the order.',
      psn('Visiting n places has (n-1)! possible orders and we need real walking times.',
          'Snap places to the road graph, use Dijkstra for times and Ant Colony Optimisation for the order.',
          'Does it actually work, and is ACO any good?'), MAPS[4], w4_vis, w4_terms, w4_boss),
 week(5, '', 'The proof', 'The feasibility study: method, results and honest limits.',
      psn('The supervisor asked whether the proposed work is feasible.',
          'A seeded study: improved ACO found the optimum in 39 of 40 trips; nearest neighbour was about 9% longer.',
          'All of this has to live in an app that people can use, safely.'), MAPS[5], w5_vis, w5_terms, w5_boss),
 week(6, '', 'The application', 'Layers, backend structure, API rules, the web app, security and tests.',
      psn('Algorithms need an API, a web app, security and tests around them.',
          'Three layers, four-file modules, a React web app, RLS and zod, and automated tests.',
          'Real ratings, real accounts, a bigger test and the mobile app are still missing.'), MAPS[6], w6_vis, w6_terms, w6_boss),
])

status_html = '''
<section id="status" class="band wx">
  <h2 class="sec">Status, risks and next steps</h2>
  <p class="small">As of 5 Nov 2026, from the project&rsquo;s own module-status and feasibility files.</p>
  <h3>Limitations (say them before they are found)</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Limitation</th><th>Effect</th><th>Plan</th></tr></thead><tbody>
  <tr><td>Sample ratings are invented</td><td>Gem and analytics results show the method only</td><td>Google ratings for the 55 (step 2.9a); user ratings later</td></tr>
  <tr><td>Halal tags in OSM: 2.3%</td><td>The halal filter misses untagged places</td><td>Google data, manual checks, user reports; show &ldquo;halal unknown&rdquo;</td></tr>
  <tr><td>Demo-mode login; trips in the browser</td><td>No real accounts; trips lost if browser data is cleared</td><td>Supabase Auth and the itinerary API (2B)</td></tr>
  <tr><td>Fixed walking speed, assumed driving speeds</td><td>Times are estimates</td><td>Say so in the app; compare a few legs with a map service</td></tr>
  <tr><td>Snapping to the nearest node</td><td>Small error at each end of a leg</td><td>Report snap distance (already in the API); snap to segments later</td></tr>
  <tr><td>Small benchmark</td><td>10 trips per size, one seed</td><td>50+ trips, several seeds, 12 to 20 stops (Phase 3)</td></tr>
  <tr><td>Supabase free tier pauses when idle</td><td>The demo could fail</td><td>Open the dashboard before demos</td></tr>
  <tr><td>No CI yet</td><td>Mistakes caught later</td><td>GitHub Actions (Phase 3)</td></tr>
  <tr><td>Landing page photos supplied by the student</td><td>Licence not confirmed</td><td>Confirm before any public release</td></tr></tbody></table></div>
  <h3>Submodule status</h3>
  <p class="small"><b>Built (7):</b> Food Place Searching, Hidden Gem Highlighting, Food Place Visualisation, Route Planner, Food Places Visualisation, Food Places Analysis, Food Place Suggestion.<br><b>Partial (6):</b> Registration, Login, Profile and Preference Setup, Itinerary Planner, Itinerary Review and Customisation, Past Food Hopping Visualisation.</p>
  <h3>Google ratings (step 2.9a)</h3>
  <p class="small">Match only if names are similar and positions within about 100 m, and report the match rate. Google&rsquo;s terms only allow the place ID to be stored permanently, so ratings are refreshed by re-running the script. The reason not to scrape Google or TripAdvisor: it breaks their terms of service.</p>
</section>'''

meeting_html = '''
<section id="meeting" class="band wx">
  <h2 class="sec">Supervisor meeting: how to present it</h2>
  <p class="small">From the project&rsquo;s own meeting guide and study guide. The order and the five numbers below come from the guide; the one-line summaries are my own.</p>
  <h3>Agenda</h3>
  <ol class="five"><li>The module diagram (4 modules, 13 submodules).</li><li>Live demo.</li><li>Feasibility numbers.</li><li>Risks and next steps.</li><li>Questions, plus one decision to ask for.</li></ol>
  <h3>Demo script</h3>
  <p class="small">Choose the Komtar preset, add the six worked-example places, plan the route, show the comparison card, then open Analytics. If the Wi-Fi or database fails, fall back to screenshots in the slides.</p>
  <h3>Five numbers</h3>
  <ul class="nums"><li><b>0% / 2.3%</b><span>OSM places rated / tagged halal</span></li><li><b>14 / 35 / 6</b><span>gems / Popular / no label</span></li><li><b>26,689 / 34,732</b><span>road nodes / edges</span></li><li><b>39 of 40</b><span>trips where ACO was exact</span></li><li><b>about 9%</b><span>nearest neighbour longer; 10 stops take about 46 + 7 ms</span></li></ul>
  <h3>Decision to ask for</h3>
  <p class="small">Confirm the improved ACO settings (elitist deposit, MAX-MIN limits, beta = 2) as the default, with the textbook version kept as a baseline only, chosen for solution quality rather than speed.</p>
  <h3>Three tips from the guide</h3>
  <ul class="chips-row"><li>Say the answer first: &ldquo;Yes, it is feasible.&rdquo; Then show the proof.</li><li>State the limits yourself: sample ratings and early results.</li><li>For deep algorithm questions give the short answer and offer the details in the report.</li></ul>
  <h3>Before you start</h3>
  <ul class="chips-row"><li>Open the Supabase dashboard so the project wakes up</li><li>Start the backend and the web app</li><li>Check <code>/health/db</code> shows 1241 places</li><li>Practise the demo once</li><li>Have the diagrams open, laptop charged, phone hotspot ready</li></ul>
</section>'''

import markdown, re
_md = open(os.path.join(HERE, 'eytk.md')).read().split('\n', 1)[1]  # drop the H1
_h = markdown.markdown(_md, extensions=['tables', 'fenced_code'])
_h = _h.replace('<h3>', '<h5>').replace('</h3>', '</h5>').replace('<h2>', '<h3>').replace('</h2>', '</h3>')
_h = re.sub(r'<table>', '<div class="tbl-wrap"><table>', _h).replace('</table>', '</table></div>')
_h = re.sub(r'<pre>', '<div class="dgw" tabindex="0" role="group" aria-label="Scrollable code"><pre>', _h).replace('</pre>', '</pre></div>')
_h = _h.replace('<hr />', '')
eytk_html = ('<section id="eytk" class="band wx eytk"><h2 class="sec">EYTK: Everything You Need To Know</h2>'
             '<p class="small">The project&rsquo;s own study guide (<code>docs/presentation/EVERYTHING-YOU-NEED-TO-KNOW.md</code>), included in full, as written by the project owner. Names and the meeting time were removed from the first lines. Counts such as 277 / 93 tests are the guide&rsquo;s own and were not re-run.</p>'
             + _h + '</section>')

nav = '<a class="wx" href="#big-picture">Big picture</a>' + ''.join(f'<a class="w{n}" href="#week-{n}">Topic {n}</a>' for n in range(1, 7)) + '<a class="wx" href="#status">Status</a><a class="wx" href="#meeting">Meeting</a><a class="wx" href="#eytk">EYTK</a><a class="wx" href="#cheat-sheet">Cheat sheet</a><a class="wx" href="#drill">Flashcards</a>'

CSS = (open(os.path.join(HERE, 'style.css')).read() + open(os.path.join(HERE, 'extra_cst.css')).read()
       + open(os.path.join(HERE, 'bigp.css')).read() + open(os.path.join(HERE, 'extra_cmt323.css')).read())
JS = open(os.path.join(HERE, 'script.js')).read()

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#060510">
<title>CAT405 Notes: Final Year Project (MyMakanRoute)</title>
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="icon" href="../favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Caveat:wght@600&family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
<header class="hero">
  <a class="back" href="../">&larr; All subjects</a>
  <img class="subj" src="../assets/subjects/cat405.svg" width="96" height="96" alt="">
  <p class="eyebrow">CAT405 · Final Year Project · MyMakanRoute</p>
  <h1>One project, told as one story</h1>
  <p class="lead">There are no slides for this subject, so these are notes on the project itself. Read it as <b>problem, solution, new problem</b>: each part exists because the one before it left a gap.</p>
  <nav class="jump" aria-label="Jump to a section">{nav}</nav>
</header>
<main>

<section id="big-picture" class="bigp wx">
  <h2 class="sec">Big picture: read this first</h2>
  <p class="headsup"><b>One question runs through all six topics:</b> can a planner find good, lesser-known food places in Penang and turn a handful of them into the shortest walk? The idea (Topic 1) needs data (Topic 2). Data lets us label hidden gems and search (Topic 3). Picking several places creates an ordering problem, solved by the route planner (Topic 4). A feasibility study shows it works (Topic 5), and an application with an API, a web app, security and tests wraps it all (Topic 6).</p>
  <p class="small">Source note: these notes are my own summary of the owner&rsquo;s project folder (plan, feasibility report, architecture notes, code). Nothing here comes from lecture slides.</p>
  <h3>The chain: each part fixes a gap the last one left</h3>
  <ol class="chain c6">
    <li class="w1"><span class="tn">Topic 1</span><b>The idea and the plan</b><span class="kw">Four modules, thirteen submodules, phases</span><span class="bridge">But a hidden gem needs ratings &hellip;</span></li>
    <li class="w2"><span class="tn">Topic 2</span><b>The data</b><span class="kw">OSM, SAMPLE places, PostGIS, road graph</span><span class="bridge">But which places count as gems? &hellip;</span></li>
    <li class="w3"><span class="tn">Topic 3</span><b>Hidden gems and search</b><span class="kw">Rating 4.3+, 1 to 100 reviews, filters, ranking</span><span class="bridge">But what order should they be visited in? &hellip;</span></li>
    <li class="w4"><span class="tn">Topic 4</span><b>The route planner</b><span class="kw">Graph, snap, Dijkstra, ACO</span><span class="bridge">But does it really work? &hellip;</span></li>
    <li class="w5"><span class="tn">Topic 5</span><b>The proof</b><span class="kw">39 of 40 trips optimal; honest limits</span><span class="bridge">But it must live in a real app &hellip;</span></li>
    <li class="w6"><span class="tn">Topic 6</span><b>The application</b><span class="kw">Layers, API, web app, security, tests</span><span class="bridge">Still missing: real ratings and accounts, mobile app (see Status).</span></li>
  </ol>

  <h3>How Topic 1 connects to Topic 6</h3>
  <p class="small">Topic 1 promises four modules. Topic 3 delivers Food Discovery, Topic 4 the Route Planner of Food Hopping, Topic 5 the evidence that the plan is feasible, and Topic 6 the structure that holds all four modules together. Topic 2 is the shared foundation under every module. <i>(This mapping is my own.)</i></p>
  <div class="promise tbl-wrap"><table><thead><tr><th>Topic 1 promised &hellip;</th><th>Delivered in &hellip;</th></tr></thead><tbody>
    <tr><td>Food Discovery (search, hidden gems, visualisation)</td><td><b>Topic 3</b>, on the data of <b>Topic 2</b>.</td></tr>
    <tr><td>Food Hopping (route planner)</td><td><b>Topic 4</b>; proven in <b>Topic 5</b>.</td></tr>
    <tr><td>Food Stalls Analytics</td><td><b>Topic 5</b> (analytics numbers) and <b>Topic 6</b> (endpoint).</td></tr>
    <tr><td>User Management</td><td><b>Topic 6</b> (demo mode now); real login in the Status section.</td></tr>
    <tr><td>Intelligent Computing</td><td><b>Topic 4</b> (Ant Colony Optimisation).</td></tr></tbody></table></div>

  <h3>Four threads that run through all six topics</h3>
  <p class="small">These links are my own summary, not text from the project files.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Thread</th><th class="t1">Topic 1</th><th class="t2">Topic 2</th><th class="t3">Topic 3</th><th class="t4">Topic 4</th><th class="t5">Topic 5</th><th class="t6">Topic 6</th></tr></thead><tbody>
    <tr><th>Honesty about sample data</th><td>Never document unbuilt work</td><td>Ratings invented, marked SAMPLE</td><td>Gap: no 101 to 200 reviews</td><td>Speeds are assumptions</td><td>Indicative results only</td><td>Demo mode labelled</td></tr>
    <tr><th>Repeatability</th><td>Tests before commits</td><td>Migrations rebuild the same DB</td><td>Pure function</td><td>Seeded ACO</td><td><code>npm run feasibility</code></td><td>Mocked tests</td></tr>
    <tr><th>Settings, not fixed code</th><td>Decisions in the plan</td><td>Config from <code>.env</code></td><td>Gem thresholds</td><td>ACO parameters</td><td>Larger test planned</td><td>CORS and limits</td></tr>
    <tr><th>One job per part</th><td>Helper agents</td><td>One migration per change</td><td>Routes, controller, service, model</td><td>Graph, snap, Dijkstra, ACO</td><td>Brute force as judge</td><td>Three layers</td></tr></tbody></table></div>

  <h3>If you remember only six sentences</h3>
  <ol class="five">
    <li><b>Topic 1:</b> MyMakanRoute is a Penang food hopping planner with four modules and thirteen submodules that finds hidden gems and plans the shortest walk.</li>
    <li><b>Topic 2:</b> OpenStreetMap gives places and roads but no ratings, so 55 SAMPLE places carry invented ratings until real ones arrive.</li>
    <li><b>Topic 3:</b> a hidden gem has rating 4.3 or more and 1 to 100 reviews; results are ranked gems first, then nearest.</li>
    <li><b>Topic 4:</b> the planner snaps places to a road graph, uses Dijkstra for walking times and Ant Colony Optimisation for the visiting order.</li>
    <li><b>Topic 5:</b> in a small seeded study improved ACO found the optimum in 39 of 40 trips, while nearest neighbour was about 9% longer at 8 to 10 stops.</li>
    <li><b>Topic 6:</b> a three-layer Express and React application with validation, RLS and tests wraps it, with real accounts and ratings still to come.</li>
  </ol>
</section>

<section id="story" class="band">
  <h2 class="sec">Previously on MyMakanRoute</h2>
  <p class="small">Tap a card to jump to that topic. Read the &ldquo;But then&rdquo; line, then the next card&rsquo;s &ldquo;Problem&rdquo;: they are the same sentence.</p>
  {story_html}
</section>
{weeks_html}
{status_html}
{meeting_html}
{eytk_html}
<section id="cheat-sheet" class="band wx">
  <h2 class="sec">Cheat sheet</h2>
  <h3>Numbers to remember</h3>
  {numbers_html}
  <h3>Do not overclaim</h3>
  {traps_html}
</section>
<section id="drill" class="band wx">
  <h2 class="sec">Flashcards</h2>
  <p class="small">Tap a card to flip it. Say the answer out loud before you flip.</p>
  {cards_html}
</section>
</main>
<footer class="foot"><p>Built from the author&rsquo;s own MyMakanRoute project documents and code (state of 5 Nov 2026). There are no lecture slides for CAT405. Diagrams are redrawn. Items marked &ldquo;my own&rdquo; are my additions. Sample ratings in the project are invented and marked SAMPLE; test counts are quoted from the project&rsquo;s module-status file.</p></footer>
<script>
{JS}
</script>
</body>
</html>'''
open(os.path.join(OUT, 'index.html'), 'w').write(PAGE)
print('cat405 ok', len(PAGE), 'cards', N_CARDS)
