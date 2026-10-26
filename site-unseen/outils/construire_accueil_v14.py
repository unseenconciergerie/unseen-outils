"""
Construit la nouvelle page d'accueil (charte V1.4, validée par Jay le 26/10/2026).

Point de départ : la maquette validée « 09 Accueil Sable rosé » (Livrables/Maquettes
site (évolution)/), elle-même tirée de l'ancien index.html. Ce script :
  - remet les chemins du site (img/...) et la couleur de saison (season.css) ;
  - réécrit les sections nouvelles en trois langues (data-en, data-fr, data-zh) ;
  - reprend les textes des services déjà traduits dans l'ancien index.html ;
  - remplace la ligne de logos par un bandeau qui défile ;
  - garde le diaporama du haut de page (anim.js) avec deux photos.
Il n'est à lancer qu'une fois : ensuite, c'est index.html qu'on modifie directement.

Lancer, depuis le dossier du projet :
    python3 site-unseen/outils/construire_accueil_v14.py
"""
import html as H
import re
import subprocess
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
MAQUETTE = SITE.parent / "Livrables" / "Maquettes site (évolution)" / "09 Accueil Sable rosé, version retenue (26-10).html"


def t(en, fr, zh, balise="span", attrs=""):
    """Élément trilingue : le texte anglais est affiché par défaut, le script des langues fait le reste."""
    q = lambda s: H.escape(s, quote=True)
    return f'<{balise}{attrs} data-en="{q(en)}" data-fr="{q(fr)}" data-zh="{q(zh)}">{en}</{balise}>'


def image(nom, alt_en="", alt_fr="", alt_zh="", classe="", attrs=' loading="lazy"'):
    alt = f' alt="{H.escape(alt_en)}" data-alt-en="{H.escape(alt_en)}" data-alt-fr="{H.escape(alt_fr)}" data-alt-zh="{H.escape(alt_zh)}"' if alt_en else ' alt=""'
    c = f' class="{classe}"' if classe else ""
    return f'<picture><source type="image/avif" srcset="img/{nom}.avif"><img{c} src="img/{nom}.webp"{alt}{attrs}></picture>'


def section(h, debut, fin="</section>"):
    i = h.index(debut)
    return i, h.index(fin, i) + len(fin)


# ---------------------------------------------------------------- départ
h = MAQUETTE.read_text(encoding="utf-8", errors="surrogateescape")
ancien = subprocess.run(["git", "-C", str(SITE), "show", "HEAD:site-unseen/index.html"],
                        capture_output=True, text=True).stdout

h = re.sub(r'<base href="[^"]*">\n?', "", h)
# couleur de saison : le fichier season.css reprend la main sur l'accent
h = h.replace("<style>\n/* --- Version 2 : Lin et prune --- */", '<link rel="stylesheet" href="season.css">\n<style>\n/* --- Version 2 : Lin et prune --- */', 1)

# ---------------------------------------------------------------- menu
def menu(indent):
    liens = [("#services", "Services", "Services", "服务"), ("#destinations", "Destinations", "Destinations", "目的地"),
             ("#now", "Seasons", "Saisons", "当季"), ("professionals.html", "Professionals", "Professionnels", "合作伙伴"),
             ("#contact", "Contact", "Contact", "联系我们")]
    return ("\n" + indent).join(t(en, fr, zh, "a", f' href="{href}"') for href, en, fr, zh in liens)


for bloc in ('<nav class="nav">', '<div class="navpanel" id="navpanel" aria-hidden="true">\n  <nav>'):
    i = h.index(bloc) + len(bloc)
    j = h.index("</nav>", i)
    h = h[:i] + "\n      " + menu("      ") + "\n    " + h[j:]

