"""
Applique la maquette 12c (validée par Jay le 27/10/2026) à la vraie page professionals.html.

Reprend les blocs et le français réécrit de Livrables/Maquettes site (évolution)/_script_v5.py,
et ajoute le chinois (écrit directement en chinois, pas traduit mot à mot) de tous les nouveaux
textes. Différences avec la maquette : chemins du site, photo « Qui nous sommes » en avif/webp
(img/pro-qui.*), pas de bandeau « maquette », la page s'ouvre dans la langue du visiteur.

À lancer une seule fois (la page est modifiée sur place), depuis le dossier du projet :
    python3 site-unseen/outils/appliquer_pro_12c.py
"""
import html
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
PAGE = ICI.parent / "professionals.html"
sys.path.insert(0, str(ICI.parents[1] / "Livrables" / "Maquettes site (évolution)"))
import _script_v5 as v  # noqa: E402  (blocs, textes FR réécrits, styles)

# Chinois de chaque texte anglais nouveau ou modifié (clé = texte anglais exact)
ZH = {
    # Qui nous sommes
    "Who we are": "关于我们",
    "An independent concierge, based in Paris.": "一家扎根巴黎的独立礼宾机构。",
    "In Paris, we are the local network your clients do not have. Beyond Paris, we follow them wherever they go: the Alps in winter, the Riviera in summer, the rest of Europe on request.":
        "在巴黎，我们就是您的客户所缺少的那份本地人脉。离开巴黎，我们同样随行：冬季的阿尔卑斯，夏季的蔚蓝海岸，以及他们想去的欧洲任何地方。",
    "Each request is handled personally, with the partner best placed for it, and stays between us, you and the client.":
        "每一项需求都由专人亲自处理，交给最合适的合作伙伴完成，并且只在您、您的客户与我们之间。",
    "Independent": "独立", "No group, no booking network, no imposed inventory.": "不隶属任何集团或预订网络，没有必须推销的固定产品。",
    "International": "国际化", "Clients from the Middle East, Asia, the United States and Europe.": "客户来自中东、亚洲、美国与欧洲。",
    # Ce que vous pouvez nous demander
    "What you can ask us": "您可以交给我们的事", "Everything your clients may ask for in France.": "您的客户在法国的一切所需。",
    "Palace hotels": "殿堂级酒店", "Reservations, upgrades and suites, in Paris and wherever your clients travel.": "预订、升级与套房安排，在巴黎，也在客户前往的任何地方。",
    "Fine dining": "星级餐饮", "Michelin-starred tables, private rooms and chef's tables, often at short notice.": "米其林星级餐厅、私人包厢与主厨餐桌，临时需求也能安排。",
    "Shopping and sourcing": "私人购物与寻物", "Private appointments at the luxury houses, pieces that are hard to find, styling.": "奢侈品牌的私享预约、难觅单品的搜寻，以及造型建议。",
    "Events and access": "赛事与活动", "Formula 1, Roland-Garros, Fashion Week, football, private previews.": "F1大奖赛、法网、时装周、足球赛事与私人预展。",
    "Private transport": "私人出行", "Chauffeured cars, airport transfers, helicopters, private aviation through our partners.": "专车司机、机场接送、直升机，以及经合作伙伴安排的私人飞机。",
    "Evenings": "夜间安排", "Tables at the right venues, private clubs, evenings arranged end to end.": "热门场所的座位、私人会所，整晚行程一手安排。",
    "Seasons": "季节目的地", "Chalets in winter; villas, beach clubs and yachts in summer.": "冬季的雪山木屋；夏季的别墅、海滩俱乐部与游艇。",
    "Tailor-made": "量身定制", "Family stays, celebrations, anything that does not fit a category.": "家庭出游、庆典活动，以及任何无法归类的需求。",
    # Nos engagements
    "Our commitments": "我们的承诺",
    "A real person, every time.": "每一次，都是真人回复。", "Every message is answered by someone who knows your request. No bots, no call centre.": "每条消息都由熟悉您需求的人亲自回复，没有机器人，也没有呼叫中心。",
    "A first answer within 24 hours.": "24小时内首次答复。", "For every request, wherever you are.": "无论您身在何处，每项需求皆如此。",
    "Partners we know.": "熟悉可靠的合作伙伴。", "Each request goes to the supplier best placed for it.": "每项需求都交给最合适的服务商。",
    "One clear price.": "一个清晰的价格。", "Confirmed in writing before anything is booked.": "预订前以书面形式确认。",
    "Discretion.": "绝对保密。", "Nothing about a client is shared without their consent.": "未经客户同意，不透露任何信息。",
    # Onglets : intitulés communs
    "What we do for you": "我们为您做什么", "Sample programme": "行程示例",
    "A fictional example. Each programme is quoted on request.": "示例为虚构内容。每份行程均按需单独报价。",
    "Arrival.": "抵达。", "Departure.": "离开。",
    # Agences et DMC
    "Your client stays yours.": "客户始终属于您。", "We never approach your client for ourselves, during or after the stay.": "无论行程期间还是结束后，我们都不会私下联系您的客户。",
    "You stay informed.": "全程知情。", "Updates at each step, with your client's agreement.": "在客户同意的前提下，每个环节都会向您同步。",
    "Paris, and beyond.": "巴黎，以及更远的地方。", "Paris, then the Alps, the Riviera or elsewhere in Europe, as one trip.": "从巴黎到阿尔卑斯、蔚蓝海岸或欧洲其他城市，串联成一段完整旅程。",
    "It works both ways.": "合作是双向的。", "When our clients travel to your region, we think of you first.": "当我们的客户前往您所在的地区，我们首先想到的是您。",
    "A Gulf family, four nights in Paris.": "海湾家庭，巴黎四晚。", "Parents, three children and a nanny, arriving by private jet in June.": "父母、三个孩子和一位保姆，六月乘私人飞机抵达。",
    "Car and luggage van at the aircraft, connecting suites in a palace, the family's routines shared before arrival.": "专车与行李车在机旁等候，入住殿堂级酒店的连通套房，家庭的生活习惯提前告知酒店。",
    "Day 2, the city at their pace.": "第二天，按他们的节奏游巴黎。", "A private guide at the Louvre, lunch in a private room, shopping by appointment for the parents.": "卢浮宫私人导览，私人包厢午餐，父母享受预约购物。",
    "Day 3, outside Paris.": "第三天，走出巴黎。", "Disneyland Paris with a VIP guide for the children, then a table that is usually fully booked.": "孩子们由VIP导游陪同畅游巴黎迪士尼，晚上入座一家平时一位难求的餐厅。",
    "Purchases collected, the same driver back to the aircraft, luggage sent ahead.": "所购物品统一取回，同一位司机送回机旁，行李提前送达。",
    # Aviation privée
    "At the aircraft.": "机旁迎候。", "A driver at the stairs and a luggage van, at any hour.": "司机在舷梯旁等候，另备行李车，全天候待命。",
    "The stay, ready.": "落地即可入住。", "Suite, tables and appointments arranged before the wheels touch down.": "套房、餐厅与各项预约，在飞机落地前已全部安排妥当。",
    "Access.": "专属通道。", "Grand Prix, Roland-Garros, Fashion Week and private evenings, through our partners.": "通过合作伙伴，安排F1大奖赛、法网、时装周与私人晚宴。",
    "Your passengers stay yours.": "乘客始终属于您。", "We never approach your passengers for ourselves.": "我们不会私下联系您的乘客。",
    "Paris, then the Alps.": "先巴黎，后阿尔卑斯。", "A couple and their two teenagers: Christmas in Paris, New Year in Courchevel.": "一对夫妇带着两个十几岁的孩子：圣诞在巴黎，新年在库舍维尔。",
    "Paris, three nights.": "巴黎，三晚。", "Palace hotel, Christmas shopping by appointment, a festive dinner, an evening at a show.": "入住殿堂级酒店，预约圣诞购物，一顿节日晚宴，一晚演出。",
    "The transfer.": "转场。", "Private jet or helicopter to Courchevel, luggage and skis sent ahead.": "乘私人飞机或直升机前往库舍维尔，行李与雪具提前送达。",
    "Courchevel, four nights.": "库舍维尔，四晚。", "Chalet on the slopes, passes and equipment ready, a table on the mountain every day.": "入住雪道旁的木屋，雪票与装备到达即备好，每天在山上订好午餐座位。",
    "New Year's Eve.": "跨年夜。", "A table for the evening, and cars both ways.": "预订跨年晚宴，往返均有专车。",
    # Sportifs et agents
    "Training and recovery.": "训练与恢复。",
    "Private gym sessions, physiotherapy, massage and cryotherapy, booked around training, after matches and at the end of the season.": "私人健身房、理疗、按摩与冷冻疗法，围绕训练时间安排，帮助赛后与赛季结束后的恢复。",
    "Rest and privacy.": "休息与私密。", "Quiet suites, a private floor when needed, discreet arrivals and departures.": "安静的套房，需要时可包下整层，进出低调不受打扰。",
    "The right table.": "合适的餐桌。", "Restaurants briefed on the nutrition plan, a chef at the residence on request.": "餐厅提前了解营养方案，也可安排私厨上门。",
    "Cars and drivers.": "车辆与司机。", "Chauffeured cars, and sports or luxury cars delivered where needed.": "专车司机，或将跑车、豪华车送到指定地点。",
    "Family and entourage.": "家人与随行人员。", "Plans for partners, children and friends while the athlete trains or competes.": "运动员训练或比赛期间，为伴侣、孩子与朋友安排行程。",
    "Nothing goes public.": "绝不外传。", "No photos, no posts, no names shared, during or after the stay.": "行程期间及之后，不拍照、不发布、不透露任何姓名。",
    "A tournament in Paris.": "巴黎的一场大赛。", "A player and their team, ten days in Paris during a major tournament.": "一位球员与团队，在一项重大赛事期间于巴黎停留十天。",
    "Car at the airport, a hotel close to the venue, a quiet floor, a room set up for rest.": "机场专车接机，入住赛场附近的酒店，安静的楼层，房间为休息专门布置。",
    "Match and training days.": "比赛与训练日。", "Cars at fixed times, a restaurant that follows the nutrition plan, physiotherapy between sessions.": "专车定时接送，餐厅按营养方案备餐，训练间隙安排理疗。",
    "Rest days.": "休息日。", "A private dinner, shopping by appointment before the shops open.": "一顿私人晚宴，商店开门前的预约购物。",
    "The family.": "家人。", "Seats, transport and plans for the family on match days.": "比赛日为家人安排座位、交通与行程。",
    # Ambassades et missions
    "Hosting.": "接待。", "Arrivals, hotels and programmes for visiting delegations and guests.": "为来访的代表团与宾客安排接机、酒店与日程。",
    "Everyday errands.": "日常事务。", "Food halls, deliveries, gifts for official occasions.": "高端食品采购、配送，以及正式场合的礼品。",
    "Children and families.": "孩子与家庭。", "Disneyland Paris, museum workshops, sports clubs, school holidays.": "巴黎迪士尼、博物馆工作坊、体育俱乐部与假期安排。",
    "Home and logistics.": "居家与手续。", "Trusted providers and the many small steps of a new posting.": "可靠的居家服务商，以及新任职时的各种琐碎手续。",
    "Discretion by default.": "始终保密。", "Nothing about the mission or its families is shared.": "使团及其家属的任何信息都不会外泄。",
    "A delegation on an official visit.": "代表团正式访问。", "Eight people, three days, an agenda set by the protocol office.": "八人，三天，日程由礼宾处制定。",
    "Cars at the airport, rooms ready, the schedule checked with protocol the evening before.": "机场专车接机，房间提前备好，前一晚与礼宾处核对日程。",
    "Meeting days.": "会议日。", "Cars on standby, lunches close to each appointment, official gifts chosen and wrapped.": "专车全程待命，午餐就近安排，正式礼品挑选并包装妥当。",
    "The evening.": "晚间。", "A dinner for the delegation in a private room.": "在私人包厢为代表团设宴。",
    "Luggage collected, cars to the airport at the agreed time.": "酒店取回行李，按约定时间送往机场。",
    # Mariages et événements
    "Guests by family.": "按家庭安排宾客。", "Hotels chosen by family, rooms on the same floor, menus agreed in advance.": "为每个家庭挑选酒店，房间安排在同一楼层，菜单提前确认。",
    "Arrivals and transfers.": "抵达与接送。", "Airport welcome, cars and luggage vans, the train or the aircraft to the celebration.": "机场迎接，专车与行李车，再乘火车或飞机前往婚礼举办地。",
    "The wedding shopping.": "婚礼采购。", "Jewellery and outfits by private appointment.": "珠宝与礼服，私享预约选购。",
    "The planner stays in charge.": "由您主导。", "You remain the family's contact. We report to you after each step.": "您始终是这家人的联系人，每个环节结束后我们都会向您汇报。",
    "A wedding family, before the celebration.": "婚礼前，一家人在巴黎。", "Twelve guests, three nights in Paris on their way to a wedding elsewhere in Europe.": "十二位宾客，前往欧洲其他地方参加婚礼前，在巴黎停留三晚。",
    "Cars and a luggage van, rooms on the same floor, vegetarian menus agreed with the hotel.": "专车与行李车，房间同一楼层，与酒店提前确认素食菜单。",
    "Day 2, the shopping.": "第二天，采购。", "Jewellery and outfits by private appointment, a private room for twelve in the evening.": "珠宝与礼服私享预约，晚上为十二人预留私人包厢。",
    "Day 3, two paces.": "第三天，各取所需。", "A quiet day with a driver for the elders, the Seine and an evening out for the younger guests.": "长辈由司机陪同轻松度过一天，年轻人游塞纳河并外出共度夜晚。",
    "Luggage and purchases taken to the train or the aircraft.": "行李与所购物品送至火车站或机场。",
    # Hôtels et resorts
    "What we bring.": "我们带来什么。", "Guests prepared in advance: preferences, arrival times, one contact before, during and after.": "提前告知宾客信息：喜好、抵达时间，入住前、中、后都由一人对接。",
    "What we look for.": "我们期待什么。", "A dedicated contact, priority on the dates that matter, terms agreed with each house.": "一位专属联系人，关键日期优先保障，并与每家酒店约定合作条款。",
    "Your guest stays yours.": "宾客始终属于您。", "We never approach your guests for ourselves.": "我们不会私下联系您的宾客。",
    "A few houses.": "少而精的合作。", "A limited number of partners in each market, so that each one matters.": "每个目的地只与少数伙伴合作，让每一家都举足轻重。",
    "A guest of your resort heading to Paris.": "您的度假村宾客前往巴黎。", "A family who stays with you every year spends a week in Paris in spring.": "一个每年都入住您度假村的家庭，春天在巴黎度过一周。",
    "Car at the aircraft, suites in a palace, preferences passed on by your team.": "机旁专车迎接，入住殿堂级酒店套房，喜好由您的团队提前告知。",
    "The week.": "这一周。", "Shopping by appointment, tables that are hard to get, a day at Roland-Garros.": "预约购物，一位难求的餐厅，以及一天的法网观赛。",
    "The same driver to the aircraft, purchases packed and checked.": "同一位司机送至机旁，所购物品包装并清点妥当。",
    "Your team.": "您的团队。", "Kept informed at each step. The guest remains yours.": "每一步都同步告知。宾客始终属于您。",
    # Où et quand
    "Where and when": "何地，何时", "Paris all year. The Alps and the Riviera in season.": "巴黎全年无休，阿尔卑斯与蔚蓝海岸随季而行。",
    "Winter": "冬季", "Courchevel, Megève, Val d'Isère, Gstaad.": "库舍维尔、梅杰夫、瓦勒迪泽尔、格施塔德。",
    "Spring": "春季", "Monaco Grand Prix, Cannes, Roland-Garros.": "摩纳哥大奖赛、戛纳电影节、法网。",
    "Summer": "夏季", "Saint-Tropez, Cannes, Monaco, villas and yachts.": "圣特罗佩、戛纳、摩纳哥、别墅与游艇。",
    "Autumn": "秋季", "Paris Fashion Week, the art fairs, the Paris season.": "巴黎时装周、艺术博览会、巴黎的社交季。",
    "The Alps": "阿尔卑斯", "Formula 1": "F1大奖赛", "The Riviera": "蔚蓝海岸", "Paris": "巴黎",
    # Textes déjà en ligne dont l'anglais a changé
    "Car at the aircraft, hotel, dinner, the days that follow. Your crew flies, we take the ground.": "机旁专车、酒店、当晚的晚餐与之后几天的行程。您的机组负责飞行，地面的一切交给我们。",
    "Private gym hours, treatments to recover after a long season, meals that follow the nutrition plan, arrivals away from the lobby. For the athlete, the family and the entourage.":
        "私人健身时段、漫长赛季后的恢复护理、按营养方案准备的餐食、避开大堂的低调入住。服务运动员本人，也照顾家人与随行人员。",
    "For planners bringing a celebration to Paris or the Riviera: guest stays, transfers, dinners, and the brunch the day after.":
        "在巴黎或蔚蓝海岸筹办婚礼？宾客的住宿、接送、晚宴，直到第二天的早午餐，都交给我们。",
    "Terms and references are shared by email, on request.": "合作条款与参考案例，可应要求通过邮件提供。",
}


