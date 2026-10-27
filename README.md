# Sarat Tech · سراة التقنية — company website

One self-contained page, English and Arabic. `index.html` opens directly from disk or from any static host; fonts and the brand mark are embedded, nothing else is loaded.

## Edit and rebuild

```
cd source
python3 build_site.py
```

`build_site.py` reads `template.html`, embeds the font subsets in `fonts/` (Oswald, Cairo — SIL Open Font License) and the brand mark (`logo-vertical-en-dark.svg`, header wordmark from `logo_paths.json`), and writes `../index.html`. Edit `template.html`, never `index.html`.

## Languages

Desktop shows English and Arabic as one spread; the header toggle gives EN, عربي, or both. Phones show one language. The choice is remembered in the browser.

## Not on the page yet

- Products section: returns when the first product's name and logo are settled.
- Team section: added when names and photos are shared.