# ---------------------------------------------------------------- haut de page
i, j = section(h, '<div class="hero-bg" aria-hidden="true">', "</div>")
h = h[:i] + '''<div class="hero-bg" aria-hidden="true">
    <picture class="hslide is-on"><source type="image/avif" srcset="img/hero.avif"><img class="bg" src="img/hero.webp" alt="The Eiffel Tower at dusk, seen from a Paris avenue" data-alt-en="The Eiffel Tower at dusk, seen from a Paris avenue" data-alt-fr="La tour Eiffel au crépuscule, vue depuis une avenue de Paris" data-alt-zh="黄昏时分，从巴黎街道远眺埃菲尔铁塔" fetchpriority="high"></picture>
  </div>''' + h[j:]
h = re.sub(r'<img class="nv-hs"[^>]*>', "", h)
h = h.replace(".hslide:not(:first-child){display:none!important}", "")
h = re.sub(r"\.nv-hs\{[^}]*\}@keyframes nvhs\{[^}]*\{[^}]*\}[^}]*\{[^}]*\}[^}]*\{[^}]*\}\}", "", h)
h = h.replace(".hslide img{opacity:1!important}", "")

# ---------------------------------------------------------------- services (textes de l'ancien site, déjà traduits)
cartes = re.findall(r'<article class="card">(.*?)</article>', ancien, re.S)
def attrs_de(bloc, balise):
    m = re.search(rf'<{balise}[^>]*data-en="([^"]*)"[^>]*data-fr="([^"]*)"[^>]*data-zh="([^"]*)"', bloc)
    return [H.unescape(x) for x in m.groups()]
ordre = [(0, "v2-stay"), (1, "v2-dining"), (2, "v2-access"), (3, "v2-shopping"), (4, "v2-transport"), (6, "v2-season"), (5, "v2-evening")]
lis, ims = [], []
for k, (n, img) in enumerate(ordre):
    tag = attrs_de(cartes[n], 'span class="tag"')
    titre = attrs_de(cartes[n], "h3")
    texte = attrs_de(cartes[n], "p")
    on = ' class="on"' if k == 0 else ""
    lis.append(f'<li{on} data-i="{k}">{t(*tag, "span", " class=\"t\"")}<div>{t(*titre, "h3")}{t(*texte, "p")}</div></li>')
    ims.append(image(img, classe="on" if k == 0 else ""))
titre_svc = attrs_de(ancien[ancien.index('<section id="services"'):], "h2")
lede_svc = attrs_de(ancien[ancien.index('<section id="services"'):], 'p class="lede"')
svc = f'''<section id="services" class="sec-dark nv-svc">
  <div class="wrap">
    <div class="head reveal">
      <div class="eyebrow"><span class="n">02</span>{t("Services", "Services", "服务", "span", ' class="t"')}</div>
      {t(*titre_svc, "h2")}
      {t(*lede_svc, "p", ' class="lede"')}
    </div>
    <div class="nv-grid">
      <ul class="nv-list" id="nvsvc">{"".join(lis)}</ul>
      <div class="nv-img" id="nvimg">{"".join(ims)}</div>
    </div>
  </div>
</section>'''
i, j = section(h, '<section id="services"')
h = h[:i] + svc + h[j:]
h = h.replace(".nv-img img{position:absolute", ".nv-img picture{position:absolute;inset:0}.nv-img img{position:absolute", 1)

# ---------------------------------------------------------------- destinations
def tuile(classe, lien, img, alt, sur, nom, ligne):
    return (f'<a class="nd {classe} reveal" href="{lien}">{image(img, *alt)}<div class="in">'
            f'{t(*sur)}{t(*nom, "h3")}{t(*ligne, "p")}</div></a>')
