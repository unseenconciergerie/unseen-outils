"""
Images d'aperçu au partage d'un lien (WhatsApp, Snapchat, iMessage, LinkedIn, X) et icônes du site
(27/10/2026). Une image 1200 x 630 par page : la grande photo de la page, assombrie à gauche,
le mot « UNSEEN. » en blanc et le nom de la page. Icônes PNG tirées du logo iceberg des réseaux
(le SVG seul n'était pas lu par Snapchat ni WhatsApp, d'où l'icône cassée).

    assistant-prospection/venv/bin/python site-unseen/outils/apercus_partage.py apercu  → page de choix pour Jay
    assistant-prospection/venv/bin/python site-unseen/outils/apercus_partage.py site <icone>  → images + balises
    (<icone> = classique ou glacier, selon le choix de Jay)
"""
import html
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SITE = Path(__file__).resolve().parent.parent
IMG = SITE / "img"
PROJET = SITE.parent
POLICE_TITRE = Path.home() / "Library/Fonts/LeagueSpartan-Bold.ttf"
POLICE_TEXTE = PROJET / "assistant-prospection/sources_offre_partenaire/polices/DMSans-600.ttf"
LOGOS = PROJET / "Livrables/Logos-reseaux"
ICONES = {"classique": LOGOS / "Noir et blanc (classique)/Noir et blanc - Instagram et Facebook profil - iceberg fond noir.png",
          "glacier": LOGOS / "Glacier (ski)/Glacier - Instagram et Facebook profil - iceberg fond noir.png"}
APERCU = PROJET / "Livrables/Maquettes site (évolution)/17 Aperçus au partage et icône (27-10).html"

# page : (photo source, texte sous le logo, cadrage horizontal 0 à 1)
PAGES = {
    "index.html": ("hero.webp", "PRIVATE LUXURY CONCIERGE · PARIS", .5),
    "professionals.html": ("pro-hero.webp", "FOR TRAVEL PROFESSIONALS", .6),
    "paris.html": ("paris-hero.webp", "PARIS", .5),
    "riviera.html": ("riviera-hero.webp", "THE RIVIERA", .5),
    "ocean-indien.html": ("maurice-hero.webp", "THE INDIAN OCEAN", .5),
    "saison-ski-2026-2027.html": ("ski-courchevel.webp", "THE ALPS · WINTER 2026-2027", .5),
    "formule-1.html": ("f1-monaco-port.webp", "FORMULA 1 · MONACO", .5),
    "legal.html": ("hero.webp", "LEGAL NOTICE", .5),
}


def image_apercu(source, texte, cx):
    """1200 x 630 : photo recadrée, dégradé sombre à gauche, logo et texte en blanc."""
    im = Image.open(IMG / source).convert("RGB")
    l, h = im.size
    ratio = 1200 / 630
    if l / h > ratio:                      # trop large : on coupe sur les côtés
        nl = int(h * ratio)
        x = int((l - nl) * cx)
        im = im.crop((x, 0, x + nl, h))
    else:                                  # trop haute : on coupe en haut et en bas
        nh = int(l / ratio)
        y = (h - nh) // 2
        im = im.crop((0, y, l, y + nh))
    im = im.resize((1200, 630), Image.LANCZOS)
    voile = Image.new("L", (1200, 630))
    d = ImageDraw.Draw(voile)
    for x in range(1200):                  # noir à 88 % à gauche, 16 % à droite
        d.line([(x, 0), (x, 630)], fill=int(225 - 185 * x / 1200))
    im = Image.composite(Image.new("RGB", (1200, 630), (20, 19, 22)), im, voile)
    d = ImageDraw.Draw(im)
    titre = ImageFont.truetype(str(POLICE_TITRE), 118)
    petit = ImageFont.truetype(str(POLICE_TEXTE), 26)
    d.text((72, 300), "UNSEEN.", font=titre, fill="white")
    d.rectangle((76, 450, 76 + 64, 453), fill="#7AA3BC")
    # lettres espacées, comme les petits titres du site
    x = 76
    for c in texte:
        d.text((x, 478), c, font=petit, fill=(232, 226, 228))
        x += petit.getlength(c) + 4.5
    return im


def icones(choix):
    """favicon PNG 32 et 48, icône iPhone 180, icônes Android 192 et 512."""
    logo = Image.open(ICONES[choix]).convert("RGB")
    # le logo occupe le centre de l'image : on resserre un peu pour qu'il soit lisible en petit
    l, h = logo.size
    m = int(l * .14)
    logo = logo.crop((m, m, l - m, h - m))
    sorties = {"favicon-32.png": 32, "favicon-48.png": 48, "apple-touch-icon.png": 180, "icon-192.png": 192, "icon-512.png": 512}
    for nom, taille in sorties.items():
        logo.resize((taille, taille), Image.LANCZOS).save(SITE / nom, optimize=True)
    return list(sorties)


