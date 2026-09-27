"""Pip the penguin. Run by .github/workflows/pip.yml when someone opens a `pip|<snack>` issue.

Reads ISSUE_TITLE / ISSUE_USER from the environment, updates data/pip.json, redraws
assets/pip.svg, rewrites the PIP blocks in README.md and writes the issue reply to reply.md.
`python scripts/pip.py --render` just redraws from the current state.
"""
import json
import os
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

from art import FONT, MONO, SKY_DEFS, penguin, sky, svg

ROOT = Path(__file__).resolve().parent.parent
STATE, IMG, README = ROOT / "data/pip.json", ROOT / "assets/pip.svg", ROOT / "README.md"
REPO = "Isha1218/Isha1218"
DAILY_LIMIT = 10

SNACKS = {  # snack: (pose, emoji, past-tense verb, reactions)
    "fish": ("eat", "🐟", "gave Pip a fish", ["*nom nom* that was a GOOD fish", "fish!! my favourite food group",
                                              "10/10 fish. would eat again", "crunchy. salty. perfect."]),
    "krill": ("happy", "🦐", "tossed Pip some krill", ["krill!! tiny but mighty", "a whole handful?? for me??",
                                                     "krill is just ocean confetti", "happy dance activated"]),
    "book": ("read", "📖", "lent Pip a book", ["ooh a new book. do not disturb", "no spoilers please!!",
                                            "adding this to my tbr pile", "one more chapter. ok two."]),
    "snowball": ("bonk", "❄️", "threw a snowball at Pip", ["HEY. ...okay rematch", "you have declared war",
                                                          "i'm not crying, it's just snow", "*plots revenge*"]),
}
LEVELS = [(0, "hatchling", ()), (5, "waddler", ("scarf",)), (15, "ice explorer", ("scarf", "beanie")),
          (40, "floe captain", ("scarf", "beanie", "shades")), (100, "emperor", ("scarf", "shades", "crown"))]
FACTS = [
    "a group of penguins in the water is called a raft.",
    "emperor penguin dads balance the egg on their feet for about two months of antarctic winter.",
    "gentoo penguins are the fastest-swimming birds, reaching around 35 km/h.",
    "penguins can drink seawater: a gland above their eyes filters out the salt.",
    "adélie and gentoo penguins court each other with carefully chosen pebbles.",
    "the black back and white belly are camouflage called countershading.",
    "emperor penguins can dive deeper than 500 metres.",
    "the smallest penguin, the little penguin, is only about 33 cm tall.",
    "galápagos penguins live right on the equator.",
    "penguins 'toboggan' — sliding on their bellies to save energy.",
]


def new_state():
    return {"counts": {k: 0 for k in SNACKS}, "feeders": {}, "log": [], "today": {"date": "", "users": {}},
            "last": None}


def level(total):
    i = max(i for i, (need, _, _) in enumerate(LEVELS) if total >= need)
    nxt = LEVELS[i + 1][0] if i + 1 < len(LEVELS) else None
    return i, LEVELS[i], nxt


def fit(text, room=246):
    """Squeeze a line into the bubble if it's too long for the average glyph width."""
    return f' textLength="{room}" lengthAdjust="spacingAndGlyphs"' if len(text) * 8.4 > room else ""


