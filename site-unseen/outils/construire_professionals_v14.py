"""
Construit la page « Professionals » (professionals.html), validée par Jay le 26/10/2026
(maquette « 11b Professionals SANS destinations »).

Les textes sont écrits dans les trois langues (data-en, data-fr, data-zh), le chinois
rédigé directement et non traduit mot à mot. Les styles viennent de la maquette.
Script à lancer une fois ; ensuite on modifie professionals.html directement.

Lancer, depuis le dossier du projet :
    python3 site-unseen/outils/construire_professionals_v14.py
"""
import html as H
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
MAQ = SITE.parent / "Livrables" / "Maquettes site (évolution)" / "11b Professionals SANS destinations (26-10).html"


def q(s):
    return H.escape(s, quote=True)


def t(en, fr, zh, balise="span", attrs=""):
    return f'<{balise}{attrs} data-en="{q(en)}" data-fr="{q(fr)}" data-zh="{q(zh)}">{en}</{balise}>'


def image(nom, alt):
    en, fr, zh = alt
    return (f'<picture><source type="image/avif" srcset="img/{nom}.avif"><img src="img/{nom}.webp" alt="{q(en)}" '
            f'data-alt-en="{q(en)}" data-alt-fr="{q(fr)}" data-alt-zh="{q(zh)}" loading="lazy"></picture>')


maq = MAQ.read_text(encoding="utf-8")
css = maq[maq.index("<style>") + 7:maq.index("</style>")]
css = css.replace("--accent:#7AA3BC;--sur-accent:#000;            /* saison active : Glacier */", "--accent:#7AA3BC;--sur-accent:#000;            /* remplacé par season.css */")
css += """
.lang{align-items:center;line-height:1}
.lang span{color:var(--trait);font-weight:400}
.lang button{background:none;border:0;font:inherit;line-height:1;color:var(--texte-3);cursor:pointer;padding:6px 2px}
.lang button[aria-pressed="true"]{color:var(--noir)}
.panel .langs{display:flex;gap:14px}
.panel .langs button{background:none;border:0;font:inherit;font-size:16px;color:var(--texte-3);padding:6px 0;cursor:pointer}
.panel .langs button[aria-pressed="true"]{color:var(--noir)}
.ph picture,.split-img picture{display:block;height:100%}
.hero picture{position:absolute;inset:0}
.hero h1{font-size:clamp(34px,4.6vw,60px);max-width:760px}
.hero-in{padding-top:120px}
:lang(zh) h1,:lang(zh) h2,:lang(zh) h3{font-family:'Noto Sans SC',sans-serif;font-weight:700;letter-spacing:0}
"""

MENU = [("index.html#services", "Services", "Services", "服务"), ("index.html#destinations", "Destinations", "Destinations", "目的地"),
        ("index.html#now", "Seasons", "Saisons", "当季"), ("professionals.html", "Professionals", "Professionnels", "合作伙伴"),
        ("#contact", "Contact", "Contact", "联系我们")]
nav = "".join(t(en, fr, zh, "a", f' href="{h}"' + (' class="on"' if h == "professionals.html" else "")) for h, en, fr, zh in MENU)
nav_panel = "".join(t(en, fr, zh, "a", f' href="{h}"') for h, en, fr, zh in MENU)
LANGS = '<button type="button" data-l="en" aria-pressed="true">EN</button><span>/</span><button type="button" data-l="fr" aria-pressed="false">FR</button><span>/</span><button type="button" data-l="zh" aria-pressed="false" lang="zh">中文</button>'

