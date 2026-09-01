#!/usr/bin/env python3
"""Builds ../Aperitif Website/index.html — the online Apéritif & Digestif list.

One file out, no dependencies, no outside requests. See README.md.
"""
import html, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "Aperitif Website", "index.html")
CREST = open(os.path.join(HERE, "crest.svg"), encoding="utf-8").read().strip()

TITLE = "Mr. Paul's Apéritif &amp; Digestif List"
DESC = ("Bitters, amari, tawny port and cordials at Mr. Paul's Supper Club in Edina, "
        "Minnesota — {n} bottles to open the appetite or settle it, with ABV and where each was made.")

# ---------------------------------------------------------------- bottles --
# ("Name", price, "abv", "House", "Town, Country", "character", "extra search", "ask")
#   price  â plain number, one pour
#   abv    â string with the % on it. "" prints nothing: use it when the bottle
#            is unconfirmed. A blank beats a wrong number on a bar menu.
#   ask    â small copper line under the entry, for house pours where the brand
#            varies. "" for everything else.
# Keep each section alphabetical. Must match ../Aperitif List.md.

SECTIONS = [
    ("Aperitif", "aperitif", "Before dinner.", "Pour", [
        ("Aperol", 10, "11%", "Campari Group", "Novi Ligure, Italy",
         "Gentian, rhubarb and cinchona; low-proof aperitivo", "", ""),
        ("Bonal", 9, "16%", "Distillerie Bonal", "Saint-Laurent-du-Pont, France",
         "Mistelle wine base, gentian root and cinchona bark", "gentiane quina", ""),
        ("Campari", 9, "24%", "Campari Group", "Novi Ligure, Italy",
         "Neutral spirit infused with herbs, chinotto and cascarilla", "", ""),
        ("H&H Madeira", 10, "19%", "Henriques & Henriques", "Câmara de Lobos, Madeira",
         "Fortified Tinta Negra, oxidative and off-dry", "henriques rainwater", ""),
        ("Salers Gentian", 10, "16%", "Distillerie de la Salers", "Auvergne, France",
         "Macerated yellow gentian root, oak-aged", "", ""),
    ]),
    ("Amaro", "amaro", "After dinner, bitter.", "Pour", [
        ("Amargo de Chile", 8, "32%", "CH Distillery", "Chicago, Illinois",
         "Mole spice, chile heat, cocoa and cinnamon", "amargo de chille latin", ""),
        ("Amaro Nonino", 13, "35%", "Nonino Distillatori", "Percoto, Italy",
         "Grape distillate, orange zest and thyme; barrique-aged", "quintessentia", ""),
        ("Amaro Noveis", 9, "24%", "Distillerie Francoli", "Ghemme, Italy",
         "Gentian, wormwood, genepy and rhubarb; alpine", "antico", ""),
        ("Averna", 17, "29%", "Fratelli Averna", "Caltanissetta, Sicily",
         "Caramel, bitter orange, lemon and Mediterranean herbs", "", ""),
        ("Cardamaro", 9, "17%", "Bosca", "Canelli, Italy",
         "Wine based; cardoon, blessed thistle, 23 botanicals", "cardoon", ""),
        ("Cynar", 12, "16.5%", "Campari Group", "Novi Ligure, Italy",
         "Artichoke leaf and twelve botanicals; vegetal", "artichoke", ""),
        ("Dr. Ferneti's", 9, "35%", "Earl Giles", "Minneapolis, Minnesota",
         "29 botanicals; mint, eucalyptus, artichoke and saffron", "dr fernetis fernet", ""),
        ("Fernet Branca", 9, "39%", "Fratelli Branca", "Milan, Italy",
         "27 herbs; saffron, myrrh, aloe and rhubarb", "", ""),
        ("Heirloom Genepy", 9, "51%", "Heirloom Liqueurs", "Minneapolis, Minnesota",
         "Artemisia and alpine botanicals with honey", "genepi", ""),
        ("Jägermeister", 10, "35%", "Mast-Jägermeister", "Wolfenbüttel, Germany",
         "56 herbs, roots and fruits; anise and licorice", "jagermeister", ""),
        ("Romana Amaro", 12, "35%", "Romana", "Italy",
         "33 Italian botanicals; herbal and bittersweet", "", ""),
    ]),
    ("Tawny Port", "tawny-port", "Taylor Fladgate, by the glass.", "Glass", [
        ("Taylor Fladgate 10 Year", 12, "20%", "Taylor Fladgate", "Vila Nova de Gaia, Portugal",
         "Cask-aged tawny, a blend averaging ten years", "", ""),
        ("Taylor Fladgate 20 Year", 20, "20%", "Taylor Fladgate", "Vila Nova de Gaia, Portugal",
         "Cask-aged tawny, a blend averaging twenty years", "", ""),
    ]),
    ("After Dinner", "after-dinner", "Sweeter — cordials, cremes and liqueurs.", "Pour", [
        ("Brady's Irish Creme", 10, "17%", "Brady’s", "Derry, Northern Ireland",
         "Dairy cream with Irish whiskey", "bradys", ""),
        ("Chartreuse Green", 18, "55%", "Chartreux Fathers", "Entre-Deux-Guiers, France",
         "130 botanicals; herbal, minty and peppery", "verte", ""),
        ("Chartreuse Yellow", 18, "43%", "Chartreux Fathers", "Entre-Deux-Guiers, France",
         "The same 130 botanicals; honeyed, saffron and anise", "jaune", ""),
        ("Disaronno", 10, "28%", "ILLVA Saronno", "Saronno, Italy",
         "Apricot kernel oil, burnt sugar and seventeen herbs and fruits", "amaretto", ""),
        ("Grand Marnier", 10, "40%", "Marnier Lapostolle", "Neauphle-le-Château, France",
         "Cognac blended with bitter orange essence", "cordon rouge", ""),
        ("Heirloom Pineapple", 9, "30%", "Heirloom Liqueurs", "Minneapolis, Minnesota",
         "Queen Victoria pineapple and quassia bark", "amaro", ""),
        ("Leroux Polish Blackberry", 8, "35%", "Leroux", "United States",
         "Blackberry in the Polish jeżynówka style, sweetened", "brandy", ""),
        ("Letterpress Limoncello", 13, "28%", "Letterpress Distilling", "Seattle, Washington",
         "Five weeks on lemon zest; Washington blackberry honey, not sugar", "", ""),
        ("Licor 43", 11, "31%", "Diego Zamora", "Cartagena, Spain",
         "Citrus, fruit and vanilla; 43 ingredients", "cuarenta y tres", ""),
        ("Luxardo Maraschino", 9, "32%", "Luxardo", "Torreglia, Italy",
         "Marasca cherries, pot-distilled, matured in ash vats", "", ""),
        ("Romana Sambuca", 12, "42%", "Romana", "Italy",
         "Anise and elderflower over a neutral base, sweetened", "sambuca", ""),
        ("St. George Nola Coffee", 12, "25%", "St. George Spirits", "Alameda, California",
         "Cold-infused Yirgacheffe coffee, chicory and vanilla", "saint george", ""),
        ("St. Germain", 10, "20%", "St-Germain", "France",
         "Elderflower macerated in grape eau-de-vie", "saint germain elderflower", ""),
    ]),
]

