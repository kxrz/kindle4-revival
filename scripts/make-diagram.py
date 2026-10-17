#!/usr/bin/env python3
"""Draw the step-by-step overview (docs/img/steps-{fr,en}-{light,dark}.svg).

Usage: python3 scripts/make-diagram.py
"""
import html, os

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "img")

STEPS = {
    "fr": {
        "title": "Kindle 4 : de l'étagère à KOReader",
        "subtitle": "Firmware 4.1.4 · testé en octobre 2026",
        "trap": "piège", "optional": "si besoin",
        "steps": [
            ("kindle", "Identifier", ["Firmware 4.x", "Série B00E ou B023"], "WinterBreak"),
            ("download", "Télécharger", ["fetch-files.sh", "empreintes SHA-256"], None),
            ("unlock", "Jailbreak", ["3 fichiers à la racine", "Redémarrer · D → R → ←"], "certificats 2025"),
            ("grid", "KUAL", ["KUAL-KDK-1.0.azw2", "dans documents/"], None),
            ("wrench", "Réparer KUAL", ["RuntimeException ?", "runme.sh retire le Booklet"], "optional"),
            ("book", "KOReader", ["paquet « kindle »", "no framework"], None),
            ("dict", "Dictionnaires", ["Wiktionnaire fr-fr, en-fr", "un dossier par dico"], None),
            ("folders", "Bibliothèque", ["Genre / Auteur /", "Série NN - Titre"], None),
        ],
    },
    "en": {
        "title": "Kindle 4: from the shelf to KOReader",
        "subtitle": "Firmware 4.1.4 · tested in October 2026",
        "trap": "trap", "optional": "if needed",
        "steps": [
            ("kindle", "Identify", ["Firmware 4.x", "Serial B00E or B023"], "WinterBreak"),
            ("download", "Download", ["fetch-files.sh", "SHA-256 checked"], None),
            ("unlock", "Jailbreak", ["3 files at the root", "Restart · D → R → ←"], "2025 certificates"),
            ("grid", "KUAL", ["KUAL-KDK-1.0.azw2", "in documents/"], None),
            ("wrench", "Fix KUAL", ["RuntimeException?", "runme.sh drops the Booklet"], "optional"),
            ("book", "KOReader", ["\"kindle\" package", "no framework"], None),
            ("dict", "Dictionaries", ["Wiktionary fr-fr, en-fr", "one folder each"], None),
            ("folders", "Library", ["Genre / Author /", "Series NN - Title"], None),
        ],
    },
}

THEMES = {
    "light": dict(bg="#ffffff", card="#f5f4f0", line="#1a1a1a", text="#111111", sub="#5b5b5b",
                  badge="#111111", badge_text="#ffffff", trap="#b45309", trap_bg="#fdf1e3", dash="#9a9a9a"),
    "dark": dict(bg="#0d1117", card="#161b22", line="#e8e8e8", text="#f2f2f2", sub="#a3a3a3",
                 badge="#f2f2f2", badge_text="#0d1117", trap="#f59e0b", trap_bg="#2a1f0f", dash="#6b6b6b"),
}

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
CW, CH, GX, GY, MX, TOP = 270, 168, 46, 92, 40, 118


def icon(kind, x, y, c):
    """Line pictograms in a 44x44 box at (x, y)."""
    s = f'fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
    t = f'transform="translate({x},{y})"'
    shapes = {
        "kindle": f'<rect x="8" y="2" width="28" height="40" rx="4" {s}/><rect x="12" y="7" width="20" height="24" {s}/>'
                  f'<circle cx="22" cy="36.5" r="2.6" {s}/>',
        "download": f'<path d="M22 4v24M12 18l10 10 10-10" {s}/><path d="M6 32v6h32v-6" {s}/>',
        "unlock": f'<rect x="8" y="20" width="28" height="20" rx="3" {s}/><path d="M15 20v-7a8 8 0 0 1 15.5-3" {s}/>'
                  f'<circle cx="22" cy="30" r="2.4" {s}/>',
        "grid": f'<rect x="6" y="6" width="13" height="13" rx="2" {s}/><rect x="25" y="6" width="13" height="13" rx="2" {s}/>'
                f'<rect x="6" y="25" width="13" height="13" rx="2" {s}/><rect x="25" y="25" width="13" height="13" rx="2" {s}/>',
        "wrench": f'<path d="M28 6a9 9 0 0 0-8.5 12L7 30.5a3.5 3.5 0 0 0 5 5L24.5 23A9 9 0 0 0 36 14l-5 5-6-1-1-6 5-5z" {s}/>',
        "book": f'<path d="M22 10c-4-3-10-4-16-3v28c6-1 12 0 16 3 4-3 10-4 16-3V7c-6-1-12 0-16 3z" {s}/><path d="M22 10v28" {s}/>',
        "dict": f'<text x="22" y="30" text-anchor="middle" font-family="Georgia, serif" font-size="22" font-weight="700" '
                f'fill="{c}">Aa</text><path d="M8 36h28" {s}/>',
        "folders": f'<path d="M5 14h12l3 4h19v20H5z" {s}/><path d="M9 14V9h10l3 4h13v5" {s}/>',
    }
    return f'<g {t}>{shapes[kind]}</g>'


