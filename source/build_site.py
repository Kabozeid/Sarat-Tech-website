"""Sarat Tech one-page website — generated, never hand-assembled.

Reads template.html, embeds the subset fonts (Oswald, Cairo — SIL OFL) as base64,
embeds the brand's English vertical mark (logo-vertical-en-dark.svg, copied from
../../Brand/SaratTech_Logo_2026-10-26/svg) as the spine for both languages, builds the header
wordmark from the same lettering (logo_paths.json), and
writes one self-contained HTML file one level up.

Run:  python3 build_site.py
"""
import base64, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "SaratTech_Website_2026-10-27.html")
GOLD, BLACK, WHITE = "#B28F3E", "#231F20", "#FFFFFF"

P = json.load(open(os.path.join(HERE, "logo_paths.json")))
LW, LH = P["sarat"]["w"], P["sarat"]["h"]
AR = LW / LH


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


def scaled(d, k):
    """Scale every number in an SVG path string (paths here use absolute M/L/C/Q/Z + commas)."""
    return re.sub(r"-?\d+\.?\d*(?:e-?\d+)?", lambda m: f"{float(m.group(0)) * k:.2f}", d)


def place(entry, size, x, y, w=None, align="center"):
    """<path> for a text outline generated at size 100, rescaled to `size`, ink box top-left at (x,y)."""
    k = size / 100
    bx0, by0, bx1, by1 = [v * k for v in entry["bbox"]]
    bw = bx1 - bx0
    if w is not None:
        x = x + (w - bw) / 2 if align == "center" else (x + w - bw if align == "right" else x)
    return (f'<path d="{scaled(entry["d"], k)}" transform="translate({x - bx0:.1f},{y - by0:.1f})"/>',
            by1 - by0, bw)


def lockup_vertical(W=1000, cls="lockup"):
    """Letters + TECH + Arabic, no frame (the page carries the frame)."""
    lw = round(W * 0.69); lh = lw / AR
    gap = round(W * 0.143)
    parts = [f'<path class="l-letters" d="{P["sarat"]["d"]}" transform="translate({(W - lw) / 2:.1f},0) scale({lw / LW:.5f})"/>']
    y = lh + gap
    p, h, _ = place(P["tech"], W * 0.235, 0, y, W); parts.append(f'<g class="l-text">{p}</g>'); y += h + W * 0.075
    aw = P["arabic"]["bbox"][2] - P["arabic"]["bbox"][0]
    size = 100 * (W * 0.76) / aw
    p, h, _ = place(P["arabic"], size, 0, y, W); parts.append(f'<g class="l-text">{p}</g>'); y += h
    H = round(y)
    return (f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
            f'aria-labelledby="lockup-title"><title id="lockup-title">Sarat Tech · سراة التقنية</title>{"".join(parts)}</svg>')


