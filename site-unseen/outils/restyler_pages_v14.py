"""
Passe les pages existantes (ski, Formule 1, mentions légales, page d'erreur) à la charte V1.4 :
DM Sans au lieu de Montserrat/Raleway, sable rosé au lieu du bleu très clair, anthracite pour
les blocs sombres, menu du nouveau site, et menu « trois traits » sur téléphone.
À lancer une fois : python3 site-unseen/outils/restyler_pages_v14.py
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
POLICE_DM = "family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700"

MENU = [("index.html#services", "Services", "Services", "服务"), ("index.html#destinations", "Destinations", "Destinations", "目的地"),
        ("index.html#now", "Seasons", "Saisons", "当季"), ("professionals.html", "Professionals", "Professionnels", "合作伙伴"),
        ("index.html#contact", "Contact", "Contact", "联系我们")]
liens = "\n      ".join(f'<a href="{h}" data-en="{en}" data-fr="{fr}" data-zh="{zh}">{en}</a>' for h, en, fr, zh in MENU)

MOBILE_CSS = """
/* Menu sur téléphone (charte V1.4) */
.burger{display:none;width:44px;height:44px;border:0;background:none;cursor:pointer;position:relative;margin-left:6px}
.burger span{position:absolute;left:11px;right:11px;height:1.5px;background:#000;transition:transform .25s,opacity .25s}
.burger span:nth-child(1){top:16px}.burger span:nth-child(2){top:22px}.burger span:nth-child(3){top:28px}
.menu-open .burger span:nth-child(1){transform:translateY(6px) rotate(45deg)}
.menu-open .burger span:nth-child(2){opacity:0}
.menu-open .burger span:nth-child(3){transform:translateY(-6px) rotate(-45deg)}
.mpanel{position:fixed;left:0;right:0;bottom:0;top:64px;background:#fff;z-index:59;padding:26px 22px calc(26px + env(safe-area-inset-bottom));display:flex;flex-direction:column;opacity:0;pointer-events:none;transform:translateY(-8px);transition:opacity .25s,transform .25s}
.menu-open .mpanel{opacity:1;pointer-events:auto;transform:none}
.mpanel a{font-family:'League Spartan',sans-serif;font-weight:800;font-size:30px;text-decoration:none;color:#000;padding:12px 0;border-bottom:1px solid #E5D7D0}
.mpanel .bas{margin-top:auto;display:flex;flex-direction:column;gap:10px}
.mpanel .bas a{font-family:'DM Sans',sans-serif;font-weight:500;font-size:16px;border:0;padding:0}
@media(max-width:900px){.burger{display:block}}
"""
MOBILE_HTML = f"""<nav class="mpanel" id="mpanel" aria-hidden="true">
  {liens}
  <div class="bas"><a href="https://wa.me/33613850733">WhatsApp</a><a href="mailto:contact@unseenconciergerie.com">contact@unseenconciergerie.com</a></div>
</nav>
"""
MOBILE_JS = """<script>
(function(){var b=document.getElementById('burger'),p=document.getElementById('mpanel');if(!b)return;
b.addEventListener('click',function(){var o=document.body.classList.toggle('menu-open');b.setAttribute('aria-expanded',o);p.setAttribute('aria-hidden',!o);});
p.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){document.body.classList.remove('menu-open');});});})();
</script>
</body>"""


def commun(h):
    h = re.sub(r"family=Montserrat:wght@[0-9;]+", POLICE_DM, h)
    h = re.sub(r"family=Raleway:wght@[0-9;]+&", "", h)
    h = h.replace("'Montserrat'", "'DM Sans'").replace("'Raleway'", "'DM Sans'")
    h = h.replace("--bleu-clair:#F4F6FC", "--bleu-clair:#F4EAE5").replace("--gris-doux:#D9D9D9", "--gris-doux:#E5D7D0")
    return h


for nom in ("saison-ski-2026-2027.html", "formule-1.html"):
    f = SITE / nom
    h = commun(f.read_text(encoding="utf-8"))
    h = h.replace(".topbar{position:sticky;top:0;z-index:60;background:var(--bleu-clair)", ".topbar{position:sticky;top:0;z-index:60;background:rgba(255,255,255,.96);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)")
    h = h.replace(".sec-dark{background:var(--noir);color:var(--blanc)}", ".sec-dark{background:#2B2A2E;color:var(--blanc)}")
    h = h.replace("footer{background:var(--noir);", "footer{background:#1E1D20;")
    h = re.sub(r'(<nav class="nav">)(.*?)(</nav>)', lambda m: m.group(1) + "\n      " + liens + "\n    " + m.group(3), h, count=1, flags=re.S)
    if 'id="burger"' not in h:
        i = h.index('<div class="langsw">'); j = h.index("</div>", i) + 6
        h = h[:j] + '\n    <button class="burger" id="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mpanel"><span></span><span></span><span></span></button>' + h[j:]
        i = h.index('<div class="topbar">'); j = h.index("</div>\n</div>", i) + len("</div>\n</div>")
        h = h[:j] + "\n" + MOBILE_HTML + h[j:]
        h = h.replace("</style>", MOBILE_CSS + "</style>", 1)
        h = h.replace("</body>", MOBILE_JS, 1)
    f.write_text(h, encoding="utf-8")
    print("ok", nom)

f = SITE / "legal.html"
h = commun(f.read_text(encoding="utf-8"))
h = h.replace("--accent:#1E4636", "--accent:#4F7C97")
h = h.replace(".topbar{position:sticky;top:0;background:var(--bleu-clair)", ".topbar{position:sticky;top:0;background:#FFFFFF")
h = h.replace("footer{background:var(--noir);", "footer{background:#1E1D20;")
f.write_text(h, encoding="utf-8"); print("ok legal.html")

f = SITE / "404.html"
h = commun(f.read_text(encoding="utf-8")).replace("--noir:#0B0B0B", "--noir:#2B2A2E")
f.write_text(h, encoding="utf-8"); print("ok 404.html")