dest = f'''<section id="destinations" class="sec-white">
  <div class="wrap">
    <div class="head reveal">
      <div class="eyebrow"><span class="n">03</span>{t("Destinations", "Destinations", "目的地", "span", ' class="t"')}</div>
      {t("Among the places we go.", "Parmi nos destinations.", "我们常去的地方。", "h2")}
      {t("Paris first, then wherever the season takes you. And further, when you ask: Ibiza, Mykonos, London, Milan, and wherever else you have in mind.",
         "Paris d'abord, puis là où la saison vous emmène. Et plus loin si vous le demandez : Ibiza, Mykonos, Londres, Milan, et partout où vous avez envie d'aller.",
         "从巴黎出发，随季节而行。若您有意，我们也可以走得更远：伊维萨、米科诺斯、伦敦、米兰，以及任何您心之所向的地方。", "p", ' class="lede"')}
    </div>
    <div class="nv-dest">
      {tuile("nd1", "paris.html", "v2-paris", ("Paris at dusk", "Paris au crépuscule", "黄昏时的巴黎"), ("The base", "Notre base", "大本营"), ("Paris", "Paris", "巴黎"),
             ("Palaces, starred tables, Fashion Week, the houses of the Faubourg.", "Palaces, tables étoilées, Fashion Week, les maisons du Faubourg.", "殿堂级酒店、米其林餐桌、时装周，以及圣奥诺雷街的各大名店。"))}
      {tuile("nd2", "saison-ski-2026-2027.html", "v2-alps", ("A chalet at night in the Alps", "Un chalet la nuit dans les Alpes", "阿尔卑斯山间的夜色木屋"), ("Winter", "L'hiver", "冬季"), ("The Alps", "Les Alpes", "阿尔卑斯"),
             ("Courchevel, Megève, Gstaad. A season held a step ahead.", "Courchevel, Megève, Gstaad. Une saison préparée avec un temps d'avance.", "库舍维尔、梅杰夫、格施塔德。雪季，我们总是提前一步。"))}
      {tuile("nd3", "riviera.html", "v2-riviera", ("A table above the sea on the Riviera", "Une table au-dessus de la mer, sur la Riviera", "蔚蓝海岸，临海而设的餐桌"), ("Summer", "L'été", "夏季"), ("The Riviera", "La Riviera", "蔚蓝海岸"),
             ("Monaco, Saint-Tropez, Cannes. Villas, boats, the Grand Prix.", "Monaco, Saint-Tropez, Cannes. Villas, bateaux, le Grand Prix.", "摩纳哥、圣特罗佩、戛纳。别墅、游艇与大奖赛。"))}
      {tuile("nd4", "maurice.html", "v2-mauritius", ("The beach of LUX* Le Morne, Mauritius", "La plage du LUX* Le Morne, à Maurice", "毛里求斯LUX* Le Morne酒店的海滩"), ("Counter-season", "Contre-saison", "反季之选"), ("Mauritius", "Maurice", "毛里求斯"),
             ("Open when Europe closes: resorts, staffed villas, island days.", "Ouverte quand l'Europe ferme : resorts, villas avec personnel, journées sur l'île.", "欧洲淡季时，这里正当时：度假酒店、配备管家的别墅，以及海岛时光。"))}
    </div>
    <p class="lede" style="margin-top:44px">{t("UNSEEN. belongs to no group and no booking network: we recommend an address because it is the right one. Agencies, jet operators, sports management:",
        "UNSEEN. n'appartient à aucun groupe ni réseau de réservation : nous recommandons une adresse parce que c'est la bonne. Agences, compagnies d'aviation privée, agents de sportifs :",
        "UNSEEN.不隶属于任何集团或预订网络：我们推荐一个地方，只因为它是对的。旅行社、私人航空公司、体育经纪机构：")} {t("working with us &rarr;", "travailler avec nous &rarr;", "与我们合作 &rarr;", "a", ' href="professionals.html" class="nv-link"')}</p>
  </div>
</section>'''
i, j = section(h, '<section id="destinations"')
h = h[:i] + dest + h[j:]