ETAPES = [
    (("The brief", "Le brief", "需求"), ("Dates, guests, what they expect. A message is enough.", "Les dates, les invités, ce qu'ils attendent. Un message suffit.", "日期、客人、期望。一条消息就够。")),
    (("The answer", "La réponse", "答复"), ("What is possible, in writing, within the day.", "Ce qui est possible, par écrit, dans la journée.", "当天书面告知可行方案。")),
    (("Your terms", "Vos conditions", "合作条款"), ("Agreed with you before the first request, never discussed with your client.", "Convenues avec vous avant la première demande, jamais discutées devant votre client.", "在首次合作前与您约定，绝不在您的客户面前讨论。")),
    (("On the ground", "Sur place", "落地执行"), ("One person follows your clients from arrival to departure.", "Une seule personne suit vos clients de l'arrivée au départ.", "从抵达到离开，由同一位专人全程跟进。")),
    (("The debrief", "Le compte rendu", "回访"), ("A short note after the stay, so the next one is even easier.", "Une courte note après le séjour, pour que le suivant soit encore plus simple.", "行程结束后附上简短回顾，让下一次更加顺畅。")),
]

PUBLICS = [
    ("pro-agencies", ("Monaco harbour at night", "Le port de Monaco la nuit", "夜色中的摩纳哥港"),
     ("Agencies & DMCs", "Agences et DMC", "旅行社与目的地管理公司"),
     ("You sell the trip. We make France work.", "Vous vendez le voyage. Nous faisons fonctionner la France.", "行程由您设计，法国的一切由我们落实。"),
     ("Your itinerary stays yours. We add what a local team can open: tables, suites, access, drivers, and the last-minute changes.",
      "Votre itinéraire reste le vôtre. Nous ajoutons ce qu'une équipe sur place sait ouvrir : tables, suites, accès, chauffeurs, et les changements de dernière minute.",
      "行程依旧属于您。我们补上只有本地团队才能打开的部分：餐桌、套房、准入、专车，以及最后一刻的变动。"),
     ("An agency in Mumbai sends a family of six for five days. We hold two suites on the Avenue Montaigne, a chef's table, a private visit of the Louvre at opening, and a car for the week. The agency hears from us after each day.",
      "Une agence de Mumbai envoie une famille de six personnes pour cinq jours. Nous retenons deux suites avenue Montaigne, une table du chef, une visite privée du Louvre à l'ouverture et une voiture pour la semaine. L'agence reçoit un point chaque soir.",
      "孟买一家旅行社送来六口之家，停留五天。我们为其预留蒙田大道的两间套房、一张主厨餐桌、卢浮宫开馆时的私人参观，以及一周的专车。每天结束后，我们都会向旅行社汇报。")),
    ("pro-aviation", ("A private van with leather seats", "Un van privé aux sièges en cuir", "配备真皮座椅的私人商务车"),
     ("Private aviation", "Aviation privée", "私人航空"),
     ("Once your passengers have landed in France, we look after their stay.", "Une fois vos passagers posés en France, nous prenons soin de leur séjour.", "您的乘客在法国落地之后，余下的行程交给我们。"),
     ("Car at the aircraft, hotel, dinner, the next day. Your crew flies, we take the ground.",
      "La voiture au pied de l'avion, l'hôtel, le dîner, le lendemain. Votre équipage vole, nous prenons le relais au sol.",
      "机旁接机、酒店、晚餐，乃至第二天的安排。机组负责飞行，地面由我们接手。"),
     ("A charter lands at Le Bourget on Friday night. A driver is at the stairs, the suite is ready, a table is held for 10 pm, and Saturday is planned around the boutique appointments.",
      "Un vol privé se pose au Bourget le vendredi soir. Le chauffeur attend au pied de la passerelle, la suite est prête, une table est retenue pour 22 h, et le samedi s'organise autour des rendez-vous en boutique.",
      "一架包机周五晚间降落勒布尔歇机场。司机已在舷梯旁等候，套房已备妥，晚上十点的餐桌已预留，周六则围绕精品店的预约来安排。")),
    ("pro-sport", ("A private gym with a city view", "Une salle de sport privée avec vue sur la ville", "俯瞰城市的私人健身房"),
     ("Athletes & agents", "Sportifs et agents", "运动员与经纪人"),
     ("Discreet stays around the calendar.", "Des séjours discrets, autour du calendrier.", "围绕赛程，低调安排每一次出行。"),
     ("Private gym hours, recovery on site, meals built around a plan, arrivals that avoid the lobby. For the athlete, the family and the entourage.",
      "Des créneaux privés en salle de sport, la récupération sur place, des repas pensés selon un plan, des arrivées qui évitent le hall. Pour le sportif, sa famille et son entourage.",
      "私人健身时段、现场恢复理疗、按营养计划定制的餐食，以及避开大堂的出入动线。为运动员本人、家人与团队而设。"),
     ("A player's family travels for a match in Paris. A private floor, a nutritionist's menu, seats for the family, a quiet exit after the final whistle.",
      "La famille d'un joueur vient pour un match à Paris. Un étage privatisé, un menu de nutritionniste, des places pour la famille, une sortie discrète après le coup de sifflet final.",
      "一位球员的家人来巴黎观赛。整层私享、营养师定制菜单、家属观赛席位，终场哨响后安静离场。")),
    ("pro-embassy", ("A Haussmann façade in Paris", "Une façade haussmannienne à Paris", "巴黎的奥斯曼风格建筑立面"),
     ("Embassies & missions", "Ambassades et missions", "使馆与外交使团"),
     ("The details around official visits.", "Les détails autour des visites officielles.", "官方访问之外的每一处细节。"),
     ("The protocol is yours. We handle what surrounds it: accommodation for the delegation, dinners, shopping, family programmes.",
      "Le protocole vous appartient. Nous gérons ce qui l'entoure : l'hébergement de la délégation, les dîners, le shopping, les programmes pour les familles.",
      "礼宾由您负责。我们处理其余的一切：代表团住宿、晚宴、购物，以及家属行程。"),
     ("A delegation of twelve for three days. Rooms on one floor, a private dining room for the second evening, a programme for the spouses, and one contact for the embassy.",
      "Une délégation de douze personnes pendant trois jours. Des chambres sur un même étage, un salon privé pour le deuxième soir, un programme pour les conjoints, et un seul contact pour l'ambassade.",
      "十二人代表团，为期三天。同层客房、第二晚的私人包厢、为配偶准备的专属行程，使馆只需对接一位联系人。")),
    ("pro-events", ("Guests and photographers at a private evening", "Invités et photographes lors d'une soirée privée", "私人晚会上的宾客与摄影师"),
     ("Weddings & events", "Mariages et événements", "婚礼与活动"),
     ("Your guests, looked after in France.", "Vos invités, pris en charge en France.", "您的宾客，在法国有人照料。"),
     ("For planners bringing a celebration to Paris or the Riviera: guest stays, transfers, dinners, the day after.",
      "Pour les organisateurs qui font venir une célébration à Paris ou sur la Riviera : les séjours des invités, les transferts, les dîners, le lendemain.",
      "为将庆典带到巴黎或蔚蓝海岸的策划人：宾客住宿、接送、晚宴，以及庆典后的安排。"),
     ("Eighty guests for a wedding on the Riviera. Hotels by family, airport welcome, a rehearsal dinner by the sea, and a concierge desk for the whole week.",
      "Quatre-vingts invités pour un mariage sur la Riviera. Les hôtels par famille, l'accueil à l'aéroport, un dîner de répétition au bord de la mer, et un comptoir de conciergerie pour toute la semaine.",
      "蔚蓝海岸的一场婚礼，八十位宾客。按家庭安排酒店、机场迎接、海边彩排晚宴，整周设有礼宾服务台。")),
    ("pro-hotels", ("The Mondo restaurant at LUX* Belle Mare, Mauritius", "Le restaurant Mondo du LUX* Belle Mare, à Maurice", "毛里求斯LUX* Belle Mare的Mondo餐厅"),
     ("Hotels & resorts", "Hôtels et resorts", "酒店与度假村"),
     ("Your guests, before and after your doors.", "Vos clients, avant et après votre porte.", "在您的酒店之外，继续照料您的客人。"),
     ("We send an international clientele to a limited number of houses, and look after them in Paris before they fly to you.",
      "Nous adressons une clientèle internationale à un nombre limité de maisons, et nous en prenons soin à Paris avant qu'elle ne s'envole vers vous.",
      "我们只为少数酒店输送国际客人，并在他们飞往您那里之前，在巴黎照料好他们。"),
     ("A couple stays three nights in Paris before Mauritius. We arrange the city, then hand them over to the resort with their preferences already known.",
      "Un couple passe trois nuits à Paris avant Maurice. Nous organisons la ville, puis nous le confions au resort avec ses préférences déjà connues.",
      "一对夫妇飞往毛里求斯前在巴黎停留三晚。我们安排好巴黎的一切，再把他们交给度假村，连同已知的偏好一起。")),
]

