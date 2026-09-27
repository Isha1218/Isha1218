"""Builds assets/terminal.svg, a neofetch-style card.  Run: python3 scripts/build_terminal.py"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "terminal.svg"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
CH = 8.4  # pinned width per character at 14px, so every font lines up the same

LOGO = [
    "██╗███╗   ███╗",
    "██║████╗ ████║",
    "██║██╔████╔██║",
    "██║██║╚██╔╝██║",
    "██║██║ ╚═╝ ██║",
    "╚═╝╚═╝     ╚═╝",
]
INFO = [  # (key, value); key None = continuation line
    ("Education", "CS @ University of Washington, class of '28"),
    ("Now", "ML research, forecasting Arctic sea ice"),
    (None, "teaching assistant, UW CSE"),
    ("Prev", "SWE intern @ Affirm, pricing platform"),
    (None, "SWE intern @ Chipp, fintech"),
    ("Builds", "AI products, full-stack apps, ML models"),
    ("Languages", "Python · Go · JavaScript · Java · Dart"),
    ("Tools", "React · Flutter · FastAPI · PyTorch · AWS"),
    ("Contact", "linkedin.com/in/ishita-mundra"),
]
SWATCHES = ["#ff7b72", "#ffa657", "#e3b341", "#7ee787", "#79c0ff", "#d2a8ff", "#f778ba", "#e6edf3"]


def text(x, y, s, fill, cls="", extra="", ch=CH):
    return (f'<text x="{x}" y="{y}" fill="{fill}" {cls} {extra} xml:space="preserve" '
            f'textLength="{len(s) * ch:.1f}" lengthAdjust="spacingAndGlyphs">{escape(s)}</text>')


def build():
    w, h = 900, 430
    cmd = "neofetch --user ishita"
    x0, y0, lh = 34, 78, 25
    parts, n = [], 0

    def show(el):  # every output line fades in, one after the other
        nonlocal n
        n += 1
        return f'<g class="line" style="animation-delay:{1.35 + n * .09:.2f}s">{el}</g>'

    for i, row in enumerate(LOGO):
        parts.append(show(text(x0 + 10, y0 + 58 + i * 19.6, row, "url(#grad)", extra='style="font-size:17px"', ch=10.2)))
    kx, vx, y = 250, 360, y0 + 40
    parts.append(show(text(kx, y, "ishita", "#79c0ff", extra='font-weight="700"')
                      + text(kx + 6 * CH, y, "@", "#e6edf3")
                      + text(kx + 7 * CH, y, "mundra", "#79c0ff", extra='font-weight="700"')))
    y += lh * .7
    parts.append(show(f'<rect x="{kx}" y="{y - 6}" width="{13 * CH}" height="1.5" fill="#484f58"/>'))
    y += lh * .6
    for k, v in INFO:
        el = (text(kx, y, k, "#d2a8ff", extra='font-weight="700"') if k else "") + text(vx, y, v, "#e6edf3")
        parts.append(show(el))
        y += lh
    y += 4
    parts.append(show("".join(f'<rect x="{kx + i * 30}" y="{y - 14}" width="30" height="16" fill="{c}"/>'
                              for i, c in enumerate(SWATCHES))))
    py = h - 30
    typed = len(cmd)
    css = f"""
text{{font-family:{MONO};font-size:14px}}
.line{{opacity:0;animation:in .25s ease-out forwards}}
@keyframes in{{to{{opacity:1}}}}
.cursor{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.done{{opacity:0;animation:in 0s {1.5 + n * .09:.2f}s forwards}}
"""
    body = f"""<defs>
<linearGradient id="grad" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{x0 + 10 + 14 * 10.2}" y2="0">
<stop offset="0" stop-color="#7ee787"/><stop offset=".5" stop-color="#79c0ff"/><stop offset="1" stop-color="#d2a8ff"/></linearGradient>
<clipPath id="typed"><rect x="{x0 + 2 * CH}" y="{y0 - 18}" height="26" width="0">
<animate attributeName="width" begin="0.2s" dur="1s" fill="freeze" calcMode="discrete" values="{';'.join(str(round(i * CH, 1)) for i in range(typed + 1))}"/></rect></clipPath></defs>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="#0d1117" stroke="#30363d"/>
<path d="M.5,12.5 a12,12 0 0 1 12,-12 h{w - 25} a12,12 0 0 1 12,12 v24 h-{w - 1}z" fill="#161b22"/>
<line x1=".5" y1="36.5" x2="{w - .5}" y2="36.5" stroke="#30363d"/>
<circle cx="22" cy="18.5" r="6" fill="#ff5f57"/><circle cx="42" cy="18.5" r="6" fill="#febc2e"/><circle cx="62" cy="18.5" r="6" fill="#28c840"/>
<text x="{w / 2}" y="23" fill="#8b949e" text-anchor="middle" style="font-size:12px">ishita@github: ~</text>
{text(x0, y0, "$", "#7ee787")}
<g clip-path="url(#typed)">{text(x0 + 2 * CH, y0, cmd, "#e6edf3")}</g>
{''.join(parts)}
<g class="done">{text(x0, py, "$", "#7ee787")}<rect class="cursor" x="{x0 + 2 * CH}" y="{py - 13}" width="{CH}" height="17" fill="#e6edf3"/></g>"""
    alt = ("Terminal window running neofetch for Ishita Mundra. "
           + " ".join(f"{k or ''} {v}." for k, v in INFO))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="{escape(alt)}"><title>{escape(alt)}</title><style>{css}</style>{body}</svg>\n')


if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(build())
    print("wrote", OUT)
