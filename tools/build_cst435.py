#!/usr/bin/env python3
"""CST435 Parallel and Cloud Computing: notes page built from the user's 5 lecture topics (7 decks)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root (the folder that GitHub Pages serves)
import os, json
from notes_lib import mindmap, terms, psn, qa, week, E

OUT = os.path.join(ROOT, 'cst435')
os.makedirs(OUT, exist_ok=True)

# ====================================================================== mind maps
MAPS = {
1: mindmap('Why Parallel?',
  [('Why one core stalled', ['Clock speed hit heat limits', 'Deep pipelines run hot', 'Design and testing too hard', 'Moore: transistors still grow']),
   ('The multi-core fix', ['Many cores on one chip (CMP)', '2x cores, 1/2 clock = 1/4 power', 'Hyper-threading: 2 threads/core', 'Every machine becomes parallel']),
   ('Parallel vs distributed', ['Parallel: faster, tightly coupled', 'Distributed: share resources', 'Fine grain vs coarse grain', 'Homogeneous vs heterogeneous']),
   ('Design basics', ['Distributed memory: messages', 'Shared memory: race conditions', 'Partition: data, task, model', 'Communicate, sync, balance load'])],
  [('Parallel machines', ['Cluster of PCs', 'Shared-memory multiprocessor', 'Chip multi-processor (CMP)']),
   ('Metrics', ['Speedup = T(1) / T(p)', 'Efficiency = S / p', 'Cost = p x T(p)', 'Computation-to-comm ratio']),
   ('Scalability', ['Strong: fixed input size', 'Weak: input grows with p', 'Sub, linear, super-linear']),
   ('HPC trends', ['TOP500 ranks by LINPACK', 'Green500 adds power use', 'MPI + OpenMP + CUDA hybrid'])],
  'Mind map of Topic 1: why parallel and distributed computing, metrics and scalability'),
2: mindmap('Cloud Computing',
  [('Idea and history', ['Computing as a public utility', 'Parkhill 1966: computer utility', 'Telecom VPNs gave the cloud icon', 'AWS 2006 from idle capacity']),
   ('Enabling technologies', ['Grid and cluster computing', 'Utility computing', 'Virtualization', 'Service-oriented architecture']),
   ('5 characteristics', ['On-demand self-service', 'Broad network access', 'Resource pooling', 'Rapid elasticity', 'Measured service']),
   ('Economics', ['CapEx becomes OpEx', 'Utility or subscription billing', 'May cost more in the long run', 'SLA with penalties'])],
  [('Service models', ['IaaS: Amazon EC2', 'PaaS: App Engine, Azure', 'SaaS: Sales Cloud, web apps']),
   ('Deployment models', ['Public cloud', 'Private (on-premise or hosted)', 'Community: common vision', 'Hybrid: two or more']),
   ('9 key features', ['Agility, cost, multi-tenancy', 'Device and location independence', 'Reliability, scalability', 'Security, maintenance, metering']),
   ('Challenges', ['Control of data, vendor lock-in', 'Network latency', 'SLA compliance (providers)', 'Proprietary APIs']),
   ('Adoption checklist', ['Deployment model', 'Application suitability', 'Financial advantage', 'Provider choice and SLA'])],
  'Mind map of Topic 2: cloud computing history, characteristics, service and deployment models'),
3: mindmap('Parallel Architecture',
  [('Memory hierarchy', ['L1 fastest, L3 largest', 'Locality: spatial + temporal', 'Cache hit vs miss', 'Write-through vs write-back']),
   ('Virtual memory', ['Cache for secondary storage', 'Pages of 4 to 16 KB', 'Page table: virtual to physical', 'TLB caches page-table entries']),
   ('Inside one core (ILP)', ['Pipelining: stages', 'Multiple issue, superscalar', 'Speculation: guess, then undo', 'Hardware multithreading, SMT'])],
  [('Flynn taxonomy', ['SISD: classic von Neumann', 'SIMD: vector units, GPUs', 'MISD: not commercial', 'MIMD: multi-core, clusters']),
   ('Shared memory', ['SMP; UMA vs NUMA', 'Bus contention limits scale', 'Cache coherence problem', 'Invalidate + snooping (MESI)']),
   ('Distributed memory', ['Clusters, Beowulf', 'Single system image', 'Loosely coupled systems']),
   ('Interconnects', ['Bus, crossbar (shared)', 'Ring, mesh, hypercube (direct)', 'Crossbar, omega (indirect)', 'Diameter, bisection width'])],
  'Mind map of Topic 3: memory hierarchy, ILP, Flynn taxonomy, shared and distributed memory, interconnects'),
4: mindmap('Parallel Software',
  [('Why it is on software', ['Problems keep growing', 'Hardware cannot keep pace', 'Auto-parallelising is limited', 'Serial copies do not help']),
   ('Writing parallel code', ['Task parallelism: split the tasks', 'Data parallelism: split the data', 'Tree-style global sum wins', 'Rethink the algorithm']),
   ('Coordination', ['Communication', 'Load balancing', 'Synchronization']),
   ('Grain size', ['Fine: easier load balance', 'Coarse: high comp/comm ratio'])],
  [('Performance', ['Speedup = Tserial / Tparallel', 'Efficiency = S / p', 'Wall clock vs CPU time', 'Linear, sub, super-linear']),
   ("Amdahl's law", ['S = 1 / (α + (1-α) / P)', 'Fixed problem size', 'Serial part caps the speedup']),
   ("Gustafson's law", ['S = P + (1-P) α', 'Problem grows with P', 'Serial share shrinks']),
   ('Overhead', ['Interprocess interaction', 'Synchronization and idling', 'Contention', 'Excess computation'])],
  'Mind map of Topic 4: why parallel software, task and data parallelism, speedup laws and overhead'),
5: mindmap('Communication',
  [('MPI', ['Message-passing library', '6 core calls (of 129)', 'Rank + communicator', 'Blocking vs non-blocking']),
   ('MPI collectives', ['Barrier: synchronize', 'Broadcast: one to many', 'Reduction: many to one', 'Scatter and gather']),
   ('Request-reply', ['doOperation, getRequest, sendReply', 'Failures: omission, timeout', 'Duplicates and lost replies'])],
  [('RPC', ['Client and server stubs', 'Marshal and unmarshal', 'Synchronous or asynchronous']),
   ('RMI and gRPC', ['RMI: methods on remote objects', 'gRPC: protobuf over HTTP/2', 'Proxy and skeleton']),
   ('Group + multicast', ['One-to-many delivery', 'FIFO, causal, total order', 'Overlay networks']),
   ('Decoupled styles', ['Publish-subscribe events', 'Message queue: put, get, poll', 'Shared memory']),
   ('Topologies', ['Client-server', 'Peer-to-peer', 'Group'])],
  'Mind map of Topic 5: MPI, request-reply, RPC, RMI, gRPC, group communication, queues'),
}

# ====================================================================== topic 1 visuals
t1_vis = '''
  <h3>The road to multi-core</h3>
  <ol class="tl">
    <li><b>Vacuum tubes</b><span>Early machines, huge and slow.</span></li>
    <li><b>Transistors</b><span>Smaller, cheaper, more reliable.</span></li>
    <li><b>Integrated circuit</b><span>A CPU on one chip: the microprocessor (8080 up to Pentium 4).</span></li>
    <li><b>Clock wall</b><span>Higher frequency means more heat and power, so single-core speed stalls.</span></li>
    <li><b>Multi-core</b><span>Use extra transistors for more cores instead (CMP).</span></li>
  </ol>
  <p class="small"><b>Moore's law (as the slides state it):</b> transistor density doubles roughly every 18 months. More transistors kept arriving, but they could no longer be spent on a faster clock.</p>
  <div class="tbl-wrap"><table><thead><tr><th></th><th>AMD ('05)</th><th>Intel ('06)</th><th>IBM ('04)</th><th>Sun ('07)</th></tr></thead><tbody>
  <tr><th>Processors per chip</th><td>2</td><td>2</td><td>2</td><td>8</td></tr>
  <tr><th>Threads per processor</th><td>1</td><td>2</td><td>2</td><td>16</td></tr>
  <tr><th>Threads per chip</th><td>2</td><td>4</td><td>4</td><td>128</td></tr></tbody></table></div>
  <h3>Parallel vs distributed</h3>
  <div class="tbl-wrap"><table><thead><tr><th></th><th>Parallel system</th><th>Distributed system</th></tr></thead><tbody>
  <tr><th>Goal</th><td>Faster execution of one application</td><td>Sharing resources, higher throughput</td></tr>
  <tr><th>Grain size</th><td>Fine</td><td>Coarse</td></tr>
  <tr><th>Architecture</th><td>Tightly coupled, homogeneous, may share memory</td><td>Loosely coupled, heterogeneous, no shared memory</td></tr>
  <tr><th>Concern</th><td>Splitting one job across processors</td><td>Hiding internals behind a single system image</td></tr></tbody></table></div>
  <p class="small">They overlap: both use many processors on a network, with several activities running and cooperating at once. Shared research issues: interprocess communication, resource management, scheduling and load balancing, grain size.</p>
  <h3>Worked example: summing 1024 numbers</h3>
  <p class="small">PE#0 holds the whole array and splits it by sending halves to other PEs. Serial time is 1023 additions. Each addition costs 1 time unit and each send costs 3. Notice that speedup rises with p, but efficiency falls because communication grows.</p>
  <div class="bars" role="table" aria-label="Summation example: speedup against ideal">
    <div class="row" role="row"><span>p = 2</span><span class="track"><span class="fill" style="width:98.75%"></span><span class="ideal" style="left:100%"></span></span><span>speedup 1.975 · eff. 98.75%</span></div>
    <div class="row" role="row"><span>p = 4</span><span class="track"><span class="fill" style="width:95.07%"></span><span class="ideal" style="left:100%"></span></span><span>speedup 3.803 · eff. 95.07%</span></div>
    <div class="row" role="row"><span>p = 8</span><span class="track"><span class="fill" style="width:86%"></span><span class="ideal" style="left:100%"></span></span><span>speedup 6.91 · eff. 86%</span></div>
  </div>
  <p class="small">Bar length = efficiency (speedup divided by p). The dark line is ideal linear speedup. Runtimes were 518, 269 and 148 time units.</p>
  <h3>Strong vs weak scalability</h3>
  <div class="two"><div><h4>Strong scalability</h4><p>Vary the number of processors, <b>keep the input size fixed</b> (the slides use n = 1024 and p from 1 to 512).</p></div>
  <div><h4>Weak scalability</h4><p>Vary the number of processors <b>and grow the input with them</b> (n = 1024 × p).</p></div></div>
  <h3>Parallelism basics</h3>
  <div class="two"><div><h4>Distributed memory</h4><p>Each process has its own memory. Cooperate by <b>point-to-point</b> or <b>collective</b> messages over an interconnection network (example: MPI). Partition the data across processes. PGAS mixes this with a global address space.</p></div>
  <div><h4>Shared memory</h4><p>Cores share one main memory over a bus or crossbar, as in multi-core CPUs. Risks: <b>race conditions</b> and keeping caches coherent (cache-coherent NUMA). Examples: Pthreads, OpenMP, CUDA.</p></div></div>
  <p class="small"><b>Designing a parallel program means deciding:</b> how to partition (data, task or model parallelism), how to communicate, how to synchronise, and how to balance load.</p>
'''
t1_terms = terms([
 ('Moore\'s law', 'Transistor density doubles roughly every 18 months (as the slides state it).'),
 ('Multi-core / CMP', 'Several processor cores replicated on a single die and socket. Also called Chip Multi-Processor.'),
 ('Hyper-Threading', 'Two threads execute at the same time on one core, so the OS sees two logical processors.'),
 ('Parallel computing', 'Using multiple processors together to solve a problem faster than one processor could.'),
 ('Examples of parallel machines', 'A cluster of PCs on a fast network, a shared-memory multiprocessor (SMP), and a chip multi-processor (CMP).'),
 ('Distributed system', 'Autonomous computers interconnected so they cooperate and share resources. Examples: cluster, grid.'),
 ('Speedup', 'T(1) / T(p): single-processor time over p-processor time. Sub-linear (< p), linear (≈ p), super-linear (> p, rare).'),
 ('Efficiency', 'Speedup divided by p. How usefully each processor is kept busy.'),
 ('Cost', 'Run time T(p) multiplied by p.'),
 ('Computation-to-communication ratio', 'Time spent computing divided by time spent sending messages. Higher means better speedup and efficiency.'),
 ('Strong / weak scalability', 'Fixed input size with more processors / input grows with the processors.'),
 ('TOP500 and LINPACK', 'TOP500 ranks HPC systems by LINPACK (solving a dense linear system A·x = b, in GFlop/s). Green500 ranks by power efficiency.'),
 ('HPC trend', '1993: CM5/1025, 5.9 GFlop/s, 1025 cores. 2016: Sunway TaihuLight, about 93 million GFlop/s, 10 million cores (six orders of magnitude). Modern HPC is hybrid: MPI between nodes, OpenMP inside a node, GPUs (CUDA) as accelerators.'),
])
t1_boss = qa('Why did the industry move to multi-core instead of just making one core faster?',
 '''<p>Clock frequency was getting hard to raise: deeply pipelined circuits run hot, the power draw and cooling costs grow, and designing and verifying such chips needs huge teams. Meanwhile more transistors kept arriving, so the spare transistors went into <b>more cores</b>. Doubling the cores while halving the frequency keeps the same performance at about a quarter of the power. Many applications were also already multithreaded.</p>''', 1) + \
 qa('In the summation example (n = 1024) the serial time is 1023 and the 8-PE run takes 148. Find the speedup and efficiency, and say why efficiency is lower than with 2 PEs.',
 '''<ul><li><b>Speedup</b> = 1023 / 148 ≈ <b>6.91</b>.</li><li><b>Efficiency</b> = 6.91 / 8 ≈ <b>86%</b> (with 2 PEs it was 98.75%).</li>
 <li><b>Why:</b> more PEs means more distribution steps, each costing communication time (3 units per send), so a larger share of the run is communication instead of useful addition. The computation-to-communication ratio drops.</li></ul>''', 2) + \
 qa('Quiz from the slides: machine A does 10 jobs/hour at $100/hour, machine B does 2 jobs/hour at $15/hour, and finishing earlier saves $6 per hour. You have 10 jobs. Which machine?',
 '''<p>My working (the slide gives no answer, so treat this as my reading):</p><ul><li><b>A:</b> 10 jobs take 1 hour, cost $100.</li><li><b>B:</b> 10 jobs take 5 hours, cost 5 × $15 = $75.</li>
 <li>A finishes 4 hours sooner, worth 4 × $6 = $24. So A's effective cost is $100 − $24 = <b>$76</b> against B's <b>$75</b>.</li></ul>
 <p>It is almost a tie, with B just $1 cheaper. A is better if finishing early matters more than the saving. The point is that price per hour alone is the wrong measure: you must compare <b>price per job including time saved</b> (the price/performance idea).</p>''', 3)

# ====================================================================== topic 2 visuals
t2_vis = '''
  <h3>How the idea grew</h3>
  <ol class="tl">
    <li><b>1960s</b><span>John McCarthy: computation may someday be organised as a public utility.</span></li>
    <li><b>1966</b><span>Douglas Parkhill, "The Challenge of the Computer Utility": elastic, online, public/private/community forms.</span></li>
    <li><b>1990s</b><span>Telecoms switch from dedicated circuits to VPNs and balance traffic. The cloud symbol marks the provider/user boundary.</span></li>
    <li><b>2006</b><span>Amazon sells spare data-centre capacity (often only ~10% used) as Amazon Web Services.</span></li>
    <li><b>2007–08</b><span>Google, IBM and universities start research. Gartner sees a shift from owned assets to per-use services.</span></li>
  </ol>
  <h3>The five characteristics, and what they mean</h3>
  <ul class="chips-row"><li><b>On-demand self-service</b></li><li><b>Broad network access</b></li><li><b>Resource pooling</b> (multi-tenancy)</li><li><b>Rapid elasticity</b></li><li><b>Measured service</b> (metering)</li></ul>
  <p class="small">Enabling technologies behind them: grid computing, cluster computing, utility computing, virtualization and service-oriented architecture.</p>
  <h3>Service models: who manages what</h3>
  <div class="layers" aria-label="Cloud service models">
    <div class="l"><b>SaaS<br><small>Application-as-a-service</small></b><span>You just use the finished application. Examples: Google web apps, CRM such as Salesforce Sales Cloud and Service Cloud.</span></div>
    <div class="l"><b>PaaS</b><span>You deploy your own code on the provider's platform. Examples: Google App Engine, Microsoft Azure.</span></div>
    <div class="l"><b>IaaS</b><span>You rent virtual infrastructure (servers, storage, network) and manage everything above it. Example: Amazon EC2.</span></div>
  </div>
  <p class="small">Memory hook: the higher up you go, the less you manage and the more the provider does.</p>
  <h3>Deployment models</h3>
  <div class="two">
    <div><h4>Public cloud</h4><p>Run by a cloud provider and offered to the general public.</p></div>
    <div><h4>Private cloud</h4><p>For one organisation, either on-premise or externally hosted.</p></div>
    <div><h4>Community cloud</h4><p>Shared by organisations with a common vision.</p></div>
    <div><h4>Hybrid cloud</h4><p>A combination of any two or more of the models above.</p></div>
  </div>
  <h3>Cloud layers (infrastructure)</h3>
  <ul class="chips-row"><li>Physical infrastructure</li><li>Virtual infrastructure</li><li>Applications and platform software</li><li>Cloud management and service-creation tools</li></ul>
  <h3>Money: CapEx to OpEx</h3>
  <div class="two">
    <div><h4>What you gain</h4><p>No upfront hardware purchase (<b>CapEx</b> becomes <b>OpEx</b>), pay only for use, low barriers to entry, shared costs, low management overhead, terminate any time, SLAs with financial penalties.</p></div>
    <div><h4>What to watch</h4><p>You may save little and even <b>pay more in operating cost</b>. It makes less sense when the capital expense is small or the capital budget is more flexible than the operating budget. Savings depend on your data-centre efficiency, existing costs, adoption level and what you host.</p></div>
  </div>
  <p class="small"><b>Billing items providers charge for:</b> instances (extra for high-memory or high-CPU), data transfer in and out, storage (GB-month), I/O requests, PUT and GET requests, IP addresses, load balancing. Some let you bid on instances.</p>
  <h3>Cloud is not the same as...</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Related idea</th><th>One-line difference</th></tr></thead><tbody>
   <tr><th>Autonomic computing</th><td>Systems that manage themselves</td></tr>
   <tr><th>Client-server</th><td>Any application split into service providers and requesters</td></tr>
   <tr><th>Grid computing</th><td>A virtual supercomputer from loosely coupled networked computers on very large tasks</td></tr>
   <tr><th>Mainframe</th><td>Powerful machines for bulk critical work, such as census and finance</td></tr>
   <tr><th>Utility computing</th><td>Computing sold as a metered service, like electricity</td></tr>
   <tr><th>Peer-to-peer</th><td>No central coordination; each participant is both supplier and consumer</td></tr></tbody></table></div>
  <h3>Challenges and adoption</h3>
  <div class="two">
    <div><h4>For consumers</h4><p>Control of data, data replication, network latency, unsupported applications, vendor lock-in.</p></div>
    <div><h4>For providers</h4><p>SLA compliance, software licensing model, proprietary APIs.</p></div>
    <div><h4>Before adopting, check</h4><p>Deployment model selection, application suitability, financial advantage, cloud provider selection, SLA.</p></div>
  </div>
'''
t2_terms = terms([
 ('Cloud computing', 'Internet-based computing where shared resources, software and information are provided on demand, like the electricity grid.'),
 ('Why "cloud"', 'A metaphor from network diagrams, where a cloud shape stood for the abstracted network. It marked the boundary of provider responsibility.'),
 ('Elastic provisioning', 'Resources scale up and down on demand, so users need not engineer for peak load.'),
 ('Multi-tenancy', 'Many users share the same resources and costs, which raises utilisation (systems are often only 10–20% utilised).'),
 ('QoS and SLA', 'Quality of Service requirements, usually written into a Service Level Agreement.'),
 ('Utility vs subscription billing', 'Utility: by resources consumed, like electricity. Subscription: by time, like a newspaper.'),
 ('Agility', 'Rapidly and cheaply re-provisioning infrastructure: faster idea-to-cash, reduced risk of innovation.'),
 ('Device and location independence', 'Access from any device and place through a web browser.'),
 ('Reliability', 'Redundant sites support business continuity and disaster recovery, yet big providers still suffer outages.'),
 ('Security', 'Can improve through centralisation and dedicated security resources, but control of sensitive data and audit-log access are concerns, and complexity rises as data spreads wider.'),
 ('Maintenance', 'Applications need no installation on every user machine, and updates reach everyone instantly.'),
 ('Metering', 'Usage measured per client and per application (daily to annually), which lets clients compare vendors on cost and QoS.'),
 ('Nicholas Carr', 'Argues IT is becoming standardised and cheaper, like the move from private electricity generators to the grid.'),
])
t2_boss = qa('Explain why cloud computing arose and what "CapEx to OpEx" means.',
 '''<p>Data centres were built for peak demand and sat mostly idle (Amazon's ran at about 10%). Amazon found that a new, shared architecture brought big efficiency gains and began selling access as AWS in 2006. Customers gain the same advantage: they <b>rent</b> computing instead of buying it, so a large one-time <b>capital expenditure</b> on hardware becomes a pay-as-you-go <b>operating expenditure</b>. That lowers barriers to entry, but the long-run operating bill can end up higher.</p>''', 1) + \
 qa('Which service model or deployment model fits? (a) A start-up wants to upload its own web app without managing servers. (b) A team wants raw virtual machines. (c) A company uses an online CRM. (d) A bank keeps regulated data in its own data centre but uses a provider for peaks.',
 '''<ul><li><b>(a) PaaS</b>, e.g. Google App Engine or Azure.</li><li><b>(b) IaaS</b>, e.g. Amazon EC2.</li><li><b>(c) SaaS</b>, e.g. Salesforce Sales Cloud.</li>
 <li><b>(d) Hybrid cloud</b>: a private cloud for the regulated data plus a public cloud for peak load.</li></ul>''', 2)

# ====================================================================== topic 3 visuals
t3_vis = '''
  <h3>Memory hierarchy: why caches work</h3>
  <div class="pyr" aria-label="Memory hierarchy from fast and small to large and slow">
    <div style="--k:0;width:34%"><b>L1 cache</b><br>smallest, fastest</div>
    <div style="--k:1;width:50%"><b>L2 cache</b></div>
    <div style="--k:2;width:66%"><b>L3 cache</b></div>
    <div style="--k:3;width:82%"><b>Main memory</b></div>
    <div style="--k:4;width:100%"><b>Secondary storage</b> (swap space for virtual memory)</div>
  </div>
  <div class="pyr-note"><span>faster, smaller</span><span>larger, slower</span></div>
  <p class="small"><b>Principle of locality:</b> after touching one location you tend to touch a nearby one (<b>spatial</b>) or the same one again soon (<b>temporal</b>). Summing an array with a cache block of 16 reads 16 elements in one fetch, so 16 additions run before the next read. A <b>hit</b> is found in cache; a <b>miss</b> goes to a lower level. Write-through updates memory on every write; write-back marks the line <b>dirty</b> and writes it only when the line is replaced.</p>
  <h3>Virtual memory in four steps</h3>
  <ol class="tl">
    <li><b>Too big</b><span>A program or its data may not fit in main memory.</span></li>
    <li><b>Pages</b><span>Keep only active pages (4 to 16 KB) in memory; idle ones sit in swap space.</span></li>
    <li><b>Page table</b><span>Maps virtual page numbers to physical addresses, but adds time to every access.</span></li>
    <li><b>TLB</b><span>A small cache (16 to 512 entries) of page-table entries. A page fault means the page is only on disk.</span></li>
  </ol>
  <h3>Inside one core: instruction-level parallelism</h3>
  <div class="bars" role="table" aria-label="1000 floating point additions">
    <div class="row" role="row"><span>Not pipelined</span><span class="track"><span class="fill" style="width:100%"></span></span><span>7000 ns</span></div>
    <div class="row" role="row"><span>7-stage pipeline</span><span class="track"><span class="fill" style="width:14.4%"></span></span><span>1006 ns</span></div>
  </div>
  <p class="small">One addition still takes 7 ns, but once the pipeline is full a result finishes every ns, so 1000 additions take about 1006 ns (7 to fill, then 999 more).</p>
  <div class="two">
    <div><h4>Pipelining</h4><p>Split a unit into stages; the output of one is the input of the next.</p></div>
    <div><h4>Multiple issue</h4><p>Replicate functional units. <b>Static</b>: scheduled at compile time. <b>Dynamic</b> (superscalar): scheduled at run time.</p></div>
    <div><h4>Speculation</h4><p>Guess an instruction's result (e.g. that z &gt; 0), run ahead, and recompute if the guess was wrong.</p></div>
    <div><h4>Hardware multithreading</h4><p><b>Fine-grained</b>: switch every instruction, skipping stalled threads. <b>Coarse-grained</b>: switch only on long stalls. <b>SMT</b>: threads share the functional units at once.</p></div>
  </div>
  <p class="small">Riddle from the slides: the lake is half covered on <b>day 59</b>, because the area doubles each day and is full on day 60.</p>
  <h3>Flynn's taxonomy</h3>
  <div class="flynn" aria-label="Flynn taxonomy grid">
    <div></div><div class="h">Single data stream</div><div class="h">Multiple data streams</div>
    <div class="h">Single instruction stream</div><div class="cell"><b>SISD</b>Classic von Neumann, one processor<small>one instruction, one data item at a time</small></div><div class="cell"><b>SIMD</b>Vector computers, GPUs<small>synchronous, one thread of control</small></div>
    <div class="h">Multiple instruction streams</div><div class="cell"><b>MISD</b>Pipeline; not commercially available<small>rare in practice</small></div><div class="cell"><b>MIMD</b>Multi-core, multiprocessors, distributed systems<small>asynchronous, many threads of control</small></div>
  </div>
  <p class="small"><b>Bank analogy:</b> tellers are processors, customers are tasks. <b>SIMD/SPMD:</b> accounts are split among tellers who all do the same thing in lockstep. <b>MIMD:</b> each teller processes a transaction her own way, and any shared data access is locked.</p>
  <h3>SIMD, vectors and GPUs</h3>
  <div class="two">
    <div><h4>SIMD</h4><p>Same instruction on many data items (data parallelism). With <b>4 ALUs and 15 items</b> it takes 4 rounds (4+4+4+3). Drawbacks: ALUs must all do the same thing or idle, they need no instruction storage, and it suits big regular data problems only.</p></div>
    <div><h4>Vector processors</h4><p>Vector registers, vectorised and pipelined units, <b>interleaved memory</b> banks, strided access, scatter/gather. <b>Pros:</b> fast, easy to use, vectorising compilers, high memory bandwidth. <b>Cons:</b> poor on irregular data, limited scalability.</p></div>
    <div><h4>GPUs</h4><p>Graphics pipeline turns points, lines and triangles into pixels. Several stages are programmable <b>shader functions</b>, implicitly parallel. Current GPUs use SIMD parallelism, though they are not pure SIMD.</p></div>
  </div>
  <h3>Shared memory and the cache coherence problem</h3>
  <p class="small">Shared-memory systems (SMP) let every processor reach every memory location through an interconnect. A bus does not scale well beyond about 64 processors because of <b>bus contention</b>.</p>
  <div class="two">
    <div><h4>UMA</h4><p>Uniform memory access: identical processors, <b>equal access time</b> to all memory. Typical SMP, also called CC-UMA.</p></div>
    <div><h4>NUMA</h4><p>Non-uniform: often several SMPs linked; memory across the link is <b>slower</b>. With coherence maintained it is CC-NUMA.</p></div>
  </div>
  <ol class="steps-h" aria-label="Cache coherence problem, step by step">
    <li><span>Core 1 reads <b>x = 15213</b> from main memory into its private cache.</span></li>
    <li><span>Core 2 reads x too: both caches hold 15213.</span></li>
    <li><span>Core 1 writes <b>x = 21660</b> (assume write-through, so memory also has 21660).</span></li>
    <li><span>Core 2 reads x again from its own cache and gets the <b>stale 15213</b>. That is the coherence problem.</span></li>
    <li class="srv"><span><b>Fix:</b> invalidation-based protocol with <b>snooping</b>. Core 1's write sends an invalidation over the inter-core bus, so Core 2's copy is marked INVALID and it must refetch.</span></li>
  </ol>
  <p class="small"><b>Invalidate vs update:</b> after several writes to one location, invalidation signals only once; update must broadcast every write with its new value. So invalidation usually produces less bus traffic and performs better. More refined protocols such as <b>MSI</b> and <b>MESI</b> (Modified, Exclusive, Shared, Invalid) add cache state bits. <b>Private caches</b> are closer and cause less contention; <b>shared caches</b> let threads share data and give one busy thread more space.</p>
  <h3>Distributed memory and interconnects</h3>
  <div class="two">
    <div><h4>Cluster</h4><p>A collection of whole computers joined by a network and used as one unified resource with a <b>single system image</b>. Cheap, scalable, "typical" environment. <b>Beowulf</b> is a do-it-yourself Linux cluster of up to hundreds of nodes.</p></div>
    <div><h4>Loosely coupled</h4><p>Whole computers (often heterogeneous) over TCP/IP. Suited to distributed applications, not parallel ones, unless very coarse-grained or trivially parallel.</p></div>
  </div>
  <div class="tbl-wrap"><table><thead><tr><th>Network (p nodes)</th><th>Diameter</th><th>Bisection width</th><th>Links</th></tr></thead><tbody>
   <tr><th>Fully connected</th><td>1</td><td>p²/4</td><td>p(p−1)/2</td></tr>
   <tr><th>Star</th><td>2</td><td>1</td><td>p−1</td></tr>
   <tr><th>Complete binary tree</th><td>2 lg((p+1)/2)</td><td>1</td><td>p−1</td></tr>
   <tr><th>Linear array</th><td>p−1</td><td>1</td><td>p−1</td></tr>
   <tr><th>Ring</th><td>(not filled on slide)</td><td>2</td><td>p</td></tr>
   <tr><th>Hypercube</th><td>log p</td><td>p/2</td><td>(p log p)/2</td></tr></tbody></table></div>
  <p class="small"><b>Shared-memory interconnects:</b> a <b>bus</b> (cheap, but contention grows with devices) or a <b>crossbar</b> switch (simultaneous communication, faster, but costly). <b>Distributed-memory:</b> <b>direct</b> (ring, toroidal mesh, fully connected, hypercube built by joining two lower-dimension cubes) or <b>indirect</b> (crossbar, omega network). <b>Bisection width</b> is the number of simultaneous communications possible across the divide when the machine is split in half; bisection bandwidth is the data rate across it.</p>
  <h3>Taxonomy in one tree</h3>
  <p class="small">Parallel computers split into <b>SIMD</b> (vector, GPU) and <b>MIMD</b> (pipeline-style systems, multiprocessors with shared memory such as SMP and multicore, and loosely coupled multicomputers with distributed memory such as clusters).</p>
'''
t3_terms = terms([
 ('Multitasking', 'Illusion of running many programs on one processor: each process takes a time slice, then waits.'),
 ('Thread', 'A unit of work inside a process. When one thread blocks, another can run. A master thread starts threads (forking) and waits for them (joining).'),
 ('Cache', 'Memory reachable faster than main memory, usually on the CPU chip.'),
 ('Spatial / temporal locality', 'Next access is near this one / this location is accessed again soon.'),
 ('Write-through / write-back', 'Update memory on every write / mark the line dirty and write on replacement.'),
 ('Virtual memory', 'Main memory acting as a cache for secondary storage, holding only active pages.'),
 ('Page table / TLB / page fault', 'Maps virtual to physical addresses / small cache of page-table entries / page is valid but only on disk.'),
 ('ILP', 'Instruction-level parallelism: several functional units execute instructions at once (pipelining, multiple issue).'),
 ('Superscalar', 'Dynamic multiple issue: units scheduled at run time.'),
 ('SMT', 'Simultaneous multithreading: a variation of fine-grained multithreading that lets several threads use the functional units together.'),
 ('SIMD / SPMD', 'Same instruction on many data (data parallelism). SPMD is the more common form on general-purpose machines.'),
 ('MIMD', 'Independent processors with their own control unit and ALU.'),
 ('SMP', 'Symmetric multiprocessor: shared global memory, equal access for all processors.'),
 ('UMA / NUMA', 'Equal memory access time / unequal; CC-NUMA when cache coherent.'),
 ('Cache coherence', 'If one processor updates a shared location, all others see the update. Done in hardware.'),
 ('Snooping', 'Caches watch the shared bus for writes by others and invalidate their stale copy.'),
 ('Diameter / bisection width', 'Longest shortest path between two nodes / simultaneous communications across the halves.'),
])
t3_boss = qa('Why do private caches create a coherence problem, and why is invalidation usually preferred over update?',
 '''<p>Each core caches its own copy of x. When one core writes a new value, other cores' copies (and possibly memory) are now <b>stale</b>, so another core can read an outdated value. The fix is a hardware coherence protocol. In the <b>invalidation-with-snooping</b> approach a write sends an invalidation across the inter-core bus, other copies are marked invalid, and they refetch when needed. After repeated writes to the same location, invalidation signals <b>only the first time</b>, whereas update must broadcast <b>every write</b> with its value, so invalidation generates less bus traffic.</p>''', 1) + \
 qa('Classify each with Flynn\'s taxonomy: (a) a GPU running one shader over many pixels, (b) a quad-core CPU running four different programs, (c) an old single-core PC. Then compute: a 7-stage, 1 ns-per-stage pipelined adder does 1000 additions. How long, and how much faster than unpipelined?',
 '''<ul><li><b>(a) SIMD</b>, <b>(b) MIMD</b>, <b>(c) SISD</b>.</li><li>Pipelined: 7 + 999 = <b>1006 ns</b>. Unpipelined: 1000 × 7 = <b>7000 ns</b>, so about <b>7× faster</b> (6.96).</li></ul>''', 2)

# ====================================================================== topic 4 visuals (calculator)
def am(a, P):
    return 1.0 / (a + (1 - a) / P)
def gu(a, P):
    return P - (P - 1) * a

def calc_html():
    a0, P0 = 0.67, 10
    X0, X1, Y0, Y1, MAXP = 56, 536, 292, 18, 64
    def px(p): return X0 + (p - 1) / (MAXP - 1) * (X1 - X0)
    def py(s): return Y0 - s / MAXP * (Y0 - Y1)
    def path(fn):
        return 'M' + ' L'.join(f'{px(p):.1f} {py(fn(p)):.1f}' for p in range(1, MAXP + 1))
    ticks = ''.join(f'<line class="ax" x1="{X0}" y1="{py(v):.1f}" x2="{X1}" y2="{py(v):.1f}"/><text class="tick" x="{X0 - 8}" y="{py(v) + 4:.1f}" text-anchor="end">{v}</text>' for v in (0, 16, 32, 48, 64))
    xt = ''.join(f'<text class="tick" x="{px(v):.1f}" y="{Y0 + 18}" text-anchor="middle">{v}</text>' for v in (1, 16, 32, 48, 64))
    return f'''
  <h3>Try it: Amdahl vs Gustafson</h3>
  <div class="calc">
    <div class="ctl">
      <div><label for="alpha">Serial fraction α <output id="alpha-o">67%</output></label><input id="alpha" type="range" min="0" max="100" value="67"></div>
      <div><label for="procs">Processors P <output id="procs-o">10</output></label><input id="procs" type="range" min="1" max="64" value="10"></div>
    </div>
    <div class="out">
      <div><b id="o-am">{am(a0, P0):.2f}</b><span>Amdahl speedup</span></div>
      <div><b id="o-gu">{gu(a0, P0):.2f}</b><span>Gustafson speedup</span></div>
      <div><b id="o-ea">{am(a0, P0) / P0 * 100:.0f}%</b><span>Amdahl efficiency</span></div>
      <div><b id="o-cap">{1 / a0:.2f}</b><span>Amdahl limit, 1/α</span></div>
    </div>
    <svg id="chart" viewBox="0 0 560 330" role="img" aria-label="Speedup against number of processors for Amdahl, Gustafson and ideal">
      {ticks}{xt}
      <path class="c-ideal" d="{path(lambda p: p)}"/>
      <path id="p-am" class="c-am" d="{path(lambda p: am(a0, p))}"/>
      <path id="p-gu" class="c-gu" d="{path(lambda p: gu(a0, p))}"/>
      <circle id="d-am" class="pt-am" r="5" cx="{px(P0):.1f}" cy="{py(am(a0, P0)):.1f}"/>
      <circle id="d-gu" class="pt-gu" r="5" cx="{px(P0):.1f}" cy="{py(gu(a0, P0)):.1f}"/>
      <text class="tick" x="{(X0 + X1) / 2}" y="326" text-anchor="middle">processors P</text>
      <text class="lg" x="70" y="34" fill="currentColor">- - ideal (linear)</text><text class="lg" x="70" y="52" style="fill:var(--c)">Gustafson</text><text class="lg" x="150" y="52" style="fill:var(--warn)">Amdahl</text>
    </svg>
    <p class="note">Slide example: α = 0.67 and P = 10 gives Amdahl 1.42 and Gustafson 3.97. Move α towards 0 and the two laws agree and approach ideal. Gustafson is higher because it assumes the problem grows with P.</p>
  </div>'''

t4_vis = f'''
  <h3>Why the burden moves to software</h3>
  <p class="small">Problems keep growing (climate modelling, protein folding, drug discovery, energy research, data analysis) and hardware and compilers cannot keep pace. In shared-memory programs you <b>start one process and fork threads</b>; in distributed-memory programs you <b>start multiple processes</b>. Running many copies of a serial program does not help: you want <b>one</b> program to run faster. Automatic translators exist but have had limited success and often produce very inefficient code, so sometimes the best parallel solution is a brand-new algorithm.</p>
  <h3>Better algorithm: summing across cores</h3>
  <div class="tree">
    <figure><svg viewBox="0 0 300 150" role="img" aria-label="Naive global sum: all cores send to core 0">
      <g class="ed"><path d="M150 38 L30 112"/><path d="M150 38 L65 112"/><path d="M150 38 L100 112"/><path d="M150 38 L135 112"/><path d="M150 38 L170 112"/><path d="M150 38 L205 112"/><path d="M150 38 L240 112"/><path d="M150 38 L272 112"/></g>
      <circle class="nm n" cx="150" cy="30" r="16"/><text x="150" y="34" text-anchor="middle">0</text>
      {''.join(f'<circle class="n" cx="{x}" cy="120" r="12"/><text x="{x}" y="124" text-anchor="middle">{i}</text>' for i, x in zip(range(1, 8), (30, 65, 100, 135, 170, 205, 240)))}
    </svg><figcaption><b>Naive:</b> everyone sends to the master. Core 0 does <b>7 receives and 7 additions</b> (999 each with 1000 cores).</figcaption></figure>
    <figure><svg viewBox="0 0 300 170" role="img" aria-label="Tree sum: pairs of cores add in rounds">
      <g class="ed"><path d="M150 28 L90 70"/><path d="M150 28 L210 70"/><path d="M90 78 L50 122"/><path d="M90 78 L130 122"/><path d="M210 78 L170 122"/><path d="M210 78 L250 122"/></g>
      <circle class="nm n" cx="150" cy="22" r="14"/><text x="150" y="26" text-anchor="middle">0</text>
      <circle class="n" cx="90" cy="74" r="13"/><text x="90" y="78" text-anchor="middle">0</text><circle class="n" cx="210" cy="74" r="13"/><text x="210" y="78" text-anchor="middle">4</text>
      <circle class="n" cx="50" cy="128" r="12"/><text x="50" y="132" text-anchor="middle">0</text><circle class="n" cx="130" cy="128" r="12"/><text x="130" y="132" text-anchor="middle">2</text>
      <circle class="n" cx="170" cy="128" r="12"/><text x="170" y="132" text-anchor="middle">4</text><circle class="n" cx="250" cy="128" r="12"/><text x="250" y="132" text-anchor="middle">6</text>
      <text x="150" y="160" text-anchor="middle" style="font-size:11px">(after odd cores 1, 3, 5, 7 have been added in)</text>
    </svg><figcaption><b>Tree:</b> pair up cores, halve the active cores each round. Core 0 does <b>3 receives and 3 additions</b> for 8 cores, and only <b>10</b> for 1000 cores: almost a 100× improvement over 999.</figcaption></figure>
  </div>
  <h3>Two ways to split the work</h3>
  <div class="two">
    <div><h4>Data parallelism</h4><p>Split the <b>data</b>; each core does similar operations on its part. Professor P's 300 scripts: three assistants grade <b>100 exams each</b>.</p></div>
    <div><h4>Task parallelism</h4><p>Split the <b>tasks</b>. The same three assistants each grade a different set of questions: <b>Q1–5, Q6–10, Q11–15</b> on every exam.</p></div>
  </div>
  <h3>Issues in designing parallel programs</h3>
  <ul class="chips-row"><li><b>Communication:</b> cores send partial sums to one another</li><li><b>Load balancing:</b> share work evenly</li><li><b>Synchronization:</b> keep cores from racing too far ahead</li></ul>
  <p class="small"><b>Grain size</b> is how many tasks one processor handles. <b>Coarse-grained</b> has a high computation-to-communication ratio; <b>fine-grained</b> balances load more easily.</p>
  <h3>Speedup, efficiency and the fence-painting example</h3>
  <p class="small">30 min of serial prep, 1 min per picket, 30 min of serial cleanup, 300 pickets.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Painters</th><th>Time</th><th>Speedup</th><th>Efficiency</th></tr></thead><tbody>
   <tr><td>1</td><td>30 + 300 + 30 = 360</td><td>1.0×</td><td>100%</td></tr>
   <tr><td>2</td><td>30 + 150 + 30 = 210</td><td>1.7×</td><td>85%</td></tr>
   <tr><td>10</td><td>30 + 30 + 30 = 90</td><td>4.0×</td><td>40%</td></tr>
   <tr><td>100</td><td>30 + 3 + 30 = 63</td><td>5.7×</td><td>5.7%</td></tr>
   <tr><td>Infinite</td><td>30 + 0 + 30 = 60</td><td>6.0×</td><td>very low</td></tr></tbody></table></div>
  <p class="small">The 60 minutes of serial work caps speedup at 6. That is Amdahl's law in action. A spray gun would be a better <b>serial</b> algorithm (120 minutes serial), and later speedups must be measured against it.</p>
  {calc_html()}
  <h3>Amdahl vs Gustafson in words</h3>
  <div class="two">
    <div><h4>Amdahl's law</h4><p>S = 1 / (α + (1−α)/P). The <b>problem size is constant</b>; speedup is bounded by the serial fraction α. Models control parallelism (fork-join).</p></div>
    <div><h4>Gustafson-Barsis's law</h4><p>S = P + (1−P)α. Programmers <b>scale the problem up</b> to use extra processors, so the serial share shrinks. Models data parallelism (SIMD/SPMD).</p></div>
  </div>
  <p class="small">They are two models with different meanings of "serial part", not a contradiction. Slide example, α = 0.67 on 10 processors: Amdahl 1.42, Gustafson 3.97.</p>
  <h3>Why real speedup falls short</h3>
  <div class="two">
    <div><h4>Shapes of speedup</h4><p><b>Trivially parallel</b> (ray tracing): S = P. <b>Divide and conquer</b> (merge sort): S ≈ P / log₂P. <b>Communication-bound</b> (large matrices): S ≈ 1/C(P). <b>Super-linear</b> exceeds the 45° line, but is rare.</p></div>
    <div><h4>Sources of overhead</h4><p><b>Interprocess interaction</b>, <b>synchronization</b>, <b>idling</b> (load imbalance, serial parts), <b>contention</b> for shared resources, <b>excess computation</b> (work the serial version never does). Roughly: T<sub>parallel</sub> = T<sub>serial</sub> / p + T<sub>overhead</sub>.</p></div>
  </div>
  <p class="small"><b>Taking timings:</b> decide what you are measuring (whole run, one segment, CPU time or wall-clock time). Use <b>MPI_Wtime</b> in MPI and <b>omp_get_wtime</b> in OpenMP. Communication cost is measured by <b>latency</b> (time for a message to cross) and <b>bandwidth</b> (data per unit time).</p>
'''
t4_terms = terms([
 ('Task parallelism', 'Partition the different tasks among cores.'),
 ('Data parallelism', 'Partition the data among cores; each does similar work on its part.'),
 ('Coordination', 'Communication, load balancing and synchronization.'),
 ('Load balancing', 'Sharing work evenly so no core is overloaded.'),
 ('Synchronization', 'Making sure cores working at different paces do not get too far ahead.'),
 ('Grain size', 'The group of tasks one processor performs; fine, medium or coarse.'),
 ('Parallel run-time', 'Time from the start of the computation to the moment the <b>last</b> processor finishes.'),
 ('Speedup', 'T1 / T(P), where T1 is the best sequential program. Linear is ideal; super-linear is rare.'),
 ('Efficiency', 'Speedup / P: fraction of time a processor is usefully employed.'),
 ('Scalability', 'Capacity to increase speedup in proportion to processors.'),
 ('Amdahl\'s law', 'S = 1/(α + (1−α)/P). Speedup is limited by the serial fraction.'),
 ('Gustafson-Barsis\'s law', 'S = P + (1−P)α. Larger problems keep more processors useful.'),
 ('Latency / bandwidth', 'Time for a message to go node to node / data transferable per unit time.'),
 ('Overhead sources', 'Interprocess interaction, synchronization, idling, contention, excess computation.'),
 ('Coming next', 'The course writes explicitly parallel C programs with Pthreads, OpenMP, MPI and CUDA.'),
])
t4_boss = qa("Explain how Gustafson's law differs from Amdahl's law and why they give different answers for the same program.",
 '''<p><b>Amdahl</b> fixes the problem size and asks how much faster that same problem runs on P processors; the serial fraction caps the speedup at 1/α. <b>Gustafson</b> fixes the run time and lets the problem grow with the machine, so the serial part becomes a smaller share and speedup keeps growing, S = P + (1−P)α. They answer different questions with different meanings of the "serial part". For α = 0.67 and P = 10, Amdahl gives 1.42 and Gustafson 3.97.</p>''', 1) + \
 qa('Using the fence-painting numbers (30 min prep, 1 min per picket, 30 min cleanup, 300 pickets), find the time, speedup and efficiency with 5 painters.',
 '''<ul><li><b>Time</b> = 30 + 300/5 + 30 = 30 + 60 + 30 = <b>120</b> minutes.</li><li><b>Speedup</b> = 360 / 120 = <b>3.0</b>.</li><li><b>Efficiency</b> = 3.0 / 5 = <b>60%</b>.</li></ul>
 <p>(Same pattern as the slide's table; the 5-painter row is my calculation, not printed on the slide.)</p>''', 2) + \
 qa('In the tree-style global sum, why does the master do fewer receives than in the naive version, and how many with 8 cores?',
 '''<p>In the naive version every other core sends to core 0, so core 0 does <b>7 receives and 7 additions</b>. In the tree version cores add in pairs and half of them drop out each round, so core 0 only handles <b>log₂8 = 3</b> receives and additions. The work is shared instead of piled on one core, and the gap grows with more cores (10 vs 999 for 1000 cores).</p>''', 3)

# ====================================================================== topic 5 visuals
t5_vis = '''
  <h3>The map of communication models</h3>
  <div class="two">
    <div><h4>Message passing (MPI)</h4><p>Each process has local memory; data moves only by messages. Best for clusters and parallel programs.</p></div>
    <div><h4>Request-reply, RPC, RMI, gRPC</h4><p>A client asks a server to run something and waits for the result. Remote invocation.</p></div>
    <div><h4>Group communication, multicast</h4><p>One message to every member of a group, without knowing who they are.</p></div>
    <div><h4>Publish-subscribe</h4><p>Publishers post events; subscribers receive the ones they registered interest in.</p></div>
    <div><h4>Message queuing</h4><p>Sender and receiver need not run at the same time; messages wait in a queue.</p></div>
    <div><h4>Shared memory</h4><p>Processes communicate by reading and writing shared data.</p></div>
  </div>
  <h3>MPI</h3>
  <p class="small">A message-passing <b>library specification</b>, not a language or a product. The MPI Forum began in 1992 and finalised the draft in May 1994; it is the de facto standard. A <b>communicator</b> groups processes and defines the context; <code>MPI_COMM_WORLD</code> holds all of them. Each process in a communicator has a <b>rank</b> numbered from 0.</p>
  <p class="small"><b>Six functions are enough</b> to write a complete program (MPI has 129): MPI_INIT, MPI_FINALIZE, MPI_COMM_SIZE, MPI_COMM_RANK, MPI_SEND, MPI_RECV.</p>
<pre class="code">program main
  MPI_INIT ( )
  MPI_COMM_SIZE (MPI_COMM_WORLD, count)
  MPI_COMM_RANK (MPI_COMM_WORLD, myid)
  print ("I am", myid, "of", count)
  MPI_FINALIZE ( )
end</pre>
  <div class="two">
    <div><h4>Point-to-point</h4><p>Always <b>exactly two</b> processes. <code>MPI_Send(buf, count, datatype, dest, tag, comm)</code> and <code>MPI_Recv(buf, count, datatype, source, tag, comm, status)</code>. Blocking calls return when finished; non-blocking return right away so the program can do other work. Modes: standard, buffered, synchronous, ready.</p></div>
    <div><h4>Collective</h4><p><b>Barrier</b>: everyone waits until all arrive (no data). <b>Broadcast</b>: one to many. <b>Reduction</b>: many to one with a computation. Also <b>scatter</b> (one to many) and <b>gather</b> (many to one).</p></div>
  </div>
  <p class="small">Every MPI message is <b>typed</b>: the datatype (e.g. MPI_INT, MPI_DOUBLE) must be given in both send and receive. Other services: virtual topologies, derived datatypes, dynamic task creation, client/server, one-sided put/get, parallel I/O.</p>
  <h3>Request-reply and its failure issues</h3>
  <p class="small">The base protocol under RPC and RMI. The client calls <b>doOperation</b> and waits; the server's <b>getRequest</b> receives it, runs the method, and <b>sendReply</b> returns the result. Runs over UDP or TCP.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Style</th><th>Client sends</th><th>Server sends</th></tr></thead><tbody>
    <tr><th>R</th><td>Request</td><td>nothing</td></tr><tr><th>RR</th><td>Request</td><td>Reply</td></tr><tr><th>RRA</th><td>Request, then acknowledge the reply</td><td>Reply</td></tr></tbody></table></div>
  <p class="small"><b>Problems to handle:</b> omission failures (lost messages), no guaranteed ordering, <b>timeouts</b>, discarding <b>duplicate requests</b>, lost replies, and keeping a <b>history</b> of replies.</p>
  <h3>RPC: ten steps</h3>
  <ol class="steps-h">
    <li><span>Client procedure calls the <b>client stub</b> as if it were local.</span></li>
    <li><span>Stub <b>marshals</b> the procedure id and arguments into a message and calls the local OS.</span></li>
    <li><span>Client OS sends the message to the remote OS.</span></li>
    <li class="srv"><span>Remote OS hands it to the <b>server stub</b>.</span></li>
    <li class="srv"><span>Server stub unpacks (<b>unmarshals</b>) parameters and calls the server procedure.</span></li>
    <li class="srv"><span>Server does the work and returns the result to the stub.</span></li>
    <li class="srv"><span>Stub packs the result into a message and calls the OS.</span></li>
    <li class="srv"><span>Server OS sends it to the client OS.</span></li>
    <li><span>Client OS gives the message to the client stub.</span></li>
    <li><span>Stub unpacks the result and returns to the client.</span></li>
  </ol>
  <p class="small">A <b>dispatcher</b> on the server picks which server stub handles a request. <b>Synchronous RPC</b>: the client blocks until the reply arrives. <b>Asynchronous RPC</b>: the client carries on after the request and the reply is handled later (it can even use two asynchronous calls, one each way).</p>
  <h3>RMI, DCE, gRPC</h3>
  <div class="two">
    <div><h4>RMI</h4><p>Invokes <b>methods on objects</b> in other processes. Uses a <b>communication module</b> (request-reply), a <b>remote reference module</b> (translates local and remote references), <b>proxies</b> on the client (hide marshalling) and a <b>dispatcher</b> plus <b>skeleton</b> on the server.</p></div>
    <div><h4>gRPC</h4><p>Google's RPC stack, open-sourced in 2015. Uses <b>protocol buffers</b> (binary serialisation, open-sourced 2008: compact, fast, version-tolerant) over <b>HTTP/2</b>. Platform independent and high performance.</p></div>
  </div>
  <div class="tbl-wrap"><table><thead><tr><th>RPC vs RMI</th><th>Same</th><th>Different</th></tr></thead><tbody>
    <tr><th>Similarities</th><td>Programming with interfaces; built on request-reply; similar transparency; local and remote calls use the same syntax</td><td></td></tr>
    <tr><th>Differences</th><td></td><td>RMI is object-oriented, with unique object references and richer parameter passing; RMI invokes <b>methods</b>, RPC invokes <b>functions</b></td></tr></tbody></table></div>
  <h3>Group communication, overlays, pub-sub, queues</h3>
  <div class="two">
    <div><h4>Multicast</h4><p>One message to every member of a group. Benefits: fault tolerance through replicated services, service discovery, better performance via replicated data, event notification. <b>Broadcast</b> goes to all machines.</p></div>
    <div><h4>Group communication</h4><p>The sender may not know the receivers. Groups are dynamic (create, join, leave). Needs <b>FIFO, causal or total ordering</b>, membership management, failure detection.</p></div>
    <div><h4>Overlay networks</h4><p>Virtual nodes and links on top of an existing network, adding services (multicast, secure communication) without changing the underlying network. Examples: Skype, peer-to-peer sharing, streaming, multi-player gaming.</p></div>
    <div><h4>Publish-subscribe</h4><p>Also "distributed event-based systems". Publishers publish structured events to an event service; subscribers register interest via subscriptions.</p></div>
  </div>
  <div class="tbl-wrap"><table><thead><tr><th>Queue primitive</th><th>Meaning</th></tr></thead><tbody>
    <tr><th>Put</th><td>Append a message to a queue</td></tr><tr><th>Get</th><td>Block until the queue is non-empty, then remove the first message</td></tr>
    <tr><th>Poll</th><td>Check the queue and remove the first message; never block</td></tr><tr><th>Notify</th><td>Install a handler called when a message is put in the queue</td></tr></tbody></table></div>
  <p class="small"><b>Topologies:</b> client-server (the most common), peer-to-peer (peers equally privileged, e.g. Napster, Kazaa, BitTorrent), and group (multicasting).</p>
'''
t5_terms = terms([
 ('MPI', 'Message Passing Interface: a message-passing library specification, the de facto standard for message-passing applications.'),
 ('Rank', 'A process\'s number within a communicator, starting at 0.'),
 ('Communicator', 'A group of processes plus a communication context. MPI_COMM_WORLD is the default one.'),
 ('Blocking / non-blocking', 'Returns when the operation completes / returns immediately so other work can proceed.'),
 ('Barrier / broadcast / reduction', 'Synchronise all / one to many / many to one with a combining operation.'),
 ('Derived datatype', 'User-built MPI type, which can describe non-contiguous data.'),
 ('Request-reply protocol', 'The base protocol for client-server remote invocation.'),
 ('Stub', 'Local stand-in that marshals arguments and unmarshals results so a remote call looks local.'),
 ('Marshalling', 'Packing a procedure id and arguments into a message.'),
 ('Dispatcher', 'Selects which server stub or method receives a request.'),
 ('Proxy / skeleton', 'RMI client stand-in for a remote object / server side that implements the remote interface.'),
 ('Protocol buffers', 'Google\'s binary serialisation format used with gRPC.'),
 ('Multicast / overlay network', 'One message to a group / virtual network built on top of a real one.'),
 ('Publish-subscribe', 'Decoupled event delivery from publishers to interested subscribers.'),
 ('Message queue', 'Loosely coupled communication with put, get, poll and notify.'),
])
t5_boss = qa('Compare RPC, RMI and gRPC.',
 '''<ul><li><b>RPC</b> calls a <b>procedure/function</b> in another process through client and server <b>stubs</b>, built on request-reply.</li>
 <li><b>RMI</b> calls <b>methods on remote objects</b>. It is object-oriented, uses unique object references and proxies/skeletons, so parameter passing is richer.</li>
 <li><b>gRPC</b> is Google's RPC stack: <b>protocol buffers</b> over <b>HTTP/2</b>, platform independent and fast, and necessary when talking to gRPC services such as Google's.</li></ul>
 <p>All three give the programmer the illusion of a local call.</p>''', 1) + \
 qa('Which model fits? (a) one process must tell every member of a group at once; (b) sender and receiver are not running at the same time; (c) clients only want events they asked for; (d) 8 MPI processes each hold a partial sum and process 0 needs the total.',
 '''<ul><li><b>(a)</b> Multicast / group communication.</li><li><b>(b)</b> Message queuing (put and get from a queue).</li><li><b>(c)</b> Publish-subscribe.</li><li><b>(d)</b> An MPI <b>reduction</b>, a collective operation (many to one).</li></ul>''', 2)

# ====================================================================== story, cheat sheet, flashcards
story = [
 (1, 'Why one core stopped being enough', 'Clock speed hit heat and power limits even though transistors kept multiplying.',
  'Multi-core chips, parallel and distributed computing, plus speedup, efficiency and scalability to judge them.', 'Owning big parallel machines is costly. What if you rent them?'),
 (2, 'Rent computing instead of owning it', 'Hardware sized for peak load sits idle most of the time.',
  'Cloud computing: on-demand, pooled, metered. IaaS, PaaS and SaaS; public, private, community, hybrid.', 'Whatever you rent, speed depends on how the hardware is built.'),
 (3, 'Inside a parallel machine', 'You need to know how caches, pipelines and many cores really work together.',
  'Memory hierarchy, ILP, Flynn taxonomy, shared and distributed memory, interconnects, cache coherence.', 'Hardware offers parallelism, but only software can use it.'),
 (4, 'The burden moves to software', 'Serial programs do not speed up on their own and compilers cannot parallelise well.',
  'Parallel algorithms, task and data parallelism, coordination, speedup laws and overhead analysis.', 'Separate processes with separate memory must talk to each other.'),
 (5, 'How processes talk', 'Distributed-memory processes can only cooperate by sending messages.',
  'MPI, request-reply, RPC, RMI, gRPC, group communication, publish-subscribe and message queues.', 'Next in the course: writing real code with Pthreads, OpenMP, MPI and CUDA.'),
]
story_html = '<ol class="story">' + ''.join(
    f'<li class="w{n}"><a href="#week-{n}"><span class="wk">Topic {n}</span><h3>{t}</h3>'
    f'<p><b>Problem</b>{p}</p><p><b>Fix</b>{s}</p><p class="but"><b>But then</b>{b}</p></a></li>' for n, t, p, s, b in story) + '</ol>'

numbers = [('S = T(1)/T(p)', 'speedup'), ('E = S / p', 'efficiency'), ('Cost = p × T(p)', 'run time times processors'),
           ('S = 1/(α+(1−α)/P)', 'Amdahl: fixed problem size'), ('S = P+(1−P)α', 'Gustafson: problem grows'),
           ('5', 'cloud characteristics (on-demand, network, pooling, elasticity, measured)'), ('3 + 4', 'service models (IaaS, PaaS, SaaS) + deployment models'),
           ('4', 'Flynn classes: SISD, SIMD, MISD, MIMD'), ('4 to 16 KB', 'typical page size'), ('16 to 512', 'TLB entries'),
           ('7 vs 3', 'master receives for 8 cores: naive vs tree'), ('6 of 129', 'MPI calls needed for a full program'),
           ('1006 ns', '1000 adds on a 7-stage pipeline'), ('1.42 vs 3.97', 'Amdahl vs Gustafson, α 0.67, P 10')]
numbers_html = '<ul class="nums">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in numbers) + '</ul>'
traps = [
 '<b>Amdahl</b> keeps the problem size fixed; <b>Gustafson</b> grows it with P. Both are correct for their own model.',
 '<b>Parallel</b> aims for faster execution (fine grain, tightly coupled); <b>distributed</b> aims at sharing resources (coarse grain, loosely coupled, no shared memory).',
 '<b>Strong</b> scalability = fixed input; <b>weak</b> scalability = input grows with the processors.',
 'Speedup is T(1)/T(p) against the <b>best sequential</b> program. Efficiency is speedup divided by <b>p</b>, not by time.',
 '<b>UMA</b>: equal access time. <b>NUMA</b>: unequal. Both can be cache coherent (CC-UMA, CC-NUMA).',
 '<b>Invalidate</b> beats <b>update</b> because it generates less bus traffic.',
 '<b>Write-through</b> updates memory immediately; <b>write-back</b> marks lines dirty and writes later.',
 '<b>Page table</b> maps virtual to physical addresses; the <b>TLB</b> caches page-table entries.',
 '<b>MISD</b> is not commercially available; SIMD includes GPUs, MIMD includes multi-core.',
 '<b>RPC</b> invokes functions; <b>RMI</b> invokes methods on objects. gRPC = protobuf + HTTP/2.',
 'The cloud <b>service models</b> (IaaS, PaaS, SaaS) are different from the <b>deployment models</b> (public, private, community, hybrid).',
 'Cloud can cost <b>more</b> in operating expense; CapEx savings are not guaranteed.',
]
traps_html = '<ul class="traps">' + ''.join(f'<li>{t}</li>' for t in traps) + '</ul>'
cards = [
 ('Why multi-core?', 'Higher clock speeds cause heat and power problems. Use the extra transistors for more cores; 2× cores at ½ frequency gives the same performance at ¼ the power.'),
 ('Parallel vs distributed: goal', 'Parallel: faster execution of one application. Distributed: sharing resources to raise throughput.'),
 ('Speedup, efficiency, cost', 'S = T(1)/T(p). E = S/p. Cost = p × T(p).'),
 ('Strong vs weak scalability', 'Strong: more processors, fixed input. Weak: more processors and a proportionally larger input.'),
 ('Cloud: five characteristics', 'On-demand self-service, broad network access, resource pooling, rapid elasticity, measured service.'),
 ('IaaS, PaaS, SaaS examples', 'IaaS: Amazon EC2. PaaS: Google App Engine, Microsoft Azure. SaaS: Google web apps, Salesforce Sales Cloud and Service Cloud.'),
 ('Four deployment models', 'Public, private (on-premise or externally hosted), community (common vision), hybrid (two or more).'),
 ('CapEx vs OpEx', 'Cloud turns upfront capital spending into operating spending. Savings are not guaranteed.'),
 ('Principle of locality', 'Spatial: nearby locations next. Temporal: the same location again soon.'),
 ('Write-through vs write-back', 'Update memory on each write vs mark dirty and write on replacement.'),
 ('Page table and TLB', 'Page table translates virtual to physical addresses; TLB caches 16 to 512 entries to avoid the lookup cost.'),
 ('Flynn taxonomy', 'SISD (von Neumann), SIMD (vector, GPU), MISD (pipeline, not commercial), MIMD (multi-core, clusters).'),
 ('UMA vs NUMA', 'Uniform: equal access time (SMP). Non-uniform: access across a link is slower (CC-NUMA).'),
 ('Cache coherence fix', 'Invalidation-based protocol with snooping; MSI and MESI add state bits. Invalidation generates less bus traffic than update.'),
 ('Bisection width', 'The number of simultaneous communications across the divide when a network is split in half.'),
 ('Task vs data parallelism', 'Task: split what is done. Data: split what it is done to. (Grading by question vs grading by exam pile.)'),
 ('Amdahl\'s law', 'S = 1/(α + (1−α)/P). Fixed problem size; the serial part caps speedup at 1/α.'),
 ('Gustafson-Barsis\'s law', 'S = P + (1−P)α. The problem grows with P, so the serial share shrinks.'),
 ('Sources of overhead', 'Interprocess interaction, synchronization, idling, contention, excess computation.'),
 ('MPI six basics', 'MPI_INIT, MPI_FINALIZE, MPI_COMM_SIZE, MPI_COMM_RANK, MPI_SEND, MPI_RECV.'),
 ('MPI collectives', 'Barrier (sync), broadcast (one to many), reduction (many to one), scatter, gather.'),
 ('RPC in one line', 'A client stub marshals the call, the server stub unmarshals and runs it, and the result returns the same way. Can be synchronous or asynchronous.'),
 ('RPC vs RMI', 'RPC calls functions; RMI calls methods on remote objects with unique references and proxies/skeletons.'),
 ('Message queue primitives', 'Put, Get (blocks), Poll (never blocks), Notify (handler on arrival).'),
]
cards_html = '<div class="cards" id="cards">' + ''.join(
    f'<button class="card" type="button" aria-pressed="false"><span class="front">{q}</span><span class="back">{a}</span></button>' for q, a in cards) + '</div>'

weeks_html = ''.join([
 week(1, '', 'Parallel and distributed computing', 'Why one fast core stopped being enough.',
      psn('Single-core clock speeds hit heat and power limits, though transistor counts kept growing.',
          'Put many cores on a chip, and study parallel and distributed computing with speedup, efficiency and scalability.',
          'Owning large parallel machines is expensive. What if you rent computing instead?'), MAPS[1], t1_vis, t1_terms, t1_boss),
 week(2, '', 'Cloud computing', 'Rent computing like electricity.',
      psn('Hardware sized for peak load sits mostly idle, and buying it needs a big upfront spend.',
          'Cloud computing: on-demand, pooled, metered resources delivered as IaaS, PaaS or SaaS on public, private, community or hybrid clouds.',
          'Whatever you rent, its speed depends on how the hardware is built.'), MAPS[2], t2_vis, t2_terms, t2_boss),
 week(3, '', 'Parallel architecture', 'What is really inside a parallel machine.',
      psn('To use parallel hardware well you must know how caches, pipelines and many cores cooperate.',
          'Memory hierarchy, virtual memory, ILP, Flynn taxonomy, shared and distributed memory, interconnects and cache coherence.',
          'Hardware offers parallelism, but only software can exploit it.'), MAPS[3], t3_vis, t3_terms, t3_boss),
 week(4, '', 'Parallel software', 'The burden moves to the programmer.',
      psn('Hardware and compilers cannot parallelise serial programs well enough on their own.',
          'Design parallel algorithms with task and data parallelism, coordinate cores, and judge results with speedup, Amdahl and Gustafson.',
          'Separate processes with separate memory can only cooperate by exchanging messages.'), MAPS[4], t4_vis, t4_terms, t4_boss),
 week(5, '', 'Communication', 'How processes talk to each other.',
      psn('Distributed-memory processes have no shared variables, so they must send messages.',
          'MPI, request-reply, RPC, RMI, gRPC, group communication, publish-subscribe and message queues.',
          'Next in the course: writing real programs with Pthreads, OpenMP, MPI and CUDA.'), MAPS[5], t5_vis, t5_terms, t5_boss),
])
nav = '<a class="wx" href="#big-picture">Big picture</a>' + ''.join(f'<a class="w{n}" href="#week-{n}">Topic {n}</a>' for n in range(1, 6)) + '<a class="wx" href="#cheat-sheet">Cheat sheet</a><a class="wx" href="#drill">Flashcards</a>'

CSS = open(os.path.join(HERE, 'style.css')).read() + open(os.path.join(HERE, 'extra_cst.css')).read() + open(os.path.join(HERE, 'bigp.css')).read()
JS = open(os.path.join(HERE, 'script.js')).read()
CALC_JS = '''
(function () {
  try {
    var a = document.getElementById('alpha'), p = document.getElementById('procs');
    if (!a || !p) { return; }
    var X0 = 56, X1 = 536, Y0 = 292, Y1 = 18, MAXP = 64;
    function px(n) { return X0 + (n - 1) / (MAXP - 1) * (X1 - X0); }
    function py(s) { return Y0 - s / MAXP * (Y0 - Y1); }
    function am(al, n) { return 1 / (al + (1 - al) / n); }
    function gu(al, n) { return n - (n - 1) * al; }
    function path(fn) { var d = []; for (var n = 1; n <= MAXP; n++) { d.push(px(n).toFixed(1) + ' ' + py(fn(n)).toFixed(1)); } return 'M' + d.join(' L'); }
    function set(id, t) { document.getElementById(id).textContent = t; }
    function render() {
      var al = a.value / 100, n = +p.value, sa = am(al, n), sg = gu(al, n);
      set('alpha-o', a.value + '%'); set('procs-o', n);
      set('o-am', sa.toFixed(2)); set('o-gu', sg.toFixed(2)); set('o-ea', Math.round(sa / n * 100) + '%');
      set('o-cap', al > 0 ? (1 / al).toFixed(2) : 'no limit');
      document.getElementById('p-am').setAttribute('d', path(function (k) { return am(al, k); }));
      document.getElementById('p-gu').setAttribute('d', path(function (k) { return gu(al, k); }));
      var da = document.getElementById('d-am'), dg = document.getElementById('d-gu');
      da.setAttribute('cx', px(n)); da.setAttribute('cy', py(sa)); dg.setAttribute('cx', px(n)); dg.setAttribute('cy', py(sg));
    }
    a.addEventListener('input', render); p.addEventListener('input', render); render();
  } catch (e) {}
})();
'''

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#060510">
<title>CST435 Parallel and Cloud Computing Notes</title>
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
  <p class="eyebrow">CST435 Parallel and Cloud Computing · Test notes</p>
  <h1>Topics 1 to 5, as one story</h1>
  <p class="lead">Every topic exists because the one before it left a gap. Read it as <b>problem, solution, new problem</b>, and the facts hang together.</p>
  <nav class="jump" aria-label="Jump to a section">{nav}</nav>
</header>
<main>

<section id="big-picture" class="bigp wx">
  <h2 class="sec">Big picture: read this first</h2>
  <p class="headsup"><b>One question runs through the whole subject:</b> how do many processors, inside one box or spread over a network, work together on one job, and what does it cost? Topic 1 asks the question, Topic 2 shows where you can rent the answer, Topics 3 and 4 show how hardware and software deliver it, and Topic 5 shows how the separate pieces talk to each other.</p>
  <h3>The chain: each topic fixes a gap the last one left</h3>
  <ol class="chain">
    <li class="w1"><span class="tn">Topic 1</span><b>Parallel and distributed computing</b><span class="kw">Multi-core, speedup, efficiency, scalability, shared vs distributed memory</span><span class="bridge">But owning big machines is costly &hellip;</span></li>
    <li class="w2"><span class="tn">Topic 2</span><b>Cloud computing</b><span class="kw">Rent, pool and meter resources: IaaS, PaaS, SaaS</span><span class="bridge">But speed depends on how the hardware is built &hellip;</span></li>
    <li class="w3"><span class="tn">Topic 3</span><b>Parallel architecture</b><span class="kw">Caches, ILP, Flynn, SMP and clusters, interconnects, coherence</span><span class="bridge">But hardware cannot parallelise your program &hellip;</span></li>
    <li class="w4"><span class="tn">Topic 4</span><b>Parallel software</b><span class="kw">Task and data parallelism, Amdahl, Gustafson, overhead</span><span class="bridge">But separate memories must send messages &hellip;</span></li>
    <li class="w5"><span class="tn">Topic 5</span><b>Communication</b><span class="kw">MPI, RPC, RMI, gRPC, multicast, publish-subscribe, queues</span><span class="bridge">Next: write real code (Pthreads, OpenMP, MPI, CUDA)</span></li>
  </ol>

  <h3>How Topic 1 connects to Topic 5</h3>
  <p class="small">Topic 1 (slide 20) lists the issues that parallel and distributed computing share: <b>interprocess communication</b>, resource management, scheduling and load balancing, and grain size. Topic 5 is the full answer to the first one. Topic 1 also splits systems into <b>shared-memory</b> (cooperate by sharing data) and <b>distributed-memory</b> (cooperate by messages). Topic 5 is the toolbox for the second kind: MPI, RPC, RMI, gRPC, multicast, publish-subscribe and queues.</p>
  <div class="promise tbl-wrap"><table><thead><tr><th>Topic 1 raised &hellip;</th><th>Answered in &hellip;</th></tr></thead><tbody>
    <tr><td>Interprocess communication</td><td><b>Topic 5</b> (message passing, remote calls, group communication). Interconnect hardware: Topic 3.</td></tr>
    <tr><td>Resource management, resource sharing, availability, incremental growth, wasted capacity (utilisation only about 25%)</td><td><b>Topic 2</b> (resource pooling, multi-tenancy, elasticity, redundant sites, metering).</td></tr>
    <tr><td>Scheduling and load balancing, grain size</td><td><b>Topic 4</b> (coordination, load balancing, fine vs coarse grain).</td></tr>
    <tr><td>Absolute performance and price/performance</td><td><b>Topic 3</b> (how hardware gets fast), <b>Topic 4</b> (speedup, Amdahl, Gustafson), <b>Topic 2</b> (pay per use).</td></tr>
    <tr><td>Computation-to-communication ratio</td><td><b>Topic 4</b> (overhead, latency, bandwidth) and <b>Topic 5</b> (what each message costs and can go wrong).</td></tr></tbody></table></div>

  <h3>Five threads that run through all five topics</h3>
  <p class="small">These links are my own summary of the slides, to show how the topics connect. They are not slide text.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Thread</th><th class="t1">T1 Intro</th><th class="t2">T2 Cloud</th><th class="t3">T3 Architecture</th><th class="t4">T4 Software</th><th class="t5">T5 Communication</th></tr></thead><tbody>
    <tr><th>How machines share data</th><td>Shared memory vs distributed memory basics</td><td>Cloud components talk through APIs and web services</td><td>SMP, UMA/NUMA vs clusters; cache coherence</td><td>Shared: fork threads. Distributed: start processes</td><td>Message passing (MPI) vs the shared-memory model</td></tr>
    <tr><th>The cost of talking</th><td>Computation-to-communication ratio; efficiency fell from 98.75% to 86% as p grew</td><td>Network latency; data-transfer charges</td><td>Bus contention, coherence traffic, interconnect limits</td><td>Latency, bandwidth, overhead</td><td>Failures: omission, timeouts, duplicate requests</td></tr>
    <tr><th>Scaling up</th><td>Strong and weak scalability</td><td>Rapid elasticity, scalability</td><td>A bus stops scaling around 64 processors</td><td>Serial part caps speedup (Amdahl)</td><td>Multicast and group communication reach many receivers</td></tr>
    <tr><th>Hiding the complexity</th><td>Distributed systems aim for a single system image</td><td>Cloud hides the infrastructure</td><td>A cluster presents one system image</td><td>Not hidden: you design the coordination yourself</td><td>Stubs and proxies make a remote call look local</td></tr>
    <tr><th>Many workers together</th><td>Multi-core chips, clusters, grids</td><td>Multi-tenancy, resource pooling</td><td>MIMD, SMT, multicore</td><td>Task and data parallelism</td><td>Group communication, publish-subscribe</td></tr></tbody></table></div>

  <h3>The three levels of a modern HPC system</h3>
  <p class="small">Topic 1 (HPC trends) says modern machines combine three kinds of parallelism. Each lands in a later topic.</p>
  <div class="hpc">
    <div><b>Between nodes: MPI</b>Message passing across a cluster. Topic 5 (communication), Topic 3 (clusters, interconnects).</div>
    <div><b>Inside a node: OpenMP</b>Multi-core CPUs sharing memory. Topic 3 (shared memory, coherence), Topic 4 (threads).</div>
    <div><b>Accelerators: CUDA</b>Massively parallel GPUs. Topic 3 (SIMD, GPUs).</div>
  </div>

  <h3>If you remember only five sentences</h3>
  <ol class="five">
    <li><b>Topic 1:</b> a single core ran out of heat budget, so chips got more cores, and we measure the gain with speedup, efficiency and scalability.</li>
    <li><b>Topic 2:</b> instead of buying for peak load, rent shared, metered resources on demand, as IaaS, PaaS or SaaS.</li>
    <li><b>Topic 3:</b> speed depends on the memory hierarchy, instruction-level tricks, how processors share memory, and keeping caches coherent.</li>
    <li><b>Topic 4:</b> software must be redesigned for parallelism, and its gain is capped by the serial part and by overhead.</li>
    <li><b>Topic 5:</b> processes with separate memories cooperate only by messages: MPI, remote calls, groups, events and queues.</li>
  </ol>
</section>

<section id="story" class="band">
  <h2 class="sec">Previously on Parallel and Cloud Computing</h2>
  <p class="small">Tap a card to jump to that topic. Read the "But then" line, then the next card's "Problem": they are the same sentence.</p>
  {story_html}
</section>
{weeks_html}
<section id="cheat-sheet" class="band wx">
  <h2 class="sec">Cheat sheet</h2>
  <h3>Formulas and numbers to remember</h3>
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
<footer class="foot"><p>Built from the CST435 lecture decks (Topics 1 to 5, including Parts 1 and 2). Diagrams are redrawn, not copied from the slides. Practical sections on Pthreads, OpenMP, MPI programming and CUDA are not in these decks.</p></footer>
<script>
{JS}
{CALC_JS}
</script>
</body>
</html>'''
open(os.path.join(OUT, 'index.html'), 'w').write(PAGE)
print('cst435 ok', len(PAGE))