onglets = "".join(t(*p[2], "button", f' type="button" data-i="{i}"' + (' class="on"' if i == 0 else "")) for i, p in enumerate(PUBLICS))
fiches = ""
for i, (img, alt, tag, titre, texte, exemple) in enumerate(PUBLICS):
    fiches += (f'<div class="pub{" on" if i == 0 else ""}"><div class="ph">{image(img, alt)}</div><div>'
               f'{t(*tag, "span", " class=\"tag\"")}{t(*titre, "h3")}{t(*texte, "p")}'
               f'<div class="ex">{t("A request, start to finish", "Une demande, du début à la fin", "一次委托，从头到尾", "b")}{t(*exemple)}</div></div></div>\n      ')

LOGOS = [("lux.svg", "LUX* Resorts &amp; Hotels", 40), ("dorchester.svg", "Dorchester Collection", 24), ("heritage.png", "Heritage Resorts", 56),
         ("luxaviation.svg", "Luxaviation", 26), ("p1-travel.svg", "P1 Travel", 50), ("f1-experiences.png", "F1 Experiences", 30),
         ("la-folie-douce.png", "La Folie Douce", 26)]
logos = "".join(f'<img src="img/partenaires/{f}" alt="{a}" style="height:{h}px" decoding="async">' for f, a, h in LOGOS)
logos += "".join(f'<img src="img/partenaires/{f}" alt="" aria-hidden="true" style="height:{h}px" decoding="async">' for f, a, h in LOGOS)

