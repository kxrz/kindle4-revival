#!/usr/bin/env python3
"""Render a terminal transcript as an SVG "screenshot" (used for docs/img).

Usage: python3 term2svg.py transcript.txt out.svg [--title "zsh"]
Lines starting with "$ " are drawn as commands, "# " as comments, the rest as output.
"""
import argparse, html

BG, FG, PROMPT, CMD, COMMENT, OK, ERR = "#1e1f24", "#d4d4d8", "#7dd3fc", "#f4f4f5", "#8b8b94", "#86efac", "#fca5a5"
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
CW, LH, PAD, BAR = 8.9, 20, 18, 34


def line_svg(y, text):
    if text.startswith(("$ ", "> ")):
        return (f'<text x="{PAD}" y="{y}" xml:space="preserve"><tspan fill="{PROMPT}">{text[0]} </tspan>'
                f'<tspan fill="{CMD}" font-weight="600">{html.escape(text[2:])}</tspan></text>')
    color = COMMENT if text.startswith("# ") else FG
    if text.startswith(("OK ", "Done", "copied")) or " OK" in text[:12]:
        color = OK
    if any(w in text for w in ("MISMATCH", "Error", "Exception", "KUALBooklet.jar")):
        color = ERR
    return f'<text x="{PAD}" y="{y}" fill="{color}" xml:space="preserve">{html.escape(text)}</text>'


def render(lines, title):
    width = int(max(60, max((len(l) for l in lines), default=0)) * CW + 2 * PAD)
    height = BAR + PAD + len(lines) * LH + PAD // 2
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
           f'font-family="{FONT}" font-size="14">',
           f'<rect width="{width}" height="{height}" rx="10" fill="{BG}"/>',
           f'<rect width="{width}" height="{BAR}" rx="10" fill="#2a2b31"/>',
           f'<rect y="{BAR - 10}" width="{width}" height="10" fill="#2a2b31"/>']
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        out.append(f'<circle cx="{20 + i * 20}" cy="{BAR // 2}" r="6" fill="{c}"/>')
    out.append(f'<text x="{width // 2}" y="{BAR // 2 + 5}" fill="#9b9ba3" text-anchor="middle" font-size="13">'
               f'{html.escape(title)}</text>')
    y = BAR + PAD + 6
    for l in lines:
        out.append(line_svg(y, l.rstrip("\n")))
        y += LH
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("out")
    ap.add_argument("--title", default="Terminal")
    a = ap.parse_args()
    lines = open(a.transcript, encoding="utf-8").read().rstrip("\n").split("\n")
    open(a.out, "w", encoding="utf-8").write(render(lines, a.title))
