"""
Construit les pages de destination (paris.html, maurice.html) dans le style du nouveau site.

Le gabarit (barre du haut, menu téléphone, langues, pied de page, styles) est repris de
professionals.html, pour que toutes les pages se ressemblent. Textes en trois langues,
le chinois écrit directement. Une photo ne sert que sur une seule page du site.

Lancer, depuis le dossier du projet :
    python3 site-unseen/outils/construire_destinations_v14.py
"""
import html as H
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
GABARIT = (SITE / "professionals.html").read_text(encoding="utf-8")


def q(s):
    return H.escape(s, quote=True)


def t(en, fr, zh, balise="span", attrs=""):
    return f'<{balise}{attrs} data-en="{q(en)}" data-fr="{q(fr)}" data-zh="{q(zh)}">{en}</{balise}>'


def image(nom, alt=("", "", ""), attrs=' loading="lazy"'):
    en, fr, zh = alt
    a = f' alt="{q(en)}" data-alt-en="{q(en)}" data-alt-fr="{q(fr)}" data-alt-zh="{q(zh)}"' if en else ' alt=""'
    return f'<picture><source type="image/avif" srcset="img/{nom}.avif"><img src="img/{nom}.webp"{a}{attrs}></picture>'


CSS_DEST = """
/* Pages de destination */
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:34px;margin-top:52px}
.cardd .ph{aspect-ratio:4/5;overflow:hidden;background:#111;margin-bottom:20px}
.cardd .ph picture{display:block;height:100%}
.cardd .ph img{width:100%;height:100%;object-fit:cover;transition:transform .6s}
.cardd:hover .ph img{transform:scale(1.04)}
.cardd .tag{display:block;font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);font-weight:600;margin-bottom:8px}
.cardd h3{font-size:22px;margin-bottom:8px}
.cardd p{font-size:15.5px;color:var(--texte-2);line-height:1.6}
.rows{list-style:none;margin-top:44px;max-width:780px}
.rows li{display:flex;gap:20px;padding:20px 0;border-top:1px solid rgba(255,255,255,.14);font-size:17px;line-height:1.6}
.rows li:last-child{border-bottom:1px solid rgba(255,255,255,.14)}
.rows li b{color:var(--accent);font-weight:600;font-size:13px;flex:0 0 26px;padding-top:3px}
.cats{display:grid;grid-template-columns:repeat(4,1fr);gap:48px 40px;margin-top:52px}
.cats.trois{grid-template-columns:repeat(3,1fr)}
.cat{border-top:1px solid rgba(255,255,255,.2);padding-top:20px}
.cat .k2{display:block;font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);font-weight:600}
.cat h3{font-size:20px;margin:8px 0 16px}
.cat ul{list-style:none;display:flex;flex-direction:column;gap:12px}
.cat li{position:relative;padding-left:18px;font-size:15px;line-height:1.55;color:#CFC8CA}
.cat li:before{content:"";position:absolute;left:0;top:.8em;width:8px;height:1px;background:var(--accent)}
.cat.large{grid-column:1/-1;display:grid;grid-template-columns:1fr 2fr;gap:0 40px;align-items:start}
.cat.large ul{flex-direction:row;flex-wrap:wrap;gap:12px 40px;padding-top:4px}
.cat.large li{flex:1 1 220px}
@media(max-width:900px){.cats,.cats.trois{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:14px;margin:32px calc(var(--pad) * -1) 0;padding:0 var(--pad) 8px;scroll-padding-left:var(--pad);scrollbar-width:none;-webkit-overflow-scrolling:touch}.cats::-webkit-scrollbar{display:none}.cat,.cat.large{flex:0 0 80%;scroll-snap-align:start;display:block;background:rgba(255,255,255,.04);padding:20px 18px 22px;border-top:2px solid var(--accent)}.cat.large ul{flex-direction:column}.cat.large li{flex:none}}
.mosaic{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;background:#000}
.mosaic figure{margin:0;aspect-ratio:4/5;overflow:hidden}
.mosaic picture{display:block;height:100%}
.mosaic img{width:100%;height:100%;object-fit:cover}
.cta{text-align:center}
.cta .lede{margin:0 auto}
.cta .row{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:30px}
.cta .btn-noir{background:#000;color:#fff;border-color:#000}
.cta .btn-noir:hover{background:var(--accent);border-color:var(--accent);color:var(--sur-accent)}
.cta .btn-ligne{color:#000}
.cta .btn-ligne:hover{background:#000;color:#fff}
@media(max-width:900px){
  .cards{scroll-padding-left:var(--pad);display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:16px;margin:32px calc(var(--pad) * -1) 0;padding:0 var(--pad) 8px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
  .cards::-webkit-scrollbar{display:none}
  .cardd{flex:0 0 76%;scroll-snap-align:start}
  .mosaic{grid-template-columns:1fr 1fr}
  .mosaic figure{aspect-ratio:1/1}
  .cta .row{flex-direction:column}
  .cta .btn{width:100%}
}
"""