CHOIX = [("Agency or DMC", "Agence ou DMC", "旅行社或目的地管理公司"), ("Private aviation", "Aviation privée", "私人航空"),
         ("Sports management", "Agent de sportifs", "体育经纪"), ("Embassy", "Ambassade", "使馆"),
         ("Planner", "Organisateur d'événements", "活动策划"), ("Hotel or resort", "Hôtel ou resort", "酒店或度假村"), ("Other", "Autre", "其他")]
options = "".join(t(*c, "option") for c in CHOIX)

etapes = "".join(f"<li>{t(*e[0], 'h3')}{t(*e[1], 'p')}</li>" for e in ETAPES)

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#FFFFFF">
<title>UNSEEN. — For travel professionals</title>
<meta name="description" content="UNSEEN. for travel agencies, DMCs, private aviation, sports management, embassies and planners: your clients in France, looked after through one point of contact.">
<meta property="og:title" content="UNSEEN. — For travel professionals">
<meta property="og:description" content="Your clients in France, looked after as you would yourself.">
<meta property="og:image" content="https://unseenconciergerie.com/img/hero.jpg">
<meta property="og:type" content="website">
<meta property="og:url" content="https://unseenconciergerie.com/professionals.html">
<link rel="canonical" href="https://unseenconciergerie.com/professionals.html">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
<style>{css}</style>
<link rel="stylesheet" href="season.css">
</head>
<body>

<header class="top">
  <div class="top-in">
    <a class="mark" href="index.html">UNSEEN.</a>
    <nav class="nav">{nav}</nav>
    <div class="lang">{LANGS}</div>
    <button class="burger" id="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="panel"><span></span><span></span><span></span></button>
  </div>
