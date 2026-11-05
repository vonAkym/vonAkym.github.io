#!/usr/bin/env python3
"""CSE341 (CKS221/CSE 341) Software Architecture and Design notes page, built from the user's 6 lecture decks
plus the supplementary "views" deck. Content rules: only what is in the decks; anything that is my own summary,
example or reading is labelled on the page. Diagrams are redrawn as inline SVG, not copied from the slides.

Six topics, one per lecture deck (the decks themselves call them Topic 1 and Topic 2 Parts 1 and 2):
  Topic 1 = Lecture 1 (what is architecture), Topic 2 = Lecture 2 (why it matters, documenting, 4+1 views),
  Topic 3 = Lecture 3 (general architectural styles), Topic 4 = Lecture 4 (module views, first four module styles),
  Topic 5 = Lecture 5 (aspects and data model styles), Topic 6 = Lecture 6 (C&C and allocation styles).
The supplementary "views" deck (example figures only) has its own section, id="supplement"."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root (the folder that GitHub Pages serves)
from notes_lib import mindmap, terms, psn, qa, week, E

OUT = os.path.join(ROOT, 'cse341')
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
1: mindmap('Software Architecture',
  [('What it is', ['A set of software structures', 'An abstraction of the system', 'Public details only', 'Every system has one', 'Not every one is good']),
   ('What it does', ['Shows qualities to stakeholders', 'Focuses on structure', 'Flags costly choices early', 'Basis for core decisions']),
   ('Structure vs view', ['Structure: elements as they exist', 'View: a representation of one', 'Architects design structures', 'Architects document views'])],
  [('Module structures', ['Static code units', 'Who may use whom', 'Inheritance relations', 'Reason about modifiability']),
   ('C&C structures', ['Runtime components', 'Connectors between them', 'Shared data stores', 'Reason about performance']),
   ('Allocation structures', ['Software to processors', 'Software to files and folders', 'Modules to teams']),
   ('Analogy', ['Building: needs then blueprints', 'Body: skeleton, veins, X-ray', 'Web: documents or computers'])],
  'Mind map of Topic 1: what software architecture is, what it does, and the three kinds of structure'),
2: mindmap('Why Architecture Matters',
  [('Why it matters', ['Reason about change as it evolves', 'Predict qualities early', 'Communication among stakeholders', 'Constraints on implementation', 'Assemble, not only create', 'Reason about cost and schedule', 'Reusable core of a product line']),
   ('Quality attributes', ['Performance', 'Modifiability', 'Security', 'Scalability'])],
  [('Why document it', ['An artifact: a document', 'Education: new people', 'Communication: all roles', 'Analysis and construction']),
   ('Views', ['One picture fits no one', 'Document the relevant views', 'Then add what spans views', 'Not all views are needed']),
   ('4+1 view model', ['Logical view', 'Process view', 'Development view', 'Physical view', 'Use case view (the +1)'])],
  'Mind map of Topic 2: why architecture matters, why to document it, and the 4+1 view model'),
3: mindmap('Architectural Styles',
  [('What a style gives', ['Components that do a job', 'Connectors that link them', 'Constraints on joining them', 'Semantic models']),
   ('Request and peer styles', ['Client-server', 'Peer-to-peer', 'Service oriented (SOA)', 'Microservice']),
   ('Event and data styles', ['Event-driven (EDA)', 'Data-centered', 'Data flow: pipe-and-filter'])],
  [('Structure styles', ['Layered pattern', 'Main program / subprogram']),
   ('EDA parts', ['Event', 'Event producer', 'Event consumer', 'Event broker']),
   ('Layered ERP example', ['User interaction layer', 'Functionality layer', 'Business rules layer', 'Application core layer', 'Database layer']),
   ('Why styles exist', ['Same choices recur', 'Better properties result'])],
  'Mind map of Topic 3: the nine general architectural styles and what a style contains'),
4: mindmap('Module Views',
  [('Parts of a module view', ['Elements: modules', 'Relations', 'Constraints', 'What it is for', 'Properties on each module']),
   ('Relations', ['Is-part-of', 'Depends-on', 'Is-a']),
   ('Notations', ['Informal boxes', 'UML packages and classes', 'Dependency structure matrix']),
   ('Limit', ['Static, no runtime view', 'Map to C&C views'])],
  [('Decomposition', ['Is-part-of, no loops', 'One parent per module']),
   ('Uses', ['Uses: depends on correct B', 'Hard to deliver if loops or long chains']),
   ('Generalization', ['Is-a: commonality, variation', 'Abstract modules']),
   ('Layered', ['Allowed-to-use, one direction', 'At least two layers', 'Stack, rings, sidecar'])],
  'Mind map of Topic 4: module views, their relations and notations, and the first four module styles'),
5: mindmap('Aspects and Data Model',
  [('Aspects style', ['Crosscutting concerns', 'Aspect modules', 'Crosscuts relation', 'Access control, transactions, logging']),
   ('Where it comes from', ['Aspect-oriented programming', 'Complements OOP', 'Shown as stereotyped UML classes'])],
  [('Data model style', ['Elements: data entities', 'Name, attributes, primary key', 'Access rules']),
   ('Notations', ['Crow foot ERD', 'UML class diagram']),
   ('Relations', ['One-to-one, one-to-many', 'Many-to-many', 'Generalization, aggregation'])],
  'Mind map of Topic 5: the aspects style and the data model style'),
6: mindmap('Runtime and Allocation',
  [('C&C view basics', ['Components and connectors', 'One relation: attachment', 'Ports attach to roles', 'Runtime behaviour', 'Properties for analysis']),
   ('Call-return', ['Client-server', 'Peer-to-peer', 'SOA']),
   ('Data flow', ['Pipe-and-filter', 'Batch sequential']),
   ('Event-based', ['Publish-subscribe', 'SOA']),
   ('Repository', ['Shared data', 'Blackboard'])],
  [('Allocation views', ['Maps software to non-software', 'Deployment style', 'Install style', 'Work assignment style']),
   ('Deployment', ['Processes to hardware', 'Allocated-to', 'Migrates-to', 'Copy-migrates-to']),
   ('Install', ['Components to files and folders', 'Allocated-to, containment', 'Folders form a tree']),
   ('Work assignment', ['Modules to teams', 'Allocated-to', 'Basis for budget and schedule'])],
  'Mind map of Topic 6: component-and-connector styles and the three allocation styles'),
}

# ====================================================================== topic 1 visuals
d_cat = svg(700, 262,
    box(20, 14, 200, 66, ['Module structures', 'static code units'], small_rest=True)
    + box(250, 14, 200, 66, ['C&C structures', 'runtime parts'], small_rest=True)
    + box(480, 14, 200, 66, ['Allocation structures', 'software meets the world'], small_rest=True)
    + arr(120, 80, 120, 124, 'ct') + arr(350, 80, 350, 124, 'ct') + arr(580, 80, 580, 124, 'ct')
    + box(20, 124, 200, 112, ['Good for reasoning', 'about modifiability:', 'who does what, who', 'may use whom'], 'bx', bold=False)
    + box(250, 124, 200, 112, ['Good for reasoning', 'about performance,', 'security, availability', 'while it runs'], 'bx', bold=False)
    + box(480, 124, 200, 112, ['Maps software onto', 'CPUs, file systems,', 'networks and', 'development teams'], 'bx', bold=False)
    + txt(350, 256, 'Redrawn from the slide text. The slides say the first two sets of structures are linked to the third by allocation.', 'ts'),
    'Redrawn: the three categories of architectural structure and what each is used to reason about', 'ct')

w1_vis = f'''
  <h3>The big idea</h3>
  <p class="small">The slides open with one sentence: studying software architecture is studying how software systems are designed and built. Software architecture is the foundational element of software design. It means understanding and organising a system, its components, how they interact, the environment they run in, and the core principles used to design the software.</p>
  <h4>The building analogy (from the slides)</h4>
  <div class="tbl-wrap"><table><thead><tr><th>Step</th><th>Building a house</th><th>Building software</th></tr></thead><tbody>
  <tr><th>1</th><td>Requirements for the building are collected</td><td>Requirements are specified</td></tr>
  <tr><th>2</th><td>A design is created to satisfy them</td><td>A high-level design is created</td></tr>
  <tr><th>3</th><td>The design is refined into elaborate blueprints</td><td>Detailed algorithms are developed from that design</td></tr>
  <tr><th>4</th><td>Construction follows the blueprints</td><td>Code is written to implement the algorithms</td></tr>
  <tr><th>5</th><td>The building is occupied and used</td><td>The system is deployed, used and maintained</td></tr></tbody></table></div>

  <h3>What is architecture? Four ideas</h3>
  <div class="cards3">
    <div class="c"><h4>1. A set of structures</h4><p>A <b>structure</b> is a set of elements held together by a relation. Software systems are made of many structures.</p></div>
    <div class="c"><h4>2. An abstraction</h4><p>It selects some details and hides others. Elements talk through <b>interfaces</b>, which split an element into public and private details. Architecture is about the public side only.</p></div>
    <div class="c"><h4>3. Every system has one</h4><p>Any system can be shown to have elements and relations among them, which is enough to reason about it.</p></div>
    <div class="c"><h4>4. Not all are good</h4><p>The definition does not care whether the architecture is a good one or a bad one.</p></div>
  </div>
  <h4>What architecture is used for</h4>
  <ul class="chips-row"><li>Helps stakeholders see, understand and analyse a system&rsquo;s qualities</li><li>Focuses on structure, not implementation</li><li>Anticipates expensive choices before they are made</li><li>Basis for core decisions and high-quality work</li></ul>

  <h3>Structures and views</h3>
  <div class="two"><div><h4>Structure</h4><p>The set of elements itself, as it exists in software or hardware.</p></div>
  <div><h4>View</h4><p>A representation of a coherent set of architectural elements and the relations among them, written by and read by stakeholders. In short: a view is a representation of a structure.</p></div></div>
  <p class="small">The slides put it this way: architects <b>design</b> structures, and <b>document</b> views of those structures. They also use a body analogy: a skeleton picture, a blood-vessel picture and an X-ray are three different views of one body. They look different and have different properties, yet they are all related and together describe the body. So to talk about an architecture you must say which structure and view you mean.</p>

  <h3>The three categories of structure</h3>
  {d_cat}
  <div class="tbl-wrap"><table><thead><tr><th>Category</th><th>Elements and relations</th><th>Questions it answers (from the slides)</th></tr></thead><tbody>
  <tr><th>Module</th><td>Implementation units (modules) with assigned responsibilities. Relations: is part of, depends on, is a. Layers are an aggregation of modules. Example notation: UML package and class diagrams.</td><td>What is each module responsible for? What may it use, and what does it actually use? Which modules are related by inheritance?</td></tr>
  <tr><th>Component-and-connector (C&amp;C)</th><td>Components: encapsulated, replaceable parts with runtime behaviour. Connectors: pathways of interaction between them. Components have ports; ports have interfaces; ports attach to connector roles.</td><td>What are the major executing components and how do they interact? Which data stores are shared? Which parts are replicated, or can run in parallel? How does data flow through the system? Can the structure change while running?</td></tr>
  <tr><th>Allocation</th><td>Mappings from software structures to non-software ones: deployment (software to hardware), implementation (modules to files in development, test and build environments), work assignment (modules to teams).</td><td>Which processor does each element run on? Where is each element stored during development, testing and building? Which team builds it?</td></tr></tbody></table></div>
  <p class="small">The deck also shows the web as an example: one view is a collection of linked documents seen through a browser (HTTP, URI, MIME and HTML are the standards), another is a set of computers joined by the Internet as clients and servers. Same system, different views. The slides finish with a figure of the architecture design activity and a case study (a CS One-Stop Portal) that are pictures only, so they are not reproduced here.</p>
'''
w1_terms = terms([
 ('Software architecture', 'The foundational element of software design: understanding and organising a system, its components, their interactions, the environment, and the principles used to design it.'),
 ('Structure', 'A set of elements held together by a relation; the elements as they exist in software or hardware.'),
 ('View', 'A representation of a coherent set of architectural elements and their relations, written and read by stakeholders. A representation of a structure.'),
 ('Abstraction', 'Selecting certain details and suppressing others. Architecture keeps the public side of an element and leaves its private details out.'),
 ('Interface', 'What an element shows to others. It partitions an element into public and private details.'),
 ('Module structure', 'Software split into implementation units (modules), each with specific responsibilities. Static.'),
 ('Component-and-connector structure', 'Elements with runtime behaviour (components) and their interactions (connectors).'),
 ('Allocation structure', 'Relations between software elements and non-software elements such as CPUs, file systems, networks and development teams.'),
 ('Component', 'An encapsulated, replaceable system element with runtime behaviour.'),
 ('Connector', 'A pathway of interaction between components.'),
 ('Deployment / implementation / work assignment structure', 'Software to hardware; modules to files in development, test and build environments; modules to the teams who build them.'),
])
w1_boss = ''.join([
 qa('Give the slide definition of architecture in your own words using the four ideas.',
  '''<ol><li>It is a <b>set of software structures</b> (elements held together by relations).</li><li>It is an <b>abstraction</b>: some details are chosen, others hidden. Only the public side of an element&rsquo;s interface is architectural.</li><li><b>Every</b> system has an architecture.</li><li>An architecture can be <b>good or bad</b>; the definition does not judge.</li></ol>''', 1),
 qa('What is the difference between a structure and a view? Who does what with each?',
  '''<p>A <b>structure</b> is the set of elements as they exist in the software or hardware. A <b>view</b> is a representation of a structure, written for stakeholders to read. <b>Architects design structures and document views of them.</b></p>''', 2),
 qa('Name the three categories of structure and say what each one is mainly used to reason about.',
  '''<ul><li><b>Module:</b> static code units. The slides call them the primary tool for reasoning about <b>modifiability</b>.</li><li><b>Component-and-connector:</b> runtime behaviour. Used for runtime properties such as <b>performance, security and availability</b>.</li><li><b>Allocation:</b> maps software onto non-software things (CPUs, file systems, networks, teams).</li></ul>''', 3),
 qa('Why does the slide deck show a skeleton, a blood-vessel picture and an X-ray?',
  '''<p>They are three different views of one body. They are drawn differently and have different properties, yet they are all connected and together describe the body. Software is the same: no single diagram shows everything, so you must say which structure and view you are using.</p>''', 4),
 qa('Which questions do module, C&amp;C and allocation structures each answer? Give one for each.',
  '''<ul><li><b>Module:</b> what other modules is this module allowed to use?</li><li><b>C&amp;C:</b> which parts of the system can run in parallel?</li><li><b>Allocation:</b> which team is each software element assigned to (or which processor does it run on)?</li></ul><p>Other questions are on the list above; any one per category is fine.</p>''', 5),
])

# ====================================================================== topic 2 visuals
d_41 = svg(700, 298,
    box(20, 18, 210, 84, ['Logical view', 'problem-domain', 'classes and objects'], small_rest=True)
    + box(470, 18, 210, 84, ['Process view', 'interacting runtime', 'processes'], small_rest=True)
    + box(20, 196, 210, 84, ['Development view', 'modules, libraries,', 'packages, subsystems'], small_rest=True)
    + box(470, 196, 210, 84, ['Physical view', 'hardware and where', 'software is placed'], small_rest=True)
    + box(255, 107, 190, 84, ['Use case view', 'the +1: ties the', 'other four together'], 'bxs')
    + ln(230, 60, 255, 128, True) + ln(470, 60, 445, 128, True) + ln(230, 238, 255, 170, True) + ln(470, 238, 445, 170, True),
    'Redrawn: the 4+1 view model, with the use case view tying together the logical, process, development and physical views', 'v41')

w2_vis = f'''
  <h3>Why architecture matters</h3>
  <p class="small">The slides give seven reasons. Together they say that the architecture decides whether the system will be good, and that it is the one thing everyone can talk about early.</p>
  <ol class="five">
    <li class="w2"><b>Reason about and manage change</b> as the system evolves.</li>
    <li class="w2"><b>Predict qualities early</b>, before the system exists.</li>
    <li class="w2"><b>Communicate</b>: a documented architecture helps stakeholders talk to each other.</li>
    <li class="w2"><b>Constrain</b> the choices made later in implementation.</li>
    <li class="w2"><b>Assemble</b>: architecture-based development focuses on putting components together, not only creating them.</li>
    <li class="w2"><b>Cost and schedule</b>: the architect and project manager can reason about both.</li>
    <li class="w2"><b>Reuse</b>: it can be a transferable, reusable model at the heart of a product line.</li>
  </ol>
  <h4>Good software and quality attributes</h4>
  <p class="small">Good software delivers the required functionality <i>and</i> quality. Architecture is largely about achieving quality attributes, and a system&rsquo;s quality attributes are substantially determined by its architecture. So the architect has to document enough that the architecture can be analysed to see whether the system built from it will have the qualities needed.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Attribute</th><th>What the architecture should do (from the slides)</th></tr></thead><tbody>
  <tr><th>Performance</th><td>Focus on time-based behaviour of elements, shared resources, and the frequency and volume of communication between elements.</td></tr>
  <tr><th>Modifiability</th><td>Limit interactions (coupling) so that each change affects only a small number of elements, ideally one.</td></tr>
  <tr><th>Security</th><td>Build authorization into the architecture to guard against intrusion; design safeguards and a recovery mechanism.</td></tr>
  <tr><th>Scalability</th><td>Avoid hard-coding resource assumptions or limits.</td></tr></tbody></table></div>

  <h3>Why document the architecture?</h3>
  <p class="small">Documentation is the creation of an artifact: a document, which may be electronic files, web pages, a whiteboard snapshot or paper. So documenting an architecture is a concrete task: producing a software architecture document. The slides add a joke by Steuart Henderson Britt: an undocumented architecture is a wink in the dark, you know what you are doing but nobody else does.</p>
  <div class="cards3">
    <div class="c"><h4>1. Education</h4><p>Introduce people to the system: new team members, outside analysts, a new architect, or a first-time customer who must approve funding.</p></div>
    <div class="c"><h4>2. Communication</h4><p>The main way different stakeholders talk. It gives a rough way to gauge progress and the work left, and a framework for attacking the design systematically.</p></div>
    <div class="c"><h4>3. Analysis and construction</h4><p>It tells implementers what to build, and must hold the information needed to evaluate quality attributes.</p></div>
  </div>

  <h3>Which views, and which notations?</h3>
  <p class="small">Documenting an architecture is a matter of documenting the relevant views, then adding documentation that applies to more than one view. The slides pose two questions: which views are useful, and which notations should describe them. Their answer: one representation will not satisfy all stakeholders, and what suits depends on how complex the diagram is, so the architect develops <b>multiple views</b>.</p>
  <h3>The 4+1 view model</h3>
  <p class="small">Philippe Kruchten of IBM (1995) proposed four fundamental views linked by use cases or scenarios. His aim was to make sure architects consider and document all the important aspects of software-intensive systems. Hofmeister, Nord and Soni (2000) suggest similar views and add a <i>conceptual</i> view.</p>
  {d_41}
  <div class="tbl-wrap"><table><thead><tr><th>View</th><th>Shows</th><th>UML diagrams the slides list</th></tr></thead><tbody>
  <tr><th>Logical</th><td>The vocabulary of the problem domain as classes and objects.</td><td>Class, object, state, sequence, communication.</td></tr>
  <tr><th>Process</th><td>How the system is made of interacting processes at runtime; concurrency and synchronization.</td><td>Control flow charts, data flow charts.</td></tr>
  <tr><th>Development</th><td>The code base as components or modules: libraries, packages, subsystems.</td><td>Component and package diagrams.</td></tr>
  <tr><th>Physical</th><td>The hardware and how software components are spread across processors.</td><td>Deployment diagrams.</td></tr>
  <tr><th>Use case (+1)</th><td>The system&rsquo;s functionality. It ties the other four together and helps explain them.</td><td>Use case diagrams.</td></tr></tbody></table></div>
  <p class="small">The slides&rsquo; own summary of views: different views address different concerns, not all views are needed, and keeping several views in step costs effort, especially as the system evolves.</p>
'''
w2_terms = terms([
 ('Quality attribute', 'A required quality of the system such as performance, modifiability, security or scalability. Largely determined by the architecture.'),
 ('Coupling', 'Interaction between elements. The slides say limit it so that a change affects few elements.'),
 ('Stakeholder', 'Anyone with a role that needs the architecture: for example team members, analysts, customers, project managers. The slides show a figure of the roles without a list.'),
 ('Architecture document', 'The concrete artifact produced by documenting: files, web pages, a whiteboard snapshot or paper.'),
 ('Product line', 'A family of products built on a shared, reusable architecture model.'),
 ('4+1 view model', 'Kruchten (IBM, 1995): logical, process, development and physical views, tied together by use cases (the +1).'),
 ('Logical view', 'Problem-domain vocabulary as classes and objects.'),
 ('Process view', 'Interacting runtime processes; concurrency and synchronization.'),
 ('Development view', 'Code organisation: libraries, packages, subsystems.'),
 ('Physical view', 'Hardware and how software is spread across processors.'),
 ('Use case view', 'The requirements as use cases; ties the other four views together.'),
 ('Conceptual view', 'A view added by Hofmeister, Nord and Soni (2000). The slides name it but do not describe it.'),
])
w2_boss = ''.join([
 qa('Give four reasons architecture is important.',
  '''<p>Any four of: it lets you reason about and manage change; it enables early prediction of qualities; a documented architecture improves communication among stakeholders; it constrains later implementation; it focuses on assembling components; it supports reasoning about cost and schedule; it can be a reusable model for a product line.</p>''', 1),
 qa('Match each quality attribute to what the architecture should do: performance, modifiability, security, scalability.',
  '''<ul><li><b>Performance:</b> manage time-based behaviour, shared resources and how often and how much elements communicate.</li><li><b>Modifiability:</b> limit coupling so a change touches few elements.</li><li><b>Security:</b> include authorization, safeguards and recovery.</li><li><b>Scalability:</b> do not hard-code resource assumptions or limits.</li></ul>''', 2),
 qa('What are the three uses of architecture documentation?',
  '''<p>(1) <b>Education</b>: introduce people to the system. (2) <b>Communication</b> among stakeholders, plus a way to gauge progress. (3) <b>Basis for analysis and construction</b>: it tells implementers what to build and holds the information needed to evaluate quality attributes.</p>''', 3),
 qa('Name the five views of the 4+1 model and say what the +1 is for.',
  '''<p>Logical, process, development and physical, plus the <b>use case view</b>. The use case view is the +1: it ties the other four together and helps define and explain the structures and functions in them.</p>''', 4),
 qa('Why not just draw one big diagram of the architecture?',
  '''<p>The slides say one representation will not satisfy all stakeholders, and the right one depends on the complexity of the diagram. So the architect develops multiple views. The cost is the effort of keeping them all up to date as the system evolves, which is why not every view is needed.</p>''', 5),
 qa('Which view would you open to answer each: &ldquo;Which servers run this?&rdquo; &ldquo;What classes model a customer?&rdquo; &ldquo;What runs at the same time?&rdquo;',
  '''<p><b>Physical</b> (hardware and where software sits), <b>logical</b> (classes and objects), <b>process</b> (interacting processes, concurrency). This mapping is my own application of the slide table; the slides do not set these questions.</p>''', 6),
])

# ====================================================================== topic 3 visuals
d_csp = svg(700, 232,
    box(115, 14, 120, 54, ['Server'], 'bxs')
    + box(10, 150, 90, 46, ['Client']) + box(130, 150, 90, 46, ['Client']) + box(250, 150, 90, 46, ['Client'])
    + arr(175, 68, 55, 150, 'cs', both=True) + arr(175, 68, 175, 150, 'cs', both=True) + arr(175, 68, 295, 150, 'cs', both=True)
    + txt(175, 222, 'Client-server: clients ask, one server serves', 'ts')
    + box(400, 24, 90, 46, ['Peer']) + box(600, 24, 90, 46, ['Peer']) + box(400, 150, 90, 46, ['Peer']) + box(600, 150, 90, 46, ['Peer'])
    + arr(490, 47, 600, 47, 'cs', both=True) + arr(490, 173, 600, 173, 'cs', both=True)
    + arr(445, 70, 445, 150, 'cs', both=True) + arr(645, 70, 645, 150, 'cs', both=True)
    + arr(480, 70, 610, 150, 'cs', both=True) + arr(610, 70, 480, 150, 'cs', both=True)
    + txt(545, 222, 'Peer-to-peer: every node has the same role', 'ts'),
    'Redrawn: client-server (many clients attached to one server) beside peer-to-peer (nodes joined directly to each other)', 'cs')

d_eda = bus('ed', [['Event producer', 'UI, sensor, ...'], ['Event producer', 'another source']], ['Event broker', 'routes events'],
            [['Event consumer', 'service or function'], ['Event consumer', 'service or function']],
            'Redrawn: event producers send events to an event broker, which routes them to event consumers', 'events', 'events')

d_erp = svg(700, 290,
    box(100, 8, 500, 46, ['User interaction layer', 'screens, forms, menus, reports'], small_rest=True)
    + box(100, 62, 500, 46, ['Functionality layer', 'moves between modules, handles data input'], small_rest=True)
    + box(100, 116, 500, 46, ['Business rules layer', 'decides how the modules behave'], small_rest=True)
    + box(100, 170, 500, 46, ['Application core layer', 'all system code; where customisations go'], small_rest=True)
    + box(100, 224, 500, 46, ['Database layer', 'tables, indexes and data of each module'], small_rest=True)
    + arr(60, 20, 60, 270, 'er') + txt(60, 286, 'may use', 'ts'),
    'Redrawn: the five layers of the ERP example from the slides, each allowed to use the layer below', 'er')

w3_vis = f'''
  <h3>What is an architectural style?</h3>
  <p class="small">Engineers building many systems in many domains noticed that certain design choices keep producing solutions with better properties. An <b>architectural style</b> is a specialization of element and relation types, together with a set of constraints on how they can be used. Each style describes a category of system with four parts:</p>
  <div class="cards3">
    <div class="c"><h4>Components</h4><p>The parts that do a job the system needs, for example a database or a computational module.</p></div>
    <div class="c"><h4>Connectors</h4><p>What lets components communicate, coordinate and cooperate.</p></div>
    <div class="c"><h4>Constraints</h4><p>Rules for how components may be joined into a system.</p></div>
    <div class="c"><h4>Semantic models</h4><p>Let a designer understand the overall properties of the system.</p></div>
  </div>

  <h3>The nine styles in this lecture</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Style</th><th>Idea (from the slides)</th><th>Benefits or example named</th></tr></thead><tbody>
  <tr><th>1. Client-server</th><td>Two main components: the client (usually the user interface) and the server (back-end services), communicating. 2-tier, 3-tier, n-tier and cloud computing show this style.</td><td>Scalability, separation of concerns, flexibility in client types. Web apps, networked games, banking.</td></tr>
  <tr><th>2. Peer-to-peer</th><td>Every node has the same capabilities and responsibilities, and nodes talk to each other directly.</td><td>Decentralization, fault tolerance, distributed processing. BitTorrent, real-time collaboration.</td></tr>
  <tr><th>3. Data-centered (C&amp;C type)</th><td>A data store is accessed often by components that update, add, delete or change its data.</td><td>Integrability: components can change and new clients be added without affecting other clients.</td></tr>
  <tr><th>4. Event-driven (EDA)</th><td>Built around events, meaning occurrences or changes of state. Components talk mostly through events, not request-response, which decouples them.</td><td>Real-time flow between applications, microservices and devices. E-commerce, IoT, finance, logistics, social media, healthcare.</td></tr>
  <tr><th>5. Layered (module type)</th><td>Logical layers such as presentation, business logic and data access, each with one responsibility.</td><td>Separation of concerns, modularity, maintainability. Common in web apps.</td></tr>
  <tr><th>6. Service oriented (SOA) (C&amp;C type)</th><td>A set of independent services, each for one task (orders, inventory, payments), that talk over a common platform and work together. Each can be updated without affecting the others.</td><td>Reuse services in different systems or combine them for complex tasks; flexible and scalable.</td></tr>
  <tr><th>7. Microservice</th><td>Splits a big app into independent services that talk through APIs: loosely coupled, highly maintainable and testable, independently deployable, organised around business capabilities.</td><td>The slides contrast it with the layered pattern and SOA in a figure only (no text).</td></tr>
  <tr><th>8. Data flow</th><td>Input data is transformed through a series of components into output data. Pipe-and-filter: filters connected by pipes that carry data to the next component.</td><td></td></tr>
  <tr><th>9. Main program / subprogram</th><td>A classic structure that breaks function into a control hierarchy: a main program calls components, which may call other components.</td><td></td></tr></tbody></table></div>

  <h3>Client-server versus peer-to-peer</h3>
  {d_csp}
  <p class="small">Redrawn. The slides compare the two in a picture and say P2P computers are dedicated to serving each other, so they can communicate directly.</p>

  <h3>Event-driven architecture: four parts</h3>
  {d_eda}
  <div class="tbl-wrap"><table><thead><tr><th>Part</th><th>Role</th></tr></thead><tbody>
  <tr><th>Event</th><td>A meaningful change or occurrence, often a time-stamped piece of data saying what happened.</td></tr>
  <tr><th>Event producer</th><td>Generates and sends events: a user interface, a sensor or any source that starts one.</td></tr>
  <tr><th>Event consumer</th><td>Listens for events and reacts: a service, a function or any module built to respond.</td></tr>
  <tr><th>Event broker</th><td>The go-between that routes events from producers to consumers. The slides name Apache Kafka, RabbitMQ and AWS Lambda as ways to build it.</td></tr></tbody></table></div>

  <h3>Layered example: an ERP system</h3>
  {d_erp}
  <p class="small">Redrawn from the slide text. The slides say the ERP covers accounts, stock, HR, production, purchasing, finance and more, and give each layer its own job as shown above. The business-rules example in the slides: when a new employee is entered in HR and payroll, add an introductory course to that employee&rsquo;s training menu.</p>
  <p class="small"><b>Three tags to remember:</b> the slides label data-centered and SOA as <i>C&amp;C</i> styles and the layered pattern as a <i>module</i> style. That is the first hint that the next two topics split styles by structure category.</p>
'''
w3_terms = terms([
 ('Architectural style', 'A specialization of element and relation types plus constraints on how they can be used. Describes a category of system.'),
 ('Client-server', 'Client (usually the user interface) and server (back-end services) communicate. 2-tier, 3-tier, n-tier and cloud follow it.'),
 ('Peer-to-peer (P2P)', 'Every node has the same capabilities and responsibilities; nodes talk directly.'),
 ('Data-centered architecture', 'A shared data store is used by components that update, add, delete or modify the data. Promotes integrability.'),
 ('Integrability', 'Existing components can change and new clients be added without affecting other clients.'),
 ('Event-driven architecture (EDA)', 'Design around events; components are decoupled and talk mainly through events instead of request-response.'),
 ('Event / producer / consumer / broker', 'The change that happened; the source that emits it; the part that reacts; the intermediary that routes events.'),
 ('Layered pattern', 'Logical layers each with one responsibility, for example presentation, business logic, data access.'),
 ('Service oriented architecture (SOA)', 'Independent services for specific tasks, joined over a common platform; reusable and updatable one at a time.'),
 ('Microservice architecture', 'An app split into independent services that talk by API; loosely coupled, independently deployable, organised around business capabilities.'),
 ('API', 'Named in the slides as the way microservices interact. The slides do not define it.'),
 ('Pipe-and-filter', 'Filters (components) joined by pipes that move data from one filter to the next.'),
 ('Main program / subprogram', 'A control hierarchy where a main program calls components, which may call others.'),
])
w3_boss = ''.join([
 qa('What does an architectural style contain?',
  '''<p>Components that perform needed functions, connectors for communication, coordination and cooperation, constraints on how components may be integrated, and semantic models that help a designer see the system&rsquo;s overall properties.</p>''', 1),
 qa('Compare client-server and peer-to-peer in one short paragraph.',
  '''<p>In <b>client-server</b>, the system is split into a client (usually the user interface) and a server (back-end services); the benefits listed are scalability, separation of concerns and flexible client types. In <b>peer-to-peer</b>, every node has the same capabilities and responsibilities and nodes communicate directly; the benefits listed are decentralization, fault tolerance and distributed processing.</p>''', 2),
 qa('List the four key components of event-driven architecture and what each does.',
  '''<ul><li><b>Event:</b> a meaningful, often time-stamped change.</li><li><b>Event producer:</b> generates and emits events.</li><li><b>Event consumer:</b> listens and reacts.</li><li><b>Event broker:</b> routes events from producers to consumers.</li></ul>''', 3),
 qa('Why is EDA described as decoupled?',
  '''<p>Components talk mainly through events, not by direct request-response, so a producer does not need to know which consumers exist. The slides say EDA decouples the components of a system.</p>''', 4),
 qa('Name the five layers of the ERP example and what the business-rules layer does.',
  '''<p>User interaction, functionality, business rules, application core, database. The <b>business rules layer</b> sets how the ERP modules behave, for example adding an introductory course to the training menu when a new employee is entered in HR and payroll.</p>''', 5),
 qa('What is the difference between SOA and microservices? What do the slides actually say?',
  '''<p>The slides describe <b>SOA</b> as independent services for specific tasks, communicating over a common platform and updatable independently. They describe <b>microservices</b> as breaking a large app into independent services that interact by API: loosely coupled, easy to maintain and test, independently deployable, organised around business capabilities.</p>
  <p><b>My own reading:</b> the two descriptions overlap heavily. The slide that compares layered, SOA and microservice is a figure only, so the files give no explicit list of differences.</p>''', 6),
])

# ====================================================================== topic 4 visuals
d_dec = svg(700, 330,
    '<rect class="lane" x="10" y="8" width="680" height="314" rx="14"/>'
    + txt(24, 30, 'E-LEARNING SYSTEM (my own sketch for the slide exercise)', 'ts', 'start')
    + box(24, 46, 126, 262, [''], 'bx2') + box(160, 46, 126, 262, [''], 'bx2') + box(296, 46, 126, 262, [''], 'bx2')
    + box(432, 46, 126, 262, [''], 'bx2') + box(568, 46, 112, 262, [''], 'bx2')
    + txt(87, 70, 'Course', 'tb') + txt(87, 89, 'management', 'tb')
    + txt(223, 70, 'Lesson', 'tb') + txt(223, 89, 'delivery', 'tb')
    + txt(359, 80, 'Quiz', 'tb')
    + txt(495, 70, 'User', 'tb') + txt(495, 89, 'management', 'tb')
    + txt(624, 70, 'Progress', 'tb') + txt(624, 89, 'tracking', 'tb')
    + box(36, 112, 102, 40, ['Course list'], 'bx', bold=False) + box(36, 160, 102, 40, ['Course', 'details'], 'bx', bold=False)
    + box(172, 112, 102, 40, ['Videos'], 'bx', bold=False) + box(172, 160, 102, 40, ['Documents'], 'bx', bold=False) + box(172, 208, 102, 40, ['Slides'], 'bx', bold=False),
    'Redrawn: a decomposition view of the e-learning exercise, with modules nested inside the system and submodules nested inside modules', 'dec')

d_lay = svg(700, 262,
    box(60, 14, 360, 56, ['Layer 3 (top)'], 'bx') + box(60, 82, 360, 56, ['Layer 2'], 'bx') + box(60, 150, 360, 56, ['Layer 1 (bottom)'], 'bx')
    + arr(450, 28, 450, 194, 'ly') + txt(450, 220, 'allowed to use', 'ts')
    + box(520, 14, 160, 192, ['Sidecar', 'utility library or', 'platform service', '(OS, runtime)'], 'bxs')
    + txt(300, 256, 'Generic labels: a layered view is a stack where each layer may use the ones below it', 'ts'),
    'Redrawn: three layers in a stack with an allowed-to-use arrow pointing down, and a sidecar box for utilities', 'ly')

d_asp = svg(700, 262,
    box(40, 14, 170, 52, ['Account']) + box(265, 14, 170, 52, ['Customer']) + box(490, 14, 170, 52, ['ATM'])
    + arr(125, 112, 125, 66, 'as', dash=True) + arr(350, 112, 350, 66, 'as', dash=True) + arr(575, 112, 575, 66, 'as', dash=True)
    + txt(362, 98, 'crosscuts', 'ts', 'start')
    + box(40, 120, 620, 40, ['Aspect: access control'], 'bxs') + box(40, 166, 620, 40, ['Aspect: transaction management'], 'bxs') + box(40, 212, 620, 40, ['Aspect: logging'], 'bxs'),
    'Redrawn: three business modules (Account, Customer, ATM) crosscut by aspect modules for access control, transaction management and logging', 'as')

w4_vis = f'''
  <h3>What a module view is</h3>
  <p class="small">Every module view has four parts, which the slides repeat for each style: <b>elements</b>, <b>relations</b>, <b>constraints</b> and <b>what it is for</b>. A <b>module</b> is an implementation unit of software that provides a coherent set of responsibilities. A responsibility is a general statement of what an architecture element is expected to contribute. Each module can also carry <b>properties</b>: responsibilities, visibility information (which other modules can use it), revision history.</p>
  <div class="cards3">
    <div class="c"><h4>Is-part-of</h4><p>Part/whole between a submodule and the aggregate module. In its most general form it just means aggregation.</p></div>
    <div class="c"><h4>Depends-on</h4><p>A depends on B. A logical association between classes in a UML class diagram also shows a dependency.</p></div>
    <div class="c"><h4>Is-a</h4><p>Generalization/specialization between a specific child module and a general parent. Inheritance is a special case.</p></div>
  </div>
  <p class="small"><b>Constraints</b> may limit visibility between modules. <b>Uses</b> of module views, from the slides: a blueprint for the code, impact analysis, explaining the system and the code base, requirements traceability, planning incremental development, and work assignments, schedules and budgets.</p>
  <p class="small"><b>The limit:</b> a module view is a static partition of functions, so it is hard to infer runtime behaviour from it. It is not used to analyse performance or reliability. Module views are therefore mapped to C&amp;C views, and one module may take part in many runtime components. The slides add that it is unlikely any architecture documentation is complete without at least one module view.</p>
  <p class="small"><b>Notations:</b> informal boxes; UML (packages, classes and more); and a <b>dependency structure matrix</b>, a square matrix showing dependency between modules.</p>

  <h3>The six module styles at a glance</h3>
  <p class="small">This lecture covers the first four. Aspects and data model come in the next lecture (Topic 5).</p>
  <div class="tbl-wrap"><table><thead><tr><th>Style</th><th>Relation</th><th>Key constraints</th><th>What it is for</th></tr></thead><tbody>
  <tr><th>Decomposition</th><td>Is-part-of (decomposition relation); say what criteria you used.</td><td>No loops in the decomposition graph. A module has only one parent.</td><td>Reason about and communicate structure; input for work assignment; localize changes.</td></tr>
  <tr><th>Uses</th><td>Uses (a form of depends-on): A uses B if A needs a correctly working B.</td><td>No topological constraints, but loops, broad fan-out or long chains hurt incremental delivery.</td><td>Plan increments and subsets; debug and test; gauge effect of change.</td></tr>
  <tr><th>Generalization</th><td>Generalization (is-a): inheritance, interface inheritance, realization.</td><td>A module can have several parents, though multiple inheritance is often seen as dangerous.</td><td>Inheritance in OO design; describe evolution and extension; reuse.</td></tr>
  <tr><th>Layered</th><td>Allowed-to-use between layers.</td><td>Every piece of software is in exactly one layer. At least two layers. No circular use: a lower layer cannot use one above.</td><td>Modifiability and portability; manage complexity; separation of concerns.</td></tr>
  <tr><th>Aspects</th><td>Crosscuts: binds an aspect module to the modules it affects.</td><td>An aspect may crosscut regular modules and other aspects. One that crosscuts itself can recurse forever.</td><td>Model crosscutting concerns in OO design; modifiability.</td></tr>
  <tr><th>Data model</th><td>One-to-one, one-to-many, many-to-many; generalization; aggregation.</td><td>Avoid functional dependencies.</td><td>Describe data structure; analyse impact of data changes; avoid redundancy and inconsistency.</td></tr></tbody></table></div>

  <h3>Decomposition</h3>
  <p class="small">Modules are drawn as named boxes containing other named boxes, or as nested UML packages. A <b>subsystem</b> is an aggregated module that does a functionally cohesive part of the mission, can run independently and can be developed or deployed in increments. The slide example is a Mars exploration robot: navigation, motion, power management, communication and monitoring are subsystems, but a utility library is a module group, not a subsystem, because it cannot do work that is recognisably part of the system&rsquo;s purpose on its own.</p>
  {d_dec}
  <p class="small"><b>My own answer</b> to the slide exercise (the slides give none). The five modules come from the exercise text. The submodules shown are only those the text hints at (a course list and course details; videos, documents and slides). Other splits are possible.</p>

  <h3>Uses and Generalization</h3>
  <p class="small">The <b>uses</b> view is drawn as a dependency with the stereotype <code>&lt;&lt;use&gt;&gt;</code> in UML packages, or as a dependency matrix. The slides&rsquo; example is ATIA-M, a large web-based Java EE app for U.S. Army training with C# desktop clients: its uses view helps plan incremental development. <b>Generalization</b> sits at the heart of UML: modules are shown as classes or interfaces, and a module may be marked <i>abstract</i> if it has no complete implementation. The example is a PetStore app. The generalization exercise on the slides is a picture only.</p>

  <h3>Layered style</h3>
  {d_lay}
  <p class="small">A layering is more than a partition: layers follow a strict ordering relation. Five ways to draw it, per the slides:</p>
  <div class="tbl-wrap"><table><thead><tr><th>Notation</th><th>Meaning</th></tr></thead><tbody>
  <tr><th>Stack</th><td>Boxes stacked; allowed-to-use is read top-down by adjacency. Arrows can also be used.</td></tr>
  <tr><th>Segmented layers</th><td>A layer is split into segments (a finer grouping). Often an ambiguity: state whether segments may use each other (in the slide example the top layer&rsquo;s segments may not, the bottom layer&rsquo;s may).</td></tr>
  <tr><th>Rings</th><td>Concentric circles, innermost = lowest layer. Sectors of a ring = segments. No difference in meaning from a stack, except a ring can show adjacency that a stack cannot.</td></tr>
  <tr><th>Sidecar</th><td>A box beside the layers, often a utility library or platform service. You must say which usage rules apply.</td></tr>
  <tr><th>Size and colour</th><td>Colour may mark the responsible team; size the relative amount of code. Explain them in a key.</td></tr></tbody></table></div>
  <p class="small">The UNIX System V layer structure is the slide example, shown as a figure only.</p>

'''
w5_vis = f'''
  <h3>Aspects style</h3>
  <p class="small">In practice business code (open an account, deposit, withdraw) gets mixed with code for <b>crosscutting concerns</b> such as access control, transaction management and logging. The aspects style puts that code in separate <b>aspect</b> modules and binds each aspect to the modules that need it. The term comes from aspect-oriented programming (AOP), which complements OOP by factoring the crosscutting code out of the classes. Aspects are shown in UML as stereotyped classes. The slide example, IkeWiki, uses aspects for transaction management, exception handling and authorization checks.</p>
  {d_asp}

  <h3>Data model style</h3>
  <p class="small">Elements are <b>data entities</b>, with a name, attributes, a primary key and access rules. The slide notations are the <b>Crow&rsquo;s Foot ERD</b>, with special symbols at the line ends showing cardinality, and a UML class diagram where classes stand for entities. The example is a PetShop web store that keeps a catalogue and takes orders: most of its functions retrieve, create or update the data shown in the model.</p>
'''
w4_terms = terms([
 ('Module', 'An implementation unit of software that provides a coherent set of responsibilities.'),
 ('Responsibility', 'A general statement of what an architecture element is expected to contribute.'),
 ('Is-part-of / depends-on / is-a', 'The three module relations: aggregation, dependency, generalization (inheritance is a special case).'),
 ('Dependency structure matrix', 'A square matrix showing dependency between modules.'),
 ('Subsystem', 'An aggregated module that does a functionally cohesive part of the mission, can run independently and be developed or deployed incrementally.'),
 ('Uses relation', 'A uses B if A depends on the presence of a correctly working B to meet its own requirements.'),
 ('Fan-out', 'Used in the slides when saying that broad fan-out in uses relations hurts incremental delivery. Not defined there; plainly, one module using many others.'),
 ('Generalization', 'The is-a relation with a parent and child; supports extension, evolution and reuse.'),
 ('Abstract module', 'A module marked as not containing a complete implementation.'),
 ('Layer', 'A grouping of modules that offers a cohesive set of services through a public interface.'),
 ('Allowed-to-use', 'The one-way relation between layers; a lower layer cannot use one above.'),
 ('Sidecar', 'A box beside a layer diagram, often a utility library or platform service.'),
])
w5_terms = terms([
 ('Crosscutting concern', 'Logic needed in many modules, such as access control, transaction management and logging.'),
 ('Aspect / AOP', 'A module that holds a crosscutting concern. Aspect-oriented programming factors this code out of classes.'),
 ('Data entity', 'An object that holds information to be stored or represented, with attributes and a primary key.'),
 ('Crow&rsquo;s Foot ERD', 'Entity-relationship notation with symbols at line ends for cardinality.'),
])
w5_boss = ''.join([
 qa('What problem does the aspects style solve? Use the bank example.',
  '''<p>An Account module should hold only account logic (open, close, deposit, withdraw), but in practice access control, transaction management and logging get mixed in. Aspects move that crosscutting code into separate modules and bind them to Account, Customer, ATM and others.</p>''', 1),
 qa('Name the elements, notations and example of the data model style.',
  '''<p>Elements are <b>data entities</b>, each with a name, attributes, a primary key and access rules. Notations: the <b>Crow&rsquo;s Foot ERD</b> (symbols at the line ends show cardinality) or a UML class diagram. Relations: one-to-one, one-to-many, many-to-many, generalization and aggregation. The slide example is a PetShop web store whose functions mostly retrieve, create or update the modelled data.</p>''', 2),
 qa('Which constraint of the aspects style can cause trouble, and which one of the data model style should you follow?',
  '''<p>An aspect may crosscut regular modules and other aspects, but one that crosscuts itself can recurse forever. For the data model style the slides say to avoid functional dependencies.</p>''', 3),
])
w4_boss = ''.join([
 qa('List the parts every module-style description has, and the three module relations.',
  '''<p>Elements, relations, constraints and what it is for. The relations are <b>is-part-of</b>, <b>depends-on</b> and <b>is-a</b>.</p>''', 1),
 qa('Why can a module view not tell you about performance? What do you do about it?',
  '''<p>It is a static partition of the software&rsquo;s functions, so runtime behaviour cannot be inferred from it. Map the module view to a component-and-connector view. A module may take part in many runtime components.</p>''', 2),
 qa('State the two constraints of the decomposition style and what the style is used for.',
  '''<p>No loops in the decomposition graph, and a module can have only one parent. It is used to reason about and communicate structure, to give input for work assignment, and to reason about localizing changes.</p>''', 3),
 qa('Uses style: what makes an architecture hard to deliver in increments?',
  '''<p>The style has no topological constraints, but the slides say loops, broad fan-out or long dependency chains impair delivery in incremental subsets.</p>''', 4),
 qa('Give the three constraints of the layered style and one reason a lower layer cannot use a higher one.',
  '''<p>Every piece of software is in exactly one layer; there are at least two layers; allowed-to-use must not be circular.</p>
  <p><b>My own reading</b> of the reason: if a lower layer could use a higher one, the layers would form a loop, which is the circular use the rule forbids. The slides state the rule, not the reason.</p>''', 5),
 qa('Segmented layers: what ambiguity do the slides warn about?',
  '''<p>Whether segments of a layer may use each other. In the slide example the top layer&rsquo;s segments may not, but the bottom layer&rsquo;s may, so you have to state the usage rules for segments consistently.</p>''', 6),
 qa('Exercise: draw a decomposition view for the e-learning system.',
  '''<p>Draw the system with five nested modules: course management, lesson delivery, quiz, user management, progress tracking. Then split modules further. <b>My own sketch</b> is in the diagram above (course list and details; videos, documents and slides). The slides set the exercise but give no model answer.</p>''', 7),
])

# ====================================================================== topic 6 visuals
d_att = svg(700, 188,
    box(20, 40, 160, 84, ['Client', 'component'], 'bxs')
    + '<rect class="bxs" x="174" y="76" width="14" height="14" rx="2"/>'
    + ln(188, 83, 272, 83) + txt(230, 70, 'attached', 'ts')
    + box(278, 30, 150, 104, ['Connector', 'request/reply'], 'bx')
    + '<rect class="bxs" x="272" y="76" width="14" height="14" rx="2"/>' + '<rect class="bxs" x="420" y="76" width="14" height="14" rx="2"/>'
    + txt(300, 160, 'request role', 'ts') + txt(406, 160, 'reply role', 'ts')
    + ln(434, 83, 518, 83) + txt(476, 70, 'attached', 'ts')
    + '<rect class="bxs" x="512" y="76" width="14" height="14" rx="2"/>'
    + box(520, 40, 160, 84, ['Server', 'component'], 'bxs')
    + txt(100, 150, 'service-request port', 'ts') + txt(600, 150, 'reply port', 'ts')
    + txt(350, 182, 'Small squares are ports (on components) and roles (on connectors). The one C&C relation is attachment.', 'ts'),
    'Redrawn: a client component port attached to the request role of a connector, and a server port attached to its reply role', 'att')

d_pf = svg(700, 130,
    txt(30, 26, 'input', 'ts') + arr(10, 66, 70, 66, 'pf')
    + box(70, 38, 130, 56, ['Filter']) + arr(200, 66, 270, 66, 'pf') + txt(235, 56, 'pipe', 'ts')
    + box(270, 38, 130, 56, ['Filter']) + arr(400, 66, 470, 66, 'pf') + txt(435, 56, 'pipe', 'ts')
    + box(470, 38, 130, 56, ['Filter']) + arr(600, 66, 680, 66, 'pf') + txt(660, 26, 'output', 'ts')
    + txt(350, 120, 'Data is transformed step by step; connected filters must agree on the type of data on the pipe', 'ts'),
    'Redrawn: three filters joined by pipes, with input on the left and output on the right', 'pf')

d_ps = bus('ps', [['Publisher', 'announces events'], ['Both roles', 'publishes and listens']], ['Event distributor', 'e.g. an event bus'],
           [['Subscriber', 'listens for events'], ['Subscriber', 'listens for events']],
           'Redrawn: publishers announce events to an event distributor, which delivers them to registered subscribers', 'announce', 'listen')

w6_vis = f'''
  <h3>Component-and-connector (C&amp;C) views</h3>
  <p class="small">A C&amp;C view shows the system <b>while it runs</b>. A <b>component</b> is a unit of behaviour; its description says what it can do and what it needs to do it (processes, objects, clients, servers, data stores). A <b>connector</b> is a mechanism that relates components, for example data flow, control flow, a communication link and protocol, or shared storage. There is only one relation in a C&amp;C view: <b>attachment</b>. It ties a component&rsquo;s <i>port</i> to a connector&rsquo;s <i>role</i> and so lays out the computational topology.</p>
  {d_att}
  <p class="small">Every element should have a name and a quality-attribute type so it can be analysed. Which properties you record depends on the analysis: for performance you would note things like reliability, performance, resource needs, functionality and security. The view is used for qualitative and quantitative analysis, and together with its supporting documents it communicates the architect&rsquo;s design intent. It answers the runtime questions from Topic 1: which components run, which data stores are shared, what is replicated, how data flows, what runs in parallel, whether structure changes as it executes.</p>

  <h3>Four categories of C&amp;C style</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Category</th><th>How components interact</th><th>Styles named</th></tr></thead><tbody>
  <tr><th>Call-return</th><td>By synchronous calls. A component gets control and data, does its work, then returns control to the caller.</td><td>Client-server, peer-to-peer, SOA</td></tr>
  <tr><th>Data flow</th><td>Driven by data moving through the system; each step transforms inputs into outputs.</td><td>Pipe-and-filter, batch sequential</td></tr>
  <tr><th>Event-based</th><td>By asynchronous events or messages. Control moves when events happen, not by explicit calls; components publish and/or subscribe.</td><td>Publish-subscribe, SOA</td></tr>
  <tr><th>Repository</th><td>Through large shared collections of data.</td><td>Shared data, blackboard</td></tr></tbody></table></div>
  <p class="small">Note that SOA appears under both call-return and event-based. The slides say it is both, depending on the connector type: call-return connectors (SOAP, REST) or asynchronous messaging.</p>

  <h3>The styles in detail</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Style</th><th>Elements and relation</th><th>Constraints and properties</th><th>What it is for</th></tr></thead><tbody>
  <tr><th>Client-server</th><td>Client invokes services; server provides them; a request/reply connector with a request role and a reply role. Attachment ties client request ports to the request role and server reply ports to the reply role.</td><td>Clients connect to the server through request/reply connectors; components may be arranged in tiers. Properties: how many clients can connect, maximum request rates, dynamic introduction of clients, local or remote calls, encryption.</td><td>Modifiability and reuse by factoring out common services; scalability and availability if the server is replicated; analysing dependability, security, throughput.</td></tr>
  <tr><th>SOA</th><td>Service consumers and providers; infrastructure components (enterprise service bus, service registry, orchestration server); connectors: call-return or asynchronous messaging.</td><td>Service providers may also be consumers. Properties: performance, reliability, availability, cost.</td><td>Interoperability of distributed components on different platforms or across the Internet; dynamic reconfiguration.</td></tr>
  <tr><th>Pipe-and-filter</th><td>Filters transform data on input ports into data on output ports; pipes are one-way conduits that keep the order and value of data.</td><td>Connected filters must agree on data type. Properties: how end-of-data is signalled, pipe capacity, whether each filter is its own process.</td><td>Reuse (filters are independent); functional composition; throughput when data is transformed serially.</td></tr>
  <tr><th>Publish-subscribe</th><td>Components with publish or subscribe ports; an event distributor (such as an event bus) with announce and listen roles.</td><td>Publish ports attach to announce roles, subscribe ports to listen roles. A component may do both. Properties: which events, when an announcer is blocked.</td><td>Sending events to unknown recipients, isolating producers from consumers; GUI frameworks, mailing lists, bulletin boards, social networks.</td></tr>
  <tr><th>Shared data</th><td>Data stores and data accessors; connectors read and write.</td><td>The store is attached to accessors through connectors. Properties: types of data, performance, distribution, number of accesses allowed.</td><td>Many components using persistent data; better modifiability by decoupling producers from consumers.</td></tr></tbody></table></div>
  {d_pf}
  {d_ps}
  <p class="small">The slides&rsquo; summary: call-return for direct request and response, data flow for continuous processing, event-based for dynamic user interaction, repository for centralised data management. The slide ATM banking example and the event-based-or-call-return questions are pictures only.</p>

  <h3>Allocation styles</h3>
  <p class="small">Allocation styles map software onto things that are not software. Each has a software element and an environmental element:</p>
  <div class="tbl-wrap"><table><thead><tr><th>Style</th><th>Software element</th><th>Environment element</th><th>Relations</th><th>Used for</th></tr></thead><tbody>
  <tr><th>Deployment</th><td>Usually processes from C&amp;C views</td><td>Computing hardware: processor, memory, disk, network (router, bandwidth, firewall, bridge)</td><td>Allocated-to; with dynamic allocation also migrates-to, copy-migrates-to, execution-migrates-to</td><td>Analysing performance, availability, deployability, security; testers&rsquo; runtime dependencies; integration test planning; cost estimates when buying.</td></tr>
  <tr><th>Install</th><td>A C&amp;C component</td><td>Configuration items: files and folders (executables, data, logs, configuration, scripts)</td><td>Allocated-to; containment (folders form a tree)</td><td>Understanding file layout; build-and-deploy procedures; finding log and configuration files; updating, multiple installed versions; spotting a missing or damaged file&rsquo;s role.</td></tr>
  <tr><th>Work assignment</th><td>A module</td><td>An organisational unit: person, team, department, subcontractor</td><td>Allocated-to</td><td>Team resourcing; explaining the project to a new hire; basis for work breakdown, budget and schedule estimates.</td></tr></tbody></table></div>
  <p class="small"><b>Migrates-to</b> means a software element can move from one processor to another. <b>Copy-migrates-to</b> is the same, except the element sends a copy and keeps the original where it was. The slide example deployment views (UML) are figures only.</p>
'''
w6_terms = terms([
 ('Attachment', 'The single C&amp;C relation: a component port is attached to a connector role.'),
 ('Port', 'A point on a component where a connector attaches; has an interface.'),
 ('Role', 'What a connector can be called on to do at one end, for example the request role and the reply role.'),
 ('Call-return', 'Synchronous calls: a component gets control and data, finishes, and hands control back.'),
 ('Request/reply connector', 'Used by a client to invoke a server. Has a request role and a reply role.'),
 ('Enterprise service bus', 'In SOA, an infrastructure component such as a service registry or an orchestration server. The slides do not define it further.'),
 ('Filter / pipe', 'A component that transforms data / a one-way conduit that keeps the order and value of data.'),
 ('Batch sequential', 'Named under data flow; the slides give no description.'),
 ('Publish-subscribe', 'Components announce events and subscribe to events through an event distributor.'),
 ('Event bus', 'An example of an event distributor.'),
 ('Shared data / blackboard', 'Repository styles where components use large shared collections of data. The slides describe shared data only.'),
 ('Deployment style', 'Software elements allocated to hardware.'),
 ('Install style', 'C&amp;C components allocated to files and folders.'),
 ('Work assignment style', 'Modules allocated to people or teams.'),
 ('Migrates-to / copy-migrates-to', 'A software element moves to another processor / sends a copy there and keeps its own.'),
])
w6_boss = ''.join([
 qa('What is the only relation in a C&amp;C view, and what does it connect?',
  '''<p><b>Attachment</b>: ports on components are attached to roles on connectors. It lays out the computational topology.</p>''', 1),
 qa('List the four categories of C&amp;C style with one example each.',
  '''<ul><li><b>Call-return:</b> client-server.</li><li><b>Data flow:</b> pipe-and-filter.</li><li><b>Event-based:</b> publish-subscribe.</li><li><b>Repository:</b> shared data.</li></ul><p>SOA is named under both call-return and event-based.</p>''', 2),
 qa('Why is SOA both call-return and event-based?',
  '''<p>It depends on the connector: SOAP or REST connectors are call-return, while asynchronous messaging is event-based.</p>''', 3),
 qa('Describe pipe-and-filter: its two element types, its main constraint and one benefit.',
  '''<p>Filters transform data; pipes are one-way conduits carrying data between filters. Filters joined by a pipe must agree on the data type. Benefits include reuse, because each filter is independent, and higher throughput when data is transformed serially.</p>''', 4),
 qa('How does publish-subscribe isolate producers from consumers?',
  '''<p>Components do not talk to each other. Publishers announce events to an event distributor (for example an event bus) and subscribers register to listen. So events can go to recipients the sender does not know.</p>''', 5),
 qa('Name the three allocation styles and what each maps onto what.',
  '''<ul><li><b>Deployment:</b> software (usually processes) onto hardware.</li><li><b>Install:</b> C&amp;C components onto files and folders in the production, development, test or build environment.</li><li><b>Work assignment:</b> modules onto people, teams or organisations.</li></ul>''', 6),
 qa('What is the difference between migrates-to and copy-migrates-to?',
  '''<p>Both describe a software element moving to another processor. With copy-migrates-to the element sends a copy and keeps the original where it was.</p>''', 7),
 qa('True or false (the slide quiz): the attachment relation says how ports on components are connected to roles on connectors. A client-server server can add clients dynamically without constraints. Event-based styles use synchronous invocation.',
  '''<p><b>True</b>: attachment ties ports to roles. <b>False</b>: there are constraints on how many clients can connect and whether they can be added dynamically. <b>False</b>: event-based styles are asynchronous, and control moves when events occur, not by explicit calls.</p>''', 8),
 qa('True or false (more from the slide quiz): in publish-subscribe, components talk directly with no go-between. Pipe-and-filter lets each filter work independently. Shared data is mainly for real-time processing. In SOA, consumers and providers must be on different platforms.',
  '''<p><b>False</b>: they communicate through an event distributor. <b>True</b>. <b>False</b>: shared data suits centralised data management. <b>False</b>: they can be on the same platform; SOA allows interoperability across platforms but does not require it.</p>''', 9),
])

# ====================================================================== story, cheat sheet, flashcards
story = [
 (1, 'What is architecture?', 'Software is too big to reason about from the code, and different people need different pictures of it.',
  'Treat architecture as an abstraction made of structures: module, component-and-connector and allocation. Architects design structures and document views of them.',
  'Why spend time on this? And a single picture still will not suit every reader.'),
 (2, 'Why it matters, and how to show it', 'Quality (performance, modifiability, security, scalability) depends on the architecture, and stakeholders need to understand it.',
  'Document it for education, communication and analysis, using several views such as the 4+1 model.',
  'Designers keep meeting the same problems. Are there proven shapes to reuse?'),
 (3, 'Architectural styles', 'Certain design choices keep giving better systems, so naming them saves effort.',
  'Nine general styles, from client-server to layered, SOA, microservice and pipe-and-filter.',
  'One line per style is not enough to document a real system. Each style needs its elements, relations and constraints, starting with the code.'),
 (4, 'Module views and four styles', 'We need a static picture of the code: who owns what, who uses whom, in which layer.',
  'Module views with three relations, and the first four styles: decomposition, uses, generalization, layered.',
  'Two module styles are still missing: code that cuts across modules (logging, security) and the data the system keeps.'),
 (5, 'Aspects and data model', 'Some code does not sit in one module, and the stored data needs its own description.',
  'Aspects style for crosscutting concerns, data model style for data entities and their relations.',
  'All six module styles are static. None of them shows how the system behaves while it runs.'),
 (6, 'Runtime and allocation styles', 'We must reason about running behaviour, and about where things live and who builds them.',
  'C&amp;C styles (call-return, data flow, event-based, repository) and allocation styles (deployment, install, work assignment).',
  'The slides stop here and do not say how to choose among styles for a given system. That question is not answered in the files.'),
]
story_html = '<ol class="story">' + ''.join(
    f'<li class="w{n}"><a href="#week-{n}"><span class="wk">Topic {n}</span><h3>{t}</h3>'
    f'<p><b>Problem</b>{p}</p><p><b>Fix</b>{s}</p><p class="but"><b>But then</b>{b}</p></a></li>' for n, t, p, s, b in story) + '</ol>'

numbers = [('3', 'structure categories: module, C&C, allocation'), ('4 + 1', 'views in the 4+1 model (logical, process, development, physical + use case)'),
           ('1995', 'Kruchten publishes the 4+1 view model (IBM)'), ('2000', 'Hofmeister, Nord and Soni add a conceptual view'),
           ('4', 'quality attributes named: performance, modifiability, security, scalability'), ('7', 'reasons architecture is important (slide list)'),
           ('3', 'uses of architecture documentation'), ('9', 'general styles in Topic 3'), ('4', 'EDA parts: event, producer, consumer, broker'),
           ('5', 'layers in the ERP example'), ('6', 'module styles'), ('3', 'module relations: is-part-of, depends-on, is-a'),
           ('2+', 'minimum number of layers in the layered style'), ('1', 'parent allowed per module in decomposition'),
           ('4', 'C&C categories: call-return, data flow, event-based, repository'), ('1', 'relation in C&C views: attachment'),
           ('3', 'allocation styles: deployment, install, work assignment')]
numbers_html = '<ul class="nums">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in numbers) + '</ul>'
traps = [
 'A <b>structure</b> is the elements as they exist; a <b>view</b> is a representation of it. Architects design structures and document views.',
 'Architecture keeps the <b>public</b> side of an element. Private details are not architectural.',
 '<b>Module</b> structures are static (code). <b>C&amp;C</b> structures are runtime. Do not use module views to judge performance.',
 'The 4+1 model has <b>five</b> views. The +1 is the <b>use case</b> view.',
 'Decomposition: <b>no loops</b> and <b>one parent</b>. Generalization may have several parents (but it is risky).',
 'Layered style: <b>at least two layers</b>, every piece of code in exactly one layer, <b>no circular</b> use.',
 'Uses style has <b>no</b> topological constraints, yet loops and long chains hurt incremental delivery.',
 'The <b>only</b> C&amp;C relation is attachment (port to role).',
 'Event-based means <b>asynchronous</b>; call-return means <b>synchronous</b>. SOA can be either, by connector.',
 'In publish-subscribe, components do <b>not</b> talk directly: they go through an event distributor.',
 'Copy-migrates-to <b>keeps</b> the original; migrates-to moves it.',
 'Slide questions and exercises mostly have <b>no model answers</b>. Answers on this page that go beyond the slides are labelled "my own".',
]
traps_html = '<ul class="traps">' + ''.join(f'<li>{t}</li>' for t in traps) + '</ul>'
cards = [
 ('Define software architecture', 'A set of software structures: elements, relations among them, and properties of both. An abstraction showing public details only.'),
 ('Structure vs view', 'Structure: the elements as they exist. View: a representation of a structure. Architects design structures and document views.'),
 ('Three structure categories', 'Module (static code units), component-and-connector (runtime), allocation (software to non-software).'),
 ('What do allocation structures map?', 'Software structures onto CPUs, file systems, networks and development teams.'),
 ('Four quality attributes in the slides', 'Performance, modifiability, security, scalability.'),
 ('Three uses of architecture documentation', 'Education, communication among stakeholders, and basis for analysis and construction.'),
 ('4+1 view model: the five views', 'Logical, process, development, physical, plus use case (the +1).'),
 ('Logical vs process view', 'Logical: classes and objects of the problem domain. Process: interacting runtime processes, concurrency, synchronization.'),
 ('Development vs physical view', 'Development: code organisation (packages, subsystems). Physical: hardware and where software is placed.'),
 ('What is an architectural style?', 'A specialization of element and relation types with constraints on their use.'),
 ('Four parts of a style', 'Components, connectors, constraints, semantic models.'),
 ('Client-server vs P2P', 'Client-server: user interface client and back-end server. P2P: every node has the same role and talks directly.'),
 ('Four EDA parts', 'Event, event producer, event consumer, event broker.'),
 ('Five layers of the ERP example', 'User interaction, functionality, business rules, application core, database.'),
 ('Pipe-and-filter', 'Filters transform data; pipes carry it one way between filters. Data flow style.'),
 ('Decomposition style constraints', 'No loops in the graph; each module has only one parent. Relation: is-part-of.'),
 ('Uses style in one line', 'A uses B if A needs a correctly working B. Good for planning increments and testing.'),
 ('Generalization style', 'Is-a relation; captures commonality and variation; modules can be abstract; several parents allowed.'),
 ('Layered style constraints', 'Each piece of software in one layer; at least two layers; no circular allowed-to-use.'),
 ('Layered notations', 'Stack, segmented layers, rings, layers with a sidecar, size and colour.'),
 ('Aspects style', 'Aspect modules hold crosscutting concerns (access control, transactions, logging) and crosscut other modules.'),
 ('Data model style notations', 'Crow&rsquo;s Foot ERD or a UML class diagram. Elements are data entities.'),
 ('Why module views are limited', 'They are static, so they cannot show runtime behaviour. Map them to C&amp;C views.'),
 ('C&amp;C relation', 'Attachment of component ports to connector roles.'),
 ('Four C&amp;C categories', 'Call-return, data flow, event-based, repository.'),
 ('Publish-subscribe in one line', 'Publishers announce events to an event distributor; subscribers listen through it. Producers and consumers stay isolated.'),
 ('Three allocation styles', 'Deployment (software to hardware), install (components to files and folders), work assignment (modules to teams).'),
 ('Migrates-to vs copy-migrates-to', 'Migrates-to moves a software element to another processor. Copy-migrates-to sends a copy and keeps the original.'),
]
cards_html = '<div class="cards" id="cards">' + ''.join(
    f'<button class="card" type="button" aria-pressed="false"><span class="front">{q}</span><span class="back">{a}</span></button>' for q, a in cards) + '</div>'
N_CARDS = len(cards)

weeks_html = ''.join([
 week(1, '', 'What is software architecture?', 'Structures, views and the three categories of structure.',
      psn('Software is too big to reason about from the code alone, and different people need different pictures.',
          'See architecture as an abstraction made of structures (module, C&amp;C, allocation). Architects design structures and document views of them.',
          'Why is this worth doing? And one picture still will not suit every reader.'), MAPS[1], w1_vis, w1_terms, w1_boss),
 week(2, '', 'Why it matters, and how to document it', 'Quality attributes, documentation and the 4+1 view model.',
      psn('Quality depends on the architecture, and stakeholders need to understand it.',
          'Document it for education, communication and analysis, with several views, for example the 4+1 model.',
          'Designers keep hitting the same problems. Are there proven shapes to reuse?'), MAPS[2], w2_vis, w2_terms, w2_boss),
 week(3, '', 'Architectural styles', 'Nine general styles, with client-server, EDA and layered looked at more closely.',
      psn('Some design choices keep producing better systems; naming them saves time.',
          'A style = components, connectors, constraints and semantic models. Nine styles from client-server to pipe-and-filter.',
          'One line per style cannot document a real system. We need elements, relations and constraints, starting with the code.'), MAPS[3], w3_vis, w3_terms, w3_boss),
 week(4, '', 'Module views and four styles', 'What a module view is, then decomposition, uses, generalization and layered.',
      psn('We need a static picture of the code: what belongs where, who may use whom.',
          'Module views with is-part-of, depends-on and is-a, and the first four styles: decomposition, uses, generalization, layered.',
          'Two styles are still missing: code that crosscuts modules, and the data the system stores.'), MAPS[4], w4_vis, w4_terms, w4_boss),
 week(5, '', 'Aspects and data model', 'The last two module styles: crosscutting concerns and data entities.',
      psn('Logging, security and transactions are needed in many modules, and the stored data needs a model.',
          'The aspects style moves crosscutting code into aspect modules; the data model style shows data entities and how they relate.',
          'All six module styles are static, so none shows the system running.'), MAPS[5], w5_vis, w5_terms, w5_boss),
 week(6, '', 'Runtime and allocation styles', 'Component-and-connector styles, then the three allocation styles.',
      psn('We need to reason about running behaviour, and about where software lives and who builds it.',
          'C&amp;C styles in four categories (call-return, data flow, event-based, repository) and three allocation styles (deployment, install, work assignment).',
          'The slides stop here. How to choose among the styles for a given system is not covered in the files.'), MAPS[6], w6_vis, w6_terms, w6_boss),
])

supplement_html = '''
<section id="supplement" class="band wx">
  <h2 class="sec">Supplement: examples of views</h2>
  <p class="small">This is the extra deck, <i>Supplementary material: views</i> (slides 28 to 38, from another university&rsquo;s course). It has <b>no explanatory text</b>: each slide is a title and one UML figure. The figures below are <b>cropped from those slides</b> (the owner asked for them to be included), not redrawn. Credit lines on the slides: &copy; Pearson Education; J. Scott Hawker / R. Kuehl, RIT Software Engineering; some figures also marked uml-diagrams.org or Scott W. Ambler. They belong to their authors. Under each figure, the kind of view, the tie-back to Topics 4 to 6 and the plain-words description are <b>my own reading</b>; the slides themselves do not explain the figures. Wide figures scroll sideways inside their box.</p>
  <figure class="slidefig">
    <figcaption><b>Module View Example: UML Module Diagram</b> <span class="small">(slide 29)</span></figcaption>
    <div class="dgw" tabindex="0" role="group" aria-label="Scrollable figure"><img src="img/sup-slide29.png" alt="Figure from slide 29 of the supplementary deck: Module View Example: UML Module Diagram" loading="lazy"></div>
    <p class="small"><b>Kind of view (my mapping):</b> Module. <b>Tie back to:</b> Topic 4: layered style, depends-on.<br><b>My reading:</b> Folder-like packages inside a presentation layer, a business layer and a data layer, with dashed dependency arrows between them, labelled with what each shape is.</p>
  </figure>
  <figure class="slidefig">
    <figcaption><b>Module View Example</b> <span class="small">(slide 30)</span></figcaption>
    <div class="dgw" tabindex="0" role="group" aria-label="Scrollable figure"><img src="img/sup-slide30.png" alt="Figure from slide 30 of the supplementary deck: Module View Example" loading="lazy"></div>
    <p class="small"><b>Kind of view (my mapping):</b> Module. <b>Tie back to:</b> Topic 4: decomposition and uses.<br><b>My reading:</b> Nested packages (a customer-service package, an order-processing system and a domain package) with dependency and access arrows between them, and database interfaces at the bottom.</p>
  </figure>
  <figure class="slidefig">
    <figcaption><b>Module View Example: UML Domain Model Class Diagram</b> <span class="small">(slide 31)</span></figcaption>
    <div class="dgw" tabindex="0" role="group" aria-label="Scrollable figure"><img src="img/sup-slide31.png" alt="Figure from slide 31 of the supplementary deck: Module View Example: UML Domain Model Class Diagram" loading="lazy"></div>
    <p class="small"><b>Kind of view (my mapping):</b> Module. <b>Tie back to:</b> Topic 4: generalization. Topic 5: data model.<br><b>My reading:</b> Classes for things like book, author, account and library, with multiplicities and association, aggregation, composition and generalization lines, plus interfaces.</p>
  </figure>
  <figure class="slidefig">
    <figcaption><b>Module View Example: UML Class Diagram</b> <span class="small">(slide 32)</span></figcaption>
    <div class="dgw" tabindex="0" role="group" aria-label="Scrollable figure"><img src="img/sup-slide32.png" alt="Figure from slide 32 of the supplementary deck: Module View Example: UML Class Diagram" loading="lazy"></div>
    <p class="small"><b>Kind of view (my mapping):</b> Module. <b>Tie back to:</b> Topic 4: is-a and depends-on. Topic 5: data model.<br><b>My reading:</b> A university class diagram: student, seminar, course, professor and address, with attributes, operations and multiplicities on the links.</p>
  </figure>
  <figure class="slidefig">
    <figcaption><b>Component-and-Connector: UML Component Diagram</b> <span class="small">(slide 33)</span></figcaption>
    <div class="dgw" tabindex="0" role="group" aria-label="Scrollable figure"><img src="img/sup-slide33.png" alt="Figure from slide 33 of the supplementary deck: Component-and-Connector: UML Component Diagram" loading="lazy"></div>
    <p class="small"><b>Kind of view (my mapping):</b> C&amp;C. <b>Tie back to:</b> Topic 6: components, ports, attachment.<br><b>My reading:</b> Several subsystems (web store, warehouses, accounting), each with components inside, joined through ports by provided and required interfaces and delegation connectors.</p>
  </figure>
  <figure class="slidefig">
    <figcaption><b>Component-and-Connector: Client Server View Example</b> <span class="small">(slide 34)</span></figcaption>
    <div class="dgw" tabindex="0" role="group" aria-label="Scrollable figure"><img src="img/sup-slide34.png" alt="Figure from slide 34 of the supplementary deck: Component-and-Connector: Client Server View Example" loading="lazy"></div>
    <p class="small"><b>Kind of view (my mapping):</b> C&amp;C. <b>Tie back to:</b> Topic 6: client-server.<br><b>My reading:</b> Repository-access client libraries on one side and a server holding a web server and a version-control service on the other, linked by protocol connectors.</p>
  </figure>
  <figure class="slidefig">
    <figcaption><b>Component-and-Connector: Another Example</b> <span class="small">(slide 35)</span></figcaption>
    <div class="dgw" tabindex="0" role="group" aria-label="Scrollable figure"><img src="img/sup-slide35.png" alt="Figure from slide 35 of the supplementary deck: Component-and-Connector: Another Example" loading="lazy"></div>
    <p class="small"><b>Kind of view (my mapping):</b> C&amp;C. <b>Tie back to:</b> Topic 6: call-return.<br><b>My reading:</b> Two user-interface components calling data-access components for facilities, students, seminars and schedules, which in turn use infrastructure components for security and persistence, ending at a university database.</p>
  </figure>
  <figure class="slidefig">
    <figcaption><b>Component-and-Connector: Embedded Example</b> <span class="small">(slide 36)</span></figcaption>
    <div class="dgw" tabindex="0" role="group" aria-label="Scrollable figure"><img src="img/sup-slide36.png" alt="Figure from slide 36 of the supplementary deck: Component-and-Connector: Embedded Example" loading="lazy"></div>
    <p class="small"><b>Kind of view (my mapping):</b> C&amp;C. <b>Tie back to:</b> Topic 6: components and connectors in a real system.<br><b>My reading:</b> A dense component diagram of an embedded system: a control system, sensors, actuators and an operator panel, joined by buses and ports.</p>
  </figure>
  <figure class="slidefig">
    <figcaption><b>Allocation View: UML Deployment Diagram Example</b> <span class="small">(slide 37)</span></figcaption>
    <div class="dgw" tabindex="0" role="group" aria-label="Scrollable figure"><img src="img/sup-slide37.png" alt="Figure from slide 37 of the supplementary deck: Allocation View: UML Deployment Diagram Example" loading="lazy"></div>
    <p class="small"><b>Kind of view (my mapping):</b> Allocation (deployment). <b>Tie back to:</b> Topic 6: deployment style.<br><b>My reading:</b> Nested boxes for a server device, a web-server runtime and the deployed packaged application, with a second device holding database schemas, joined by a TCP/IP link.</p>
  </figure>
  <figure class="slidefig">
    <figcaption><b>Allocation View: UML Implementation Diagram</b> <span class="small">(slide 38)</span></figcaption>
    <div class="dgw" tabindex="0" role="group" aria-label="Scrollable figure"><img src="img/sup-slide38.png" alt="Figure from slide 38 of the supplementary deck: Allocation View: UML Implementation Diagram" loading="lazy"></div>
    <p class="small"><b>Kind of view (my mapping):</b> Allocation (install). <b>Tie back to:</b> Topic 6: install style.<br><b>My reading:</b> A packaged web application drawn as folders and files (configuration, libraries, pages), each file linked to the component it implements.</p>
  </figure>
  <p class="small"><b>Note:</b> the first slide in the deck (slide 28) is only the title, <i>Supplemental Material: Examples of Views</i>.</p>
</section>'''
nav = '<a class="wx" href="#big-picture">Big picture</a>' + ''.join(f'<a class="w{n}" href="#week-{n}">Topic {n}</a>' for n in range(1, 7)) + '<a class="wx" href="#supplement">Supplement</a><a class="wx" href="#cheat-sheet">Cheat sheet</a><a class="wx" href="#drill">Flashcards</a>'

CSS = (open(os.path.join(HERE, 'style.css')).read() + open(os.path.join(HERE, 'extra_cst.css')).read()
       + open(os.path.join(HERE, 'bigp.css')).read() + open(os.path.join(HERE, 'extra_cmt323.css')).read())
JS = open(os.path.join(HERE, 'script.js')).read()

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#060510">
<title>CSE341 Notes: Software Architecture and Design</title>
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
  <img class="subj" src="../assets/subjects/cse341.svg" width="96" height="96" alt="">
  <p class="eyebrow">CSE341 · Software Architecture and Design</p>
  <h1>Topics 1 to 6, as one story</h1>
  <p class="lead">Every topic exists because the one before it left a gap. Read it as <b>problem, solution, new problem</b>, and the facts hang together.</p>
  <nav class="jump" aria-label="Jump to a section">{nav}</nav>
</header>
<main>

<section id="big-picture" class="bigp wx">
  <h2 class="sec">Big picture: read this first</h2>
  <p class="headsup"><b>One question runs through all six topics:</b> how do we describe a software system so that builders, managers and customers can reason about it before and while it is built? Topic 1 says an architecture is a set of structures. Topic 2 says why it matters and why you need several views. Topic 3 names the styles designers reuse. Topics 4 and 5 then spell out the module styles (the code), and Topic 6 the running system (C&amp;C) and where it lives (allocation).</p>
  <h3>The chain: each topic fixes a gap the last one left</h3>
  <ol class="chain c6">
    <li class="w1"><span class="tn">Topic 1</span><b>What is architecture?</b><span class="kw">Structures, abstraction, views, module / C&amp;C / allocation</span><span class="bridge">But why bother, and one picture is not enough &hellip;</span></li>
    <li class="w2"><span class="tn">Topic 2</span><b>Why it matters, how to document it</b><span class="kw">Quality attributes, documentation, 4+1 views</span><span class="bridge">But designers keep meeting the same problems &hellip;</span></li>
    <li class="w3"><span class="tn">Topic 3</span><b>Architectural styles</b><span class="kw">Nine general styles: client-server, EDA, layered, SOA, microservice &hellip;</span><span class="bridge">But a name is not a design; each style needs detail &hellip;</span></li>
    <li class="w4"><span class="tn">Topic 4</span><b>Module views and four styles</b><span class="kw">Decomposition, uses, generalization, layered</span><span class="bridge">But two module styles are still missing &hellip;</span></li>
    <li class="w5"><span class="tn">Topic 5</span><b>Aspects and data model</b><span class="kw">Crosscutting concerns, data entities</span><span class="bridge">But all module views are static; what happens at runtime? &hellip;</span></li>
    <li class="w6"><span class="tn">Topic 6</span><b>Runtime and allocation styles</b><span class="kw">C&amp;C: call-return, data flow, event-based, repository. Allocation: deployment, install, work assignment</span><span class="bridge">The slides stop here: choosing a style is not covered.</span></li>
  </ol>

  <h3>How Topic 1 connects to Topic 6</h3>
  <p class="small">Topic 1 lists three kinds of structure and the questions each answers. Topics 4 to 6 are those three kinds again, one by one: module structures become the six module styles (Topics 4 and 5), C&amp;C structures become the C&amp;C styles and allocation structures become the three allocation styles (both Topic 6). Topic 3 is the bridge, because it shows the same styles in short form and tags some of them module (layered) and some C&amp;C (data-centered, SOA).</p>
  <div class="promise tbl-wrap"><table><thead><tr><th>Topic 1 raised &hellip;</th><th>Answered in &hellip;</th></tr></thead><tbody>
    <tr><td>Module structures and their questions</td><td><b>Topics 4 and 5</b> (six module styles).</td></tr>
    <tr><td>C&amp;C structures and their questions</td><td><b>Topic 6</b> (four categories, five styles).</td></tr>
    <tr><td>Allocation structures</td><td><b>Topic 6</b> (deployment, install, work assignment).</td></tr>
    <tr><td>Structure vs view, and several views</td><td><b>Topic 2</b> (4+1 views).</td></tr>
    <tr><td>Quality attributes</td><td><b>Topic 2</b> (what each needs). <b>Topics 4 to 6</b> (each style says what it is for).</td></tr></tbody></table></div>

  <h3>Four threads that run through all six topics</h3>
  <p class="small">These links are my own summary of the slides, to show how the topics connect. They are not slide text.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Thread</th><th class="t1">Topic 1</th><th class="t2">Topic 2</th><th class="t3">Topic 3</th><th class="t4">Topic 4</th><th class="t5">Topic 5</th><th class="t6">Topic 6</th></tr></thead><tbody>
    <tr><th>Structure vs view</th><td>Defined</td><td>4+1 views</td><td>Styles are patterns of structure</td><td>Module views</td><td>Module views (aspects, data)</td><td>C&amp;C and allocation views</td></tr>
    <tr><th>Quality attributes</th><td>Architecture enables or inhibits them</td><td>Performance, modifiability, security, scalability</td><td>Benefits listed per style</td><td>Modifiability and portability</td><td>Modifiability</td><td>Performance, security, availability</td></tr>
    <tr><th>Audience</th><td>Stakeholders</td><td>Education, communication, analysis</td><td>Designer</td><td>New developers, planners</td><td>Developers, data designers</td><td>Testers, operators, managers</td></tr>
    <tr><th>Layered and SOA</th><td>&ndash;</td><td>&ndash;</td><td>Layered and SOA introduced</td><td>Layered as a module style</td><td>&ndash;</td><td>SOA as a C&amp;C style</td></tr></tbody></table></div>

  <h3>If you remember only six sentences</h3>
  <ol class="five">
    <li><b>Topic 1:</b> software architecture is a set of structures, an abstraction that shows public details, and there are three kinds: module, component-and-connector and allocation.</li>
    <li><b>Topic 2:</b> architecture decides quality attributes, so document it, and use several views such as the 4+1 model because one picture suits no one.</li>
    <li><b>Topic 3:</b> architectural styles are reusable shapes made of components, connectors and constraints, from client-server to layered, SOA and pipe-and-filter.</li>
    <li><b>Topic 4:</b> module views show the static code through is-part-of, depends-on and is-a, in four styles: decomposition, uses, generalization and layered.</li>
    <li><b>Topic 5:</b> the last two module styles are aspects, for crosscutting concerns, and the data model, for data entities.</li>
    <li><b>Topic 6:</b> C&amp;C styles show runtime behaviour in four categories, and allocation styles map software to hardware, files and teams.</li>
  </ol>
</section>

<section id="story" class="band">
  <h2 class="sec">Previously on CSE341</h2>
  <p class="small">Tap a card to jump to that topic. Read the "But then" line, then the next card&rsquo;s "Problem": they are the same sentence.</p>
  {story_html}
</section>
{weeks_html}
{supplement_html}
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
<footer class="foot"><p>Built from the CSE341 (CKS221) Software Architecture and Design lecture decks, Lectures 1 to 6, one topic each, plus the supplementary views deck as its own section. The slides belong to their lecturers and publishers; this page is a student&rsquo;s own summary. The diagrams are redrawn, except the figures in the Supplement section, which are cropped from the supplementary deck. Items marked "my own" are not from the slides. Topic numbers here group the lectures as: Topic 1 = Lecture 1, Topic 2 = Lecture 2, Topic 3 = Lecture 3, Topic 4 = Lectures 4 and 5, Topic 5 = Lecture 6 and the supplement.</p></footer>
<script>
{JS}
</script>
</body>
</html>'''
open(os.path.join(OUT, 'index.html'), 'w').write(PAGE)
print('cse341 ok', len(PAGE), 'cards', N_CARDS)
