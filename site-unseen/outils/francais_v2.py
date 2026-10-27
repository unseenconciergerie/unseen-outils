"""
Français réécrit du site (27/10/2026) : les textes qui sentaient la traduction de l'anglais
sont réécrits comme un rédacteur français l'aurait fait (règle de Jay du 27/10).

Pages concernées : accueil, Paris, Riviera, Océan Indien, Alpes, Formule 1, 404.
(La page Professionnels est déjà faite ; les mentions légales seront revues à part.)

Deux usages, depuis le dossier du projet :
    python3 site-unseen/outils/francais_v2.py comparer   → page « avant / après » pour Jay
    python3 site-unseen/outils/francais_v2.py appliquer  → modifie les pages (après accord de Jay)
"""
import html
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "professionals.html", "paris.html", "riviera.html", "ocean-indien.html", "saison-ski-2026-2027.html",
         "formule-1.html", "404.html"]
NOMS = {"index.html": "Accueil", "professionals.html": "Professionnels", "paris.html": "Paris", "riviera.html": "Riviera", "ocean-indien.html": "Océan Indien",
        "saison-ski-2026-2027.html": "Alpes, saison de ski", "formule-1.html": "Formule 1", "404.html": "Page d'erreur"}
COMPARAISON = SITE.parent / "Livrables" / "Maquettes site (évolution)" / "13 Français réécrit, avant-après (27-10).html"