</header>
<nav class="panel" id="panel" aria-hidden="true">
  {nav_panel}
  <div class="bas"><a href="https://wa.me/33613850733">WhatsApp</a><a href="mailto:contact@unseenconciergerie.com">contact@unseenconciergerie.com</a><div class="langs">{LANGS}</div></div>
</nav>

<div class="hero">
  {image("pro-hero", ("A private jet on a snowy runway", "Un jet privé sur une piste enneigée", "停在雪地跑道上的私人飞机")).replace(' loading="lazy"', ' fetchpriority="high"')}
  <div class="hero-in">
    {t("For travel professionals", "Pour les professionnels du voyage", "致旅行行业伙伴", "div", ' class="k"')}
    {t("Your clients in France, looked after as you would yourself.", "Vos clients en France, comme si vous étiez là.", "您的客户在法国，我们像您一样用心照料。", "h1")}
    {t("Agencies, private aviation, sports management, embassies, planners. When your clients land, UNSEEN. takes over the ground, discreetly, through one point of contact.",
       "Agences, aviation privée, agents de sportifs, ambassades, organisateurs. Quand vos clients atterrissent, UNSEEN. prend le relais au sol, discrètement, avec un seul interlocuteur.",
       "旅行社、私人航空、体育经纪、使馆、活动策划。您的客户一落地，UNSEEN.便低调接手地面的一切，全程只需一位联系人。", "p")}
    <div class="row">{t("Send us a brief", "Envoyer une demande", "提交需求", "a", ' class="btn btn-accent" href="#contact"')}<a class="btn btn-ghost" href="https://wa.me/33613850733">WhatsApp</a></div>
  </div>
</div>

<section>
  <div class="wrap split">
    <div class="split-img rv">{image("pro-bar", ("A bar lit in amber", "Un bar aux lumières ambrées", "琥珀色灯光下的酒吧"))}</div>
    <div class="rv">
      <div class="eyebrow"><span class="n">01</span>{t("What we handle", "Ce que nous prenons en charge", "我们负责什么", "span", ' class="t"')}</div>
      {t("Everything that happens once they land.", "Tout ce qui se passe une fois qu'ils ont atterri.", "落地之后的一切。", "h2")}
      {t("You keep the client and the relationship. We take care of what happens on the ground, and keep you informed at every step.",
         "Vous gardez le client et la relation. Nous nous occupons de ce qui se passe sur place, et vous tenons informé à chaque étape.",
         "客户与关系始终属于您。我们负责地面的一切，并在每一步向您通报。", "p", ' class="lede"')}
      {t("A <strong>palace suite</strong> that never appears online. A <strong>table</strong> at the restaurant that is full, on the evening they want it. A <strong>driver</strong> waiting at the aircraft. A seat at the <strong>Fashion Week</strong> show or the <strong>Grand Prix</strong>. A <strong>private appointment</strong> with a maison. And everything nobody planned, handled by the same person, from arrival to departure.",
         "Une <strong>suite de palace</strong> qui n'apparaît jamais en ligne. Une <strong>table</strong> dans le restaurant complet, le soir voulu. Un <strong>chauffeur</strong> qui attend au pied de l'avion. Une place au défilé de la <strong>Fashion Week</strong> ou au <strong>Grand Prix</strong>. Un <strong>rendez-vous privé</strong> dans une maison. Et tout ce que personne n'avait prévu, géré par la même personne, de l'arrivée au départ.",
         "从不在网上出现的<strong>殿堂级酒店套房</strong>。客满餐厅里、指定当晚的<strong>餐桌</strong>。在飞机旁等候的<strong>专车司机</strong>。<strong>时装周</strong>秀场或<strong>大奖赛</strong>的座位。品牌名店的<strong>私人预约</strong>。还有一切计划之外的事，从抵达到离开，都由同一个人处理。", "p", ' class="prose"')}
    </div>
  </div>