# ---------------------------------------------------------------- carte
carte = f'''<section id="map" class="sec-dark nv-map">
  <div class="wrap">
    <div class="head reveal">
      <div class="eyebrow"><span class="n">04</span>{t("Map", "Carte", "地图", "span", ' class="t"')}</div>
      {t("Paris is where it starts.", "Tout commence à Paris.", "一切，从巴黎开始。", "h2")}
      {t("A few ideas of what we arrange, from Paris to wherever the season is. Choose a point.",
         "Quelques idées de ce que nous organisons, de Paris jusqu'à là où se trouve la saison. Choisissez un point.",
         "从巴黎到当季所在之处，这是我们可以为您安排的一些灵感。请点选地图上的地点。", "p", ' class="lede"')}
    </div>
    <div class="nv-mapgrid">
      <div class="nv-eu"><svg id="europe" viewBox="0 0 560 420" role="img" aria-label="Map of Europe with UNSEEN. destinations"></svg></div>
      <div class="nv-info" id="nvinfo" aria-live="polite"></div>
    </div>
  </div>
</section>'''
i, j = section(h, '<section id="map"')
h = h[:i] + carte + h[j:]

# ---------------------------------------------------------------- en ce moment
def carte_now(lien, img, quand, titre, texte, bouton):
    return (f'<a class="nn reveal" href="{lien}">{image(img)}<div>{t(*quand)}{t(*titre, "h3")}{t(*texte, "p")}{t(*bouton, "b")}</div></a>')
now = f'''<section id="now" class="sec-pale">
  <div class="wrap">
    <div class="head reveal">
      <div class="eyebrow"><span class="n">05</span>{t("Right now", "En ce moment", "当季", "span", ' class="t"')}</div>
      {t("What we are working on this season.", "Ce que nous préparons cette saison.", "本季，我们正在筹备的。", "h2")}
    </div>
    <div class="nv-now">
      {carte_now("saison-ski-2026-2027.html", "v2-now-ski", ("December 2026 to April 2027", "Décembre 2026 à avril 2027", "2026年12月至2027年4月"), ("The ski season", "La saison de ski", "滑雪季"),
                 ("The good chalets for Christmas and February are being taken now. Tell us your weeks.", "Les beaux chalets de Noël et de février partent maintenant. Dites-nous vos semaines.", "圣诞与二月的好木屋，此刻正被陆续订走。告诉我们您的日期。"),
                 ("The ski season &rarr;", "La saison de ski &rarr;", "滑雪季 &rarr;"))}
      {carte_now("formule-1.html", "v2-now-gp", ("Monaco, June 2027", "Monaco, juin 2027", "摩纳哥，2027年6月"), ("The Grand Prix", "Le Grand Prix", "摩纳哥大奖赛"),
                 ("Terraces and boats for the race weekend sell out a season ahead.", "Les terrasses et les bateaux du week-end de course partent une saison à l'avance.", "比赛周末的观赛露台与游艇，提前一季便已售罄。"),
                 ("The Grand Prix weekend &rarr;", "Le week-end du Grand Prix &rarr;", "大奖赛周末 &rarr;"))}
    </div>
  </div>
</section>'''
i, j = section(h, '<section id="now"')
h = h[:i] + now + h[j:]

# ---------------------------------------------------------------- partenaires : bandeau qui défile
LOGOS = [("lux.svg", "LUX* Resorts &amp; Hotels", 40), ("dorchester.svg", "Dorchester Collection", 24), ("heritage.png", "Heritage Resorts", 56),
         ("luxaviation.svg", "Luxaviation", 26), ("p1-travel.svg", "P1 Travel", 50), ("f1-experiences.png", "F1 Experiences", 30),
         ("la-folie-douce.png", "La Folie Douce", 26)]
