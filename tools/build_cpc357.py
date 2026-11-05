#!/usr/bin/env python3
"""CPC357 IoT Architecture and Smart Applications notes page.
Sources (all from the owner's folders): current-year decks Lecture 2 Sensors and Actuators, 3 IoT Circuit, 4 Embedded System,
5 IoT Networks (Mohd Nadhir Ab Wahab, USM); older Learning Materials decks for the topics this year's folder does not have yet:
Chapters 1 and 2 (Yung-Wey Chong, USM) and the IoT Protocol, Cloud Technology, Data Analytics and Security decks (Mohd Nadhir, 2024/25);
the project brief. Content rules: only what is in the decks; my own summaries, calculations and readings of figures are labelled on the page.
Diagrams are redrawn as inline SVG; no slide images.

Topics (my own grouping of the 12 decks): 1 = Chapters 1+2, 2 = Sensors and Actuators, 3 = IoT Circuit + Embedded System,
4 = IoT Networks + IoT Protocol, 5 = Cloud + Data Analytics + Security."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root (the folder that GitHub Pages serves)
from notes_lib import mindmap, terms, psn, qa, week, E

OUT = os.path.join(ROOT, 'cpc357')
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
1: mindmap('IoT System',
  [('What IoT is', ['Physical devices + software', 'Sensors and connectivity', 'Collect and exchange data', 'Sensor, link, process, UI']),
   ('Architecture parts', ['Sensors and actuators', 'Embedded system', 'IoT gateway', 'Wireless network', 'Cloud']),
   ('Design considerations', ['Scalability, reliability', 'Security and privacy', 'Power and cost', 'Interoperability'])],
  [('Protocol stack', ['IoT apps: CoAP, MQTT', 'Transport: UDP', 'Internet: IPv6, 6LoWPAN', 'Link: 802.X']),
   ('Gateway', ['Aggregates data', 'Translates protocols', 'Secures the channel', 'Processes locally']),
   ('Challenges', ['Security and privacy', 'Interoperability', 'Data analytics and AI', 'Scale and updates'])],
  'Mind map of Topic 1: what IoT is, its architecture parts, protocol stack, gateway and challenges'),
2: mindmap('Sensors and Actuators',
  [('Sensors', ['Output for a measurand', 'A transducer', 'Passive or active', 'Analog or digital']),
   ('Choosing one', ['Environment: temperature, size', 'Economics: cost, lifetime', 'Sensitivity, range, linearity', 'Response time, stability']),
   ('Sensor chain', ['Sensing element', 'Signal conditioning', 'ADC: sample, quantize, encode', 'Errors and calibration'])],
  [('Examples', ['Temperature, humidity', 'Accelerometer, gyro', 'Light, ultrasonic', 'Ultrasonic: echo timing']),
   ('Actuators', ['Produce action or motion', 'Hydraulic: big force', 'Pneumatic: air, quick', 'Electric: precise']),
   ('Electric kinds', ['Solenoid (linear)', 'DC and AC motor', 'Stepper and servo', 'Heater, light, siren']),
   ('The loop', ['Sensor measures', 'Controller decides', 'Actuator acts'])],
  'Mind map of Topic 2: sensors, how to choose them, the signal chain, and the types of actuators'),
3: mindmap('Circuit and Embedded',
  [('Basic circuit', ['Source, closed path, load', 'Current, voltage, resistance', 'Ohm: V = I x R', 'Open path: nothing works']),
   ('Series', ['Same current everywhere', 'Resistances add up', 'Voltage drops add up', 'One break stops all']),
   ('Parallel', ['Same voltage on each branch', 'Branch currents add up', 'Total R is smaller', 'Branches work separately'])],
  [('Embedded system', ['Hardware plus software', 'One task, runs alone', 'Real-time limits', 'Microcontroller on a chip']),
   ('Boards', ['Arduino', 'Raspberry Pi', 'Maker Feather AIoT S3', 'Factors: power, memory, pins']),
   ('Arduino program', ['setup() once, loop() forever', 'pinMode, digitalWrite', 'digitalRead, analogRead', 'analogWrite, servo write'])],
  'Mind map of Topic 3: circuit basics with Ohm law, series and parallel circuits, and embedded systems programming'),
4: mindmap('Networks and Protocols',
  [('Network basics', ['PAN, LAN, WAN', 'End and intermediary devices', 'Ethernet local, IP remote', 'Routers direct packets']),
   ('Wireless basics', ['Modulation of a carrier', 'Short vs long range', 'High vs low power', 'Few vs many devices']),
   ('Wireless kinds', ['RFID and NFC', 'Bluetooth LE, ZigBee', 'Wi-Fi, 6LoWPAN', 'LoRaWAN, Sigfox, cellular'])],
  [('Internet and transport', ['IPv6: 128-bit addresses', 'IANA, RIR, ISP', 'TCP: reliable', 'UDP: fast, best effort']),
   ('REST and CoAP', ['REST: resource URLs', 'CoAP: 4-byte header on UDP', 'GET POST PUT DELETE', 'Caching with Max-Age']),
   ('MQTT', ['Publish and subscribe', 'Broker and topics', 'QoS 0, 1, 2', 'Retained, last will'])],
  'Mind map of Topic 4: network basics, wireless technologies, internet layers and the REST, CoAP and MQTT protocols'),
5: mindmap('Cloud, Data, Security',
  [('Cloud basics', ['On-demand, pay as you go', 'Five NIST characteristics', 'IaaS, PaaS, SaaS', 'Public, private, hybrid']),
   ('Cloud benefits', ['Variable instead of capital cost', 'Economies of scale', 'Speed and agility', 'Go global in minutes']),
   ('Data in IoT', ['Volume, velocity, veracity', 'Garbage in, garbage out', 'Noise, anomalies, gaps', 'Data fusion'])],
  [('Databases', ['RDBMS: schema, ACID', 'NoSQL: flexible, BASE', 'Scale up vs scale out']),
   ('Security', ['Confidentiality', 'Integrity', 'Availability', 'Authentication, encryption']),
   ('Trust and privacy', ['Secure protocols: TLS, DTLS', 'Data minimisation', 'User consent', 'Transparency']),
   ('Real attacks', ['Mirai: default passwords', 'Verkada, Ring cameras', 'SILEX, ChargePoint'])],
  'Mind map of Topic 5: cloud computing, IoT data and databases, and security, trust and privacy'),
}

SRC12 = '<p class="small src"><b>Source of this topic:</b> Learning Materials decks, Chapter 1 (Introduction to IoT and Smart Applications) and Chapter 2 (IoT Architecture and Protocols), by Dr Yung-Wey Chong. These are the older decks in your folder; this year&rsquo;s folder has no Lecture 1.</p>'
SRC2 = '<p class="small src"><b>Source of this topic:</b> this year&rsquo;s Lecture 2 (7 Oct 2026, Mohd Nadhir Ab Wahab). Where marked &ldquo;older deck&rdquo;, the point comes from the Learning Materials Chapter 3 (Dr Chong), which covers the same topic in more depth.</p>'

# ====================================================================== topic 1
d_sys = svg(700, 150,
    box(8, 36, 100, 56, ['Sensors', 'detect'], small_rest=True) + box(128, 36, 100, 56, ['Embedded', 'device'], small_rest=True)
    + box(248, 36, 100, 56, ['Gateway', 'aggregate'], small_rest=True) + box(368, 36, 100, 56, ['Network', 'wireless, IP'], small_rest=True)
    + box(488, 36, 100, 56, ['Cloud', 'store, analyse'], small_rest=True) + box(608, 36, 86, 56, ['User', 'interface'], 'bxs', small_rest=True)
    + ''.join(arr(108 + 120 * i, 64, 128 + 120 * i, 64, 'sy') for i in range(5))
    + txt(350, 20, 'My own sketch of the parts named across Chapters 1 and 2 (the slides show this as a reference-model figure)', 'ts')
    + txt(68, 124, 'Actuators act on the', 'ts') + txt(68, 140, 'result (Topic 2)', 'ts')
    + arr(68, 112, 68, 96, 'sy', dash=True),
    'Sketch of an IoT system: sensors, embedded device, gateway, network, cloud and user interface, with actuators acting on the result', 'sy')

w1_vis = f'''
  {SRC12}
  <h3>What IoT is and how it works</h3>
  <p class="small"><b>Internet of Things (IoT)</b> means the network of physical devices embedded with electronics, software, sensors and network connectivity, so objects can collect and exchange data. The slides describe the flow in four steps: <b>sensor, connectivity, data processing, user interface</b>. A second slide frames the value as <b>connect things, control anything, gain insights, take action</b>. The phrase &ldquo;Internet of Things&rdquo; is credited to Kevin Ashton (MIT), from a talk about RFID technology to Procter &amp; Gamble. (The timeline figure shows a few more firsts, such as the smart fridge and the smart watch, but its dates are not clear in the text, so I left them out.)</p>
  {d_sys}
  <h3>Design considerations (the eight on the slide)</h3>
  <ul class="chips-row"><li>Scalability</li><li>Reliability and availability</li><li>Security and privacy</li><li>Performance</li><li>Interoperability</li><li>Power efficiency</li><li>Cost</li><li>Maintainability</li></ul>
  <p class="small">Interoperability means devices from different makers can work together. The slides use these eight as the checklist for the hospital scenario below.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Scenario on the slide</th><th>Discussion questions on the slide</th></tr></thead><tbody>
  <tr><td>MediCare Hospital tracks 5000 medical assets (wheelchairs, IV pumps, monitors) in a 10-storey building. Assets move between floors; battery replacement about once a year; location within 5 metres; usage history kept; budget $200,000; HIPAA compliance needed.</td><td>Which sensors and why? How to trade location accuracy against battery life? Edge or cloud processing? Main security concerns and fixes?</td></tr></tbody></table></div>
  <p class="small"><b>The slides give no model answers.</b> Use the eight considerations, the gateway (below) and Topic 2 to argue your own.</p>

  <h3>Embedded system, gateway and wireless choice</h3>
  <div class="two"><div><h4>Embedded versus general-purpose</h4><p>An embedded system does one dedicated job inside a larger system, with tightly matched software (firmware), a microcontroller, low power, a minimal interface and a small size. A general-purpose computer runs many tasks, has a full operating system, and uses more power.</p></div>
  <div><h4>IoT gateway</h4><p>A device that connects IoT devices to the cloud. It <b>aggregates</b> data, <b>translates</b> protocols, gives a <b>secure</b> channel and does some <b>local processing</b>. Benefits: lower delay, less bandwidth (filter and combine before sending), better security by local encryption.</p></div></div>
  <p class="small"><b>Choosing a wireless technology</b> (slide criteria): range, power use, data rate, delay, topology (point-to-point, star, mesh), cost, scalability, and the environment (indoor or outdoor, interference).</p>

  <h3>Protocol stack and trade-offs</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Layer</th><th>Conventional web</th><th>IoT</th></tr></thead><tbody>
  <tr><th>Application and payload</th><td>HTML, XML, JSON over HTTP</td><td>Binary or JSON over CoAP or MQTT</td></tr>
  <tr><th>Transport</th><td>TCP or UDP</td><td>UDP</td></tr>
  <tr><th>Internet</th><td>IPv4, IPv6</td><td>IPv6 and IP routing, with 6LoWPAN</td></tr>
  <tr><th>Network and link</th><td>Ethernet MAC and PHY</td><td>802.X MAC and PHY</td></tr></tbody></table></div>
  <div class="two"><div><h4>Advantages of IoT (slide)</h4><p>Less human effort and time; more automation and optimisation; less waste and better use of natural resources.</p></div>
  <div><h4>Disadvantages (slide)</h4><p>Security of confidential data; network attacks; keeping privacy.</p></div></div>
  <p class="small"><b>Four challenges:</b> security and privacy (encryption, authentication and access control, privacy rules such as PDPA); interoperability (many standards, need common frameworks); data analytics and AI (big data, predictive machine learning, AI-driven decisions); scalability and management (huge device counts, over-the-air updates, device lifecycle).</p>
'''
w1_terms = terms([
 ('IoT', 'Network of physical devices with electronics, software, sensors and connectivity that collect and exchange data.'),
 ('Four-step flow', 'Sensor, connectivity, data processing, user interface.'),
 ('Embedded system', 'A computer built into a larger machine to do one dedicated task, with software tuned to its hardware.'),
 ('Microcontroller / SoC', 'A small computer on one chip; the slides prefer a System on Chip (SoC) for size and power limits.'),
 ('IoT gateway', 'Device between IoT devices and the cloud: aggregates, translates protocols, secures and pre-processes data.'),
 ('Edge versus cloud processing', 'Processing near the device versus in the cloud. The slides ask you to choose and justify; they give no rule.'),
 ('CoAP', 'Constrained Application Protocol, a light, HTTP-like protocol for small devices.'),
 ('MQTT', 'Message Queuing Telemetry Transport, a light publish/subscribe messaging protocol.'),
 ('6LoWPAN', 'A way to run IPv6 over low-power wireless links (named in the IoT stack).'),
 ('Interoperability', 'Devices and systems from different makers working together.'),
 ('PDPA', 'The privacy law named on the challenges slide. The slide gives no detail on it.'),
])
w1_boss = ''.join([
 qa('What is IoT, and what are the four steps of how it works on the slides?',
  '''<p>IoT is a network of physical devices that contain electronics, software, sensors and connectivity, so they can collect and exchange data. The four steps are sensor (detect), connectivity (send), data processing (analyse) and user interface (show or act).</p>''', 1),
 qa('List the eight design considerations.',
  '''<p>Scalability, reliability and availability, security and privacy, performance, interoperability, power efficiency, cost, maintainability.</p>''', 2),
 qa('What are the four jobs of an IoT gateway, and two benefits?',
  '''<p>Data aggregation, protocol translation, security, local processing. Benefits (any two): lower delay because data is processed locally; less bandwidth because data is filtered and combined before going to the cloud; better security through local encryption and data management.</p>''', 3),
 qa('Compare an embedded system with a general-purpose computer on four points.',
  '''<p>Purpose: dedicated task versus many tasks. Hardware: microcontroller with limited resources versus powerful CPU, GPU and memory. Software: firmware versus a full operating system. Power: energy-efficient versus high consumption. (Also: minimal interface and compact size versus full interface and larger form.)</p>''', 4),
 qa('How does the IoT protocol stack differ from the conventional web stack?',
  '''<p>Application layer: CoAP or MQTT with binary or JSON payload instead of HTTP with HTML, XML or JSON. Transport: UDP. Internet layer: IPv6 with 6LoWPAN. Link: 802.X MAC and PHY instead of Ethernet. Each choice suits low-power, small devices (the reason is spelled out in Topic 4).</p>''', 5),
 qa('For the MediCare scenario, name two design considerations that matter most and say why. (The slides give no answer; this is my own reasoning.)',
  '''<p><b>My reasoning:</b> power efficiency, because the target is one battery change per year across 5000 assets; and security and privacy, because the hospital needs HIPAA compliance. Cost also matters because of the $200,000 budget. The slides leave the actual answers open.</p>''', 6),
])

# ====================================================================== topic 2
d_loop = svg(700, 130,
    box(10, 30, 150, 56, ['Sensor', 'measures temperature'], small_rest=True) + box(270, 30, 150, 56, ['Controller', 'decision maker'], small_rest=True)
    + box(530, 30, 150, 56, ['Actuator', 'cooling fan'], 'bxs', small_rest=True)
    + arr(160, 58, 270, 58, 'lp') + arr(420, 58, 530, 58, 'lp')
    + txt(215, 46, 'reading', 'ts') + txt(475, 46, 'if too hot: fan on', 'ts') + txt(475, 78, 'else: no action', 'ts')
    + txt(350, 116, 'The usable output of a sensor becomes the input of an actuator (slide)', 'ts'),
    'Redrawn: sensor measures temperature, controller decides, actuator turns on a cooling fan', 'lp')

d_adc = svg(700, 120,
    box(10, 30, 120, 56, ['Physical', 'quantity'], small_rest=True) + box(160, 30, 120, 56, ['Sensing', 'element'], small_rest=True)
    + box(310, 30, 120, 56, ['Signal', 'conditioning'], small_rest=True) + box(460, 30, 120, 56, ['ADC', 'to digital'], small_rest=True)
    + box(610, 30, 84, 56, ['Controller'], 'bxs')
    + ''.join(arr(130 + 150 * i, 58, 160 + 150 * i, 58, 'ad') for i in range(4))
    + txt(350, 108, 'Older deck (Chapter 3), my chain drawing from its slides', 'ts'),
    'Redrawn: sensor signal chain from physical quantity to sensing element, signal conditioning, analog to digital conversion, controller', 'ad')

w2_vis = f'''
  {SRC2}
  <h3>What a sensor is</h3>
  <p class="small">The American National Standards Institute (ANSI) defines a sensor as a device that gives a usable output in response to a specified <b>measurand</b> (the thing being measured). It acquires a physical parameter and converts it into a signal suitable for processing (optical, electrical, mechanical), so a sensor is a <b>transducer</b>. Without sensors there would be no automation. Sensors detect many kinds of phenomena: <b>acoustic</b> (wave amplitude, phase, velocity), <b>electric</b> (charge, voltage, current), <b>optical</b> (refractive index, reflectivity), <b>mechanical</b> (position, velocity, force, pressure), <b>biological/chemical</b> (fluid concentrations), <b>magnetic</b> (field, flux) and <b>thermal</b> (temperature, heat).</p>
  <p class="small">The slide lists four physical principles behind sensors: Ampere&rsquo;s law (a current-carrying conductor in a magnetic field feels a force), the Curie-Weiss law (above a transition temperature a ferromagnetic material behaves as paramagnetic), Faraday&rsquo;s law of induction (a coil resists a change in magnetic field), and the photoconductive effect (light on certain semiconductors lowers their resistance, as in a photoresistor).</p>
  <h3>Choosing a sensor</h3>
  <div class="tbl-wrap"><table><thead><tr><th>Environmental factors</th><th>Economic factors</th><th>Sensor characteristics</th></tr></thead><tbody>
  <tr><td>Temperature range, humidity effects, corrosion, size, overrange protection, susceptibility to EM interference, ruggedness, power consumption, self-test capability</td><td>Cost, availability, lifetime</td><td>Sensitivity, range, stability, repeatability, linearity, error, response time, frequency response</td></tr></tbody></table></div>
  <p class="small"><b>Older deck (Chapter 3):</b> a good sensor has accuracy and precision, sensitivity (output change per input change), suitability to its environment, linearity, fast response time, high resolution, selectivity (specific to its target) and low noise sensitivity. <b>Passive</b> sensing detects energy that is naturally available (such as reflected sunlight); <b>active</b> sensing uses its own energy source and measures the reflection (examples on the slide: synthetic aperture radar and laser fluorosensors).</p>

  <h3>Sensors on the slides</h3>
  <div class="cards3">
    <div class="c"><h4>Temperature</h4><p>Used in buildings, plants, engines, appliances and computers. Temperature can also be measured indirectly through pressure, volume, electrical resistance or strain.</p></div>
    <div class="c"><h4>Accelerometer</h4><p>Measures along one axis and ignores the other directions. Used for vibration, impacts, air bags, washing machines, heart monitors, car alarms.</p></div>
    <div class="c"><h4>Gyro</h4><p>Senses angular velocity: rotation angle change per unit time, in degrees per second. Used in car navigation, stability control, mobile games, camera-shake detection, robots.</p></div>
    <div class="c"><h4>Light</h4><p>Built from a photoresistor, photodiode or phototransistor. Used in cameras, infrared detectors and ambient lighting.</p></div>
    <div class="c"><h4>Ultrasonic</h4><p>The transmitter (trig pin) sends a 40 kHz sound; if it hits an object the sound bounces back to the receiver (echo pin). This is SONAR; the radio version is RADAR. The slide says distance is calculated from time-of-flight. <b>My own working:</b> distance = speed of sound x echo time / 2, because the sound travels there and back.</p></div>
    <div class="c"><h4>More modules</h4><p>The slides show a photo catalogue of Arduino-style sensor modules (soil moisture, flame, PIR motion, DHT11, and others) with no text. See the DHT code in Topic 3.</p></div>
  </div>
  <h3>From signal to data (older deck)</h3>
  {d_adc}
  <div class="tbl-wrap"><table><thead><tr><th>Step</th><th>Idea</th></tr></thead><tbody>
  <tr><th>Sensing element</th><td>The transducer that touches the phenomenon: thermistor for temperature, piezoelectric crystal for pressure, photoresistor for light.</td></tr>
  <tr><th>Signal conditioning</th><td>Amplification, attenuation, filtering (reject unwanted noise), linearisation, isolation (protect equipment), cold junction compensation (for thermocouples).</td></tr>
  <tr><th>Analog versus digital</th><td>Analog output is continuous (0 to 100 &deg;C) and needs ADC; digital output is 0s and 1s (motion or no motion).</td></tr>
  <tr><th>ADC</th><td>Sampling (continuous to discrete; Nyquist: sample at least twice the highest frequency, otherwise aliasing), quantisation (match to the nearest of limited levels; more bits give more levels), encoding (binary code).</td></tr>
  <tr><th>Errors</th><td>Systematic (repeatable: calibration, design, environment) and random (noise, thermal, vibration). Fixes: bridge circuits, temperature compensation, shielding, digital filtering, calibration curves.</td></tr></tbody></table></div>

  <h3>Actuators: the other half</h3>
  <p class="small">An actuator produces action or motion. Its input is mainly an electrical signal, air or fluid; its output is a position or a rate, from a few microns to a few metres. The slide&rsquo;s loop: the <b>sensor</b> reads temperature, the <b>controller</b> decides, the <b>actuator</b> acts.</p>
  {d_loop}
  <div class="tbl-wrap"><table><thead><tr><th>Type</th><th>How it works</th><th>Advantages</th><th>Disadvantages</th></tr></thead><tbody>
  <tr><th>Hydraulic</th><td>Fluid pressure in a cylinder or fluid motor gives linear, rotary or oscillating motion.</td><td>Very large force and high speed; welding, clamping, lifting vehicles.</td><td>Leaks, expensive, needs noise reduction, heat exchangers and high maintenance.</td></tr>
  <tr><th>Pneumatic</th><td>Vacuum or compressed air gives linear or rotary motion.</td><td>Low cost, works at extreme temperatures, low maintenance, long life, quick start and stop.</td><td>Pressure loss reduces efficiency; compressor must run all the time; air can be polluted.</td></tr>
  <tr><th>Electric</th><td>A motor turns electrical energy into torque (the slide&rsquo;s example is a solenoid electric bell).</td><td>Many industrial uses (automating valves), quiet, no fluid leaks, reprogrammable, best position control.</td><td>Expensive; depends on environmental conditions.</td></tr></tbody></table></div>
  <p class="small"><b>Electric examples on the slides:</b> a <b>solenoid</b> is a tightly wound coil that makes a magnetic field when current flows (control valves, car doors). Rotary actuators include <b>DC, AC, stepper and servo motors</b>. <b>Other actuators:</b> heaters (with a temperature sensor and controller), lights (show machine state) and sirens or horns (warn about unattended or dangerous machines). The older deck adds thermal and magnetic actuators (a wax that expands as it warms).</p>
  <p class="small">One slide shows the cycle as &ldquo;the observation&rdquo; (sensor sees a physical change and gives a low-power electrical output), &ldquo;the translation&rdquo; (the microcontroller reads it and triggers a response) and &ldquo;the action&rdquo; (a higher-power electrical input becomes a physical change, such as a heater turning on). <b>Two slips on the slides (my note):</b> the electric actuator text sits under a repeated &ldquo;Pneumatic Actuators&rdquo; title, and the rotary actuator slide calls a rotary actuator a &ldquo;pneumatic cylinder&rdquo; yet lists motors.</p>
'''
w2_terms = terms([
 ('Sensor', 'Device that gives a usable output in response to a specified measurand (ANSI definition).'),
 ('Measurand', 'The physical quantity being measured. (My plain gloss; the slide uses the word without defining it.)'),
 ('Transducer', 'Converts one form of energy or signal into another; a sensor is one.'),
 ('Passive / active sensing', 'Passive uses naturally available energy; active sends out its own energy and reads the reflection (older deck).'),
 ('Sensitivity', 'Change in output relative to change in input.'),
 ('Linearity', 'Output proportional to input; an ideal sensor is not nonlinear.'),
 ('Signal conditioning', 'Amplifying, filtering, isolating and otherwise preparing the sensor signal.'),
 ('ADC', 'Analog-to-digital conversion: sampling, quantisation, encoding.'),
 ('Nyquist criterion', 'Sample at least twice the highest frequency in the signal.'),
 ('Aliasing', 'Overlap of frequency components when sampling is too slow.'),
 ('Actuator', 'Device that produces action or motion from an input such as an electrical signal, air or fluid.'),
 ('Solenoid', 'A coil of wire that makes a magnetic field when current passes; a linear actuator.'),
 ('Servo motor', 'Motor with position feedback; the slide code sets its angle from 0 to 180 degrees.'),
])
w2_boss = ''.join([
 qa('Define sensor and actuator, and say how they connect in an IoT system.',
  '''<p>A sensor gives a usable output (an electrical signal) in response to a measurand, converting a physical parameter into a signal. An actuator produces action or motion from an input such as an electrical signal, air or fluid. The controller reads the sensor and decides; the usable output of a sensor becomes the input signal for an actuator. Example on the slide: temperature sensor, controller, cooling fan.</p>''', 1),
 qa('List the three groups of factors for choosing a sensor, with two examples each.',
  '''<p>Environmental (temperature range, humidity effects, corrosion, size, ruggedness, power consumption); economic (cost, availability, lifetime); sensor characteristics (sensitivity, range, stability, repeatability, linearity, response time).</p>''', 2),
 qa('How does an ultrasonic sensor measure distance? Give the formula and a worked example (the formula is my own working).',
  '''<p>The trig pin sends a 40 kHz sound; if an object is in the way, it reflects back to the echo pin. The slide says the distance comes from time-of-flight. <b>My working:</b> distance = speed x time / 2 (divide by 2 because the sound goes out and back). <b>Example (my numbers, speed of sound taken as about 343 m/s, not on the slide):</b> an echo time of 0.01 s gives 343 x 0.01 / 2 = 1.715 m.</p>''', 3),
 qa('Walk through the sensor signal chain from the older deck, and say why each step exists.',
  '''<p>Sensing element touches the phenomenon; signal conditioning amplifies, filters and cleans the weak or noisy signal; the ADC samples, quantises and encodes it into digital values; the controller then uses the data. Sampling must be at least twice the highest signal frequency (Nyquist) or aliasing happens.</p>''', 4),
 qa('Compare hydraulic, pneumatic and electric actuators.',
  '''<p>Hydraulic: huge force, but leaks, cost and maintenance. Pneumatic: cheap, durable, quick, but the compressor must keep running and pressure loss costs efficiency. Electric: quiet, leak-free and reprogrammable with the best position control, but expensive and sensitive to environment.</p>''', 5),
 qa('Name four rotary-motor types and three non-motor actuators from the slides.',
  '''<p>DC, AC, stepper and servo motors. Heaters, lights, and sirens or horns. (Solenoids are the linear electric example.)</p>''', 6),
])
# ====================================================================== topic 3
d_sp = svg(700, 190,
    '<text class="tb" x="170" y="22" text-anchor="middle">Series: 9 V battery, 500 uA</text>'
    + box(10, 40, 70, 44, ['9 V'], 'bxs') + box(110, 40, 80, 44, ['R1', '3 kOhm'], small_rest=True) + box(220, 40, 80, 44, ['R2', '10 kOhm'], small_rest=True) + box(330, 40, 80, 44, ['R3', '5 kOhm'], small_rest=True)
    + arr(80, 62, 110, 62, 'sp') + arr(190, 62, 220, 62, 'sp') + arr(300, 62, 330, 62, 'sp')
    + txt(150, 106, '1.5 V', 'ts') + txt(260, 106, '5.0 V', 'ts') + txt(370, 106, '2.5 V', 'ts') + txt(260, 124, 'drops add to 9 V', 'ts')
    + '<text class="tb" x="560" y="22" text-anchor="middle">Parallel: 9 V on each</text>'
    + box(440, 40, 70, 128, ['9 V'], 'bxs')
    + box(540, 34, 152, 36, ['10 kOhm: 0.9 mA'], bold=False) + box(540, 76, 152, 36, ['2 kOhm: 4.5 mA'], bold=False) + box(540, 118, 152, 36, ['1 kOhm: 9.0 mA'], bold=False)
    + arr(510, 52, 540, 52, 'sp') + arr(510, 94, 540, 94, 'sp') + arr(510, 136, 540, 136, 'sp')
    + txt(590, 180, 'total 14.4 mA (my sum)', 'ts'),
    'Redrawn: a series circuit with three resistors and their voltage drops, and a parallel circuit with three branches and their currents', 'sp')

d_up = svg(700, 130,
    box(10, 30, 110, 56, ['Button', 'open'], small_rest=True) + box(160, 30, 140, 56, ['INPUT_PULLUP', 'pin pulled to 5 V'], small_rest=True)
    + box(340, 30, 130, 56, ['reads HIGH', 'not pressed'], small_rest=True) + box(510, 30, 180, 56, ['pressed: pin to ground', 'reads LOW'], 'bxs', small_rest=True)
    + arr(120, 58, 160, 58, 'up') + arr(300, 58, 340, 58, 'up') + arr(470, 58, 510, 58, 'up', dash=True)
    + txt(350, 112, 'Pull-up logic from the slide: unpressed = HIGH, pressed = LOW', 'ts'),
    'Redrawn: with an internal pull-up the pin reads HIGH when the button is open and LOW when it is pressed', 'up')

SRC3 = '<p class="small src"><b>Source of this topic:</b> this year&rsquo;s Lecture 3 (IoT Circuit, 22 Oct 2026) and Lecture 4 (Embedded System, 28 Oct 2026), both by Mohd Nadhir Ab Wahab. Points marked &ldquo;older deck&rdquo; are from the Learning Materials Chapter 4 (Dr Chong).</p>'

w3_vis = f'''
  {SRC3}
  <h3>Part 1: the circuit that powers it</h3>
  <p class="small">Every electric circuit has three parts: a <b>source of energy</b>, a <b>closed path</b> and a <b>device that uses the energy</b>. If any part is open, the device does not work. <b>Current</b> is the flow of electrons, <b>voltage</b> is the driving force that pushes it, and <b>resistance</b> is anything that slows it. They link through <b>Ohm&rsquo;s law: V = I x R</b>, which rearranges to I = V / R and R = V / I.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Slide example</th><th>Working</th></tr></thead><tbody>
  <tr><td>Find current: 12 V across 3 ohm</td><td>I = V / R = 12 / 3 = <b>4 A</b></td></tr>
  <tr><td>Find resistance: 36 V, 4 A</td><td>R = V / I = 36 / 4 = <b>9 ohm</b></td></tr>
  <tr><td>Find voltage: 2 A through 7 ohm</td><td>V = I x R = 2 x 7 = <b>14 V</b></td></tr></tbody></table></div>
  {d_sp}
  <div class="tbl-wrap"><table><thead><tr><th></th><th>Series</th><th>Parallel</th></tr></thead><tbody>
  <tr><th>Layout</th><td>Components end to end in a line</td><td>All components across the same two nodes</td></tr>
  <tr><th>Current</th><td>Same through every component</td><td>Splits; total = sum of branch currents</td></tr>
  <tr><th>Voltage</th><td>Drops add up to the total</td><td>Same across every branch</td></tr>
  <tr><th>Total resistance</th><td>R1 + R2 + R3</td><td>1 / (1/R1 + 1/R2 + 1/R3), always less than the smallest branch</td></tr>
  <tr><th>Advantages (slide)</th><td>Does not heat easily, so little fire risk (the series slide repeats its advantage text in both columns)</td><td>Each branch gets the same voltage; add or remove a device without affecting the others; a fault in one branch leaves other paths working</td></tr>
  <tr><th>Disadvantages (slide)</th><td>A fault or break stops all appliances after it</td><td>Needs many wires; cannot give an exact same current to each element; cannot raise voltage because resistance drops</td></tr></tbody></table></div>
  <p class="small"><b>Series example (slide):</b> 3 + 10 + 5 = 18 kohm. The current is 500 microamp, so the drops are 500 uA x 3 k = 1.5 V, x 10 k = 5.0 V, x 5 k = 2.5 V; these add to 9 V (my check). <b>Parallel example (slide):</b> 1/R = 1/10k + 1/2k + 1/1k, so R = 625 ohm. With 9 V across each: 9/10k = 0.9 mA, 9/2k = 4.5 mA, 9/1k = 9.0 mA. <b>The slide&rsquo;s total-resistance formula is typed as 1/(R1 + R2 + R3), which is a typo;</b> the working above uses the correct form, and 625 ohm matches only that form.</p>
  <h4>Series-parallel worked example (slide: 24 V, R1 = 100, R2 = 250, R3 = 350, R4 = 200 ohm)</h4>
  <div class="tbl-wrap"><table><thead><tr><th>Step</th><th>Working</th></tr></thead><tbody>
  <tr><td>1. Parallel pairs</td><td>R1//R2 = 100 x 250 / 350 = 71.429 ohm; R3//R4 = 350 x 200 / 550 = 127.27 ohm (shortcut of two resistors: product over sum)</td></tr>
  <tr><td>2. Series total</td><td>71.429 + 127.27 = 198.70 ohm</td></tr>
  <tr><td>3. Total current</td><td>I = 24 / 198.70 = 120.78 mA</td></tr>
  <tr><td>4. Voltage drops</td><td>Across R1//R2: 120.78 mA x 71.429 = 8.6275 V; across R3//R4: 120.78 mA x 127.27 = 15.373 V</td></tr>
  <tr><td>5. Branch currents</td><td>I1 = 8.6275 / 100 = 86.275 mA; I2 = 8.6275 / 250 = 34.51 mA; I3 = 15.373 / 350 = 43.922 mA; I4 = 15.373 / 200 = 76.863 mA</td></tr></tbody></table></div>
  <p class="small">The slide reaches the same table (E, I, R rows). The shortcut in step 1 is my note, not slide text.</p>
  <p class="small"><b>Slide exercises and answers:</b> (a) 4 A through 1, 2, 3 ohm in series: drops 4, 8, 12 V and power 16, 32, 48 W (the slide gives these; P = V x I, my note on the formula). (b) 24 V across 1, 2, 3 ohm in parallel: currents 24, 12, 8 A and power 576, 288, 192 W. (c) 4 V across 1 k, 2.2 k, 6.8 k and 470 ohm in parallel: currents 4 mA, 1.82 mA, 588.2 uA, 8.51 mA; total 14.92 mA; total R 268.1 ohm. <b>No answer on the slides for:</b> the 24 V circuit with R1 = 5, R2 = 4, R3 = 12 (R2 and R3 in parallel) and R4 = 8 ohm, nor the 10-resistor equivalent-resistance puzzle. <b>My working for the first, from my reading of the figure:</b> R2//R3 = 4 x 12 / 16 = 3 ohm; R total = 5 + 3 + 8 = 16 ohm; I total = 24 / 16 = 1.5 A; V1 = 7.5 V; V across R2//R3 = 4.5 V (I2 = 1.125 A, I3 = 0.375 A); V4 = 12 V; 7.5 + 4.5 + 12 = 24 V.</p>

  <h3>Part 2: the brain, an embedded system</h3>
  <p class="small">An <b>embedded system</b> is hardware and software that together form a component of a larger machine. What is unique: it is designed for one specific task, runs on its own without human intervention, and must meet real-time performance limits. Examples on the slides: industrial robots, GPS receivers, cameras, DVD players, routers, set-top boxes, game consoles, photocopiers, microwave ovens, refrigerators and car systems.</p>
  <div class="two"><div><h4>Microprocessor</h4><p>Only a CPU, in one or a few chips. It has no RAM, ROM or peripherals of its own and depends on external circuits.</p></div>
  <div><h4>Microcontroller</h4><p>&ldquo;A computer on a chip&rdquo;: CPU, input/output, memory, clock, timer and other peripherals together, running a single program for dedicated tasks.</p></div></div>
  <p class="small">The slides show an Arduino Uno WiFi, a Raspberry Pi 4 and the <b>Maker Feather AIoT S3</b> board (an ESP32-S3 board; its pin map refers to the ESP32-S3 datasheets). Older deck: embedded hardware is the microcontroller or microprocessor plus memory (RAM, ROM, flash); software is firmware, middleware and application; interfaces are sensors in, actuators out, and communication interfaces such as UART, I2C and SPI. When choosing a board, check processor speed and power, memory, pins and connectivity, language and IDE support, and community support.</p>

  <h3>Programming it (Arduino, in C)</h3>
  <p class="small">A sketch has two main functions: <code>setup()</code> runs <b>once</b> after power-up or reset (set variables, pin modes, libraries) and <code>loop()</code> runs again and again to respond. Variables can be local (inside a function), formal parameters, or global (outside all functions, kept for the whole program). Pins are inputs by default; <code>pinMode(pin, mode)</code> sets INPUT, OUTPUT or INPUT_PULLUP.</p>
  {d_up}
  <pre class="code">int LED = 6;                 // LED on pin 6
void setup() {{ pinMode(LED, OUTPUT); }}
void loop() {{
  digitalWrite(LED, HIGH); delay(500);   // on for 500 ms
  digitalWrite(LED, LOW);  delay(500);   // off for 500 ms
}}</pre>
  <div class="tbl-wrap"><table><thead><tr><th>Function</th><th>What it does (slides)</th></tr></thead><tbody>
  <tr><th>digitalWrite(pin, HIGH/LOW)</th><td>Sets an OUTPUT pin to 5 V (3.3 V on 3.3 V boards) or 0 V. If you forget pinMode(OUTPUT), an LED may look dim because the internal pull-up is enabled.</td></tr>
  <tr><th>digitalRead(pin)</th><td>Reports whether a voltage is applied: on/off sensors.</td></tr>
  <tr><th>analogRead(pin)</th><td>Returns 0 to 1023 for 0 to 5 V. Example: 2.5 V on pin 0 gives 512 (about half of 1023).</td></tr>
  <tr><th>analogWrite(pin, 0-255)</th><td>Used for the DC motor speed example (type a speed 0 to 255).</td></tr>
  <tr><th>map(val, 0, 1023, 0, 180)</th><td>Scales a potentiometer reading to a servo angle for myservo.write().</td></tr>
  <tr><th>delay(), millis()</th><td>Wait, or time since start (time functions listed in the summary slide).</td></tr></tbody></table></div>
  <p class="small"><b>Sensor example (slide):</b> the DHT22 humidity and temperature sensor on pin 2, read every 2 seconds. Each reading takes about 250 ms. The code checks <code>isnan()</code> on the readings and prints &ldquo;Failed to read from DHT sensor!&rdquo; if any failed, then prints humidity, temperature (C and F) and the heat index. <b>Small typos on the slides (my note):</b> the analog example writes <code>serial.begin</code> where Arduino expects <code>Serial.begin</code>, and the setup example is written <code>Void</code> with a capital V.</p>
'''
w3_terms = terms([
 ('Ohm&rsquo;s law', 'V = I x R: voltage equals current times resistance.'),
 ('Series circuit', 'Components end to end; same current, resistances and voltage drops add.'),
 ('Parallel circuit', 'Components across the same nodes; same voltage, branch currents add.'),
 ('Voltage drop', 'The part of the supply voltage used across one component (V = I x R for that component).'),
 ('Microcontroller', 'A computer on one chip: CPU, memory, clock, timer and input/output.'),
 ('Microprocessor', 'A CPU alone; needs external memory and peripherals.'),
 ('Firmware', 'Low-level software tightly tied to the hardware (older deck).'),
 ('setup() / loop()', 'Arduino functions: run once at start / repeat forever.'),
 ('INPUT_PULLUP', 'Enables the pin&rsquo;s internal pull-up resistor so an open button reads HIGH and a pressed one reads LOW.'),
 ('analogRead', 'Reads a voltage as a number 0 to 1023 for 0 to 5 V.'),
 ('UART / I2C / SPI', 'Communication interfaces between the embedded system and other devices (older deck; the slides only name them).'),
])
w3_boss = ''.join([
 qa('State Ohm&rsquo;s law and solve: a battery pushes current through 3 ohm and 12 V is applied. Then find the voltage for 2 A through 7 ohm.',
  '''<p>V = I x R. First: I = V / R = 12 / 3 = 4 A. Second: V = 2 x 7 = 14 V.</p>''', 1),
 qa('Three resistors 3 k, 10 k and 5 k are in series across a battery that drives 500 microamp. Find total resistance, battery voltage and each drop.',
  '''<p>Total R = 3 + 10 + 5 = 18 kohm. Drops: 500 uA x 3 k = 1.5 V; x 10 k = 5.0 V; x 5 k = 2.5 V. Battery voltage = sum = 9 V (equally 500 uA x 18 k = 9 V, my check).</p>''', 2),
 qa('Three resistors 10 k, 2 k and 1 k are in parallel across 9 V. Find total resistance and each branch current.',
  '''<p>1/R = 1/10k + 1/2k + 1/1k = 0.1 + 0.5 + 1.0 = 1.6 mS, so R = 625 ohm. Currents: 9/10k = 0.9 mA, 9/2k = 4.5 mA, 9/1k = 9.0 mA; total 14.4 mA (my sum; 9 V / 625 ohm = 14.4 mA agrees).</p>''', 3),
 qa('Series versus parallel: give one advantage and one disadvantage of each.',
  '''<p>Series: advantage, it does not heat easily; disadvantage, one break stops everything after it. Parallel: advantage, same voltage for each branch and a fault in one branch leaves the rest working; disadvantage, it needs many wires.</p>''', 4),
 qa('Differentiate a microprocessor from a microcontroller, and name three unique features of an embedded system.',
  '''<p>A microprocessor is a CPU only and relies on external memory and peripherals. A microcontroller puts CPU, memory, input/output, clock and timer on one chip and runs dedicated tasks. Embedded systems are built for one task, run without human intervention, and have real-time constraints.</p>''', 5),
 qa('A button wired with INPUT_PULLUP reads HIGH. Is it pressed? Why? And what does analogRead return for 2.5 V?',
  '''<p>No, it is not pressed. The internal pull-up ties the pin to 5 V, so an open button reads HIGH; pressing the button connects the pin to ground and it reads LOW. analogRead gives 0 to 1023 for 0 to 5 V, so 2.5 V gives about 512 (the slide&rsquo;s figure).</p>''', 6),
])

# ====================================================================== topic 4
d_osi = svg(700, 256,
    '<text class="tb" x="120" y="18" text-anchor="middle">TCP/IP model</text><text class="tb" x="580" y="18" text-anchor="middle">OSI model</text>'
    + box(10, 30, 220, 42, ['Application']) + box(10, 80, 220, 42, ['Host-to-host (transport)']) + box(10, 130, 220, 42, ['Internet']) + box(10, 180, 220, 42, ['Network access'])
    + ''.join(box(470, 30 + 28 * i, 220, 26, [t], bold=False) for i, t in enumerate(['Application', 'Presentation', 'Session', 'Transport', 'Network', 'Data link', 'Physical']))
    + arr(230, 51, 470, 71, 'os', both=True, dash=True) + arr(230, 101, 470, 127, 'os', both=True, dash=True)
    + arr(230, 151, 470, 155, 'os', both=True, dash=True) + arr(230, 201, 470, 197, 'os', both=True, dash=True)
    + txt(350, 248, 'Matches drawn by me from the slide figure', 'ts'),
    'Redrawn: the TCP/IP four-layer model beside the seven-layer OSI model, with matching layers', 'os')

d_mq = svg(700, 160,
    box(10, 20, 130, 50, ['Publisher', 'temperature sensor'], small_rest=True) + box(10, 90, 130, 50, ['Publisher', 'pacemaker monitor'], small_rest=True)
    + box(270, 50, 150, 60, ['Broker', 'topics, pushes'], 'bxs', small_rest=True)
    + box(550, 20, 140, 50, ['Subscriber', 'analytics app'], small_rest=True) + box(550, 90, 140, 50, ['Subscriber', 'dashboard'], small_rest=True)
    + arr(140, 45, 270, 70, 'mq') + arr(140, 115, 270, 92, 'mq') + arr(420, 70, 550, 45, 'mq') + arr(420, 92, 550, 115, 'mq')
    + txt(205, 40, 'publish to topic', 'ts') + txt(470, 40, 'push to subscribers', 'ts')
    + txt(350, 154, 'Publishers do not need to know the subscribers (slide)', 'ts'),
    'Redrawn: MQTT publishers send messages to topics on a broker, and the broker pushes them to subscribers', 'mq')

SRC4 = '<p class="small src"><b>Source of this topic:</b> this year&rsquo;s Lecture 5 (IoT Networks, dated 19 Nov 2025, Mohd Nadhir Ab Wahab) and the older Learning Materials deck &ldquo;IoT Protocols&rdquo; (Dec 2024) for the internet, transport and application protocols.</p>'

w4_vis = f'''
  {SRC4}
  <h3>Part 1: connecting things to a network</h3>
  <p class="small">A <b>Personal Area Network (PAN)</b> spans a few metres around a person and is common in IoT. A <b>Local Area Network (LAN)</b> covers a small area, is normally high speed and under one administrator. A <b>Wide Area Network (WAN)</b> covers a wide area and may be lower speed with parts from different Internet service providers (ISPs). An <b>end device</b> is the source or destination of a message; <b>intermediary devices</b> connect end devices and join networks; <b>addresses</b> identify devices; <b>media</b> carry the message. <b>Ethernet</b> rules cover communication between local devices; <b>IP</b> covers remote devices; <b>routers</b> direct packets across several networks (routing).</p>
  <p class="small">IoT devices are often embedded devices working in poor conditions, so they use light protocols (CoAP and MQTT, below). The slides also say IoT traffic carries traceable signatures and confidential data, so devices need a secure framework: authentication, authorization, network-enforced policy and secure analytics.</p>
  {d_osi}
  <p class="small">The slides explain that OSI is complex while TCP/IP is widely used, so TCP/IP is the mainstream reference model.</p>

  <h3>Part 2: wireless technologies</h3>
  <p class="small">A wireless device sends signals as electromagnetic waves: the transmitter encodes and the receiver decodes. <b>Modulation</b> turns digital bits into an analog signal by changing a carrier&rsquo;s frequency, amplitude or phase. There are many technologies because of trade-offs: short or long distance, high or low power, high or low speed, few or many devices, device-to-device or device-to-infrastructure, indoor or outdoor.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Technology</th><th>Key facts from the slides</th></tr></thead><tbody>
  <tr><th>RFID</th><td>Tags on objects; readers (interrogators) send a signal and read the response. Passive, active or battery-assisted passive. Range 10 cm to 200 m. Road tolls, building access, inventory.</td></tr>
  <tr><th>NFC</th><td>13.56 MHz, based on RFID. Read/write mode and peer-to-peer mode. Smart home, contactless payment, asset tracking; passive tags store information.</td></tr>
  <tr><th>Bluetooth / BLE</th><td>Short-distance PAN, 2.4 GHz ISM band. Fast connection (milliseconds), 1 Mbps. BLE sleeps until reconnection, so batteries last years. Beacons give location services.</td></tr>
  <tr><th>ZigBee</th><td>IEEE 802.15.4 for layers 1 and 2 plus the ZigBee stack. CSMA with collision avoidance. Low power, low cost, low throughput, up to about 65k nodes, little or no quality-of-service guarantee.</td></tr>
  <tr><th>6LoWPAN</th><td>Small packets, 16-bit short or 64-bit extended addresses, 250/40/20 kbps, star and mesh, low power and cost, inherently unreliable links.</td></tr>
  <tr><th>Wi-Fi</th><td>WLAN based on IEEE 802.11; 2.4, 3.6 and 4.9/5.0 GHz bands; range up to 100 m; tablets, laptops, phones.</td></tr>
  <tr><th>LPWAN</th><td>Low power (months to years), long range (several km), low data rate, deep penetration, wide coverage, sub-GHz bands, public or private deployment.</td></tr>
  <tr><th>LoRaWAN</th><td>Wide-area link for power-limited devices; extended star topology (gateways relay between end devices and a central network server); 0.3 to 50 kbps; multi-layer encryption with unique keys for application, network and device.</td></tr>
  <tr><th>Sigfox</th><td>Network provider; ultra narrow band; 140 messages per day per device; 12-byte uplink and 8-byte downlink payload; roaming.</td></tr></tbody></table></div>
  <p class="small"><b>My reading of the slide figure</b> (bandwidth against range): RFID/NFC and BLE sit at short range and low bandwidth, ZigBee and 802.15.x at short-to-medium range, Wi-Fi variants at higher bandwidth and short-to-medium range, 2G to 5G at medium-to-long range with 5G the highest bandwidth, and LPWAN at long range with low bandwidth. A last slide compares operator strengths (reliability, global coverage, roaming, licensed spectrum, security) with IoT strengths (fast time to market, diversity, developer community) and what each gains when combined (deep coverage, low device cost, long battery life).</p>

  <h3>Part 3: the protocols on top (older deck)</h3>
  <div class="two"><div><h4>Internet layer</h4><p><b>IPv6</b> uses 128-bit addresses (2 to the power 128, about 3.4 x 10 to the power 38) against IPv4&rsquo;s 32-bit (about 4.3 billion). They are not interoperable. IANA hands blocks to five regional registries, which give blocks to ISPs, which assign addresses to customers.</p></div>
  <div><h4>Transport layer</h4><p><b>TCP</b>: connection-oriented, highly reliable, time is less critical. <b>UDP</b>: connectionless, best effort, fast and efficient.</p></div></div>
  <div class="cards3">
    <div class="c"><h4>REST (RESTful HTTP)</h4><p>The architecture style of the web: every resource has an ID (a URL, for example a sensor&rsquo;s temperature), resources are linked by standard methods, communication is stateless (state is kept on the client).</p></div>
    <div class="c"><h4>CoAP</h4><p>RESTful services for networked embedded devices. 4-byte header, multicast support, fits a single UDP packet or 802.15.4 frame. Methods GET, POST, PUT, DELETE like HTTP; resources by URI. Caching with the Max-Age option; proxies can cache.</p></div>
    <div class="c"><h4>Why not plain HTTP/TCP?</h4><p>Constrained networks have very low power (must sleep), tiny computing resources, a need to save bandwidth, about 100 kbit/s, high loss and variable links, so TCP and HTTP are not suitable.</p></div>
  </div>
  <p class="small"><b>The next gap (slide):</b> HTTP and CoAP struggle across firewalls (which block incoming connections and hide networks behind one address) and are not event-oriented. IoT needs one-to-many emitting, listening for events, tiny packets in huge volumes, and pushing over unreliable networks. That is the case for MQTT.</p>
  {d_mq}
  <h4>MQTT in the slides</h4>
  <div class="tbl-wrap"><table><thead><tr><th>Feature</th><th>Detail</th></tr></thead><tbody>
  <tr><th>Model</th><td>Publish/subscribe through a <b>broker</b>; open source and royalty-free; 2-byte minimum overhead; distributes one-to-none, one-to-one or one-to-many.</td></tr>
  <tr><th>Topics</th><td>Hierarchical with /, for example sensors/COMPUTER1/temperature/HDD1. <b>+</b> matches one level, <b>#</b> matches all remaining levels (sensors/+/temperature/+ and sensors/COMPUTER1/#).</td></tr>
  <tr><th>Retained message</th><td>The server keeps a message and sends it to new subscribers.</td></tr>
  <tr><th>Clean session</th><td>If true, subscriptions are removed at the end of the session; if false, they stay (durable).</td></tr>
  <tr><th>Last will and testament</th><td>A message the server publishes if the client drops unexpectedly, used as an alarm.</td></tr>
  <tr><th>QoS 0</th><td>At most once, no acknowledgement, can be lost (&ldquo;fire and forget&rdquo;).</td></tr>
  <tr><th>QoS 1</th><td>At least once; stored at the sender until PUBACK; may arrive more than once.</td></tr>
  <tr><th>QoS 2</th><td>Exactly once; sender keeps the message until PUBREC; receiver holds the packet ID until it sends PUBCOMP.</td></tr>
  <tr><th>Security</th><td>Native login is weak (plain-text username and password); use SSL/TLS (adds overhead), client certificates or pre-shared keys, or encrypt the content.</td></tr></tbody></table></div>
  <div class="tbl-wrap"><table><thead><tr><th></th><th>MQTT</th><th>HTTP</th></tr></thead><tbody>
  <tr><th>Orientation</th><td>Data centric</td><td>Document centric</td></tr>
  <tr><th>Pattern</th><td>Publish/subscribe</td><td>Request/response</td></tr>
  <tr><th>Complexity, size</th><td>Simple; small, compact binary header of 2 bytes</td><td>Complex; large text-based messages</td></tr>
  <tr><th>Service level</th><td>Three quality-of-service settings</td><td>Same level for all</td></tr>
  <tr><th>Distribution</th><td>1 to 0, 1 to 1, 1 to n</td><td>1 to 1 only</td></tr></tbody></table></div>
  <p class="small"><b>Application (slide):</b> monitoring many patients with pacemakers at home: an MQTT client in the home appliance sends diagnostics to the broker; the analytics application subscribed to the topic looks for abnormalities and notifies the clinician.</p>
'''
w4_terms = terms([
 ('PAN / LAN / WAN', 'Personal (metres), local (small area, one owner) and wide (large area, several ISPs) networks.'),
 ('Routing', 'Directing a packet to its destination across several networks; routers do it.'),
 ('Modulation', 'Encoding digital bits as changes in a carrier&rsquo;s frequency, amplitude or phase.'),
 ('RFID / NFC', 'Tag-and-reader identification; NFC is short range at 13.56 MHz.'),
 ('BLE', 'Bluetooth Low Energy: sleeps between connections for years of battery life.'),
 ('LPWAN', 'Low-power wide-area networks: long range, low rate, low power. LoRaWAN and Sigfox are examples.'),
 ('IPv6', '128-bit addresses; about 3.4 x 10^38 of them.'),
 ('TCP / UDP', 'Reliable connection-oriented transport / fast best-effort connectionless transport.'),
 ('REST', 'Web architecture style: resources with IDs, stateless communication.'),
 ('CoAP', 'Constrained Application Protocol: 4-byte header, UDP, REST-like.'),
 ('MQTT broker', 'Intermediary that receives published messages and pushes them to topic subscribers.'),
 ('QoS 0 / 1 / 2', 'At most once / at least once / exactly once delivery.'),
 ('Last will', 'A message published automatically if a client disconnects abnormally.'),
])
w4_boss = ''.join([
 qa('Distinguish PAN, LAN and WAN, and say which protocols handle local and remote communication.',
  '''<p>PAN: a few metres around a person (common in IoT). LAN: small area, high speed, one administrator. WAN: wide area, often lower speed, parts from several ISPs. Ethernet rules cover local devices; IP covers remote devices.</p>''', 1),
 qa('Why are there so many wireless technologies? Give three trade-offs and place BLE and LoRaWAN on them.',
  '''<p>Because of trade-offs: distance (short versus long), power (low versus high), speed (low versus high), number of devices, indoor versus outdoor. BLE: short range, low power, years of battery, up to 1 Mbps. LoRaWAN: long range, low power, low data rate of 0.3 to 50 kbps.</p>''', 2),
 qa('Compare TCP and UDP and explain which suits IoT.',
  '''<p>TCP is connection-oriented and highly reliable but heavy. UDP is connectionless, fast and best effort. Constrained IoT networks have low power, little computing, high loss and low bandwidth, so the slides call TCP and HTTP unsuitable and the IoT stack uses UDP.</p>''', 3),
 qa('What is CoAP, and how does it relate to HTTP?',
  '''<p>A RESTful protocol for constrained devices: 4-byte header, multicast support, one message fits a single UDP packet or 802.15.4 frame. It uses the same style of methods (GET, POST, PUT, DELETE) and a subset of HTTP response codes, so it translates easily to HTTP. Responses can be cached using Max-Age.</p>''', 4),
 qa('Explain MQTT publish/subscribe, the wildcards, and the three QoS levels. What does a subscription to sensors/+/temperature/+ receive?',
  '''<p>Publishers send messages to topics on a broker, which pushes them to subscribers; publishers do not need to know the consumers. + matches one level; # matches all remaining levels. QoS 0: at most once; QoS 1: at least once (PUBACK, possible duplicates); QoS 2: exactly once (PUBREC, PUBCOMP). The subscription receives the temperature of every device and sub-item under sensors, for example all computers and all disks.</p>''', 5),
 qa('Give four differences between MQTT and HTTP.',
  '''<p>MQTT is data centric, publish/subscribe, simple with a 2-byte header, has three QoS levels and supports 1-to-many. HTTP is document centric, request/response, complex and text-heavy, has one service level and is 1-to-1 only.</p>''', 6),
])
# ====================================================================== topic 5
d_ctl = svg(700, 140,
    box(20, 24, 170, 56, ['IaaS', 'infrastructure'], small_rest=True) + box(265, 24, 170, 56, ['PaaS', 'platform'], small_rest=True)
    + box(510, 24, 170, 56, ['SaaS', 'software'], 'bxs', small_rest=True)
    + arr(190, 52, 265, 52, 'ct') + arr(435, 52, 510, 52, 'ct')
    + txt(105, 104, 'More control over', 'ts') + txt(105, 120, 'IT resources', 'ts') + txt(595, 104, 'Less control over', 'ts') + txt(595, 120, 'IT resources', 'ts'),
    'Redrawn: the cloud service models IaaS, PaaS and SaaS, from more control over IT resources to less', 'ct')

d_cia = svg(700, 120,
    box(10, 28, 200, 56, ['Confidentiality', 'no unauthorised disclosure'], small_rest=True) + box(250, 28, 200, 56, ['Integrity', 'accurate, unaltered'], small_rest=True)
    + box(490, 28, 200, 56, ['Availability', 'working when needed'], small_rest=True)
    + txt(350, 108, 'The three key aspects of security on the slide', 'ts'),
    'Redrawn: the three key aspects of IoT security, confidentiality, integrity and availability', 'ci')

SRC5 = '<p class="small src"><b>Source of this topic:</b> three older Learning Materials decks by Mohd Nadhir Ab Wahab: Cloud Technology (Jan 2025), Data Analytics for IoT and Smart Applications (Jan 2025) and Security, Trust, and Privacy (Jan 2025). This year&rsquo;s folder does not have them yet, so check they still match your lectures.</p>'

w5_vis = f'''
  {SRC5}
  <h3>Part 1: cloud computing</h3>
  <p class="small"><b>Cloud computing</b> is the on-demand delivery of compute power, databases, storage, applications and other IT resources over the internet with pay-as-you-go pricing. The five <b>NIST characteristics</b> (slide figure): on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service. Building blocks on the slides: servers and virtualisation, networking, storage, data centres, middleware, runtime environments, virtualisation software, management and monitoring tools, APIs, security, user interfaces, billing and metering.</p>
  {d_ctl}
  <p class="small">The slide labels the three service models IaaS (infrastructure as a service), PaaS (platform) and SaaS (software), with more control on the left and less on the right. A stack figure shows which layers you manage and which the provider manages; the layer-by-layer shading is too small to read reliably, so I only note that the provider manages more as you move toward SaaS (my reading).</p>
  <div class="tbl-wrap"><table><thead><tr><th>Deployment</th><th>Points on the slide</th></tr></thead><tbody>
  <tr><th>Public cloud</th><td>Cost-efficient pay-as-you-go, easily scalable, global reach.</td></tr>
  <tr><th>Private cloud</th><td>Data security and compliance (healthcare, finance), tailored control, dedicated resources for performance.</td></tr>
  <tr><th>Hybrid cloud</th><td>Balances the two: critical data stays on-premises, less sensitive work uses the public cloud, costs optimised.</td></tr></tbody></table></div>
  <p class="small"><b>Six advantages (slides):</b> trade capital expense for variable expense (instead of investing in data centres on a forecast, pay only for what you consume); massive economies of scale (the slide names AWS, passing savings on); stop guessing capacity; increase speed and agility; stop spending money running and maintaining data centres; go global in minutes. Cloud IoT platforms shown: ThingWorx, V-ONE, SAP, ThingSpeak, favoriot, AWS, Salesforce, Microsoft Azure, Google Cloud. A smart-home case study asks how the cloud handles large real-time data, how to cut delay for remote control, and which security measures to use; <b>the slide gives no answers.</b></p>

  <h3>Part 2: data from IoT</h3>
  <p class="small"><b>Structured data</b> sits in fixed fields in a file or record; <b>unstructured data</b> is raw. Storage can be local, centralised or distributed. IoT data is a massive volume of mixed, streaming, geographically spread data with high speed (<b>velocity</b>), doubtful accuracy (<b>veracity</b>: sleeping nodes, flat batteries, limited sensors) and uneven flow (<b>variability</b>). The slides stress <b>garbage in, garbage out</b>: bad input gives bad decisions, accurate data gives actionable insight. The reasons to analyse: decision making, operational efficiency, real-time monitoring, user experience, scalability, cost reduction, innovation.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Data problem</th><th>Quality fix and techniques (slides)</th></tr></thead><tbody>
  <tr><th>Noise and error</th><td><b>Noise reduction:</b> filtering, smoothing, quality-aware sampling.</td></tr>
  <tr><th>Abnormal points</th><td><b>Anomaly detection and cleansing:</b> model &ldquo;normal&rdquo;, flag what does not fit; statistical methods, machine learning (isolation forests, clustering), rule-based.</td></tr>
  <tr><th>Missing values</th><td><b>Missing value prediction:</b> imputation (mean, median, mode), machine learning models, time-series interpolation.</td></tr>
  <tr><th>Duplicate and inconsistent data</th><td><b>Data fusion:</b> combine sources to filter interference (sensor fusion, model-based fusion, information fusion).</td></tr></tbody></table></div>
  <div class="tbl-wrap"><table><thead><tr><th></th><th>Relational (RDBMS)</th><th>NoSQL (&ldquo;not only SQL&rdquo;)</th></tr></thead><tbody>
  <tr><th>Data</th><td>Structured, uniform; tables and columns; predefined schema</td><td>Key-value and document stores; no fixed schema; denormalised data avoids joins</td></tr>
  <tr><th>Query</th><td>SQL (select, insert, update, delete)</td><td>Does not use SQL as its query language</td></tr>
  <tr><th>Scaling</th><td>Scale up (more hardware power)</td><td>Scale out (spread the load by partitioning and replication)</td></tr>
  <tr><th>Transactions</th><td><b>ACID:</b> atomic, consistent, isolated, durable</td><td><b>BASE:</b> basically available, soft state, eventually consistent</td></tr></tbody></table></div>
  <p class="small">The slide says IoT data gathering is <b>not uniform</b>, which is the argument for NoSQL (my link: this is why a flexible schema suits sensors). Popular analytics tools shown: Apache Spark, TensorFlow, Power BI, Kibana, Tableau, SAP. Case studies: predictive maintenance on factory machines (less unplanned downtime) and smart-city traffic signals (less congestion). Challenges and answers: <b>volume</b> (distributed computing, cloud, <b>edge computing</b> near the source), <b>variety</b>, <b>real-time processing</b>, <b>interoperability</b>; plus security (encryption in transit and at rest, access control, audits) and privacy (anonymise and aggregate, follow regulations, be transparent).</p>

  <h3>Part 3: security, trust and privacy</h3>
  {d_cia}
  <div class="cards3">
    <div class="c"><h4>Security</h4><p>Measures that protect connected devices, networks and data from unauthorised access, attacks and disruption. Challenges: many devices, secure transmission, limited processing power and memory, firmware flaws, no uniform standards.</p></div>
    <div class="c"><h4>Trust</h4><p>User reliance on the security, reliability and ethical behaviour of devices and the whole ecosystem: device, data and ecosystem trust. Built by secure protocols (MQTT with TLS, CoAP with DTLS), end-to-end encryption and integrity checks (digital signatures, hash functions).</p></div>
    <div class="c"><h4>Privacy</h4><p>Control over how personal data is collected, processed and shared. Key aspects: data minimisation (collect only what is needed), user consent, transparency. Concerns: profiling, weak consent, breaches, location tracking, cross-device tracking, third-party sharing, retention.</p></div>
  </div>
  <div class="tbl-wrap"><table><thead><tr><th>Control</th><th>What it does (slides)</th></tr></thead><tbody>
  <tr><th>Authentication</th><td>Verify identity before access: passwords, biometrics, digital certificates, multi-factor.</td></tr>
  <tr><th>Authorization</th><td>Give permissions to authenticated entities: role-based access control (RBAC) and the least privilege principle.</td></tr>
  <tr><th>Encryption</th><td>Code data so only a key holder can read it: end-to-end encryption and TLS.</td></tr>
  <tr><th>Data integrity</th><td>Detect tampering: hash functions and checksums.</td></tr></tbody></table></div>
  <p class="small"><b>Real cases on the slides:</b> <b>Mirai</b> botnet scans for IoT devices and logs in if the default username and password were never changed. <b>Verkada</b>: attackers used admin credentials found online to reach feeds from over 150,000 cameras. <b>Ring</b>: weak, recycled and default credentials exposed live feeds. <b>SILEX</b> malware deleted device firmware. <b>ChargePoint</b> EV charger flaws let attackers set the maximum charging current, which could disable the home electrical system. <b>Pattern across the cases (my note):</b> most began with default or weak credentials, which links straight to the authentication row above. Fixes for privacy: design it in from the start, inform users, give control over shared data, minimum collection, update and patch, work with legal experts.</p>
'''
w5_terms = terms([
 ('Cloud computing', 'On-demand delivery of IT resources over the internet with pay-as-you-go pricing.'),
 ('IaaS / PaaS / SaaS', 'Infrastructure, platform and software as a service; control over IT resources falls from left to right.'),
 ('Public / private / hybrid cloud', 'Shared pay-as-you-go cloud / dedicated cloud for strict data rules / a mix of both.'),
 ('Structured data', 'Data in fixed fields in a file or record.'),
 ('Velocity, veracity, variability', 'Speed of data, how accurate it is, and how unevenly it flows.'),
 ('GIGO', 'Garbage in, garbage out: poor input data gives poor decisions.'),
 ('Data fusion', 'Combining several data sources to filter interference.'),
 ('Edge computing', 'Processing data closer to the source (named as a fix for scale).'),
 ('ACID / BASE', 'Relational transaction rules / NoSQL transaction rules (eventual consistency).'),
 ('Scale up / scale out', 'Add power to one machine / spread the load over many.'),
 ('Confidentiality, integrity, availability', 'Keep data private, correct, and reachable.'),
 ('RBAC / least privilege', 'Role-based access control / give only the permissions a function needs.'),
 ('TLS / DTLS', 'Transport security for MQTT / for CoAP (the slide pairs them).'),
 ('Data minimisation', 'Collect only the data needed for the purpose.'),
])
w5_boss = ''.join([
 qa('Define cloud computing and list the five NIST characteristics.',
  '''<p>On-demand delivery of compute, storage, databases, applications and other IT resources via the internet, with pay-as-you-go pricing. NIST characteristics: on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service.</p>''', 1),
 qa('Compare public, private and hybrid clouds and choose one for a hospital asset tracker with patient-related data. (The choice is my reasoning.)',
  '''<p>Public: cheap, scalable, global. Private: tight security and compliance, dedicated performance. Hybrid: sensitive data stays on-premises while less sensitive work uses the public cloud. <b>My reasoning:</b> hybrid or private, because the slides link private cloud to regulated sectors such as healthcare; the slides do not decide this case.</p>''', 2),
 qa('Give four of the six advantages of cloud computing on the slides.',
  '''<p>Trade capital expense for variable expense; massive economies of scale; stop guessing capacity; increase speed and agility; stop spending money on running data centres; go global in minutes.</p>''', 3),
 qa('Why does garbage in mean garbage out matter for IoT, and what four data quality techniques fix it?',
  '''<p>IoT data can be noisy, missing or unreliable (sleeping nodes, flat batteries, limited sensors), and computers process bad input without question, leading to bad decisions. Fixes: noise reduction (filtering, smoothing, quality-aware sampling), anomaly detection and cleansing, missing value prediction (imputation, interpolation) and data fusion.</p>''', 4),
 qa('Compare relational and NoSQL databases on schema, scaling and transactions. Which fits IoT?',
  '''<p>Relational: predefined schema, scale up, ACID transactions. NoSQL: no fixed schema, scale out by partitioning and replication, BASE transactions (eventual consistency). The slides stress that IoT data is not uniform, which suits NoSQL (my link; the slide shows the contrast rather than a verdict).</p>''', 5),
 qa('Define the three key aspects of IoT security and give one real case that broke the first of them.',
  '''<p>Confidentiality: no disclosure to unauthorised parties. Integrity: data and device operations stay accurate. Availability: systems are working when needed. A confidentiality case: Verkada, where attackers used admin credentials found online to reach private feeds from over 150,000 cameras.</p>''', 6),
 qa('What stopped Mirai-style attacks being easy, according to the slides, and what controls match?',
  '''<p>Mirai logs in with the default username and password, so changing defaults and using strong authentication (strong passwords, certificates, multi-factor) with authorization (RBAC, least privilege) blocks it. Regular updating of firmware and access policies also helps (best-practice lists on the slides).</p>''', 7),
])

# ====================================================================== project section
w_pj = f'''
<section id="project" class="band wx">
  <h2 class="sec">Project and assignment</h2>
  <p class="small">From the project brief (<b>CPC357-Project.pdf</b>) in your folder. The project: build a working IoT system for a real urban problem that supports <b>UN SDG 11, Sustainable Cities and Communities</b> (smart cities), and hand in one technical report per group. <b>Due 3 January 2027, 11.59 pm Malaysia time; late work is not accepted.</b></p>
  <div class="tbl-wrap"><table><thead><tr><th>Requirement</th><th>Detail from the brief</th></tr></thead><tbody>
  <tr><th>Objectives</th><td>Design and build a functional smart city IoT system; show you understand IoT architecture; apply cloud computing and data analytics; visualise sensor data in a web or mobile app.</td></tr>
  <tr><th>Hardware</th><td>Any suitable platform, for example Raspberry Pi, Maker Feather S3, or another microcontroller with sensors. <b>Justify the sensor choice</b> for your application.</td></tr>
  <tr><th>Cloud</th><td>Any platform, for example AWS or GCP.</td></tr>
  <tr><th>Visualisation</th><td>A web or mobile app showing real-time or historical data. The core requirement is working hardware-to-cloud integration: collect, process, visualise.</td></tr></tbody></table></div>
  <h3>The report must contain</h3>
  <div class="cards3">
    <div class="c"><h4>1. System architecture</h4><p>Detailed architecture diagram; each component and how they interact.</p></div>
    <div class="c"><h4>2. Hardware documentation</h4><p>List of sensors and parts, why you chose them, and a setup and configuration guide.</p></div>
    <div class="c"><h4>3. SDG 11 impact analysis</h4><p>How the system tackles smart city challenges, and the possible real-world impact.</p></div>
    <div class="c"><h4>4. Repository link</h4><p>GitHub or GitLab with all source code, a full README (description, setup and install steps, dependencies).</p></div>
    <div class="c"><h4>5. Video link</h4><p>YouTube (public or unlisted): system overview and architecture, a live demonstration, and the data visualisation.</p></div>
  </div>
  <div class="tbl-wrap"><table><thead><tr><th>Rubric</th><th>Weight</th><th>What earns the top band (70 to 100%)</th></tr></thead><tbody>
  <tr><th>IoT system design, plan and implementation</th><td>35%</td><td>Clear architecture, well-justified sensors, seamless hardware-cloud integration, effective data visualisation.</td></tr>
  <tr><th>Technical documentation</th><td>35%</td><td>Clear diagrams, detailed hardware documentation, organised code, complete README, accessible repository, working links.</td></tr>
  <tr><th>SDG 11 impact and innovation</th><td>10%</td><td>Highly innovative, clear alignment with SDG 11 goals, real-world applicability.</td></tr>
  <tr><th>Presentation (video)</th><td>20%</td><td>Clear, professional, covers overview, live prototype, visualisation and SDG 11 impact within the time limit.</td></tr></tbody></table></div>
  <p class="small"><b>Rules that cost marks:</b> the repository and video links must be inside the PDF report (links sent by email are not accepted); broken or inaccessible links lose marks; check them before submitting. The work must be your own: no copying internet projects or another student&rsquo;s work; plagiarism can mean an F for the report or the whole coursework. <b>The brief does not state the video time limit,</b> only that the rubric measures work &ldquo;within time limit&rdquo;; ask your lecturer.</p>
  <h3>Assignment 1 (review of IoT applications)</h3>
  <p class="small">The brief in your folder (<b>CPC357 - Assignment 1_v1.pdf</b>) asks a group of 2 to review <b>four recent-trend IoT applications</b> in a report of at most <b>15 pages</b> excluding references (Times New Roman 12, single spacing), with a cover page, figures, comparison tables, recent references, and layman&rsquo;s wording. It counts for <b>10%</b> of the course grade, graded A to F; the rubric is Style and format 10%, Contents 60% (must pass the Turnitin plagiarism filter), Language 10%, Structure 10%, Completeness and accuracy 10%. <b>Check the date:</b> this file is headed Semester 1, 2023/2024 and gives a due date of 1 December 2022, so confirm this year&rsquo;s deadline on eLearn.</p>
  <p class="small"><b>My own links, not from the brief:</b> sensors and actuators (Topic 2) and boards (Topic 3) feed the hardware documentation; the network and protocol choice (Topic 4, for example MQTT) feeds the architecture diagram; cloud, database and visualisation choices (Topic 5) feed the integration; security and privacy (Topic 5) feed the SDG 11 impact discussion.</p>
</section>
'''

# ====================================================================== story, cheat sheet, flashcards
story = [
 (1, 'What is an IoT system?', 'Ordinary objects can sense but cannot share, so nothing is automated or learned from them.',
  'Add sensors, software and connectivity: sensor, link, processing, interface, with a gateway and the cloud behind it.',
  'The system is only as good as what it senses and does. How do sensors and actuators work?'),
 (2, 'Sensors and actuators', 'The world is physical, but computers only understand electrical signals.',
  'Sensors turn a measurand into a usable signal; actuators turn the controller&rsquo;s signal into action.',
  'Both need power and a brain. What circuit and computer sit in the middle?'),
 (3, 'Circuit and embedded system', 'Sensors and actuators need a powered, closed circuit and something to decide.',
  'Ohm&rsquo;s law and series/parallel circuits for power; a microcontroller running Arduino code for decisions.',
  'One working device is alone. How does it talk to others?'),
 (4, 'Networks and protocols', 'Devices are small, battery-powered and sit on poor links, but must reach distant systems.',
  'Pick the right wireless technology, then light protocols on UDP: CoAP and MQTT.',
  'Data now arrives in huge, messy volumes. Where does it go and how is it protected?'),
 (5, 'Cloud, data and security', 'Piles of unreliable data, and a connected world open to attack.',
  'Cloud storage and platforms, data quality and databases, and security, trust and privacy controls.',
  'This is the end of the material in the folder; the project puts the whole chain together.'),
]
story_html = '<ol class="story">' + ''.join(
    f'<li class="w{n}"><a href="#week-{n}"><span class="wk">Topic {n}</span><h3>{t}</h3>'
    f'<p><b>Problem</b>{p}</p><p><b>Fix</b>{s}</p><p class="but"><b>But then</b>{b}</p></a></li>' for n, t, p, s, b in story) + '</ol>'

numbers = [('V = I x R', 'Ohm&rsquo;s law'), ('4 A, 9 ohm, 14 V', 'the three Ohm examples (12 V/3, 36 V/4 A, 2 A x 7)'),
           ('18 kohm', 'series example 3 + 10 + 5'), ('625 ohm', 'parallel example 10 k, 2 k, 1 k'),
           ('198.70 ohm, 120.78 mA', 'series-parallel example at 24 V'), ('0 to 1023', 'analogRead range for 0 to 5 V (2.5 V gives about 512)'),
           ('0 to 255', 'analogWrite range in the motor example'), ('0 to 180', 'servo angle after map()'),
           ('40 kHz', 'ultrasonic sensor sound'), ('13.56 MHz', 'NFC frequency'), ('2.4 GHz', 'Bluetooth ISM band'),
           ('1 Mbps', 'Bluetooth data rate'), ('~65k', 'ZigBee node limit'), ('0.3 to 50 kbps', 'LoRaWAN data rate'),
           ('140 / day, 12 B, 8 B', 'Sigfox messages per device, uplink and downlink payload'),
           ('128-bit vs 32-bit', 'IPv6 vs IPv4 address size'), ('4 bytes / 2 bytes', 'CoAP header / MQTT minimum overhead'),
           ('QoS 0, 1, 2', 'at most / at least / exactly once'), ('5', 'NIST cloud characteristics'), ('6', 'cloud advantages on the slides'),
           ('150,000', 'cameras reached in the Verkada hack'), ('35 / 35 / 10 / 20', 'project rubric: design, documentation, SDG 11, presentation (%)'),
           ('3 Jan 2027, 11.59 pm', 'project due date')]
numbers_html = '<ul class="nums">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in numbers) + '</ul>'
traps = [
 'Parallel total resistance is <b>smaller</b> than the smallest branch; use 1/R = 1/R1 + 1/R2 + ... (the slide prints it wrongly as 1/(R1 + R2 + R3)).',
 'Series: same <b>current</b>. Parallel: same <b>voltage</b>.',
 'Two resistors in parallel: product over sum (my shortcut), for example 100 and 250 give 71.429 ohm.',
 'An INPUT_PULLUP button reads <b>HIGH when not pressed</b> and LOW when pressed.',
 'analogRead is 0 to 1023, analogWrite is 0 to 255; they are different scales.',
 'Ultrasonic distance divides the echo time by 2 (out and back); the slide only says time-of-flight.',
 'A microprocessor is only a CPU; a microcontroller has CPU, memory and peripherals on one chip.',
 'TCP/IP model has four layers (application, host-to-host, internet, network access); OSI has seven.',
 'CoAP runs on UDP with a 4-byte header; MQTT uses a broker with a 2-byte minimum overhead.',
 'MQTT: + is one level, # is all remaining levels. QoS 1 may deliver twice; QoS 2 delivers exactly once.',
 'IaaS gives the most control, SaaS the least. Hybrid keeps sensitive data on-premises.',
 'ACID goes with relational databases, BASE with NoSQL. Relational scales up, NoSQL scales out.',
 'Project links must be in the PDF report, not by email. The Assignment 1 brief in the folder carries 2022 and 2023/24 dates.',
 'Topics 1, 4 (protocols) and 5 come from older decks (2024/25), not this year&rsquo;s folder; confirm they match your lectures.',
]
traps_html = '<ul class="traps">' + ''.join(f'<li>{t}</li>' for t in traps) + '</ul>'
cards = [
 ('IoT four-step flow', 'Sensor, connectivity, data processing, user interface.'),
 ('Eight IoT design considerations', 'Scalability, reliability, security and privacy, performance, interoperability, power efficiency, cost, maintainability.'),
 ('Gateway functions', 'Aggregate data, translate protocols, secure the channel, process locally.'),
 ('Sensor (ANSI)', 'A device that gives a usable output in response to a specified measurand.'),
 ('Sensor choice: three factor groups', 'Environmental, economic, sensor characteristics.'),
 ('Ultrasonic sensor', 'Trig sends 40 kHz sound; echo receives it; distance from time-of-flight (sound goes out and back).'),
 ('Sensor to actuator', 'Sensor measures, controller decides, actuator acts; the sensor output becomes the actuator input.'),
 ('Hydraulic vs pneumatic vs electric', 'Big force and leaks / cheap, quick, compressor on / quiet, precise, expensive.'),
 ('ADC steps', 'Sampling, quantisation, encoding. Sample at least twice the highest frequency.'),
 ('Ohm&rsquo;s law', 'V = I x R; I = V / R; R = V / I.'),
 ('Series rules', 'Same current; resistances add; voltage drops add.'),
 ('Parallel rules', 'Same voltage; currents add; total resistance smaller than any branch.'),
 ('Parallel example', '10 k, 2 k, 1 k in parallel = 625 ohm; at 9 V: 0.9, 4.5, 9.0 mA.'),
 ('Embedded system: three unique points', 'One specific task, runs without human intervention, real-time constraints.'),
 ('Microprocessor vs microcontroller', 'CPU only, needs external parts / computer on a chip with memory and peripherals.'),
 ('setup() and loop()', 'setup runs once after power-up or reset; loop repeats.'),
 ('INPUT_PULLUP', 'Internal pull-up to 5 V: open button reads HIGH, pressed reads LOW.'),
 ('PAN, LAN, WAN', 'Personal (metres), local (small area, one owner), wide (large area, many ISPs).'),
 ('BLE', '2.4 GHz, sleeps between connections, years of battery, 1 Mbps.'),
 ('LPWAN', 'Low power, long range, low data rate, deep penetration; LoRaWAN and Sigfox.'),
 ('IPv6 vs IPv4', '128-bit (about 3.4 x 10^38) vs 32-bit (about 4.3 billion); not interoperable.'),
 ('TCP vs UDP', 'Connection-oriented reliable / connectionless best effort, fast.'),
 ('CoAP', 'REST-like on UDP, 4-byte header, GET POST PUT DELETE, Max-Age caching.'),
 ('MQTT', 'Publish/subscribe through a broker; topics with + and #; QoS 0, 1, 2; retained; last will.'),
 ('Cloud definition', 'On-demand delivery of IT resources over the internet with pay-as-you-go pricing.'),
 ('IaaS, PaaS, SaaS', 'Infrastructure, platform, software as a service; control drops from IaaS to SaaS.'),
 ('Four data quality fixes', 'Noise reduction, anomaly detection and cleansing, missing value prediction, data fusion.'),
 ('ACID vs BASE', 'Atomic, consistent, isolated, durable / basically available, soft state, eventually consistent.'),
 ('CIA of security', 'Confidentiality, integrity, availability.'),
 ('Mirai lesson', 'It logs in with default credentials; change defaults, use strong authentication.'),
 ('Project at a glance', 'SDG 11 smart city system; hardware + cloud + visualisation; PDF report with repo and video links; due 3 Jan 2027, 11.59 pm.'),
]
cards_html = '<div class="cards" id="cards">' + ''.join(
    f'<button class="card" type="button" aria-pressed="false"><span class="front">{q}</span><span class="back">{a}</span></button>' for q, a in cards) + '</div>'
N_CARDS = len(cards)

weeks_html = ''.join([
 week(1, '', 'The IoT system', 'What IoT is, its parts, the stack and the challenges.',
      psn('Ordinary objects can sense but cannot share, so nothing is automated or learned from them.',
          'Add sensors, software and connectivity; route data through a gateway and the cloud to a user interface.',
          'The system depends on what it senses and does. How do sensors and actuators work?'), MAPS[1], w1_vis, w1_terms, w1_boss),
 week(2, '', 'Sensors and actuators', 'Turning the physical world into signals and signals into action.',
      psn('The world is physical but computers only understand electrical signals.',
          'Sensors give a usable signal for a measurand; actuators turn the controller&rsquo;s signal into motion.',
          'Both need power and a brain: what circuit and computer sit in the middle?'), MAPS[2], w2_vis, w2_terms, w2_boss),
 week(3, '', 'IoT circuit and embedded systems', 'Ohm&rsquo;s law, series and parallel circuits, and programming a microcontroller.',
      psn('Sensors and actuators need a closed, powered circuit and something to decide.',
          'Ohm&rsquo;s law and series/parallel analysis; a microcontroller running Arduino code.',
          'One device on its own is isolated: how does it talk to others?'), MAPS[3], w3_vis, w3_terms, w3_boss),
 week(4, '', 'IoT networks and protocols', 'Network basics, wireless technologies, TCP/IP, REST, CoAP and MQTT.',
      psn('Devices are small and battery-powered on poor links but must reach distant systems.',
          'Choose the wireless technology by trade-offs; use light protocols on UDP such as CoAP and MQTT.',
          'Data arrives in huge, messy volumes: where does it go and how is it protected?'), MAPS[4], w4_vis, w4_terms, w4_boss),
 week(5, '', 'Cloud, data and security', 'Cloud services, IoT data quality and databases, security, trust and privacy.',
      psn('Large amounts of unreliable data, and a connected world open to attack.',
          'Cloud platforms, data quality methods, suitable databases, and security, trust and privacy controls.',
          'The folder&rsquo;s material ends here; the project joins all five topics into a working system.'), MAPS[5], w5_vis, w5_terms, w5_boss),
])
nav = ('<a class="wx" href="#big-picture">Big picture</a>' + ''.join(f'<a class="w{n}" href="#week-{n}">Topic {n}</a>' for n in range(1, 6))
       + '<a class="wx" href="#project">Project</a><a class="wx" href="#cheat-sheet">Cheat sheet</a><a class="wx" href="#drill">Flashcards</a>')

CSS = (open(os.path.join(HERE, 'style.css')).read() + open(os.path.join(HERE, 'extra_cst.css')).read()
       + open(os.path.join(HERE, 'bigp.css')).read() + open(os.path.join(HERE, 'extra_cmt323.css')).read())
JS = open(os.path.join(HERE, 'script.js')).read()

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#060510">
<title>CPC357 Notes: IoT Architecture and Smart Applications</title>
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
  <img class="subj" src="../assets/subjects/cpc357.svg" width="96" height="96" alt="">
  <p class="eyebrow">CPC357 · IoT Architecture and Smart Applications</p>
  <h1>Topics 1 to 5, as one story</h1>
  <p class="lead">Every topic exists because the one before it left a gap. Read it as <b>problem, solution, new problem</b>, and the facts hang together.</p>
  <nav class="jump" aria-label="Jump to a section">{nav}</nav>
</header>
<main>

<section id="big-picture" class="bigp wx">
  <h2 class="sec">Big picture: read this first</h2>
  <p class="headsup"><b>One question runs through all five topics:</b> how does a physical thing sense the world, act on it, talk to others, and put its data to safe use? Topic 1 is the system map. Topic 2 gives it senses and muscles. Topic 3 gives it power and a brain. Topic 4 lets it talk. Topic 5 gives the data somewhere to go and a way to stay safe.</p>
  <p class="small"><b>Where the material comes from:</b> this year&rsquo;s folder has Lectures 2 to 5 (sensors and actuators, circuit, embedded system, networks). Lecture 1 is missing and the later lectures (protocols, cloud, data, security) are not in it yet, so Topics 1 and 5 and the protocol part of Topic 4 come from the older decks in your Learning Materials folder (2024/25). Each topic says which decks it uses.</p>
  <h3>The chain: each topic fixes a gap the last one left</h3>
  <ol class="chain">
    <li class="w1"><span class="tn">Topic 1</span><b>The IoT system</b><span class="kw">Parts, stack, gateway, challenges</span><span class="bridge">But what does it sense and do? &hellip;</span></li>
    <li class="w2"><span class="tn">Topic 2</span><b>Sensors and actuators</b><span class="kw">Measurand, signal chain, motion</span><span class="bridge">But they need power and a brain &hellip;</span></li>
    <li class="w3"><span class="tn">Topic 3</span><b>Circuit and embedded</b><span class="kw">Ohm&rsquo;s law, microcontroller, Arduino</span><span class="bridge">But it is alone &hellip;</span></li>
    <li class="w4"><span class="tn">Topic 4</span><b>Networks and protocols</b><span class="kw">Wireless, TCP/IP, CoAP, MQTT</span><span class="bridge">But where does the data go? &hellip;</span></li>
    <li class="w5"><span class="tn">Topic 5</span><b>Cloud, data, security</b><span class="kw">Cloud, quality, databases, protection</span><span class="bridge">Then the project builds the whole chain.</span></li>
  </ol>

  <h3>How Topic 1 connects to Topic 5</h3>
  <p class="small">Topic 1 draws the whole pipeline once: sensor, connectivity, data processing, user interface. Topics 2 to 5 open each box in turn: the sensing and acting box (2), the device box (3), the connectivity box (4) and the processing and storage box with its protection (5). The project asks you to build all five boxes and show them working.</p>
  <div class="promise tbl-wrap"><table><thead><tr><th>Topic 1 raised &hellip;</th><th>Answered in &hellip;</th></tr></thead><tbody>
    <tr><td>Sensors and actuators in the architecture</td><td><b>Topic 2</b>.</td></tr>
    <tr><td>Embedded system and microcontroller</td><td><b>Topic 3</b> (and the circuit that powers it).</td></tr>
    <tr><td>Wireless technology choice, protocol stack, CoAP and MQTT</td><td><b>Topic 4</b>.</td></tr>
    <tr><td>Cloud, data analytics and AI, challenges</td><td><b>Topic 5</b>.</td></tr>
    <tr><td>Security and privacy challenge</td><td><b>Topic 5</b> (and the secure framework in Topic 4).</td></tr></tbody></table></div>

  <h3>Four threads that run through all five topics</h3>
  <p class="small">These links are my own summary of the slides, to show how the topics connect. They are not slide text.</p>
  <div class="tbl-wrap"><table><thead><tr><th>Thread</th><th class="t1">Topic 1</th><th class="t2">Topic 2</th><th class="t3">Topic 3</th><th class="t4">Topic 4</th><th class="t5">Topic 5</th></tr></thead><tbody>
    <tr><th>Small and power-limited</th><td>Power efficiency</td><td>Low-power signals</td><td>Microcontroller, circuit</td><td>BLE, LPWAN, UDP</td><td>Edge computing</td></tr>
    <tr><th>Signal to data</th><td>Four-step flow</td><td>ADC</td><td>analogRead</td><td>Payload, topics</td><td>Data quality</td></tr>
    <tr><th>Trade-offs</th><td>Design considerations</td><td>Choosing a sensor</td><td>Series vs parallel</td><td>Wireless trade-offs</td><td>SQL vs NoSQL</td></tr>
    <tr><th>Protection</th><td>Security challenge</td><td>Isolation, error control</td><td>Real-time limits</td><td>Secure framework, TLS</td><td>CIA, authentication</td></tr></tbody></table></div>

  <h3>If you remember only five sentences</h3>
  <ol class="five">
    <li><b>Topic 1:</b> an IoT system moves data from sensors through connectivity and processing to a user interface, with a gateway and cloud between, under eight design considerations.</li>
    <li><b>Topic 2:</b> sensors turn a measurand into a usable signal through a conditioning and ADC chain, and actuators (hydraulic, pneumatic, electric) turn the controller&rsquo;s decision into motion.</li>
    <li><b>Topic 3:</b> Ohm&rsquo;s law (V = I x R) with series and parallel rules powers the circuit, and a microcontroller running setup() and loop() is the brain.</li>
    <li><b>Topic 4:</b> pick a wireless technology by range, power and rate trade-offs, then use light protocols on UDP: CoAP (REST-like) or MQTT (publish/subscribe with a broker).</li>
    <li><b>Topic 5:</b> the cloud stores and analyses data, data quality and the right database make it useful, and security, trust and privacy controls (authentication, encryption, minimisation) keep it safe.</li>
  </ol>
</section>

<section id="story" class="band">
  <h2 class="sec">Previously on CPC357</h2>
  <p class="small">Tap a card to jump to that topic. Read the "But then" line, then the next card&rsquo;s "Problem": they are the same sentence.</p>
  {story_html}
</section>
{weeks_html}
{w_pj}
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
<footer class="foot"><p>Built from the CPC357 lecture decks in the owner&rsquo;s folders and the project and assignment briefs. The slides belong to their lecturers; this page is a student&rsquo;s own summary in own words, with redrawn diagrams and no slide images. Items marked "my own" or "my reading" are not from the slides.</p></footer>
<script>
{JS}
</script>
</body>
</html>'''
open(os.path.join(OUT, 'index.html'), 'w').write(PAGE)
print('cpc357 ok', len(PAGE), 'cards', N_CARDS)
