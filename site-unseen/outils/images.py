"""
Prépare toutes les images du site UNSEEN. à partir des photos d'origine.

Ce que fait ce script :
  1. il reprend chaque photo en haute définition (dossier Bureau/UNSEEN./photo unsplash)
  2. il la recadre au format exact où le site l'affiche
  3. il la réduit à la taille utile (jamais plus grande que l'original)
  4. il l'enregistre en AVIF (format moderne, très léger) et en WebP (secours)

Pourquoi deux formats : l'AVIF pèse deux à trois fois moins lourd qu'un JPG
à qualité égale, mais les navigateurs d'avant 2023 ne le lisent pas. Le WebP
sert de filet de sécurité pour eux. Le site choisit tout seul le bon fichier.

Lancement :  python3 site-unseen/outils/images.py
"""

from pathlib import Path
from PIL import Image, ImageOps

# ---------------------------------------------------------------- dossiers

RACINE = Path(__file__).resolve().parent.parent      # site-unseen/
SORTIE = RACINE / "img"                              # où atterrissent les images
ORIGINAUX = Path.home() / "Desktop" / "UNSEEN." / "photo unsplash"

# ---------------------------------------------------------------- réglages

# Qualité AVIF. Attention : l'échelle de l'AVIF n'est pas celle du JPG.
# Un AVIF à 52 correspond à peu près à un JPG à 85, en trois fois plus léger.
QUALITE_AVIF = 52
# "4:2:0" allège la couleur sans toucher au détail (l'œil voit mal les nuances
# de couleur, très bien les contours). "speed=3" encode plus lentement mais
# plus finement : on ne le fait qu'une fois, autant le faire bien.
AVIF_OPTIONS = dict(subsampling="4:2:0", speed=3)

# Le WebP ne sert qu'aux vieux navigateurs : un peu plus petit et plus compressé,
# personne ne le remarquera, et cela économise le quota d'hébergement.
QUALITE_WEBP = 74
REDUCTION_WEBP = 0.8

# ---------------------------------------------------------------- catalogue
#
# Pour chaque image du site :
#   source   : le fichier d'origine ("site" = on garde l'image actuelle,
#              faute d'avoir l'original en haute définition)
#   ratio    : la forme dans laquelle le site l'affiche (largeur / hauteur)
#   largeur  : la largeur du fichier à produire, calculée sur la taille
#              d'affichage réelle multipliée par deux pour les écrans Retina
#   centrage : quel point de la photo garder au recadrage (0.5 = le centre,
#              0 = le haut ou la gauche, 1 = le bas ou la droite)

CATALOGUE = {
    # --- ouverture : trois photos qui se succèdent en fondu, plein écran ---
    # Toutes nocturnes et parisiennes, pour que l'enchaînement reste discret.
    "hero":       dict(source="michael-pointner-ekenpbomYY4-unsplash.jpg", ratio=16/9, largeur=2000),
    "hero-2":     dict(source="thijs-x5NotAuHLAg-unsplash.jpg",            ratio=16/9, largeur=2000, centrage=(0.5, 0.6)),
    "hero-3":     dict(source="francesco-zivoli-jEAE4T27Gi8-unsplash.jpg", ratio=16/9, largeur=2000, centrage=(0.5, 0.4)),

    # --- bandeau éditorial pleine largeur ---
    # "la part la plus utile de ce metier est celle que vous ne voyez jamais" :
    # une salle entiere prete, avant que personne n'arrive.
    "band":       dict(source="luis-gherasim-MJ41r9C3oxU-unsplash.jpg",     ratio=2/1,  largeur=1900),

    # --- les huit cartes de services : affichées à ~280 px, format portrait 4:5 ---
    "s-stay":     dict(source="site",                                       ratio=4/5, largeur=700),
    "s-table":    dict(source="antonio-araujo-G1sU_-iyU2E-unsplash.jpg",    ratio=4/5, largeur=700),
    "s-access":   dict(source="marc-kleen-8CqwTEGPLmo-unsplash.jpg",        ratio=4/5, largeur=700),
    "s-wardrobe": dict(source="IMG_6517.jpeg",                              ratio=4/5, largeur=700),
    "s-transport":dict(source="glenn-villas-KMNPw-5Au64-unsplash.jpg",      ratio=4/5, largeur=700),
    "s-evening":  dict(source="giusi-borrasi-eH-IOSeI0Yk-unsplash.jpg",     ratio=4/5, largeur=700),
    "s-charter":  dict(source="philip-myrtorp-Y7mbRjf9T9s-unsplash.jpg",    ratio=4/5, largeur=700),
    "s-sport":    dict(source="sam-tsonis-AK0SbB8bvr4-unsplash.jpg",        ratio=4/5, largeur=700),

    # --- les trois destinations : demi-largeur de page, soit ~635 px ---
    "d-paris":    dict(source="tuna-ekici-yYiQYpyZ2gE-unsplash.jpg", ratio=3/2, largeur=1300, centrage=(0.5, 0.45)),
    "d-europe":   dict(source="site",                                ratio=3/2, largeur=1300),
    "d-ocean":    dict(source="site",                                ratio=3/2, largeur=1300),

    # --- les trois saisons : un tiers de page, soit ~386 px, format 16:9 ---
    "y-summer":   dict(source="site",                                    ratio=16/9, largeur=900),
    "y-winter":   dict(source="rayyan-9uqZZFTp-Lc-unsplash.jpg",         ratio=16/9, largeur=900),
    "y-calendar": dict(source="matys-ouvrard-KJuB7nTF58k-unsplash.jpg",  ratio=16/9, largeur=900),

    # --- les sept destinations de la carte : bandeau fin en tête de fiche ---
    # Format très panoramique (3:1) pour illustrer le lieu sans repousser la
    # liste des partenaires hors de l'écran.
    "m-paris":      dict(source="christian-dubendorfer-aK2L4SzQDV4-unsplash.jpg",    ratio=3/1, largeur=1100),
    "m-london":     dict(source="site-g8",                                           ratio=3/1, largeur=1100),
    "m-sainttropez":dict(source="pexels-guillaume-dhalluin-2159303303-35975998.jpg", ratio=3/1, largeur=1100),
    "m-cannes":     dict(source="julien-lanoy--m7dpaWPV3Q-unsplash.jpg",             ratio=3/1, largeur=1100),
    "m-monaco":     dict(source="mark-de-jong-mYoOSPFRO00-unsplash.jpg",             ratio=3/1, largeur=1100, centrage=(0.5, 0.78)),
    "m-alps":       dict(source="tim-arnold-k6h9FTRmUso-unsplash.jpg",               ratio=3/1, largeur=1100),
    "m-mauritius":  dict(source="saad-khan-425b2PhNuHA-unsplash.jpg",                ratio=3/1, largeur=1100),

    # --- la mosaïque du bas : quatre colonnes pleine largeur, soit ~480 px ---
    "g1": dict(source="aleksandr-galichkin-dOUMF7aEsYs-unsplash.jpg", ratio=4/5, largeur=1000),
    "g2": dict(source="site", ratio=4/5, largeur=1000),
    "g3": dict(source="site", ratio=4/5, largeur=1000),
    "g4": dict(source="site", ratio=4/5, largeur=1000),
    "g5": dict(source="site", ratio=4/5, largeur=1000),
    "g6": dict(source="site", ratio=4/5, largeur=1000),
    "g7": dict(source="alex-avila-fUWZKKYxbrI-unsplash.jpg", ratio=4/5, largeur=1000),
    "g8": dict(source="site", ratio=4/5, largeur=1000),
}