# clé = texte anglais exact de la page ; valeur = nouveau français
REECRIT = {
    'A suite that was never listed. A table that closed three weeks ago. A seat on the night everyone wanted one. You tell us when, we handle the rest, and you never see how.':
        "Une suite jamais proposée à la réservation. Une table complète depuis trois semaines. La place que tout le monde s'arrache. Dites-nous quand, nous nous occupons du reste.",
    'You always know where your request stands. If something cannot be done, we say so straight away and come back with an alternative, never at the last minute.':
        "Vous savez à tout moment où en est votre demande. Si quelque chose n'est pas possible, nous vous le disons tout de suite et nous vous proposons une autre solution, jamais à la dernière minute.",
    'A message. Dates, city, and roughly what you have in mind. Nothing else is needed to start, and there is no form to fill in.':
        "Un simple message : les dates, la ville, et une idée de ce que vous souhaitez. Il n'en faut pas plus pour commencer, et aucun formulaire à remplir.",
    'What is available, what it costs, and how long the option holds. In writing. We do not promise anything we cannot deliver.':
        "Ce qui est disponible, le prix, et jusqu'à quand l'option est garantie. Le tout par écrit. Nous ne promettons jamais ce que nous ne pouvons pas tenir.",
    'One contact from start to finish, reachable at any hour and in any time zone. If a table falls through at seven, another one is standing at eight.':
        'Un seul interlocuteur du début à la fin, joignable à toute heure, où que vous soyez. Si une réservation saute à 19 h, une autre table vous attend à 20 h.',
    'Afterwards':
        'Après',
    'Nothing leaves. Your name, your dates and your itinerary are never disclosed or confirmed to anyone, including to other clients and to the press. During, and long after.':
        'Rien ne filtre. Votre nom, vos dates et votre programme ne sont jamais révélés ni confirmés à qui que ce soit, ni aux autres clients, ni à la presse. Pendant votre séjour, et bien après.',
    'One number. Everything behind it.':
        'Un seul numéro, et tout le reste suit.',
    'No switchboard, no ticket, no account manager discovering your file as you speak. One person already knows it, and answers.':
        "Pas de standard, pas de ticket, personne qui découvre votre dossier en vous écoutant. Une seule personne le connaît déjà, et c'est elle qui vous répond.",
    'Rooms and categories that never reach a booking engine. Upgrades arranged before arrival, late check-out held, and amenities set to your preferences rather than a standard list.':
        'Des chambres et des catégories introuvables sur les sites de réservation. Surclassement réglé avant votre arrivée, late check-out garanti, et des attentions selon vos goûts, pas selon une liste type.',
    "Tables at short notice in rooms that show nothing available. Private dining rooms, chef's counters, and menus adjusted to an allergy, a fast, or a schedule that will not wait.":
        "Des tables obtenues au dernier moment dans des restaurants complets. Salons privés, chef's tables, et des menus adaptés à une allergie, un jeûne ou un emploi du temps serré.",
    'Formula 1 weekends, Fashion Weeks, Art Basel, Roland-Garros, sold-out shows. The paddock, the courtside, the front row, and the rooms that open afterwards.':
        'Les week-ends de Formule 1, les Fashion Weeks, Art Basel, Roland-Garros, les spectacles à guichets fermés. Le paddock, le bord de court, le premier rang, et les soirées privées qui suivent.',
    'Shopping and sourcing':
        'Shopping et sourcing',
    'Appointments outside opening hours with the major houses, waiting lists, styling, and sourcing pieces that are no longer made.':
        "Des rendez-vous en dehors des heures d'ouverture dans les grandes maisons, l'accès aux listes d'attente, du styling, et la recherche de pièces qui ne se fabriquent plus.",
    'Chauffeurs who know the city and never talk about it, airport and terminal transfers, long-distance journeys, and a helicopter leg where the road would cost three hours.':
        "Des chauffeurs qui connaissent la ville et savent rester discrets, des transferts depuis l'aéroport ou depuis la gare, de longs trajets, et un hélicoptère quand la route prendrait trois heures.",
    'Villas and charters':
        'Villas et yachts',
    'Staffed villas by the week, yachts by the day or by the season, with crew, tender and chef. Provisioning, berths and shore transfers form one plan rather than four separate bookings.':
        'Des villas avec personnel à la semaine, des yachts à la journée ou pour la saison, avec équipage, annexe et chef. Avitaillement, places au port et transferts à terre : tout est organisé ensemble.',
    'Evenings and closed rooms':
        'Soirées et lieux privés',
    'Private clubs, booths that are never sold, opera boxes, and evenings built around a guest list rather than a venue. Entry is arranged before you arrive, never negotiated at the door.':
        'Clubs privés, tables jamais mises en vente, et des soirées pensées autour des invités plutôt que du lieu. Votre entrée est réglée avant votre arrivée, jamais négociée à la porte.',
    'Mauritius, Réunion, the Maldives. Open when Europe closes.':
        "Maurice, La Réunion, les Maldives. Le soleil quand l'Europe hiberne.",
    'A few ideas of what we arrange, from Paris to wherever the season is. Choose a point.':
        "Quelques idées de ce que nous organisons, de Paris jusqu'aux destinations de saison. Choisissez un point sur la carte.",
    'The good chalets for Christmas and February are being taken now. Tell us your weeks.':
        'Les plus beaux chalets pour Noël se réservent dès maintenant. Dites-nous vos semaines.',
    'Terraces and boats for the race weekend sell out a season ahead.':
        "Les terrasses et les bateaux pour le week-end de la course se réservent une saison à l'avance.",
    'WhatsApp is the fastest way to reach us, at any hour and in any time zone. A first message takes one line.':
        'WhatsApp est le moyen le plus rapide de nous joindre, à toute heure, où que vous soyez. Une ligne suffit pour commencer.',
    'Start a conversation':
        'Écrire sur WhatsApp',
    'Every request is handled personally. Leave a few details and we come back to you within 24 hours with what is possible, what it involves and what it costs.':
        'Chaque demande est traitée personnellement. Laissez-nous quelques informations : sous 24 heures, nous vous disons ce qui est possible, comment, et à quel prix.',
    'Your request is on its way. We come back to you within 24 hours.':
        'Votre demande nous est bien parvenue. Nous revenons vers vous sous 24 heures.',
    'The city where the address book was built, and where a name still opens a door faster than a payment does.':
        "La ville où notre carnet d'adresses s'est construit, et où un nom ouvre encore les portes plus vite qu'une carte bancaire.",
    'Everyone comes. Few get in.':
        'Tout le monde y vient. Peu y entrent vraiment.',
    'The best suites never reach a booking site, the right tables show nothing available, the houses of the Faubourg keep their appointments for the people they know. We work from the inside, all year.':
        "Les plus belles suites ne sont jamais proposées en ligne, les bonnes tables affichent complet, et les maisons du Faubourg-Saint-Honoré réservent leurs rendez-vous à ceux qu'elles connaissent. Nous y travaillons de l'intérieur, toute l'année.",
    'A table facing the Tower at night, a terrace, a quiet street at breakfast.':
        'Un dîner face à la tour Eiffel illuminée, une terrasse, une rue tranquille au petit-déjeuner.',
    'One contact. Everything the week needs.':
        'Un seul interlocuteur pour toute votre semaine.',
    'A palace suite that was never listed, upgrade arranged before you land.':
        'Une suite de palace introuvable en ligne, avec le surclassement réglé avant votre arrivée.',
    'A late check-out, held for you.':
        'Un late check-out, garanti.',
    'Where you eat':
        'Où dîner',
    'A table at the restaurant that is fully booked.':
        'Une table dans un restaurant qui affiche complet.',
    'Personal shopping and private appointments on the Faubourg.':
        'Du personal shopping et des rendez-vous privés rue du Faubourg-Saint-Honoré.',
    'How you move':
        'Se déplacer',
    'Tell us the dates.':
        'Donnez-nous vos dates.',
    'Use the contact form':
        'Remplir le formulaire',
    'Monaco, Saint-Tropez, Cannes. Villas taken before winter ends, beach clubs where a table already carries a name, days that begin at the berth.':
        "Monaco, Saint-Tropez, Cannes. Des villas réservées avant la fin de l'hiver, des beach clubs où votre table vous attend déjà, et des journées qui commencent sur le ponton.",
    'The villas, the boats and the Grand Prix terraces are taken months ahead. We start in January, so your name is already on the list when you decide.':
        "Les villas, les bateaux et les terrasses du Grand Prix se réservent des mois à l'avance. Nous nous y mettons dès janvier, pour que votre nom figure déjà sur la liste le jour où vous vous décidez.",
    'The whole summer, one contact.':
        "Tout l'été, un seul interlocuteur.",
    'A tender from the boat to the beach.':
        "L'annexe pour rejoindre la plage depuis le bateau.",
    'The Indian Ocean, when Europe closes.':
        "L'océan Indien, quand l'Europe se met en sommeil.",
    'Mauritius, Réunion, the Maldives. Lagoons, resorts, staffed villas, helicopter legs and days at sea with a crew.':
        'Maurice, La Réunion, les Maldives. Des lagons, des resorts, des villas avec personnel, des trajets en hélicoptère et des journées en mer avec équipage.',
    'Warm all year, easy from Paris.':
        "Le soleil toute l'année, à un vol direct de Paris.",
    'Mauritius is our base in the Indian Ocean: a direct flight from Paris, French spoken everywhere, and a season of its own, at its best from May to June and September to December. Réunion and the Maldives are close by. Many of our clients stop in Paris first, then fly south.':
        "Maurice est notre base dans l'océan Indien : un vol direct depuis Paris, le français parlé partout, et des saisons bien à elle, les plus belles de mai à juin et de septembre à décembre. La Réunion et les Maldives sont à deux pas. Beaucoup de nos clients s'arrêtent d'abord à Paris avant de s'envoler vers le sud.",
    'At the foot of the mountain, on the sunset side of the island.':
        'Au pied du Morne, sur la côte où le soleil se couche.',
    'The newest address on the island, a rooftop, the life of the bay close by.':
        "La plus récente adresse de l'île, avec son rooftop et l'animation de la baie à deux pas.",
    'A few nights in Paris on the way, as one trip.':
        'Quelques nuits à Paris en chemin, le tout organisé comme un seul voyage.',
    'The season, arranged before it starts.':
        "La saison, préparée avant même qu'elle ne commence.",
    "Courchevel in late December. Gstaad the week after. A late addition to Val d'Isère, three days before the children arrive. We hold the season a step ahead, so nothing is left to chance once you're there.":
        "Courchevel fin décembre, Gstaad la semaine suivante, puis Val d'Isère ajouté au dernier moment, trois jours avant l'arrivée des enfants. Nous gardons une longueur d'avance sur la saison, pour que rien ne soit laissé au hasard une fois sur place.",
    'Booked months before the first snowfall.':
        'Tout se réserve des mois avant les premières neiges.',
    'The best chalets, the best tables at altitude, the best transfers: all of it is taken months in advance. We work the season from October, so your name is already on the list when you decide to come.':
        "Les plus beaux chalets, les meilleures tables d'altitude, les transferts les plus pratiques : tout se réserve des mois à l'avance. Nous préparons la saison dès octobre, pour que votre nom figure déjà sur la liste le jour où vous décidez de venir.",
    'The reference. 1850 for the address, the altitude restaurants, the boutiques that stay open past dinner.':
        "La référence. Courchevel 1850 pour le prestige, les restaurants d'altitude, et des boutiques ouvertes bien après le dîner.",
    'A village built around its reputation, not around visitors. Quieter, closer to Geneva, no less exacting.':
        'Un vrai village, qui a bâti sa réputation sans courir après les visiteurs. Plus discret, plus proche de Genève, tout aussi exigeant.',
    'High altitude, early snow, a nightlife that runs until the lifts open again.':
        "La haute altitude, une neige qui arrive tôt, et des nuits qui se prolongent jusqu'à l'ouverture des remontées.",
    "Europe's highest resort. For skiing that starts at the door and doesn't stop at lunch.":
        "La plus haute station d'Europe, pour chausser les skis devant sa porte et skier jusqu'au soir.",
    'The centre of the Three Valleys, English-speaking by habit, chalets built for entertaining.':
        'Le cœur des Trois Vallées, une clientèle très internationale, et des chalets faits pour recevoir.',
    "Switzerland's quiet version of exclusive. Fewer people, longer dinners.":
        "Le luxe à la suisse, tout en discrétion. Moins de monde, et des dîners qui s'éternisent.",
    'Each resort, its own way.':
        'À chaque station, son art de vivre.',
    'A chalet with staff at 1850, booked before the good ones are gone.':
        'Un chalet avec personnel à 1850, réservé avant que les plus beaux ne soient pris.',
    'A horse-drawn sleigh through the village.':
        'Une promenade en traîneau à cheval dans le village.',
    'The afternoon party at La Folie Douce.':
        "L'après-ski en musique à La Folie Douce.",
    'A chalet built for entertaining.':
        'Un chalet fait pour recevoir.',
    'The race, watched from where it matters.':
        'La course, vue depuis les meilleures places.',
    "Monaco in May. The paddock on race morning. A table that's still open on Saturday night, in a town where every table is booked by February. We hold the weekend months before the grid is set.":
        'Monaco en mai. Le paddock le matin de la course. Une table encore disponible le samedi soir, dans une ville où tout est réservé dès février. Nous bloquons votre week-end des mois avant que la grille de départ ne soit connue.',
    'Booked before the season is announced.':
        "Tout se réserve avant même l'annonce du calendrier.",
    'Hospitality packages and paddock access sell out months ahead, often before the calendar itself is confirmed. We hold what matters for the weekend you want, starting with Monaco.':
        "Les packages hospitalité et les accès paddock s'arrachent des mois à l'avance, parfois avant même la confirmation du calendrier. Nous réservons l'essentiel pour le week-end de votre choix, à commencer par Monaco.",
    'The one everyone asks for. A harbour of yachts, a circuit through the streets, and a town that empties of everything but racing for four days.':
        'Celle que tout le monde demande. Un port rempli de yachts, un circuit tracé dans les rues, et une ville entièrement tournée vers la course pendant quatre jours.',
    'Formula 1 after dark. The Strip as a straight, and a paddock that runs past midnight.':
        "La Formule 1 de nuit. Le Strip de Las Vegas transformé en ligne droite, et un paddock qui s'anime encore après minuit.",
    'Spring heat, a purpose-built track, and a hospitality scene that rivals the racing.':
        "La chaleur du printemps, un circuit tracé pour l'événement, et une offre hospitalité qui rivalise avec la course elle-même.",
    'One contact. Everything the weekend needs.':
        'Un seul interlocuteur pour tout votre week-end.',
    'Hospitality or paddock access, held before the good tiers are gone.':
        'Un accès hospitalité ou paddock, réservé avant que les meilleures places ne partent.',
    'Private transport to the circuit, door to grid.':
        "Un transport privé jusqu'au circuit, de votre porte à la grille de départ.",
    'A terrace, a yacht, or a table for the nights around the race.':
        'Une terrasse, un yacht, ou une table pour les soirées du week-end.',
    'Whatever the weekend needs, through one contact.':
        'Tout le reste, avec un seul interlocuteur.',
    'Tell us which race.':
        'Dites-nous quelle course vous intéresse.',
    'The address you followed does not lead anywhere. It may have moved, or never existed at all.':
        "Ce lien ne mène nulle part. La page a peut-être été déplacée, ou n'a jamais existé.",
    'Around the Tower':
        'Autour de la tour Eiffel',
    'Palaces, starred tables, Fashion Week, the houses of the Faubourg.':
        'Palaces, tables étoilées, Fashion Week, les maisons du Faubourg-Saint-Honoré.',
}

