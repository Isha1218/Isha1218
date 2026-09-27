"""Builds the static art: hero banner, library shelf and snack buttons.  Run: python scripts/build_art.py"""
import random
from pathlib import Path

from art import FONT, MONO, SKY_DEFS, penguin, sky, svg

OUT = Path(__file__).resolve().parent.parent / "assets"


def hero():
    w, h = 900, 320
    rnd = random.Random(3)
    tagline = "penguins waddle, i build. same energy."
    cw, x0, y0 = 12, 58, 158                       # textLength pins every font to 12px/char
    steps = [i * cw for i in range(len(tagline) + 1)] + [len(tagline) * cw] * 24
    widths = ";".join(map(str, steps))
    cursor = ";".join(str(x0 + s + 2) for s in steps)
    snow = "".join(
        f'<circle class="snow" style="animation-duration:{rnd.uniform(7, 13):.1f}s;animation-delay:-{rnd.uniform(0, 13):.1f}s" '
        f'cx="{rnd.uniform(0, w):.0f}" cy="-6" r="{rnd.choice((1, 1.4, 1.8))}" fill="#fff" opacity=".8"/>'
        for _ in range(26))
    css = """
.aurora{filter:url(#glow);animation:drift 10s ease-in-out infinite alternate}
@keyframes drift{from{transform:translateX(-40px);opacity:.35}to{transform:translateX(40px);opacity:.75}}
.snow{animation:fall linear infinite}
@keyframes fall{to{transform:translate(-20px,340px)}}
.walk{animation:walk 17s linear infinite}
@keyframes walk{from{transform:translateX(-80px)}to{transform:translateX(990px)}}
.wobble{transform-box:fill-box;transform-origin:50% 100%;animation:wobble .42s ease-in-out infinite alternate}
@keyframes wobble{from{transform:rotate(-7deg)}to{transform:rotate(7deg)}}
.cursor{animation:cur 1s steps(1) infinite}@keyframes cur{50%{opacity:0}}
"""
    body = f"""<defs>{SKY_DEFS}
<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
<linearGradient id="au" x1="0" x2="1"><stop offset="0" stop-color="#2dd4bf" stop-opacity="0"/>
<stop offset=".35" stop-color="#2dd4bf"/><stop offset=".7" stop-color="#a78bfa"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/></linearGradient>
<clipPath id="type"><rect x="{x0}" y="{y0 - 22}" height="32" width="0"><animate attributeName="width" values="{widths}" calcMode="discrete" dur="7s" repeatCount="indefinite"/></rect></clipPath>
<clipPath id="frame"><rect width="{w}" height="{h}" rx="18"/></clipPath></defs>
<g clip-path="url(#frame)">{sky(w, h)}
<path class="aurora" d="M-60,110 C150,30 300,150 470,70 S760,20 960,90" stroke="url(#au)" stroke-width="46" fill="none"/>
<path class="aurora" style="animation-delay:-5s" d="M-60,60 C180,120 360,10 560,80 S800,120 960,40" stroke="url(#au)" stroke-width="26" fill="none" opacity=".6"/>
<circle cx="815" cy="62" r="24" fill="#fef9c3"/><circle cx="826" cy="55" r="22" fill="#0b1230"/>
<path d="M0,250 L90,200 L150,232 L240,178 L330,240 L900,240 L900,320 L0,320Z" fill="#1e3a66" opacity=".7"/>
<path d="M560,244 L640,196 L700,226 L760,188 L860,244Z" fill="#284a80" opacity=".8"/>
<path d="M0,262 Q220,248 450,258 T900,254 L900,320 L0,320Z" fill="#dbeafe"/>
<path d="M0,262 Q220,248 450,258 T900,254" stroke="#fff" stroke-width="3" fill="none"/>
<path d="M120,285 l40,6 M520,292 l55,-4 M700,280 l30,8" stroke="#bfdbfe" stroke-width="2"/>
<text x="{x0}" y="112" font-family="{FONT}" font-size="54" font-weight="800" fill="#f8fafc">hi, i'm ishita</text>
<text x="{x0}" y="{y0}" font-family="{MONO}" font-size="20" fill="#99f6e4" textLength="{len(tagline) * cw}" lengthAdjust="spacingAndGlyphs" clip-path="url(#type)">{tagline}</text>
<rect class="cursor" y="{y0 - 17}" width="10" height="21" fill="#99f6e4"><animate attributeName="x" values="{cursor}" calcMode="discrete" dur="7s" repeatCount="indefinite"/></rect>
<text x="{x0}" y="196" font-family="{FONT}" font-size="15" fill="#a5b4fc">teaching books to talk back · Flutter · Python · TypeScript</text>
<g transform="translate(772,266) scale(1.25)"><ellipse cx="0" cy="0" rx="34" ry="6" fill="#bfdbfe"/>{penguin("read", ("beanie",))}</g>
<g transform="translate(0,268)"><g class="walk"><g class="wobble">{penguin("idle", ("scarf",), carry=True)}</g></g></g>
{snow}</g>"""
    return svg(w, h, body, css, "hi, i'm ishita. penguins waddle, i build. same energy.")