def brand_vertical_en(cls="lockup"):
    """The brand file SaratTech_logo-vertical-en-dark.svg (SARAT letters + TECH in the gold frame), used for both
    languages on Kabozeid's instruction of 2026-10-27. Fill attributes become classes so the page's motion applies."""
    s = open(os.path.join(HERE, "logo-vertical-en-dark.svg"), encoding="utf-8").read()
    s = re.sub(r'<svg [^>]*>', f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1674" role="img" aria-labelledby="lockup-title">', s, count=1)
    s = s.replace('<title>', '<title id="lockup-title">', 1)
    s = s.replace('<rect width="1000" height="1674" fill="#231F20"/>', '')
    assert s.count('<g fill="#B28F3E">') == 1 and s.count('<g fill="#FFFFFF">') == 1
    s = s.replace('<path fill="#B28F3E" fill-rule="evenodd"', '<path class="l-frame" fill-rule="evenodd"', 1)
    s = s.replace('<g fill="#B28F3E">', '<g class="l-letters">').replace('<g fill="#FFFFFF">', '<g class="l-text">')
    return s.strip()


def wordmark_en(H=400, cls="wordmark"):
    """Header mark: the same lettering and TECH as the vertical mark, set in a row. No Arabic line, both languages."""
    pad = round(H * 0.1)
    lh = H - 2 * pad; lw = lh * AR
    ts = H * 0.36; kt = ts / 100
    tw = (P["tech"]["bbox"][2] - P["tech"]["bbox"][0]) * kt
    th = (P["tech"]["bbox"][3] - P["tech"]["bbox"][1]) * kt
    gap = round(H * 0.18)
    W = round(pad + lw + gap + tw + pad)
    body = (f'<path class="l-letters" d="{P["sarat"]["d"]}" transform="translate({pad:.1f},{pad}) scale({lw / LW:.5f})"/>'
            f'<g class="l-text">{place(P["tech"], ts, pad + lw + gap, (H - th) / 2)[0]}</g>')
    return (f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Sarat Tech">'
            f'{body}</svg>')


def lockup_horizontal(direction="ltr", H=400, cls="wordmark"):
    pad = round(H * 0.1)
    lh = H - 2 * pad; lw = lh * AR
    ts, asz = H * 0.33, H * 0.30
    kt, ka = ts / 100, asz / 100
    tw = (P["tech"]["bbox"][2] - P["tech"]["bbox"][0]) * kt
    aw = (P["arabic"]["bbox"][2] - P["arabic"]["bbox"][0]) * ka
    th = (P["tech"]["bbox"][3] - P["tech"]["bbox"][1]) * kt
    ah = (P["arabic"]["bbox"][3] - P["arabic"]["bbox"][1]) * ka
    bw = max(tw, aw)
    gap = round(H * 0.18); inner = round(H * 0.08)
    W = round(pad + lw + gap + bw + pad)
    by = (H - (th + inner + ah)) / 2
    if direction == "ltr":
        lx, bx, al = pad, pad + lw + gap, "left"
        block = place(P["tech"], ts, bx, by, bw, al)[0] + place(P["arabic"], asz, bx, by + th + inner, bw, al)[0]
    else:
        lx, bx, al = W - pad - lw, pad, "right"
        block = place(P["arabic"], asz, bx, by, bw, al)[0] + place(P["tech"], ts, bx, by + ah + inner, bw, al)[0]
    body = (f'<path class="l-letters" d="{P["sarat"]["d"]}" transform="translate({lx:.1f},{pad}) scale({lw / LW:.5f})"/>'
            f'<g class="l-text">{block}</g>')
    return (f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Sarat Tech">'
            f'{body}</svg>')


def mark_square(W=256):
    """Favicon: the SARAT letters alone in the gold frame, as the parent's favicon."""
    t = round(W * 0.06)
    lw = round(W * 0.56); lh = lw / AR
    body = (f'<rect width="{W}" height="{W}" fill="{BLACK}"/>'
            f'<path fill="{GOLD}" fill-rule="evenodd" d="M0,0H{W}V{W}H0Z M{t},{t}V{W - t}H{W - t}V{t}Z"/>'
            f'<path fill="{GOLD}" d="{P["sarat"]["d"]}" transform="translate({(W - lw) / 2:.1f},{(W - lh) / 2:.1f}) scale({lw / LW:.5f})"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}">{body}</svg>'
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def letters_only(cls="letters"):
    return (f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LW} {LH}" aria-hidden="true">'
            f'<path d="{P["sarat"]["d"]}"/></svg>')


tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
subs = {
    "OSWALD_B64": b64(os.path.join(HERE, "fonts", "Oswald.woff2")),
    "CAIRO_B64": b64(os.path.join(HERE, "fonts", "Cairo.woff2")),
    "LOCKUP_VERTICAL": brand_vertical_en(),
    "WORDMARK_LTR": wordmark_en(),
    "WORDMARK_RTL": wordmark_en(),
    "LETTERS": letters_only(),
    "FAVICON": mark_square(),
}
for k, v in subs.items():
    assert "{{" + k + "}}" in tpl, k
    tpl = tpl.replace("{{" + k + "}}", v)
left = re.findall(r"{{[A-Z_]+}}", tpl)
assert not left, left
open(OUT, "w", encoding="utf-8").write(tpl)
print("wrote", os.path.abspath(OUT), f"{os.path.getsize(OUT) / 1024:.0f} KB")