# Textes dont l'anglais et le chinois changent aussi (pour rester d'accord avec le français, 27/10)
AUSSI = {
    "Private clubs, booths that are never sold, opera boxes, and evenings built around a guest list rather than a venue. Entry is arranged before you arrive, never negotiated at the door.":
        ("Private clubs, booths that are never sold, and evenings built around a guest list rather than a venue. Entry is arranged before you arrive, never negotiated at the door.",
         "私人会所、从不对外出售的卡座，以及以宾客名单而非场地为核心安排的夜晚。入场事先安排妥当，从不在门口交涉。"),
    "The good chalets for Christmas and February are being taken now. Tell us your weeks.":
        ("The good chalets for Christmas are being taken now. Tell us your weeks.", "圣诞季的好木屋，此刻正被陆续订走。告诉我们您的日期。"),
    "Around the Tower": ("Around the Eiffel Tower", "埃菲尔铁塔周边"),
    "A table facing the Tower at night, a terrace, a quiet street at breakfast.":
        ("A table facing the Eiffel Tower at night, a terrace, a quiet street at breakfast.", "夜里正对埃菲尔铁塔的餐桌、一处露台，以及早餐时分安静的街道。"),
}

MOTIF = re.compile(r'data-en="([^"]*)" data-fr="([^"]*)"')


