"""
Dessine la carte de l'Europe de l'accueil directement dans index.html.

Avant : la page téléchargeait un outil de dessin (d3) et un fond de carte au moment
de la visite, environ 400 Ko, ce qui ralentissait le site sur téléphone.
Maintenant : le dessin est calculé ici, une fois, avec exactement la même projection
(Natural Earth, même cadrage) ; la page n'a plus rien à télécharger pour la carte.

Le fond de carte est rangé dans outils/donnees/countries-110m.json (world-atlas 2.0.2).

Lancer, depuis le dossier du projet :
    python3 site-unseen/outils/carte_europe.py
"""
import html as H
import json
import math
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
TOPO = json.loads((Path(__file__).parent / "donnees" / "countries-110m.json").read_text())

W, HT = 560, 420
CADRE = [[-10, 58], [28, 58], [-10, 35], [28, 35]]       # même cadrage qu'avant
EU = {"France", "Germany", "Italy", "Spain", "United Kingdom", "Switzerland", "Belgium", "Netherlands", "Austria",
      "Portugal", "Ireland", "Denmark", "Sweden", "Norway", "Poland", "Czechia", "Greece", "Croatia", "Luxembourg",
      "Slovenia", "Hungary", "Slovakia", "Finland"}
PARIS = (2.35, 48.86)
LIEUX = [  # clé, coordonnées, position du nom (x, y) par rapport au point, (en, fr, zh)
    ("paris", PARIS, (10, -8), ("Paris", "Paris", "巴黎")),
    ("london", (-0.1, 51.5), (-58, -6), ("London", "Londres", "伦敦")),
    ("alps", (6.6, 45.4), (-14, 26), ("The Alps", "Les Alpes", "阿尔卑斯")),
    ("milan", (9.19, 45.46), (10, 0), ("Milan", "Milan", "米兰")),
    ("riviera", (5.6, 43.25), (10, 16), ("The Riviera", "La Riviera", "蔚蓝海岸")),
    ("ibiza", (1.43, 38.9), (10, 4), ("Ibiza", "Ibiza", "伊维萨")),
    ("mykonos", (25.3, 37.4), (-78, -10), ("Mykonos", "Mykonos", "米科诺斯")),
    ("marbella", (-4.88, 36.51), (-70, 16), ("Marbella", "Marbella", "马贝拉")),
]


def brut(lon, lat):
    """Projection Natural Earth (formule de d3.geoNaturalEarth1), en radians."""
    l, p = math.radians(lon), math.radians(lat)
    p2 = p * p
    p4 = p2 * p2
    return (l * (0.8707 - 0.131979 * p2 + p4 * (-0.013791 + p4 * (0.003971 * p2 - 0.001529 * p4))),
            p * (1.007226 + p2 * (0.015085 + p4 * (-0.044475 + 0.028874 * p2 - 0.005916 * p4))))


# Cadrage identique à d3 fitExtent([[8,8],[W-8,H-8]], cadre)
pts = [brut(*c) for c in CADRE]
xs = [150 * x for x, _ in pts]; ys = [-150 * y for _, y in pts]
w, h = W - 16, HT - 16
k = min(w / (max(xs) - min(xs)), h / (max(ys) - min(ys)))
TX = 8 + (w - k * (max(xs) + min(xs))) / 2
TY = 8 + (h - k * (max(ys) + min(ys))) / 2
ECH = 150 * k


def proj(lon, lat):
    x, y = brut(lon, lat)
    return TX + ECH * x, TY - ECH * y


# --- lecture du fichier topojson (arcs codés en différences)
sx, sy = TOPO["transform"]["scale"]; tx, ty = TOPO["transform"]["translate"]
ARCS = []
for arc in TOPO["arcs"]:
    x = y = 0; pts_arc = []
    for dx, dy in arc:
        x += dx; y += dy
        pts_arc.append((x * sx + tx, y * sy + ty))
    ARCS.append(pts_arc)


def anneau(indices):
    pts_a = []
    for i in indices:
        a = ARCS[i] if i >= 0 else ARCS[~i][::-1]
        pts_a.extend(a if not pts_a else a[1:])
    # la Russie traverse l'antiméridien : on garde son extrémité est d'un seul tenant
    return [(lon + 360 if lon < -170 else lon, lat) for lon, lat in pts_a]