une = "".join(f'<img src="img/partenaires/{f}" alt="{a}" style="height:{hh}px" decoding="async">' for f, a, hh in LOGOS)
deux = "".join(f'<img src="img/partenaires/{f}" alt="" aria-hidden="true" style="height:{hh}px" decoding="async">' for f, a, hh in LOGOS)
part = f'''<section id="partners" class="sec-white">
  <div class="wrap">
    <div class="head reveal"><div class="eyebrow"><span class="n">06</span>{t("Partners", "Partenaires", "合作伙伴", "span", ' class="t"')}</div>{t("They work with us.", "Ils travaillent avec nous.", "与我们同行的伙伴。", "h2")}</div>
  </div>
  <div class="marquee" aria-label="Partners"><div class="track">{une}{deux}</div></div>
</section>'''
i, j = section(h, '<section id="partners"')
h = h[:i] + part + h[j:]
h = h.replace('<span class="n">06</span><span class="t" data-en="Contact"', '<span class="n">07</span><span class="t" data-en="Contact"')

# ---------------------------------------------------------------- styles du bandeau
h = h.replace("/* partenaires */", '''/* partenaires : bandeau qui défile sans s'arrêter */
.marquee{pointer-events:none;-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent;overflow:hidden;margin-top:40px;border-top:1px solid var(--gris-doux);border-bottom:1px solid var(--gris-doux);padding:38px 0;-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.track{display:flex;align-items:center;gap:80px;width:max-content;animation:defile 36s linear infinite;will-change:transform;-webkit-backface-visibility:hidden;backface-visibility:hidden}
.track img{width:auto;flex:none}
@keyframes defile{from{transform:translate3d(0,0,0)}to{transform:translate3d(-50%,0,0)}}
@media(max-width:860px){.marquee{padding:28px 0}.track{gap:52px;animation-duration:17s}.track img{transform:scale(.8)}}
@media(prefers-reduced-motion:reduce){.track{animation:none;flex-wrap:wrap;justify-content:center;width:auto}}
/* partenaires */''', 1)

# ---------------------------------------------------------------- carte : textes trilingues
i = h.index(" const P={paris:"); j = h.index("};", i) + 2
h = h[:i] + ''' const P={
  paris:{c:paris,n:["Paris","Paris","巴黎"],t:["The base","Notre base","大本营"],d:["Dinner at the Plaza Athénée, a private appointment on the Faubourg, the front row at Fashion Week.","Un dîner au Plaza Athénée, un rendez-vous privé dans une maison du Faubourg, le premier rang à la Fashion Week.","在雅典娜广场酒店晚餐，在圣奥诺雷街名店私享预约，坐上时装周的头排。"]},
  london:{c:[-0.1,51.5],n:["London","Londres","伦敦"],t:["An idea","Une idée","灵感"],d:["A late night at Tape, Sunday lunch in the countryside, Wimbledon in July.","Une fin de soirée au Tape, un déjeuner du dimanche à la campagne, Wimbledon en juillet.","在Tape畅玩至深夜，周日去乡间午餐，七月的温布尔登。"],k:"out"},
  alps:{c:[6.6,45.4],n:["The Alps","Les Alpes","阿尔卑斯"],t:["An idea","Une idée","灵感"],d:["Lunch on the terrace at La Folie Douce, a staffed chalet in Courchevel 1850, a helicopter drop for fresh snow.","Un déjeuner en terrasse à La Folie Douce, un chalet avec personnel à Courchevel 1850, une dépose en hélicoptère sur la neige fraîche.","在La Folie Douce露台午餐，入住库舍维尔1850配备管家的木屋，乘直升机直达新雪坡。"],k:"out"},
  milan:{c:[9.19,45.46],n:["Milan","Milan","米兰"],t:["An idea","Une idée","灵感"],d:["Fashion Week, a fitting in the Quadrilatero, an evening on Lake Como.","La Fashion Week, un essayage dans le Quadrilatero, une soirée au bord du lac de Côme.","米兰时装周，在四方区私享试衣，傍晚去科莫湖畔。"],k:"out"},
  riviera:{c:[5.6,43.25],n:["The Riviera","La Riviera","蔚蓝海岸"],t:["An idea","Une idée","灵感"],d:["The Monaco Grand Prix from a terrace, lunch at Club 55, a day on a yacht off Saint-Tropez.","Le Grand Prix de Monaco depuis une terrasse, un déjeuner au Club 55, une journée en yacht au large de Saint-Tropez.","在露台观赏摩纳哥大奖赛，于Club 55午餐，在圣特罗佩外海度过游艇一日。"],k:"out"},
  ibiza:{c:[1.43,38.9],n:["Ibiza","Ibiza","伊维萨"],t:["An idea","Une idée","灵感"],d:["Dinner on Formentera, a sunset table at Beso Beach, a villa above the cliffs.","Un dîner à Formentera, une table au coucher du soleil au Beso Beach, une villa au-dessus des falaises.","去福门特拉岛晚餐，在Beso Beach看日落，入住悬崖上的别墅。"],k:"out"},
  mykonos:{c:[25.3,37.4],n:["Mykonos","Mykonos","米科诺斯"],t:["An idea","Une idée","灵感"],d:["A party at Scorpios, a boat to Delos, a villa above the bay.","Une soirée au Scorpios, un bateau jusqu'à Délos, une villa au-dessus de la baie.","在Scorpios狂欢，乘船前往提洛岛，入住俯瞰海湾的别墅。"],k:"out"},
  marbella:{c:[-4.88,36.51],n:["Marbella","Marbella","马贝拉"],t:["An idea","Une idée","灵感"],d:["A long lunch at Puente Romano, Nikki Beach in the afternoon, a villa above the golf courses.","Un long déjeuner au Puente Romano, Nikki Beach l'après-midi, une villa au-dessus des golfs.","在Puente Romano悠长午餐，午后去Nikki Beach，入住俯瞰高尔夫球场的别墅。"],k:"out"}};''' + h[j:]