def apercu():
    dossier = APERCU.parent / "17 apercus"
    dossier.mkdir(exist_ok=True)
    cartes = ""
    for page, (src, texte, cx) in PAGES.items():
        nom = f"og-{page.replace('.html', '')}.jpg"
        image_apercu(src, texte, cx).save(dossier / nom, quality=85, optimize=True, progressive=True)
        cartes += f'<figure><img src="17 apercus/{nom}"><figcaption>{page}</figcaption></figure>'
    for choix, chemin in ICONES.items():
        im = Image.open(chemin).convert("RGB")
        l, h = im.size; m = int(l * .14)
        im.crop((m, m, l - m, h - m)).resize((180, 180), Image.LANCZOS).save(dossier / f"icone-{choix}.png")
    APERCU.write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aperçus au partage et icône</title><style>body{{font-family:-apple-system,system-ui,sans-serif;max-width:1300px;margin:0 auto;padding:24px 16px;background:#F4EAE5;color:#2B2A2E}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:18px}}figure img{{width:100%;display:block;border-radius:10px}}figcaption{{font-size:13px;color:#8A8083;margin-top:6px}}
.ic{{display:flex;gap:40px;flex-wrap:wrap}}.ic div{{text-align:center}}.ic img{{width:120px;border-radius:50%;display:block;margin:0 auto 8px}}
.ic .tab{{width:32px;border-radius:6px}}</style></head><body>
<h1>Ce que l'on voit en partageant le lien du site</h1>
<p>Une image par page (1200 × 630). Elle s'affiche dans WhatsApp, Snapchat, iMessage, LinkedIn et X quand quelqu'un envoie le lien.</p>
<div class="g">{cartes}</div>
<h2 style="margin-top:40px">L'icône du site : laquelle ?</h2>
<p>Elle apparaît dans l'onglet du navigateur, dans le petit rond de l'aperçu Snapchat, et sur l'écran d'accueil de l'iPhone si quelqu'un ajoute le site.</p>
<div class="ic"><div><img src="17 apercus/icone-classique.png"><img class="tab" src="17 apercus/icone-classique.png"><b>1. Classique</b><br>iceberg blanc sur noir<br>(ne change jamais)</div>
<div><img src="17 apercus/icone-glacier.png"><img class="tab" src="17 apercus/icone-glacier.png"><b>2. Glacier</b><br>iceberg bleu sur noir<br>(couleur de la saison actuelle)</div></div>
</body></html>""", encoding="utf-8")
    print("aperçu :", APERCU)


def site(choix):
    """Écrit les images dans img/, les icônes à la racine, et les balises dans chaque page."""
    for page, (src, texte, cx) in PAGES.items():
        nom = f"og-{page.replace('.html', '')}.jpg"
        image_apercu(src, texte, cx).save(IMG / nom, quality=85, optimize=True, progressive=True)
        chemin = SITE / page
        t = chemin.read_text(encoding="utf-8")
        url = "https://unseenconciergerie.com/" + ("" if page == "index.html" else page)
        titre = html.unescape(re.search(r"<title>([^<]*)</title>", t).group(1))
        desc = re.search(r'<meta name="description" content="([^"]*)"', t)
        desc = html.unescape(desc.group(1)) if desc else "UNSEEN. Private luxury concierge in Paris."
        # on retire les anciennes balises og:/twitter: et icônes, puis on remet un bloc complet
        t = re.sub(r'[ \t]*<meta (?:property|name)="(?:og|twitter):[^"]*" content="[^"]*">\n?', "", t)
        t = re.sub(r'[ \t]*<link rel="(?:icon|apple-touch-icon|manifest)"[^>]*>\n?', "", t)
        bloc = (f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="UNSEEN.">\n'
                f'<meta property="og:url" content="{url}">\n<meta property="og:title" content="{html.escape(titre)}">\n'
                f'<meta property="og:description" content="{html.escape(desc)}">\n'
                f'<meta property="og:image" content="https://unseenconciergerie.com/img/{nom}">\n'
                f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
                f'<meta name="twitter:card" content="summary_large_image">\n'
                f'<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">\n'
                f'<link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">\n'
                f'<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n')
        t = t.replace("</title>\n", "</title>\n" + bloc, 1)
        chemin.write_text(t, encoding="utf-8")
        print(page, "→", nom)
    # page d'erreur : seulement les icônes (elle n'a pas d'aperçu, Google ne la montre pas)
    chemin = SITE / "404.html"
    t = chemin.read_text(encoding="utf-8")
    t = re.sub(r'[ \t]*<link rel="(?:icon|apple-touch-icon)"[^>]*>\n?', "", t)
    t = t.replace('<link rel="stylesheet" href="/fonts.css">',
                  '<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">\n'
                  '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="stylesheet" href="/fonts.css">', 1)
    chemin.write_text(t, encoding="utf-8")
    print("icônes :", icones(choix))


if __name__ == "__main__":
    apercu() if sys.argv[1] == "apercu" else site(sys.argv[2])
