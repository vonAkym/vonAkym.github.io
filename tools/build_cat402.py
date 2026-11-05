#!/usr/bin/env python3
"""CAT402 Professional and Technopreneurship Development notes page, built from the user's 5 lecture decks,
the mini project guidelines and agenda, and the lecturer's practice questions (photos of the projector screen). Content rules: only what is in the decks; anything that is my own summary,
example or reading is labelled on the page. Diagrams are redrawn as inline SVG, not copied from the slides.

Topics = the five lecture decks in order (Introduction, Augmented Marketer, Operating E-business, Selling on the Web, Marketing on the Web).
The lecture decks of Weeks 3 to 5 carry a Cengage Learning copyright line, so everything is in my own words with redrawn figures."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root (the folder that GitHub Pages serves)
from notes_lib import mindmap, terms, psn, qa, week, E

OUT = os.path.join(ROOT, 'cat402')
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


# ====================================================================== mind maps
MAPS = {
1: mindmap('CAT402 Course Map',
  [('Two parts', ['Technopreneurship development', 'Professional development', 'Business plan from idea to plan', 'Ethics, law, privacy, cyber law']),
   ('Coursework 100%', ['Tests 40%', 'Assignment 20%', 'Project 30%', 'Project presentation 10%']),
   ('Learning outcomes', ['CLO1 career and e-business ideas', 'CLO2 e-business plan', 'CLO3 ethics, law, social issues', 'CLO4 present the plan'])],
  [('Lecturers', ['Dr Suzi Iryanti Fadilah W1-W7', 'Dr Azizul Rahman Mohd Shariff W9-W12']),
   ('Schedule', ['W3 to W5 e-business topics', 'Test 1 in Week 6', 'W9 to W11 future tech and projects', 'Test 2 in Week 12']),
   ('Class rules', ['Attendance taken every class', 'Late work is penalised', 'No test replacement without MC', 'Plagiarism: grade F, maybe barred'])],
  'Mind map of Topic 1: the CAT402 course, its two parts, coursework, outcomes, schedule and rules'),
2: mindmap('The Augmented Marketer',
  [('Career model', ['Before: degree, job, promotion', 'Now: skills, portfolio, opportunities', 'Several income paths per person', 'Employers ask: what can you do?']),
   ('GenAI at work', ['Writing, research, coding, data', 'Value: know what to ask and check', 'Risks: wrong, generic, biased', 'Prompt, understand, verify, adapt']),
   ('Human plus AI', ['AI: fast, scalable, drafts', 'Human: context, judgement, trust', 'Humans stay in charge'])],
  [('Entrepreneurial mindset', ['See problem, find opportunity', 'Create value, test, improve', 'Employees can have it too']),
   ('Digital entrepreneurship', ['E-commerce, apps, content', 'Freelancing, data services', 'Start small']),
   ('Opportunity formula', ['Skill + real problem', '+ digital tool + customer', '= possible value']),
   ('Skill stack', ['Domain and digital skills', 'Communication, critical thinking', 'Problem solving, AI literacy', 'Entrepreneurial mindset'])],
  'Mind map of Topic 2: the changed graduate career model, GenAI, human plus AI, and digital entrepreneurship'),
3: mindmap('Operating an E-business',
  [('Three levels', ['Strategic: long-term goals', 'Tactical: plans for the goals', 'Operational: daily execution', 'Top-down flow']),
   ('Time tools', ['Pareto: 20% effort, 80% results', 'Eisenhower matrix', '20% strategy, 60% routine', '20% unexpected events']),
   ('Stagnation', ['Zalora: partners and AI', 'eBay: back to core strengths', 'Amazon: new businesses', 'Do not be number one in everything'])],
  [('Strategic areas', ['Business objectives', 'Infrastructure investment', 'Revenue operations integration']),
   ('Tactical areas', ['Marketing campaigns', 'CRM', 'Automation', 'Integrating RevOps']),
   ('Operational areas', ['Order fulfilment and logistics', 'Customer support', 'RevOps execution']),
   ('Challenges', ['Data silos', 'Scaling', 'Customer retention', 'Security'])],
  'Mind map of Topic 3: strategic, tactical and operational levels of an e-business, time tools and technology'),
4: mindmap('Selling on the Web',
  [('Revenue models', ['Web catalog', 'Digital content', 'Advertising-supported', 'Advertising-subscription mixed', 'Fee-based']),
   ('Digital content', ['Freemium', 'Subscriptions', 'Fixed-fee sponsorships', 'Cost-per-click advertising', 'Affiliate marketing']),
   ('Advertising', ['Search ads and ad networks', 'Sell your own ad space', 'Trends: video, mobile, native'])],
  [('Web catalog', ['Organised and consistent data', 'Better customer experience', 'Supports business growth']),
   ('Channels', ['Multi-channel: sell everywhere', 'Omni-channel: one unified view', 'Single, multi, cross, omni']),
   ('Design for success', ['First impression', 'User experience and mobile', 'Consistent brand', 'Colour palette', 'Stand out']),
   ('Web presence', ['Attract visitors', 'Build trust', 'Encourage return visits'])],
  'Mind map of Topic 4: revenue models, web catalog, channels and website design for selling online'),
5: mindmap('Marketing on the Web',
  [('Strategy basics', ['SMART goals', '4Ps and 7Ps', 'Product-based strategy', 'Customer-based strategy']),
   ('Know your market', ['Segmentation bases', 'Segment, target, position', 'Relationship marketing', 'CRM and customer lifecycle']),
   ('Choosing tactics', ['Online goals', 'Business environment', 'Audience and competitors', 'Site tech, resources, risk'])],
  [('Reach people', ['Display ads', 'Email marketing', 'Viral marketing', 'SEO and paid search']),
   ('Marketing process', ['Attract', 'Convert', 'Close', 'Delight']),
   ('Branding', ['Purpose and personality', 'Guidelines and experience', 'Three key questions', 'Brand and marketing together']),
   ('Channel mix', ['Owned', 'Paid', 'Earned'])],
  'Mind map of Topic 5: marketing strategy, segmentation, relationships, tactics, channels and branding'),
}

# ====================================================================== topic 1
d_cw = svg(700, 140,
    '<rect class="bxs" x="20" y="30" width="280" height="44" rx="8"/>' + txt(160, 58, 'Tests 40%', 'tb ton')
    + '<rect class="bx" x="300" y="30" width="140" height="44" rx="0"/>' + txt(370, 58, 'Assignment 20%', 'tb')
    + '<rect class="bx" x="440" y="30" width="210" height="44" rx="0"/>' + txt(545, 58, 'Project 30%', 'tb')
    + '<rect class="bxs" x="650" y="30" width="30" height="44" rx="8"/>'
    + txt(665, 100, '10%', 'ts') + txt(665, 118, 'presentation', 'ts')
    + txt(350, 14, 'Coursework = 100% (bar widths drawn to scale)', 'ts'),
    'Redrawn: coursework split into tests 40 percent, assignment 20 percent, project 30 percent and project presentation 10 percent', 'cw')

w1_vis = f'''
  <h3>What the course is</h3>
  <p class="small">CAT 402 / CAT 402W is called <b>Professional and Technopreneurship Development</b>. A <i>technopreneur</i> is the course&rsquo;s word for someone who starts a business around IT. The synopsis says the course has two parts.</p>
  <div class="two"><div><h4>1. Technopreneurship development</h4><p>Entrepreneurship through IT-based products and services, covering the whole path from defining the business idea to writing the business plan. Students are encouraged to join the annual business plan competition.</p></div>
  <div><h4>2. Professional development</h4><p>Issues IT professionals must understand: ethics, social implications, professionalism, intellectual property, cyber laws, freedom of speech and privacy. It also covers careers: job applications, interviews, career paths and graduate studies.</p></div></div>
  <p class="small">Workshops and seminars with successful technopreneurs are planned. They talk about developing ideas, launching and running a business, and creating marketing strategies that last.</p>

  <h3>Coursework: 100%</h3>
  {d_cw}
  <div class="tbl-wrap"><table><thead><tr><th>Item</th><th>Weight</th><th>Linked outcome code on the slide</th></tr></thead><tbody>
  <tr><th>Tests</th><td>40% (two tests of 20% each)</td><td>(13)</td></tr>
  <tr><th>Assignment (group, submitted Weeks 14 to 15)</th><td>20%</td><td>(03)</td></tr>
  <tr><th>Project</th><td>30%</td><td>(32)</td></tr>
  <tr><th>Project presentation</th><td>10%</td><td>(53)</td></tr></tbody></table></div>
  <p class="small">The numbers in brackets are on the slide with no explanation. They look like codes that tie each item to the learning outcomes, but the slide does not say so, so treat that as my guess. The mini project (Weeks 1 to 15) is worth 40%, which is the project 30% plus the presentation 10%. That sum is my own arithmetic.</p>

  <h3>Tests</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Test</th><th>When</th><th>Where</th></tr></thead><tbody>
  <tr><th>Test 1 (Week 6)</th><td>6 November 2026, 8.30 to 9.30 am</td><td>Dewan Utama Peperiksaan D (L17)</td></tr>
  <tr><th>Test 2 (Week 12)</th><td>18 December 2026, 8.30 to 9.30 am</td><td>Dewan Utama Peperiksaan D (L17)</td></tr></tbody></table></div>
  <p class="small">The slides do not say which weeks each test covers. <b>My own reading:</b> Test 1 sits after the Dr Suzi weeks (Weeks 1 to 5) and Test 2 after the Dr Azizul weeks, so these notes should fit Test 1.</p>

  <h3>Learning outcomes (CLOs)</h3>
  <div class="tbl-wrap"><table><thead><tr><th>CLO</th><th>In short</th></tr></thead><tbody>
  <tr><th>CLO1</th><td>Know your own skills, responsibilities and motivation so you can make career decisions, including e-business ideas, planning and launching.</td></tr>
  <tr><th>CLO2</th><td>Develop a sustainable IT-based e-business plan that works across platforms and channels, includes marketing (including affiliate marketing) and protects online business from threats.</td></tr>
  <tr><th>CLO3</th><td>Study ethical, legal and social issues of ICT: computing ethics, privacy, intellectual property, cybercrime and cyber law.</td></tr>
  <tr><th>CLO4</th><td>Present the e-business plan clearly and with confidence.</td></tr></tbody></table></div>

  <h3>Weekly plan</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Week</th><th>Topic</th><th>Lecturer</th></tr></thead><tbody>
  <tr><th>1</th><td>Course overview and coursework explanation</td><td rowspan="7">Dr Suzi Iryanti Fadilah</td></tr>
  <tr><th>2</th><td>Introduction to e-business</td></tr>
  <tr><th>3</th><td>Operating e-business</td></tr>
  <tr><th>4</th><td>Selling on the web</td></tr>
  <tr><th>5</th><td>Marketing on the web</td></tr>
  <tr><th>6</th><td>Test 1 (20%)</td></tr>
  <tr><th>7</th><td>Online lecture</td></tr>
  <tr><th>8</th><td>Semester break</td><td></td></tr>
  <tr><th>9</th><td>Introduction to future technologies and concepts</td><td rowspan="6">Dr Azizul Rahman Mohd Shariff</td></tr>
  <tr><th>10</th><td>ICT project challenges</td></tr>
  <tr><th>11</th><td>Technology project proposal requirements</td></tr>
  <tr><th>12</th><td>Test 2 (20%)</td></tr>
  <tr><th>13</th><td>Christmas, no class</td></tr>
  <tr><th>14 to 15</th><td>No class; group assignment submission (20%)</td></tr></tbody></table></div>
  <p class="small"><b>Heads up, two mismatches in the files:</b> the deck for the Operating E-business lecture is titled &ldquo;Week 6&rdquo; on its first slide, but the schedule above puts that topic in Week 3. Also the second file in the folder (the Augmented Marketer deck) takes the place of the schedule&rsquo;s &ldquo;Introduction to e-business&rdquo; in Week 2, and no separate Introduction to e-business deck is in the folder. I follow the file order.</p>
  <h4>Class rules (from the slides)</h4>
  <ul class="chips-row"><li>Attendance is taken at every class</li><li>Late assignments are penalised according to the reasons</li><li>No replacement test without a valid MC or an exemption letter from a recognised body</li><li>Plagiarism: grade F for the copied work or the whole coursework, and the final exam may be barred</li></ul>
  <p class="small">References listed: Quinn, <i>Ethics for the Information Age</i> (8th ed.); Napier, Rivers and Wagner, <i>Creating a Winning E-Business</i> (2nd ed.); Reynolds, <i>Ethics in Information Technology</i> (6th ed.). Additional: Horan, <i>The One Page Business Plan for the Creative Entrepreneur</i>; Chaffey, <i>E-Business and E-Commerce Management</i> (5th ed.); Blank and Dorf, <i>The Startup Owner&rsquo;s Manual</i>.</p>
'''
w1_terms = terms([
 ('Technopreneur', 'Not defined on the slides. The course title joins technology and entrepreneurship; plainly, a person who starts a business built on IT.'),
 ('CLO', 'Course learning outcome: what you should be able to do at the end. There are four.'),
 ('PLO', 'Program learning outcome. The CLO table cites codes such as PLO9 and PLO8 without explaining them.'),
 ('Professional development', 'Part 2 of the course: ethics, law, social issues, privacy and career skills.'),
 ('Technopreneurship development', 'Part 1 of the course: IT-based business ideas through to a business plan.'),
 ('MC', 'Medical certificate, the proof needed to replace a missed test.'),
])
w1_boss = ''.join([
 qa('List the four coursework items and their weights. Which two make up the mini project?',
  '''<p>Tests 40%, assignment 20%, project 30%, project presentation 10%. The mini project is worth 40%: the project 30% plus the project presentation 10% (my arithmetic from the two slides).</p>''', 1),
 qa('When are the two tests, and who teaches each half of the course?',
  '''<p>Test 1: Week 6, 6 November 2026, 8.30 to 9.30 am. Test 2: Week 12, 18 December 2026, same time. Both at Dewan Utama Peperiksaan D (L17). Dr Suzi Iryanti Fadilah teaches Weeks 1 to 7; Dr Azizul Rahman Mohd Shariff teaches Weeks 9 to 12.</p>''', 2),
 qa('What are the two components of the course?',
  '''<p>Technopreneurship development (IT-based business ideas through to the business plan) and professional development (ethics, social implications, professionalism, intellectual property, cyber law, free speech, privacy, plus career skills).</p>''', 3),
 qa('What happens if you copy another student&rsquo;s work, or let yours be copied?',
  '''<p>Both get grade F for the copied work or for the whole coursework, and barring from the final exam is possible depending on the case.</p>''', 4),
])

# ====================================================================== topic 2
d_cm = svg(700, 150,
    box(10, 20, 160, 44, ['Employee'], 'bx') + box(190, 20, 160, 44, ['Freelancer'], 'bx') + box(370, 20, 160, 44, ['Digital service'], 'bx')
    + box(550, 20, 140, 44, ['Digital product'], 'bx') + box(190, 92, 160, 44, ['Entrepreneur'], 'bxs')
    + arr(170, 42, 190, 42, 'cm') + arr(350, 42, 370, 42, 'cm') + arr(530, 42, 550, 42, 'cm')
    + arr(620, 64, 350, 114, 'cm')
    + txt(530, 130, 'Paths can overlap: you do not have to choose everything today', 'ts'),
    'Redrawn: career paths that can overlap, from employee to freelancer, digital service, digital product and entrepreneur', 'cm')

d_of = svg(700, 96,
    box(10, 24, 120, 48, ['Skill']) + txt(146, 54, '+', 'tb') + box(160, 24, 140, 48, ['Real problem']) + txt(316, 54, '+', 'tb')
    + box(330, 24, 130, 48, ['Digital tool']) + txt(476, 54, '+', 'tb') + box(490, 24, 100, 48, ['Customer']) + txt(606, 54, '=', 'tb')
    + box(620, 24, 70, 48, ['Value'], 'bxs'),
    'Redrawn: the opportunity formula, skill plus real problem plus digital tool plus customer equals possible value', 'of')

w2_vis = f'''
  <h3>The worry behind the lecture</h3>
  <p class="small">The lecture opens with a poll: if you graduate tomorrow, what worries you most? Finding a job, having enough skills, competing with AI, choosing a career, or starting something on your own. The slide says the point is <i>not</i> to become an entrepreneur. The real question is: how do I stay valuable when technology changes? Entrepreneurship is one possible path, and the ability to adapt is needed on all paths.</p>
  <h3>How the graduate career model changed</h3>
  <div class="two"><div><h4>Before</h4><p>Degree &rarr; job &rarr; promotion &rarr; career.</p></div>
  <div><h4>Now</h4><p>Degree &rarr; skills &rarr; portfolio &rarr; opportunities &rarr; continuous learning. One person can have several income or career paths.</p></div></div>
  <p class="small"><b>Professional development</b> is not just attending courses. It means steadily improving knowledge, skills, communication, judgement and adaptability, so you become more useful over time. What makes someone employable is usually a mix (degree, CGPA, technical skill, communication, experience, portfolio, problem solving) and the mix changes by job. Employers increasingly ask &ldquo;What can you do? What problem can you solve? Can you learn quickly?&rdquo;, not only &ldquo;What did you study?&rdquo;</p>

  <h3>GenAI: where human value stays</h3>
  <p class="small">GenAI can already help with writing, research, coding, data, design, marketing and analysis. So &ldquo;I can use AI&rdquo; is not the valuable skill. The valuable skill is knowing what to ask, check, improve and apply.</p>
  <div class="tbl-wrap"><table><thead><tr><th>GenAI is</th><th>Humans bring</th></tr></thead><tbody>
  <tr><td>Fast, scalable, pattern-based, good at drafts</td><td>Context, judgement, responsibility, trust, relationships</td></tr></tbody></table></div>
  <p class="small">The slide&rsquo;s conclusion: the future is not human versus AI but <b>human plus AI</b>. What GenAI cannot easily replace: trust, responsibility, professional judgement, understanding the customer, ethical decisions, human relationships and knowing the local context.</p>
  <div class="cards3">
    <div class="c"><h4>Risks of GenAI</h4><p>Wrong information, generic output, bias, privacy issues, overdependence, lack of originality. Professional development means learning to <b>check</b> AI.</p></div>
    <div class="c"><h4>The dangerous habit</h4><p><b>Prompt &rarr; copy &rarr; submit</b> may give an answer but not a capable graduate. Better: <b>prompt &rarr; understand &rarr; verify &rarr; adapt &rarr; create</b>.</p></div>
    <div class="c"><h4>Using AI safely</h4><p>Use it to speed up learning, not replace it. Check facts, understand the output, protect confidential information, and follow academic and professional rules.</p></div>
  </div>

  <h3>From mindset to digital entrepreneurship</h3>
  <p class="small">An <b>entrepreneurial mindset</b> is not &ldquo;I must start a company&rdquo;. It is: see a problem, find an opportunity, create value, test, improve. Employees can have it too. <b>Digital entrepreneurship</b> means creating value with digital technology: e-commerce, digital services, apps, websites, content, online education, data services, freelancing. Start small. GenAI lowers an old barrier (&ldquo;I need a whole team&rdquo;) because one person can prototype content, a website, a business idea, customer communication and data analysis. But a prototype is not a successful business.</p>
  {d_of}
  <p class="small">The slides give two cases: a <b>data graduate</b> (Excel and Power BI skill; small businesses cannot understand their sales data; solution is a simple dashboard with monthly insights; GenAI helps explain trends and draft reports) and a <b>computing graduate</b> (web development skill; a small business has no simple booking system; solution is a low-cost booking website that saves the owner time).</p>
  <h4>Show evidence, not a list</h4>
  <p class="small">Do not only say &ldquo;I know Power BI.&rdquo; Show it with a portfolio: dashboard, website, app, campaign, case study, data analysis, prototype or digital product. Evidence is stronger than a list of skills.</p>
  {d_cm}
  <div class="tbl-wrap"><table><thead><tr><th>New graduate skill stack (7)</th></tr></thead><tbody>
  <tr><td>1 Domain knowledge &middot; 2 Digital skills &middot; 3 Communication &middot; 4 Critical thinking &middot; 5 Problem solving &middot; 6 AI literacy &middot; 7 Entrepreneurial mindset</td></tr></tbody></table></div>
  <p class="small"><b>The big connection (slide):</b> professional development builds capability; GenAI amplifies it; an entrepreneurial mindset finds opportunities; digital entrepreneurship creates value. Take-home line: <b>learn, build, show, solve, improve</b>, use GenAI, but remain the human in charge.</p>
'''
w2_terms = terms([
 ('Professional development', 'Continually improving knowledge, skills, communication, judgement and adaptability so you become more useful over time.'),
 ('GenAI', 'Generative AI tools that help with writing, research, coding, data, design, marketing and analysis. The slides do not define it further.'),
 ('Human plus AI', 'The slides&rsquo; view of the future: AI gives speed and drafts, humans give context, judgement and trust.'),
 ('Entrepreneurial mindset', 'See a problem, find an opportunity, create value, test, improve. Employees can have it.'),
 ('Digital entrepreneurship', 'Creating value using digital technology (e-commerce, apps, content, freelancing and more).'),
 ('Opportunity formula', 'Skill + real problem + digital tool + customer = possible value.'),
 ('Portfolio', 'Evidence of what you can do: dashboard, website, app, campaign, case study, prototype.'),
 ('AI literacy', 'One of the seven skills in the skill stack. Not defined on the slides; the slides link it to knowing what to ask, check, improve and apply.'),
])
w2_boss = ''.join([
 qa('Why does the lecturer say the lecture is not about becoming an entrepreneur?',
  '''<p>The real question is how to stay valuable when technology changes. Entrepreneurship is only one path; professional adaptability matters on every path.</p>''', 1),
 qa('Complete the loop: prompt, ___, ___, ___, create. Why is &ldquo;prompt, copy, submit&rdquo; dangerous?',
  '''<p>Prompt &rarr; <b>understand</b> &rarr; <b>verify</b> &rarr; <b>adapt</b> &rarr; create. Copy and submit may give an answer but does not make a capable graduate, and AI output can be wrong, generic, biased or unoriginal.</p>''', 2),
 qa('Give the opportunity formula and apply it to one of the two cases.',
  '''<p>Skill + real problem + digital tool + customer = possible value. Data graduate: Excel and Power BI skill + small businesses cannot read their sales data + dashboard and monthly insights + those small businesses = value. Computing graduate: web development + no booking system + low-cost booking site + the business owner.</p>''', 3),
 qa('What can humans offer that GenAI cannot easily replace?',
  '''<p>Trust, responsibility, professional judgement, understanding the customer, ethical decisions, human relationships, and knowing the local context.</p>''', 4),
 qa('List the seven skills in the new graduate skill stack.',
  '''<p>Domain knowledge, digital skills, communication, critical thinking, problem solving, AI literacy, entrepreneurial mindset.</p>''', 5),
 qa('How does this lecture lead into the next topic (operating an e-business)?',
  '''<p><b>My own link, not on the slides:</b> once you have a skill, a problem and a customer, the next question is how to run the business, which is the strategic, tactical and operational planning in Topic 3.</p>''', 6),
])
# ====================================================================== topic 3
d_lv = svg(700, 262,
    box(60, 14, 420, 62, ['Strategic', 'long-term vision, revenue targets, objectives'], 'bxs', small_rest=True)
    + box(60, 100, 420, 62, ['Tactical', 'departments turn goals into actions'], 'bx', small_rest=True)
    + box(60, 186, 420, 62, ['Operational', 'daily work: fulfilment, support, automation'], 'bx', small_rest=True)
    + arr(40, 24, 40, 238, 'lv') + txt(40, 258, 'top-down', 'ts')
    + box(510, 14, 170, 62, ['Technology'], 'bx') + ln(480, 45, 510, 45, True) + ln(480, 131, 510, 45, True) + ln(480, 217, 510, 45, True)
    + txt(595, 100, 'one set of shared,', 'ts') + txt(595, 118, 'real-time data', 'ts') + txt(595, 136, 'for all three levels', 'ts'),
    'Redrawn: strategic, tactical and operational levels flowing top-down, all supported by technology', 'lv')

d_pa = svg(700, 170,
    txt(350, 16, 'Pareto principle (80/20)', 'ts')
    + '<rect class="bxs" x="110" y="34" width="86" height="40" rx="0"/>' + '<rect class="bx" x="196" y="34" width="344" height="40" rx="0"/>'
    + txt(153, 60, '20%', 'tb ton') + txt(368, 60, '80%', 'tb') + txt(70, 60, 'Effort', 'ts', 'end')
    + '<rect class="bxs" x="110" y="96" width="344" height="40" rx="0"/>' + '<rect class="bx" x="454" y="96" width="86" height="40" rx="0"/>'
    + txt(282, 122, '80%', 'tb ton') + txt(497, 122, '20%', 'tb') + txt(70, 122, 'Results', 'ts', 'end')
    + txt(350, 160, 'A small part of the effort gives most of the results (filled = the part that matters most)', 'ts'),
    'Redrawn: 20 percent of the effort gives 80 percent of the results, and the other 80 percent of effort gives 20 percent of results', 'pa')

d_ei = svg(700, 200,
    txt(255, 14, 'Urgent', 'ts') + txt(465, 14, 'Not urgent', 'ts')
    + box(150, 24, 210, 68, ['Do', 'do it now'], 'bxs', small_rest=True) + box(370, 24, 210, 68, ['Decide', 'schedule a time to do it'], 'bx', small_rest=True)
    + box(150, 100, 210, 68, ['Delegate', 'who can do it for you?'], 'bx', small_rest=True) + box(370, 100, 210, 68, ['Delete', 'eliminate it'], 'bx', small_rest=True)
    + txt(138, 62, 'Important', 'ts', 'end') + txt(138, 138, 'Not important', 'ts', 'end')
    + txt(350, 192, 'Eisenhower decision matrix, redrawn', 'ts'),
    'Redrawn: Eisenhower decision matrix with four boxes: do, decide, delegate, delete', 'ei')

w3_vis = f'''
  <h3>Three levels: strategy, tactics, operations</h3>
  <p class="small">The slides say every business, big or small, has two main uses of managers&rsquo; time: <b>strategy</b> and <b>tactics</b>, and a third part, <b>operations</b>, completes them.</p>
  <div class="cards3">
    <div class="c"><h4>Strategy</h4><p>The long-term goals and the ways to reach them: where the company should go and how to succeed in the medium and long term.</p></div>
    <div class="c"><h4>Tactics</h4><p>Actions and decisions that aim at specific goals and support the strategy; daily operations and controlling ongoing processes.</p></div>
    <div class="c"><h4>Operations</h4><p>The routine tasks, methods, steps and resources needed to run the business every day and carry out the tactics.</p></div>
  </div>
  {d_lv}
  <p class="small">The slides&rsquo; example: a large e-commerce firm sets a strategic goal to raise sales by 20% in Q4. Marketing then launches a targeted email campaign (tactical) and operations handles the extra orders (operational). Doing tasks without a clear goal is only <i>productivity</i>; the slides want <b>efficiency</b>, meaning results, so start from goals and work out which tasks are needed.</p>
  <h4>Do not be &ldquo;number one&rdquo; in everything</h4>
  <p class="small">The owner should generate ideas and open new space for growth. An owner who does every job (management, accounting, driving the van) causes <b>stagnation</b>: stopping, with no growth or change. The slides advise delegating and hiring specialists, which looks costly but pays off in profit and effectiveness.</p>

  <h3>Stagnation and how firms escaped it</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Firm</th><th>Pressure</th><th>What it did</th></tr></thead><tbody>
  <tr><th>Zalora / FashionValet</th><td>Shopee and Lazada widened their products and customers.</td><td>Strategic partnerships with payment gateways and logistics firms; invested in AI and machine learning for stock, recommendations and targeted marketing.</td></tr>
  <tr><th>eBay</th><td>Competition from Amazon and AliExpress; trouble keeping buyers and sellers.</td><td>Refocused on its core strength, a marketplace for unique, hard-to-find items; allowed new products next to used ones (C2C and B2C); improved its interface and search.</td></tr>
  <tr><th>Amazon</th><td>Its size and rivals such as Walmart, Alibaba and Shopify.</td><td>Expanded beyond e-commerce (AWS cloud, Prime Video, Whole Foods, Amazon Go) and kept investing in customer experience, for example Prime membership.</td></tr></tbody></table></div>
  <p class="small">The slides&rsquo; general cure: decisive action, new strategies, and promoting high self-organisation. The common thread is that an e-business must keep innovating.</p>

  <h3>Two tools for using time well</h3>
  {d_pa}
  <p class="small"><b>Pareto principle (80/20):</b> most results come from a small share of the effort or sources. In strategic planning the slides suggest about 20% of time for mandatory strategic planning and 80% for everything else. Notice that the slide states the principle only; it gives no worked business examples like the ones in Exclusive Tips below.</p>
  {d_ei}
  <p class="small"><b>Eisenhower matrix</b> (important versus urgent). The slides turn it into a time split for a business: <b>20%</b> of time for strategic tasks, <b>60%</b> for routine tasks such as customer service and mail, and <b>20%</b> for force majeure (unexpected events). Their example: a logistics firm thought force majeure took 50 to 60% of its time, but most of it was really routine work such as car repairs. Seeing that let them stop stressing, plan the routine, and hire a specialist for it.</p>

  <h3>The strategic framework</h3>
  <p class="small">The long-term vision and roadmap that guides decisions in the digital world. Its focus is high-level goals: market position, value proposition, infrastructure planning and overall revenue strategy. It aims to line up all resources and activities for growth that lasts. Three key areas:</p>
  <div class="cards3">
    <div class="c"><h4>Business objectives</h4><p><b>Growth targets</b> (for example +30% online sales), <b>value proposition</b> (what makes you worth buying from; Zalora: trendy, affordable fashion with fast delivery) and <b>market expansion</b> (Amazon: books to groceries, electronics, media).</p></div>
    <div class="c"><h4>Infrastructure investment</h4><p><b>Cloud</b> (AWS, Google Cloud) copes with traffic spikes in big sales; <b>e-commerce platforms</b> (Shopify for fast launch, Magento for customising) plug into payments and stock.</p></div>
    <div class="c"><h4>Revenue operations (RevOps)</h4><p>Aligns sales, marketing and customer service on one strategy, data and tools. Real-time analytics (HubSpot, Salesforce, Marketo) drive decisions. TikTok is the slides&rsquo; example.</p></div>
  </div>
  <h3>The tactical framework</h3>
  <p class="small">Turns strategic goals into practical steps using technology, customer insight and processes.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Key component</th><th>Objective and tools (from the slides)</th></tr></thead><tbody>
  <tr><th>Marketing campaigns</th><td>Convert potential customers into loyal buyers. Targeted Facebook and Google ads, Instagram ads, personalised content. Zalora tailors ads for Black Friday and Chinese New Year from customer data.</td></tr>
  <tr><th>CRM</th><td>Manage customer relationships through their whole life with the firm. HubSpot, Zoho; Salesforce for large firms; HubSpot CRM has a free option for small firms.</td></tr>
  <tr><th>Automation</th><td>Automate repetitive tasks so the team can focus on strategy. Zapier links apps (a web form feeds the CRM); email automation (Mailchimp, SendGrid, HubSpot) nurtures leads and follows up abandoned carts.</td></tr>
  <tr><th>Integrating RevOps</th><td>Marketing, sales and support work together, with no silos and no bottleneck in the sales cycle. Marketing gives sales good leads, sales close them, support solves issues and feeds back to both.</td></tr></tbody></table></div>
  <h3>The operational framework</h3>
  <p class="small">Keeps daily activity running smoothly so the business meets customer demand efficiently, using the right tools and workflows.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Key component</th><th>Objective and tools</th></tr></thead><tbody>
  <tr><th>Order fulfilment and logistics</th><td>Deliver accurately, efficiently and on time. Couriers and tracking (ShipBob, UPS, J&amp;T Express, DHL); AI route planning; order management systems (Brightpearl, Cin7) automate stock, orders and delivery updates.</td></tr>
  <tr><th>Customer support</th><td>Fast, reliable, personal help. Zendesk, LiveChat, Freshdesk; AI chatbots; IVR phone routing; self-service FAQs and knowledge bases.</td></tr>
  <tr><th>RevOps execution</th><td>Line up operational workflows with revenue activity to improve experience and retention. HubSpot Service Hub; Shopee and Lazada track support tickets and delivery feedback and spot upsell and cross-sell chances.</td></tr></tbody></table></div>
  <h4>Technology and typical problems</h4>
  <div class="two"><div><h4>Role of technology</h4><p>Cloud (AWS, Azure) for flexibility; automation (Zapier, ActiveCampaign); real-time analytics (Google Analytics, Power BI, Tableau); RevOps platforms (HubSpot, Salesforce).</p></div>
  <div><h4>Challenges and fixes</h4><p><b>Data silos</b>: RevOps systems share data. <b>Scaling</b>: cloud scales up and down. <b>Retention</b>: AI and predictive analytics spot at-risk customers. <b>Security</b>: follow rules such as GDPR and use secure payment gateways such as Stripe.</p></div></div>
  <p class="small"><b>For small start-ups</b> the slides advise a niche market, affordable tools (Instagram Shops, Canva, Shopify) and customer feedback; a local example is a batik seller using Instagram Shops, Shopee Seller Center and Mailchimp, delivering with Pos or J&amp;T Express. Established firms invest in data and RevOps; all firms keep customer satisfaction at the core and can use chatbots to support customers without growing cost.</p>
'''
w3_terms = terms([
 ('Strategy', 'Long-term goals and the plan to reach them.'),
 ('Tactics', 'Actions and decisions that support the strategy.'),
 ('Operations', 'Routine daily tasks, methods and resources that keep the business running.'),
 ('Stagnation', 'Stopping or lacking growth, development or change. Harmful: dissatisfaction, low productivity, lost opportunities.'),
 ('Pareto principle (80/20)', 'About 20% of effort gives about 80% of results; the other 80% of effort gives the remaining 20%.'),
 ('Eisenhower matrix', 'Important versus urgent grid: do, decide, delegate, delete. The slides use it for a 20/60/20 time split.'),
 ('Force majeure', 'Unpredictable events that can affect a business. Often smaller than they feel, because much of what looks unexpected is really routine.'),
 ('RevOps (revenue operations)', 'Uniting sales, marketing and customer success around shared data, tools and processes to grow revenue.'),
 ('Data silo', 'Data stuck in one team, so others cannot see it. The fix named in the slides is a RevOps system that shares data.'),
 ('CRM', 'Customer relationship management: tools to track interactions and follow up leads.'),
 ('OMS', 'Order management system: automates stock tracking, order processing and delivery updates.'),
 ('IVR', 'Interactive voice response: phone system that routes calls to the right department.'),
 ('Churn', 'Customers leaving. The slides mention reducing churn by spotting at-risk customers.'),
])
w3_boss = ''.join([
 qa('Define strategic, tactical and operational levels in one line each, and say how they connect.',
  '''<p><b>Strategic:</b> long-term goals. <b>Tactical:</b> plans that serve those goals. <b>Operational:</b> day-to-day execution. The flow is top-down, with shared technology giving every level the same real-time data.</p>''', 1),
 qa('What is the Pareto principle and how do the slides apply it to planning time?',
  '''<p>About 20% of effort produces about 80% of results. For planning, the slides suggest about 20% of time for mandatory strategic planning and 80% for everything else.</p>''', 2),
 qa('Give the time split from the slides&rsquo; Eisenhower discussion and explain the logistics example.',
  '''<p>20% strategic tasks, 60% routine tasks, 20% force majeure. A logistics firm believed force majeure took 50 to 60% of its time, but much of it was routine (such as car repairs). Naming it routine let them plan it, stop stressing, and give it to a specialist.</p>''', 3),
 qa('How did Zalora, eBay and Amazon each deal with stagnation?',
  '''<p><b>Zalora:</b> partnerships (payments, logistics) and AI investment. <b>eBay:</b> refocused on unique, hard-to-find items, mixed new with used goods, improved interface and search. <b>Amazon:</b> expanded into AWS, Prime Video, Whole Foods and Amazon Go, and invested in customer experience.</p>''', 4),
 qa('Name the three key areas of the strategic framework, and the tactical and operational components.',
  '''<p><b>Strategic:</b> business objectives, infrastructure investment, revenue operations integration. <b>Tactical:</b> marketing campaigns, CRM, automation, integrating RevOps. <b>Operational:</b> order fulfilment and logistics, customer support, RevOps execution.</p>''', 5),
 qa('List four challenges and the solution the slides give for each.',
  '''<ul><li>Data silos: RevOps systems such as HubSpot or Salesforce.</li><li>Scaling: cloud infrastructure scales up and down.</li><li>Customer retention: AI and predictive analytics to find at-risk customers.</li><li>Security: comply with rules such as GDPR and use secure payment gateways such as Stripe.</li></ul>''', 6),
 qa('Why should an owner delegate instead of doing every job?',
  '''<p>An owner who does all roles blocks growth and leads to stagnation. Delegating and hiring specialists seems expensive but raises profit and effectiveness over time.</p>''', 7),
])

# ====================================================================== topic 4
d_ch = svg(700, 150,
    '<path class="bx" d="M10 34 H160 L180 64 L160 94 H10 Z"/>' + txt(80, 70, 'Single channel', 'tb')
    + '<path class="bx" d="M180 34 H350 L370 64 L350 94 H180 L200 64 Z"/>' + txt(275, 70, 'Multi-channel', 'tb')
    + '<path class="bx" d="M370 34 H520 L540 64 L520 94 H370 L390 64 Z"/>' + txt(450, 70, 'Cross-channel', 'tb')
    + '<path class="bxs" d="M540 34 H680 V94 H540 L560 64 Z"/>' + txt(618, 70, 'Omni-channel', 'tb ton')
    + txt(80, 118, 'one touch-point', 'ts') + txt(275, 118, 'many, acting alone', 'ts') + txt(450, 118, 'one brand, one view', 'ts') + txt(618, 118, 'customer-centred', 'ts')
    + txt(350, 142, 'My short captions under the four stage names on the slide figure', 'ts'),
    'Redrawn: four stages of selling channels, single channel, multi-channel, cross-channel and omni-channel', 'ch')

w4_vis = f'''
  <h3>Why revenue models come first</h3>
  <p class="small">After you can run an e-business (Topic 3), the next question is how it earns money. A <b>revenue model</b> is how a company brings in money. The learning goals of the chapter are: what a revenue model is, how firms change theirs, the revenue issues of selling online, how to build a good web presence, what makes a site usable, and how firms use the web to connect with customers.</p>
  <h3>Five web revenue models</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Model</th><th>Idea</th></tr></thead><tbody>
  <tr><th>Web catalog</th><td>Sell products from an online catalog, an online version of a mail-order catalog.</td></tr>
  <tr><th>Digital content</th><td>Sell or license information or media that is delivered over the web.</td></tr>
  <tr><th>Advertising-supported</th><td>The content is free to users and advertisers pay.</td></tr>
  <tr><th>Advertising-subscription mixed</th><td>Users pay a subscription and ads also appear.</td></tr>
  <tr><th>Fee-based</th><td>Charge for a transaction or a service.</td></tr></tbody></table></div>
  <p class="small">The slide lists these five names and notes that the same model can work for both B2C (business to consumer) and B2B (business to business) sales. The one-line ideas in the table are <b>my own plain-words reading</b>, because the slides give only the names and pictures. The slides&rsquo; revenue-model picture adds ideas such as subscription, pay per view, commissions, affiliate, feature listings, ads and sponsorships.</p>

  <h3>Web catalog</h3>
  <p class="small">Product catalog management means keeping product data high quality across all sales channels: organising, standardising and publishing it to each channel. The slides give four reasons to invest in it.</p>
  <ul class="chips-row"><li>Organised catalog: customers cannot touch the product, so detailed descriptions and images plus easy search make up for it</li><li>Consistent information: no short forms or false claims, across all channels</li><li>Better customer experience, even for first-time buyers</li><li>Business growth: a base for a bigger catalog and a faster launch</li></ul>
  <p class="small">The catalog &ldquo;must have&rdquo; features shown on a slide figure: sort and filter (colour, size, price, rating), quick view, a back-to-top button, and a way to load more products without paging.</p>
  <h4>Multi-channel versus omni-channel</h4>
  <div class="two"><div><h4>Multi-channel</h4><p>Promote and sell wherever customers buy: marketplaces, social media, messaging apps, online communities. Each channel works on its own.</p></div>
  <div><h4>Omni-channel</h4><p>All channels (direct marketing, ads, sales, web, mobile, call centre) are fused into one approach with unified data and experience. It is about the customer. Example: an abandoned cart triggers an email coupon, retargeting ads remind of it, and a finished order brings cross-sells.</p></div></div>
  <div class="tbl-wrap"><table><thead><tr><th>Characteristic</th><th>Multi-channel</th><th>Omni-channel</th></tr></thead><tbody>
  <tr><th>Goals and incentives</th><td>Each channel has its own goals</td><td>Incentives drive collaboration across channels</td></tr>
  <tr><th>Customer data</th><td>Stored separately per channel</td><td>One integrated view of the customer</td></tr>
  <tr><th>Analytics</th><td>Channel-specific</td><td>360-degree view of all touchpoints</td></tr>
  <tr><th>Agent alignment</th><td>Channel-specific</td><td>Supports several channels, alone or with other agents</td></tr></tbody></table></div>
  {d_ch}
  <p class="small">Slide figures also claim that adding channels raises revenue (the chart shows average increases of 38%, 120% and 190% for one, two and three extra channels over cart-only) and that omni-channel firms keep far more customers (89% versus 33%). These are the figures as I read them from low-resolution images, so check before quoting.</p>

  <h3>Digital content, subscriptions, advertising</h3>
  <div class="cards3">
    <div class="c"><h4>Digital content: freemium</h4><p>Give a free tier and charge for a premium one. The slides use Spotify: an ad-supported free service plus paid premium. Other content types sold online: ebooks, music, courses, software, photos, templates.</p></div>
    <div class="c"><h4>Other digital content models</h4><p>Fixed-fee sponsorships, subscriptions, cost-per-click advertising, and affiliate marketing and sales.</p></div>
    <div class="c"><h4>Affiliate marketing</h4><p>Endorse a product you like on your site; when a visitor clicks your affiliate link and buys, you get a share of the sale. Quick and popular.</p></div>
    <div class="c"><h4>Subscriptions</h4><p>Netflix, Spotify and Amazon Prime. Benefits: loyal user base, steady predictable revenue, predictable sales pipeline. Hard to build: these firms spend billions on original content to keep people renewing.</p></div>
    <div class="c"><h4>Advertising revenue</h4><p>Google gives services free and earns from ads (AdWords, now Google Ads). AdSense lets a site owner show Google&rsquo;s ads and get paid per click. You can also sell ad space directly at a fixed price, which pays well only if traffic is large. Unless you are Google or Facebook, ads alone need a very large user base.</p></div>
    <div class="c"><h4>Ad trends named</h4><p>Programmatic, beacon, social media, VR, buy buttons, mobile, video and native advertising.</p></div>
  </div>
  <p class="small">The slide of business-model examples groups real firms: e-commerce and marketplace (Amazon, Zalando), on-demand (Uber, Airbnb), subscription (Netflix, Salesforce), freemium (Spotify, Dropbox, Mailchimp), ad-supported (Google, Facebook, Quora), peer to peer (Uber, Airbnb, LinkedIn) and open source (Red Hat, GitHub).</p>

  <h3>Design for success</h3>
  <p class="small">A site with customers but a poor design loses them. The slides give five rules, plus the idea that you design for the people who will use and buy.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Rule</th><th>What it means</th></tr></thead><tbody>
  <tr><th>First impression</th><td>Like a messy shop floor, a messy layout, poor images or mismatched fonts make people leave. Look at competitors; keep it clean and professional with consistent, high-quality images.</td></tr>
  <tr><th>User experience</th><td>Easy to find things; simple navigation; clear next-step buttons; clear FAQ and contact pages; mobile friendly with big buttons and a condensed menu.</td></tr>
  <tr><th>Consistent brand</th><td>Same brand image on every platform, including the site, chosen to fit the audience (delicate for wedding dresses, outdoorsy for survival kits).</td></tr>
  <tr><th>Colour palette</th><td>Keep logo colours, pick colours that complement each other, and know what colours say: green fresh, yellow joy, orange bold call-to-action, red energy, purple luxury, blue calm and professional, white clean, black luxury.</td></tr>
  <tr><th>Stand out</th><td>Keep a familiar layout but add something memorable such as a fun colour scheme, a bold logo or animation.</td></tr></tbody></table></div>
  <h4>Web presence objectives and strategies</h4>
  <div class="tbl-wrap"><table><thead><tr><th>Objective</th><th>Strategy</th></tr></thead><tbody>
  <tr><td>Attract visitors</td><td>Put links to the site in marketing emails</td></tr>
  <tr><td>Make visitors stay and explore</td><td>Product reviews, comparisons and advice</td></tr>
  <tr><td>Get visitors to follow links for information</td><td>Clearly labelled links that hint at what is behind them</td></tr>
  <tr><td>Give an impression that matches the organisation&rsquo;s image</td><td>Use logos, characters, slogans and catchphrases</td></tr>
  <tr><td>Build a trusting relationship</td><td>Make sure information is valid and objective</td></tr>
  <tr><td>Reinforce positive images visitors already have</td><td>Show testimonials, awards and external reviews</td></tr>
  <tr><td>Encourage return visits</td><td>Keep information current and regularly updated</td></tr></tbody></table></div>
  <p class="small">The slide also shows accessibility goals for business sites without listing them in text, so they are not covered here. A class activity asks each member to pick one type of website, find an example, and say why its design works.</p>
'''
w4_terms = terms([
 ('Revenue model', 'How a company earns money. The chapter names five for the web.'),
 ('B2C / B2B', 'Business to consumer / business to business. The same revenue model can serve both.'),
 ('Web catalog', 'A revenue model that sells products from an online catalog (my plain-words gloss).'),
 ('Product catalog management', 'Keeping product data high quality across all channels: organise, standardise, publish.'),
 ('Multi-channel', 'Promoting and selling in many places where customers already are.'),
 ('Omni-channel', 'All channels fused with unified data and experience around the customer.'),
 ('Freemium', 'Free tier plus a paid premium tier. Spotify is the slides&rsquo; example.'),
 ('Affiliate marketing', 'Earn a share of a sale when a visitor buys through your link.'),
 ('Subscription', 'Recurring payment for continued access; predictable revenue, loyal base.'),
 ('AdWords / AdSense', 'Google Ads: ads shown on search results. AdSense: ads shown on site owners&rsquo; pages, paid per click.'),
 ('Cost per click (CPC)', 'Paying or being paid each time someone clicks an ad.'),
 ('Native / programmatic advertising', 'Named in the ad trends list. The slides do not define them.'),
 ('Call to action (CTA)', 'A prompt such as a Buy Now button that tells a visitor what to do next.'),
 ('Responsive website', 'A site that looks right on phones and tablets as well as computers.'),
])
w4_boss = ''.join([
 qa('List the five web revenue models and give one real example for freemium and for subscription.',
  '''<p>Web catalog, digital content, advertising-supported, advertising-subscription mixed, fee-based. Freemium: Spotify (free with ads, paid premium). Subscription: Netflix, Spotify or Amazon Prime.</p>''', 1),
 qa('Why invest in product catalog management? Give the four reasons.',
  '''<p>Organised catalog (customers cannot touch the product, so detail and search help), consistent information across channels, better customer experience, and business growth.</p>''', 2),
 qa('Explain the difference between multi-channel and omni-channel.',
  '''<p>Multi-channel sells everywhere customers buy, but each channel works on its own with its own data and goals. Omni-channel joins all channels into one approach with a single customer view, so the experience is seamless and consistent.</p>''', 3),
 qa('What are the built-in advantages of a subscription model, and why is it not easy?',
  '''<p>Loyal user base, a continuous stream of predictable revenue and a more predictable sales pipeline. It is hard because firms like Netflix and Spotify spend billions on original content to keep subscribers renewing.</p>''', 4),
 qa('How does a site owner earn from Google AdSense, and what is the downside of selling ad space directly?',
  '''<p>Google places code that shows ads that match your content, and you are paid each time someone clicks. Selling ad space directly at a flat price can pay a lot with heavy traffic, but little if traffic is low.</p>''', 5),
 qa('Name the five design-for-success rules.',
  '''<p>First impression, user experience (including mobile), consistent brand and design, colour palette, and standing out from the crowd.</p>''', 6),
 qa('Marketplace versus your own site: what do these slides give you to reason with?',
  '''<p>The slides never compare the two directly. <b>My own reading, using the notes:</b> a marketplace is one more channel (multi-channel), so it reaches buyers where they already are; your own site gives control over design, brand, user experience and data, which is what the design rules and the omni-channel idea of one customer view need. Use this reasoning in Exclusive Tips.</p>''', 7),
])
# ====================================================================== topic 5
d_mp = svg(700, 130,
    box(10, 28, 120, 54, ['Attract', 'strangers'], small_rest=True) + box(150, 28, 120, 54, ['Convert', 'visitors'], small_rest=True)
    + box(290, 28, 120, 54, ['Close', 'leads'], small_rest=True) + box(430, 28, 120, 54, ['Delight', 'customers'], small_rest=True)
    + box(570, 28, 120, 54, ['Promoters', 'spread the word'], 'bxs', small_rest=True)
    + arr(130, 55, 150, 55, 'mp') + arr(270, 55, 290, 55, 'mp') + arr(410, 55, 430, 55, 'mp') + arr(550, 55, 570, 55, 'mp')
    + txt(70, 106, 'blog, keywords,', 'ts') + txt(70, 122, 'social posts', 'ts') + txt(210, 106, 'forms, CTAs,', 'ts') + txt(210, 122, 'landing pages', 'ts')
    + txt(350, 106, 'CRM, email,', 'ts') + txt(350, 122, 'workflows', 'ts') + txt(490, 106, 'surveys, smart', 'ts') + txt(490, 122, 'content, monitoring', 'ts'),
    'Redrawn: the target marketing process, attract strangers, convert visitors to leads, close leads as customers, delight customers into promoters', 'mp')

d_lc = svg(700, 120,
    ''.join(box(8 + i * 98, 26, 90, 50, [t], 'bxs' if i == 6 else 'bx') for i, t in enumerate(['Awareness', 'Knowledge', 'Consider', 'Selection', 'Purchase', 'Retention', 'Advocacy']))
    + ''.join(arr(98 + i * 98, 51, 106 + i * 98, 51, 'lc') for i in range(6))
    + txt(350, 108, 'Customer lifecycle in seven stages (the stage names are on the slide figure; my labels shortened)', 'ts'),
    'Redrawn: the seven-stage customer lifecycle from awareness to advocacy', 'lc')

w5_vis = f'''
  <h3>Why marketing comes after selling</h3>
  <p class="small">A site with a good revenue model and design still earns nothing if nobody comes. The chapter&rsquo;s goals: product-based and customer-based strategies, talking to market segments, customer characteristics along the relationship life cycle, web advertising, email marketing, technology-enabled CRM, brands on the web, viral social media campaigns, and search engine positioning.</p>
  <h3>Goals and the marketing mix</h3>
  <div class="two"><div><h4>SMART goals</h4><p><b>S</b>pecific (for example raise market share 10%), <b>M</b>easurable, <b>A</b>ttainable (a stretch but not near impossible), <b>R</b>elevant to the mission, <b>T</b>ime-based with a finish date such as one year.</p></div>
  <div><h4>4Ps, extended to 7Ps</h4><p><b>Product</b> (what you sell), <b>Price</b>, <b>Promotion</b> (how you talk to buyers), <b>Place</b> (where it is sold). The extended mix adds <b>People</b>, <b>Process</b> and <b>Physical evidence</b>.</p></div></div>
  <div class="tbl-wrap"><table><thead><tr><th>Strategy</th><th>Pros</th><th>Cons</th></tr></thead><tbody>
  <tr><th>Product-based</th><td>Focus on what you do best; build a reputation for quality; loyalty to the product.</td><td>You can leave customers behind; a quality product still has to match a target market.</td></tr>
  <tr><th>Customer-based</th><td>Find out what customers want and provide it; more likely to buy; more loyalty.</td><td>Costly (market research, hard for small firms); can distract from making quality products.</td></tr></tbody></table></div>

  <h3>Segment your market</h3>
  <p class="small">Divide customers into groups with shared qualities so each group gets a better, more fitting experience. The slides use four bases: <b>geographic</b> (country, city, climate), <b>demographic</b> (age, gender, income, education), <b>psychographic</b> (lifestyle, interests, values, personality) and <b>behavioural</b> (purchase, usage, occasion, loyalty, buyer stage). The flow is <b>segmentation &rarr; targeting &rarr; positioning</b>.</p>
  <ul class="chips-row"><li>VIPs: shop most often or spend most</li><li>Active, long-time recurring users</li><li>Reactivated: bought, went quiet, bought again</li><li>Low-tier recurring: shop less and spend less</li><li>New customers (first purchase)</li><li>New visitors who joined the mailing list without buying</li></ul>
  <p class="small">Why it pays, per the slides: saves time and money, builds better customer relationships, shows your strengths and weaknesses. One slide quotes a DMA finding of a 760% boost in email revenue from segmented campaigns; another shows an example where segments average $42 per customer against $28 for all customers (slide figures).</p>

  <h3>Relationship marketing and CRM</h3>
  <p class="small"><b>Relationship marketing</b> is everything a brand does to build strong, lasting customer relationships (influencer programs, referrals, affiliate marketing), and the key part is two-way conversation. <b>CRM</b> aims to improve customer satisfaction, expand the customer base, enhance sales and improve workforce productivity. Its three functions, sales, marketing and customer service, run along the customer lifecycle and support each other.</p>
  {d_lc}
  <p class="small">The slide on return on investment (ROI) shows referral revenue growing about 3 times between year 1 and year 2, and says long-term partnerships are the best way to approach relationship marketing.</p>

  <h3>Advertising on the web and picking tactics</h3>
  <div class="cards3">
    <div class="c"><h4>Display ad types</h4><p>Text, image, video and mobile ads. Ads can be classed by how they are served (banner, contextual, search, local, mobile, map, social), how they are displayed (expandable, floating, pop-up, interstitial, wallpaper and others) and where (browser, non-browser, feeds, newsletters, email).</p></div>
    <div class="c"><h4>Seven uses of the Internet in marketing</h4><p>Raise awareness; build loyalty; generate leads; shorten the sales cycle with relevant information; collect customer information; communicate company information; improve customer service.</p></div>
    <div class="c"><h4>Four adopter stages</h4><p><b>Traditionalists</b> (offline first, low risk), <b>pragmatists</b> (cautious trials, no plan or budget), <b>adopters</b> (use several tactics, small budget), <b>innovators</b> (full engagement, test new tactics such as video and mobile search).</p></div>
  </div>
  <h4>Seven factors for selecting tactics</h4>
  <div class="tbl-wrap"><table><thead><tr><th>Factor</th><th>Ask yourself</th></tr></thead><tbody>
  <tr><th>1. Online goals</th><td>Map goals to business objectives: awareness, visibility, traffic, online or offline sales, sign-ups, downloads.</td></tr>
  <tr><th>2. Business environment</th><td>B2B has longer sales cycles (for example paid search leading to a whitepaper download, then email follow-up); a crowded market needs a standout idea.</td></tr>
  <tr><th>3. Online audience</th><td>Who are they and where do they spend time online? Age, income, gender, media habits, web experience.</td></tr>
  <tr><th>4. Online competitors</th><td>Rivals include local and global firms and marketplaces; study their tactics and either compete head-on or find a niche.</td></tr>
  <tr><th>5. Site technology</th><td>Platform, CMS, dynamic or static, database, analytics package.</td></tr>
  <tr><th>6. Internal resources</th><td>Enough money and people? You can outsource, but still need an in-house online marketing champion.</td></tr>
  <tr><th>7. Risk tolerance</th><td>Cautious firms pick proven tactics; risk and reward usually rise together. Think about investment size, time and effort, and how well outcomes can be predicted.</td></tr></tbody></table></div>
  <p class="small">A slide table scores common tactics (banners, email, affiliate, SEO, paid search, social, blogs, podcasts and others) against advantages and disadvantages such as click-through rate, ease, audience type, measurability, credibility and cost. Its symbols are small icons, so the cell-by-cell ratings are not reproduced here.</p>

  <h3>Marketing process and email</h3>
  {d_mp}
  <p class="small">The <b>target marketing process</b> moves people from strangers to visitors to leads to customers to promoters. A content marketing plan asks: who are your people, what are your objectives and goals, what content, how often, and how will you promote it.</p>
  <div class="two"><div><h4>Email marketing</h4><p>The slides say email outperforms the other online strategies (SEO, pay-per-click, content marketing) and is the most cost-effective way to reach goals. Strategies: real-time personalisation, multi-channel marketing intelligence, scheduling campaigns, and strong content. Benefits chart: more leads, better sales, better conversion rates, lower marketing cost.</p></div>
  <div><h4>Email process: 5 steps</h4><p><b>Define</b> (name the campaign, subject, details) &rarr; <b>test</b> (browsers, email clients) &rarr; <b>send</b> (now or scheduled) &rarr; <b>measure</b> (opens, clicks, activity) &rarr; <b>report</b> (usage, bounces, social sharing).</p></div></div>

  <h3>Branding</h3>
  <p class="small">A brand is more than a logo: it is the customer&rsquo;s total experience, in your promise, values, personality and how you talk and answer the phone. It is a badge of trust. A good brand delivers a clear message, proves credibility, connects emotionally, motivates a purchase and creates loyalty. Loyal customers need yes to <b>three questions</b>: did it perform as expected, was quality as good as promised or better, and was the whole experience positive?</p>
  <div class="two"><div><h4>Branding (identity)</h4><p>Brand purpose, personality, guidelines (visual rules, voice, tone) and brand experience (consistency builds trust).</p></div>
  <div><h4>Marketing (sharing it)</h4><p>Informative (awareness), inspirational, profitable, a tool for selling. Do not sound too salesy or you lose credibility.</p></div></div>
  <p class="small">Checklist to evaluate a brand: does it relate to the audience at a glance, show your uniqueness, reflect your promise and hold value inside, and reflect the values you want to represent. Brand guidelines give marketing its outline; marketing then reinforces the brand.</p>

  <h3>Viral, search and the channel mix</h3>
  <div class="cards3">
    <div class="c"><h4>Viral marketing</h4><p>Users pass the message on, creating buzz. How: appealing content, the right platform for the audience, the right influencer. Methods: social media optimisation, SEO, influencers, mobile. Benefits: lower cost, huge reach, better interaction, awareness (good for new firms).</p></div>
    <div class="c"><h4>Search engine marketing</h4><p><b>Organic</b> rankings come from SEO. <b>Paid</b> search is pay-per-click: advertisers bid for a keyword and the highest bid gets the top spot. A slide cites paid search visits converting 35% better than organic for e-commerce.</p></div>
    <div class="c"><h4>SEO versus PPC</h4><p><b>SEO:</b> long-term return, high volume, awareness; but hard to measure, slow, needs design and development work. <b>PPC:</b> quick to set up, measurable; but costlier, lower ceiling, and can suffer ad blindness.</p></div>
    <div class="c"><h4>Owned, paid, earned</h4><p><b>Owned:</b> you control it (your site). <b>Paid:</b> you pay for placement (PPC, paid social). <b>Earned:</b> others give you free exposure. They work best together; the combined return exceeds the sum of the parts.</p></div>
  </div>
'''
w5_terms = terms([
 ('SMART goal', 'Specific, measurable, attainable, relevant, time-based.'),
 ('4Ps / 7Ps', 'Product, price, promotion, place; plus people, process, physical evidence.'),
 ('Market segmentation', 'Dividing customers into groups with shared qualities so each can be targeted better.'),
 ('Segmentation bases', 'Geographic, demographic, psychographic, behavioural.'),
 ('Targeting / positioning', 'The steps after segmentation: choose which segments to serve, then decide how to place the offer for them (my plain-words gloss; the slide shows only the three names).'),
 ('Relationship marketing', 'Everything a brand does to build strong, lasting relationships; two-way conversation is the key part.'),
 ('CRM', 'Customer relationship management; sales, marketing and customer service along the lifecycle.'),
 ('Customer lifecycle', 'Awareness, knowledge, consideration, selection, purchase, retention, advocacy.'),
 ('Display ad', 'An ad shown on a web page: text, image, video or mobile.'),
 ('Conversion', 'Turning a visitor or lead into a customer or other wanted action. Not defined on the slides.'),
 ('Brand', 'The customer&rsquo;s total experience of the business, not only logo and slogan.'),
 ('Viral marketing', 'Buzz created when users pass a message on to other users and sites.'),
 ('SEO / SEM / PPC', 'Search engine optimisation (organic ranking) / search engine marketing / pay-per-click (paid ranking by bid).'),
 ('Owned, paid, earned media', 'Your own property; placements you pay for; free exposure others give you.'),
])
w5_boss = ''.join([
 qa('Spell out SMART and give the four Ps plus the three added in the 7Ps.',
  '''<p>Specific, Measurable, Attainable, Relevant, Time-based. Product, price, promotion, place; plus people, process, physical evidence.</p>''', 1),
 qa('Compare product-based and customer-based marketing strategies with one pro and one con each.',
  '''<p>Product-based: pro, you focus on making the best product and build a quality reputation; con, you may ignore customers and their target market. Customer-based: pro, you give customers what they want, raising loyalty; con, research is costly and can distract from product quality.</p>''', 2),
 qa('What are the four bases of market segmentation, and what is the flow?',
  '''<p>Geographic, demographic, psychographic and behavioural. Flow: segmentation, then targeting, then positioning.</p>''', 3),
 qa('Name the seven stages of the customer lifecycle and say which CRM functions support it.',
  '''<p>Awareness, knowledge, consideration, selection, purchase, retention, advocacy. CRM&rsquo;s sales, marketing and customer service functions support each other along it.</p>''', 4),
 qa('List the seven factors for choosing online marketing tactics.',
  '''<p>Online goals, business environment, online audience, online competitors, site technology, internal resources, risk tolerance.</p>''', 5),
 qa('Describe the target marketing process and the five-step email marketing process.',
  '''<p>Attract strangers, convert visitors into leads, close leads as customers, delight customers into promoters. Email: define, test, send, measure, report.</p>''', 6),
 qa('Distinguish organic and paid search, and owned, paid and earned media.',
  '''<p>Organic search ranking comes from SEO; paid search uses pay-per-click bidding for top positions. Owned = your own property, paid = placements you pay for, earned = free exposure from others. Using all three together gives more return than the parts separately.</p>''', 7),
 qa('Why do the slides say branding and marketing work in harmony?',
  '''<p>Brand guidelines give marketing its outline (voice, purpose, look); marketing campaigns then reinforce the brand and spread awareness. Branding gives the identity, marketing shares it to drive sales. Too salesy marketing costs credibility.</p>''', 8),
])

# ====================================================================== mini project
w_mp = f'''
<section id="mini-project" class="band wx">
  <h2 class="sec">Mini project (40%): real digital marketing campaign</h2>
  <p class="small">From the project guidelines deck and the agenda document. The goal: promote a product or service with several kinds of digital content, then analyse the results. Groups of 4 (the deck says 231 students, so 45 groups of 4 and 1 group of 5). The product or service can be real or hypothetical.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Deliverable</th><th>When</th><th>Weight</th><th>Requirements</th></tr></thead><tbody>
  <tr><th>Campaign strategy and plan</th><td>Week 1</td><td>20% (strategic alignment)</td><td>Product or service, target audience, value proposition, marketing goals (for example awareness), content types and platform strategy (more than one platform allowed).</td></tr>
  <tr><th>Content and public deployment</th><td>Weeks 3 to 5</td><td>20% creativity + 30% engagement (agenda document)</td><td>At least 3 short videos of 1 to 3 minutes made with Canva or CapCut, plus posts; captions, subject lines and clear calls to action; published PUBLIC on at least 3 platforms; shareable links and screenshots kept as proof.</td></tr>
  <tr><th>Interactive dashboard</th><td>Weeks 14 to 15</td><td>20%</td><td>Excel or Power BI using the dataset shared on eLearn; must show goals and insights in a clear, creative layout, not just raw data.</td></tr>
  <tr><th>Pre-recorded presentation</th><td>Week 14</td><td>10% (with the report)</td><td>3 to 5 minute video: execution, performance numbers, dashboard insights, lessons learned.</td></tr>
  <tr><th>Final report (PDF)</th><td>Week 15, via eLearn</td><td>(included above)</td><td>5 to 7 pages minimum, no maximum, excluding cover and appendices; Arial or Times New Roman 12 pt; 1.5 line spacing; PDF.</td></tr></tbody></table></div>
  <h3>Roles, report layout, grading</h3>
  <div class="cards3">
    <div class="c"><h4>Roles</h4><p><b>Content creator</b>: visuals and videos. <b>Writer</b>: captions, calls to action, report drafting. <b>Researcher/analyst</b>: audience research, platform analytics and the dashboard. <b>Project manager</b>: timeline, proof of public posting, final submission.</p></div>
    <div class="c"><h4>Report sections</h4><p>Cover page, executive summary, campaign plan, content creation, deployment details (proof), performance analysis, key takeaways, appendices (optional).</p></div>
    <div class="c"><h4>Grading</h4><p>Creativity of content 20%, strategic alignment 20%, engagement results 30%, dashboard 20%, report and presentation quality 10%.</p></div>
  </div>
  <p class="small"><b>Mismatch in the files:</b> the guidelines deck gives engagement results as 20% (its list adds up to only 90%), but the agenda document gives 30%, and with 30% the list adds up to 100%. I used the agenda document&rsquo;s 30%. Confirm with the lecturer.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Where this page&rsquo;s notes help your project</th></tr></thead><tbody>
  <tr><td><b>My own links, not from the slides:</b> goals use the SMART rule (Topic 5); platform choice uses the seven tactic factors (Topic 5); content follows attract, convert, close, delight (Topic 5); the dashboard and engagement analysis follow the data-driven decisions idea (Topic 3); a clear brand voice follows branding (Topic 5).</td></tr></tbody></table></div>
</section>
'''

# ====================================================================== exclusive tips
def tip(n, group, scenario, opts, ans, why, basis):
    o = ''.join(f'<li><b>{l}.</b> {t}</li>' for l, t in opts)
    good = dict(opts)[ans]
    body = (f'<p>{scenario}</p><ol type="a" class="tipopts" style="list-style:none;padding-left:0">{o}</ol>'
            f'<p><b>Answer: {ans}.</b> {good}</p><p>{why}</p><p class="small"><b>Basis:</b> {basis}</p>')
    return qa(f'<small>{group}</small> {scenario[:110].split(".")[0]}&hellip;', body, n)

NB = 'Notes-backed'
RS = 'Reasoned from the notes'
NN = 'Not covered in the Weeks 1 to 5 decks'
tips_html = ''.join([
 tip(1, 'Pareto', 'A retailer finds that 20% of products cause 80% of returns. Using the Pareto Principle, the company should:',
     [('a', 'Increase discounts on top problematic products and other products'), ('b', 'Investigate and improve the top problematic products'), ('c', 'Ignore the returns because they are a minority, focus on top perform products'), ('d', 'Remove all top problematic products from the catalog')],
     'b', 'Pareto says a small part of the cause (20% of products) gives most of the effect (80% of returns), so effort on that small part pays most. Fixing it is the efficient move. Removing the products (d) throws away sales, discounts (a) do not address the cause, and ignoring (c) wastes the lever. <b>This question appears twice on the lecturer&rsquo;s slides (once headed TIPS) with the options in a different order, so learn the content: &ldquo;investigate and improve the top problematic products&rdquo;.</b>',
     f'{NB}: Topic 3 (Pareto, 20% effort gives 80% results). The slides state the principle; the application to returns is my reasoning.'),
 tip(2, 'Pareto', 'An e-commerce company notices that 80% of its revenue comes from 20% of its customers. According to the Pareto Principle, which strategy should the company prioritize?',
     [('a', 'Focus on nurturing relationship with the top 20% of customers'), ('b', 'Expand to entirely new markets to attract 80% customers'), ('c', 'Offer discounts randomly to all customers'), ('d', 'Focus marketing efforts evenly across all customers')],
     'a', 'The vital few customers bring most revenue, so protect and grow them. This also matches relationship marketing and the VIP segment in Topic 5.',
     f'{NB}: Topic 3 (Pareto) plus Topic 5 (VIPs segment, relationship marketing and CRM).'),
 tip(3, 'Pareto', 'An online retailer finds that 20% of its products account for 80% of total sales. Which action aligns with the Pareto Principle to optimize inventory?',
     [('a', 'Randomly promote low-selling products in social media such as tiktok with creative content'), ('b', 'Remove the top 20% of products to reduce inventory cost'), ('c', 'Focus on ensuring top-selling products are always in stock'), ('d', 'Stock all products equally al the time to avoid shortages')],
     'c', 'The top sellers carry most of the sales, so running out of them hurts most. Treating all products equally (d) ignores the 80/20 split; removing the top 20% (b) removes the sales.',
     f'{NB}: Topic 3 (Pareto); the inventory application is my reasoning.'),
 tip(4, 'Pareto', 'A digital marketing team discovers that 20% of campaigns generate 80% of leads. Which strategy is consistent with the Pareto Principle?',
     [('a', 'Focus 20% on brand awareness, ignoring conversions'), ('b', 'Run all campaigns equally regardless of results to maximize leads'), ('c', 'Analyze and replicate the top 20% of campaigns'), ('d', 'Stop all campaigns except the top 20% performers')],
     'c', 'Learn why the top campaigns work and repeat that. Option d is the trap: it also stops the other 80%, which still gives some results and may be needed (the slides never say to drop everything outside the 20%).',
     f'{NB}: Topic 3 (Pareto), Topic 5 (measuring campaigns). The trap reading is mine.'),
 tip(5, 'Pareto', 'A SaaS platform finds that 20% of reported issues cause 80% of customer complaints. What should the company do according to the Pareto Principle?',
     [('a', 'Respond to all complaints with the same priority all the time. Every complaint is important.'), ('b', 'Prioritize main issue and ignore minor issues to reduce effort and time in solving complaints ticket'), ('c', 'Reduce customer support staff to cut costs and time in solving complaints ticket'), ('d', 'Resolving the 20% of issues causing most complaints')],
     'd', 'Fix the vital few issues that cause most complaints. Option b sounds close but says &ldquo;ignore&rdquo; minor issues, which goes further than Pareto and is bad for customer support (Topic 3 operational framework: customer support must be fast and reliable).',
     f'{NB}: Topic 3 (Pareto; customer support). Choosing d over b is my reasoning on the wording.'),
 tip(6, 'Marketplace', 'A Malaysian seller debates setting up their own online site, aware that marketplaces drive high traffic but also charge fees, whereas their own site may require investment in marketing to attract buyers. Which statement BEST captures the trade-off between selling on marketplaces versus an independent e-commerce site?',
     [('a', 'Independent sites automatically guarantee top traffic based on organic and paid SEO'), ('b', 'Marketplaces provide traffic but charge fees, while independent sites may require more upfront marketing but yield greater profits per sale'), ('c', 'Owned sites always cheaper, safer and better for both seller and customer compared marketplace'), ('d', 'Marketplaces require no transaction fees and infrastructure setup compared owned websites')],
     'b', 'The only option that states both sides. Others use absolute words (&ldquo;guarantee&rdquo;, &ldquo;always&rdquo;, &ldquo;no fees&rdquo;), which are usually wrong. Topic 5 says SEO takes time and paid search costs money, so traffic is not automatic.',
     f'{RS}: Topic 4 (multi-channel, own site design), Topic 5 (SEO and PPC). The decks have no marketplace fee figures.'),
 tip(7, 'Marketplace', 'A Malaysian fashion retailer decides to build its own online store because the marketplace platform&rsquo;s layout and algorithm limit how products can be displayed and promoted. What is a primary advantage of having an independent online store compared to selling only on a marketplace?',
     [('a', 'Guaranteed top positioning on all search engines'), ('b', 'Full control over branding, user experience, and promotions'), ('c', 'Hidden customer fees and conflict from third parties.'), ('d', 'Lower initial marketing costs and high traffic')],
     'b', 'Your own site lets you apply the design-for-success rules (consistent brand, user experience, standing out) and run your own promotions. a and d are traps because a new site has no guaranteed traffic and needs marketing.',
     f'{NB}: Topic 4 (design for success: brand, user experience, stand out).'),
 tip(8, 'Marketplace', 'A local Malaysian artisan sells exclusively on TikTok Shop. After recent platform fee increases and tighter competition, their profit margins have shrunk significantly, yet most of their revenue still comes from this single channel. What is a primary strategic risk of depending heavily on one e-commerce platform like TikTok Shop?',
     [('a', 'Guaranteed seller and customer loyalty regardless of competition in online market'), ('b', 'Vulnerability to policy or fee changes that can suddenly reduce profitability'), ('c', 'High visibility and low cost maintenance infrastructure'), ('d', 'Improved brand reputation, trustworthiness and awareness inside outside Malaysia')],
     'b', 'The scenario itself shows it: fees rose and margins shrank. Relying on one channel puts the platform in control. This is the argument for multi-channel or omni-channel selling.',
     f'{RS}: Topic 4 (multi-channel versus single channel; the stage figure starts at single channel).'),
 tip(9, 'Marketplace', 'A small Malaysian beauty brand only lists products on TikTok Shop. While traffic is high, competition and algorithm changes frequently shift product visibility. What competitive disadvantage might arise from relying solely on TikTok Shop for sales?',
     [('a', 'Higher probability of being featured in TikTok live-sell sessions'), ('b', 'More control over pricing than independent stores'), ('c', 'Inability to gather detailed customer behavior data for strategic marketing'), ('d', 'Brand dilution and cash flow volatility')],
     'c', 'a and b are advantages, not disadvantages. Between c and d, c fits the notes: omni-channel and CRM depend on one integrated view of customer data, and a platform seller does not own that view. <b>This is my best pick, not a certain one; d is the second most likely.</b>',
     f'{RS}: Topic 4 (omni-channel unified customer data), Topic 5 (CRM and segmentation).'),
 tip(10, 'Marketplace', 'A Malaysian retailer notes its online sales grew significantly this year due to the overall surge in e-commerce adoption, especially as nearly two-thirds of Malaysians now shop online and platforms like TikTok Shop are rapidly gaining market share. Which strategic action should the retailer prioritize to leverage this trend?',
     [('a', 'Expand its presence on both Shopee and TikTok Shop and tailor offers for young online shoppers'), ('b', 'Maintain focus only on both online and physical store promotions'), ('c', 'Reduce its online advertising budget and focus on elderly shopper as well'), ('d', 'Start selling in own website because the market is saturated and the cost is rising on both shopee and tiktok')],
     'a', 'The market is growing and the platforms are where buyers are, so be on more than one (multi-channel) and tailor to a segment (segmentation). b, c and d move away from the growth. The retailer picks a segment, as in market segmentation.',
     f'{RS}: Topic 4 (multi-channel) and Topic 5 (segmentation and targeting).'),
 tip(11, 'Attention economy', 'In the context of the attention economy, which of the following strategies is most effective for an entrepreneur to create a strong online persona and capture the attention of potential customers?',
     [('a', 'Post content that highlights your personal story and the mission behind your brand'), ('b', 'Develop a personalized content strategy that resonates with the specific needs and interests of the target audience.'), ('c', 'Use content curation to share industry trends and updates, positioning yourself as a thought leader.'), ('d', 'Partner with influencers to regularly promote your products to reach a larger audience quickly.')],
     'b', 'The notes keep returning to the target audience: segment, know their needs, then fit content to them (customer-based strategy, content marketing plan starting with &ldquo;who are your people&rdquo;). Options a, c and d can all work, so <b>this is my pick by the notes, and the answer the lecturer expects may differ</b>. The term &ldquo;attention economy&rdquo; itself is not in the Weeks 1 to 5 decks.',
     f'{RS}: Topic 5 (segmentation, customer-based strategy, content marketing plan, branding).'),
 tip(12, 'Law', 'A Malaysian YouTuber films people in public and posts the video without their consent; someone&rsquo;s face is clearly visible and identifiable. Under Malaysian law (including PDPA considerations), what may apply?',
     [('a', 'A guaranteed licence requirement by FINAS'), ('b', 'No legal issues, as all public filming is allowed'), ('c', 'A copyright claim against the filmed individuals'), ('d', 'Possible civil action for privacy breach and defamation if individuals are identifiable and harmed')],
     'd', 'By elimination. b is too absolute. c is backwards: the filmed people are the ones who may complain, not the ones who would claim copyright over the creator&rsquo;s video. a says a licence is &ldquo;guaranteed&rdquo; to be required, which is too strong. d is the only option that matches a privacy and personal data concern. <b>Law is not covered in the Weeks 1 to 5 decks (the course covers it in the second half), so this answer is reasoned from general knowledge, not from your notes.</b>',
     f'{NN}. Course outcome CLO3 lists privacy, intellectual property and cyber law.'),
 tip(13, 'Law', 'A Malaysian YouTuber uploads clips from another creator&rsquo;s video without asking permission, and then monetizes the video. Under the Malaysian Copyright Act 1987, what legal issue is most likely to arise from this action?',
     [('a', 'Copyright infringement because the creator&rsquo;s exclusive rights were used without consent'), ('b', 'Moral rights requiring attribution of the creator'), ('c', 'Any use of copyrighted content is allowed if it&rsquo;s only on YouTube'), ('d', 'Fair dealing automatically covers all uses without consent')],
     'a', 'Using someone else&rsquo;s video without permission, then earning money from it, is the textbook case of copyright infringement. c and d use &ldquo;any&rdquo; and &ldquo;automatically&rdquo;, which are wrong. b is a real idea, but &ldquo;most likely&rdquo; points to infringement of the exclusive rights. <b>Not covered in the Weeks 1 to 5 decks, so this is general knowledge, not from your notes.</b>',
     f'{NN}. Course outcome CLO3 lists intellectual property.'),
])

w_tips = f'''
<section id="exclusive-tips" class="band wx">
  <h2 class="sec">Exclusive Tips</h2>
  <p class="small">These are the practice questions the lecturer showed in class (photos of the projector screen; one slide is headed &ldquo;TIPS&rdquo;). <b>The lecturer gave no answer key.</b> The answers below are my own, worked out from the notes on this page, and each one says how well the notes support it. The questions come in three clusters: Pareto (5), selling on a marketplace versus your own site (5, plus one on content strategy) and Malaysian law (2). Tap a question to see the answer and the reason. Try it first.</p>
  <ul class="chips-row"><li><b>Notes-backed</b>: the notes state the idea</li><li><b>Reasoned from the notes</b>: I applied the notes to the scenario</li><li><b>Not covered</b>: not in Weeks 1 to 5; general knowledge</li></ul>
  <p class="small"><b>Pattern across all 13 questions:</b> the right answer is the one that keeps to the idea of the lesson (Pareto: act on the vital few; marketplace: traffic versus control; own site: control but more marketing effort), and the wrong ones use absolute words such as &ldquo;always&rdquo;, &ldquo;guaranteed&rdquo;, &ldquo;automatically&rdquo; or &ldquo;ignore&rdquo;. That pattern is my observation, not a rule from the slides.</p>
  {tips_html}
</section>
'''

# ====================================================================== story, cheat sheet, flashcards
story = [
 (1, 'What does this course want from me?', 'A two-part course with tests, a big project and two lecturers is hard to plan for.',
  'Learn the map: the coursework split, the CLOs, the schedule, the rules.',
  'Why does the course aim at business and AI skills? Because the graduate world has changed.'),
 (2, 'The Augmented Marketer', 'Technology and GenAI changed what employers value, and a degree alone is not enough.',
  'Build skills, show a portfolio, use human plus AI, and think like an entrepreneur.',
  'Once you have an idea, how do you actually run the business?'),
 (3, 'Operating an e-business', 'Running a business means long-term goals, plans and daily work, and an owner cannot do it all.',
  'Strategic, tactical and operational levels; Pareto and Eisenhower for time; RevOps and technology tools.',
  'A well-run business still needs a way to earn money.'),
 (4, 'Selling on the web', 'The business must bring in revenue and keep customers on its site.',
  'Revenue models, web catalog, multi-channel to omni-channel, and design for success.',
  'A good shop earns nothing if nobody finds it.'),
 (5, 'Marketing on the web', 'People have to know the site exists, trust it and come back.',
  'SMART goals, segmentation, CRM, tactics, email, branding, viral, SEO and PPC, and the owned-paid-earned mix.',
  'The lectures stop here; the next lecturer moves to future technology, ethics and law (Weeks 9 to 12).'),
]
story_html = '<ol class="story">' + ''.join(
    f'<li class="w{n}"><a href="#week-{n}"><span class="wk">Topic {n}</span><h3>{t}</h3>'
    f'<p><b>Problem</b>{p}</p><p><b>Fix</b>{s}</p><p class="but"><b>But then</b>{b}</p></a></li>' for n, t, p, s, b in story) + '</ol>'

numbers = [('40 / 20 / 30 / 10', 'tests / assignment / project / project presentation (%)'), ('20 + 20', 'two tests of 20% each'),
           ('6 Nov 2026', 'Test 1, 8.30 to 9.30 am, Dewan Utama Peperiksaan D (L17)'), ('18 Dec 2026', 'Test 2'),
           ('4', 'course learning outcomes'), ('7', 'skills in the new graduate skill stack'), ('3', 'levels: strategic, tactical, operational'),
           ('80 / 20', 'Pareto: 20% of effort gives 80% of results'), ('20 / 60 / 20', 'time split: strategy / routine / force majeure'),
           ('5', 'web revenue models'), ('4', 'channel stages: single, multi, cross, omni'), ('5', 'design-for-success rules'),
           ('7', 'rules; actually 7 web presence objectives and 7 factors for selecting tactics'), ('4 and 7', '4Ps and 7Ps'),
           ('4', 'segmentation bases'), ('7', 'customer lifecycle stages'), ('4', 'adopter stages'), ('5', 'email marketing process steps'),
           ('35%', 'paid search conversion advantage over organic (slide, MarketLive)'), ('40%', 'mini project (30% project + 10% presentation)'),
           ('3 / 3 / 1-3 min', 'platforms, short videos, minutes per video'), ('5 to 7', 'minimum report pages')]
numbers_html = '<ul class="nums">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in numbers) + '</ul>'
traps = [
 'The 20/60/20 time split (strategy, routine, force majeure) is not the same as the 80/20 Pareto rule.',
 'Pareto says act on the vital few. It does <b>not</b> say to ignore the rest or remove the top 20%.',
 '<b>Multi-channel</b> = many channels, each separate. <b>Omni-channel</b> = all joined with one customer view.',
 'Freemium = free tier + paid premium. Subscription = recurring payment. Do not mix them up.',
 'AdWords/Google Ads shows ads on search results. AdSense shows ads on your own website and pays you per click.',
 'Organic search ranking comes from SEO; paid search is pay-per-click bidding.',
 'Owned = your own property; paid = you pay; earned = others give free exposure.',
 '4Ps are product, price, promotion, place. People, process and physical evidence are the extra three of the 7Ps.',
 'Product-based strategy can neglect customers; customer-based strategy can be costly.',
 'RevOps joins sales, marketing and customer service. CRM manages the customer relationship.',
 'Absolute words in options (always, guaranteed, automatically, ignore) are usually the trap.',
 'Mini project engagement weight: guidelines deck says 20%, agenda document says 30%. Confirm with the lecturer.',
 'Week labels in the files do not always match the schedule (the Operating E-business deck says Week 6).',
]
traps_html = '<ul class="traps">' + ''.join(f'<li>{t}</li>' for t in traps) + '</ul>'
cards = [
 ('CAT402 coursework split', 'Tests 40%, assignment 20%, project 30%, project presentation 10%.'),
 ('Two parts of CAT402', 'Technopreneurship development; professional development.'),
 ('Opportunity formula', 'Skill + real problem + digital tool + customer = possible value.'),
 ('Safe AI habit', 'Prompt, understand, verify, adapt, create. Not prompt, copy, submit.'),
 ('Human vs GenAI', 'GenAI: fast, scalable, drafts. Humans: context, judgement, responsibility, trust, relationships.'),
 ('Seven-skill stack', 'Domain, digital, communication, critical thinking, problem solving, AI literacy, entrepreneurial mindset.'),
 ('Strategic / tactical / operational', 'Long-term goals / plans that serve them / daily execution.'),
 ('Pareto principle', '20% of effort gives 80% of results. Focus on the vital few.'),
 ('Eisenhower time split in the slides', '20% strategy, 60% routine, 20% force majeure.'),
 ('Strategic framework: three areas', 'Business objectives, infrastructure investment, revenue operations integration.'),
 ('Tactical framework: four parts', 'Marketing campaigns, CRM, automation, integrating RevOps.'),
 ('Operational framework: three parts', 'Order fulfilment and logistics, customer support, RevOps execution.'),
 ('RevOps', 'Aligns sales, marketing and customer service on shared data, tools and processes to grow revenue.'),
 ('How Zalora escaped stagnation', 'Partnerships with payment and logistics firms; AI and machine learning.'),
 ('Five web revenue models', 'Web catalog, digital content, advertising-supported, advertising-subscription mixed, fee-based.'),
 ('Freemium', 'Free tier plus paid premium, for example Spotify.'),
 ('Subscription advantages', 'Loyal users, predictable revenue, predictable pipeline.'),
 ('Multi-channel vs omni-channel', 'Multi: many separate channels. Omni: one unified experience and customer view.'),
 ('Five design-for-success rules', 'First impression, user experience, consistent brand, colour palette, stand out.'),
 ('SMART', 'Specific, measurable, attainable, relevant, time-based.'),
 ('Segmentation bases', 'Geographic, demographic, psychographic, behavioural.'),
 ('Segmentation flow', 'Segmentation, targeting, positioning.'),
 ('Customer lifecycle', 'Awareness, knowledge, consideration, selection, purchase, retention, advocacy.'),
 ('Seven factors for selecting tactics', 'Goals, environment, audience, competitors, site technology, resources, risk tolerance.'),
 ('Target marketing process', 'Attract, convert, close, delight (strangers, visitors, leads, customers, promoters).'),
 ('Email marketing process', 'Define, test, send, measure, report.'),
 ('Three brand-loyalty questions', 'Did it perform as expected? Was quality as promised or better? Was the whole experience positive?'),
 ('Owned, paid, earned', 'Your property; placements you pay for; free exposure from others.'),
 ('Mini project minimums', 'Groups of 4; 3 platforms, public; 3 short videos (1 to 3 min); 5 to 7 page PDF; 3 to 5 min video; dashboard in Excel or Power BI.'),
]
cards_html = '<div class="cards" id="cards">' + ''.join(
    f'<button class="card" type="button" aria-pressed="false"><span class="front">{q}</span><span class="back">{a}</span></button>' for q, a in cards) + '</div>'
N_CARDS = len(cards)

weeks_html = ''.join([
 week(1, '', 'Course overview and coursework', 'The two parts, the marks, the dates and the rules.',
      psn('A two-part course with tests, a project and two lecturers is hard to plan for.',
          'A map of the coursework split, learning outcomes, weekly plan and class rules.',
          'Why aim at business and AI skills? The graduate world has changed.'), MAPS[1], w1_vis, w1_terms, w1_boss),
 week(2, '', 'The Augmented Marketer: you in the GenAI era', 'Staying valuable when technology changes.',
      psn('GenAI and technology changed what employers value; a degree is not enough.',
          'Build skills, show a portfolio, use human plus AI, and keep an entrepreneurial mindset.',
          'With an idea in hand, how do you run the business?'), MAPS[2], w2_vis, w2_terms, w2_boss),
 week(3, '', 'Operating your e-business', 'Strategy, tactics and operations, with time tools and technology.',
      psn('Running a business needs long-term goals, plans and daily work, and an owner cannot do it all.',
          'Three levels; Pareto and Eisenhower for time; RevOps and tools across the levels.',
          'A well-run business still needs revenue.'), MAPS[3], w3_vis, w3_terms, w3_boss),
 week(4, '', 'Selling on the web', 'How an online business earns money and keeps its visitors.',
      psn('The business must bring in revenue and keep customers on its site.',
          'Choose a revenue model, manage the catalog, sell through multiple or all channels, and design for success.',
          'A good shop earns nothing if nobody finds it.'), MAPS[4], w4_vis, w4_terms, w4_boss),
 week(5, '', 'Marketing on the web', 'Goals, segments, relationships, tactics, brands and search.',
      psn('People have to know the site exists, trust it and return.',
          'SMART goals, segmentation, CRM, tactic selection, email, branding, viral marketing, SEO and PPC, and an owned-paid-earned mix.',
          'The lecture decks stop here. Weeks 9 to 12 (another lecturer) cover future technology and projects, which are not in the folder.'), MAPS[5], w5_vis, w5_terms, w5_boss),
])
nav = ('<a class="wx" href="#big-picture">Big picture</a>' + ''.join(f'<a class="w{n}" href="#week-{n}">Topic {n}</a>' for n in range(1, 6))
       + '<a class="wx" href="#mini-project">Mini project</a><a class="wx" href="#exclusive-tips">Exclusive Tips</a><a class="wx" href="#cheat-sheet">Cheat sheet</a><a class="wx" href="#drill">Flashcards</a>')

CSS = (open(os.path.join(HERE, 'style.css')).read() + open(os.path.join(HERE, 'extra_cst.css')).read()
       + open(os.path.join(HERE, 'bigp.css')).read() + open(os.path.join(HERE, 'extra_cmt323.css')).read())
JS = open(os.path.join(HERE, 'script.js')).read()

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#060510">
<title>CAT402 Notes: Professional and Technopreneurship Development</title>
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
  <img class="subj" src="../assets/subjects/cat402.svg" width="96" height="96" alt="">
  <p class="eyebrow">CAT402 · Professional and Technopreneurship Development</p>
  <h1>Topics 1 to 5, as one story</h1>
  <p class="lead">Every topic exists because the one before it left a gap. Read it as <b>problem, solution, new problem</b>, and the facts hang together.</p>
  <nav class="jump" aria-label="Jump to a section">{nav}</nav>
</header>
<main>

<section id="big-picture" class="bigp wx">
  <h2 class="sec">Big picture: read this first</h2>
  <p class="headsup"><b>One question runs through all five topics:</b> how does a graduate turn a skill into an online business that earns money, runs well and gets found? Topic 1 is the course map. Topic 2 says why: technology and AI changed what a graduate must offer. Topics 3 to 5 then build the business: run it (operate), earn from it (sell), and get customers to it (market).</p>
  <h3>The chain: each topic fixes a gap the last one left</h3>
  <ol class="chain">
    <li class="w1"><span class="tn">Topic 1</span><b>Course overview</b><span class="kw">Two parts, coursework, CLOs, schedule, rules</span><span class="bridge">But why business and AI skills? &hellip;</span></li>
    <li class="w2"><span class="tn">Topic 2</span><b>The Augmented Marketer</b><span class="kw">Career model, GenAI, human plus AI, opportunity formula, portfolio</span><span class="bridge">But how do you run the business? &hellip;</span></li>
    <li class="w3"><span class="tn">Topic 3</span><b>Operating an e-business</b><span class="kw">Strategic, tactical, operational; Pareto; RevOps; tools</span><span class="bridge">But how does it earn money? &hellip;</span></li>
    <li class="w4"><span class="tn">Topic 4</span><b>Selling on the web</b><span class="kw">Revenue models, catalog, channels, design</span><span class="bridge">But nobody knows it exists &hellip;</span></li>
    <li class="w5"><span class="tn">Topic 5</span><b>Marketing on the web</b><span class="kw">SMART, segments, CRM, tactics, email, brand, search</span><span class="bridge">The decks stop here; Weeks 9 to 12 move to future technology, projects and (per the synopsis) ethics and law.</span></li>
  </ol>

  <h3>How Topic 1 connects to Topic 5</h3>
  <p class="small">Topic 1 sets the aim: a business plan and an e-business that works across platforms and channels, with marketing and protection from threats (CLO2). Topics 3 to 5 are that outcome in pieces: running it (3), selling across channels (4) and marketing it (5). Topic 2 supplies the person: the skills and mindset. The mini project then asks you to do the Topic 5 steps for real.</p>
  <div class="promise tbl-wrap"><table><thead><tr><th>Topic 1 raised &hellip;</th><th>Answered in &hellip;</th></tr></thead><tbody>
    <tr><td>Define the business idea (CLO1)</td><td><b>Topic 2</b> (opportunity formula, mindset).</td></tr>
    <tr><td>E-business plan across platforms and channels (CLO2)</td><td><b>Topic 3</b> (operating levels), <b>Topic 4</b> (channels, revenue models).</td></tr>
    <tr><td>Marketing strategies, including affiliate marketing (CLO2)</td><td><b>Topic 4</b> (affiliate model), <b>Topic 5</b> (marketing).</td></tr>
    <tr><td>Mini project campaign</td><td><b>Topic 5</b> and the Mini project section.</td></tr>
    <tr><td>Ethics, law, privacy (CLO3)</td><td>Not in these five decks; later weeks. Two Exclusive Tips questions touch it.</td></tr></tbody></table></div>

  <h3>Four threads that run through all five topics</h3>
  <p class="small">These links are my own summary of the slides, to show how the topics connect. They are not slide text.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Thread</th><th class="t2">Topic 2</th><th class="t3">Topic 3</th><th class="t4">Topic 4</th><th class="t5">Topic 5</th></tr></thead><tbody>
    <tr><th>Focus on what matters most</th><td>Check AI, keep human judgement</td><td>Pareto 80/20, Eisenhower</td><td>Standing out, clear design</td><td>Segments, VIPs, targeting</td></tr>
    <tr><th>Know the customer</th><td>Customer in the opportunity formula</td><td>CRM, personalised ads</td><td>Omni-channel customer view</td><td>Segmentation, CRM, lifecycle</td></tr>
    <tr><th>Use data</th><td>Dashboard case</td><td>Real-time analytics, RevOps</td><td>Catalog data quality</td><td>Measure opens and clicks</td></tr>
    <tr><th>Technology as helper</th><td>GenAI</td><td>Cloud, automation, AI</td><td>Platforms, ad networks</td><td>Email tools, SEO, PPC</td></tr></tbody></table></div>

  <h3>If you remember only five sentences</h3>
  <ol class="five">
    <li><b>Topic 1:</b> CAT402 mixes technopreneurship and professional development, marked by tests (40%), an assignment (20%), a project (30%) and a presentation (10%).</li>
    <li><b>Topic 2:</b> in the GenAI era you stay valuable through skills, a portfolio, human plus AI and an entrepreneurial mindset, and you check AI instead of copying it.</li>
    <li><b>Topic 3:</b> an e-business is run at strategic, tactical and operational levels, using Pareto and Eisenhower for time and RevOps and technology to join the teams.</li>
    <li><b>Topic 4:</b> an online business earns through revenue models such as catalog, digital content and advertising, sells across channels toward omni-channel, and wins with good design.</li>
    <li><b>Topic 5:</b> web marketing starts from SMART goals and segments, builds relationships through CRM, picks tactics by seven factors, and mixes owned, paid and earned channels.</li>
  </ol>
</section>

<section id="story" class="band">
  <h2 class="sec">Previously on CAT402</h2>
  <p class="small">Tap a card to jump to that topic. Read the "But then" line, then the next card&rsquo;s "Problem": they are the same sentence.</p>
  {story_html}
</section>
{weeks_html}
{w_mp}
{w_tips}
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
<footer class="foot"><p>Built from the CAT402 lecture decks (five lectures), the mini project guidelines and agenda, and the lecturer&rsquo;s practice questions. The slides belong to their lecturers and publishers (Weeks 4 and 5 carry a Cengage Learning copyright line); this page is a student&rsquo;s own summary in own words, with redrawn diagrams. Items marked "my own" are not from the slides. The Exclusive Tips answers are not an official answer key.</p></footer>
<script>
{JS}
</script>
</body>
</html>'''
open(os.path.join(OUT, 'index.html'), 'w').write(PAGE)
print('cat402 ok', len(PAGE), 'cards', N_CARDS)
