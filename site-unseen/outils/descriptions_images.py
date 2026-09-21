"""
Ajoute une description à chaque photo du site (l'attribut "alt").

À quoi ça sert : Google ne sait pas regarder une image. Il lit cette
description pour comprendre ce qu'elle montre. Sans elle, les photos du site
n'existent pas pour lui. Avec elle, elles peuvent ressortir dans Google Images.
La description ne s'affiche jamais à l'écran.

Le site étant bilingue, chaque photo reçoit les deux versions, sur le même
principe que le reste de la page : data-alt-en et data-alt-fr. La bascule
EN/FR du site s'occupe d'échanger l'une pour l'autre.

Lancement :  python3 site-unseen/outils/descriptions_images.py
"""

import re
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "index.html"

# Une description par photo : (anglais, français).
# Elles décrivent ce que l'on voit, simplement. Pas d'accumulation de
# mots-clés : Google pénalise, et ça ne se lit pas.
DESCRIPTIONS = {
    "hero": ("The illuminated top of the Eiffel Tower at night above Paris",
             "Le sommet illuminé de la tour Eiffel la nuit au-dessus de Paris"),

    # les huit services
    "s-stay": ("The domes of a Monte-Carlo palace hotel against a clear sky",
               "Les coupoles d'un palace de Monte-Carlo sur un ciel dégagé"),
    "s-table": ("A sushi chef preparing a piece at the counter",
                "Un chef sushi préparant une pièce au comptoir"),
    "s-access": ("Formula 1 cars lined up in the pit lane before the start",
                 "Les Formule 1 alignées dans la voie des stands avant le départ"),
    "s-wardrobe": ("Handbags displayed on the shelves of a luxury boutique",
                   "Des sacs exposés sur les étagères d'une boutique de luxe"),
    "s-transport": ("A black chauffeur-driven car waiting at night",
                    "Une berline noire avec chauffeur attendant de nuit"),
    "s-evening": ("The gilded boxes and chandeliers of an opera house",
                  "Les loges dorées et les lustres d'un opéra"),
    "s-charter": ("Yachts moored in a Mediterranean marina",
                  "Des yachts amarrés dans un port de Méditerranée"),
    "s-sport": ("The front wing and tyre of a Formula 1 car",
                "L'aileron avant et le pneu d'une Formule 1"),

    # les trois destinations
    "d-paris": ("The rooftops of Paris at dusk, seen from above",
                "Les toits de Paris au crépuscule, vus d'en haut"),
    "d-europe": ("A seafront palace hotel lit up at night on the French Riviera",
                 "Un palace en bord de mer illuminé la nuit sur la Côte d'Azur"),
    "d-ocean": ("Overwater villas on a turquoise lagoon in the Indian Ocean",
                "Des villas sur pilotis au-dessus d'un lagon turquoise de l'océan Indien"),

    # le bandeau
    "band": ("An empty theatre auditorium, prepared before the audience arrives",
             "Une salle de spectacle vide, préparée avant l'arrivée du public"),

    # les trois saisons
    "y-summer": ("The coastline of Monaco at sunset",
                 "La côte de Monaco au coucher du soleil"),
    "y-winter": ("A wooden chalet under snow beside a cable car in the Alps",
                 "Un chalet de bois sous la neige près d'une télécabine dans les Alpes"),
    "y-calendar": ("Formula 1 cars through a corner during a Grand Prix",
                   "Des Formule 1 dans un virage pendant un Grand Prix"),

    # la mosaïque du bas
    "g1": ("The clay court at Roland-Garros during a match",
           "Le court en terre battue de Roland-Garros pendant un match"),
    "g2": ("A waterfall in the tropical forest of Mauritius",
           "Une cascade dans la forêt tropicale de Maurice"),
    "g3": ("Palm trees below Le Morne mountain in Mauritius",
           "Des palmiers au pied de la montagne du Morne à Maurice"),
    "g4": ("A turquoise lagoon and its reef seen from the air",
           "Un lagon turquoise et son récif vus du ciel"),
    "g5": ("A white sand beach and turquoise water seen from above",
           "Une plage de sable blanc et une eau turquoise vues d'en haut"),
    "g6": ("A lit garden and its reflecting pool at nightfall",
           "Un jardin éclairé et son bassin à la tombée de la nuit"),
    "g7": ("The Eiffel Tower against a clear blue sky",
           "La tour Eiffel sur un ciel bleu dégagé"),
    "g8": ("Tower Bridge lit up at night in London",
           "Le Tower Bridge illuminé la nuit à Londres"),
}


def echapper(texte):
    """Protège les guillemets, qui fermeraient l'attribut avant l'heure."""
    return texte.replace('"', "&quot;")


def decrire(balise):
    """Remplace alt="" par la description, dans les deux langues."""
    code = balise.group(0)
    nom = re.search(r'src="img/([^."]+)\.webp"', code)
    if not nom:
        return code

    paire = DESCRIPTIONS.get(nom.group(1))
    if not paire:
        return code                      # photo sans description prévue

    en, fr = echapper(paire[0]), echapper(paire[1])
    # La page s'ouvre en anglais : alt porte l'anglais, et les deux
    # attributs data- permettent à la bascule de langue de l'échanger.
    return code.replace('alt=""',
                        f'alt="{en}" data-alt-en="{en}" data-alt-fr="{fr}"')


def main():
    html = PAGE.read_text(encoding="utf-8")

    if "data-alt-en" in html:
        print("Les descriptions sont déjà en place, rien à faire.")
        return

    html, nombre = re.subn(r'<img[^>]*src="img/[^."]+\.webp"[^>]*>', decrire, html)
    PAGE.write_text(html, encoding="utf-8")

    decrites = html.count("data-alt-en")
    print(f"{decrites} photos sur {nombre} ont reçu une description, en anglais et en français.")


if __name__ == "__main__":
    main()