</section>

<section class="sable">
  <div class="wrap">
    <div class="eyebrow"><span class="n">02</span>{t("How it works", "Comment ça se passe", "合作流程", "span", ' class="t"')}</div>
    {t("One brief. One contact. No surprises.", "Une demande. Un interlocuteur. Aucune surprise.", "一份需求，一位联系人，没有意外。", "h2")}
    <ol class="steps rv">{etapes}</ol>
  </div>
</section>

<section class="sombre">
  <div class="wrap">
    <div class="eyebrow"><span class="n">03</span>{t("Who we work with", "Avec qui nous travaillons", "我们的合作对象", "span", ' class="t"')}</div>
    {t("Each partner has its own way of working.", "Chaque partenaire a sa façon de travailler.", "每一位伙伴，都有自己的合作方式。", "h2")}
    {t("Choose yours: what we do for you, and what a request looks like, start to finish.",
       "Choisissez le vôtre : ce que nous faisons pour vous, et à quoi ressemble une demande, du début à la fin.",
       "请选择您的类型：我们能为您做什么，一次委托从头到尾是什么样子。", "p", ' class="lede"')}
    <div class="tabs" id="tabs">{onglets}</div>
    <div class="pubs" id="pubs">
      {fiches}
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="eyebrow"><span class="n">04</span>{t("Partners", "Partenaires", "合作伙伴", "span", ' class="t"')}</div>
    {t("They work with us.", "Ils travaillent avec nous.", "与我们同行的伙伴。", "h2")}
  </div>
  <div class="marquee" aria-label="Partners"><div class="track">{logos}</div></div>
</section>

<section class="sombre" id="contact">
  <div class="wrap contact">
    <div>
      <div class="eyebrow"><span class="n">05</span>{t("Contact", "Contact", "联系我们", "span", ' class="t"')}</div>
      {t("Send us your next brief.", "Envoyez-nous votre prochaine demande.", "把下一份需求交给我们。", "h2")}
      {t("Terms, references and a sample programme for your clients are shared by email, on request.",
         "Nos conditions, nos références et un exemple de programme pour vos clients vous sont envoyés par e-mail, sur demande.",
         "合作条款、参考案例和客户行程示例，可应要求通过电子邮件发送。", "p", ' class="lede"')}
      <div style="margin-top:36px">
        <div class="ci">{t("Partnerships", "Partenariats", "合作洽谈")}<a href="mailto:partners@unseenconciergerie.com">partners@unseenconciergerie.com</a></div>
        <div class="ci"><span>WhatsApp</span><a href="https://wa.me/33613850733">+33 6 13 85 07 33</a></div>
        <div class="ci">{t("Direct", "Ligne directe", "直线电话")}<a href="tel:+33649668833">+33 6 49 66 88 33</a></div>
      </div>
    </div>
    <form id="proform" novalidate>
      <div><label for="p-nom">{t("Name", "Nom", "姓名")}</label><input id="p-nom" type="text" autocomplete="name"></div>
      <div><label for="p-soc">{t("Company", "Société", "公司")}</label><input id="p-soc" type="text" autocomplete="organization"></div>
      <div><label for="p-mail">{t("Email", "E-mail", "邮箱")}</label><input id="p-mail" type="email" autocomplete="email" inputmode="email"></div>
      <div><label for="p-type">{t("You are", "Vous êtes", "您的身份")}</label><select id="p-type">{options}</select></div>
      <div class="full"><label for="p-brief">{t("Your brief", "Votre demande", "您的需求")}</label><textarea id="p-brief" rows="3"></textarea></div>
      {t("Send", "Envoyer", "发送", "button", ' class="btn btn-accent" type="submit"')}
    </form>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="mark">UNSEEN.</div>
    <div style="margin-top:20px">{t("Private luxury concierge. Sole trader registered in France.", "Conciergerie privée de luxe. Entreprise individuelle immatriculée en France.", "私人尊享礼宾服务。法国注册个人企业。")} 8 rue du Docteur Gravery, 77100 Meaux. SIRET 999 356 587 00017.
      <br><a href="legal.html">{t("Legal notice, terms and privacy", "Mentions légales, conditions et confidentialité", "法律声明、条款与隐私")}</a></div>
  </div>
