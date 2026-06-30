#!/usr/bin/env python3
"""Generate circular SVG resource icons for Wingspan-style food tokens.

One SVG per food kind:
  invertebrate, seed, fish, fruit, rodent, nectar

Each is a colored circle (per-kind palette) with a simple symbolic icon
centered inside. Designs are generic geometric primitives — basic
silhouettes intended as functional resource indicators, not reproducing
any commercial token artwork.

Output:  <repo>/icons/<kind>.svg
Convert to PNG via the companion Nix flake (see flake.nix) or run
rsvg-convert / inkscape directly.

Stdlib only — no external deps.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR   = REPO_ROOT / "icons"

SIZE   = 256
CENTER = SIZE // 2
RADIUS = SIZE // 2 - 6

COLORS = {
    "invertebrate": "#FF7390",
    "seed":         "#FFD94D",
    "fish":         "#4080FF",
    "fruit":        "#FF8033",
    "rodent":       "#8C6648",
    "nectar":       "#F259F2",
}
ICON_FILL = "#1a1a2e"


def fish_icon():
    return f'''
<ellipse cx="{CENTER-12}" cy="{CENTER}" rx="60" ry="30" fill="{ICON_FILL}"/>
<polygon points="{CENTER+45},{CENTER} {CENTER+90},{CENTER-32} {CENTER+90},{CENTER+32}" fill="{ICON_FILL}"/>
<circle cx="{CENTER-50}" cy="{CENTER-8}" r="4" fill="{COLORS['fish']}"/>
'''

def seed_icon():
    return f'''
<ellipse cx="{CENTER-30}" cy="{CENTER+8}" rx="14" ry="22" fill="{ICON_FILL}" transform="rotate(-20 {CENTER-30} {CENTER+8})"/>
<ellipse cx="{CENTER+5}"  cy="{CENTER-12}" rx="14" ry="22" fill="{ICON_FILL}" transform="rotate(10 {CENTER+5} {CENTER-12})"/>
<ellipse cx="{CENTER+38}" cy="{CENTER+16}" rx="14" ry="22" fill="{ICON_FILL}" transform="rotate(30 {CENTER+38} {CENTER+16})"/>
'''

def invertebrate_icon():
    return f'''
<path d="M {CENTER-70} {CENTER}
         q 20 -40 40 0
         q 20 40 40 0
         q 20 -40 40 0"
      stroke="{ICON_FILL}" stroke-width="18" fill="none" stroke-linecap="round"/>
'''

def fruit_icon():
    return f'''
<circle cx="{CENTER}" cy="{CENTER+8}" r="56" fill="{ICON_FILL}"/>
<ellipse cx="{CENTER+18}" cy="{CENTER-50}" rx="22" ry="12" fill="{ICON_FILL}" transform="rotate(-35 {CENTER+18} {CENTER-50})"/>
<line x1="{CENTER}" y1="{CENTER-48}" x2="{CENTER+4}" y2="{CENTER-36}" stroke="{ICON_FILL}" stroke-width="6" stroke-linecap="round"/>
'''

def rodent_icon():
    return f'''
<circle cx="{CENTER}"    cy="{CENTER+8}"  r="56" fill="{ICON_FILL}"/>
<circle cx="{CENTER-30}" cy="{CENTER-38}" r="16" fill="{ICON_FILL}"/>
<circle cx="{CENTER+30}" cy="{CENTER-38}" r="16" fill="{ICON_FILL}"/>
<circle cx="{CENTER-18}" cy="{CENTER-8}"  r="5"  fill="{COLORS['rodent']}"/>
<circle cx="{CENTER+18}" cy="{CENTER-8}"  r="5"  fill="{COLORS['rodent']}"/>
<path d="M {CENTER+45} {CENTER+45} q 30 -10 40 -40"
      stroke="{ICON_FILL}" stroke-width="6" fill="none" stroke-linecap="round"/>
'''

def nectar_icon():
    petals = []
    for i in range(5):
        ang = -math.pi/2 + i * (2*math.pi/5)
        px = CENTER + int(40 * math.cos(ang))
        py = CENTER + int(40 * math.sin(ang))
        petals.append(f'<circle cx="{px}" cy="{py}" r="28" fill="{ICON_FILL}"/>')
    petals.append(f'<circle cx="{CENTER}" cy="{CENTER}" r="22" fill="{COLORS["nectar"]}"/>')
    return "\n".join(petals)


ICON_BUILDERS = {
    "invertebrate": invertebrate_icon,
    "seed":         seed_icon,
    "fish":         fish_icon,
    "fruit":        fruit_icon,
    "rodent":       rodent_icon,
    "nectar":       nectar_icon,
}


def svg_for(kind: str) -> str:
    bg    = COLORS[kind]
    inner = ICON_BUILDERS[kind]()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}">
  <circle cx="{CENTER}" cy="{CENTER}" r="{RADIUS+3}" fill="#1a1a2e"/>
  <circle cx="{CENTER}" cy="{CENTER}" r="{RADIUS}"   fill="{bg}"/>
  {inner}
</svg>
'''


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for kind in COLORS:
        path = OUT_DIR / f"{kind}.svg"
        path.write_text(svg_for(kind), encoding="utf-8")
        print(f"wrote {path.relative_to(REPO_ROOT)}  ({path.stat().st_size} B)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
