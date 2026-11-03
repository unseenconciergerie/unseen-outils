"""
Version « téléphone » des photos de la page d'accueil (contrôle PageSpeed du 03/11/2026 :
les photos étaient téléchargées en 1100 px de large alors qu'elles s'affichent en 300 px).

Pour chaque photo v2-*, on crée une copie de 760 px de large (AVIF et WebP) :
  img/v2-xxx-760.avif et img/v2-xxx-760.webp
Les originaux ne sont JAMAIS modifiés. Le navigateur choisit tout seul : un écran large ou un
iPhone très haute définition garde l'original, un téléphone plus modeste prend la copie légère.
Les logos de partenaires ne sont pas touchés (réduits, ils n'étaient pas plus légers).

    assistant-prospection/venv/bin/python site-unseen/outils/images_mobile.py
"""
from pathlib import Path

from PIL import Image

IMG = Path(__file__).resolve().parent.parent / "img"
LARGEUR = 760
PHOTOS = ["access", "alps", "dining", "evening", "mauritius", "now-gp", "now-ski",
          "paris", "riviera", "season", "shopping", "stay", "transport"]

for nom in PHOTOS:
    im = Image.open(IMG / f"v2-{nom}.avif").convert("RGB")
    petit = im.resize((LARGEUR, round(im.height * LARGEUR / im.width)), Image.LANCZOS)
    petit.save(IMG / f"v2-{nom}-{LARGEUR}.avif", "AVIF", quality=58)
    petit.save(IMG / f"v2-{nom}-{LARGEUR}.webp", "WEBP", quality=80)
    print(nom, im.size, "->", petit.size,
          (IMG / f"v2-{nom}.avif").stat().st_size // 1024, "Ko ->",
          (IMG / f"v2-{nom}-{LARGEUR}.avif").stat().st_size // 1024, "Ko (avif)")