</footer>

<a class="wa" href="https://wa.me/33613850733" aria-label="WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.6.3-.2.2-.8.8-.8 1.9s.8 2.2.9 2.4c.1.1 1.6 2.5 4 3.5 1.5.6 2.1.7 2.8.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg></a>

<script>
// Langues : même mémoire que la page d'accueil (localStorage « unseen-lang »)
(function(){{
  var TITRES={{en:'UNSEEN. — For travel professionals',fr:'UNSEEN. — Pour les professionnels du voyage',zh:'UNSEEN. — 旅行行业合作'}};
  function setLang(l){{
    document.querySelectorAll('[data-en]').forEach(function(n){{var v=n.getAttribute('data-'+l);if(v!==null)n.innerHTML=v;}});
    document.querySelectorAll('[data-alt-en]').forEach(function(n){{var v=n.getAttribute('data-alt-'+l);if(v!==null)n.setAttribute('alt',v);}});
    document.documentElement.lang=l;document.title=TITRES[l];
    document.querySelectorAll('button[data-l]').forEach(function(b){{b.setAttribute('aria-pressed',b.dataset.l===l?'true':'false');}});
    try{{localStorage.setItem('unseen-lang',l);}}catch(e){{}}
  }}
  document.querySelectorAll('button[data-l]').forEach(function(b){{b.addEventListener('click',function(){{setLang(b.dataset.l);}});}});
  var s=null;try{{s=localStorage.getItem('unseen-lang');}}catch(e){{}}
  var nav=(navigator.language||'').toLowerCase();
  if(s==='fr'||s==='zh')setLang(s);else if(!s&&nav.indexOf('zh')===0)setLang('zh');else if(!s&&nav.indexOf('fr')===0)setLang('fr');
}})();
// Menu sur téléphone
var b=document.getElementById('burger'),pn=document.getElementById('panel');
b.onclick=function(){{var o=document.body.classList.toggle('menu-open');b.setAttribute('aria-expanded',o);pn.setAttribute('aria-hidden',!o);}};
pn.querySelectorAll('a').forEach(function(a){{a.onclick=function(){{document.body.classList.remove('menu-open');}};}});
// Onglets des publics
var bt=document.querySelectorAll('#tabs button'),pu=document.querySelectorAll('.pub');
bt.forEach(function(x){{x.onclick=function(){{bt.forEach(function(y){{y.classList.remove('on');}});x.classList.add('on');pu.forEach(function(p,i){{p.classList.toggle('on',i==x.dataset.i);}});x.scrollIntoView({{behavior:'smooth',inline:'center',block:'nearest'}});}};}});
// Formulaire : prépare un e-mail à partners@ (le site n'a pas de serveur)
document.getElementById('proform').addEventListener('submit',function(e){{
  e.preventDefault();
  var v=function(id){{return document.getElementById(id).value.trim();}};
  var corps='Name: '+v('p-nom')+'\\nCompany: '+v('p-soc')+'\\nEmail: '+v('p-mail')+'\\nType: '+document.getElementById('p-type').selectedOptions[0].text+'\\n\\n'+v('p-brief');
  location.href='mailto:partners@unseenconciergerie.com?subject='+encodeURIComponent('Brief: '+(v('p-soc')||v('p-nom')))+'&body='+encodeURIComponent(corps);
}});
// Apparition douce
var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target);}}}});}},{{threshold:.12}});
document.querySelectorAll('.rv').forEach(function(el){{io.observe(el);}});
</script>
</body>
</html>
'''
(SITE / "professionals.html").write_text(page, encoding="utf-8")
print("professionals.html écrit")
