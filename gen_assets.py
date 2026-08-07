"""Generates the animated SVG assets used by README.md.

GitHub renders SVGs referenced from a README as <img>, which allows CSS and
SMIL animations embedded in the SVG but never JavaScript. Every asset here is
therefore a self-contained, deterministic animation loop.

Run: python gen_assets.py  (writes into ./assets/)
"""
import random
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

BG = "#0b1016"
SURFACE = "#111924"
SURFACE2 = "#161f2c"
BORDER = "#263140"
TEXT = "#e6edf3"
MUTED = "#8fa3b8"
GREEN = "#57d9a3"
GREEN_DIM = "#2c5c49"
AMBER = "#e3b341"
ORANGE = "#d97757"
MONO = "'Cascadia Code','SF Mono',Consolas,Menlo,monospace"

ICONS = {
    "github": '<symbol id="i-github" viewBox="0 0 48 48"><path fill="#e6edf3" d="M24 4a20 20 0 0 0-6.3 39c1 .2 1.4-.5 1.4-1v-3.8c-5.6 1.2-6.8-2.4-6.8-2.4-.9-2.3-2.2-3-2.2-3-1.8-1.2.1-1.2.1-1.2 2 .1 3.1 2.1 3.1 2.1 1.8 3 4.7 2.2 5.8 1.7.2-1.3.7-2.2 1.3-2.7-4.5-.5-9.2-2.2-9.2-9.9 0-2.2.8-4 2.1-5.4-.2-.5-.9-2.6.2-5.4 0 0 1.7-.5 5.5 2.1a19 19 0 0 1 10 0c3.8-2.6 5.5-2.1 5.5-2.1 1.1 2.8.4 4.9.2 5.4a7.8 7.8 0 0 1 2.1 5.4c0 7.7-4.7 9.4-9.2 9.9.7.6 1.4 1.9 1.4 3.8V42c0 .5.4 1.2 1.4 1A20 20 0 0 0 24 4z"/></symbol>',
    "person": '<symbol id="i-person" viewBox="0 0 24 24"><circle cx="12" cy="8.5" r="3.8" fill="none" stroke="#c9d5e0" stroke-width="1.9"/><path d="M5 20c1-4 3.5-5.5 7-5.5s6 1.5 7 5.5" fill="none" stroke="#c9d5e0" stroke-width="1.9" stroke-linecap="round"/></symbol>',
    "claude": '<symbol id="i-claude" viewBox="0 0 24 24"><g stroke="#d97757" stroke-width="2.4" stroke-linecap="round"><path d="M12 4v16M4 12h16M6.5 6.5l11 11M17.5 6.5l-11 11"/></g></symbol>',
    "anti": '<symbol id="i-anti" viewBox="0 0 24 24"><linearGradient id="ag-grad" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#3a89fe"/><stop offset=".45" stop-color="#64b684"/><stop offset=".72" stop-color="#e0a02d"/><stop offset="1" stop-color="#eb5b34"/></linearGradient><path fill="none" stroke="url(#ag-grad)" stroke-width="3.1" stroke-linecap="round" d="M3.5 20.2 C7.2 19.4 9.6 13 11.2 7.6 Q12 5.3 12.8 7.6 C14.4 13 16.8 19.4 20.5 20.2"/></symbol>',
    "tests": '<symbol id="i-tests" viewBox="0 0 24 24"><path d="M10 3h4M12 3v4" stroke="#57d9a3" stroke-width="1.8" stroke-linecap="round"/><path d="M12 7c-1 3-5 8-5 11a5 5 0 0 0 10 0c0-3-4-8-5-11z" fill="none" stroke="#57d9a3" stroke-width="1.8" stroke-linejoin="round"/><path d="M9.8 15.5l1.7 1.7 3-3" fill="none" stroke="#57d9a3" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>',
    "sonar": '<symbol id="i-sonar" viewBox="0 0 24 24"><g fill="none" stroke="#549dd0" stroke-width="1.9" stroke-linecap="round"><path d="M4 19a15 15 0 0 1 15-15"/><path d="M7 19a12 12 0 0 1 12-12"/><path d="M10 19a9 9 0 0 1 9-9"/></g></symbol>',
    "horusec": '<symbol id="i-horusec" viewBox="0 0 24 24"><path d="M12 3l7 2.8v5.7c0 4.3-2.9 7.4-7 9-4.1-1.6-7-4.7-7-9V5.8z" fill="none" stroke="#c084fc" stroke-width="1.8" stroke-linejoin="round"/><path d="M8.8 11.8l2.2 2.2 4-4.4" fill="none" stroke="#c084fc" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>',
    "copilot": '<symbol id="i-copilot" viewBox="0 0 24 24"><rect x="3" y="7.5" width="18" height="10" rx="5" fill="none" stroke="#e6edf3" stroke-width="1.8"/><rect x="7.5" y="10.2" width="2.4" height="4.6" rx="1.2" fill="#e6edf3"/><rect x="14.1" y="10.2" width="2.4" height="4.6" rx="1.2" fill="#e6edf3"/></symbol>',
    "docker": '<symbol id="i-docker" viewBox="0 0 48 48"><g fill="#2496ed"><rect x="10" y="20" width="6" height="6" rx="1"/><rect x="17" y="20" width="6" height="6" rx="1"/><rect x="24" y="20" width="6" height="6" rx="1"/><rect x="17" y="13" width="6" height="6" rx="1"/><rect x="24" y="13" width="6" height="6" rx="1"/><rect x="24" y="6" width="6" height="6" rx="1"/><path d="M4 29h37c2 0 4-1.5 4-1.5s-2-2.8-5-2.5c-.4-2.4-2.5-3.5-2.5-3.5s-2.4 1.6-1.8 4c-9 0-31.7 0-31.7 0s-.6 8.5 8 11.5c9 3.2 20.5 1 26-6"/></g></symbol>',
    "playwright": '<symbol id="i-playwright" viewBox="0 0 24 24"><path d="M4 5.5c2.7 1.1 5.3 1.1 8-.4 2.7 1.5 5.3 1.5 8 .4v6.3c0 5-3.4 8.6-8 9.7-4.6-1.1-8-4.7-8-9.7z" fill="none" stroke="#45ba4b" stroke-width="1.8" stroke-linejoin="round"/><circle cx="8.7" cy="10.8" r="1.3" fill="#45ba4b"/><circle cx="15.3" cy="10.8" r="1.3" fill="#45ba4b"/><path d="M8.7 15c1 1.4 2.1 2 3.3 2s2.3-.6 3.3-2" fill="none" stroke="#45ba4b" stroke-width="1.7" stroke-linecap="round"/></symbol>',
    "k8s": '<symbol id="i-k8s" viewBox="0 0 48 48"><polygon fill="#326ce5" points="24,3 42,12 46,31 33,45 15,45 2,31 6,12"/><g stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round"><circle cx="24" cy="24" r="8"/><path d="M24 10v6M24 32v6M11 17l5.5 3.2M37 17l-5.5 3.2M14 36l4.5-4.5M34 36l-4.5-4.5"/></g></symbol>',
    "gha": '<symbol id="i-gha" viewBox="0 0 48 48"><circle cx="19" cy="19" r="13" fill="none" stroke="#2088ff" stroke-width="3.5"/><path fill="#2088ff" d="M15.5 13.5l9 5.5-9 5.5z"/><circle cx="36" cy="34" r="6" fill="none" stroke="#2088ff" stroke-width="3"/><path d="M28.5 27.5 L31.5 30.5" stroke="#2088ff" stroke-width="3" stroke-linecap="round"/></symbol>',
}


