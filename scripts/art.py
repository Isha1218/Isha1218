"""Shared SVG pieces: the penguin, the night sky, and small helpers.

Every penguin is drawn around (0, 0) = the point between its feet, ~64 units tall.
"""
import random
from xml.sax.saxutils import escape

BODY, BELLY, ORANGE, CHEEK = "#1e293b", "#f8fafc", "#fb923c", "#fda4af"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

# Animations shared by every scene. transform-box makes rotations pivot on the element itself.
BASE_CSS = """
.blink{transform-box:fill-box;transform-origin:center;animation:blink 5s infinite}
@keyframes blink{0%,94%,100%{transform:scaleY(1)}97%{transform:scaleY(.1)}}
.twinkle{animation:twinkle 3s ease-in-out infinite alternate}
@keyframes twinkle{from{opacity:.15}to{opacity:.9}}
.page{transform-box:fill-box;transform-origin:0% 50%;animation:flip 3.2s ease-in-out infinite}
@keyframes flip{0%,70%{transform:scaleX(1)}85%{transform:scaleX(0)}100%{transform:scaleX(-1)}}
.heart{animation:rise 2.4s ease-out infinite}
@keyframes rise{0%{transform:translateY(0);opacity:0}20%{opacity:1}100%{transform:translateY(-18px);opacity:0}}
.bob{animation:bob 2.2s ease-in-out infinite alternate}
@keyframes bob{to{transform:translateY(-3px)}}
"""


def eyes(pose):
    if pose == "happy":
        return ('<path d="M-9,-50 q3,-4 6,0 M3,-50 q3,-4 6,0" stroke="#f8fafc" '
                'stroke-width="2" fill="none" stroke-linecap="round"/>')
    if pose == "bonk":
        return ('<path d="M-9,-53 l5,3 l-5,3 M9,-53 l-5,3 l5,3" stroke="#f8fafc" '
                'stroke-width="1.8" fill="none" stroke-linecap="round"/>')
    return ('<g class="blink"><circle cx="-6" cy="-50" r="3.4" fill="#f8fafc"/>'
            '<circle cx="6" cy="-50" r="3.4" fill="#f8fafc"/>'
            '<circle cx="-5.3" cy="-49.6" r="1.9" fill="#0f172a"/>'
            '<circle cx="6.7" cy="-49.6" r="1.9" fill="#0f172a"/></g>')


OPEN_BOOK = ('<g transform="translate(0,-20)">'
             '<path d="M-17,-9 L0,-5 L17,-9 L17,9 L0,13 L-17,9Z" fill="#f472b6"/>'
             '<path d="M-15,-7 L0,-3.5 L0,10.5 L-15,7Z" fill="#fff7ed"/>'
             '<path class="page" d="M0,-3.5 L15,-7 L15,7 L0,10.5Z" fill="#fffbeb" stroke="#fde68a" stroke-width=".5"/>'
             '</g>')


