"""
Prépare les photos de la version 2 du site (charte V1.4, octobre 2026).

Pour chaque photo : un .avif (lu par les navigateurs récents, très léger) et un
.webp (pour les autres), dans site-unseen/img/. Les photos sources sont les
originaux rangés dans ~/Documents/UNSEEN./ (Pexels, LUX*, Heritage).

Lancer, depuis le dossier du projet :
    assistant-prospection/venv/bin/python site-unseen/outils/images_v14.py
"""
from pathlib import Path
from PIL import Image, ImageOps

IMG = Path(__file__).resolve().parent.parent / "img"
DOCS = Path.home() / "Documents" / "UNSEEN."
PEX = DOCS / "Photos libres de droit (Pexels)"
LUX = DOCS / "prestataire" / "LUX" / "Photos LUX (galeries officielles)"

# nom dans le site : (photo source, largeur maximale en pixels)
PHOTOS = {
    # Accueil
    "hero-2": (PEX / "pexels-jan-tang-598592438-39133585.jpg", 2000),
    "v2-stay": (PEX / "pexels-eugenia-remark-5767088-31588353.jpg", 1100),
    "v2-dining": (PEX / "pexels-lens-clickk-2148991298-30479386.jpg", 1100),
    "v2-access": (PEX / "pexels-filipgrobgaard-15416899.jpg", 1100),
    "v2-shopping": (PEX / "pexels-umudicreative-18046813.jpg", 1100),
    "v2-transport": (PEX / "pexels-moonlightshotz-11139383.jpg", 1100),
    "v2-season": (PEX / "pexels-julieaagaard-2096983.jpg", 1100),
    "v2-evening": (PEX / "pexels-flavionascimento-40041430.jpg", 1100),
    "v2-paris": (PEX / "pexels-jvas71-10674585.jpg", 1400),
    "v2-alps": (PEX / "pexels-andreasebnerfotografie-31299068.jpg", 1100),
    "v2-riviera": (PEX / "pexels-reinaypa-alvarez-2148254549-37958994.jpg", 1100),
    "v2-mauritius": (LUX / "maurice - luxlemorne" / "01_plage_llm_beach_1.jpg", 1400),
    "v2-now-ski": (PEX / "pexels-andreasebnerfotografie-12404364.jpg", 900),
    "v2-now-gp": (PEX / "pexels-ermal-a-murati-1676092345-37460936.jpg", 900),
    # Professionals
    # « Qui nous sommes » (27/10) : photo choisie pour les PDF partenaires, jamais utilisée sur le site
    "pro-qui": (Path(__file__).resolve().parents[2] / "assistant-prospection" / "sources_offre_partenaire" / "images" / "deck" / "v6_entree_palace.jpg", 1100),
    "pro-hero": (PEX / "pexels-katie-cerami-110690626-20562287.jpg", 2000),
    "pro-bar": (PEX / "pexels-benhur-emmanuel-83498627-11828428.jpg", 1100),
    "pro-agencies": (PEX / "pexels-eray-altay-2187659-3834352.jpg", 1200),
    "pro-aviation": (PEX / "pexels-autotrade-design-424968731-17246680.jpg", 1200),
    "pro-sport": (PEX / "pexels-waqas-ilyas-81841622-36877065.jpg", 1200),
    "pro-embassy": (PEX / "pexels-jean-paul-wettstein-677916508-30266395.jpg", 1200),
    "pro-events": (PEX / "pexels-agustina-croce-302580711-13411720.jpg", 1200),
    "pro-hotels": (LUX / "maurice - luxbellemare" / "01_restaurantsbars_lbm_mondo_1.jpg", 1200),
    # Paris
    "paris-hero": (PEX / "pexels-ivan-drazic-20457695-29730792.jpg", 2000),
    "paris-faubourg": (PEX / "pexels-matreding-14806248.jpg", 1000),
    "paris-montaigne": (PEX / "pexels-raylarinda-sehrin-2153377292-32693037.jpg", 1000),
    "paris-vendome": (PEX / "pexels-lstan-39662961.jpg", 1000),
    "paris-tour": (PEX / "pexels-resul-muslu-1241786177-32392380.jpg", 1000),
    "paris-toits": (PEX / "pexels-arsonela-32534994.jpg", 1000),
    "paris-seine": (PEX / "pexels-kirandeepsingh-16909140.jpg", 1000),
    "paris-m1": (PEX / "pexels-ameliacui-4331639.jpg", 900),
    "paris-m2": (PEX / "pexels-eugenia-remark-5767088-18045516.jpg", 900),
    "paris-m3": (PEX / "pexels-takatak-34687788.jpg", 900),
    "paris-m4": (PEX / "pexels-travel-with-lenses-734723610-30596983.jpg", 900),
    # Maurice (photos LUX*, accord donné le 26/10/2026)
    "maurice-hero": (LUX / "maurice - luxgrandgaube" / "06_architecture_lgg_aerial_2.jpg", 2000),
    "maurice-lemorne": (LUX / "maurice - luxlemorne" / "10_plage_llm_beach_2.jpg", 1000),
    "maurice-bellemare": (LUX / "maurice - luxbellemare" / "05_plagepiscine_lbm_beach_1.jpg", 1000),
    "maurice-grandbaie": (LUX / "maurice - luxgrandbaie" / "04_aerial_lgb_aerial_4.jpg", 1000),
    "maurice-grandgaube": (LUX / "maurice - luxgrandgaube" / "01_plage_lgg_beach_1.jpg", 1000),
    "maurice-reunion": (LUX / "reunion - luxsaintgilles" / "04_aerial_lsg_aerial_1.jpg", 1000),
    "maurice-maldives": (LUX / "maldives - luxsouthariatoll" / "01_vuesaériennes_lsaa_aerial_1.jpg", 1000),
    "maurice-m1": (LUX / "maurice - luxbellemare" / "07_villas_lbm_prestige-villa.jpg", 900),
    "maurice-m2": (LUX / "maurice - luxlemorne" / "08_piscines_llm_pool_1.jpg", 900),
    "maurice-m3": (LUX / "maurice - luxgrandbaie" / "02_restaurantsbars_lgb-beach-rouge_cover.jpg", 900),
    "maurice-m4": (LUX / "maldives - luxsouthariatoll" / "02_villaspavillons_lsaa_lux-villa_1.jpg", 900),
    # Riviera (photos choisies par Jay le 26/10)
    "riviera-hero": (PEX / "pexels-hudson-mcdonald-692563691-28193003.jpg", 2200),
    "riviera-monaco": (PEX / "pexels-mustafa-tunahan-yazici-712218731-18501146.jpg", 1000),
    "riviera-tropez": (PEX / "pexels-romouz-sadeq-796619306-27849870.jpg", 1000),
    "riviera-cannes": (PEX / "pexels-fundademirtas-30575584.jpg", 1000),
    "riviera-ferrat": (PEX / "pexels-lisa-325143818-13766320.jpg", 1000),
    "riviera-eze": (PEX / "pexels-metaxstudios-39359166.jpg", 1000),
    "riviera-mer": (PEX / "pexels-tahir-osman-109306362-28242421.jpg", 1000),
    "riviera-m1": (PEX / "pexels-sanne-van-houts-1102643-30645939.jpg", 900),
    "riviera-m2": (PEX / "pexels-larissafarber-29205614.jpg", 900),
    "riviera-m3": (PEX / "pexels-matteo-milan-136935423-18030809.jpg", 900),
    "riviera-m4": (PEX / "pexels-earth-photart-2149767641-38030480.jpg", 900),
}

DEJA = set()  # rempli au lancement : on ne refait que les photos absentes


def preparer(nom, source, largeur):
    im = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    if im.width > largeur:
        im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
    im.save(IMG / f"{nom}.webp", "WEBP", quality=74, method=6)
    im.save(IMG / f"{nom}.avif", "AVIF", quality=58)
    return (IMG / f"{nom}.avif").stat().st_size + (IMG / f"{nom}.webp").stat().st_size


if __name__ == "__main__":
    total = 0
    for nom, (source, largeur) in PHOTOS.items():
        if (IMG / f"{nom}.avif").exists():
            continue
        total += preparer(nom, source, largeur)
        print("ok", nom)
    print(f"Total : {total / 1e6:.1f} Mo (avif + webp)")
