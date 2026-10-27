"""
Allège les photos trop lourdes signalées par le contrôle technique du 27/10/2026 (page Formule 1
et grande photo de Paris) : largeur ramenée à ce qu'un écran affiche vraiment, formats AVIF et
WebP comme le reste du site, JPG de secours plus léger. Qualité visuelle gardée (mêmes réglages
que images_v14.py). Les originaux d'avant sont gardés dans le dossier temporaire de la session.

    assistant-prospection/venv/bin/python site-unseen/outils/alleger_photos.py
"""
from pathlib import Path

from PIL import Image, ImageOps

IMG = Path(__file__).resolve().parent.parent / "img"
# nom : (fichier source, largeur maximale)
PHOTOS = {
    "f1-monaco-port": ("f1-monaco-port.jpg", 2000),   # grande photo du haut de page
    "f1-monaco-circuit": ("f1-monaco-circuit.jpg", 1400),
    "f1-nuit": ("f1-nuit.jpg", 1200),                 # photos verticales : 1200 suffit
    "f1-paddock": ("f1-paddock.jpg", 1200),
    "f1-piste": ("f1-piste.jpg", 1200),
    "f1-detail": ("f1-detail.jpg", 1400),
    "paris-hero": ("paris-hero.webp", 1800),
}

for nom, (source, largeur) in PHOTOS.items():
    im = ImageOps.exif_transpose(Image.open(IMG / source)).convert("RGB")
    if im.width > largeur:
        im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
    avant = sum((IMG / f"{nom}.{e}").stat().st_size for e in ("avif", "webp", "jpg") if (IMG / f"{nom}.{e}").exists())
    im.save(IMG / f"{nom}.avif", "AVIF", quality=58)
    im.save(IMG / f"{nom}.webp", "WEBP", quality=74, method=6)
    if (IMG / f"{nom}.jpg").exists():
        im.save(IMG / f"{nom}.jpg", "JPEG", quality=80, optimize=True, progressive=True)
    apres = sum((IMG / f"{nom}.{e}").stat().st_size for e in ("avif", "webp", "jpg") if (IMG / f"{nom}.{e}").exists())
    print(f"{nom:20} {im.width}x{im.height}  avif {(IMG / f'{nom}.avif').stat().st_size // 1024} Ko, "
          f"webp {(IMG / f'{nom}.webp').stat().st_size // 1024} Ko  (total {avant // 1024} -> {apres // 1024} Ko)")