def penguin(pose="idle", acc=(), carry=False):
    """pose: idle | happy | eat | read | bonk.  acc: any of scarf, beanie, shades, crown."""
    p = [f'<ellipse cx="0" cy="-32" rx="22" ry="31" fill="{BODY}"/>',
         f'<ellipse cx="0" cy="-23" rx="15.5" ry="20" fill="{BELLY}"/>',
         f'<ellipse cx="-8" cy="-1" rx="8" ry="3.5" fill="{ORANGE}"/>',
         f'<ellipse cx="8" cy="-1" rx="8" ry="3.5" fill="{ORANGE}"/>',
         f'<circle cx="-12" cy="-42" r="3" fill="{CHEEK}" opacity=".7"/>',
         f'<circle cx="12" cy="-42" r="3" fill="{CHEEK}" opacity=".7"/>',
         eyes(pose),
         f'<path d="M-4.5,-45 L4.5,-45 L0,-38.5Z" fill="{ORANGE}"/>']
    if "scarf" in acc:
        p.append('<path d="M-20,-37 q20,8 40,0 l0,6 q-20,8 -40,0z" fill="#ef4444"/>'
                 '<rect x="7" y="-33" width="7" height="15" rx="2" fill="#dc2626" transform="rotate(-12 10 -33)"/>')
    if pose == "read":
        p.append(OPEN_BOOK)
        p.append(f'<ellipse cx="-17" cy="-24" rx="6" ry="13" fill="{BODY}" transform="rotate(-35 -17 -24)"/>'
                 f'<ellipse cx="17" cy="-24" rx="6" ry="13" fill="{BODY}" transform="rotate(35 17 -24)"/>'
                 '<g fill="none" stroke="#fbbf24" stroke-width="1.4"><circle cx="-6" cy="-50" r="4.8"/>'
                 '<circle cx="6" cy="-50" r="4.8"/><path d="M-1.2,-50 h2.4"/></g>')
    else:
        p.append(f'<ellipse cx="-21" cy="-29" rx="6" ry="15" fill="{BODY}" transform="rotate(18 -21 -29)"/>'
                 f'<ellipse cx="21" cy="-29" rx="6" ry="15" fill="{BODY}" transform="rotate(-18 21 -29)"/>')
    if carry:  # closed book tucked under the right flipper
        p.append('<rect x="17" y="-36" width="11" height="15" rx="1.5" fill="#f472b6" transform="rotate(-18 22 -28)"/>'
                 '<rect x="18.5" y="-35" width="2" height="13" fill="#fff7ed" transform="rotate(-18 22 -28)"/>')
    if "shades" in acc and pose != "read":
        p.append('<path d="M-12,-53 h24 v3 q-2,6 -7,6 q-4,0 -5,-5 q-1,5 -5,5 q-5,0 -7,-6z" fill="#0f172a"/>'
                 '<path d="M-9,-51 l3,0" stroke="#64748b" stroke-width="1"/>')
    if "crown" in acc:
        p.append('<path d="M-13,-59 l0,-14 l7,7 l6,-10 l6,10 l7,-7 l0,14z" fill="#facc15" stroke="#ca8a04"/>'
                 '<circle cx="0" cy="-64" r="2" fill="#ef4444"/>')
    elif "beanie" in acc:
        p.append('<path d="M-17,-58 q17,-25 34,0z" fill="#38bdf8"/>'
                 '<rect x="-19" y="-62" width="38" height="7" rx="3.5" fill="#e0f2fe"/>'
                 '<circle cx="0" cy="-79" r="5" fill="#e0f2fe"/>')
    if pose == "eat":
        p.append('<g transform="translate(3,-41) rotate(-15)"><ellipse cx="7" cy="0" rx="7.5" ry="3.6" fill="#60a5fa"/>'
                 '<path d="M13,0 l7,-4.5 l0,9z" fill="#3b82f6"/><circle cx="3" cy="-.8" r=".9" fill="#0f172a"/></g>')
    if pose == "happy":
        for x, d in ((-22, 0), (24, 1.2)):
            p.append(f'<path class="heart" style="animation-delay:{d}s" transform="translate({x},-66)" '
                     'd="M0,3 C-6,-3 -3,-7 0,-3 C3,-7 6,-3 0,3Z" fill="#fb7185"/>')
    if pose == "bonk":
        p.append('<g fill="#f8fafc"><circle cx="4" cy="-62" r="8"/><circle cx="-5" cy="-60" r="6"/>'
                 '<circle cx="13" cy="-58" r="4"/><circle cx="-13" cy="-56" r="2.5"/></g>'
                 '<path d="M-24,-70 l2,4 4,1 -4,1 -2,4 -2,-4 -4,-1 4,-1z M26,-66 l1.5,3 3,1 -3,1 -1.5,3 -1.5,-3 -3,-1 3,-1z" fill="#fde047"/>')
    return "<g>" + "".join(p) + "</g>"


def sky(w, h, seed=7, stars=40):
    rnd = random.Random(seed)
    s = [f'<rect width="{w}" height="{h}" rx="18" fill="url(#sky)"/>']
    for _ in range(stars):
        x, y, r = rnd.uniform(10, w - 10), rnd.uniform(8, h * .55), rnd.choice((.8, 1, 1.2, 1.6))
        s.append(f'<circle class="twinkle" style="animation-delay:-{rnd.uniform(0, 3):.1f}s" '
                 f'cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff"/>')
    return "".join(s)


SKY_DEFS = ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#070b1f"/><stop offset=".6" stop-color="#15204a"/>'
            '<stop offset="1" stop-color="#2b3d73"/></linearGradient>')


def svg(w, h, body, css="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
            f'<style>{BASE_CSS}{css}</style>{body}</svg>\n')
