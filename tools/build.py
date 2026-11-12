#!/usr/bin/env python3
"""Build theme.css from src/theme.src.css, embedding fonts/*.woff2 as base64 (no network at runtime)."""
import base64, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
faces = [  # (family, file, style, weight)
    ("Ithaca Display", "BodoniModa-Regular.woff2", "normal", "400"),
    ("Ithaca Display", "BodoniModa-Italic.woff2", "italic", "400"),
    ("Ithaca Label", "Jost-Regular.woff2", "normal", "300 600"),  # variable, wght 300-600
    ("Ithaca Script", "PinyonScript-Regular.woff2", "normal", "400"),
    ("Ithaca Hand", "PatrickHand-Regular.woff2", "normal", "400"),
]
css = []
for fam, f, style, weight in faces:
    b64 = base64.b64encode((root / "fonts" / f).read_bytes()).decode()
    css.append(f'@font-face {{ font-family: "{fam}"; src: url("data:font/woff2;base64,{b64}") format("woff2"); '
               f'font-weight: {weight}; font-style: {style}; font-display: swap; }}')
src = (root / "src" / "theme.src.css").read_text(encoding="utf-8")
assert "/*@FONTS@*/" in src
out = src.replace("/*@FONTS@*/", "/* Bundled fonts (SIL OFL 1.1): Bodoni Moda as Ithaca Display, Jost as Ithaca Label, Pinyon Script as Ithaca Script, Patrick Hand as Ithaca Hand. */\n" + "\n".join(css))
(root / "theme.css").write_text(out, encoding="utf-8")
print(f"theme.css {len(out.encode())/1024:.1f} KB")
