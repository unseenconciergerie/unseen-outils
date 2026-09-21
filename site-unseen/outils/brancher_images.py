"""
Branche le site sur les nouvelles images AVIF et WebP.

Remplace dans index.html chaque balise de ce genre :

    <img src="img/hero.jpg" alt="">

par celle-ci :

    <picture><source type="image/avif" srcset="img/hero.avif"><img src="img/hero.webp" alt=""></picture>

Le navigateur lit la liste de haut en bas et prend le premier format qu'il
comprend : l'AVIF pour tous les navigateurs récents, le WebP pour les autres.

Le script ne touche pas à l'image de partage (og:image), qui doit rester
un JPG : Facebook, LinkedIn et WhatsApp ne savent pas lire l'AVIF.

Lancement :  python3 site-unseen/outils/brancher_images.py
"""

import re
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "index.html"


def convertir(balise):
    """Enveloppe une balise <img src="img/x.jpg"> dans un <picture>."""
    nom = re.search(r'src="img/([^."]+)\.jpg"', balise.group(0)).group(1)
    interieur = balise.group(0).replace(f'img/{nom}.jpg', f'img/{nom}.webp')
    return (f'<picture><source type="image/avif" srcset="img/{nom}.avif">'
            f'{interieur}</picture>')


def main():
    html = PAGE.read_text(encoding="utf-8")

    if "<picture>" in html:
        print("Les balises <picture> sont déjà en place, rien à faire.")
        return

    # On ne touche qu'aux balises <img>, jamais aux <meta> de partage
    html, nombre = re.subn(r'<img[^>]*src="img/[^."]+\.jpg"[^>]*>', convertir, html)

    # Une balise <picture> forme une boîte supplémentaire autour de l'image.
    # Sans cette règle, les images des cartes perdraient leur hauteur.
    css = "picture{display:block;width:100%;height:100%}\n"
    html = html.replace("/* ---------- mosaique ---------- */",
                        f"/* les images sont servies en AVIF avec repli WebP */\n{css}\n/* ---------- mosaique ---------- */")

    PAGE.write_text(html, encoding="utf-8")
    print(f"{nombre} images branchées sur l'AVIF, avec repli WebP.")


if __name__ == "__main__":
    main()