def svg(w, h, style, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" font-family="{MONO}">'
        f"<style>{style}</style><defs>{defs}</defs>{body}</svg>"
    )


# ---------------------------------------------------------------- pipeline
def build_pipeline():
    NW, NH, JOB_GAP, LINE_GAP = 150, 40, 14, 14
    TOP, X0, TAB_W, CARD_W, CARD_PAD, CARD_GAP, INNER_GAP = 8, 8, 28, 530, 12, 40, 36
    CYCLE = 12.0  # seconds; 6 stages x 1.5s + 3s all-green pause
    STAGE_T = 1.5

    stages = [
        ("plan", "#57d9a3", [[("Issues", "github", None)]]),
        ("code", "#7c8cf8", [
            [("Dev 1", "person", "claude"), ("Dev 2", "person", "anti"), ("Dev 3", "person", "claude")],
            [("GitHub", "github", None)],
        ]),
        ("test", "#e3b341", [[("Unit Tests", "tests", None), ("SonarQube", "sonar", None),
                              ("Horusec", "horusec", None), ("Copilot", "copilot", None)]]),
        ("package", "#38bdf8", [[("Docker", "docker", None)]]),
        ("e2e", "#c084fc", [[("Playwright", "playwright", None)]]),
        ("release", "#f47067", [[("Kubernetes", "k8s", None)]]),
    ]
    badge_color = {"claude": ORANGE, "anti": "#3a89fe"}

    def row_lines(jobs):
        return 2 if len(jobs) > 3 else 1

    def row_height(jobs):
        n = row_lines(jobs)
        return n * NH + (n - 1) * LINE_GAP

    cards, nodes, edges, rows = [], [], [], []
    y_cursor = TOP
    for c, (name, color, rws) in enumerate(stages):
        rows_h = sum(row_height(j) for j in rws)
        card_h = CARD_PAD * 2 + rows_h + (len(rws) - 1) * INNER_GAP
        cards.append((c, name, color, X0, y_cursor, CARD_W, card_h))
        row_y = y_cursor + CARD_PAD
        for jobs in rws:
            rows.append((c, jobs, row_y))
            row_y += row_height(jobs) + INNER_GAP
        y_cursor += card_h + CARD_GAP
    total_h = y_cursor - CARD_GAP + TOP

    placed_rows = []
    for c, jobs, ry in rows:
        lines = row_lines(jobs)
        per = -(-len(jobs) // lines)
        pts = []
        for r, job in enumerate(jobs):
            line, idx = divmod(r, per)
            count = min(per, len(jobs) - line * per)
            line_w = count * NW + (count - 1) * JOB_GAP
            x = X0 + TAB_W + (CARD_W - TAB_W - line_w) / 2 + idx * (NW + JOB_GAP)
            y = ry + line * (NH + LINE_GAP)
            nodes.append((c, job, x, y))
            pts.append((x + NW / 2, y))
        placed_rows.append((c, pts))

    for i in range(1, len(placed_rows)):
        tc = placed_rows[i][0]
        for ax, ay in placed_rows[i - 1][1]:
            for bx, by in placed_rows[i][1]:
                y1, y2 = ay + NH, by
                mid = (y1 + y2) / 2
                edges.append((tc, f"M{ax} {y1} C{ax} {mid},{bx} {mid},{bx} {y2}", ax, y1, bx, y2, mid))

    def pct(t):
        return round(t / CYCLE * 100, 2)

    css = [
        f".nrect{{fill:{SURFACE2};stroke:{BORDER};stroke-width:1.2}}",
        f".ntext{{font-size:12.5px;fill:{TEXT}}}",
        f".tab-label{{font-size:11.5px;letter-spacing:1.2px;fill:{BG};font-weight:700;text-transform:uppercase;text-anchor:middle}}",
        f".spin{{fill:none;stroke:{GREEN};stroke-width:1.8;stroke-linecap:round;stroke-dasharray:24 20}}",
        f".chk{{fill:none;stroke:{TEXT};stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}",
        "@keyframes dashmove{to{stroke-dashoffset:-14}}",
    ]
    for c in range(6):
        a, b = pct(c * STAGE_T), pct((c + 1) * STAGE_T)
        idle = "" if c == 0 else f"0%,{a}%{{stroke-opacity:.35;fill-opacity:.05}}"
        css.append(
            f"@keyframes card{c}{{{idle}{a + .01}%,{b}%{{stroke-opacity:1;fill-opacity:.09}}"
            f"{b + .01}%,100%{{stroke-opacity:.6;fill-opacity:.05}}}}"
            f".card{c}{{animation:card{c} {CYCLE}s linear infinite}}"
        )
        ring_idle = "" if c == 0 else f"0%,{a}%{{stroke:{BORDER};fill:{SURFACE2}}}"
        css.append(
            f"@keyframes ring{c}{{{ring_idle}{a + .01}%,{b}%{{stroke:{GREEN};fill:{SURFACE2}}}"
            f"{b + .01}%,100%{{stroke:{GREEN_DIM};fill:{GREEN_DIM}}}}}"
            f".ring{c}{{stroke-width:1.6;animation:ring{c} {CYCLE}s linear infinite}}"
        )
        spin_idle = "" if c == 0 else f"0%,{a}%{{opacity:0}}"
        css.append(
            f"@keyframes spo{c}{{{spin_idle}{a + .01}%,{b}%{{opacity:1}}{b + .01}%,100%{{opacity:0}}}}"
            f".spo{c}{{animation:spo{c} {CYCLE}s linear infinite}}"
        )
        css.append(
            f"@keyframes chk{c}{{0%,{b}%{{opacity:0}}{b + .01}%,100%{{opacity:1}}}}"
            f".chk{c}{{animation:chk{c} {CYCLE}s linear infinite}}"
        )
        if c > 0:
            css.append(
                f"@keyframes ebase{c}{{0%,{b}%{{stroke:{BORDER}}}{b + .01}%,100%{{stroke:{GREEN_DIM}}}}}"
                f".ebase{c}{{fill:none;stroke-width:1.4;animation:ebase{c} {CYCLE}s linear infinite}}"
                f"@keyframes eop{c}{{0%,{a}%{{opacity:0}}{a + .01}%,{b}%{{opacity:1}}{b + .01}%,100%{{opacity:0}}}}"
                f".eflow{c}{{fill:none;stroke:{GREEN};stroke-width:1.6;stroke-dasharray:5 9;"
                f"animation:eop{c} {CYCLE}s linear infinite,dashmove .8s linear infinite}}"
            )

    body = [f'<rect width="546" height="{total_h}" fill="{BG}"/>',
            '<rect width="0" height="0"><animate id="cyc" attributeName="x" values="0;0" '
            f'dur="{CYCLE}s" repeatCount="indefinite"/></rect>']

    for c, name, color, x, y, w, h in cards:
        body.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{color}" stroke="{color}" class="card{c}"/>'
        )
        tab = (f"M{x + TAB_W} {y} L{x + TAB_W} {y + h} L{x + 12} {y + h} "
               f"Q{x} {y + h} {x} {y + h - 12} L{x} {y + 12} Q{x} {y} {x + 12} {y} Z")
        body.append(f'<path d="{tab}" fill="{color}"/>')
        lx, ly = x + TAB_W / 2 + 3.5, y + h / 2
        body.append(f'<text x="{lx}" y="{ly}" class="tab-label" transform="rotate(-90 {lx} {ly})">{name}</text>')

    for c, d, ax, y1, bx, y2, mid in edges:
        body.append(f'<path d="{d}" class="ebase{c}"/>')
    for c, d, ax, y1, bx, y2, mid in edges:
        body.append(f'<path d="{d}" class="eflow{c}"/>')
        t = c * STAGE_T
        body.append(
            f'<circle r="3.2" fill="{GREEN}" opacity="0">'
            f'<animateMotion path="{d}" begin="cyc.begin+{t}s;cyc.repeatEvent+{t}s" dur="0.75s"/>'
            f'<set attributeName="opacity" to="1" begin="cyc.begin+{t}s;cyc.repeatEvent+{t}s" dur="0.75s"/></circle>'
        )

    for c, (label, icon, badge), x, y in nodes:
        cy = y + NH / 2
        g = [f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="{NH / 2}" class="nrect"/>']
        scx, scy = x + 20, cy
        g.append(f'<circle cx="{scx}" cy="{scy}" r="7" class="ring{c}"/>')
        g.append(
            f'<circle cx="{scx}" cy="{scy}" r="7" class="spin spo{c}">'
            f'<animateTransform attributeName="transform" type="rotate" from="0 {scx} {scy}" '
            f'to="360 {scx} {scy}" dur="0.9s" repeatCount="indefinite"/></circle>'
        )
        g.append(f'<path d="M{x + 16.5} {y + 20.5}l2.8 2.8 5-5.6" class="chk chk{c}"/>')
        if badge:
            bc = badge_color[badge]
            g.append(f'<circle cx="{x + 45}" cy="{cy}" r="12" fill="none" stroke="{bc}" stroke-width="1.7"/>')
            g.append(f'<use href="#i-person" x="{x + 37}" y="{cy - 8}" width="16" height="16"/>')
            g.append(f'<circle cx="{x + 54.5}" cy="{cy + 9}" r="7" fill="{SURFACE2}" stroke="{bc}" stroke-width="1.3"/>')
            g.append(f'<use href="#i-{badge}" x="{x + 50.3}" y="{cy + 4.8}" width="8.5" height="8.5"/>')
            g.append(f'<text x="{x + 66}" y="{cy + 4.5}" class="ntext">{label}</text>')
        else:
            g.append(f'<use href="#i-{icon}" x="{x + 35}" y="{cy - 10}" width="20" height="20"/>')
            g.append(f'<text x="{x + 62}" y="{cy + 4.5}" class="ntext">{label}</text>')
        body.append("".join(g))

    defs = "".join(ICONS[k] for k in
                   ["github", "person", "claude", "anti", "tests", "sonar", "horusec", "copilot",
                    "docker", "playwright", "k8s"])
    (OUT / "pipeline.svg").write_text(svg(546, total_h, "".join(css), "".join(body), defs), encoding="utf-8")


# ---------------------------------------------------------------- terminal
def build_terminal():
    W, H, CYCLE = 460, 262, 16.0
    lines = [
        ("cmd", "whoami"),
        ("out", "Fran Oberto — Computer Engineer"),
        ("cmd", "ls ~/skills"),
        ("out", "backend/   devops/   quality/"),
        ("cmd", "cat stack.txt"),
        ("out", "python · kubernetes · docker · ci/cd"),
        ("cmd", "uptime"),
        ("out", "shipping code since 2020 — zero drama"),
    ]
    css = [
        f".cmd{{font-size:13px;fill:{TEXT}}}",
        f".out{{font-size:13px;fill:{MUTED}}}",
        f".p{{font-size:13px;fill:{GREEN}}}",
        "@keyframes blink{50%{opacity:0}}",
        f".caret{{fill:{GREEN};animation:blink .9s steps(1) infinite}}",
    ]
    body = [
        f'<rect width="{W}" height="{H}" rx="10" fill="{SURFACE}" stroke="{BORDER}"/>',
        f'<rect x="1" y="1" width="{W - 2}" height="30" fill="{SURFACE2}"/>',
        f'<line x1="1" y1="31" x2="{W - 1}" y2="31" stroke="{BORDER}"/>',
        f'<circle cx="18" cy="16" r="5" fill="{GREEN}"/><circle cx="34" cy="16" r="5" fill="{BORDER}"/>'
        f'<circle cx="50" cy="16" r="5" fill="{BORDER}"/>',
    ]
    t = 0.8
    for i, (kind, txt) in enumerate(lines):
        y = 56 + i * 25
        show = round(t / CYCLE * 100, 2)
        css.append(f"@keyframes ln{i}{{0%,{show}%{{opacity:0}}{show + .01}%,100%{{opacity:1}}}}"
                   f".ln{i}{{animation:ln{i} {CYCLE}s linear infinite}}")
        if kind == "cmd":
            body.append(f'<g class="ln{i}"><text x="18" y="{y}" class="p">$</text>'
                        f'<text x="34" y="{y}" class="cmd">{txt}</text></g>')
            t += 0.55 + 0.05 * len(txt)
        else:
            body.append(f'<g class="ln{i}"><text x="34" y="{y}" class="out">{txt}</text></g>')
            t += 0.9
    body.append(f'<text x="18" y="{56 + len(lines) * 25}" class="p">$</text>'
                f'<rect x="34" y="{44 + len(lines) * 25}" width="8" height="15" class="caret"/>')
    (OUT / "terminal.svg").write_text(svg(W, H, "".join(css), "".join(body)), encoding="utf-8")


# ---------------------------------------------------------------- htop
def build_htop():
    W, H = 460, 348
    cores = [("backend", 64, 2.3), ("devops", 48, 3.1), ("quality", 38, 2.7), ("ai-tools", 55, 3.6)]
    procs = [
        (1, "fran", "42.0", "47.3", "18.2", "51000h", "python api/main.py", False),
        (42, "fran", "33.1", "28.4", "12.4", "14000h", "kubectl apply -f prod/", False),
        (137, "fran", "28.6", "35.2", "9.1", "8700h", "claude code", False),
        (314, "fran", "21.3", "17.8", "7.7", "5100h", "antigravity .", False),
        (512, "fran", "12.0", "15.6", "4.2", "26000h", "pytest --cov", False),
        (999, "root", "0.1", "0.1", "0.3", "&#8734;", "[clean-code-daemon]", True),
    ]
    css = [
        f".lbl{{font-size:11px;fill:{MUTED}}}",
        f".pct{{font-size:11px;fill:{TEXT}}}",
        f".meta{{font-size:11px;fill:{MUTED}}}",
        f".metav{{font-size:11px;fill:{GREEN}}}",
        f".rh{{font-size:11.5px;fill:{GREEN};font-weight:500}}",
        f".rc{{font-size:11.5px;fill:{TEXT}}}",
        f".rk{{font-size:11.5px;fill:{GREEN_DIM}}}",
        f".rt{{font-size:11.5px;fill:{AMBER}}}",
        f".fk{{font-size:11px;fill:{MUTED}}}",
        f".fkb{{font-size:11px;fill:{BG};font-weight:600}}",
        "@keyframes swapA{0%,45%{opacity:1}50%,95%{opacity:0}100%{opacity:1}}",
        "@keyframes swapB{0%,45%{opacity:0}50%,95%{opacity:1}100%{opacity:0}}",
        "@keyframes gitpush{0%,28%{opacity:0}30%,55%{opacity:1}57%,100%{opacity:0}}",
        ".ga{animation:gitpush 12s linear infinite}",
    ]
    body = [f'<rect width="{W}" height="{H}" rx="10" fill="{SURFACE}" stroke="{BORDER}"/>']
    for i, (name, base, dur) in enumerate(cores):
        col, row = i % 2, i // 2
        x, y = 16 + col * 224, 18 + row * 22
        bw = 118
        color = GREEN if base < 50 else AMBER
        css.append(
            f"@keyframes core{i}{{from{{transform:scaleX({base / 100})}}to{{transform:scaleX({min(.96, base / 100 + .22)})}}}}"
        )
        body.append(
            f'<text x="{x}" y="{y + 10}" class="lbl">{name}</text>'
            f'<rect x="{x + 62}" y="{y}" width="{bw}" height="10" rx="2" fill="{SURFACE2}" stroke="{BORDER}"/>'
            f'<rect x="{x + 62}" y="{y}" width="{bw}" height="10" rx="2" fill="{color}" '
            f'style="transform-origin:{x + 62}px 0;animation:core{i} {dur}s ease-in-out infinite alternate"/>'
            f'<text x="{x + 188}" y="{y + 10}" class="pct">{base}%</text>'
        )
        if col == 1:
            pass
    body.append(
        f'<text x="16" y="72" class="meta">Load average: <tspan class="metav">0.99 0.98 0.97</tspan>'
        f'  Uptime: <tspan class="metav">2350 days</tspan>  Tasks: <tspan class="metav">6</tspan></text>'
    )
    body.append(f'<line x1="1" y1="82" x2="{W - 1}" y2="82" stroke="{BORDER}"/>')
    body.append(f'<rect x="1" y="83" width="{W - 2}" height="22" fill="rgba(87,217,163,.08)"/>')
    headers = [(16, "PID"), (58, "USER"), (104, "CPU%"), (148, "MEM%"), (196, "TIME+"), (268, "COMMAND")]
    body.append("".join(f'<text x="{hx}" y="98" class="rh">{ht}</text>' for hx, ht in headers))
    for i, (pid, user, cpu_a, cpu_b, mem, tim, cmd, kernel) in enumerate(procs):
        y = 124 + i * 24
        cls = "rk" if kernel else "rc"
        row = [
            f'<text x="16" y="{y}" class="{cls}">{pid}</text>',
            f'<text x="58" y="{y}" class="{cls}">{user}</text>',
        ]
        if kernel:
            row.append(f'<text x="104" y="{y}" class="rk">{cpu_a}</text>')
        else:
            d = i * 0.6
            row.append(f'<text x="104" y="{y}" class="rc" style="animation:swapA 4s linear infinite;animation-delay:-{d}s">{cpu_a}</text>')
            row.append(f'<text x="104" y="{y}" class="rc" style="animation:swapB 4s linear infinite;animation-delay:-{d}s">{cpu_b}</text>')
        row.append(f'<text x="148" y="{y}" class="{cls}">{mem}</text>')
        row.append(f'<text x="196" y="{y}" class="{cls}">{tim}</text>')
        row.append(f'<text x="268" y="{y}" class="{cls}">{cmd}</text>')
        body.append("".join(row))
    gy = 124 + len(procs) * 24
    body.append(f'<g class="ga"><text x="16" y="{gy}" class="rt">4821</text><text x="58" y="{gy}" class="rt">fran</text>'
                f'<text x="104" y="{gy}" class="rt">71.4</text><text x="148" y="{gy}" class="rt">2.1</text>'
                f'<text x="196" y="{gy}" class="rt">0:00:02</text><text x="268" y="{gy}" class="rt">git push origin main</text></g>')
    fy = H - 14
    body.append(f'<line x1="1" y1="{fy - 18}" x2="{W - 1}" y2="{fy - 18}" stroke="{BORDER}"/>')
    fx = 16
    for key, lab in [("F1", "Help"), ("F5", "Tree"), ("F6", "SortBy"), ("F9", "Kill"), ("F10", "Quit")]:
        body.append(f'<rect x="{fx}" y="{fy - 11}" width="22" height="14" rx="2" fill="{GREEN}"/>'
                    f'<text x="{fx + 3}" y="{fy}" class="fkb">{key}</text>'
                    f'<text x="{fx + 26}" y="{fy}" class="fk">{lab}</text>')
        fx += 78
    (OUT / "htop.svg").write_text(svg(W, H, "".join(css), "".join(body)), encoding="utf-8")


# ---------------------------------------------------------------- whale
def build_whale():
    random.seed(42)
    COLS, ROWS, CELL, GAP, PAD = 26, 12, 12, 4, 14
    W = PAD * 2 + COLS * (CELL + GAP) - GAP
    H = PAD * 2 + ROWS * (CELL + GAP) - GAP
    blues = ["#0b3a5e", "#0e5a94", "#1d84d0", "#48b2f2"]
    body = [f'<rect width="{W}" height="{H}" rx="12" fill="{SURFACE}" stroke="{BORDER}"/>']
    for c in range(COLS):
        for r in range(ROWS):
            x = PAD + c * (CELL + GAP)
            y = PAD + r * (CELL + GAP)
            fill = random.choice(blues) if random.random() < 0.72 else SURFACE2
            body.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{fill}"/>')
    pts = []
    for r in range(ROWS):
        y = PAD + r * (CELL + GAP) + CELL / 2
        xs = [PAD + CELL / 2, PAD + (COLS - 1) * (CELL + GAP) + CELL / 2]
        if r % 2:
            xs.reverse()
        pts.append(f"{'M' if r == 0 else 'L'}{xs[0]} {y} L{xs[1]} {y}")
    path = " ".join(pts)
    dur = 40
    for delay, r, op in [(0.0, 5, .18), (0.35, 5, .3)]:
        body.append(f'<circle r="{r}" fill="#e6f0fa" opacity="{op}">'
                    f'<animateMotion path="{path}" dur="{dur}s" begin="-{dur - delay}s" repeatCount="indefinite"/></circle>')
    body.append(f'<text font-size="16" text-anchor="middle" dy="5">'
                f'<animateMotion path="{path}" dur="{dur}s" begin="-{dur - 0.7}s" repeatCount="indefinite"/>🐳</text>')
    (OUT / "whale.svg").write_text(svg(W, H, "", "".join(body)), encoding="utf-8")


# ---------------------------------------------------------------- dashboard
def build_dashboard():
    W, H = 920, 176
    PW, GAPX = 221, 12
    css = [
        f".h4{{font-size:10.5px;fill:{MUTED};letter-spacing:1px;text-transform:uppercase}}",
        f".val{{font-size:22px;font-weight:700;fill:{GREEN}}}",
        f".sub{{font-size:10.5px;fill:{MUTED}}}",
        "@keyframes pulse{50%{opacity:.35}}",
        f".dot{{fill:{GREEN};animation:pulse 2.2s ease-in-out infinite}}",
        "@keyframes scroll{to{transform:translateX(-104px)}}",
        ".spark{animation:scroll 5.2s linear infinite}",
        "@keyframes pop{0%{r:3}50%{r:4.5}100%{r:3}}",
        f".tip{{fill:{GREEN};animation:pop 1.4s ease-in-out infinite}}",
        "@keyframes gdraw{0%{stroke-dashoffset:163}18%,100%{stroke-dashoffset:3}}",
        f".garc{{fill:none;stroke:{GREEN};stroke-width:9;stroke-linecap:round;stroke-dasharray:163;"
        "animation:gdraw 12s ease-out infinite}",
        "@keyframes shimmer{to{transform:translateX(190px)}}",
        ".shim{animation:shimmer 2.8s linear infinite}",
    ]
    body = []
    random.seed(7)

    def panel(i, title):
        x = i * (PW + GAPX)
        body.append(f'<rect x="{x}" y="1" width="{PW}" height="{H - 2}" rx="8" fill="{SURFACE}" stroke="{BORDER}"/>')
        body.append(f'<circle cx="{x + 18}" cy="20" r="3.5" class="dot"/>')
        body.append(f'<text x="{x + 30}" y="24" class="h4">{title}</text>')
        return x

    x = panel(0, "commits &#183; week")
    body.append(f'<text x="{x + 16}" y="56" class="val">34</text>')
    base = [random.uniform(18, 40) for _ in range(28)]
    pts_all = base + base
    step = 208 / 26
    pl = " ".join(f"{x + 8 + i * step:.1f},{160 - v * 2.2:.1f}" for i, v in enumerate(pts_all))
    body.append(f'<clipPath id="spc"><rect x="{x + 8}" y="66" width="205" height="100"/></clipPath>')
    body.append(f'<g clip-path="url(#spc)"><g class="spark">'
                f'<polyline points="{pl}" fill="none" stroke="{GREEN}" stroke-width="1.6"/></g>'
                f'<circle cx="{x + 205}" cy="{160 - pts_all[25] * 2.2:.1f}" r="3" class="tip"/></g>')

    x = panel(1, "code quality")
    cx, cy, r = x + PW / 2, 140, 52
    body.append(f'<path d="M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy}" fill="none" stroke="{BORDER}" '
                f'stroke-width="9" stroke-linecap="round"/>')
    body.append(f'<path d="M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy}" class="garc"/>')
    body.append(f'<text x="{cx}" y="{cy - 14}" text-anchor="middle" class="val">98.2%</text>')
    body.append(f'<text x="{cx}" y="{cy + 2}" text-anchor="middle" class="sub">sonarqube gate: passed</text>')

    x = panel(2, "uptime")
    body.append(f'<text x="{x + 16}" y="66" class="val">6y+ shipping</text>')
    body.append(f'<text x="{x + 16}" y="88" class="sub">since first commit &#183; 2020</text>')
    body.append(f'<rect x="{x + 16}" y="110" width="189" height="7" rx="3.5" fill="{SURFACE2}"/>')
    body.append(f'<clipPath id="upc"><rect x="{x + 16}" y="110" width="188.6" height="7" rx="3.5"/></clipPath>')
    body.append(f'<g clip-path="url(#upc)"><rect x="{x + 16}" y="110" width="189" height="7" fill="{GREEN_DIM}"/>'
                f'<rect x="{x - 50}" y="110" width="50" height="7" fill="{GREEN}" opacity=".6" class="shim"/></g>')
    body.append(f'<text x="{x + 16}" y="136" class="sub">availability 99.98%</text>')

    x = panel(3, "deploys &#183; month")
    body.append(f'<text x="{x + 16}" y="56" class="val">24</text>')
    heights = [random.uniform(18, 88) for _ in range(10)]
    for i, hh in enumerate(heights):
        bx = x + 14 + i * 20
        color = GREEN if i == 9 else "rgba(87,217,163,.45)"
        css.append(f"@keyframes bar{i}{{0%{{transform:scaleY(0)}}{8 + i * 3}%{{transform:scaleY(0)}}"
                   f"{20 + i * 3}%,100%{{transform:scaleY(1)}}}}")
        body.append(f'<rect x="{bx}" y="{162 - hh:.1f}" width="13" height="{hh:.1f}" rx="2" fill="{color}" '
                    f'style="transform-origin:0 162px;animation:bar{i} 10s ease-out infinite"/>')

    (OUT / "dashboard.svg").write_text(svg(W, H, "".join(css), "".join(body)), encoding="utf-8")


# ---------------------------------------------------------------- profile card
def build_profile_card():
    W, H = 920, 320
    avatar = (Path(__file__).parent / "assets" / ".avatar.b64").read_text().strip()
    phrases = ["Computer Engineer", "Backend · Python", "DevOps · Kubernetes · Docker",
               "CI/CD Pipelines · GitHub", "Clean Code · SDD", "Claude · Antigravity"]
    PCYCLE = len(phrases) * 3.0
    css = [
        f".name{{font-size:28px;font-weight:700;fill:{TEXT};font-family:-apple-system,'Segoe UI',sans-serif}}",
        f".typ{{font-size:15px;fill:{GREEN}}}",
        f".links{{font-size:12px;fill:{MUTED}}}",
        "@keyframes blink{50%{opacity:0}}",
        f".caret{{fill:{GREEN};animation:blink .9s steps(1) infinite}}",
        "@keyframes pulse{50%{opacity:.35}}",
        f".ccdot{{animation:pulse 2.2s ease-in-out infinite}}",
        f".cchead{{font-size:12px;fill:{ORANGE}}}",
        f".ccu{{font-size:11.5px;fill:{TEXT}}}",
        f".ccp{{font-size:11.5px;fill:{ORANGE}}}",
        f".cct{{font-size:11.5px;fill:{TEXT}}}",
        f".ccb{{font-size:11.5px;fill:{GREEN}}}",
        f".ccd{{font-size:11.5px;fill:{MUTED}}}",
        f".cok{{font-size:11.5px;fill:{GREEN}}}",
        f".ccs{{font-size:11px;fill:{ORANGE}}}",
        f".ccm{{font-size:11px;fill:{MUTED}}}",
    ]
    for i in range(len(phrases)):
        a = round(i / len(phrases) * 100, 2)
        b = round((i + 1) / len(phrases) * 100, 2)
        css.append(f"@keyframes ph{i}{{0%,{a}%{{opacity:0}}{a + .5}%,{b - .5}%{{opacity:1}}{b}%,100%{{opacity:0}}}}"
                   f".ph{i}{{animation:ph{i} {PCYCLE}s linear infinite}}")
    cc_lines = [
        ("ccu", "&#160;fix the flaky deploy and cut the API cold start", True),
        ("cct", "&#160;Read(k8s/deployment.yaml)", "b"),
        ("ccd", "&#160;&#160;&#8735; 142 lines", None),
        ("cct", "&#160;Edit(k8s/deployment.yaml)", "b"),
        ("ccd", "&#160;&#160;&#8735; readinessProbe.initialDelaySeconds: 30 &#8594; 5", None),
        ("cct", "&#160;Bash(pytest -q)", "b"),
        ("ccd", "&#160;&#160;&#8735; 247 passed in 12.4s", None),
        ("cct", "&#160;Bash(kubectl rollout status deploy/api)", "b"),
        ("ccd", "&#160;&#160;&#8735; deployment &#8220;api&#8221; successfully rolled out", None),
        ("cok", "&#160;&#10003; Cold start: 42s &#8594; 8s &#183; pipeline green", None),
    ]
    CCYCLE = 14.0
    for i in range(len(cc_lines)):
        t = round((0.9 + i * 0.62) / CCYCLE * 100, 2)
        css.append(f"@keyframes cl{i}{{0%,{t}%{{opacity:0}}{t + .5}%,96%{{opacity:1}}97%,100%{{opacity:0}}}}"
                   f".cl{i}{{animation:cl{i} {CCYCLE}s linear infinite}}")
    verbs = ["Beeboping", "Thinking", "Cooking", "Brewing", "Noodling", "Vibing"]
    VCYCLE = len(verbs) * 2.4
    for i in range(len(verbs)):
        a = round(i / len(verbs) * 100, 2)
        b = round((i + 1) / len(verbs) * 100, 2)
        css.append(f"@keyframes vb{i}{{0%,{a}%{{opacity:0}}{a + .5}%,{b - .5}%{{opacity:1}}{b}%,100%{{opacity:0}}}}"
                   f".vb{i}{{animation:vb{i} {VCYCLE}s linear infinite}}")

    body = [
        f'<rect width="{W}" height="{H}" rx="14" fill="{SURFACE}" stroke="{BORDER}"/>',
        f'<linearGradient id="topline" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="#3a89fe"/>'
        f'<stop offset="1" stop-color="{ORANGE}"/></linearGradient>',
        f'<rect width="{W}" height="3" fill="url(#topline)"/>',
    ]
    ax, ay = 210, 118
    body.append(f'<circle cx="{ax}" cy="{ay}" r="56" fill="none" stroke="{GREEN}" stroke-width="3" '
                f'stroke-dasharray="60 30" stroke-linecap="round">'
                f'<animateTransform attributeName="transform" type="rotate" from="0 {ax} {ay}" to="360 {ax} {ay}" '
                f'dur="8s" repeatCount="indefinite"/></circle>')
    body.append(f'<clipPath id="avc"><circle cx="{ax}" cy="{ay}" r="47"/></clipPath>')
    body.append(f'<image href="data:image/jpeg;base64,{avatar}" x="{ax - 47}" y="{ay - 47}" width="94" height="94" '
                f'clip-path="url(#avc)"/>')
    body.append(f'<text x="{ax}" y="208" text-anchor="middle" class="name">Fran Oberto</text>')
    for i, ph in enumerate(phrases):
        pw = len(ph) * 9
        body.append(f'<g class="ph{i}"><text x="{ax}" y="236" text-anchor="middle" class="typ">{ph}</text>'
                    f'<rect x="{ax + pw / 2 + 6}" y="222" width="8" height="16" class="caret"/></g>')
    body.append(f'<text x="{ax}" y="272" text-anchor="middle" class="links">in/franciscoobertozarazaga &#183; '
                f'franobertozarazaga@gmail.com</text>')

    cx0, cy0, cw, ch = 440, 24, 456, 272
    body.append(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="10" fill="#0d1420" stroke="{BORDER}"/>')
    body.append(f'<text x="{cx0 + 16}" y="{cy0 + 24}" class="cchead"><tspan class="ccdot">&#10035;</tspan> claude code</text>')
    ly = cy0 + 50
    for i, (cls, txt, bullet) in enumerate(cc_lines):
        prefix = f'<tspan class="ccp">&gt;</tspan>' if bullet is True else (
            f'<tspan class="ccb">&#9679;</tspan>' if bullet == "b" else "")
        body.append(f'<text x="{cx0 + 16}" y="{ly + i * 19}" class="{cls} cl{i}">{prefix}{txt}</text>')
    sy = cy0 + ch - 16
    body.append(f'<line x1="{cx0 + 12}" y1="{sy - 18}" x2="{cx0 + cw - 12}" y2="{sy - 18}" stroke="{BORDER}"/>')
    star_x = cx0 + 22
    body.append(f'<text x="{star_x}" y="{sy}" class="ccs" text-anchor="middle">&#10035;'
                f'<animateTransform attributeName="transform" type="rotate" from="0 {star_x} {sy - 4}" '
                f'to="360 {star_x} {sy - 4}" dur="1.6s" repeatCount="indefinite"/></text>')
    for i, v in enumerate(verbs):
        body.append(f'<text x="{cx0 + 32}" y="{sy}" class="ccs vb{i}">{v}&#8230;</text>')
    body.append(f'<text x="{cx0 + 128}" y="{sy}" class="ccm">(esc to interrupt &#183; &#8593; 3.1k tokens)</text>')

    (OUT / "profile-card.svg").write_text(svg(W, H, "".join(css), "".join(body)), encoding="utf-8")


if __name__ == "__main__":
    build_pipeline()
    build_terminal()
    build_htop()
    build_whale()
    build_dashboard()
    build_profile_card()
    print("assets generated:", sorted(p.name for p in OUT.glob("*.svg")))