def render(st):
    total = sum(st["counts"].values())
    i, (need, name, acc), nxt = level(total)
    last = st["last"]
    pose = SNACKS[last["snack"]][0] if last else "idle"
    if last:
        who = last["user"] if len(last["user"]) <= 18 else last["user"][:17] + "…"
        line1, line2 = last["reaction"], f"— thanks @{who}"
    else:
        line1, line2 = "hungry. nobody has fed me yet :(", "— click a button below!"
    prog = 1 if nxt is None else (total - need) / (nxt - need)
    rows = "".join(
        f'<text x="604" y="{112 + n * 26}" font-family="{FONT}" font-size="15" fill="#cbd5e1">{SNACKS[k][1]}  {k}</text>'
        f'<text x="860" y="{112 + n * 26}" text-anchor="end" font-family="{MONO}" font-size="15" fill="#f8fafc">{st["counts"][k]}</text>'
        for n, k in enumerate(SNACKS))
    to_next = "max level. bow down." if nxt is None else f"{nxt - total} snacks to {LEVELS[i + 1][1]}"
    body = f"""<defs>{SKY_DEFS}<clipPath id="frame"><rect width="900" height="290" rx="18"/></clipPath></defs>
<g clip-path="url(#frame)">{sky(900, 290, seed=11, stars=28)}
<path d="M0,238 Q200,212 430,236 T900,232 L900,290 L0,290Z" fill="#dbeafe"/>
<g transform="translate(90,236)"><path d="M-46,0 A46,46 0 0 1 46,0Z" fill="#f1f5f9"/><path d="M-14,0 A14,16 0 0 1 14,0Z" fill="#1e3a66"/>
<path d="M-40,-20 h80 M-30,-36 h60 M-10,0 v-20 M20,-20 v-16 M-18,-36 v-8" stroke="#cbd5e1" stroke-width="1.5"/></g>
<g transform="translate(230,240) scale(2.3)"><g class="bob">{penguin(pose, acc)}</g></g>
<path d="M312,112 l-18,26 l34,-14z" fill="#f8fafc"/>
<rect x="296" y="44" width="282" height="74" rx="16" fill="#f8fafc"/>
<text x="318" y="76" font-family="{FONT}" font-size="15" font-weight="700" fill="#0f172a"{fit(line1)}>{escape(line1)}</text>
<text x="318" y="100" font-family="{FONT}" font-size="14" fill="#475569">{escape(line2)}</text>
<rect x="588" y="30" width="290" height="236" rx="14" fill="#0b1230" opacity=".75"/>
<text x="604" y="60" font-family="{MONO}" font-size="12" letter-spacing="3" fill="#a5b4fc">PIP · LV {i + 1} · {name.upper()}</text>
<text x="604" y="84" font-family="{FONT}" font-size="13" fill="#94a3b8">{total} snacks from {len(st["feeders"])} visitors</text>
{rows}
<rect x="604" y="226" width="256" height="10" rx="5" fill="#1e293b"/>
<rect x="604" y="226" width="{max(10, 256 * prog):.0f}" height="10" rx="5" fill="#2dd4bf"/>
<text x="604" y="254" font-family="{FONT}" font-size="12" fill="#94a3b8">{escape(to_next)}</text></g>"""
    return svg(900, 290, body, "", f"Pip the penguin, level {i + 1} {name}. {line1} {line2}")


def splice(text, tag, content):
    return re.sub(rf"(<!-- PIP:{tag}:START -->).*?(<!-- PIP:{tag}:END -->)",
                  lambda m: f"{m.group(1)}\n{content}\n{m.group(2)}", text, flags=re.S)


def write_readme(st):
    total = sum(st["counts"].values())
    img = (f'<p align="center"><img src="assets/pip.svg?v={total}" width="100%" '
           f'alt="Pip the penguin, who has eaten {total} snacks so far"></p>')
    log = "\n".join(f"- `{e['date']}` {SNACKS[e['snack']][1]} **@{e['user']}** {SNACKS[e['snack']][2]}"
                    for e in st["log"][:6]) or "_nobody yet. be the first!_"
    top = sorted(st["feeders"].items(), key=lambda kv: -kv[1])[:5]
    board = " · ".join(f"{m} **@{u}** ({n})" for m, (u, n) in zip("🥇🥈🥉🏅🏅", top)) or "_the podium is empty_"
    text = README.read_text()
    for tag, content in (("IMG", img), ("LOG", log), ("BOARD", board)):
        text = splice(text, tag, content)
    README.write_text(text)


def feed(st, title, user):
    snack = title.split("|", 1)[1].strip().lower() if "|" in title else ""
    if snack not in SNACKS:
        return False, "pip squints at this. pip only accepts `fish`, `krill`, `book` or `snowball`."
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if st["today"]["date"] != today:
        st["today"] = {"date": today, "users": {}}
    if st["today"]["users"].get(user, 0) >= DAILY_LIMIT:
        return False, "pip is stuffed 🫃 and has waddled off for a nap. come back tomorrow!"
    st["today"]["users"][user] = st["today"]["users"].get(user, 0) + 1
    before = level(sum(st["counts"].values()))[0]
    st["counts"][snack] += 1
    st["feeders"][user] = st["feeders"].get(user, 0) + 1
    reaction = random.choice(SNACKS[snack][3])
    st["last"] = {"user": user, "snack": snack, "reaction": reaction}
    st["log"] = [{"date": today, "user": user, "snack": snack}] + st["log"][:49]
    i, (_, name, _), _ = level(sum(st["counts"].values()))
    up = f"\n\n🎉 **LEVEL UP!** you just turned pip into a **{name}**." if i > before else ""
    return True, (f"> {reaction}\n\n— pip 🐧{up}\n\nyour snack will show up on "
                  f"[the profile](https://github.com/{REPO.split('/')[0]}) in a few seconds.\n\n"
                  f"**penguin fact:** {random.choice(FACTS)}")


def main():
    st = json.loads(STATE.read_text()) if STATE.exists() else new_state()
    if "--render" not in sys.argv:
        user = re.sub(r"[^A-Za-z0-9-]", "", os.environ.get("ISSUE_USER", ""))[:39]
        changed, reply = feed(st, os.environ.get("ISSUE_TITLE", ""), user)
        (ROOT / "reply.md").write_text(reply)
        if not changed:
            return
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(st, indent=1) + "\n")
    IMG.write_text(render(st))
    write_readme(st)


if __name__ == "__main__":
    main()