BOOKS = [  # title, colour, width, height, dark text?
    ("BookBro", "#f472b6", 62, 214, True), ("Inkborne", "#7c3aed", 58, 200, False),
    ("Smart Ebook Reader", "#0ea5e9", 54, 222, True), ("Bookflix", "#ef4444", 60, 188, False),
    ("Aftertaste", "#22c55e", 64, 206, True), ("Upcycle AI", "#f59e0b", 56, 182, True),
    ("Idle Hands", "#14b8a6", 60, 198, True), ("Hey Ollie", "#6366f1", 58, 190, False),
    ("Vertex", "#e11d48", 54, 176, False),
]


def shelf():
    w, h, base = 900, 340, 296
    css = """
.pickme{animation:pick 6s ease-in-out infinite}@keyframes pick{0%,70%,100%{transform:translateY(0)}78%,90%{transform:translateY(-14px)}}
.wip{animation:tick 1.6s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:50% 0}
@keyframes tick{from{transform:rotate(-8deg)}to{transform:rotate(8deg)}}
.leaf{transform-box:fill-box;transform-origin:50% 100%;animation:sway 3s ease-in-out infinite alternate}
@keyframes sway{from{transform:rotate(-4deg)}to{transform:rotate(4deg)}}
"""
    books, x = [], 150
    for i, (t, c, bw, bh, dark) in enumerate(BOOKS):
        y, ink = base - bh, "#1e1b4b" if dark else "#f8fafc"
        cls = ' class="pickme"' if i == 0 else ""
        tag = ""
        if t == "Upcycle AI":
            tag = (f'<g class="wip"><path d="M{x + bw / 2},{y + 2} l0,14" stroke="#fde68a"/>'
                   f'<rect x="{x + bw / 2 - 17}" y="{y + 16}" width="34" height="16" rx="3" fill="#fde68a"/>'
                   f'<text x="{x + bw / 2}" y="{y + 28}" text-anchor="middle" font-family="{MONO}" font-size="10" '
                   f'font-weight="700" fill="#78350f">WIP</text></g>')
        books.append(
            f'<g{cls}><rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="4" fill="{c}"/>'
            f'<rect x="{x}" y="{y + 14}" width="{bw}" height="4" fill="{ink}" opacity=".25"/>'
            f'<rect x="{x}" y="{base - 20}" width="{bw}" height="4" fill="{ink}" opacity=".25"/>'
            f'<text transform="translate({x + bw / 2 + 5},{y + bh / 2}) rotate(-90)" text-anchor="middle" '
            f'font-family="{FONT}" font-size="15" font-weight="700" fill="{ink}">{t}</text>{tag}</g>')
        x += bw + 5
    body = f"""<defs><linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1230"/>
<stop offset="1" stop-color="#1f2a5a"/></linearGradient><clipPath id="frame"><rect width="{w}" height="{h}" rx="18"/></clipPath></defs>
<g clip-path="url(#frame)"><rect width="{w}" height="{h}" fill="url(#wall)"/>
<text x="36" y="46" font-family="{MONO}" font-size="13" letter-spacing="3" fill="#a5b4fc">THE ICEBERG LIBRARY</text>
<text x="36" y="70" font-family="{FONT}" font-size="15" fill="#cbd5e1">things i've built, shelved by vibe</text>
<g transform="translate(92,{base})"><path d="M-20,0 l4,-34 h32 l4,34z" fill="#c2410c"/><rect x="-22" y="-38" width="44" height="7" rx="2" fill="#ea580c"/>
<path class="leaf" d="M0,-38 C-4,-60 -24,-70 -30,-86 C-10,-80 -2,-64 0,-38Z" fill="#4ade80"/>
<path class="leaf" style="animation-delay:-1.5s" d="M0,-38 C4,-66 22,-78 30,-96 C32,-72 12,-56 0,-38Z" fill="#22c55e"/>
<path class="leaf" style="animation-delay:-.7s" d="M0,-38 C0,-70 -6,-90 2,-110 C12,-90 6,-66 0,-38Z" fill="#86efac"/></g>
{''.join(books)}
<g transform="translate({x + 64},{base}) scale(1.35)">{penguin("read", ("scarf",))}</g>
<rect x="24" y="{base}" width="{w - 48}" height="16" rx="3" fill="#a16207"/><rect x="24" y="{base}" width="{w - 48}" height="4" fill="#ca8a04"/>
<rect x="40" y="{base + 16}" width="{w - 80}" height="10" fill="#000" opacity=".25"/></g>"""
    return svg(w, h, body, css, "A bookshelf of Ishita's projects, with a penguin reading at the end.")


