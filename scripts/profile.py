"""Draws the profile art and runs the fish feeder.

  python3 scripts/profile.py            redraw everything from data/fish.json
  python3 scripts/profile.py --feed     (in the Action) count a fish from ISSUE_USER, write reply.md
"""
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS, STATE, README = ROOT / "assets", ROOT / "data/fish.json", ROOT / "README.md"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
DAILY_LIMIT = 10

TAGS = ["CS @ UW '28", "ex-Affirm", "ex-Chipp", "ML research", "AI apps", "Flutter", "Python"]
PROJECTS = [  # repo, title, one-liner, stack
    ("BookBroApp", "BookBro", "a spoiler-free AI companion for whatever you're reading", ["React", "LangChain", "FastAPI"]),
    ("aftertaste", "Aftertaste", "the carbon footprint of your food, from one photo", ["Flutter", "PyTorch", "Flask"]),
    ("bookflix", "Bookflix", "your next book, picked from the ones you loved", ["Flutter", "Flask", "Firebase"]),
]
THEMES = {
    "light": dict(ink="#1f2328", muted="#656d76", line="#d0d7de", body="#1f2328", belly="#ffffff", btn="#f6f8fa", pill="#e7ecf0"),
    "dark": dict(ink="#e6edf3", muted="#8d96a0", line="#3d444d", body="#3d444d", belly="#f0f3f6", btn="#21262d", pill="#2f363e"),
}
ORANGE, FISH = "#f59e0b", "#38bdf8"