MAST_TITLE = 'Ap&eacute;ritif <span class="amp">&amp;</span><br>Digestif'
EYEBROW = "Bitters, Amari, Port &amp; Cordials"
TAGLINE = ("One to sharpen the appetite, one to settle it. "
           "Everything on this list does one job or the other.")

LINKS = [
    ("https://mrpaulswhiskey.netlify.app/", "The whiskey list"),
    ("https://mrpaulsagave.netlify.app/", "The agave list"),
    ("https://www.mrpaulssupperclub.com/menu/", "All menus"),
    ("https://www.mrpaulssupperclub.com/", "mrpaulssupperclub.com"),
]

# ------------------------------------------------------------------- css ---
# Ink & Copper. Chosen over green-on-cream, which read too close to the agave
# sheet. No web fonts, no CDN, no images — one file that renders the same on
# bar wifi as on your desk.
CSS = """
:root{
  --ground:#121A22; --panel:#1B2530; --panel-2:#243040;
  --paper:#E4E0D5; --paper-dim:#C4C0B6;
  --copper:#C1794A; --copper-lit:#D89463; --copper-soft:#A9764F;
  --muted:#8D9AA4; --faint:#74818C;
  --rule:rgba(193,121,74,.28); --hair:rgba(193,121,74,.48);
  --field:#18212B;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,"Times New Roman",serif;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--ground); color:var(--paper);
  font-family:var(--serif);
  font-size:16px; line-height:1.5;
}
.sheet{
  max-width:680px; margin:0 auto; padding:0 26px 84px;
  border-left:1px solid var(--hair); border-right:1px solid var(--hair);
  min-height:100vh;
}
@media (max-width:640px){
  .sheet{border-left:0;border-right:0;padding:0 18px 72px}
}

/* ---------- masthead ---------- */
.mast{padding:52px 0 4px;text-align:center}
.crestwrap{width:min(150px,42%);margin:0 auto 26px;color:var(--copper)}
.crestwrap svg{display:block;width:100%;height:auto}
.mast h1{
  font-weight:400;font-size:clamp(30px,7.6vw,52px);line-height:1.16;
  letter-spacing:.1em;text-transform:uppercase;margin:0;color:var(--paper);
  text-indent:.1em;
}
.mast h1 .amp{color:var(--copper);font-style:italic;text-transform:none;letter-spacing:0}
.eyebrow{
  font-weight:400;font-style:italic;font-size:clamp(13px,3vw,15px);letter-spacing:.06em;
  color:var(--copper);margin:16px 0 0;
}
.hr{width:min(300px,68%);height:0;border-top:1px solid var(--copper);opacity:.75;margin:22px auto 0;position:relative}
.hr::after{content:'';position:absolute;left:50%;top:-3px;width:6px;height:6px;margin-left:-3px;
  background:var(--copper);transform:rotate(45deg)}
.tag{
  margin:20px auto 0;max-width:44ch;color:var(--muted);
  font-size:14.5px;line-height:1.65;
}

/* ---------- sticky controls ---------- */
.tools{
  position:sticky;top:0;z-index:20;margin:28px -26px 0;padding:12px 26px 10px;
  background:var(--ground);
}
.tools::after{content:'';position:absolute;left:0;right:0;top:100%;height:16px;pointer-events:none;
  background:linear-gradient(var(--ground),rgba(18,26,34,0))}
@media (max-width:640px){.tools{margin:24px -18px 0;padding:10px 18px 8px}}
.search{position:relative;display:block}
.search svg{position:absolute;left:13px;top:50%;transform:translateY(-50%);
  width:15px;height:15px;stroke:var(--faint);fill:none;stroke-width:1.8}
#q{
  width:100%;padding:11px 14px 11px 37px;border-radius:2px;
  background:var(--field);border:1px solid var(--rule);color:var(--paper);
  font-family:inherit;font-size:15px;
}
#q::placeholder{color:var(--faint);font-style:italic}
#q:focus{outline:2px solid var(--copper);outline-offset:1px;border-color:transparent}
.chips{display:flex;gap:7px;overflow-x:auto;padding:10px 0 2px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chip{
  flex:0 0 auto;text-decoration:none;color:var(--copper);
  font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;
  padding:6px 12px;border:1px solid var(--rule);border-radius:2px;
  transition:color .18s,border-color .18s,background .18s;white-space:nowrap;
}
.chip:hover,.chip:focus-visible{color:var(--ground);background:var(--copper);border-color:var(--copper)}

/* ---------- sections ---------- */
.sec{padding-top:44px;scroll-margin-top:120px}
.sec.hide{display:none}
.sechd{display:flex;align-items:baseline;gap:12px;
  border-bottom:1px solid var(--copper);padding-bottom:8px}
.sechd h2{
  font-weight:400;font-size:20px;letter-spacing:.18em;
  text-transform:uppercase;margin:0;color:var(--paper);
}
.cl{font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--faint);text-align:right;flex:0 0 auto}
.cl.ca{margin-left:auto;width:48px}
.cl.cb{width:30px}
.blurb{margin:12px 0 0;font-style:italic;font-size:13.5px;color:var(--muted);letter-spacing:.01em}
.pours{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-direction:column}
.pour{display:flex;flex-direction:column;padding:10px 8px 11px 0;
  border-radius:2px;transition:background .16s}
.pour.hide{display:none}
.pour:hover{background:var(--panel);padding-left:8px;margin-left:-8px}
.top{display:flex;align-items:baseline;gap:9px}
.nm{font-size:17px;line-height:1.35}
.ldr{
  flex:1;min-width:12px;align-self:flex-end;height:1px;margin-bottom:6px;
  background-image:radial-gradient(circle,rgba(228,224,213,.30) 1px,transparent 1.2px);
  background-size:5px 2px;background-repeat:repeat-x;background-position:bottom;
}
.pf{flex:0 0 auto;width:48px;text-align:right;font-size:12px;letter-spacing:.02em;
  color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap}
.pr{flex:0 0 auto;width:30px;text-align:right;font-size:16px;
  font-variant-numeric:tabular-nums;color:var(--copper);white-space:nowrap}
.org{margin-top:4px;font-size:12.5px;line-height:1.5;color:var(--muted);
  letter-spacing:.005em;max-width:60ch}
.org .ch{font-style:italic;color:var(--paper-dim)}
.org .dot{color:var(--faint)}
.org .ask{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--copper-soft);margin-top:3px}

/* ---------- empty + footer ---------- */
#empty{display:none;padding:56px 0;text-align:center;color:var(--muted);font-style:italic}
#empty.on{display:block}
.foot{margin-top:60px;padding-top:26px;border-top:1px solid var(--rule);
  color:var(--muted);font-size:13.5px;line-height:1.75}
.footmark{width:64px;margin:0 auto 20px;color:var(--copper)}
.footmark svg{display:block;width:100%;height:auto}
.links{display:flex;flex-wrap:wrap;justify-content:center;gap:12px 22px;margin:0}
.links a{color:var(--paper);text-decoration:none;font-size:11.5px;
  letter-spacing:.16em;text-transform:uppercase;
  border-bottom:1px solid var(--rule);padding-bottom:2px}
.links a:hover,.links a:focus-visible{color:var(--copper-lit);border-color:var(--copper-lit)}
@media (max-width:520px){.ldr{display:none}.top{gap:12px}.nm{flex:1}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

FOOTMARK = ('<svg viewBox="0 0 120 40" aria-hidden="true" fill="none" stroke="currentColor" '
            'stroke-width="1.1"><path d="M2 20h34M84 20h34"></path>'
            '<path d="M60 6c-6 6-9 10-9 14a9 9 0 0 0 18 0c0-4-3-8-9-14z"></path>'
            '<path d="M60 20v14"></path>'
            '<path d="M60 27c-4 0-7-2-9-5M60 27c4 0 7-2 9-5"></path>'
            '<circle cx="44" cy="20" r="2"></circle><circle cx="76" cy="20" r="2"></circle></svg>')

SEARCH_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle>'
               '<path d="M20 20l-3.6-3.6"></path></svg>')

SCRIPT = """
(function(){
  var q = document.getElementById('q'),
      pours = [].slice.call(document.querySelectorAll('.pour')),
      secs = [].slice.call(document.querySelectorAll('.sec')),
      empty = document.getElementById('empty');
  function run(){
    var t = q.value.trim().toLowerCase();
    pours.forEach(function(p){
      p.classList.toggle('hide', t !== '' && p.dataset.n.indexOf(t) === -1);
    });
    var any = false;
    secs.forEach(function(s){
      var vis = s.querySelectorAll('.pour:not(.hide)').length;
      s.classList.toggle('hide', vis === 0);
      if (vis) any = true;
    });
    empty.classList.toggle('on', !any);
  }
  q.addEventListener('input', run);
  q.addEventListener('search', run);
  run();
})();
"""


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def build():
    count = sum(len(b) for *_, b in SECTIONS)
    desc = DESC.format(n=count)

    chips = "".join(
        '<a class="chip" href="#%s">%s</a>' % (sid, html.escape(name))
        for name, sid, _, _, _ in SECTIONS)

    secs = []
    for name, sid, blurb, collabel, bottles in SECTIONS:
        rows = []
        for bname, price, abv, house, place, char, extra, ask in bottles:
            data = " ".join(x for x in (bname.lower(), extra, house.lower(),
                                        place.lower(), char.lower(), name.lower()) if x)
            org = ""
            bits = []
            if house or place:
                bits.append('<span class="hs">%s</span>'
                            % html.escape(" · ".join(x for x in (house, place) if x)))
            if char:
                bits.append('<span class="ch">%s</span>' % html.escape(char))
            if bits:
                org = '<span class="org">%s%s</span>' % (
                    '<span class="dot"> — </span>'.join(bits),
                    '<span class="ask">%s</span>' % html.escape(ask) if ask else "")
            rows.append(
                '<li class="pour" data-n="%s"><span class="top">'
                '<span class="nm">%s</span><span class="ldr"></span>'
                '<span class="pf">%s</span><span class="pr">%d</span></span>%s</li>'
                % (html.escape(data, quote=True), html.escape(bname),
                   html.escape(abv), price, org))
        secs.append(
            '  <section class="sec" id="%s">\n'
            '    <header class="sechd"><h2>%s</h2>'
            '<span class="cl ca">ABV</span><span class="cl cb">%s</span></header>\n'
            '    <p class="blurb">%s</p>\n'
            '    <ul class="pours">%s</ul>\n'
            '  </section>'
            % (sid, html.escape(name), html.escape(collabel), html.escape(blurb),
               "".join(rows)))

    links = "".join('<a href="%s">%s</a>' % (u, html.escape(t)) for u, t in LINKS)

    doc = (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<title>' + TITLE + '</title>\n'
        '<meta name="description" content="' + desc + '">\n'
        '<meta name="theme-color" content="#121A22">\n'
        '<meta name="color-scheme" content="dark">\n\n'
        '<!-- link preview (texts, iMessage, Facebook, Instagram bio, link tree) -->\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:title" content="' + TITLE + '">\n'
        '<meta property="og:description" content="' + desc + '">\n'
        '<meta property="og:site_name" content="Mr. Paul\'s Supper Club">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="twitter:title" content="' + TITLE + '">\n'
        '<meta name="twitter:description" content="' + desc + '">\n\n'
        "<!-- favicon, inlined so there is no second file to upload -->\n"
        '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\''
        " viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23121A22'/%3E"
        "%3Ctext x='16' y='23' font-family='Georgia,serif' font-size='19' fill='%23C1794A'"
        " text-anchor='middle'%3EA%3C/text%3E%3C/svg%3E\">\n"
        '</head>\n<body>\n<style>' + CSS + '</style>\n\n'
        '<div class="sheet">\n'
        '  <header class="mast">\n'
        '    <div class="crestwrap">' + CREST + '</div>\n'
        '    <h1>' + MAST_TITLE + '</h1>\n'
        '    <p class="eyebrow">' + EYEBROW + '</p>\n'
        '    <div class="hr"></div>\n'
        '    <p class="tag">' + TAGLINE + '</p>\n'
        '  </header>\n\n'
        '  <div class="tools">\n'
        '    <label class="search" for="q">' + SEARCH_ICON + '\n'
        '      <input id="q" type="search" placeholder="Search a bottle&hellip;" '
        'autocomplete="off" aria-label="Search the list">\n'
        '    </label>\n'
        '    <nav class="chips" aria-label="Jump to a category">' + chips + '</nav>\n'
        '  </div>\n\n'
        + "\n\n".join(secs) + '\n\n'
        '  <p id="empty">Nothing by that name. Try another bottle.</p>\n\n'
        '  <div class="foot">\n'
        '    <div class="footmark">' + FOOTMARK + '</div>\n'
        '    <p class="links">' + links + '</p>\n'
        '  </div>\n'
        '</div>\n\n'
        '<script>' + SCRIPT + '</script>\n\n'
        '</body>\n</html>\n')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print("wrote %s" % os.path.normpath(OUT))
    print("%d bottles across %d sections, %.0f KB"
          % (count, len(SECTIONS), len(doc.encode("utf-8")) / 1024))
    for name, _, _, _, bottles in SECTIONS:
        order = [b[0] for b in bottles]
        noabv = [b[0] for b in bottles if not b[2]]
        flag = "" if order == sorted(order, key=str.lower) else "   <-- NOT ALPHABETICAL"
        print("  %-13s %2d%s%s" % (name, len(order), flag,
              "   no ABV: " + ", ".join(noabv) if noabv else ""))


if __name__ == "__main__":
    build()
