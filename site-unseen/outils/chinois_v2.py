"""
Chinois du site, relecture du 27/10/2026 : corrige les calques de l'anglais, les faux sens et
les noms de lieux incohérents ; ajoute le chinois à la page d'erreur (404), qui n'en avait pas.
Le chinois reste écrit directement en chinois (simplifié), jamais traduit mot à mot.

Deux usages, depuis le dossier du projet :
    python3 site-unseen/outils/chinois_v2.py comparer   → page « avant / après » pour Jay
    python3 site-unseen/outils/chinois_v2.py appliquer  → modifie les pages (après accord de Jay)
"""
import html
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "professionals.html", "paris.html", "riviera.html", "ocean-indien.html",
         "saison-ski-2026-2027.html", "formule-1.html"]
COMPARAISON = SITE.parent / "Livrables" / "Maquettes site (évolution)" / "15 Chinois corrigé, avant-après (27-10).html"

# clé = anglais exact ; valeur = (nouveau chinois, pourquoi, expliqué en français pour Jay)
CORRIGE = {
    "Professionals": ("专业合作", "« 合作伙伴 » veut dire « Partenaires » : c'était le même mot que la section des logos."),
    "Access": ("入场", "« 通行 » = droit de passage (calque d'« access ») ; « 入场 » = l'entrée à un événement."),
    "Events and access": ("赛事与专属入场", "Même raison : « 活动与通行 » sonnait comme un panneau de circulation."),
    "Shopping and sourcing": ("私人购物与珍品寻觅", "« 寻源 » est du jargon d'achats industriels ; « 珍品寻觅 » = la recherche de pièces rares."),
    "Chauffeurs who know the city and never talk about it, airport and terminal transfers, long-distance journeys, and a helicopter leg where the road would cost three hours.":
        ("熟悉城市、守口如瓶的专属司机，机场与火车站接送，长途出行；若开车要三小时，便改乘直升机。",
         "« 熟悉城市却绝口不提 » était un calque ; « terminal » avait été traduit « aérogare » au lieu de « gare »."),
    "Afterwards": ("离开之后", "« 此后 » (« dorénavant ») ne voulait rien dire comme titre ; « 离开之后 » = « après votre départ »."),
    "Personal shopping and maisons": ("私人购物与奢侈品牌", "« 品牌之家 » est un calque de « maisons » ; « 奢侈品牌 » = les grandes marques de luxe."),
    "Paris, from the inside.": ("走进真正的巴黎。", "« 由内而知 » n'existe pas en chinois ; « 走进真正的巴黎 » = « entrer dans le vrai Paris »."),
    "Addresses": ("去处", "« 地址 » = adresse postale ; « 去处 » = les endroits où aller."),
    "What you do": ("玩些什么", "« 做些什么 » sonnait comme une question de travail ; « 玩些什么 » = « que faire, quoi découvrir »."),
    "How you move": ("出行方式", "« 如何往来 » était maladroit ; « 出行方式 » = « comment se déplacer »."),
    "A late check-out, held for you.": ("确保延迟退房。", "Plus naturel : « le late check-out, garanti »."),
    "A helicopter over the cirques and the waterfalls.": ("乘直升机飞越峡谷盆地与瀑布。",
        "Faux sens : « 冰斗 » est un cirque glaciaire ; ceux de La Réunion sont des cirques volcaniques (« 峡谷盆地 »)."),
    "Courchevel in late December. Gstaad the week after. A late addition to Val d'Isère, three days before the children arrive. We hold the season a step ahead, so nothing is left to chance once you're there.":
        ("十二月下旬在库舍维尔，下一周去格施塔德，孩子们抵达前三天，又临时加上瓦勒迪泽尔。我们始终比雪季快一步，让您到了之后，一切都不靠运气。",
         "Noms de stations incohérents (« 库尔雪维尔 », « 伊瑟尔河谷 ») : alignés sur ceux du reste du site (« 库舍维尔 », « 瓦勒迪泽尔 »)."),
    "Val d'Isère": ("瓦勒迪泽尔", "Nom chinois usuel de la station, le même que sur la page Professionnels."),
    "The reference. 1850 for the address, the altitude restaurants, the boutiques that stay open past dinner.":
        ("标杆之选。库舍维尔1850的顶级地段、高山餐厅，以及晚餐后仍在营业的精品店。",
         "« 1850高度的地段 » laissait croire à une altitude ; on nomme Courchevel 1850, comme en français."),
    "A helicopter to the Glacier 3000.": ("乘直升机前往Glacier 3000冰川。", "Le nom propre du glacier avait été coupé (« 3000冰川 »)."),
    "Formula 1": ("一级方程式赛车", "« F1方程式赛车 » répétait « formule » deux fois."),
    "Private transport to the circuit, door to grid.": ("私人专车直达赛道，从酒店门口一路送到发车区。",
        "Faux sens : « 维修区 » est le paddock ; « door to grid » = jusqu'à la grille de départ (« 发车区 »)."),
    "Your itinerary stays yours. We add what a local team can open: tables, suites, access, drivers, and the last-minute changes.":
        ("行程依旧属于您。我们补上只有本地团队才能拿到的部分：餐桌、套房、特别通道、专车，以及最后一刻的变动。",
         "« 准入 » est un terme administratif (autorisation officielle) ; « 特别通道 » = les accès privilégiés."),
    "Choose yours: what we do for you, and what a request looks like, start to finish.":
        ("请选择您的行业：我们能为您做什么，以及一次完整的行程示例。", "La page montre maintenant un exemple de programme : la phrase le dit, comme en français."),
}

