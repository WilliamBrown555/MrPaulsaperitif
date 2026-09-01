# Publishing the Aperitif List

How the online **Apéritif & Digestif** menu gets on the web, and how to update it later. Same setup as [[Publishing the Whiskey List]] and [[Publishing the Agave List]].

## How the pieces connect

```
Printed menu QR  →  lnk.bio/CarnivalBar  →  "Apéritif & Digestif" button  →  mrpaulsaperitif.netlify.app
```

The QR points at the **link page**, never at the menu directly. If the menu ever moves hosts, you edit one button on the link page and every printed menu still works.

## Setting it up

The whole site is one file: `Aperitif Website/index.html` in this folder. No images, no stylesheets, no fonts — the crest is inline SVG and everything else is system type, so nothing loads from outside the file. It works on bad bar wifi.

This folder is its own git repo, pushed to `github.com/WilliamBrown555/MrPaulsaperitif`, and Netlify deploys from that repo. It is already set up:

- **Netlify project:** `mrpaulsaperitif`
- **Publish directory:** `Aperitif Website`
- **Build command:** empty — the HTML is committed pre-built, so Netlify only serves the folder. Giving it a build command breaks the deploy.

Final URL: `https://mrpaulsaperitif.netlify.app`

## Add it to the link page

On **lnk.bio/CarnivalBar**, add a button pointing at `https://mrpaulsaperitif.netlify.app/`.
Suggested label: **Apéritif & Digestif**.

Put it next to the whiskey and agave buttons.

## Updating the list later

Ask Claude for a rebuild — or run it yourself:

```
cd source
python3 build_aperitif.py
```

It overwrites `Aperitif Website/index.html`. Diff that file against what was there before pushing — a deployed file can carry a hand-edit the script doesn't know about. Then:

```
git add -A
git commit -m "what changed"
git push
```

**The push is the deploy.** Same URL, live in about a minute. The QR and the link tree never change.

## Why it isn't called "Amaro"

The list runs from Aperol to twenty-year tawny. *Amaro* is accurate for eleven of the thirty-one bottles and wrong for the rest, so the page is titled **Apéritif & Digestif** — the term that actually covers a list that opens the appetite at one end and settles it at the other. The eyebrow line does the plain-language work: *Bitters, Amari, Port & Cordials*.

The vault folder, the notes and the build script were renamed to match (Sept 2026). Only the button in Toast still says "amaro" — that one is what the staff call it.

## What it looks like, and why

**Ink & Copper** — ground `#121A22`, type `#E4E0D5`, copper `#C1794A` — set in an old-style serif rather than the Helvetica the other two lists use.

The first version was deep green and gold on cream. It was killed for reading too close to the [[Agave List]]: a cream ground is a cream ground, and the eye registers that before it registers the hue. Changing the ground did the separation work that changing the accent color couldn't. Six palettes were compared before this one; the runners-up were Bottle Green and Aubergine & Rose.

So the three lists now read: whiskey dark and brassy, agave light and burgundy, this one dark and cold with warm metal.

The Mr. Paul's crest sits at the top of the page, tinted copper from CSS — it's the same `crest.svg` the agave list uses in its footer, so it stays sharp at any size and recolors with one line.

## What's on the page

All 31 bottles from [[Aperitif List]], in the same four sections and the same alphabetical order. One price per bottle — there are no half pours on this list.

Online-only: search across bottle names and alternate spellings (Jägermeister finds "jagermeister", St. Germain finds "elderflower", Chartreuse finds "verte" and "jaune"), plus jump-to-section chips.

## Still open

- **Possible duplicate Madeira.** Aperitif carries *H&H Madeira ($10)* from Liqueurs/Cordials; Dessert Wine separately lists *GLS Madiera ($12)*. Might be the same wine at two pours, might be two products. Worth checking the bottle.
- **No vermouth.** Not in the Toast group. If the bar pours Dolin, Carpano or Cocchi, they belong under Aperitif and need adding by hand.
- **The aquavit question.** The three Gamle Ode bottles read as a separate category and are off the list. Say if they should appear somewhere.

## Related

- [[Aperitif List]]
- [[Publishing the Whiskey List]]
- [[Publishing the Agave List]]
- [[Spirits Board]]