# la fiche et les noms suivent la langue affichée
h = h.replace(" const show=k=>{const v=P[k];info.innerHTML=`<span class=\"t\">${v.t}</span><h3>${v.n}</h3><p>${v.d}</p>`;",
              " const L=()=>({en:0,fr:1,zh:2}[document.documentElement.lang]||0);\n const show=k=>{const v=P[k],l=L();info.innerHTML=`<span class=\"t\">${v.t[l]}</span><h3>${v.n[l]}</h3><p>${v.d[l]}</p>`;info.dataset.k=k;")
h = h.replace(".style('font-size',size).text(k=>P[k].n);", ".style('font-size',size).attr('class','nm').text(k=>P[k].n[L()]);")
h = h.replace("dessine('#europe',", "show('paris');\n dessine('#europe',", 1) if "show('paris');" not in h else h
h = h.replace("})();\n</script>\n</body>", ''' new MutationObserver(()=>{const l=L();d3.selectAll('#europe .nm').text(k=>P[k].n[l]);show(info.dataset.k||'paris')}).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
})();
</script>
</body>''', 1)

# ---------------------------------------------------------------- styles de l'ancienne carte (Leaflet) : retirés
h = "\n".join(l for l in h.split("\n") if not re.match(r"\s*(\.leaflet|#leafletmap|\.maptabs|\.map-overview|\.mapcard|\.mapstage|\.mapgrid|\.mc-|\.partner-note)", l))

# ---------------------------------------------------------------- diaporama : deux photos
(SITE / "index.html").write_text(h, encoding="utf-8", errors="surrogateescape")
anim = (SITE / "anim.js").read_text(encoding="utf-8")
anim = anim.replace("var AUTRES_PHOTOS = ['hero-2', 'hero-3'];", "var AUTRES_PHOTOS = ['hero-2'];   /* le pont Alexandre III au coucher du soleil */")
anim = anim.replace("/* 2. L'ouverture : trois photos qui se relaient             */", "/* 2. L'ouverture : deux photos qui se relaient              */")
(SITE / "anim.js").write_text(anim, encoding="utf-8")
print("index.html écrit")