def draw(lang, theme):
    d, th = STEPS[lang], THEMES[theme]
    width = 2 * MX + 4 * CW + 3 * GX
    height = TOP + 2 * CH + GY + 56
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
         f'font-family="{FONT}" role="img" aria-label="{html.escape(d["title"])}">',
         f'<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         f'<path d="M0 0L10 5L0 10z" fill="{th["line"]}"/></marker></defs>',
         f'<rect width="{width}" height="{height}" rx="18" fill="{th["bg"]}"/>',
         f'<text x="{MX}" y="54" font-size="28" font-weight="800" fill="{th["text"]}" letter-spacing="-0.5">'
         f'{html.escape(d["title"])}</text>',
         f'<text x="{MX}" y="82" font-size="15" fill="{th["sub"]}">{html.escape(d["subtitle"])}</text>']

    def pos(i):
        row, col = divmod(i, 4)
        return MX + col * (CW + GX), TOP + row * (CH + GY)

    # connectors
    for i in range(7):
        x, y = pos(i)
        nx, ny = pos(i + 1)
        if i == 3:
            sx, sy, ex, ey = x + CW / 2, y + CH, nx + CW / 2, ny
            mid = sy + GY / 2
            o.append(f'<path d="M{sx} {sy + 4} V{mid - 14} Q{sx} {mid} {sx - 14} {mid} H{ex + 14} Q{ex} {mid} {ex} {mid + 14} '
                     f'V{ey - 6}" fill="none" stroke="{th["line"]}" stroke-width="2.2" marker-end="url(#a)"/>')
        else:
            o.append(f'<path d="M{x + CW + 6} {y + CH / 2} H{nx - 8}" stroke="{th["line"]}" stroke-width="2.2" '
                     f'marker-end="url(#a)"/>')

    for i, (ic, title, lines, note) in enumerate(d["steps"]):
        x, y = pos(i)
        optional = note == "optional"
        dash = f' stroke-dasharray="7 6" stroke="{th["dash"]}"' if optional else f' stroke="{th["line"]}"'
        o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="14" fill="{th["card"]}"{dash} stroke-width="2"/>')
        o.append(f'<circle cx="{x + 30}" cy="{y + 32}" r="16" fill="{th["badge"]}"/>')
        o.append(f'<text x="{x + 30}" y="{y + 38}" text-anchor="middle" font-size="16" font-weight="800" '
                 f'fill="{th["badge_text"]}">{i + 1}</text>')
        o.append(f'<text x="{x + 56}" y="{y + 39}" font-size="19" font-weight="750" fill="{th["text"]}">'
                 f'{html.escape(title)}</text>')
        o.append(icon(ic, x + CW - 60, y + 12, th["text"]))
        for k, line in enumerate(lines):
            o.append(f'<text x="{x + 20}" y="{y + 84 + k * 22}" font-size="14.5" fill="{th["sub"]}">{html.escape(line)}</text>')
        if note:
            label = d["optional"] if optional else f'{d["trap"]}\u00a0: {note}' if lang == "fr" else f'{d["trap"]}: {note}'
            tw = 7.1 * len(label) + 20
            o.append(f'<rect x="{x + 16}" y="{y + CH - 38}" width="{tw}" height="24" rx="12" fill="{th["trap_bg"]}"/>')
            o.append(f'<text x="{x + 26}" y="{y + CH - 21}" font-size="12.5" font-weight="650" fill="{th["trap"]}">'
                     f'{"⚠ " if not optional else ""}{html.escape(label)}</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for lang in STEPS:
        for theme in THEMES:
            path = os.path.join(OUT, f"steps-{lang}-{theme}.svg")
            open(path, "w", encoding="utf-8").write(draw(lang, theme))
            print(path)
