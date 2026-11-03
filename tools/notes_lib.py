"""Shared helpers for the subject notes pages (mind maps, terms, boss-fight answers)."""
import html
E = html.escape


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
            parts.append(f'<path class="mm-link" d="M{cstart:.1f} {CY:.1f} C{mid:.1f} {CY:.1f} {mid:.1f} {by:.1f} {inner:.1f} {by:.1f}"/>')
            parts.append(f'<rect class="mm-branch" x="{bx - bw / 2:.1f}" y="{by - 16:.1f}" width="{bw:.1f}" height="32" rx="16"/>')
            parts.append(f'<text class="mm-btxt" x="{bx:.1f}" y="{by + 4.6:.1f}" text-anchor="middle">{E(blabel)}</text>')
            dx = CX + sign * DOT_OFF
            tx = CX + sign * TXT_OFF
            for ly, leaf in zip(ys, leaves):
                m = (outer + dx) / 2
                parts.append(f'<path class="mm-link thin" d="M{outer:.1f} {by:.1f} C{m:.1f} {by:.1f} {m:.1f} {ly:.1f} {dx:.1f} {ly:.1f}"/>')
                parts.append(f'<circle class="mm-dot" cx="{dx:.1f}" cy="{ly:.1f}" r="4.2"/>')
                anchor = 'start' if sign > 0 else 'end'
                parts.append(f'<text class="mm-leaf" x="{tx:.1f}" y="{ly + 4.4:.1f}" text-anchor="{anchor}">{E(leaf)}</text>')
            y += len(leaves) * LEAF_H + GAP

    draw_side(left, -1)
    draw_side(right, 1)
    parts.append(f'<rect class="mm-center" x="{CX - 86:.1f}" y="{CY - 32:.1f}" width="172" height="64" rx="22"/>')
    words = center.split(' ')
    if len(center) > 16 and len(words) > 1:
        half = len(words) // 2 or 1
        l1, l2 = ' '.join(words[:half]), ' '.join(words[half:])
        parts.append(f'<text class="mm-ctxt" x="{CX:.1f}" y="{CY - 4:.1f}" text-anchor="middle">{E(l1)}</text>')
        parts.append(f'<text class="mm-ctxt" x="{CX:.1f}" y="{CY + 16:.1f}" text-anchor="middle">{E(l2)}</text>')
    else:
        parts.append(f'<text class="mm-ctxt" x="{CX:.1f}" y="{CY + 5:.1f}" text-anchor="middle">{E(center)}</text>')
    return (f'<svg class="mm" viewBox="0 0 {VBW} {H:.0f}" role="img" aria-label="{E(label)}" xmlns="http://www.w3.org/2000/svg">'
            + ''.join(parts) + '</svg>')


def terms(items):
    return '<dl class="terms">' + ''.join(f'<div><dt>{t}</dt><dd>{d}</dd></div>' for t, d in items) + '</dl>'


def psn(problem, solution, newp):
    return ('<div class="psn">'
            f'<div class="p"><b>Problem</b><p>{problem}</p></div><span class="arr" aria-hidden="true">&rarr;</span>'
            f'<div class="s"><b>Solution</b><p>{solution}</p></div><span class="arr" aria-hidden="true">&rarr;</span>'
            f'<div class="n"><b>New problem</b><p>{newp}</p></div></div>')


def qa(q, a, n):
    return (f'<details class="qa"><summary><span class="qn">{n}</span>{q}</summary><div class="ans">{a}</div></details>')


def week(n, label, title, blurb, psn_html, mm_svg, visuals, terms_html, boss, unit='Topic'):
    return f'''
<section id="week-{n}" class="week w{n}">
  <div class="week-head"><span class="wk">{unit} {n}</span><h2>{title}</h2><p class="blurb">{blurb}</p></div>
  {psn_html}
  <h3>Mind map</h3>
  <div class="mm-wrap" tabindex="0" role="group" aria-label="Scrollable mind map"><p class="hint">Swipe sideways to see the whole map</p>{mm_svg}</div>
  {visuals}
  <h3>Terms to know</h3>
  {terms_html}
  <h3>Boss fight</h3>
  <p class="small">Tap a question to reveal the model answer. Try it in your head first.</p>
  {boss}
</section>'''