# Page d'erreur : chinois ajouté (elle n'en avait pas)
ZH_404 = {
    "Error 404": "错误 404",
    "This page stayed unseen.": "这一页，未曾现身。",
    "The address you followed does not lead anywhere. It may have moved, or never existed at all.": "您访问的链接无法打开。页面可能已经移动，或者从未存在。",
    "Back to the site": "返回网站",
    "Write to us": "联系我们",
}

MOTIF = re.compile(r'data-en="([^"]*)" data-fr="([^"]*)" data-zh="([^"]*)"')


def comparer():
    lignes, vus = [], set()
    for nom in PAGES:
        for en, _, zh in MOTIF.findall((SITE / nom).read_text(encoding="utf-8")):
            en, zh = html.unescape(en), html.unescape(zh)
            if en in CORRIGE and en not in vus:
                vus.add(en)
                nouveau, pourquoi = CORRIGE[en]
                lignes.append((nom, en, zh, nouveau, pourquoi))
    oublies = set(CORRIGE) - vus
    assert not oublies, f"introuvables : {oublies}"
    for en, zh in ZH_404.items():
        lignes.append(("404.html", en, "(pas de chinois)", zh, "La page d'erreur s'affichait en anglais pour un visiteur chinois."))
    rangs = "".join(f"<tr><td class='p'>{n}</td><td>{html.escape(e)}</td><td class='z'>{html.escape(a)}</td>"
                    f"<td class='z n'>{html.escape(b)}</td><td>{html.escape(w)}</td></tr>" for n, e, a, b, w in lignes)
    COMPARAISON.write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Chinois corrigé, avant-après</title>
<style>body{{font-family:-apple-system,system-ui,sans-serif;max-width:1300px;margin:0 auto;padding:24px 16px;color:#1c1b1e;background:#fff}}
table{{width:100%;border-collapse:collapse;margin-top:14px}}th{{text-align:left;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#8a8083;padding:6px 8px}}
td{{vertical-align:top;padding:10px 8px;border-top:1px solid #eee;font-size:14.5px;line-height:1.5}}.p{{color:#8a8083;font-size:12px}}
.z{{font-size:16px}}.n{{background:#f4eae5}}
@media(max-width:800px){{tr{{display:block;border-top:1px solid #ddd;padding:6px 0}}th{{display:none}}td{{display:block;border:0;padding:4px 8px}}}}</style></head>
<body><h1>Chinois du site : corrections, avant / après</h1>
<p>{len(lignes)} corrections le 27/10/2026. La dernière colonne explique chaque changement en français. Pour vérifier le sens d'une phrase, collez la colonne « Après » dans DeepL. Rien n'est en ligne avant votre accord.</p>
<table><tr><th>Page</th><th>Anglais (le sens)</th><th>Avant</th><th>Après</th><th>Pourquoi</th></tr>{rangs}</table></body></html>""", encoding="utf-8")
    print(f"{len(lignes)} corrections, page : {COMPARAISON}")


def appliquer():
    for nom in PAGES:
        chemin = SITE / nom
        page, n = chemin.read_text(encoding="utf-8"), 0

        def remplace(m):
            nonlocal n
            en = html.unescape(m.group(1))
            if en not in CORRIGE:
                return m.group(0)
            n += 1
            return f'data-en="{m.group(1)}" data-fr="{m.group(2)}" data-zh="{html.escape(CORRIGE[en][0])}"'

        chemin.write_text(MOTIF.sub(remplace, page), encoding="utf-8")
        print(f"{nom} : {n} textes corrigés")

    # Page d'erreur : ajoute data-zh et le choix du chinois dans son petit script de langue
    chemin = SITE / "404.html"
    page = chemin.read_text(encoding="utf-8")
    assert "data-zh" not in page, "404 déjà traitée"
    for en, zh in ZH_404.items():
        motif = re.compile(r'(data-en="' + re.escape(html.escape(en)).replace("'", "(?:'|&#x27;)") + r'" data-fr="[^"]*")')
        page, k = motif.subn(lambda m: m.group(1) + f' data-zh="{html.escape(zh)}"', page)
        assert k == 1, en
    ancien = """  var fr = choix === 'fr' ||
           (!choix && (navigator.language || '').toLowerCase().indexOf('fr') === 0);
  if (!fr) return;
  document.documentElement.lang = 'fr';
  var noeuds = document.querySelectorAll('[data-fr]');
  for (var i = 0; i < noeuds.length; i++){
    noeuds[i].textContent = noeuds[i].getAttribute('data-fr');"""
    nouveau = """  var nav = (navigator.language || '').toLowerCase();
  var l = (choix === 'fr' || choix === 'zh') ? choix
        : (!choix && nav.indexOf('zh') === 0) ? 'zh'
        : (!choix && nav.indexOf('fr') === 0) ? 'fr' : null;
  if (!l) return;
  document.documentElement.lang = l;
  var noeuds = document.querySelectorAll('[data-' + l + ']');
  for (var i = 0; i < noeuds.length; i++){
    noeuds[i].textContent = noeuds[i].getAttribute('data-' + l);"""
    assert page.count(ancien) == 1, "script de la 404 différent de prévu"
    chemin.write_text(page.replace(ancien, nouveau), encoding="utf-8")
    print("404.html : chinois ajouté")


if __name__ == "__main__":
    {"comparer": comparer, "appliquer": appliquer}[sys.argv[1]]()