def page(fichier, titres, meta, hero, sections):
    """titres = (en, fr, zh) pour l'onglet ; meta = (description, url) ; hero = (photo, alt, petit titre, titre, texte)."""
    h = GABARIT
    # en-tête de page
    h = re.sub(r"<title>.*?</title>", f"<title>UNSEEN. — {titres[0]}</title>", h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{q(meta[0])}">', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="UNSEEN. — {q(titres[0])}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{q(meta[0])}">', h, count=1)
    h = h.replace("https://unseenconciergerie.com/professionals.html", f"https://unseenconciergerie.com/{fichier}")
    h = h.replace("</style>", CSS_DEST + "</style>", 1)
    # menu : plus aucun lien « actif »
    h = h.replace(' class="on" data-en="Professionals"', ' data-en="Professionals"')
    # contenu : tout ce qui se trouve entre le menu téléphone et le pied de page
    i = h.index('<div class="hero">'); j = h.index("<footer>")
    photo, alt, k, titre, texte = hero
    corps = f'''<div class="hero">
  {image(photo, alt, ' fetchpriority="high"')}
  <div class="hero-in">
    {t(*k, "div", ' class="k"')}
    {t(*titre, "h1")}
    {t(*texte, "p")}
    <div class="row">{t("Enquire on WhatsApp", "Nous écrire sur WhatsApp", "WhatsApp咨询", "a", ' class="btn btn-accent" href="https://wa.me/33613850733"')}{t("Tell us your dates", "Indiquez-nous vos dates", "告诉我们您的日期", "a", ' class="btn btn-ghost" href="#dates"')}</div>
  </div>
</div>

{sections}
'''
    h = h[:i] + corps + h[j:]
    # script : titre d'onglet, et plus de formulaire Professionals sur ces pages
    h = re.sub(r"var TITRES=\{[^}]*\};", "var TITRES={en:'UNSEEN. — %s',fr:'UNSEEN. — %s',zh:'UNSEEN. — %s'};" % tuple(x.replace("'", "\\\\'") for x in titres), h, count=1)
    i = h.index("// Onglets des publics"); j = h.index("// Apparition douce")
    h = h[:i] + h[j:]
    (SITE / fichier).write_text(h, encoding="utf-8")
    print("écrit :", fichier)


def bloc_intro(num, eyebrow, titre, texte, classe=""):
    return f'''<section{classe}>
  <div class="wrap">
    <div class="eyebrow"><span class="n">{num}</span>{t(*eyebrow, "span", ' class="t"')}</div>
    {t(*titre, "h2")}
    {t(*texte, "p", ' class="lede"')}
  </div>
</section>'''


def bloc_cartes(num, eyebrow, titre, cartes):
    c = "".join(f'<article class="cardd rv"><div class="ph">{image(img, alt)}</div>{t(*tag, "span", " class=\"tag\"")}{t(*nom, "h3")}{t(*txt, "p")}</article>'
                for img, alt, tag, nom, txt in cartes)
    return f'''<section class="sable">
  <div class="wrap">
    <div class="eyebrow"><span class="n">{num}</span>{t(*eyebrow, "span", ' class="t"')}</div>
    {t(*titre, "h2")}
    <div class="cards">{c}</div>
  </div>
</section>'''


def bloc_liste(num, eyebrow, titre, lignes):
    li = "".join(f"<li><b>0{k + 1}</b>{t(*l)}</li>" for k, l in enumerate(lignes))
    return f'''<section class="sombre">
  <div class="wrap">
    <div class="eyebrow"><span class="n">{num}</span>{t(*eyebrow, "span", ' class="t"')}</div>
    {t(*titre, "h2")}
    <ul class="rows">{li}</ul>
  </div>
</section>'''


def bloc_categories(num, eyebrow, titre, categories):
    """Ce que nous organisons, rangé par catégorie. Avec plus de 4 colonnes : 3 par ligne,
    et la dernière (« Partout ») sur toute la largeur."""
    trois = len(categories) > 4
    morceaux = []
    for n, (k2, nom, lignes) in enumerate(categories):
        large = " large" if trois and n == len(categories) - 1 else ""
        tete = t(*k2, "span", ' class="k2"') + t(*nom, "h3")
        liste = "".join(f"<li>{t(*l)}</li>" for l in lignes)
        morceaux.append(f'<div class="cat rv{large}"><div>{tete}</div><ul>{liste}</ul></div>')
    classe = "cats trois" if trois else "cats"
    return f'''<section class="sombre">
  <div class="wrap">
    <div class="eyebrow"><span class="n">{num}</span>{t(*eyebrow, "span", ' class="t"')}</div>
    {t(*titre, "h2")}
    <div class="{classe}">{"".join(morceaux)}</div>
  </div>
</section>'''


def bloc_mosaique(photos):
    return '<div class="mosaic">' + "".join(f"<figure>{image(p, a)}</figure>" for p, a in photos) + "</div>"


def bloc_cta(num):
    return f'''<section class="cta" id="dates">
  <div class="wrap">
    <div class="eyebrow" style="justify-content:center"><span class="n">{num}</span>{t("Your stay", "Votre séjour", "您的行程", "span", ' class="t"')}</div>
    {t("Tell us the dates.", "Indiquez-nous les dates.", "告诉我们日期。", "h2")}
    {t("One message is enough to start.", "Un message suffit pour commencer.", "一条消息，即可开始。", "p", ' class="lede"')}
    <div class="row">{t("Enquire on WhatsApp", "Nous écrire sur WhatsApp", "WhatsApp咨询", "a", ' class="btn btn-noir" href="https://wa.me/33613850733"')}{t("Use the contact form", "Utiliser le formulaire", "使用联系表单", "a", ' class="btn btn-ligne" href="index.html#contact"')}</div>
  </div>
</section>'''


# =================================================================== PARIS
page("paris.html", ("Paris", "Paris", "巴黎"),
     ("UNSEEN. in Paris: palace suites, tables that show nothing available, private appointments on the Faubourg, Fashion Week, discreet drivers.", ""),
     ("paris-hero", ("Paris and the Seine seen from above", "Paris et la Seine vus d'en haut", "俯瞰巴黎与塞纳河"),
      ("The base", "Notre base", "大本营"),
      ("Paris, from the inside.", "Paris, de l'intérieur.", "巴黎，由内而知。"),
      ("The city where the address book was built, and where a name still opens a door faster than a payment does.",
       "La ville où le carnet d'adresses s'est construit, et où un nom ouvre encore une porte plus vite qu'un paiement.",
       "这是我们积累人脉的城市。在这里，一个名字依然比一笔钱更快打开一扇门。")),
     "\n\n".join([
         bloc_intro("01", ("Why Paris", "Pourquoi Paris", "为何是巴黎"),
                    ("Everyone comes. Few get in.", "Tout le monde vient. Peu entrent.", "人人都来，进得去的却很少。"),
                    ("The best suites never reach a booking site, the right tables show nothing available, the houses of the Faubourg keep their appointments for the people they know. We work from the inside, all year.",
                     "Les plus belles suites n'arrivent jamais sur un site de réservation, les bonnes tables affichent complet, les maisons du Faubourg gardent leurs rendez-vous pour ceux qu'elles connaissent. Nous travaillons de l'intérieur, toute l'année.",
                     "最好的套房从不出现在预订网站上，对的餐厅永远显示客满，圣奥诺雷街的名店只把预约留给熟识的人。我们全年都在其中运作。")),
         bloc_cartes("02", ("Addresses", "Adresses", "地址"), ("Six corners we know by heart.", "Six quartiers que nous connaissons par cœur.", "六个我们烂熟于心的街区。"), [
             ("paris-faubourg", ("A Haussmann building on the Faubourg", "Un immeuble haussmannien du Faubourg", "圣奥诺雷街的奥斯曼建筑"), ("8th", "8e", "第八区"), ("Faubourg Saint-Honoré", "Faubourg Saint-Honoré", "圣奥诺雷街"),
              ("The houses, the private appointments, the boutiques that open early for you.", "Les grandes maisons, les rendez-vous privés, les boutiques qui ouvrent plus tôt pour vous.", "各大名店、私人预约，以及为您提前开门的精品店。")),
             ("paris-montaigne", ("A Parisian doorway in autumn", "Une porte parisienne en automne", "秋日的巴黎门廊"), ("8th", "8e", "第八区"), ("Avenue Montaigne", "Avenue Montaigne", "蒙田大道"),
              ("Couture, palace bars, and a table at the Plaza Athénée.", "La haute couture, les bars de palace, et une table au Plaza Athénée.", "高级定制、殿堂酒店酒吧，以及雅典娜广场酒店的一张餐桌。")),
             ("paris-vendome", ("Wrought-iron gates in Paris", "Des grilles en fer forgé à Paris", "巴黎的铸铁大门"), ("1st", "1er", "第一区"), ("Place Vendôme", "Place Vendôme", "旺多姆广场"),
              ("The jewellers, the Ritz, and a fitting that runs past closing.", "Les joailliers, le Ritz, et un essayage qui se prolonge après la fermeture.", "顶级珠宝商、丽兹酒店，以及打烊后仍在继续的试衣。")),
             ("paris-tour", ("A café street with the Eiffel Tower behind", "Une rue de café avec la tour Eiffel derrière", "远处是埃菲尔铁塔的咖啡街"), ("7th", "7e", "第七区"), ("Around the Tower", "Autour de la Tour", "铁塔周边"),
              ("A table facing the Tower at night, a terrace, a quiet street at breakfast.", "Une table face à la Tour la nuit, une terrasse, une rue calme au petit-déjeuner.", "夜里正对铁塔的餐桌、一处露台，以及早餐时分安静的街道。")),
             ("paris-toits", ("Paris rooftops at dusk", "Les toits de Paris au crépuscule", "黄昏时的巴黎屋顶"), ("3rd and 4th", "3e et 4e", "第三、四区"), ("Le Marais", "Le Marais", "玛黑区"),
              ("Hidden courtyards, young designers, the best Sunday in Paris.", "Des cours cachées, de jeunes créateurs, le plus beau dimanche de Paris.", "隐秘庭院、年轻设计师，还有巴黎最好的星期天。")),
             ("paris-seine", ("The Seine at night", "La Seine la nuit", "夜色中的塞纳河"), ("The river", "Le fleuve", "塞纳河"), ("The Seine", "La Seine", "塞纳河"),
              ("A private boat at sunset, dinner on the water, the bridges lit up.", "Un bateau privé au coucher du soleil, un dîner sur l'eau, les ponts illuminés.", "日落时的私人游船、水上晚餐，以及灯火通明的桥。")),
         ]),
         bloc_categories("03", ("What we arrange", "Ce que nous organisons", "我们为您安排"), ("One contact. Everything the week needs.", "Un seul contact. Tout ce que la semaine demande.", "一位联系人，满足这一周的所有需求。"), [
             (("Stay", "Séjour", "住宿"), ("Where you sleep", "Où dormir", "下榻之处"), [
                 ("A palace suite that was never listed, upgrade arranged before you land.", "Une suite de palace jamais mise en vente, surclassement réglé avant votre arrivée.", "从未公开出售的殿堂级套房，落地前已安排好升级。"),
                 ("An apartment with staff for a longer stay.", "Un appartement avec personnel pour un séjour plus long.", "长住时，配备管家的公寓。"),
                 ("A late check-out, held for you.", "Un départ tardif, gardé pour vous.", "为您保留的延迟退房。")]),
             (("Tables", "Tables", "餐桌"), ("Where you eat", "Où manger", "用餐之处"), [
                 ("A table at the restaurant that is fully booked.", "Une table dans le restaurant qui affiche complet.", "在已经订满的餐厅里，为您留出一张桌子。"),
                 ("A chef's table or a private room.", "Une table du chef ou un salon privé.", "主厨餐桌或私人包厢。"),
                 ("Dinner on the Seine, on a private boat.", "Un dîner sur la Seine, à bord d'un bateau privé.", "在塞纳河的私人游船上晚餐。")]),
             (("Experiences", "Expériences", "体验"), ("What you do", "Que faire", "做些什么"), [
                 ("Personal shopping and private appointments on the Faubourg.", "Du personal shopping et des rendez-vous privés sur le Faubourg.", "私人购物顾问，以及圣奥诺雷街名店的私人预约。"),
                 ("Fashion Week: the show, and the dinner after.", "La Fashion Week : le défilé, et le dîner qui suit.", "时装周：秀场，以及秀后的晚宴。"),
                 ("Sport: Roland-Garros, the Parc des Princes, the Stade de France.", "Le sport : Roland-Garros, le Parc des Princes, le Stade de France.", "体育：罗兰·加洛斯、王子公园球场、法兰西体育场。")]),
             (("Getting around", "Déplacements", "出行"), ("How you move", "Comment circuler", "如何往来"), [
                 ("A private driver for the whole stay.", "Un chauffeur privé pendant tout le séjour.", "全程专属私人司机。"),
                 ("A welcome at the aircraft or the train.", "Un accueil au pied de l'avion ou du train.", "机旁或站台迎接。"),
                 ("A helicopter to Deauville or Champagne.", "Un hélicoptère pour Deauville ou la Champagne.", "乘直升机前往多维尔或香槟区。")]),
         ]),
         bloc_mosaique([("paris-m1", ("The Eiffel Tower at dusk", "La tour Eiffel au crépuscule", "黄昏中的埃菲尔铁塔")),
                        ("paris-m2", ("Paris lit up at night", "Paris illuminé la nuit", "夜晚灯火通明的巴黎")),
                        ("paris-m3", ("The Eiffel Tower under an evening sky", "La tour Eiffel sous un ciel du soir", "傍晚天空下的埃菲尔铁塔")),
                        ("paris-m4", ("Paris seen from above", "Paris vu d'en haut", "俯瞰巴黎"))]),
         bloc_cta("04"),
     ]))

# =================================================================== MAURICE
page("ocean-indien.html", ("The Indian Ocean", "L'océan Indien", "印度洋"),
     ("UNSEEN. in the Indian Ocean, Mauritius, Réunion and the Maldives, with LUX* Resorts & Hotels: resorts, staffed villas, helicopter legs, days at sea, a stopover in Paris.", ""),
     ("maurice-hero", ("LUX* Grand Gaube seen from above, Mauritius", "Le LUX* Grand Gaube vu du ciel, à Maurice", "从空中俯瞰毛里求斯LUX* Grand Gaube"),
      ("The counter-season", "La contre-saison", "反季之选"),
      ("The Indian Ocean, when Europe closes.", "L'océan Indien, quand l'Europe ferme.", "欧洲淡季，正是印度洋的好时节。"),
      ("Mauritius, Réunion, the Maldives. Lagoons, resorts, staffed villas, helicopter legs and days at sea with a crew.",
       "Maurice, La Réunion, les Maldives. Des lagons, des resorts, des villas avec personnel, l'hélicoptère et des journées en mer avec équipage.",
       "毛里求斯、留尼汪、马尔代夫。泻湖、度假村、配备管家的别墅，乘直升机俯瞰海岛，或随船员出海一整天。")),
     "\n\n".join([
         bloc_intro("01", ("Why the Indian Ocean", "Pourquoi l'océan Indien", "为何是印度洋"),
                    ("Warm all year, easy from Paris.", "Chaud toute l'année, simple depuis Paris.", "四季温暖，从巴黎出发很方便。"),
                    ("Mauritius is our base in the Indian Ocean: a direct flight from Paris, French spoken everywhere, and a season of its own, at its best from May to June and September to December. Réunion and the Maldives are close by. Many of our clients stop in Paris first, then fly south.",
                     "Maurice est notre base dans l'océan Indien : un vol direct depuis Paris, le français parlé partout, et une saison bien à elle, au plus beau de mai à juin et de septembre à décembre. La Réunion et les Maldives sont toutes proches. Beaucoup de nos clients passent d'abord par Paris, puis s'envolent vers le sud.",
                     "毛里求斯是我们在印度洋的据点：从巴黎有直飞航班，岛上处处可以讲法语，季节自成一格，五月至六月、九月至十二月最为宜人。留尼汪与马尔代夫近在咫尺。我们的许多客人会先在巴黎停留，再飞往南方。")),
         bloc_cartes("02", ("With LUX*", "Avec LUX*", "携手LUX*"), ("Our partner resorts.", "Nos resorts partenaires.", "我们的合作度假村。"), [
             ("maurice-lemorne", ("The beach of LUX* Le Morne", "La plage du LUX* Le Morne", "LUX* Le Morne的海滩"), ("South-west", "Sud-ouest", "西南部"), ("LUX* Le Morne", "LUX* Le Morne", "LUX* Le Morne"),
              ("At the foot of the mountain, on the sunset side of the island.", "Au pied de la montagne, du côté du coucher de soleil.", "坐落在莫纳山脚下，岛上看日落的一侧。")),
             ("maurice-bellemare", ("The beach and pool of LUX* Belle Mare", "La plage et la piscine du LUX* Belle Mare", "LUX* Belle Mare的海滩与泳池"), ("East coast", "Côte est", "东海岸"), ("LUX* Belle Mare", "LUX* Belle Mare", "LUX* Belle Mare"),
              ("A long white beach, villas with their own pool, the morning sun.", "Une longue plage blanche, des villas avec piscine privée, le soleil du matin.", "绵长的白沙滩、带私人泳池的别墅，还有清晨的阳光。")),
             ("maurice-grandbaie", ("LUX* Grand Baie seen from above", "Le LUX* Grand Baie vu du ciel", "从空中俯瞰LUX* Grand Baie"), ("North", "Nord", "北部"), ("LUX* Grand Baie", "LUX* Grand Baie", "LUX* Grand Baie"),
              ("The newest address on the island, a rooftop, the life of the bay close by.", "La plus récente adresse de l'île, un rooftop, la vie de la baie toute proche.", "岛上最新的度假村，屋顶露台，海湾的热闹近在咫尺。")),
             ("maurice-grandgaube", ("The beach of LUX* Grand Gaube", "La plage du LUX* Grand Gaube", "LUX* Grand Gaube的海滩"), ("Northern tip", "Pointe nord", "北端"), ("LUX* Grand Gaube", "LUX* Grand Gaube", "LUX* Grand Gaube"),
              ("Two coves at the top of the island, quiet and turned to the sea.", "Deux criques tout au nord de l'île, calmes et tournées vers la mer.", "岛屿最北端的两处海湾，宁静而面朝大海。")),
             ("maurice-reunion", ("LUX* Saint-Gilles seen from above, Réunion", "Le LUX* Saint-Gilles vu du ciel, à La Réunion", "从空中俯瞰留尼汪LUX* Saint-Gilles"), ("Réunion", "La Réunion", "留尼汪"), ("LUX* Saint-Gilles", "LUX* Saint-Gilles", "LUX* Saint-Gilles"),
              ("Forty-five minutes by air: volcanoes, waterfalls, a lagoon of its own.", "À quarante-cinq minutes de vol : volcans, cascades, et un lagon bien à elle.", "飞行约四十五分钟：火山、瀑布，还有属于它自己的泻湖。")),
             ("maurice-maldives", ("LUX* South Ari Atoll seen from above, Maldives", "Le LUX* South Ari Atoll vu du ciel, aux Maldives", "从空中俯瞰马尔代夫LUX* South Ari Atoll"), ("Maldives", "Maldives", "马尔代夫"), ("LUX* South Ari Atoll", "LUX* South Ari Atoll", "LUX* South Ari Atoll"),
              ("Water villas and whale sharks, for the next trip in the Indian Ocean.", "Des villas sur l'eau et des requins-baleines, pour le prochain voyage dans l'océan Indien.", "水上别墅与鲸鲨，留给下一次的印度洋之旅。")),
         ]),
         bloc_categories("03", ("What we arrange", "Ce que nous organisons", "我们为您安排"), ("Each place, its own pleasures.", "Chaque adresse, ses propres plaisirs.", "每一处，都有自己的乐趣。"), [
             (("South-west", "Sud-ouest", "西南部"), ("LUX* Le Morne", "LUX* Le Morne", "LUX* Le Morne"), [
                 ("Kitesurfing on the Le Morne lagoon, one of the best spots in the world.", "Le kitesurf sur le lagon du Morne, l'un des plus beaux spots du monde.", "在莫纳泻湖玩风筝冲浪，这里是世界顶级的风筝冲浪胜地之一。"),
                 ("A sunrise hike up Le Morne Brabant.", "L'ascension du Morne Brabant au lever du soleil.", "日出时分徒步登上莫纳山。"),
                 ("Dinner facing the sunset.", "Un dîner face au coucher du soleil.", "面朝日落晚餐。")]),
             (("East coast", "Côte est", "东海岸"), ("LUX* Belle Mare", "LUX* Belle Mare", "LUX* Belle Mare"), [
                 ("A catamaran to the Île aux Cerfs.", "Un catamaran jusqu'à l'île aux Cerfs.", "乘双体船前往鹿岛。"),
                 ("Golf on the courses of the east coast.", "Le golf sur les parcours de la côte est.", "在东海岸的球场打高尔夫。"),
                 ("A villa with its own pool on the long beach.", "Une villa avec piscine privée sur la grande plage.", "长滩上带私人泳池的别墅。")]),
             (("North", "Nord", "北部"), ("LUX* Grand Baie", "LUX* Grand Baie", "LUX* Grand Baie"), [
                 ("A boat to the northern islets, Coin de Mire.", "Un bateau vers les îlots du nord, le Coin de Mire.", "乘船前往北部小岛，库安德迈尔岛。"),
                 ("Sunset on the rooftop.", "Le coucher du soleil sur le rooftop.", "在屋顶露台看日落。"),
                 ("The restaurants and boutiques of the bay.", "Les restaurants et les boutiques de la baie.", "海湾边的餐厅与精品店。")]),
             (("Northern tip", "Pointe nord", "北端"), ("LUX* Grand Gaube", "LUX* Grand Gaube", "LUX* Grand Gaube"), [
                 ("Snorkelling and paddle in the two coves.", "Snorkeling et paddle dans les deux criques.", "在两处海湾浮潜、玩桨板。"),
                 ("The Pamplemousses botanical garden.", "Le jardin botanique de Pamplemousses.", "庞普勒穆斯植物园。"),
                 ("A quiet week, turned to the sea.", "Une semaine calme, tournée vers la mer.", "面朝大海，安静的一周。")]),
             (("Réunion", "La Réunion", "留尼汪"), ("LUX* Saint-Gilles", "LUX* Saint-Gilles", "LUX* Saint-Gilles"), [
                 ("A helicopter over the cirques and the waterfalls.", "Un hélicoptère au-dessus des cirques et des cascades.", "乘直升机飞越冰斗与瀑布。"),
                 ("A hike on the Piton de la Fournaise volcano.", "Une randonnée sur le volcan du Piton de la Fournaise.", "徒步富尔奈斯火山。")]),
             (("Maldives", "Maldives", "马尔代夫"), ("LUX* South Ari Atoll", "LUX* South Ari Atoll", "LUX* South Ari Atoll"), [
                 ("Snorkelling with whale sharks.", "Du snorkeling avec les requins-baleines.", "与鲸鲨一同浮潜。"),
                 ("A water villa and a private dinner on the sandbank.", "Une villa sur l'eau et un dîner privé sur un banc de sable.", "水上别墅，以及沙洲上的私人晚宴。")]),
             (("Everywhere", "Partout", "全程"), ("Getting around", "Déplacements", "出行"), [
                 ("A private driver throughout the stay.", "Un chauffeur privé pendant tout le séjour.", "全程专属私人司机。"),
                 ("A helicopter transfer from the airport.", "Un transfert en hélicoptère depuis l'aéroport.", "从机场乘直升机前往酒店。"),
                 ("A few nights in Paris on the way, as one trip.", "Quelques nuits à Paris sur le chemin, en un seul voyage.", "途经巴黎小住几晚，整段行程一并安排。")]),
         ]),
         bloc_mosaique([("maurice-m1", ("A villa at LUX* Belle Mare", "Une villa du LUX* Belle Mare", "LUX* Belle Mare的别墅")),
                        ("maurice-m2", ("The pool at LUX* Le Morne", "La piscine du LUX* Le Morne", "LUX* Le Morne的泳池")),
                        ("maurice-m3", ("Beach Rouge at LUX* Grand Baie", "Le Beach Rouge du LUX* Grand Baie", "LUX* Grand Baie的Beach Rouge")),
                        ("maurice-m4", ("A water villa in the Maldives", "Une villa sur l'eau aux Maldives", "马尔代夫的水上别墅"))]),
         bloc_cta("04"),
     ]))


# =================================================================== RIVIERA
page("riviera.html", ("The Riviera", "La Riviera", "蔚蓝海岸"),
     ("UNSEEN. on the French Riviera: Monaco, Saint-Tropez, Cannes, Cap Ferrat. Villas, yachts, beach clubs, the Grand Prix and the Festival.", ""),
     ("riviera-hero", ("Monaco at night seen from the heights", "Monaco la nuit, vu des hauteurs", "从高处俯瞰夜色中的摩纳哥"),
      ("Summer", "L'été", "夏季"),
      ("The Riviera, from the water.", "La Riviera, côté mer.", "从海上看蔚蓝海岸。"),
      ("Monaco, Saint-Tropez, Cannes. Villas taken before winter ends, beach clubs where a table already carries a name, days that begin at the berth.",
       "Monaco, Saint-Tropez, Cannes. Des villas réservées avant la fin de l'hiver, des beach clubs où une table porte déjà un nom, des journées qui commencent au ponton.",
       "摩纳哥、圣特罗佩、戛纳。冬天未尽，别墅已被订走；海滩俱乐部的餐桌，早已写上了名字；一天，从码头开始。")),
     "\n\n".join([
         bloc_intro("01", ("Why now", "Pourquoi maintenant", "为何现在"),
                    ("The summer is booked in winter.", "L'été se réserve en hiver.", "夏天，要在冬天就订好。"),
                    ("The villas, the boats and the Grand Prix terraces are taken months ahead. We start in January, so your name is already on the list when you decide.",
                     "Les villas, les bateaux et les terrasses du Grand Prix partent des mois à l'avance. Nous commençons en janvier, pour que votre nom soit déjà sur la liste le jour où vous décidez.",
                     "别墅、游艇和大奖赛的观赛露台，都会提前数月被订走。我们从一月开始准备，让您决定出行时，名字早已在名单上。")),
         bloc_cartes("02", ("Destinations", "Destinations", "目的地"), ("Six places, one coast.", "Six adresses, une seule côte.", "一条海岸，六处去处。"), [
             ("riviera-monaco", ("Yachts in Monaco harbour", "Des yachts dans le port de Monaco", "摩纳哥港内的游艇"), ("Principality", "Principauté", "公国"), ("Monaco", "Monaco", "摩纳哥"),
              ("The Grand Prix, the Casino square, a table above the harbour.", "Le Grand Prix, la place du Casino, une table au-dessus du port.", "大奖赛、赌场广场，以及俯瞰港口的一张餐桌。")),
             ("riviera-tropez", ("A beach club on the Riviera", "Un beach club sur la Riviera", "蔚蓝海岸的海滩俱乐部"), ("Var", "Var", "瓦尔省"), ("Saint-Tropez", "Saint-Tropez", "圣特罗佩"),
              ("Pampelonne, the beach clubs, the old port at night.", "Pampelonne, les beach clubs, le vieux port la nuit.", "庞佩洛纳海滩、海滩俱乐部，以及夜色中的老港。")),
             ("riviera-cannes", ("The Croisette in Cannes", "La Croisette à Cannes", "戛纳的十字大道"), ("Alpes-Maritimes", "Alpes-Maritimes", "滨海阿尔卑斯省"), ("Cannes", "Cannes", "戛纳"),
              ("The Croisette, the Festival in May, the islands opposite.", "La Croisette, le Festival en mai, les îles juste en face.", "十字大道、五月的电影节，以及对面的群岛。")),
             ("riviera-ferrat", ("A villa above a cove on Cap Ferrat", "Une villa au-dessus d'une crique du Cap Ferrat", "费拉角海湾上方的别墅"), ("The cape", "Le cap", "海角"), ("Cap Ferrat", "Cap Ferrat", "费拉角"),
              ("Villas behind the pines, the quietest bays on the coast.", "Des villas derrière les pins, les baies les plus calmes de la côte.", "松林后的别墅，整条海岸最安静的海湾。")),
             ("riviera-eze", ("A stone street in Èze village", "Une ruelle en pierre du village d'Èze", "埃兹村的石板小巷"), ("Above the sea", "Au-dessus de la mer", "临海之上"), ("Èze", "Èze", "埃兹"),
              ("A village above the sea, dinner on a terrace at sunset.", "Un village perché au-dessus de la mer, un dîner en terrasse au coucher du soleil.", "悬于海上的小村，日落时分在露台晚餐。")),
             ("riviera-mer", ("The deck of a yacht at sea", "Le pont d'un yacht en mer", "海上游艇的甲板"), ("At sea", "En mer", "海上"), ("On board", "À bord", "游艇之上"),
              ("A yacht for the day or the week, with crew, tender and chef.", "Un yacht pour la journée ou la semaine, avec équipage, annexe et chef.", "按天或按周包租游艇，配备船员、接驳艇与主厨。")),
         ]),
         bloc_categories("03", ("What we arrange", "Ce que nous organisons", "我们为您安排"), ("The whole summer, one contact.", "Tout l'été, un seul contact.", "整个夏天，只需一位联系人。"), [
             (("Stay", "Séjour", "住宿"), ("Where you sleep", "Où dormir", "下榻之处"), [
                 ("A villa with staff, for the week or the season.", "Une villa avec personnel, à la semaine ou à la saison.", "配备管家的别墅，按周或整季。"),
                 ("A suite in Monaco or on Cap Ferrat.", "Une suite à Monaco ou au Cap Ferrat.", "摩纳哥或费拉角的套房。"),
                 ("A room on the beach in Saint-Tropez.", "Une chambre sur la plage à Saint-Tropez.", "圣特罗佩海滩上的客房。")]),
             (("Tables", "Tables", "餐桌"), ("Where you eat", "Où manger", "用餐之处"), [
                 ("Lunch at a beach club on Pampelonne.", "Un déjeuner dans un beach club de Pampelonne.", "在庞佩洛纳的海滩俱乐部午餐。"),
                 ("A terrace above the sea in Èze.", "Une terrasse au-dessus de la mer à Èze.", "埃兹临海的露台。"),
                 ("The right table in Monaco on Grand Prix night.", "La bonne table à Monaco le soir du Grand Prix.", "大奖赛之夜，摩纳哥那张对的餐桌。")]),
             (("Experiences", "Expériences", "体验"), ("What you do", "Que faire", "做些什么"), [
                 ("The Grand Prix from a terrace or a boat.", "Le Grand Prix depuis une terrasse ou un bateau.", "在露台或游艇上观赏大奖赛。"),
                 ("The Cannes Festival and its evenings.", "Le Festival de Cannes et ses soirées.", "戛纳电影节及其晚会。"),
                 ("A day on the Lérins islands.", "Une journée sur les îles de Lérins.", "在莱兰群岛度过一天。")]),
             (("Getting around", "Déplacements", "出行"), ("How you move", "Comment circuler", "如何往来"), [
                 ("Nice to Monaco by helicopter, in seven minutes.", "Nice-Monaco en hélicoptère, en sept minutes.", "乘直升机从尼斯到摩纳哥，只需七分钟。"),
                 ("A private driver for the whole stay.", "Un chauffeur privé pendant tout le séjour.", "全程专属私人司机。"),
                 ("A tender from the boat to the beach.", "Une annexe du bateau jusqu'à la plage.", "从游艇乘接驳艇直达海滩。")]),
         ]),
         bloc_mosaique([("riviera-m1", ("A restaurant built into the rocks above the sea", "Un restaurant accroché aux rochers au-dessus de la mer", "嵌在海边岩石上的餐厅")),
                        ("riviera-m2", ("A table set facing the bay", "Une table dressée face à la baie", "面朝海湾布置好的餐桌")),
                        ("riviera-m3", ("A beach terrace by the sea", "Une terrasse de plage au bord de l'eau", "海边的海滩露台")),
                        ("riviera-m4", ("A turquoise cove below the hills", "Une crique turquoise au pied des collines", "山脚下的碧绿海湾"))]),
         bloc_cta("04"),
     ]))