def ajouter_chinois(page):
    """Donne un data-zh à chaque élément bilingue qui n'en a pas (ou dont l'anglais a changé)."""
    manquants = []
    # anglais réécrit par la 12c : l'ancien chinois ne correspond plus, on le remplace
    anglais_change = {nouvel for _, (_, nouvel) in v.FR_REECRIT.items() if nouvel}

    def remplace(m):
        en = html.unescape(m.group(1))
        if en in ZH and (m.group(3) is None or en in anglais_change):
            return f'data-en="{m.group(1)}" data-fr="{m.group(2)}" data-zh="{html.escape(ZH[en])}"'
        if m.group(3) is None:
            manquants.append(en)
        return m.group(0)

    page = re.sub(r'data-en="([^"]*)" data-fr="([^"]*)"( data-zh="[^"]*")?', remplace, page)
    assert not manquants, f"textes sans chinois : {manquants}"
    return page


def main():
    page = PAGE.read_text(encoding="utf-8")
    assert 'class="who"' not in page, "la page a déjà reçu la 12c"
    page = v.reecrire_francais(page)
    css = v.CSS.replace(".bandeau-maquette{background:#000;color:#fff;font-size:13px;text-align:center;padding:8px 12px;position:relative;z-index:80}\n", "")
    page = page.replace("</style>", css + "</style>", 1)

    sections = page.split("<section")
    s01, s02, s03, s04, s05 = ("<section" + s for s in sections[1:6])
    debut = sections[0]
    s05, fin = s05.split("</section>", 1)[0] + "</section>", s05.split("</section>", 1)[1]

    s02 = s02.replace("</ol>", "</ol>" + v.bloc_engagements(), 1)
    morceaux = re.split(r'(<div class="pub(?: on)?">)', s03)
    for k, i in enumerate(range(2, len(morceaux), 2)):
        corps = morceaux[i]
        dernier = corps.rfind("</div></div>")
        morceaux[i] = corps[:dernier] + "</div></div>" + v.plus_onglet(v.ONGLETS[k]) + "</div>" + corps[dernier + 12:]
    s03 = "".join(morceaux)
    s03, n_ex = re.subn(r'<div class="ex">.*?</div>', "", s03, flags=re.S)
    assert n_ex == 6, n_ex
    s03 = re.sub(r'<div class="pub( on)?">', lambda m: f'<div class="pub{m.group(1) or ""}"><div class="haut">', s03)
    s03 = ('<style>.pub.on{display:block}.pub>.haut{display:grid;grid-template-columns:1fr 1.1fr;gap:56px;align-items:center}'
           '@media(max-width:900px){.pub>.haut{grid-template-columns:1fr;gap:22px}}</style>') + s03

    qui = v.bloc_qui("01").replace(
        f'<img src="{v.DECK}v6_entree_palace.jpg" alt="">',
        '<picture><source type="image/avif" srcset="img/pro-qui.avif"><img src="img/pro-qui.webp" '
        'alt="The entrance of a Paris palace hotel" data-alt-en="The entrance of a Paris palace hotel" '
        'data-alt-fr="L\'entrée d\'un palace parisien" data-alt-zh="巴黎一家殿堂级酒店的入口" loading="lazy"></picture>')
    assert "pro-qui" in qui
    # liens des saisons : chemins du site
    saisons = v.bloc_saisons("06").replace('href="../../site-unseen/', 'href="')

    page = debut + "".join([qui, s01, v.bloc_services("03"), s02, s03, saisons, s04, s05]) + fin
    compteur = iter(range(1, 20))
    page = re.sub(r'(<div class="eyebrow"><span class="n">)\d\d(</span>)', lambda m: f"{m.group(1)}{next(compteur):02d}{m.group(2)}", page)
    page = ajouter_chinois(page)
    PAGE.write_text(page, encoding="utf-8")
    print("professionals.html mise à jour (12c + chinois)")


if __name__ == "__main__":
    main()