def svg(w, h, body, css, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="{escape(label)}"><title>{escape(label)}</title><style>{css}</style>{body}</svg>\n')


def penguin(t):
    """Chubby flat penguin, feet at (0,0), ~105 tall. A fish arcs into its beak every few seconds."""
    return f"""<g class="gulp">
<ellipse cx="-43" cy="-40" rx="8" ry="17" fill="{t['body']}" transform="rotate(28 -43 -40)"/>
<ellipse cx="43" cy="-40" rx="8" ry="17" fill="{t['body']}" transform="rotate(-28 43 -40)"/>
<ellipse cx="0" cy="-50" rx="46" ry="50" fill="{t['body']}"/>
<path d="M-3,-99 q3,-12 12,-8 q-7,1 -6,8z" fill="{t['body']}"/>
<g fill="{t['belly']}"><circle cx="-14" cy="-62" r="20"/><circle cx="14" cy="-62" r="20"/><ellipse cx="0" cy="-34" rx="33" ry="31"/></g>
<g class="blink"><ellipse cx="-14" cy="-63" rx="6.5" ry="7.5" fill="#1f2328"/><ellipse cx="14" cy="-63" rx="6.5" ry="7.5" fill="#1f2328"/></g>
<circle cx="-11.5" cy="-66" r="2.4" fill="#fff"/><circle cx="16.5" cy="-66" r="2.4" fill="#fff"/>
<ellipse cx="-26" cy="-51" rx="6.5" ry="3.8" fill="#ffadbd" opacity=".85"/><ellipse cx="26" cy="-51" rx="6.5" ry="3.8" fill="#ffadbd" opacity=".85"/>
<path d="M-6,-55 q6,-4 12,0 q-6,7 -12,0z" fill="{ORANGE}"/>
<ellipse cx="-15" cy="-2" rx="11" ry="4.5" fill="{ORANGE}"/><ellipse cx="15" cy="-2" rx="11" ry="4.5" fill="{ORANGE}"/></g>
<g class="fish"><ellipse cx="0" cy="0" rx="10" ry="5" fill="{FISH}"/><path d="M8,0 l8,-5.5 v11z" fill="{FISH}"/></g>"""


PENGUIN_CSS = """
.gulp{transform-box:fill-box;transform-origin:50% 100%;animation:gulp 4s ease-in-out infinite}
@keyframes gulp{0%,52%,68%,100%{transform:scale(1)}58%{transform:scale(1.05,.93)}}
.blink{transform-box:fill-box;transform-origin:center;animation:blink 4s infinite}
@keyframes blink{0%,88%,100%{transform:scaleY(1)}92%{transform:scaleY(.1)}}
.fish{animation:toss 4s ease-in infinite}
@keyframes toss{0%{transform:translate(90px,-20px) rotate(0);opacity:0}
10%{opacity:1}30%{transform:translate(60px,-120px) rotate(-140deg)}
52%{transform:translate(4px,-56px) rotate(-200deg);opacity:1}54%,100%{transform:translate(4px,-56px);opacity:0}}
@media (prefers-reduced-motion:reduce){.gulp,.blink,.fish{animation:none}.fish{opacity:0}}
"""


def header(t, st):
    w, h, x = 880, 176, 170
    pills, px = [], x
    for tag in TAGS:
        tw = len(tag) * 7.8 + 22
        pills.append(f'<rect x="{px}" y="96" width="{tw:.0f}" height="26" rx="13" fill="none" stroke="{t["line"]}"/>'
                     f'<text x="{px + 11}" y="113.5" font-family="{MONO}" font-size="13" fill="{t["ink"]}" '
                     f'textLength="{len(tag) * 7.8:.1f}" lengthAdjust="spacingAndGlyphs">{escape(tag)}</text>')
        px += tw + 8
    n, last = st["count"], st.get("last")
    fed = f"{n} fish eaten" + (f" · last one from @{last}" if last else " · be the first")
    body = f"""<g transform="translate(80,158)">{penguin(t)}</g>
<text x="{x}" y="70" font-family="{SANS}" font-size="40" font-weight="700" fill="{t['ink']}">Ishita Mundra</text>
{''.join(pills)}
<text x="{x}" y="156" font-family="{MONO}" font-size="13" fill="{t['muted']}">{escape(fed)}</text>"""
    return svg(w, h, body, PENGUIN_CSS, f"Ishita Mundra. {', '.join(TAGS)}. A penguin catching a fish; {fed}.")


def card(repo, title, blurb, stack):
    w, h = 300, 150
    bx, tags = 20, []
    for s in stack:
        tw = len(s) * 7.2 + 18
        tags.append(f'<rect x="{bx}" y="110" width="{tw:.0f}" height="22" rx="11" fill="#21262d"/>'
                    f'<text x="{bx + 9}" y="125" font-family="{MONO}" font-size="12" fill="#c9d1d9" '
                    f'textLength="{len(s) * 7.2:.1f}" lengthAdjust="spacingAndGlyphs">{s}</text>')
        bx += tw + 6
    words, lines, cur = blurb.split(), [], ""
    for wd in words:  # wrap at ~36 chars
        if len(cur) + len(wd) + 1 > 36:
            lines.append(cur); cur = wd
        else:
            cur = f"{cur} {wd}".strip()
    lines.append(cur)
    text = "".join(f'<text x="20" y="{70 + i * 19}" font-family="{SANS}" font-size="14" fill="#9198a1">{escape(l)}</text>'
                   for i, l in enumerate(lines[:2]))
    body = f"""<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="10" fill="#0d1117" stroke="#30363d"/>
<g transform="translate(20,26)" fill="#9198a1"><path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"/></g>
<text x="44" y="39" font-family="{SANS}" font-size="17" font-weight="700" fill="{FISH}">{title}</text>
{text}{''.join(tags)}"""
    return svg(w, h, body, "", f"{title}: {blurb}. Built with {', '.join(stack)}.")


def button(t):
    """A GitHub-style button, like the Follow button."""
    label = "Feed the penguin"
    lw = len(label) * 7.6
    w = 38 + lw + 14
    body = (f'<rect x=".5" y=".5" width="{w - 1:.0f}" height="31" rx="6" fill="{t["btn"]}" stroke="{t["line"]}"/>'
            f'<g transform="translate(20,16)"><ellipse rx="7.5" ry="4" fill="{t["ink"]}"/><path d="M6,0 l6,-4.5 v9z" fill="{t["ink"]}"/>'
            f'<circle cx="-3.5" cy="-.8" r="1.1" fill="{t["btn"]}"/></g>'
            f'<text x="38" y="21" font-family="{SANS}" font-size="14" font-weight="600" fill="{t["ink"]}" '
            f'textLength="{lw:.1f}" lengthAdjust="spacingAndGlyphs">{label}</text>')
    return svg(round(w), 32, body, "", "Feed the penguin a fish")


def splice(text, n, v):
    issue = "https://github.com/Isha1218/Isha1218/issues/new?title=feed+the+penguin+%F0%9F%90%9F&body=hit+Submit+and+the+penguin+gets+a+fish."
    return re.sub(r"(<!-- HEADER:START -->).*?(<!-- HEADER:END -->)", lambda m: f"""{m.group(1)}
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark-{v}.svg">
  <img src="assets/header-light-{v}.svg" width="100%" alt="Ishita Mundra. {', '.join(TAGS)}. A penguin catching a fish; {n} fish eaten so far.">
</picture>

<a href="{issue}"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/feed-dark-{v}.svg">
  <img src="assets/feed-light-{v}.svg" height="32" alt="Feed the penguin a fish">
</picture></a>
{m.group(2)}""", text, flags=re.S)


def render(st):
    ASSETS.mkdir(exist_ok=True)
    # Each version of the header gets its own filename: GitHub's image CDN ignores query strings
    # and caches by path, so a new name is the only way visitors see the new art right away.
    svgs = {f"header-{n}": header(t, st) for n, t in THEMES.items()}
    svgs.update({f"feed-{n}": button(t) for n, t in THEMES.items()})
    v = hashlib.sha1("".join(svgs.values()).encode()).hexdigest()[:8]
    for old in [*ASSETS.glob("header-*.svg"), *ASSETS.glob("feed-*.svg")]:
        old.unlink()
    for name, body in svgs.items():
        (ASSETS / f"{name}-{v}.svg").write_text(body)
    for p in PROJECTS:
        (ASSETS / f"card-{p[0].lower()}.svg").write_text(card(*p))
    README.write_text(splice(README.read_text(), st["count"], v))


def feed(st, user):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    day = st.setdefault("today", {"date": today, "users": {}})
    if day["date"] != today:
        st["today"] = day = {"date": today, "users": {}}
    if day["users"].get(user, 0) >= DAILY_LIMIT:
        return False, "the penguin is full for today. come back tomorrow 🐧"
    day["users"][user] = day["users"].get(user, 0) + 1
    st["count"] += 1
    st["last"] = user
    return True, f"🐟 fish #{st['count']} delivered. thanks @{user}! 🐧"


def main():
    st = json.loads(STATE.read_text()) if STATE.exists() else {"count": 0, "last": None}
    if "--feed" in sys.argv:
        user = re.sub(r"[^A-Za-z0-9-]", "", os.environ.get("ISSUE_USER", ""))[:39]
        changed, reply = feed(st, user)
        (ROOT / "reply.md").write_text(reply)
        if not changed:
            return
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(st, indent=1) + "\n")
    render(st)


if __name__ == "__main__":
    main()