def chemin(geo):
    polys = [geo["arcs"]] if geo["type"] == "Polygon" else geo["arcs"]
    d, visible = [], False
    for poly in polys:
        for r in poly:
            p = [proj(*c) for c in anneau(r)]
            if any(-40 < x < W + 40 and -40 < y < HT + 40 for x, y in p):
                visible = True
            d.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in p) + "Z")
    return "".join(d), visible


pays = []
for geo in TOPO["objects"]["countries"]["geometries"]:
    nom = geo.get("properties", {}).get("name", "")
    if nom == "Antarctica" or geo["type"] not in ("Polygon", "MultiPolygon"):
        continue
    d, visible = chemin(geo)
    if visible:
        pays.append(f'<path class="land{" eu" if nom in EU else ""}" d="{d}"/>')

px, py = proj(*PARIS)
arcs, points = [], []
for cle, c, (lx, ly), noms in LIEUX:
    ax, ay = proj(*c)
    if cle != "paris":
        mx, my = (ax + px) / 2, (ay + py) / 2 - math.hypot(ax - px, ay - py) * .22
        arcs.append(f'<path class="arc out" data-k="{cle}" d="M{ax:.1f},{ay:.1f} Q{mx:.1f},{my:.1f} {px:.1f},{py:.1f}"/>')
    base = " base" if cle == "paris" else ""
    r = 6 if cle == "paris" else 4
    en, fr, zh = noms
    points.append(f'<g class="pt{base}" data-k="{cle}" transform="translate({ax:.1f},{ay:.1f})">'
                  f'<circle r="{r}" fill="#E9C4B8"/><circle r="16" fill="transparent"/>'
                  f'<text class="nm" x="{lx}" y="{ly}" style="font-size:13px" data-en="{en}" data-fr="{fr}" data-zh="{zh}">{en}</text></g>')

svg = ('<svg id="europe" viewBox="0 0 560 420" role="img" aria-label="Map of Europe with UNSEEN. destinations">'
       f'<g>{"".join(pays)}</g><g>{"".join(arcs)}</g><g>{"".join(points)}</g></svg>')

# --- mise à jour de index.html
f = SITE / "index.html"
h = f.read_text(encoding="utf-8", errors="surrogateescape")
h = re.sub(r'<svg id="europe".*?</svg>', lambda m: svg, h, count=1, flags=re.S)
h = h.replace('<script src="https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"></script>\n', "")
h = h.replace('<script src="https://cdn.jsdelivr.net/npm/topojson-client@3.1.0/dist/topojson-client.min.js"></script>\n', "")
# le script de la carte : plus de d3, seulement le texte de la fiche et la mise en valeur du trajet
i = h.index("// Carte du monde : d'où viennent les clients, où on les emmène")
j = h.index("})();\n</script>\n</body>", i) + len("})();\n")
ancien = h[i:j]
m = re.search(r"const P=\{.*?\}\};", ancien, re.S)
P = re.sub(r"c:(?:paris|\[[^\]]*\]),", "", m.group(0))
nouveau = f"""// Carte de l'Europe (dessinée dans la page par outils/carte_europe.py) : la fiche suit le point choisi
(()=>{{
 {P}
 const info=document.getElementById('nvinfo');
 const L=()=>({{en:0,fr:1,zh:2}}[document.documentElement.lang]||0);
 const show=k=>{{const v=P[k],l=L();info.innerHTML=`<span class="t">${{v.t[l]}}</span><h3>${{v.n[l]}}</h3><p>${{v.d[l]}}</p>`;info.dataset.k=k;
   document.querySelectorAll('#europe .arc').forEach(a=>a.classList.toggle('hi',a.dataset.k===k))}};
 document.querySelectorAll('#europe .pt').forEach(g=>{{const k=g.dataset.k;g.addEventListener('mouseenter',()=>show(k));g.addEventListener('click',()=>show(k))}});
 show('paris');
 new MutationObserver(()=>show(info.dataset.k||'paris')).observe(document.documentElement,{{attributes:true,attributeFilter:['lang']}});
}})();
"""
h = h[:i] + nouveau + h[j:]
f.write_text(h, encoding="utf-8", errors="surrogateescape")
print(f"Carte écrite : {len(pays)} pays, {len(svg) / 1000:.0f} Ko dans la page")