def charger(nom, source):
    """Ouvre la photo d'origine, ou une image actuelle du site si on n'a pas mieux.

    "site"      : reprend l'image du site qui porte le même nom
    "site-xxx"  : reprend l'image du site nommée xxx (pour la réutiliser ailleurs)
    autre       : nom de fichier dans le dossier des photos d'origine
    """
    if source == "site":
        chemin = SORTIE / f"{nom}.jpg"
    elif source.startswith("site-"):
        chemin = SORTIE / f"{source[5:]}.jpg"
    else:
        chemin = ORIGINAUX / source
    if not chemin.exists():
        raise FileNotFoundError(f"{nom} : introuvable → {chemin}")
    image = Image.open(chemin)
    # Certaines photos d'appareil portent une consigne de rotation dans leurs
    # données EXIF : on l'applique, sinon l'image sortirait couchée.
    return ImageOps.exif_transpose(image).convert("RGB"), chemin


def preparer(nom, reglages):
    """Recadre, redimensionne et enregistre une image aux deux formats."""
    image, chemin = charger(nom, reglages["source"])
    ratio = reglages["ratio"]
    centrage = reglages.get("centrage", (0.5, 0.5))

    # On ne dépasse jamais la taille de l'original : agrandir une photo ne
    # crée aucun détail, cela ne fait que la rendre floue et plus lourde.
    largeur_max = min(reglages["largeur"], image.width, int(image.height * ratio))
    largeur = largeur_max
    hauteur = round(largeur / ratio)

    cadree = ImageOps.fit(image, (largeur, hauteur), Image.LANCZOS, centering=centrage)

    cadree.save(SORTIE / f"{nom}.avif", quality=QUALITE_AVIF, **AVIF_OPTIONS)

    largeur_webp = round(largeur * REDUCTION_WEBP)
    secours = cadree.resize((largeur_webp, round(largeur_webp / ratio)), Image.LANCZOS)
    secours.save(SORTIE / f"{nom}.webp", quality=QUALITE_WEBP, method=6)

    return {
        "nom": nom,
        "origine": chemin.name,
        "taille": f"{largeur}x{hauteur}",
        "avif": (SORTIE / f"{nom}.avif").stat().st_size,
        "webp": (SORTIE / f"{nom}.webp").stat().st_size,
        "avant": (SORTIE / f"{nom}.jpg").stat().st_size if (SORTIE / f"{nom}.jpg").exists() else 0,
    }


def main():
    resultats = []
    for nom, reglages in CATALOGUE.items():
        resultats.append(preparer(nom, reglages))
        print(f"  {nom:<12} fait")

    print()
    print(f"{'image':<12} {'format':<11} {'avant':>9} {'AVIF':>9} {'WebP':>9}  origine")
    print("-" * 86)
    for r in resultats:
        print(f"{r['nom']:<12} {r['taille']:<11} "
              f"{r['avant']/1024:8.0f}k {r['avif']/1024:8.0f}k {r['webp']/1024:8.0f}k  {r['origine'][:34]}")

    avant = sum(r["avant"] for r in resultats)
    apres = sum(r["avif"] + r["webp"] for r in resultats)
    print("-" * 86)
    print(f"{'TOTAL':<12} {'':<11} {avant/1048576:8.2f}M {apres/1048576:17.2f}M  (AVIF + WebP réunis)")
    print(f"\nGain : {(avant - apres)/1048576:.2f} Mo libérés sur le quota d'hébergement.")


if __name__ == "__main__":
    main()