def button(kind, label, color):
    icons = {
        "fish": '<ellipse cx="0" cy="0" rx="10" ry="5.5" fill="#fff"/><path d="M8,0 l9,-6 l0,12z" fill="#fff"/><circle cx="-5" cy="-1" r="1.3" fill="{c}"/>',
        "krill": '<path d="M-10,4 q2,-12 14,-10 q7,2 6,8" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M-9,3 l-5,5 M-4,5 l-2,6 M1,5 l1,6" stroke="#fff" stroke-width="1.6"/>',
        "book": '<path d="M-13,-7 L0,-4 L13,-7 L13,8 L0,11 L-13,8Z" fill="#fff"/><path d="M0,-4 v15" stroke="{c}" stroke-width="1.5"/>',
        "snowball": '<circle r="9" fill="#fff"/><circle cx="-3" cy="-3" r="2.5" fill="{c}" opacity=".35"/><path d="M12,-8 l6,-3 M13,0 l7,0 M12,8 l6,3" stroke="#fff" stroke-width="2" stroke-linecap="round"/>',
    }
    body = (f'<rect width="210" height="52" rx="26" fill="{color}"/><rect x="2" y="2" width="206" height="24" rx="12" fill="#fff" opacity=".12"/>'
            f'<g transform="translate(34,26)">{icons[kind].format(c=color)}</g>'
            f'<text x="62" y="32" font-family="{FONT}" font-size="17" font-weight="700" fill="#fff">{label}</text>')
    return svg(210, 52, body, "", label)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "hero.svg").write_text(hero())
    (OUT / "shelf.svg").write_text(shelf())
    for kind, label, color in (("fish", "give a fish", "#0284c7"), ("krill", "toss krill", "#e11d48"),
                               ("book", "lend a book", "#7c3aed"), ("snowball", "throw a snowball", "#0f766e")):
        (OUT / f"btn-{kind}.svg").write_text(button(kind, label, color))
    print("built", sorted(p.name for p in OUT.glob("*.svg")))
