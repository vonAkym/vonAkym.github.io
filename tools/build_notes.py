#!/usr/bin/env python3
"""Builds the Weeks 1-5 study notes page (index.html) with inline SVG mind maps."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root (the folder that GitHub Pages serves)
import html, json

E = html.escape

# ---------------------------------------------------------------- mind map
def mindmap(center, left, right, label):
    VBW = 1160
    CX = VBW / 2
    LEAF_H, GAP, PAD = 27, 16, 34
    BR_OFF, DOT_OFF, TXT_OFF = 222, 342, 354

    def side_height(branches):
        return sum(len(l) * LEAF_H for _, l in branches) + GAP * (len(branches) - 1)

    H = max(side_height(left), side_height(right)) + 2 * PAD
    CY = H / 2
    parts = []

    def draw_side(branches, sign):
        sh = side_height(branches)
        y = (H - sh) / 2
        for blabel, leaves in branches:
            ys = [y + i * LEAF_H + LEAF_H / 2 for i in range(len(leaves))]
            by = sum(ys) / len(ys)
            bw = min(214, len(blabel) * 7.5 + 28)
            bx = CX + sign * BR_OFF
            inner = bx - sign * bw / 2
            outer = bx + sign * bw / 2
            cstart = CX + sign * 86
            mid = (cstart + inner) / 2
            parts.append(
                f'<path class="mm-link" d="M{cstart:.1f} {CY:.1f} C{mid:.1f} {CY:.1f} {mid:.1f} {by:.1f} {inner:.1f} {by:.1f}"/>')
            parts.append(
                f'<rect class="mm-branch" x="{bx - bw / 2:.1f}" y="{by - 16:.1f}" width="{bw:.1f}" height="32" rx="16"/>')
            parts.append(
                f'<text class="mm-btxt" x="{bx:.1f}" y="{by + 4.6:.1f}" text-anchor="middle">{E(blabel)}</text>')
            dx = CX + sign * DOT_OFF
            tx = CX + sign * TXT_OFF
            for ly, leaf in zip(ys, leaves):
                m = (outer + dx) / 2
                parts.append(
                    f'<path class="mm-link thin" d="M{outer:.1f} {by:.1f} C{m:.1f} {by:.1f} {m:.1f} {ly:.1f} {dx:.1f} {ly:.1f}"/>')
                parts.append(f'<circle class="mm-dot" cx="{dx:.1f}" cy="{ly:.1f}" r="4.2"/>')
                anchor = 'start' if sign > 0 else 'end'
                parts.append(
                    f'<text class="mm-leaf" x="{tx:.1f}" y="{ly + 4.4:.1f}" text-anchor="{anchor}">{E(leaf)}</text>')
            y += len(leaves) * LEAF_H + GAP

    draw_side(left, -1)
    draw_side(right, 1)
    parts.append(
        f'<rect class="mm-center" x="{CX - 86:.1f}" y="{CY - 32:.1f}" width="172" height="64" rx="22"/>')
    words = center.split(' ')
    if len(center) > 16 and len(words) > 1:
        half = len(words) // 2 or 1
        l1, l2 = ' '.join(words[:half]), ' '.join(words[half:])
        parts.append(f'<text class="mm-ctxt" x="{CX:.1f}" y="{CY - 4:.1f}" text-anchor="middle">{E(l1)}</text>')
        parts.append(f'<text class="mm-ctxt" x="{CX:.1f}" y="{CY + 16:.1f}" text-anchor="middle">{E(l2)}</text>')
    else:
        parts.append(f'<text class="mm-ctxt" x="{CX:.1f}" y="{CY + 5:.1f}" text-anchor="middle">{E(center)}</text>')
    svg = (f'<svg class="mm" viewBox="0 0 {VBW} {H:.0f}" role="img" aria-label="{E(label)}" '
           f'xmlns="http://www.w3.org/2000/svg">' + ''.join(parts) + '</svg>')
    return svg


MAPS = {
    1: mindmap('Web Engineering',
        [('Why it exists', ['Ad-hoc builds kept failing', '84% missed business goals', '79% late, 63% over budget', '53% lacked functionality']),
         ('The fix: 4 solutions', ['Clear goals and objectives', 'Systematic, phased development', 'Careful planning', 'Iterative, continuous auditing']),
         ('Definition (Murugesan)', ['Scientific principles', 'Engineering principles', 'Management principles', '+ systematic approaches'])],
        [('Web app vs software', ['Uses internet connections', 'W3C standards', 'Delivered via a browser', 'Stored on a remote server']),
         ('Key areas', ['Front-end: UI and interaction', 'Back-end: logic, DB, security', 'Software Eng + Hypermedia', 'Network Eng + Info Systems']),
         ('Web vs desktop: 8 traits', ['Network intensiveness', 'Concurrency, performance', 'Availability, security', 'Content, aesthetics, data-driven']),
         ('How the web grew', ['First web page: 1991', 'Doc-centric to Agentic AI', 'Web 1.0, 2.0, 3.0, 4.0'])],
        'Mind map of Week 1: why Web Engineering exists, its fix, its definition and what web apps are'),
    2: mindmap('Requirements Engineering',
        [('If it fails', ['Budget overruns', 'Delay in production', '"That\'s not what I asked for"']),
         ('What a requirement is', ['1 Solves a user\'s problem', '2 Satisfies a formal agreement', '3 Documented representation']),
         ('Web app requirements', ['Hardware: server, PCs', 'Network: cloud, protocol, security', 'Design: simple to high-end', 'Functionality: AI, transactional']),
         ('Stakeholders', ['Direct or indirect influence', 'Managers, customers, owners', 'Government, HR, advisors'])],
        [('4 core activities', ['1 Elucidation (elicit + negotiate)', '2 Documentation', '3 Validation + Verification', '4 Management']),
         ('Validate vs verify', ['Validation: the RIGHT thing?', 'Verification: done CORRECTLY?']),
         ('Why web is special', ['Requirements change constantly', 'Connectivity matters', 'Browser compatibility', 'Scalability']),
         ('Agile RE', ['Customer satisfaction', 'Early incremental delivery', 'Small, motivated teams', 'Delivery over analysis/design', 'Constant customer contact'])],
        'Mind map of Week 2: requirements, stakeholders, the four activities and Agile'),
    3: mindmap('Risk Management',
        [('What is a risk?', ['Possible negative event', 'Internal or external cause', 'Blocks the project goal', 'Can be mitigated']),
         ('Protects 3 things', ['Timeline', 'Budget', 'Application quality']),
         ('3 types of risk', ['Operational / Management', 'Technical', 'Project Scope'])],
        [('4-step process', ['1 Identification', '2 Analysis (score it)', '3 Planning', '4 Monitoring and control']),
         ('Risk score', ['Score = Probability x Impact', 'Each rated 1 to 5', 'Maximum score = 25']),
         ('Priority levels', ['1-4 Low: monitor', '5-9 Medium: plan, review', '10-16 High: act quickly', '17-25 Critical: escalate']),
         ('Response strategies', ['Avoid: eliminate it', 'Mitigate: reduce it', 'Transfer: share it', 'Accept: monitor it'])],
        'Mind map of Week 3: risks, the four-step process, scoring and response strategies'),
    4: mindmap('Modelling',
        [('Why model?', ['Requirements are all words', 'Words are ambiguous', 'Model = conceptual picture']),
         ('Process model', ['Communication, Planning', 'Modelling (Analysis + Design)', 'Construction, Deployment', 'Each increment delivered']),
         ('What to model', ['Users', 'Content', 'Interaction + Functionality', 'Configuration (Week 6)'])],
        [('User diagram', ['Who uses the app', 'Roles and access rights']),
         ('Class diagram', ['Static structure', 'Classes become DB tables', 'Attributes become columns', 'Relations become keys']),
         ('Use case diagram', ['What users can do', 'Actors + main functions']),
         ('Sequence diagram', ['Objects interact over time', 'One scenario, step by step']),
         ('Prototype', ['Rough UI + navigation links', 'Links inactive, will change'])],
        'Mind map of Week 4: why we model, what to model and the main diagrams'),
    5: mindmap('Web App Design',
        [('Design covers', ['Content, aesthetics', 'Architecture', 'Interface, navigation']),
         ('7 design goals', ['Simplicity, consistency', 'Identity, compatibility', 'Robustness, navigability', 'Visual appeal']),
         ('5 quality attributes', ['Usability, functionality', 'Reliability, efficiency', 'Maintainability']),
         ('Layout parts', ['Header, navigation menu', 'Content area, sidebar', 'Footer'])],
        [('Content design', ['Interaction design', 'Information design', 'Functional design']),
         ('3 questions', ['Where am I?', 'What can I do now?', 'Where have I been / going?']),
         ('13 principles', ['Guide: anticipation, track state', 'Talk: communication, readability', 'Easy: consistency, learnability', 'Fast: efficiency, latency']),
         ('Interface workflow', ['7 steps, each feeds the next', 'Starts from the analysis model', 'Ends with interaction procedure'])],
        'Mind map of Week 5: design goals, quality attributes, interaction design and interface workflow'),
}

# ---------------------------------------------------------------- helpers
def fig(src, alt, cap):
    return (f'<figure class="shot"><button class="zoom" type="button" aria-label="Enlarge: {E(alt)}">'
            f'<img src="img/{src}" alt="{E(alt)}" loading="lazy"></button>'
            f'<figcaption>{cap}</figcaption></figure>')

def terms(items):
    out = ['<dl class="terms">']
    for t, d in items:
        out.append(f'<div><dt>{t}</dt><dd>{d}</dd></div>')
    out.append('</dl>')
    return ''.join(out)

def psn(problem, solution, newp):
    return ('<div class="psn">'
            f'<div class="p"><b>Problem</b><p>{problem}</p></div><span class="arr" aria-hidden="true">&rarr;</span>'
            f'<div class="s"><b>Solution</b><p>{solution}</p></div><span class="arr" aria-hidden="true">&rarr;</span>'
            f'<div class="n"><b>New problem</b><p>{newp}</p></div></div>')

def qa(q, a, n):
    return (f'<details class="qa"><summary><span class="qn">{n}</span>{q}</summary>'
            f'<div class="ans">{a}</div></details>')

def week(n, title, accent_cls, blurb, psn_html, visuals, terms_html, boss):
    return f'''
<section id="week-{n}" class="week {accent_cls}">
  <div class="week-head"><span class="wk">Week {n}</span><h2>{title}</h2><p class="blurb">{blurb}</p></div>
  {psn_html}
  <h3>Mind map</h3>
  <div class="mm-wrap" tabindex="0" role="group" aria-label="Scrollable mind map"><p class="hint">Swipe sideways to see the whole map</p>{MAPS[n]}</div>
  {visuals}
  <h3>Terms to know</h3>
  {terms_html}
  <h3>Boss fight</h3>
  <p class="small">Tap a question to reveal the model answer. Try it in your head first.</p>
  {boss}
</section>'''

# ---------------------------------------------------------------- week 1
cats = [('Doc-centric', 'static page, company page, web radio'), ('Interactive', 'travel planning, news site'),
        ('Transactional', 'online banking, shopping, booking'), ('Workflow-based', 'e-government'),
        ('Portal-oriented', 'community or business portal'), ('Collaborative', 'e-learning, chatroom, Wikipedia'),
        ('Social Web', 'Netflix, weblogs, Facebook'), ('Ubiquitous', 'location-aware, FoodPanda'),
        ('Semantic Web', 'knowledge management, recommender'), ('Agentic AI', 'multitask, many APIs, autonomous workflow')]
ladder = '<ol class="ladder" aria-label="Categories of web applications from simplest to most complex">' + ''.join(
    f'<li style="--i:{i};--j:{i % 5}"><span class="n">{i + 1}</span><b>{a}</b><small>{b}</small></li>' for i, (a, b) in enumerate(cats)) + '</ol>'

gens = '''<div class="tbl-wrap"><table class="gen"><thead><tr><th></th><th>Web 1.0 <small>1990s</small></th><th>Web 2.0 <small>2000s</small></th><th>Web 3.0 <small>2010s to now</small></th><th>Web 4.0 <small>emerging</small></th></tr></thead><tbody>
<tr><th>Content</th><td>Static, read-only</td><td>Dynamic, user-generated</td><td>Contextual, personalised, semantic</td><td>Symbiotic: human-AI collaboration</td></tr>
<tr><th>Tech</th><td>HTML, CSS, CGI scripts</td><td>JavaScript, AJAX, CMS, APIs</td><td>Blockchain, AI, WebAssembly, GraphQL</td><td>AI agents acting on our behalf</td></tr>
<tr><th>Who controls data</th><td>Website owner</td><td>Big platforms (Facebook, Google)</td><td>Users, via decentralised systems</td><td>-</td></tr>
<tr><th>Main use</th><td>Information sharing</td><td>Social interaction, collaboration</td><td>Decentralisation, AI</td><td>-</td></tr></tbody></table></div>'''

w1_visual = f'''
  <h3>Pictures from your slides</h3>
  <div class="shots">
    {fig('w1-key-areas.jpg', 'Four fields feeding Web Engineering', 'Four fields feed Web Engineering: Software Engineering, Hypermedia, Network Engineering, Information System.')}
    {fig('w1-categories.jpg', 'Categories of web applications by complexity and year', 'Categories grow in complexity from 1991 to 2026, ending in Agentic AI.')}
    {fig('w1-generations.jpg', 'Web 1.0 to Web 4.0', 'Web 1.0 to 4.0: static, social, smart and decentralised, symbiotic.')}
  </div>
  <h3>The complexity staircase</h3>
  <p class="small">Read left to right, top to bottom: each step is a more complex kind of web app. <span class="note">Test tip: be able to place an example on the right step.</span></p>
  {ladder}
  <h3>Web 1.0 to 4.0 at a glance</h3>
  {gens}'''

w1_terms = terms([
    ('Software', 'Tells the computer what to do. Two types: <b>system software</b> and <b>application software</b>.'),
    ('Web application', 'Software that uses the internet, follows <b>W3C</b> standards, is delivered through a <b>browser</b> and usually lives on a <b>remote server</b>.'),
    ('Web Engineering', 'Extends Software Engineering to developing web apps (Software Development Life Cycle).'),
    ('Murugesan et al., 1999', 'Uses <b>scientific, engineering and management principles</b> and <b>systematic approaches</b> to develop, deploy and maintain high-quality web systems.'),
    ('Why it exists', 'Bring web development under control, <b>minimise risks</b>, and improve <b>quality, maintainability and scalability</b>.'),
    ('Before Web Engineering', '<b>Informality</b> (do your own thing), <b>urgency</b> (rapid decisions), <b>intuition</b> (feel your way), <b>art</b> (looks good).'),
    ('Cutter, 2000', '84% failed business objectives, 79% schedule delays, 63% budget overrun, 53% lacked functionality.'),
    ('Front-end', 'Interaction design, creating UI design, interface programming.'),
    ('Back-end', 'Logic programming, accessing the database, implementing security.'),
    ('Web vs desktop: 8 traits', 'Network intensiveness, concurrency, performance, availability, content, aesthetics, security, data-driven.'),
    ('First web page', 'Tim Berners-Lee, 6 August 1991.'),
])

w1_boss = qa('Pick two of informality, urgency, intuition, art. Why does each feel helpful, why does it cause failure, and which of the four solutions fixes it?',
 '''<div class="tbl-wrap"><table><thead><tr><th>Habit</th><th>Feels helpful</th><th>Causes failure</th><th>Fixed by</th></tr></thead><tbody>
<tr><td><b>Informality</b></td><td>Easy, "do your own thing"</td><td>No shared goals, so business objectives are missed (84%)</td><td>Clearly defined goals and objectives</td></tr>
<tr><td><b>Intuition</b></td><td>"Feel" your way through complexity</td><td>Gut decisions can't be scheduled or checked: delays, overruns</td><td>Careful planning + iterative auditing</td></tr>
<tr><td><b>Urgency</b></td><td>Fast decisions</td><td>Acting before thinking, steps skipped</td><td>Systematic, phased development</td></tr>
<tr><td><b>Art</b></td><td>Pleasing look</td><td>Looks good, but features missing (53%)</td><td>Clearly defined goals</td></tr></tbody></table></div>''', 1) + \
 qa('A team builds an online hotel-booking site "as fast as possible" with no plan. It is late, over budget and missing features. Which Cutter pitfalls, which category, and which two web-vs-desktop traits?',
 '''<ul><li><b>Pitfalls:</b> schedule delays (79%), budget overrun (63%), lack of functionality (53%), and probably failing business objectives (84%).</li>
<li><b>Category:</b> Transactional (a booking system).</li>
<li><b>Traits:</b> Security (payments, personal details) and Concurrency (many people booking the same room at once). Availability and data-driven also work.</li></ul>''', 2)

# ---------------------------------------------------------------- week 2
pipeline = '''<ol class="pipe" aria-label="The four core activities of Requirements Engineering">
<li style="--s:1"><b>Elucidation</b><span>Elicit and negotiate. Stakeholders talk and reach <b>consensus</b>.</span></li>
<li style="--s:2"><b>Documentation</b><span>Write the consensus in detail in a <b>requirement document</b>.</span></li>
<li style="--s:3"><b>Validation + Verification</b><span><b>Right thing?</b> (validation) and <b>done correctly?</b> (verification)</span></li>
<li style="--s:4"><b>Management</b><span>Requirements keep changing. Use methods and tools to absorb change.</span></li></ol>'''

w2_visual = f'''
  <h3>The four activities, in order</h3>
  {pipeline}
  <div class="callout trap"><b>Exam trap.</b> Week 1 blamed <i>informality</i>, yet Agile lists <i>informal methods</i>. The difference: Agile informality is held in check by constant customer communication and small, early deliveries. It is not "do your own thing".</div>
  <h3>Pictures from your slides</h3>
  <div class="shots">
    {fig('w2-tree-swing.jpg', 'Tree swing cartoon: every role understands the request differently', 'The tree-swing cartoon: customer, leader, analyst and programmer each hear a different request. What was really needed is a simple tire swing.')}
    {fig('w2-web-vs-desktop.jpg', 'Requirements for web app versus desktop app', 'Same goal, different focus. Web: connectivity, browser compatibility, scalability. Desktop: OS compatibility, local performance, installation.')}
  </div>'''

w2_terms = terms([
    ('Requirement (IEEE 610.12)', '(1) a condition or capability needed to <b>solve a user\'s problem</b>; (2) must be met to satisfy a <b>formal agreement</b>; (3) a <b>documented representation</b> of 1 and 2.'),
    ('Stakeholder', 'A person or organisation with <b>direct or indirect influence</b> on the requirements: managers, customers, HR, government, owners, financial advisors.'),
    ('Requirements Engineering', '<b>Eliciting, understanding, specifying and validating</b> customers\' and users\' requirements (Escalona, 2004). Systematic and disciplined.'),
    ('Elucidation', 'Elicitation and negotiation: a learning and consensus-building process through communication.'),
    ('Documentation', 'Turn the agreed consensus into a detailed requirement document.'),
    ('Validation', '"Did we specify the <b>right thing</b>?"'),
    ('Verification', '"Did we specify things <b>correctly</b>?"'),
    ('Requirements Management', 'Change is normal in web projects, so you need methods and tools to integrate new requirements and changes.'),
    ('Agile Web Engineering', 'Customer satisfaction, early incremental delivery, small motivated teams, informal methods, minimal work products, simplicity. <b>Delivery over analysis and design</b>, plus continuous communication.'),
    ('Why Agile', 'Business rules change fast, management wants instant results, and stakeholders keep changing their minds.'),
])

w2_boss = qa('Why do we need both validation and verification?',
 '''<p>They catch different mistakes. <b>Validation</b> checks you are building the <b>right thing</b> (matches real needs). <b>Verification</b> checks it is specified <b>correctly</b> (clear, consistent). A document can be perfectly written yet wanted by nobody, or wanted by everybody yet so vague it is misread. Either gap ends in "That's not what I asked for."</p>
<p class="hook">Verification = built the thing right. Validation = built the right thing.</p>''', 1) + \
 qa('A neat, unambiguous requirement document describes a social feed, but students only wanted timetable and assignment reminders. Which question passed? Which failed? Which activity should have caught it? Name two stakeholders.',
 '''<ul><li><b>Passed:</b> verification (clear and correct on paper).</li><li><b>Failed:</b> validation (wrong thing).</li>
<li><b>Activity:</b> Validation and Verification. Also Elucidation, since the real need was never properly elicited.</li>
<li><b>Stakeholders:</b> students/customers (want reminders), owners or management (may want engagement), university or government (rules, privacy), managers (budget, schedule).</li></ul>''', 2)

# ---------------------------------------------------------------- week 3
def heatmap():
    rows = []
    def lvl(s):
        return 'low' if s <= 4 else 'med' if s <= 9 else 'high' if s <= 16 else 'crit'
    names = {5: 'Very High', 4: 'High', 3: 'Medium', 2: 'Low', 1: 'Very Low'}
    out = ['<div class="heat-wrap"><div class="tbl-wrap"><table class="heat" aria-label="Risk score matrix, probability by impact"><thead><tr><th class="corner">P \\ I</th>']
    for i in range(1, 6):
        out.append(f'<th scope="col">Impact {i}</th>')
    out.append('</tr></thead><tbody>')
    for p in range(5, 0, -1):
        out.append(f'<tr><th scope="row">P {p} <small>{names[p]}</small></th>')
        for i in range(1, 6):
            s = p * i
            mark = ' key' if (p, i) == (4, 5) else ''
            extra = '<small>key developer leaves</small>' if (p, i) == (4, 5) else ''
            out.append(f'<td class="{lvl(s)}{mark}"><b>{s}</b>{extra}</td>')
        out.append('</tr>')
    out.append('</tbody></table></div>')
    out.append('''<ul class="legend"><li><i class="sw low"></i><span><b>1-4 Low</b> monitor, minimal action</span></li>
<li><i class="sw med"></i><span><b>5-9 Medium</b> plan mitigation, review regularly</span></li>
<li><i class="sw high"></i><span><b>10-16 High</b> act quickly, assign ownership</span></li>
<li><i class="sw crit"></i><span><b>17-25 Critical</b> immediate response, escalate to project manager</span></li></ul></div>''')
    return ''.join(out)

flow5 = '''<ol class="flow5" aria-label="Risk planning, from risk to action">
<li><b>Prioritise</b><span>Use the score. High and Critical first.</span></li>
<li><b>Define response</b><span>Avoid, Mitigate, Transfer or Accept.</span></li>
<li><b>Plan actions</b><span>Specific steps, owner, target date, resources.</span></li>
<li><b>Implement</b><span>Fit into schedule, budget and resources.</span></li>
<li><b>Monitor + review</b><span>Check it worked, update the score, act again.</span></li></ol>'''

types3 = '''<div class="cards3">
<div class="c"><h4>Operational or Management</h4><p>Planning, coordination, people, resources, decisions.</p><p class="eg">Manpower shortage, poor team communication, delayed approvals</p><p class="imp">Hits timeline, budget, team productivity</p></div>
<div class="c"><h4>Technical</h4><p>Technology, dev tools, integration, system performance.</p><p class="eg">Bugs, tool or platform incompatibility, server failure, security holes</p><p class="imp">Hits quality, reliability, security</p></div>
<div class="c"><h4>Project Scope</h4><p>Requirements or deliverables unclear or constantly changing.</p><p class="eg">Changing user requirements, unclear objectives, extra features</p><p class="imp">Hits scope, schedule, cost, client expectations</p></div></div>
<p class="small"><b>Why classify?</b> Shows the source of the risk, makes planning easier, improves monitoring.</p>'''

w3_visual = f'''
  <h3>The risk score board</h3>
  <p class="small"><b>Risk score = Probability x Impact</b>, each rated 1 to 5. Find the cell, read the level.</p>
  {heatmap()}
  <h3>From risk to action</h3>
  {flow5}
  <div class="strat">
    <div><b>Avoid</b><span>eliminate the risk</span></div><div><b>Mitigate</b><span>reduce likelihood or impact</span></div>
    <div><b>Transfer</b><span>share the risk</span></div><div><b>Accept</b><span>monitor the risk</span></div></div>
  <div class="callout trap"><b>Exam traps.</b> Probability means <i>how likely</i>, not <i>when</i>. And <b>Transfer</b> (share it, e.g. a vendor or insurance) is not <b>Accept</b> (do nothing but watch).</div>
  <h3>Three types of risk</h3>
  {types3}
  <h3>Pictures from your slides</h3>
  <div class="shots">
    {fig('w3-risk-process.jpg', 'Risk score priority levels and the five-step planning flow', 'The slide version of the score table and the risk planning flow.')}
    {fig('w3-risk-types.jpg', 'Operational, Technical and Project Scope risks', 'The slide version of the three risk types.')}
  </div>'''

w3_terms = terms([
    ('Risk', 'Possibility of any negative occurrence from <b>external or internal</b> factors that can prevent the project goal. All projects have risks. Can be mitigated by preventive action.'),
    ('Risk management', 'Minimise risks and prevent failure, keeping <b>timeline, budget and application quality</b> safe.'),
    ('1 Risk identification', 'Find the likely or high-impact risks (e.g. manpower shortage, delay in modelling, extra storage).'),
    ('2 Risk analysis', 'Judge severity by assigning an <b>impact factor</b>; the project manager prioritises.'),
    ('3 Risk planning', 'Plan actions, starting with the highest-impact risk.'),
    ('4 Monitoring and control', 'Run the project, keep assessing risks, foresee new ones.'),
    ('Risk score', 'Probability x Impact. Example: key developer leaves, 4 x 5 = 20, <b>Critical</b>.'),
    ('Avoid / Mitigate / Transfer / Accept', 'Eliminate / reduce / share / monitor.'),
])

w3_boss = qa('Why does the score multiply probability by impact instead of using impact alone?',
 '''<p>Impact alone ranks a rare disaster (say, Malaysia going to war) above likely everyday problems and wastes planning effort. Probability asks <b>how likely</b> (not when), impact asks <b>how bad</b>. Together they show where effort pays off: a 1 x 5 risk scores 5 (Medium), far below a 5 x 3 risk at 15 (High).</p>''', 1) + \
 qa('Score, level and type: A) client keeps adding features (P5, I3). B) server crashes at launch (P2, I5). C) manager slow to approve the design (P2, I2). Then pick a strategy for A.',
 '''<div class="tbl-wrap"><table><thead><tr><th>Risk</th><th>Score</th><th>Level</th><th>Type</th></tr></thead><tbody>
<tr><td>A client adds features</td><td>5 x 3 = <b>15</b></td><td>High</td><td>Project Scope</td></tr>
<tr><td>B server crash</td><td>2 x 5 = <b>10</b></td><td>High</td><td>Technical</td></tr>
<tr><td>C slow approval</td><td>2 x 2 = <b>4</b></td><td>Low</td><td>Operational / Management</td></tr></tbody></table></div>
<p><b>Strategy for A: Mitigate.</b> Sign off requirements, treat new features as change requests, deliver in small increments, name an owner and a date.</p>''', 2)

# ---------------------------------------------------------------- week 4
which = '''<div class="tbl-wrap"><table class="which"><thead><tr><th>Question</th><th>Diagram</th><th>One-line job</th></tr></thead><tbody>
<tr><td>Who uses it?</td><td><b>User diagram</b></td><td>Identify users, roles and access rights</td></tr>
<tr><td>What is it made of?</td><td><b>Class diagram</b></td><td>Static structure: classes, attributes, operations, relationships</td></tr>
<tr><td>What can users do?</td><td><b>Use case diagram</b></td><td>Actors and the main functions</td></tr>
<tr><td>What happens, in what order?</td><td><b>Sequence diagram</b></td><td>How objects interact over time in one scenario</td></tr>
<tr><td>What will it look like?</td><td><b>Prototype</b></td><td>Rough interface: major links and screen layout</td></tr></tbody></table></div>'''

dbmap = '''<div class="dbmap" aria-label="Class diagram to database mapping">
<div><b>Class</b><span>Order</span></div><i aria-hidden="true">&rarr;</i><div><b>Table</b><span>orders</span></div>
<div><b>Attribute</b><span>orderDate</span></div><i aria-hidden="true">&rarr;</i><div><b>Column</b><span>order_date</span></div>
<div><b>Relationship</b><span>Order refers to User</span></div><i aria-hidden="true">&rarr;</i><div><b>Key</b><span>primary key + foreign key</span></div></div>'''

uc = '''<p class="small">The bookstore use case slide also shows <b>&laquo;include&raquo;</b> (checkout always includes place order and payment) and <b>&laquo;extend&raquo;</b> (optional add-ons such as writing a review). Standard meaning, not spelled out on the slide.</p>'''

w4_visual = f'''
  <h3>Which diagram answers which question</h3>
  {which}
  <h3>Class diagram to database</h3>
  {dbmap}
  <h3>Pictures from your slides (tap to enlarge)</h3>
  <div class="shots">
    {fig('w4-process-model.jpg', 'Web Engineering process model', 'The process model: Communication, Planning, Modelling (Analysis and Design), Construction, Deployment. Each increment starts at the beginning and is delivered at Deployment.')}
    {fig('w4-class-diagram.jpg', 'Online bookstore class diagram', 'Class diagram (bookstore): class name, attributes, operations, relations, composition, derived attribute, invariant.')}
    {fig('w4-use-case.jpg', 'Online bookstore use case diagram', 'Use case diagram: Visitor, Customer, Administrator and Payment Gateway, with include and extend links.')}
    {fig('w4-sequence.jpg', 'Place order sequence diagram', 'Sequence diagram: Place Order, with an alt box for payment successful versus payment failed.')}
  </div>
  {uc}'''

w4_terms = terms([
    ('Modelling', 'A <b>conceptual illustration</b> of the web app using diagrams, graphics, text and flowcharts to show content, function, architecture, components, interfaces, navigation and aesthetics.'),
    ('Why model', 'Requirements and proposals are written in <b>words</b>, and words are <b>ambiguous</b> (the watering-can example).'),
    ('Web Engineering process model', 'Communication, Planning, Modelling (Analysis + Design), Construction, Deployment, repeated per increment.'),
    ('What to model (U-C-I-F-C)', '<b>U</b>sers, <b>C</b>ontent, <b>I</b>nteraction, <b>F</b>unctionality, <b>C</b>onfiguration.'),
    ('Modelling interaction', 'The "conversation" between user and app. Tools: use cases, sequence diagrams, state diagrams, UI prototypes, navigation model.'),
    ('Modelling content', 'Text, graphics, images, video and audio.'),
    ('Prototype', 'Shows UI, content, interaction and aesthetic. Links are not active but show how it works, and it changes before the final interface. Users get what they want <b>sooner</b>.'),
    ('Configuration', 'Server, hardware, OS, where the web server lives (<b>cloud or intranet</b>), server-database interoperability, client browsers (iOS, Windows, Android). Only a think-tank now; <b>Week 6</b>.'),
])

w4_boss = qa('"We have a use case diagram, so a sequence diagram is a waste." Respond.',
 '''<p>A <b>use case diagram</b> says <i>what</i> each user can do (actors and functions), with no order or timing. A <b>sequence diagram</b> shows <i>how</i> one process happens step by step over time, including branches like payment success or failure. A use case says "the customer can place an order"; only the sequence diagram shows what the system does to make it happen.</p>''', 1) + \
 qa('Food-ordering app (customers, restaurant owners, admin). Which diagram for roles? Database design, and how does it map? Payment flow over time? Which thing to model waits until Week 6?',
 '''<ul><li><b>Roles:</b> user diagram.</li><li><b>Database:</b> class diagram. Classes become tables, attributes become columns, relationships become primary and foreign keys.</li>
<li><b>Payment flow:</b> sequence diagram.</li><li><b>Week 6:</b> Configuration.</li></ul>''', 2)

# ---------------------------------------------------------------- week 5
goals = [('Simplicity', 'All things in moderation. Avoid feature-bloat.'), ('Consistency', 'Same look, templates and navigation behaviour everywhere.'),
         ('Identity', 'Aesthetic, interface and navigation suit the application domain.'), ('Robustness', 'Relevant content and functions the user can rely on.'),
         ('Navigability', 'Users can move around without hunting for links or instructions.'), ('Visual Appeal', 'Look and feel, layout, colour, balance of text and media.'),
         ('Compatibility', 'Works across hardware, connections, operating systems and browsers.')]
goals_html = '<ul class="goals">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in goals) + '</ul>'

quality = [('Usability', 'site understandability, feedback and help, interface and aesthetics'), ('Functionality', 'searching, navigation, domain features'),
           ('Reliability', 'correct link processing, error recovery, input validation'), ('Efficiency', 'response time, page and graphics speed'),
           ('Maintainability', 'ease of correction, adaptability, extensibility')]
quality_html = '<ul class="quality">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in quality) + '</ul>'

groups = [('Guide the user', [('Anticipation', 'anticipate the next move'), ('Controlled Autonomy', 'free movement, but follow navigation conventions'),
                              ('Visible Navigation', 'the illusion of staying in one place'), ('Track State', 'log off and resume where you left')]),
          ('Talk to the user', [('Communication', 'show the status of what they started'), ('Readability', 'readable by young and old'),
                                ('Metaphor', 'familiar analogy, if appropriate')]),
          ('Keep it easy', [('Consistency', 'same controls, icons, colours, layout'), ('Learnability', 'little to learn, little to relearn'),
                            ('Focus', 'stay on the current task'), ('Flexibility', 'direct paths and free exploring')]),
          ('Save time', [('Efficiency', 'optimise the USER\'s work, not the developer\'s'), ('Latency Reduction', 'multitask so users need not wait')])]
principles = '<div class="groups">' + ''.join(
    f'<div class="g"><h4>{g}</h4><ul>' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in items) + '</ul></div>' for g, items in groups) + '</div>'

wf = ['Review user characteristics, tasks and use cases from the analysis model; refine.', 'Make a rough design prototype of the interface layout.',
      'Define the user tasks tied to each action.', 'Make screen images for each interface action.', 'Refine layout and screens using aesthetic design input.',
      'Identify the user interface objects needed.', 'Write a procedural representation of the user\'s interaction.']
workflow = '<ol class="steps7">' + ''.join(f'<li>{s}</li>' for s in wf) + '</ol>'

w5_visual = f'''
  <h3>7 design goals</h3>
  {goals_html}
  <h3>5 quality attributes</h3>
  {quality_html}
  <h3>Interaction design: 3 questions, 13 principles</h3>
  <ol class="three"><li><b>Where am I?</b><span>Show which part of the app and where in the content hierarchy.</span></li>
  <li><b>What can I do now?</b><span>Show available functions, live links, relevant content.</span></li>
  <li><b>Where have I been, and where am I going?</b><span>Give a "map" of past and possible paths.</span></li></ol>
  <p class="small">The slide lists 13 distinct principles (Communication appears twice). The four groups below are a memory aid, not slide wording.</p>
  {principles}
  <div class="callout trap"><b>Exam trap.</b> The Efficiency principle is about the <b>user's</b> efficiency, not the web engineer's or the client-server environment's.</div>
  <h3>Interface design workflow</h3>
  <p class="small">Each step uses the result of the one before. Step 1 reuses Week 4's models, step 2 reuses the prototype idea.</p>
  {workflow}
  <h3>Pictures from your slides</h3>
  <div class="shots">
    {fig('w5-quality.jpg', 'Web application quality attributes', 'Quality attributes and what each covers.')}
    {fig('w5-three-questions.jpg', 'Three interaction design questions', 'The three questions interaction design must answer.')}
    {fig('w5-campushub-layout.jpg', 'CampusHub interface layout', 'Sample layout: header, navigation menu, content area, sidebar and footer.')}
  </div>'''

w5_terms = terms([
    ('Web app design covers', 'Content, aesthetics, architecture, interface, navigation.'),
    ('Content design', 'Interaction design, information design, functional design.'),
    ('Interface layout parts', '<b>Header</b> (name, logo, search, profile), <b>navigation menu</b>, <b>content area</b>, <b>sidebar</b> (secondary content), <b>footer</b> (secondary links, contact).'),
    ('Next up', 'Configuration: where the app runs (Week 6, not in your slides).'),
])

w5_boss = qa('Interaction design must answer three questions. What goes wrong for the user if each is not answered?',
 '''<ul><li><b>Where am I?</b> Users feel lost and can't tell which part of the app they are in.</li>
<li><b>What can I do now?</b> They don't know which functions or links are available, so they stall or guess.</li>
<li><b>Where have I been / where am I going?</b> They can't retrace steps or plan a path, so navigation feels random.</li></ul>''', 1) + \
 qa('Student portal: (a) a big upload freezes the page with no message, (b) logging out loses half-filled form data, (c) menu icons differ on every page. Name the principle and a fix for each.',
 '''<div class="tbl-wrap"><table><thead><tr><th>Problem</th><th>Principle</th><th>Fix</th></tr></thead><tbody>
<tr><td>(a) Freeze, no message</td><td><b>Latency Reduction</b> and <b>Communication</b></td><td>Let the user keep working while it uploads; show progress and status</td></tr>
<tr><td>(b) Lost form data</td><td><b>Track State</b></td><td>Save the interaction state so they can return and resume</td></tr>
<tr><td>(c) Icons differ</td><td><b>Consistency</b></td><td>Use the same controls, icons, colour and layout on every page</td></tr></tbody></table></div>''', 2)

# ---------------------------------------------------------------- story cards, cheat sheet, flashcards
story = [
 (1, 'Why Web Engineering exists', 'Web apps were built by informality, urgency, intuition and art, and most projects failed.',
  'Web Engineering: systematic, phased, planned, audited development.', 'It says how to work, not what to build.'),
 (2, 'Know what to build', 'The wrong thing gets built: "That\'s not what I asked for."',
  'Requirements Engineering: elicit, document, validate and verify, manage.', 'Right requirements can still be derailed by events.'),
 (3, 'Protect the plan', 'Staff leave, tech fails, scope creeps.',
  'Risk management: identify, analyse (P x I), plan, monitor.', 'Everything is still written in words, and words are ambiguous.'),
 (4, 'Draw it so nobody misreads it', 'Words are ambiguous (the watering can).',
  'Models: user, class, use case, sequence, prototype.', 'Models show structure, not how it feels to use.'),
 (5, 'Make it usable', 'A correct model can still be a confusing website.',
  'Design goals, quality attributes, interaction principles, interface workflow.', 'It needs somewhere to run: Week 6 configuration.'),
]
story_html = '<ol class="story">' + ''.join(
    f'<li class="w{n}"><a href="#week-{n}"><span class="wk">Week {n}</span><h3>{t}</h3>'
    f'<p><b>Problem</b>{p}</p><p><b>Fix</b>{s}</p><p class="but"><b>But then</b>{b}</p></a></li>' for n, t, p, s, b in story) + '</ol>'

numbers = [('84 · 79 · 63 · 53', 'Cutter: missed objectives, delays, overrun, missing features (%)'), ('4', 'solutions of Web Engineering'), ('3', 'parts of IEEE 610.12 requirement'),
           ('4', 'RE activities: elucidate, document, validate and verify, manage'), ('1-4 · 5-9 · 10-16 · 17-25', 'Low · Medium · High · Critical'), ('4', 'risk process steps'),
           ('4', 'strategies: avoid, mitigate, transfer, accept'), ('5', 'things to model: U-C-I-F-C'), ('7', 'design goals'), ('5', 'quality attributes'),
           ('3', 'interaction design questions'), ('7', 'interface workflow steps')]
numbers_html = '<ul class="nums">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in numbers) + '</ul>'

traps = [
 '<b>Agile "informal methods"</b> vs Week 1 "informality": Agile is controlled by constant customer contact and small increments.',
 '<b>Validation</b> = right thing. <b>Verification</b> = done correctly.',
 '<b>Probability</b> is how likely, not when.',
 '<b>Transfer</b> = share the risk. <b>Accept</b> = monitor it.',
 '<b>Use case</b> = what users can do. <b>Sequence</b> = what happens, in order. <b>Class</b> = what it is made of.',
 '<b>Configuration</b> is only a think-tank in Week 4; the detail is Week 6.',
 '<b>Efficiency</b> principle = the user\'s efficiency.',
 'The principles slide shows <b>Communication</b> twice; count 13 distinct principles.',
]
traps_html = '<ul class="traps">' + ''.join(f'<li>{t}</li>' for t in traps) + '</ul>'

cards = [
 ('Cutter (2000) failure numbers', '84% failed business objectives<br>79% schedule delays<br>63% budget overrun<br>53% lack of functionality'),
 ('Web Engineering solves failure with...', 'Clearly defined goals and objectives. Systematic, phased development. Careful planning. Iterative and continuous auditing.'),
 ('Murugesan 1999 definition', 'Scientific, engineering and management principles plus systematic approaches to develop, deploy and maintain high-quality web systems.'),
 ('IEEE 610.12: a requirement is...', '1) a condition or capability that solves a user\'s problem; 2) must be met for a formal agreement; 3) a documented representation of both.'),
 ('4 core activities of RE', 'Elucidation, Documentation, Validation and Verification, Management.'),
 ('Validation vs verification', 'Validation: the RIGHT thing? Verification: done CORRECTLY?'),
 ('Risk score and levels', 'Score = Probability x Impact (1-5 each). 1-4 Low, 5-9 Medium, 10-16 High, 17-25 Critical.'),
 ('4 risk response strategies', 'Avoid (eliminate), Mitigate (reduce), Transfer (share), Accept (monitor).'),
 ('3 types of risk', 'Operational or Management, Technical, Project Scope.'),
 ('4 steps of risk management', 'Identification, Analysis, Planning, Monitoring and Control.'),
 ('5 things to model', 'Users, Content, Interaction, Functionality, Configuration (U-C-I-F-C).'),
 ('Class diagram to database', 'Classes become tables, attributes become columns, relationships become primary and foreign keys.'),
 ('7 design goals', 'Simplicity, Consistency, Identity, Robustness, Navigability, Visual Appeal, Compatibility.'),
 ('5 quality attributes', 'Usability, Functionality, Reliability, Efficiency, Maintainability.'),
 ('3 interaction design questions', 'Where am I? What can I do now? Where have I been / where am I going?'),
]
cards_html = '<div class="cards" id="cards">' + ''.join(
    f'<button class="card" type="button" aria-pressed="false"><span class="front">{q}</span><span class="back">{a}</span></button>' for q, a in cards) + '</div>'

# ---------------------------------------------------------------- page
CSS = open(os.path.join(HERE, 'style.css')).read() + open(os.path.join(HERE, 'bigp.css')).read()
JS = open(os.path.join(HERE, 'script.js')).read()

weeks_html = ''.join([
    week(1, 'Why Web Engineering exists', 'w1', 'Chaos meets discipline.',
         psn('Ad-hoc, intuition-driven web projects fail: 84% miss business goals.', 'Web Engineering: scientific, engineering and management principles with systematic, phased, audited development.', 'A discipline is not a plan. What exactly should we build?'),
         w1_visual, w1_terms, w1_boss),
    week(2, 'Requirements Engineering', 'w2', 'Agree on the right thing before building it.',
         psn('The wrong thing gets built: "That\'s not what I asked for."', 'Elicit and negotiate, document, validate and verify, manage change. Use Agile because change is constant.', 'Even right requirements can be derailed by people, technology and scope.'),
         w2_visual, w2_terms, w2_boss),
    week(3, 'Managing Risks', 'w3', 'Find what could go wrong, rank it, prepare.',
         psn('Staff leave, tech fails, scope creeps. Plans get derailed.', 'Identify, analyse (Probability x Impact), plan a response, monitor.', 'It is all still in words, and words are ambiguous.'),
         w3_visual, w3_terms, w3_boss),
    week(4, 'Modelling Web Applications', 'w4', 'Replace ambiguous words with shared pictures.',
         psn('A watering can "that fills 1 litre and has sprinkles" can be drawn a hundred ways.', 'Model users, content, interaction, functionality, configuration with user, class, use case, sequence diagrams and a prototype.', 'Models show what the system is and does, not how it feels to use.'),
         w4_visual, w4_terms, w4_boss),
    week(5, 'Web Application Design', 'w5', 'Turn a correct model into something people can use.',
         psn('A correct model can still be a confusing, inconsistent website.', 'Design goals, quality attributes, interaction principles and an interface design workflow.', 'It still needs somewhere to run: configuration (Week 6).'),
         w5_visual, w5_terms, w5_boss),
])

nav = '<a class="wx" href="#big-picture">Big picture</a>' + ''.join(f'<a class="w{n}" href="#week-{n}">Week {n}</a>' for n in range(1, 6)) + '<a class="wx" href="#cheat-sheet">Cheat sheet</a><a class="wx" href="#drill">Flashcards</a>'

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CMT322 Web Engineering Notes</title>
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
  <img class="subj" src="../assets/subjects/cmt322.svg" width="96" height="96" alt="">
  <p class="eyebrow">Web Engineering and Technologies · Test notes</p>
  <h1>Weeks 1 to 5, as one story</h1>
  <p class="lead">Every week exists because the week before it wasn't enough. Read it as <b>problem, solution, new problem</b>, and the facts hang together.</p>
  <nav class="jump" aria-label="Jump to a section">{nav}</nav>
</header>
<main>

<section id="big-picture" class="bigp wx">
  <h2 class="sec">Big picture: read this first</h2>
  <p class="headsup"><b>One question runs through the whole subject:</b> how do you build a web application so that it does not fail? Week 1 shows why web projects fail and what Web Engineering promises. Weeks 2 and 3 decide what to build and protect the plan. Weeks 4 and 5 turn the plan into models and then into a design people can use.</p>
  <h3>The chain: each week fixes a gap the last one left</h3>
  <ol class="chain">
    <li class="w1"><span class="tn">Week 1</span><b>Why Web Engineering exists</b><span class="kw">Ad-hoc builds fail; the four solutions; web vs desktop; front-end and back-end</span><span class="bridge">But a discipline does not say what to build &hellip;</span></li>
    <li class="w2"><span class="tn">Week 2</span><b>Requirements Engineering</b><span class="kw">Stakeholders; elicit, document, validate and verify, manage; Agile</span><span class="bridge">But even right requirements can be derailed &hellip;</span></li>
    <li class="w3"><span class="tn">Week 3</span><b>Managing Risks</b><span class="kw">Identify, analyse (P x I), plan, monitor; avoid, mitigate, transfer, accept</span><span class="bridge">But it is all still written in words &hellip;</span></li>
    <li class="w4"><span class="tn">Week 4</span><b>Modelling</b><span class="kw">User, class, use case and sequence diagrams; prototype; process model</span><span class="bridge">But models do not show how it feels to use &hellip;</span></li>
    <li class="w5"><span class="tn">Week 5</span><b>Web application design</b><span class="kw">Design goals, quality attributes, interaction design, interface workflow</span><span class="bridge">Next: configuration, where it runs (Week 6)</span></li>
  </ol>

  <h3>How Week 1 connects to Week 5</h3>
  <p class="small">Week 1 promised to fix four failures (84% missed business objectives, 79% late, 63% over budget, 53% missing features) and named the front-end skills: <b>interaction design, UI design and interface programming</b>. It also compared web apps with desktop apps on traits such as content, aesthetics, security and performance. Week 5 is where those front-end skills become concrete rules: <b>design goals</b>, <b>quality attributes</b> (including maintainability, which Week 1 named as an aim), <b>interaction design</b> and a seven-step <b>interface workflow</b> that starts from Week 4's models.</p>
  <div class="promise tbl-wrap"><table><thead><tr><th>Week 1 raised &hellip;</th><th>Answered in &hellip;</th></tr></thead><tbody>
    <tr><td>Failure to meet business objectives (84%)</td><td><b>Week 2</b>: agree the requirements with stakeholders and validate them.</td></tr>
    <tr><td>Schedule delays (79%) and budget overrun (63%)</td><td><b>Week 3</b>: risk management protects timeline, budget and quality.</td></tr>
    <tr><td>Lack of functionality (53%)</td><td><b>Week 2</b> (functional requirements), <b>Week 4</b> (model the functionality), <b>Week 5</b> (the functionality quality attribute).</td></tr>
    <tr><td>Systematic, phased development</td><td><b>Week 4</b>: the Web Engineering process model, one increment at a time.</td></tr>
    <tr><td>Careful planning</td><td><b>Week 3</b>: risk planning, from risk to action.</td></tr>
    <tr><td>Iterative and continuous auditing</td><td><b>Week 2</b> (requirements management, Agile), <b>Week 4</b> (increments, prototype), <b>Week 5</b> (refine layout and screens).</td></tr>
    <tr><td>Front-end skills: interaction design, UI design</td><td><b>Week 5</b>: interaction design principles and the interface design workflow.</td></tr>
    <tr><td>Quality, maintainability, scalability</td><td><b>Week 5</b> (quality attributes) and <b>Week 3</b> (protect the quality of the application).</td></tr></tbody></table></div>

  <h3>Where the weeks sit in the process model</h3>
  <p class="small">Week 4 shows the Web Engineering process model. My mapping of the weeks onto it (the slides do not draw this link): requirements work belongs to communication, risk work to planning, models and design to modelling.</p>
  <ol class="pm">
    <li class="w2"><b>Communication</b><span class="wk2">Week 2</span></li>
    <li class="w3"><b>Planning</b><span class="wk2">Week 3</span></li>
    <li class="w4"><b>Modelling</b> (analysis + design)<br><span class="wk2">Weeks 4 and 5</span></li>
    <li class="later"><b>Construction</b>not yet in these weeks</li>
    <li class="later"><b>Deployment</b>configuration comes in Week 6</li>
  </ol>

  <h3>Five threads that run through all five weeks</h3>
  <p class="small">These links are my own summary of the slides, to show how the weeks connect. They are not slide text.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Thread</th><th class="t1">Week 1</th><th class="t2">Week 2</th><th class="t3">Week 3</th><th class="t4">Week 4</th><th class="t5">Week 5</th></tr></thead><tbody>
    <tr><th>Process instead of improvisation</th><td>Informality, urgency and intuition replaced by systematic, phased work</td><td>Elicit, document, validate, manage</td><td>Identify, analyse, plan, monitor</td><td>Communication, planning, modelling, construction, deployment</td><td>A seven-step interface design workflow</td></tr>
    <tr><th>Expect change</th><td>Iterative, continuous auditing</td><td>Requirements keep changing; Agile</td><td>Changing requirements are a project-scope risk</td><td>The prototype changes before the final interface</td><td>Refine layout and screens using aesthetic input</td></tr>
    <tr><th>Keep the user in view</th><td>Front-end work: user flows, UI, features designed around user needs</td><td>Stakeholders; "That's not what I asked for"</td><td>Client expectations are hit by scope risks</td><td>User diagram: roles and access rights</td><td>User tasks; efficiency means the user's efficiency</td></tr>
    <tr><th>Catch problems early</th><td>Minimise risks</td><td>Validation and verification</td><td>Prioritise by risk score, High and Critical first</td><td>Models and a prototype show it before it is built</td><td>Start from a rough prototype</td></tr>
    <tr><th>Quality as the goal</th><td>Aim: quality, maintainability, scalability</td><td>Low user acceptance if requirements fail</td><td>Protect timeline, budget and application quality</td><td>Models make the intended quality explicit first (the class diagram guides the database)</td><td>Quality attributes and design goals</td></tr></tbody></table></div>

  <h3>If you remember only five sentences</h3>
  <ol class="five">
    <li><b>Week 1:</b> ad-hoc web projects fail (84% miss their objectives), so Web Engineering adds scientific, engineering and management discipline.</li>
    <li><b>Week 2:</b> agree what to build: elicit, document, validate and verify, manage change, and use Agile because change is constant.</li>
    <li><b>Week 3:</b> protect the plan: identify, analyse (probability x impact), plan and monitor risks, and respond by avoiding, mitigating, transferring or accepting.</li>
    <li><b>Week 4:</b> replace ambiguous words with models: user, class, use case, sequence diagrams and a prototype.</li>
    <li><b>Week 5:</b> turn the models into a usable design: goals, quality attributes, three interaction questions and an interface workflow.</li>
  </ol>
</section>

<section id="story" class="band">
  <h2 class="sec">Previously on Web Engineering</h2>
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
<footer class="foot"><p>Built from your Week 1 to 5 lecture slides. Pictures are cropped from those slides. Week 6 (configuration) is not covered.</p></footer>
<dialog id="lightbox" aria-label="Enlarged picture"><button type="button" class="close" aria-label="Close">Close</button><img alt=""></dialog>
<script>
{JS}
</script>
</body>
</html>'''

open(os.path.join(ROOT, 'cmt322', 'index.html'), 'w').write(PAGE)
print('ok', len(PAGE))