def comparer():
    """Écrit la page « avant / après » : pour chaque page du site, les phrases changées."""
    blocs, total, vus = [], 0, set()
    for nom in PAGES:
        lignes = []
        for en, fr in MOTIF.findall((SITE / nom).read_text(encoding="utf-8")):
            en, fr = html.unescape(en), html.unescape(fr)
            if en in REECRIT and en not in vus:
                vus.add(en)
                lignes.append(f"<tr><td>{html.escape(fr)}</td><td>{html.escape(REECRIT[en])}</td></tr>")
        if lignes:
            total += len(lignes)
            blocs.append(f"<h2>{NOMS[nom]} <small>{len(lignes)} phrases</small></h2><table><tr><th>Avant</th><th>Après</th></tr>{''.join(lignes)}</table>")
    oublies = set(REECRIT) - vus
    assert not oublies, f"textes introuvables : {oublies}"
    COMPARAISON.write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Français réécrit, avant-après</title>
<style>body{{font-family:-apple-system,system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:24px 16px;color:#1c1b1e;background:#fff}}
h1{{font-size:26px}}h2{{margin-top:40px;font-size:20px}}h2 small{{font-weight:400;color:#8a8083;font-size:14px}}
table{{width:100%;border-collapse:collapse;margin-top:10px}}th{{text-align:left;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#8a8083;padding:6px 10px}}
td{{vertical-align:top;padding:12px 10px;border-top:1px solid #eee;font-size:15.5px;line-height:1.55;width:50%}}
td:first-child{{color:#8a8083}}td:last-child{{background:#f4eae5}}
@media(max-width:700px){{tr{{display:block;border-top:1px solid #ddd;padding:6px 0}}th{{display:none}}td{{display:block;width:auto;border:0}}td:first-child:before{{content:"Avant : ";font-weight:600}}td:last-child:before{{content:"Après : ";font-weight:600}}}}</style></head>
<body><h1>Français réécrit du site, avant / après</h1><p>{total} phrases réécrites sur 7 pages, le 27/10/2026. Seul le français change : l'anglais et le chinois restent tels quels. Rien n'est en ligne tant que Jay n'a pas validé.</p>
{''.join(blocs)}</body></html>""", encoding="utf-8")
    print(f"{total} phrases, page écrite : {COMPARAISON}")


def appliquer():
    for nom in PAGES:
        chemin = SITE / nom
        page, n = chemin.read_text(encoding="utf-8"), 0

        def remplace(m):
            nonlocal n
            en = html.unescape(m.group(1))
            if en not in REECRIT:
                return m.group(0)
            n += 1
            if en in AUSSI:
                nouvel_en, nouveau_zh = AUSSI[en]
                return (f'data-en="{html.escape(nouvel_en)}" data-fr="{html.escape(REECRIT[en])}" '
                        f'data-zh="{html.escape(nouveau_zh)}" data-zh-ancien="')
            return f'data-en="{m.group(1)}" data-fr="{html.escape(REECRIT[en])}"'

        page = MOTIF.sub(remplace, page)
        # l'ancien data-zh suit : on le retire (il a été renommé data-zh-ancien juste au-dessus)
        page = re.sub(r' data-zh-ancien=" data-zh="[^"]*"', "", page)
        # le texte affiché par défaut (anglais) des éléments modifiés
        for vieux, (neuf, _) in AUSSI.items():
            page = page.replace(">" + html.escape(vieux, quote=False) + "<", ">" + html.escape(neuf, quote=False) + "<")
            page = page.replace(">" + vieux + "<", ">" + neuf + "<")
        chemin.write_text(page, encoding="utf-8")
        print(f"{nom} : {n} textes réécrits")


if __name__ == "__main__":
    {"comparer": comparer, "appliquer": appliquer}[sys.argv[1]]()
