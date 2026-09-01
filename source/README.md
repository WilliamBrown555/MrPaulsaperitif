# Apéritif & Digestif — build source

`build_amaro.py` builds `../Amaro Website/index.html` — the online **Apéritif & Digestif** list. Self-contained: bottle data, prices, HTML and CSS all live in the one script. Its only outside file is `crest.svg` (shared with the agave build), inlined into the masthead at build time.

## Rebuilding

```
python3 build_amaro.py
```

Prints the bottle count per section and flags any section that has fallen out of alphabetical order. Then drag the `Amaro Website` folder onto Netlify — see [[Publishing the Amaro List]].

## Editing bottles

One list per section in `SECTIONS`, near the top. Each bottle is a tuple:

```python
("Amaro Nonino", 13, "quintessentia")
#  name           price  extra search words
```

- **price** — a plain number. One pour only; this list has no half pours, so there is no half/full pair and no $25 rule.
- **extra search words** — anything a guest might type that isn't in the name: accent-free spellings (`jagermeister`), the botanical (`elderflower`), the color in French (`verte`, `jaune`). Optional; use `""` when the name covers it.

The section name is appended to every row's search text automatically, so typing "aperitif" filters to that section.

Keep sections alphabetical and matching [[Amaro List]] — the build prints a warning if one isn't.

## Checking a rebuild against the list

```python
import re
src = open('../Amaro List.md', encoding='utf-8').read()
ref = {m.group(1).strip().lower(): int(m.group(2))
       for m in re.finditer(r'^\| (.+?) \| (\d+) \|$', src, re.M)}
page = open('../Amaro Website/index.html', encoding='utf-8').read()
got = {m.group(1).replace('&amp;', '&').replace('&#x27;', "'").strip().lower(): int(m.group(2))
       for m in re.finditer(r'<span class="nm">(.*?)</span><span class="ldr"></span>'
                            r'<span class="pr">(\d+)</span>', page)}
print('missing from page:', sorted(set(ref) - set(got)))
print('on page but not in the list:', sorted(set(got) - set(ref)))
print('price mismatches:', [(k, ref[k], got[k]) for k in set(ref) & set(got) if ref[k] != got[k]])
```

All three should print empty.

## Notes on the build

- **No outside requests.** No web fonts, no CDN, no raster images. The crest is inline SVG tinted from CSS.
- **Colors** are the Ink & Copper scheme: `#121A22` ground, `#E4E0D5` type, `#C1794A` copper. Chosen after green-on-cream read too close to the agave sheet.
- **Type** is an old-style serif (Iowan / Palatino / Georgia), deliberately unlike the Helvetica on the whiskey and agave pages.
