#!/usr/bin/env python3
"""CMT323 notes page, built from the user's 3 lecture decks (Weeks 1 to 3 = textbook Chapters 1 to 3).
Content rules: only what is in the decks; anything that is my own summary or reading is labelled on the page.
Diagrams are redrawn as inline SVG or HTML, not copied from the slides."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root (the folder that GitHub Pages serves)
from notes_lib import mindmap, terms, psn, qa, week, E

OUT = os.path.join(ROOT, 'cmt323')
os.makedirs(OUT, exist_ok=True)


# ====================================================================== tiny SVG helpers
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


def parr(d, uid, fb=False, dash=False):
    cls = 'ln' + (' fb' if fb else '') + (' dash' if dash else '')
    m = 'af' if fb else 'ah'
    return f'<path class="{cls}" d="{d}" marker-end="url(#{m}{uid})"/>'


# ====================================================================== mind maps
MAPS = {
1: mindmap('Information Systems',
  [('Why firms invest', ['Operational excellence', 'New products and business models', 'Customer and supplier intimacy', 'Improved decision making', 'Competitive advantage', 'Survival']),
   ('The digital firm', ['Relationships digitally enabled', 'Core processes on digital networks', 'Assets managed digitally', 'Time shifting, space shifting']),
   ('What is new', ['Cloud, big data, IoT, AI', 'Mobile digital platform', 'New business models', 'Managers more mobile'])],
  [('What an IS is', ['Data: raw facts', 'Information: useful form', 'Input, processing, output', 'Feedback corrects the input']),
   ('Three dimensions', ['Organization', 'Management', 'Technology']),
   ('Getting real value', ['Business information value chain', 'Complementary assets', 'The right business model']),
   ('Ways to study it', ['Technical approach', 'Behavioral approach', 'Sociotechnical view'])],
  'Mind map of Week 1: why firms invest in information systems, what an information system is, and how to get value from it'),
2: mindmap('E-business and Collaboration',
  [('Business processes', ['Logically related tasks', 'Flows of material and information', 'Can be an asset or a liability', 'One function or cross-functional']),
   ('Systems by level', ['TPS: daily transactions', 'MIS: routine reports', 'DSS: nonroutine analysis', 'ESS: senior judgment']),
   ('Enterprise applications', ['Enterprise systems (ERP)', 'Supply chain management', 'Customer relationship mgmt', 'Knowledge management'])],
  [('Linking technology', ['Intranet: internal', 'Extranet: authorized partners', 'E-commerce is part of e-business', 'E-government']),
   ('Collaboration', ['Short or long term', 'Informal or formal teams', 'Needs a collaborative culture', 'Gains: quality, innovation']),
   ('Social business', ['Internal and external networks', 'Needs information transparency', 'Efficiency, innovation, speed']),
   ('Tools', ['E-mail, IM, wikis', 'Videoconferencing', 'Cloud: Google Drive and Docs', 'SharePoint, IBM Notes, Yammer']),
   ('IS function', ['CIO leads', 'Programmers, analysts, end users', 'IT governance'])],
  'Mind map of Week 2: business processes, systems for each management level, enterprise applications and collaboration'),
3: mindmap('Organizations and Strategy',
  [('Features of organizations', ['Hierarchy and accountability', 'Routines and business processes', 'Politics and culture', 'Environment and structure']),
   ('Impacts of IT', ['Lower transaction costs', 'Lower agency costs', 'Flatter organizations', 'Resistance to change']),
   ('Environment', ['Reciprocal relationship', 'Disruptive technologies', 'First movers, fast followers'])],
  [('Competitive forces', ['Traditional competitors', 'New market entrants', 'Substitute products', 'Customers', 'Suppliers']),
   ('Four strategies', ['Low-cost leadership', 'Product differentiation', 'Focus on market niche', 'Customer and supplier intimacy']),
   ('Models', ['Value chain', 'Value web', 'Synergies, core competencies']),
   ('Network strategies', ['Network economics', 'Virtual company', 'Business ecosystems']),
   ('Challenges', ['Rivals can copy systems', 'Align IT with objectives'])],
  'Mind map of Week 3: how organizations and information technology shape each other, and strategies for competitive advantage'),
}

# ====================================================================== week 1 visuals
d_is = svg(700, 322,
    txt(110, 18, 'Suppliers', 'ts') + txt(590, 18, 'Customers', 'ts')
    + arr(110, 78, 110, 26, 'is', dash=True, both=True) + arr(590, 78, 590, 26, 'is', dash=True, both=True)
    + '<rect class="lane" x="20" y="48" width="660" height="232" rx="14"/>'
    + txt(36, 68, 'ORGANIZATION', 'ts', 'start')
    + '<rect class="bx2" x="40" y="80" width="620" height="186" rx="12"/>'
    + txt(56, 100, 'INFORMATION SYSTEM', 'ts', 'start')
    + box(64, 126, 150, 70, ['Input', 'data from inside', 'and outside'], small_rest=True)
    + box(275, 116, 150, 90, ['Processing', 'classify, arrange,', 'calculate'], 'bxs', small_rest=False)
    + box(486, 126, 150, 70, ['Output', 'information'], small_rest=True)
    + arr(214, 161, 275, 161, 'is') + arr(425, 161, 486, 161, 'is')
    + parr('M561 196 V232 H139 V196', 'is', fb=True) + txt(350, 252, 'Feedback to evaluate or correct the input', 'ts')
    + arr(130, 292, 130, 266, 'is', dash=True, both=True) + arr(350, 292, 350, 266, 'is', dash=True, both=True) + arr(570, 292, 570, 266, 'is', dash=True, both=True)
    + txt(130, 312, 'Regulatory agencies', 'ts') + txt(350, 312, 'Stockholders', 'ts') + txt(570, 312, 'Competitors', 'ts'),
    'Redrawn: input, processing, output and feedback inside an organization, surrounded by suppliers, customers, regulators, stockholders and competitors', 'is')

d_bv = svg(700, 292,
    txt(10, 16, 'Business processes (slide figure)', 'ts', 'start')
    + box(10, 24, 105, 48, ['Supply chain', 'management']) + box(125, 24, 105, 48, ['Enterprise', 'management'])
    + box(240, 24, 105, 48, ['Customer', 'management']) + box(355, 24, 105, 48, ['Knowledge', 'management'])
    + ''.join(ln(cx, 72, cx, 90) for cx in (62, 177, 292, 407)) + ln(62, 90, 407, 90)
    + box(10, 116, 125, 62, ['Data collection', 'and storage']) + box(160, 116, 125, 62, ['Transformation', 'into business', 'systems'])
    + box(310, 116, 125, 62, ['Dissemination'])
    + arr(135, 147, 160, 147, 'bv') + arr(285, 147, 310, 147, 'bv')
    + arr(372, 116, 372, 91, 'bv') + arr(372, 178, 372, 195, 'bv')
    + ln(57, 196, 409, 196) + ''.join(ln(cx, 196, cx, 214) for cx in (57, 168, 281, 409))
    + box(10, 214, 95, 48, ['Planning']) + box(113, 214, 110, 48, ['Coordinating']) + box(231, 214, 100, 48, ['Controlling'])
    + box(339, 214, 140, 48, ['Modeling and', 'decision making'])
    + txt(10, 282, 'Management activities (slide figure)', 'ts', 'start')
    + parr('M460 48 H590 V108', 'bv') + parr('M479 238 H590 V186', 'bv')
    + box(500, 108, 190, 78, ['Firm profitability', 'and strategic position'], 'bxs'),
    'Redrawn: the business information value chain, from raw data through business systems to firm profitability', 'bv')

w1_vis = f'''
  <h3>What is new (from the slides)</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Area</th><th>What the slides say</th></tr></thead><tbody>
  <tr><th>Spending</th><td>Global spending on IT and IT services: nearly $3.8 trillion in 2019, plus $160 billion on management consulting and services.</td></tr>
  <tr><th>IT innovations</th><td>Cloud computing, big data, Internet of Things; the mobile digital platform; AI and machine learning; social networks used for business goals.</td></tr>
  <tr><th>E-commerce</th><td>Worldwide e-commerce nearly $3.6 trillion in 2019. Mobile retail e-commerce grows more than 20 percent a year, almost $300 billion in 2020.</td></tr>
  <tr><th>Management</th><td>Managers more mobile; they use social networks and collaboration tools; business intelligence applications speed up.</td></tr>
  <tr><th>The firm</th><td>More collaborative, less hierarchy, more weight on skills, faster decisions based on data, more willingness to talk to consumers.</td></tr></tbody></table></div>
  <p class="small">The slides also say a firm needs organizational, management and cultural changes, not only IT spending, to get the full business value. That sentence is the seed of the whole week.</p>
  <div class="two"><div><h4>A flattened world</h4><p>The Internet and global communications cut the cost of operating and trading worldwide. The result is competition for jobs, markets, resources and ideas, and economies that depend on each other.</p></div>
  <div><h4>The digital firm</h4><p>Its important business relationships, core processes and key assets are all handled digitally. That gives flexibility: <b>time shifting</b> (work at any time) and <b>space shifting</b> (work from any place).</p></div></div>

  <h3>Why firms invest: six strategic business objectives</h3>
  <div class="cards3">
    <div class="c"><h4>1. Operational excellence</h4><p>Better efficiency gives higher profit.</p><p class="eg">Walmart: digital links between suppliers and stores; over $524 billion sales in 2019.</p></div>
    <div class="c"><h4>2. New products, services, business models</h4><p>A <b>business model</b> is how a company produces, delivers and sells its products and services.</p><p class="eg">Apple: iTunes changed music distribution, then iPod, iPhone, iPad.</p></div>
    <div class="c"><h4>3. Customer and supplier intimacy</h4><p>Well-served customers come back and buy more. Close suppliers lower costs.</p><p class="eg">Mandarin Oriental Hotel tracks guest preferences. JC Penney and its Hong Kong supplier.</p></div>
    <div class="c"><h4>4. Improved decision making</h4><p>Without accurate information, managers rely on forecasts, best guesses and luck, and resources get misplaced.</p><p class="eg">Verizon: web dashboard with real-time data on complaints, network performance, outages.</p></div>
    <div class="c"><h4>5. Competitive advantage</h4><p>Often the result of achieving the earlier objectives: charge less, perform better, respond faster.</p><p class="eg">Apple, Walmart, UPS.</p></div>
    <div class="c"><h4>6. Survival</h4><p>Sometimes IT is just the cost of doing business: keep up with rivals, or obey regulations.</p><p class="eg">Citibank's ATMs. Toxic Substances Control Act, Sarbanes-Oxley Act.</p></div>
  </div>

  <h3>What an information system is</h3>
  <div class="two"><div><h4>Data</h4><p>Streams of raw facts.</p></div><div><h4>Information</h4><p>Data shaped into a form that is meaningful and useful.</p></div></div>
  <p class="small"><b>Information technology (IT)</b> is the hardware and software a business uses. An <b>information system</b> is a set of connected parts that manage information to support decisions and control, and to help with analysis, visualization and creating products. A computer is only the technical foundation, like the materials and tools used to build a house; the information system is the whole house.</p>
  {d_is}
  <p class="small">Redrawn from the slide idea. The four activities are <b>input, processing, output and feedback</b>. Feedback returns output to the right people so they can check or correct the input.</p>

  <h3>The three dimensions: more than computers</h3>
  <div class="cards3">
    <div class="c"><h4>Organization</h4><p>Hierarchy of authority (see the levels below), separate business functions (sales and marketing, human resources, finance and accounting, manufacturing and production), unique business processes, unique culture, and organizational politics.</p></div>
    <div class="c"><h4>Management</h4><p>Managers set the strategy for business challenges. They must also act creatively: create new products and services, and sometimes re-create the organization.</p></div>
    <div class="c"><h4>Technology</h4><p>Computer hardware and software, data management technology, networking and telecommunications (networks, the Internet, intranets, extranets, the World Wide Web). The <b>IT infrastructure</b> is the platform the system is built on.</p></div>
  </div>
  <p class="small"><b>The slides' UPS example:</b> organization = procedures for tracking packages and managing inventory; management = watching service levels and costs; technology = handheld computers, bar-code scanners, networks and desktop computers.</p>
  <h4>Levels in a firm</h4>
  <div class="pyr" aria-label="Levels in a firm: senior management at the top, middle management, operational management at the bottom">
    <div style="--k:3;width:40%"><b>Senior management</b></div>
    <div style="--k:2;width:68%"><b>Middle management</b><br>scientists and knowledge workers</div>
    <div style="--k:1;width:100%"><b>Operational management</b><br>production and service workers, data workers</div>
  </div>

  <h3>Why technology alone does not pay</h3>
  <p class="small">An information system is a tool for creating value. The <b>business information value chain</b> shows raw data being collected, turned into business information and passed on, so that managers can plan, coordinate, control and decide better. The value of a system depends partly on how far it leads to better decisions, higher efficiency and higher profit.</p>
  {d_bv}
  <p class="small">Redrawn. The slide figure shows two groups, business processes and management activities, both feeding firm profitability.</p>
  <p class="small"><b>But returns vary a lot.</b> The slide plots firms by IT capital stock against productivity (relative to the industry average): firms that spend similar amounts on IT end up at quite different productivity. The two factors the slides name are adopting the right business model and investing in <b>complementary assets</b> (assets you need before the main investment pays off; example: invest in the technology and in the people to make it work).</p>
  <div class="cards3">
    <div class="c"><h4>Organizational assets</h4><p>The appropriate business model. Efficient business processes.</p></div>
    <div class="c"><h4>Managerial assets</h4><p>Incentives for management innovation. Teamwork and collaborative work environments.</p></div>
    <div class="c"><h4>Social assets</h4><p>The Internet and telecommunications infrastructure. Technology standards.</p></div>
  </div>

  <h3>Three ways to study information systems</h3>
  <div class="cards3">
    <div class="c"><h4>Technical approach</h4><p>Mathematically based models. Disciplines: computer science, management science, operations research.</p></div>
    <div class="c"><h4>Behavioral approach</h4><p>Behavioral issues such as strategic business integration and implementation. Disciplines: psychology, economics, sociology.</p></div>
    <div class="c"><h4>Sociotechnical view (this course)</h4><p>Best performance comes from <b>jointly optimizing</b> the social and the technical system, which avoids a purely technological approach. Four actors: hardware and software suppliers, business firms, managers and employees, and the firm's environment (legal, social, cultural).</p></div>
  </div>
'''
w1_terms = terms([
 ('Information technology (IT)', 'The hardware and software a business uses to reach its objectives.'),
 ('Information system', 'Interrelated components that manage information to support decision making and control, and help with analysis, visualization and creating products.'),
 ('Data / Information', 'Data is a stream of raw facts. Information is data shaped into a meaningful, useful form.'),
 ('Input, processing, output, feedback', 'The four activities that produce information. Feedback sends output back to members of the organization to evaluate or correct the input.'),
 ('Business model', 'How a company produces, delivers and sells its products and services.'),
 ('Digital firm', 'A firm whose key relationships, core processes and corporate assets are digitally enabled and managed. Allows time shifting and space shifting.'),
 ('IT infrastructure', 'The platform an information system is built on (hardware, software, data management, networking).'),
 ('Knowledge workers / data workers', 'Staff groups in the firm hierarchy. The slide figure puts knowledge workers with middle management and data workers with operational management.'),
 ('Business information value chain', 'Raw data is acquired and transformed through stages that add value to it.'),
 ('Complementary assets', 'Assets required to get value from a primary investment. Organizational, managerial and social.'),
 ('Technical approach', 'Mathematical models; computer science, management science, operations research.'),
 ('Behavioral approach', 'Behavioral issues; psychology, economics, sociology.'),
 ('Sociotechnical view', 'Optimize the social and technical systems together, not the technology alone.'),
])
w1_boss = qa('Name the six strategic business objectives and give one example from the slides for each.',
 '''<ol><li><b>Operational excellence:</b> Walmart's links between suppliers and stores.</li><li><b>New products, services, business models:</b> Apple's iTunes.</li>
 <li><b>Customer and supplier intimacy:</b> Mandarin Oriental Hotel tracking preferences (customers); JC Penney with its Hong Kong supplier.</li>
 <li><b>Improved decision making:</b> Verizon's real-time dashboard.</li><li><b>Competitive advantage:</b> Apple, Walmart, UPS.</li><li><b>Survival:</b> Citibank's ATMs; regulations such as Sarbanes-Oxley.</li></ol>''', 1) + \
 qa('A student says "an information system is just a computer". Correct them using the slides.',
 '''<p>A computer and its software are only the <b>technical foundation and tools</b>, like the materials and tools used to build a house. An information system also has an <b>organization</b> dimension (hierarchy, functions, processes, culture, politics) and a <b>management</b> dimension (strategy, creative decisions). It turns <b>data</b> into <b>information</b> through <b>input, processing, output and feedback</b>.</p>''', 2) + \
 qa('UPS case (slide question): what are the inputs, processing and outputs of UPS\'s package tracking system?',
 '''<p>The slides give only the question and the three dimensions of the UPS system (procedures for tracking packages, monitoring service levels and costs, and handhelds, bar-code scanners, networks and desktop computers). They give <b>no model answer</b>.</p>
 <p><b>My own reading:</b> <b>input</b> = package and shipping data captured by scanners and handhelds; <b>processing</b> = the networked systems that record and update each package's status; <b>output</b> = tracking information and reports for staff and managers. Treat this as my summary, not slide text.</p>''', 3) + \
 qa('Two firms spend the same amount on IT but get very different returns. Why, according to the slides?',
 '''<p>Investing in technology does not guarantee good returns. The slides name two factors: <b>adopting the right business model</b> and <b>investing in complementary assets</b> (organizational, managerial and social capital). A firm that buys the technology but not the people, processes and teamwork needed to use it gets a lower return.</p>''', 4) + \
 qa('What does the sociotechnical view say, and why does it matter?',
 '''<p>Best organizational performance comes from <b>jointly optimizing</b> the social system and the technical system used in production. It matters because it stops a firm from treating a new system as a purely technological project.</p>''', 5)

# ====================================================================== week 2 visuals
d_of = svg(700, 282,
    ''.join(f'<rect class="lane" x="160" y="{y}" width="530" height="80" rx="10"/>' for y in (10, 100, 190))
    + box(10, 10, 140, 80, ['Sales'], 'bxs') + box(10, 100, 140, 80, ['Accounting'], 'bxs') + box(10, 190, 140, 80, ['Manufacturing', 'and production'], 'bxs')
    + box(180, 25, 120, 50, ['Generate order']) + box(325, 25, 120, 50, ['Submit order'])
    + box(325, 115, 120, 50, ['Check credit']) + box(465, 115, 100, 50, ['Approve', 'credit']) + box(585, 115, 100, 50, ['Generate', 'invoice'])
    + box(465, 205, 100, 50, ['Assemble', 'product']) + box(585, 205, 100, 50, ['Ship', 'product'])
    + arr(300, 50, 325, 50, 'of') + arr(385, 75, 385, 115, 'of') + arr(445, 140, 465, 140, 'of') + arr(565, 140, 585, 140, 'of')
    + parr('M635 165 V185 H515 V205', 'of') + arr(565, 230, 585, 230, 'of'),
    'Redrawn: the order fulfillment process across sales, accounting, and manufacturing and production', 'of')

d_ea = svg(700, 330,
    txt(190, 18, 'Suppliers, business partners', 'ts') + txt(510, 18, 'Customers, distributors', 'ts')
    + box(50, 30, 280, 62, ['Supply chain management', 'systems']) + box(370, 30, 280, 62, ['Customer relationship', 'management systems'])
    + ln(190, 92, 190, 118) + ln(510, 92, 510, 118)
    + box(20, 118, 660, 56, ['Enterprise systems', 'one platform across all functional areas'], 'bxs')
    + box(20, 188, 660, 44, ['Knowledge management systems'])
    + ln(100, 232, 100, 258) + ln(270, 232, 270, 258) + ln(440, 232, 440, 258) + ln(605, 232, 605, 258)
    + box(20, 258, 160, 44, ['Sales and marketing'], 'bx2') + box(190, 258, 160, 44, ['Manufacturing', 'and production'], 'bx2')
    + box(360, 258, 160, 44, ['Finance and', 'accounting'], 'bx2') + box(530, 258, 150, 44, ['Human resources'], 'bx2')
    + txt(350, 322, 'Functional areas', 'ts'),
    'Redrawn: enterprise applications link supply chain, customers and knowledge across the functional areas of a firm', 'ea')

d_cr = svg(700, 262,
    box(10, 10, 300, 108, ['Collaboration capability', 'Open culture', 'Decentralized structure', 'Breadth of collaboration'], small_rest=False)
    + box(10, 138, 300, 108, ['Collaboration technology', 'for implementation and operations', 'for strategic planning'], small_rest=False)
    + box(390, 88, 130, 70, ['Collaboration', 'quality']) + box(570, 88, 120, 70, ['Firm', 'performance'], 'bxs')
    + arr(310, 64, 390, 112, 'cr') + arr(310, 192, 390, 134, 'cr') + arr(520, 123, 570, 123, 'cr'),
    'Redrawn: collaboration capability and collaboration technology lead to collaboration quality, which leads to firm performance', 'cr')

w2_vis = f'''
  <h3>Business processes: how work actually flows</h3>
  <p class="small">A <b>business process</b> is a logically related set of tasks that defines how a specific piece of business is done; it carries flows of material, information and knowledge. A business can be seen as a collection of processes. A process may sit in one functional area or cut across several, and it can be an <b>asset</b> (done well) or a <b>liability</b> (done badly).</p>
  <div class="tbl-wrap"><table><thead><tr><th>Functional area</th><th>Example process (slides)</th></tr></thead><tbody>
  <tr><th>Manufacturing and production</th><td>Assembling the product</td></tr><tr><th>Sales and marketing</th><td>Identifying customers</td></tr>
  <tr><th>Finance and accounting</th><td>Creating financial statements</td></tr><tr><th>Human resources</th><td>Hiring employees</td></tr></tbody></table></div>
  {d_of}
  <p class="small">Redrawn from the slide's order fulfillment example: one order crosses three departments, so one process involves several functions.</p>
  <div class="two"><div><h4>IT makes existing processes more efficient</h4><p>Automate steps that were manual.</p></div>
  <div><h4>IT enables entirely new processes</h4><p>Change the flow of information, replace sequential steps with parallel steps, remove delays in decision making, and support new business models.</p></div></div>

  <h3>Systems for different management groups</h3>
  <div class="pyr" aria-label="System types by management level">
    <div style="--k:3;width:38%"><b>ESS</b> senior management</div>
    <div style="--k:2;width:70%"><b>DSS and MIS</b> middle management</div>
    <div style="--k:1;width:100%"><b>TPS</b> operational managers and staff</div>
  </div>
  <p class="small">The slides group MIS, DSS and ESS as <b>systems for business intelligence</b>: data and software tools for organizing and analyzing data so managers can decide better.</p>
  <div class="tbl-wrap"><table><thead><tr><th>System</th><th>Serves</th><th>What it does</th><th>Example in the slides</th></tr></thead><tbody>
  <tr><th>Transaction processing system (TPS)</th><td>Operational managers and staff</td><td>Performs and records the daily routine transactions; lets managers watch operations; predefined, structured goals and decisions.</td><td>Sales order entry, payroll, shipping</td></tr>
  <tr><th>Management information system (MIS)</th><td>Middle management</td><td>Reports on current performance from TPS data; answers routine questions with a predefined procedure; little analytic capability.</td><td>Sales by product and region report</td></tr>
  <tr><th>Decision support system (DSS)</th><td>Middle management</td><td>Supports <b>nonroutine</b> decisions; may use outside data as well as TPS and MIS data.</td><td>"What happens to the production schedule if December sales double?" Model-driven: voyage-estimating. Data-driven: Intrawest marketing analysis.</td></tr>
  <tr><th>Executive support system (ESS)</th><td>Senior management</td><td>Nonroutine decisions that need judgment, evaluation and insight; uses outside events (new tax laws, competitors) plus summaries from MIS and DSS.</td><td>Digital dashboard with a real-time view of financial performance</td></tr></tbody></table></div>
  <p class="small">The data chain from the slides: the TPS collects the transactions, and the MIS reads the TPS files to build reports and online displays for managers.</p>

  <h3>Enterprise applications: linking the whole firm</h3>
  <p class="small">Enterprise applications work across functional areas, run business processes across the firm and include all management levels.</p>
  {d_ea}
  <div class="cards3">
    <div class="c"><h4>Enterprise systems (ERP)</h4><p>Also called enterprise resource planning. Put data from key business processes into one system and speed up information flow. This gives more flexibility in answering customer requests, more accuracy in order fulfillment, and an overall view of operations for managers.</p></div>
    <div class="c"><h4>Supply chain management (SCM)</h4><p>Manages relationships and shared information (orders, production, inventory) with suppliers, purchasers, distributors and logistics firms. Goal: move the right amount of product from source to consumer as quickly and cheaply as possible. It is an <b>interorganizational system</b>: information flows across organizational boundaries.</p></div>
    <div class="c"><h4>Customer relationship management (CRM)</h4><p>Coordinates sales, marketing and customer service. Goals: optimize revenue, improve satisfaction, increase retention, identify and keep the most profitable customers, increase sales.</p></div>
    <div class="c"><h4>Knowledge management (KMS)</h4><p>Captures and applies knowledge and expertise, makes it available wherever it is needed, and links the firm to outside sources of knowledge.</p></div>
  </div>
  <p class="small"><b>Platforms.</b> An <b>intranet</b> is an internal network built on Internet standards, often a private part of the company website. An <b>extranet</b> is a company site open only to authorized vendors and suppliers, which helps collaboration. <b>E-business</b> = using digital technology and the Internet to run major business processes. <b>E-commerce</b> = the part of e-business that is buying and selling over the Internet. <b>E-government</b> = delivering information and services to citizens, employees and businesses with Internet technology.</p>

  <h3>Collaboration and social business</h3>
  <p class="small"><b>Collaboration</b> can be short or long term, informal or formal (teams). The slides give six reasons it matters more now: the changing nature of work, growth of professional "interaction jobs", changes in how the firm is organized, the changing scope of the firm, the emphasis on innovation, and the changing culture of work.</p>
  <div class="two"><div><h4>Social business</h4><p>Using internal and external social networking platforms to engage employees, customers and suppliers. It aims to deepen interactions and speed up information sharing, needs information transparency, and is seen as a way to raise efficiency, spur innovation and speed up decisions.</p></div>
  <div><h4>Business benefits</h4><p><b>Productivity</b> (share knowledge, solve problems), <b>quality</b> (faster fixes), <b>innovation</b> (more ideas), <b>customer service</b> (complaints handled faster), and so better <b>financial performance</b>.</p></div></div>
  {d_cr}
  <p class="small">Redrawn. A firm that relies on "command and control" puts no value on teamwork; a collaborative culture has senior managers who rely on teams, and a manager's purpose is to build teams.</p>
  <h4>The time/space matrix: pick the tool by when and where people work</h4>
  <div class="tsm">
    <div></div><div class="h">Same time<small>synchronous</small></div><div class="h">Different time<small>asynchronous</small></div>
    <div class="h">Same place<small>colocated</small></div>
    <div class="cell"><b>Face-to-face interactions</b>decision rooms, single-display groupware, shared table, wall displays, roomware</div>
    <div class="cell"><b>Continuous task</b>team rooms, large public display, shift work groupware, project management</div>
    <div class="h">Different place<small>remote</small></div>
    <div class="cell"><b>Remote interactions</b>video conferencing, instant messaging, chat and virtual worlds (the slide spells it "charts/MUDs/virtual words"; I read that as a typo), shared screens, multi-user editors</div>
    <div class="cell"><b>Communication + coordination</b>e-mail, bulletin boards, blogs, asynchronous conferencing, group calendars, workflow, version control, wikis</div>
  </div>
  <h4>Choosing collaboration tools: six steps</h4>
  <ol class="steps-h">
    <li>Identify your firm's collaboration challenges.</li><li>Identify what kinds of solutions are available.</li><li>Analyze the cost and benefit of the available products.</li>
    <li>Evaluate security risks.</li><li>Consult users about implementation and training issues.</li><li>Evaluate the product vendors.</li>
  </ol>
  <p class="small"><b>Tools named in the slides:</b> e-mail and instant messaging, wikis, virtual worlds, virtual meeting systems (videoconferencing, telepresence), cloud collaboration services (Google Drive, Google Docs), Microsoft SharePoint and IBM Notes, and enterprise social networking tools.</p>

  <h3>The information systems department</h3>
  <div class="two"><div><h4>People</h4><p>Led by a <b>chief information officer (CIO)</b>. Other senior roles: chief security officer, chief knowledge officer, chief privacy officer, chief data officer. Staff: programmers, systems analysts, information systems managers and end users.</p></div>
  <div><h4>IT governance</h4><p>The strategies and policies for using IT in the organization: decision rights, accountability, and how the IS function is organized (centralized, decentralized and so on).</p></div></div>
'''
w2_terms = terms([
 ('Business process', 'A logically related set of tasks that defines how a specific business task is done; flows of material, information and knowledge.'),
 ('Transaction processing system (TPS)', 'Records daily routine transactions such as order entry, payroll and shipping.'),
 ('Management information system (MIS)', 'Here: a type of system that reports on current performance from TPS data. Do not confuse it with MIS as the name of the field.'),
 ('Decision support system (DSS)', 'Supports nonroutine decisions. Model-driven or data-driven.'),
 ('Executive support system (ESS)', 'Supports senior management with outside events plus MIS and DSS summaries; for example a digital dashboard.'),
 ('Business intelligence', 'Data and software tools for organizing and analyzing data to improve decisions.'),
 ('Enterprise application', 'A system that spans functional areas, runs processes across the firm and includes all management levels.'),
 ('Enterprise system (ERP)', 'Integrates data from key business processes into a single system.'),
 ('Supply chain management (SCM)', 'Manages shared information and relationships with suppliers, distributors and logistics firms.'),
 ('Customer relationship management (CRM)', 'Coordinates sales, marketing and service to keep and grow profitable customers.'),
 ('Knowledge management system (KMS)', 'Captures and applies knowledge and expertise across the firm.'),
 ('Interorganizational system', 'A system that automates information flow across organizational boundaries (the slides use SCM as the example).'),
 ('Intranet / Extranet', 'Intranet: internal network on Internet standards. Extranet: site open to authorized vendors and suppliers.'),
 ('E-business / E-commerce / E-government', 'Digital-run business processes / buying and selling online (a subset of e-business) / services to citizens, employees and businesses.'),
 ('Social business', 'Using social networking platforms to engage employees, customers and suppliers.'),
 ('Time/space matrix', 'A grid of collaboration tools by same or different time, and same or different place.'),
 ('IT governance', 'Strategies, policies, decision rights and accountability for IT, and how the IS function is organized.'),
])
w2_boss = qa('Match each system type to the management level it serves, and give its key feature.',
 '''<ul><li><b>TPS</b> serves operational managers and staff: daily routine transactions with predefined, structured goals.</li><li><b>MIS</b> serves middle management: routine reports from TPS data with little analytic capability.</li>
 <li><b>DSS</b> serves middle management: nonroutine decisions, may use outside data.</li><li><b>ESS</b> serves senior management: nonroutine decisions needing judgment, with outside events and a dashboard view.</li></ul>''', 1) + \
 qa('Difference between an MIS and a DSS? Use the slides\' example.',
 '''<p>An MIS answers <b>routine</b> questions with a predefined procedure (for example a sales-by-product-and-region report). A DSS supports <b>nonroutine</b> questions such as "what is the impact on the production schedule if December sales double?", and may add outside information to TPS and MIS data.</p>''', 2) + \
 qa('Why do firms need enterprise applications, and what are the four?',
 '''<p>The slides say they link the enterprise: they span functional areas, run business processes across the firm and include all levels of management. The four are <b>enterprise systems (ERP), supply chain management, customer relationship management and knowledge management</b>.</p>
 <p><b>My own reading:</b> without them, each department's system holds its own data, so the order in the fulfillment example would have to be re-entered at each step. The slides do not say this in so many words.</p>''', 3) + \
 qa('Sharp Corporation (slide case): what was the problem, and what solved it?',
 '''<p><b>Problem:</b> hierarchical, top-down processes, new competitors, and a lack of collaboration and idea sharing. <b>Solution:</b> develop a knowledge-sharing strategy and goals, redesign the knowledge-sharing and collaboration processes, change the organizational culture, and implement Microsoft Yammer. The slides conclude that culture and business processes matter as much as the software.</p>''', 4) + \
 qa('Place these in the time/space matrix: wikis, video conferencing, team rooms.',
 '''<ul><li><b>Wikis:</b> different place, different time (communication + coordination).</li><li><b>Video conferencing:</b> different place, same time (remote interactions).</li><li><b>Team rooms:</b> same place, different time (continuous task).</li></ul>''', 5) + \
 qa('How are e-business, e-commerce and e-government related?',
 '''<p><b>E-business</b> is the broad idea: running major business processes with digital technology and the Internet. <b>E-commerce</b> is a subset of it: buying and selling goods and services over the Internet. <b>E-government</b> is the same Internet technology used to deliver information and services to citizens, employees and businesses.</p>''', 6)

# ====================================================================== week 3 visuals
d_tw = svg(700, 232,
    box(20, 76, 170, 80, ['Organizations'], 'bxs') + box(510, 76, 170, 80, ['Information', 'technology'], 'bxs')
    + box(250, 36, 200, 160, ['Mediating factors', 'Environment', 'Culture', 'Structure', 'Business processes', 'Politics', 'Management decisions'], small_rest=False)
    + parr('M105 76 C105 -4 595 -4 595 76', 'tw') + parr('M595 156 C595 236 105 236 105 156', 'tw'),
    'Redrawn: organizations and information technology influence each other, through six mediating factors', 'tw')


def tri(cx, rows, y0, step, gap):
    out = ''
    for i, n in enumerate(rows):
        for j in range(n):
            out += f'<circle class="circ" cx="{cx + (j - (n - 1) / 2) * gap:.1f}" cy="{y0 + i * step}" r="9"/>'
    return out


d_fl = svg(700, 222,
    f'<polygon class="lane" points="175,10 17,166 333,166"/>' + tri(175, [1, 3, 5, 7], 40, 38, 34)
    + txt(175, 192, 'Traditional: many levels of management', 'ts')
    + f'<polygon class="lane" points="525,10 367,166 683,166"/>' + tri(525, [1, 3, 9], 40, 56, 32)
    + txt(525, 192, 'Flattened: layers of management removed', 'ts')
    + txt(350, 214, 'Illustration only: the circle counts are mine, the slide figure shows the idea', 'ts'),
    'Redrawn: a traditional hierarchy with many levels next to a flattened organization with fewer levels', 'fl')

d_pf = svg(700, 358,
    box(20, 12, 200, 58, ['New market entrants']) + box(480, 12, 200, 58, ['Substitute products', 'and services'])
    + box(20, 288, 200, 58, ['Suppliers']) + box(480, 288, 200, 58, ['Customers'])
    + '<ellipse class="lane" cx="350" cy="179" rx="190" ry="92"/>'
    + txt(350, 120, 'Traditional competitors', 'tb tc')
    + box(232, 152, 110, 56, ['The firm'], 'bxs') + box(372, 152, 120, 56, ['Competitors'], 'bx')
    + arr(342, 180, 372, 180, 'pf', both=True)
    + arr(150, 70, 232, 114, 'pf') + arr(550, 70, 468, 114, 'pf') + arr(150, 288, 232, 244, 'pf') + arr(550, 288, 468, 244, 'pf'),
    'Redrawn: Porter\'s competitive forces model: new entrants, substitutes, suppliers and customers press on the firm and its competitors', 'pf')

w3_vis = f'''
  <h3>Organizations and IT shape each other</h3>
  <p class="small">The slides say IT and organizations influence each other, and the relationship depends on the organization's structure, business processes, politics, culture, environment and management decisions.</p>
  {d_tw}
  <div class="two"><div><h4>Technical definition</h4><p>A formal social structure that processes resources from the environment to produce outputs. A formal legal entity with internal rules and procedures, and a social structure.</p></div>
  <div><h4>Behavioral definition</h4><p>A collection of rights, privileges, obligations and responsibilities, balanced over time through conflict and conflict resolution.</p></div></div>
  <h4>Features of organizations</h4>
  <ul class="chips-row"><li>Hierarchical structure</li><li>Accountability and authority, with impartial decision making</li><li>The principle of efficiency</li><li>Routines and business processes</li><li>Politics, culture, environments, structures</li></ul>
  <p class="small"><b>Routines</b> are standard operating procedures: precise rules and practices for almost every expected situation. A <b>business process</b> is a collection of routines, and a <b>firm</b> is a collection of business processes.</p>
  <div class="cards3">
    <div class="c"><h4>Politics</h4><p>Different viewpoints cause struggle, competition and conflict. Political resistance greatly hampers organizational change.</p></div>
    <div class="c"><h4>Culture</h4><p>Assumptions that define goals and products: what to produce, how and where, and for whom. A strong unifying force, and also a limit on change.</p></div>
    <div class="c"><h4>Environments</h4><p>Organizations and environments affect each other and organizations depend on theirs. Environments change faster than organizations. An information system can act as a lens for scanning the environment.</p></div>
  </div>
  <p class="small"><b>Disruptive technologies</b> substitute products that perform as well as or better than the existing one, and bring sweeping change (examples: personal computers, smartphones, big data, AI, the Internet). <b>First movers</b> invent them; <b>fast followers</b> have the size and resources to profit from them.</p>
  <p class="small"><b>Mintzberg's five structures:</b> entrepreneurial, machine bureaucracy, divisionalized bureaucracy, professional bureaucracy, adhocracy. An information system often reflects the structure. Other features: goals (coercive, utilitarian, normative), constituencies, leadership styles, types of tasks.</p>

  <h3>What IT does to organizations</h3>
  <div class="two"><div><h4>Economic impact</h4><p>IT is a factor of production, like capital and labor, and it changes the cost of information. <b>Transaction costs</b> are the costs of participating in markets. IT lowers them, so it can be worth dealing with other firms (outsourcing) instead of growing the number of employees.</p></div>
  <div><h4>Agency theory</h4><p>The firm is a web of contracts among self-interested parties that need supervision. <b>Agency costs</b> (the costs of managing and supervising) rise as the firm grows. IT can reduce them, so a firm can grow without adding supervision costs or employees.</p></div></div>
  {d_fl}
  <p class="small"><b>Flattening:</b> decisions move to lower levels, fewer managers are needed (IT speeds decisions and widens the span of control), and in postindustrial societies authority rests more on knowledge and competence than on formal position.</p>
  <h4>Why people resist new systems</h4>
  <p class="small">Systems affect access to a key resource, information, so they get tangled in organizational politics. They can change structure, culture, politics and work. The slides name four factors: <b>the nature of the innovation, the structure of the organization, the culture of the organization, and the tasks affected</b>.</p>
  <p class="small"><b>The Internet</b> raises the accessibility, storage and distribution of information and knowledge and can greatly lower transaction and agency costs (example: a large firm that puts its internal manuals on a website saves millions in distribution).</p>
  <p class="small"><b>Before designing a system, consider:</b> the environment; structure (hierarchy, specialization, routines, processes); culture and politics; type of organization and leadership style; the main interest groups affected and users' attitudes; and the tasks, decisions and processes the system will support.</p>

  <h3>Strategy: Porter's competitive forces</h3>
  <p class="small">Why do some firms lead their industry? Porter's model gives a general view of a firm, its competitors and its environment. Five forces shape its fate.</p>
  {d_pf}
  <div class="tbl-wrap"><table><thead><tr><th>Force</th><th>What the slides say</th></tr></thead><tbody>
  <tr><th>Traditional competitors</th><td>Rivals keep creating new products, services, efficiencies and switching costs.</td></tr>
  <tr><th>New market entrants</th><td>Some industries have high barriers to entry (computer chips). Newcomers have new equipment and younger workers but little brand recognition.</td></tr>
  <tr><th>Substitute products and services</th><td>What customers might use if your prices rise too high (iTunes as a substitute for CDs).</td></tr>
  <tr><th>Customers</th><td>Can they switch easily? Can they force firms to compete on price alone in a transparent marketplace?</td></tr>
  <tr><th>Suppliers</th><td>They have market power when the firm cannot raise its prices as fast as they raise theirs.</td></tr></tbody></table></div>
  <h4>Four generic strategies enabled by IT</h4>
  <div class="cards3">
    <div class="c"><h4>Low-cost leadership</h4><p>Produce at a lower price than competitors.</p><p class="eg">Walmart's efficient customer response system.</p></div>
    <div class="c"><h4>Product differentiation</h4><p>New products or services that greatly change customer convenience and experience. Mass customization; customer experience management.</p><p class="eg">The slide's example is written "Google Nike".</p></div>
    <div class="c"><h4>Focus on market niche</h4><p>Use information systems for a focused strategy on one niche; specialize.</p><p class="eg">Hilton Hotels' OnQ system.</p></div>
    <div class="c"><h4>Customer and supplier intimacy</h4><p>Build strong ties and loyalty, and raise switching costs.</p><p class="eg">Toyota, Amazon.</p></div>
  </div>
  <p class="small"><b>The Internet</b> threatens some industries (travel agencies, printed encyclopedias, media). The forces still apply but rivalry is stronger, universal standards allow new rivals and entrants, and there are new chances to build brands and loyal customers. <b>Smart products and the Internet of Things</b> (Internet-connected sensors in products such as fitness trackers) widen product differentiation, which can increase rivalry, raise switching costs, discourage new entrants and may reduce suppliers' power.</p>

  <h3>The value chain and beyond</h3>
  <p class="small">The <b>value chain model</b> sees the firm as a series of activities that add value. It shows where competitive strategies fit best. At each stage, ask how information systems can raise efficiency and strengthen customer and supplier intimacy, using <b>benchmarking</b> and industry best practices. Example systems below are from the slide figure.</p>
  <div class="vchain-wrap" tabindex="0" role="group" aria-label="Scrollable value chain table"><div class="vchain">
    <div class="lab" style="grid-row: span 4">Support activities</div>
    <div class="sup"><b>Administration and management</b>Electronic scheduling and messaging systems</div>
    <div class="sup"><b>Human resources</b>Workforce planning systems</div>
    <div class="sup"><b>Technology</b>Computer-aided design systems</div>
    <div class="sup"><b>Procurement</b>Computerized ordering systems</div>
    <div class="lab">Primary activities</div>
    <div class="pri"><b>Inbound logistics</b>Automated warehousing systems</div>
    <div class="pri"><b>Operations</b>Computer-controlled machining systems</div>
    <div class="pri"><b>Sales and marketing</b>Computerized ordering systems</div>
    <div class="pri"><b>Service</b>Equipment maintenance systems</div>
    <div class="pri"><b>Outbound logistics</b>Automated shipment scheduling systems</div>
  </div></div>
  <div class="two"><div><h4>Industry value chain</h4><p>The firm's chain is linked to the chains of its suppliers, distributors and customers.</p></div>
  <div><h4>Value web</h4><p>Independent firms that use tightly synchronized IT to coordinate their chains and make a product or service together. More customer-driven and less linear than a traditional chain.</p></div></div>
  <div class="cards3">
    <div class="c"><h4>Synergies</h4><p>The output of some units is the input of others, or organizations pool markets and expertise.</p><p class="eg">Bank of NY and JP Morgan Chase; Google buying YouTube.</p></div>
    <div class="c"><h4>Core competencies</h4><p>An activity where the firm is a world-class leader. Relies on knowledge and experience shared across business units.</p><p class="eg">Procter and Gamble's intranet and directory of experts.</p></div>
    <div class="c"><h4>Network economics</h4><p>The cost of adding a participant is almost zero, with much greater gain. The value of a community grows with its size, and so does software's value as its installed base grows. Contrast with the law of diminishing returns.</p></div>
    <div class="c"><h4>Virtual company</h4><p>Uses networks to ally with other firms and make and distribute products without being limited by organizational boundaries or locations.</p><p class="eg">Li and Fung manages garment production and shipping and outsources all the work to thousands of suppliers.</p></div>
    <div class="c"><h4>Business ecosystems</h4><p>Industry sets of firms providing related services and products. The slides name platforms (Microsoft, Facebook), keystone firms and niche firms, and say a firm can aim to be a profitable niche player in a larger ecosystem. My reading: keystone firms run the platform.</p></div>
  </div>

  <h3>The catch: strategic systems are hard to keep</h3>
  <div class="two"><div><h4>Sustaining the advantage</h4><p>Competitors can retaliate and copy strategic systems, and a system that was an advantage may become a tool for survival.</p></div>
  <div><h4>Aligning IT with business objectives</h4><p>Do a strategic systems analysis: look at the structure of the industry and at the firm's value chains.</p></div></div>
  <p class="small">The Week 3 deck ends here. There is no Week 4 deck in the folder yet.</p>
'''
w3_terms = terms([
 ('Organization (technical)', 'A formal social structure that processes resources from the environment to produce outputs.'),
 ('Organization (behavioral)', 'A balance of rights, privileges, obligations and responsibilities, kept through conflict and conflict resolution.'),
 ('Routines', 'Standard operating procedures: precise rules and practices for expected situations.'),
 ('Disruptive technology', 'A technology that brings sweeping change to businesses, industries or markets (PCs, smartphones, AI, the Internet).'),
 ('First mover / fast follower', 'First movers invent a disruptive technology; fast followers are big enough to profit from it.'),
 ('Transaction costs', 'The costs of participating in markets. IT lowers them.'),
 ('Agency costs', 'The costs of managing and supervising a firm, which rise as it grows. IT can lower them.'),
 ('Flattened organization', 'An organization with fewer layers of management because decisions move to lower levels.'),
 ('Competitive forces model (Porter)', 'Five forces: traditional competitors, new entrants, substitutes, customers, suppliers.'),
 ('Switching costs', 'My plain-words gloss (the slides do not define it): what it costs a customer to move to a competitor. The slides say strategies and smart products can raise them.'),
 ('Mass customization', 'Listed under product differentiation in the slides. The slides give no definition.'),
 ('Value chain', 'The firm as a series of activities (primary and support) that add value to a product or service.'),
 ('Value web', 'Independent firms using synchronized IT to make a product or service together.'),
 ('Synergy', 'Units or firms gain from using each other\'s outputs, markets or expertise.'),
 ('Core competency', 'An activity for which the firm is a world-class leader.'),
 ('Network economics', 'Near-zero cost of adding a participant; value grows with the size of the network.'),
 ('Virtual company', 'A firm that uses networks and partners to make and deliver products without organizational or physical limits.'),
 ('Keystone firm / niche firm', 'Both appear in the slides under business ecosystems without a definition. My reading: the keystone firm runs the platform and niche firms fill gaps around it.'),
])
w3_boss = qa('Name Porter\'s five forces and the four generic IS strategies, each with the slide example.',
 '''<p><b>Forces:</b> traditional competitors, new market entrants, substitute products and services, customers, suppliers.</p><p><b>Strategies:</b> low-cost leadership (Walmart), product differentiation (the slide says "Google Nike"), focus on a market niche (Hilton's OnQ), strengthening customer and supplier intimacy (Toyota, Amazon).</p>''', 1) + \
 qa('Explain transaction cost theory and agency theory in one line each, and say what IT does to each cost.',
 '''<ul><li><b>Transaction costs</b> are the costs of participating in markets. Firms try to cut them by growing (hiring, buying suppliers). IT <b>lowers</b> them, so working with other firms becomes worthwhile instead of growing headcount.</li>
 <li><b>Agency costs</b> are the costs of supervising the people the firm is a web of contracts with. They rise with size. IT <b>lowers</b> them, so a firm can grow without more supervision cost or employees.</li></ul>''', 2) + \
 qa('Why do organizations resist new information systems? List the four factors.',
 '''<p>Systems control access to information, so they are tied up in politics, and they can change structure, culture and work. The four factors named in the slides: the <b>nature of the innovation</b>, the <b>structure</b> of the organization, its <b>culture</b>, and the <b>tasks affected</b>.</p>''', 3) + \
 qa('How does a value web differ from a traditional value chain?',
 '''<p>A value chain is the firm\'s own series of value-adding activities, which can be linked to those of suppliers, distributors and customers (the industry value chain). A <b>value web</b> is a group of independent firms that use highly synchronized IT to coordinate their chains and make a product together. It is more customer-driven and less linear.</p>''', 4) + \
 qa('Why does network economics break the usual law of diminishing returns?',
 '''<p>In a network the marginal cost of adding a participant is almost zero while the gain is much greater, and the value of a community (or of software with a growing installed base) rises with its size. Traditional economics expects returns to shrink as you add more.</p>''', 5) + \
 qa('Walmart (slide case): what problems did it face and how did it respond?',
 '''<p><b>Problems:</b> opportunities from new technology, a large geographic footprint, powerful competition and high costs. <b>Solutions:</b> determine business strategy, design new products and services, integrate multiple lines of business, optimize the in-store experience, and use edge computing. Result: supercenter systems speed ordering and shipping, add in-store services, warehouse for third-party sellers and offer targeted online ads.</p>''', 6) + \
 qa('If a strategic system gives a firm an edge, why might the edge disappear, and what should the firm do about it?',
 '''<p>Competitors can retaliate and copy the system, and the system may end up as a tool for survival. The slides' advice is to align IT with business objectives by running a strategic systems analysis of the industry structure and the firm's value chains.</p>''', 7)

# ====================================================================== story, cheat sheet, flashcards
story = [
 (1, 'Technology alone does not pay', 'Firms spend heavily on IT to compete, but similar spending gives very different returns.',
  'Understand what an information system is (organization, management, technology) and pair the technology with complementary assets and a sociotechnical view.',
  'A firm is not one system. Different people and functions need different systems, and they must work together.'),
 (2, 'Linking the firm and its people', 'Work flows through processes that cross departments and levels, each with different decisions to make.',
  'Systems for each level (TPS, MIS, DSS, ESS), enterprise applications (ERP, SCM, CRM, KMS), and collaboration and social tools.',
  'New systems change structure, culture and politics, and rivals can buy the same systems. How do you get lasting value?'),
 (3, 'From systems to strategy', 'Organizations and IT shape each other, and competitors keep pressing on the firm.',
  'Fit systems to the organization; use IS against Porter\'s forces with four strategies; use the value chain, value web and network strategies.',
  'Competitors can copy a strategic system, so IT must stay aligned with business objectives. (The decks stop here.)'),
]
story_html = '<ol class="story">' + ''.join(
    f'<li class="w{n}"><a href="#week-{n}"><span class="wk">Week {n}</span><h3>{t}</h3>'
    f'<p><b>Problem</b>{p}</p><p><b>Fix</b>{s}</p><p class="but"><b>But then</b>{b}</p></a></li>' for n, t, p, s, b in story) + '</ol>'

numbers = [('~$3.8 trillion', 'global IT and IT services spending, 2019'), ('$160 billion', 'spent on management consulting and services'),
           ('~$3.6 trillion', 'worldwide e-commerce, 2019'), ('> 20% a year', 'growth of mobile retail e-commerce (almost $300 billion in 2020)'),
           ('$524 billion+', 'Walmart sales in 2019 (slide figure)'), ('6', 'strategic business objectives'),
           ('4', 'activities of an information system: input, processing, output, feedback'), ('3', 'dimensions: organization, management, technology'),
           ('4', 'system types: TPS, MIS, DSS, ESS'), ('4', 'enterprise applications: ERP, SCM, CRM, KMS'),
           ('6', 'steps to choose collaboration tools'), ('2 × 2', 'time/space matrix (time × place)'),
           ('5', 'competitive forces'), ('4', 'generic IS strategies'), ('5', 'Mintzberg structures'), ('4', 'factors of resistance to change')]
numbers_html = '<ul class="nums">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in numbers) + '</ul>'
traps = [
 '<b>Information technology</b> is hardware and software; an <b>information system</b> also includes the organization and management dimensions.',
 '<b>Data</b> is raw facts; <b>information</b> is data shaped to be useful.',
 'The <b>MIS</b> system type (routine reports for middle management) is not the same as <b>MIS</b> the field of study.',
 '<b>MIS</b> = routine questions; <b>DSS</b> = nonroutine questions; <b>ESS</b> = senior managers, judgment and outside events.',
 '<b>E-commerce</b> is a subset of <b>e-business</b>.',
 '<b>Intranet</b> = internal; <b>extranet</b> = authorized outside vendors and suppliers.',
 '<b>Complementary assets</b> are organizational, managerial and social. Buying technology without them gives weak returns.',
 'IT <b>lowers</b> transaction costs and agency costs. It does not raise them.',
 '<b>Value chain</b> = one firm\'s activities; <b>value web</b> = independent firms working together.',
 'Porter\'s five forces include <b>customers and suppliers</b>, not only competitors.',
 'A strategic system is <b>not permanent</b>: competitors can copy it.',
 'Slides give class-discussion questions with <b>no model answers</b>. Answers on this page are labelled "my own reading".',
]
traps_html = '<ul class="traps">' + ''.join(f'<li>{t}</li>' for t in traps) + '</ul>'
cards = [
 ('Six strategic business objectives', 'Operational excellence; new products, services and business models; customer and supplier intimacy; improved decision making; competitive advantage; survival.'),
 ('Data vs information', 'Data: streams of raw facts. Information: data shaped into a meaningful, useful form.'),
 ('Four activities of an information system', 'Input, processing, output, feedback.'),
 ('Three dimensions of an information system', 'Organization, management and technology.'),
 ('Why technology alone does not pay', 'Returns vary. You also need the right business model and complementary assets (organizational, managerial, social).'),
 ('Sociotechnical view', 'Jointly optimize the social and the technical system. Avoids a purely technological approach.'),
 ('What is a business process?', 'A logically related set of tasks that defines how a specific business task is done. It can be an asset or a liability.'),
 ('TPS', 'Records daily routine transactions for operational managers and staff: order entry, payroll, shipping.'),
 ('MIS (system type)', 'Routine reports on current performance for middle management, based on TPS data. Little analytic capability.'),
 ('DSS', 'Supports nonroutine decisions for middle management; model-driven or data-driven.'),
 ('ESS', 'For senior management: nonroutine decisions needing judgment; outside events plus MIS and DSS summaries; digital dashboard.'),
 ('Four enterprise applications', 'Enterprise systems (ERP), supply chain management, customer relationship management, knowledge management.'),
 ('SCM in one line', 'Shares information with suppliers and distributors to move the right product from source to consumer fast and cheaply.'),
 ('Intranet vs extranet', 'Intranet: internal network on Internet standards. Extranet: open only to authorized vendors and suppliers.'),
 ('E-business, e-commerce, e-government', 'E-business: digital technology runs the major processes. E-commerce: buying and selling online (a subset). E-government: services to citizens and businesses.'),
 ('Social business', 'Using internal and external social networks to engage employees, customers and suppliers; needs information transparency.'),
 ('Time/space matrix', 'Same or different time, same or different place: face-to-face, continuous task, remote interaction, communication + coordination.'),
 ('IT governance', 'Strategies, policies, decision rights and accountability for IT, and how the IS function is organized.'),
 ('Transaction costs and IT', 'Costs of participating in markets. IT lowers them, so firms can work with other firms instead of growing staff.'),
 ('Agency costs and IT', 'Costs of managing and supervising, rising with firm size. IT lowers them, so firms grow without more supervisors.'),
 ('Four factors of resistance', 'Nature of the innovation, structure of the organization, culture of the organization, tasks affected.'),
 ('Porter\'s five forces', 'Traditional competitors, new market entrants, substitute products, customers, suppliers.'),
 ('Four generic IS strategies', 'Low-cost leadership, product differentiation, focus on market niche, customer and supplier intimacy.'),
 ('Value chain: primary vs support', 'Primary: inbound logistics, operations, sales and marketing, service, outbound logistics. Support: administration, human resources, technology, procurement.'),
 ('Value web', 'Independent firms using synchronized IT to make a product together; more customer-driven, less linear.'),
 ('Network economics', 'Adding a participant costs almost nothing and value grows with network size, unlike diminishing returns.'),
 ('Challenges of strategic systems', 'Rivals can copy them, and IT must be aligned with business objectives by strategic systems analysis.'),
]
cards_html = '<div class="cards" id="cards">' + ''.join(
    f'<button class="card" type="button" aria-pressed="false"><span class="front">{q}</span><span class="back">{a}</span></button>' for q, a in cards) + '</div>'
N_CARDS = len(cards)

weeks_html = ''.join([
 week(1, '', 'Information systems in global business', 'Why firms invest in IT, and why the technology alone is not enough.',
      psn('Firms spend heavily on IT to compete globally, but similar spending gives very different returns.',
          'Understand an information system as organization + management + technology, add complementary assets, and take the sociotechnical view.',
          'A firm is not one system. Different people and functions need different systems that work together.'), MAPS[1], w1_vis, w1_terms, w1_boss, unit='Week'),
 week(2, '', 'Global e-business and collaboration', 'Systems for every level, linked across the firm, and people who work together.',
      psn('Work crosses departments and levels, and each group makes different decisions.',
          'TPS, MIS, DSS and ESS for each level; ERP, SCM, CRM and KMS to link the firm; collaboration and social business tools; an IS department to run it.',
          'Systems change structure, culture and politics, and rivals can buy the same tools. How is lasting value won?'), MAPS[2], w2_vis, w2_terms, w2_boss, unit='Week'),
 week(3, '', 'Information systems, organizations and strategy', 'How organizations and IT shape each other, and how IS builds competitive advantage.',
      psn('Organizations and IT influence each other, and competitors keep pressing on the firm.',
          'Fit systems to the organization, use IS against the five forces with four strategies, and use the value chain, value web, synergies, core competencies and networks.',
          'Competitors can copy a strategic system, so IT has to stay aligned with business objectives.'), MAPS[3], w3_vis, w3_terms, w3_boss, unit='Week'),
])
nav = '<a class="wx" href="#big-picture">Big picture</a>' + ''.join(f'<a class="w{n}" href="#week-{n}">Week {n}</a>' for n in range(1, 4)) + '<a class="wx" href="#cheat-sheet">Cheat sheet</a><a class="wx" href="#drill">Flashcards</a>'

CSS = (open(os.path.join(HERE, 'style.css')).read() + open(os.path.join(HERE, 'extra_cst.css')).read()
       + open(os.path.join(HERE, 'bigp.css')).read() + open(os.path.join(HERE, 'extra_cmt323.css')).read())
JS = open(os.path.join(HERE, 'script.js')).read()

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#060510">
<title>CMT323 Notes: Weeks 1 to 3</title>
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
  <p class="eyebrow">CMT323 · Test notes</p>
  <h1>Weeks 1 to 3, as one story</h1>
  <p class="lead">Every week exists because the one before it left a gap. Read it as <b>problem, solution, new problem</b>, and the facts hang together.</p>
  <nav class="jump" aria-label="Jump to a section">{nav}</nav>
</header>
<main>

<section id="big-picture" class="bigp wx">
  <h2 class="sec">Big picture: read this first</h2>
  <p class="headsup"><b>One question runs through all three weeks:</b> how does a business turn information technology into real value, and keep that value? Week 1 shows why firms invest and why the technology alone is not enough. Week 2 shows the systems and teamwork that carry the work. Week 3 shows how the organization and its rivals decide whether the investment wins.</p>
  <h3>The chain: each week fixes a gap the last one left</h3>
  <ol class="chain c3">
    <li class="w1"><span class="tn">Week 1</span><b>Information systems in global business</b><span class="kw">Six objectives, data to information, three dimensions, complementary assets, sociotechnical view</span><span class="bridge">But a firm is many people and functions, not one system &hellip;</span></li>
    <li class="w2"><span class="tn">Week 2</span><b>Global e-business and collaboration</b><span class="kw">Business processes, TPS, MIS, DSS, ESS, ERP, SCM, CRM, KMS, collaboration, IS department</span><span class="bridge">But systems change the organization, and rivals can buy them too &hellip;</span></li>
    <li class="w3"><span class="tn">Week 3</span><b>Information systems, organizations and strategy</b><span class="kw">Organizational features and impacts, five forces, four strategies, value chain and web, networks</span><span class="bridge">The decks stop here: advantage can be copied, so IT must stay aligned.</span></li>
  </ol>

  <h3>How Week 1 connects to Week 3</h3>
  <p class="small">Week 1 ends on the idea that value needs more than technology: the right business model and complementary assets (organizational, managerial and social). Week 3 spells out what those are. Culture, politics, structure and business processes decide whether a new system is accepted, and the five forces, value chain and network strategies decide whether it wins. The six objectives in Week 1 (especially competitive advantage and survival) are the aims; Week 3 is the toolkit for reaching them.</p>
  <div class="promise tbl-wrap"><table><thead><tr><th>Week 1 raised &hellip;</th><th>Answered in &hellip;</th></tr></thead><tbody>
    <tr><td>Organization, management and technology as the three dimensions</td><td><b>Week 2</b> (processes, levels, enterprise applications, the IS department). <b>Week 3</b> (organization features and impacts).</td></tr>
    <tr><td>Complementary assets: business model, efficient processes, teamwork</td><td><b>Week 2</b> (business processes, collaborative culture). <b>Week 3</b> (culture, politics, resistance).</td></tr>
    <tr><td>Improved decision making</td><td><b>Week 2</b> (MIS, DSS, ESS).</td></tr>
    <tr><td>Customer and supplier intimacy</td><td><b>Week 2</b> (CRM, SCM). <b>Week 3</b> (a generic strategy).</td></tr>
    <tr><td>Competitive advantage and survival</td><td><b>Week 3</b> (five forces, four strategies, value chain, challenges).</td></tr></tbody></table></div>

  <h3>Four threads that run through all three weeks</h3>
  <p class="small">These links are my own summary of the slides, to show how the weeks connect. They are not slide text.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Thread</th><th class="t1">Week 1</th><th class="t2">Week 2</th><th class="t3">Week 3</th></tr></thead><tbody>
    <tr><th>People and culture decide success</th><td>Complementary assets; sociotechnical view</td><td>Collaborative culture; Sharp case (culture and processes changed with the software)</td><td>Culture and politics; four factors of resistance</td></tr>
    <tr><th>Better decisions</th><td>Objective 4: real-time data instead of guesses</td><td>MIS, DSS and ESS serve different managers</td><td>Flattening: decisions move to lower levels</td></tr>
    <tr><th>Connecting with others</th><td>Customer and supplier intimacy</td><td>SCM, CRM, extranets, social business</td><td>Value web, virtual company, ecosystems</td></tr>
    <tr><th>The value of the firm</th><td>Business information value chain</td><td>Business processes as assets or liabilities</td><td>Value chain; competitive forces</td></tr></tbody></table></div>

  <h3>If you remember only five sentences</h3>
  <ol class="five">
    <li><b>Week 1:</b> firms invest in information systems for six strategic objectives, and technology only pays when paired with the right business model and complementary assets.</li>
    <li><b>Week 1:</b> an information system turns data into information through input, processing, output and feedback, and has organization, management and technology dimensions.</li>
    <li><b>Week 2:</b> business processes cross departments, so each management level gets its own system (TPS, MIS, DSS, ESS) and enterprise applications link the firm.</li>
    <li><b>Week 2:</b> collaboration and social business tools, chosen by time and place, only work with a collaborative culture.</li>
    <li><b>Week 3:</b> organizations and IT shape each other, and a firm uses IS against Porter's forces, but rivals can copy strategic systems.</li>
  </ol>
</section>

<section id="story" class="band">
  <h2 class="sec">Previously on CMT323</h2>
  <p class="small">Tap a card to jump to that week. Read the "But then" line, then the next card's "Problem": they are the same sentence.</p>
  {story_html}
</section>
{weeks_html}
<section id="cheat-sheet" class="band wx">
  <h2 class="sec">Cheat sheet</h2>
  <h3>Numbers to remember</h3>
  {numbers_html}
  <h3>Exam traps</h3>
  {traps_html}
</section>
<section id="drill" class="band wx">
  <h2 class="sec">Flashcards</h2>
  <p class="small">Tap a card to flip it. Say the answer out loud before you flip.</p>
  {cards_html}
</section>
</main>
<footer class="foot"><p>Built from the CMT323 lecture decks (Weeks 1 to 3, covering Chapters 1 to 3 of the course textbook). The lecture slides belong to their publisher and lecturers; this page is a student's own summary and the diagrams are redrawn, not copied. Items marked "my own reading" or "my own summary" are not from the slides.</p></footer>
<script>
{JS}
</script>
</body>
</html>'''
open(os.path.join(OUT, 'index.html'), 'w').write(PAGE)
print('cmt323 ok', len(PAGE), 'cards', N_CARDS)
