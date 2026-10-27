"""
Page d'erreur (404) dans la charte V1.4 (27/10/2026) : sable rosé, anthracite, accent de saison,
barre du haut comme le reste du site, trois langues, liens vers les pages principales.
Tous les chemins partent de la racine (« / ») : la page s'affiche bien quelle que soit l'adresse
tapée (ex. /xyz/abc), ce qui n'était pas le cas de l'ancienne (photo et style perdus).

    python3 site-unseen/outils/page_404_v14.py maquette  → Livrables/Maquettes site (évolution)/16 …
    python3 site-unseen/outils/page_404_v14.py site      → remplace site-unseen/404.html
"""
import html
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
MAQUETTE = SITE.parent / "Livrables" / "Maquettes site (évolution)" / "16 Page d'erreur 404, charte V1.4 (27-10).html"


def t(en, fr, zh, balise="span", attrs=""):
    return (f'<{balise}{attrs} data-en="{html.escape(en)}" data-fr="{html.escape(fr)}" data-zh="{html.escape(zh)}">'
            f'{html.escape(en, quote=False)}</{balise}>')


LIENS = [("paris.html", "Paris", "Paris", "巴黎", "The base", "Notre base", "大本营"),
         ("riviera.html", "The Riviera", "La Riviera", "蔚蓝海岸", "Summer", "L'été", "夏季"),
         ("saison-ski-2026-2027.html", "The Alps", "Les Alpes", "阿尔卑斯", "Winter", "L'hiver", "冬季"),
         ("ocean-indien.html", "Indian Ocean", "Océan Indien", "印度洋", "Counter-season", "Contre-saison", "反季之选"),
         ("formule-1.html", "Formula 1", "Formule 1", "一级方程式赛车", "Grand Prix", "Grand Prix", "大奖赛"),
         ("professionals.html", "Professionals", "Professionnels", "专业合作", "Partners", "Partenaires", "合作伙伴")]


def page(base):
    liens = "".join(
        f'<a href="{base}{href}"><span class="k">{t(ken, kfr, kzh)}</span>{t(en, fr, zh, "b")}<i aria-hidden="true">&rarr;</i></a>'
        for href, en, fr, zh, ken, kfr, kzh in LIENS)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UNSEEN. — Page not found</title>
<meta name="description" content="This page does not exist. Return to UNSEEN., private luxury concierge in Paris.">
<!-- Cette page ne doit pas apparaître dans Google -->
<meta name="robots" content="noindex, follow">
<link rel="icon" href="{base}favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{base}apple-touch-icon.png">
<link rel="stylesheet" href="{base}fonts.css">
<style>
/* Charte V1.4 : sable rosé, anthracite, une seule couleur d'accent (season.css) */
:root{{--sable:#F4EAE5;--anthra:#2B2A2E;--blanc:#FFF;--trait:#E5D7D0;--texte-2:#5C5556;--texte-3:#8A8083;
  --accent:#7AA3BC;--sur-accent:#000;--max:1240px;--pad:40px}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{-webkit-text-size-adjust:100%}}
body{{font-family:'DM Sans',system-ui,-apple-system,sans-serif;background:var(--sable);color:var(--anthra);min-height:100vh;min-height:100svh;display:flex;flex-direction:column;-webkit-font-smoothing:antialiased}}
a{{color:inherit}}
.top{{background:rgba(255,255,255,.96);border-bottom:1px solid rgba(0,0,0,.07)}}
.top-in{{max-width:var(--max);margin:0 auto;padding:16px var(--pad);display:flex;align-items:center;justify-content:space-between}}
.mark{{font-family:'League Spartan',sans-serif;font-weight:800;font-size:22px;text-decoration:none;letter-spacing:-.02em}}
.lang{{display:flex;gap:8px;align-items:center;font-size:12.5px;font-weight:600}}
.lang span{{color:var(--trait)}}
.lang button{{background:none;border:0;font:inherit;color:var(--texte-3);cursor:pointer;padding:8px 2px}}
.lang button[aria-pressed="true"]{{color:var(--anthra)}}
main{{flex:1;max-width:var(--max);margin:0 auto;padding:56px var(--pad) 48px;width:100%;display:grid;grid-template-columns:1.1fr 1fr;gap:72px;align-items:center}}
.grand{{font-family:'League Spartan',sans-serif;font-weight:800;font-size:clamp(120px,19vw,260px);line-height:.8;letter-spacing:-.04em;color:transparent;-webkit-text-stroke:2px var(--anthra)}}
.eyebrow{{display:flex;gap:14px;align-items:baseline;margin-top:34px}}
.eyebrow .n{{color:var(--accent);font-size:14px;font-weight:600}}
.eyebrow .t{{font-size:12.5px;letter-spacing:.22em;text-transform:uppercase;font-weight:600}}
h1{{font-family:'League Spartan',sans-serif;font-weight:800;font-size:clamp(30px,4vw,46px);line-height:1.05;letter-spacing:-.02em;margin-top:14px}}
p.lede{{margin-top:18px;font-weight:300;font-size:19px;line-height:1.6;color:var(--texte-2);max-width:520px}}
.row{{display:flex;flex-wrap:wrap;gap:14px;margin-top:34px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 28px;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;text-decoration:none;border:1px solid var(--anthra);transition:background .2s,color .2s}}
.btn:hover{{background:var(--anthra);color:var(--blanc)}}
.btn-accent{{background:var(--accent);border-color:var(--accent);color:var(--sur-accent)}}
.btn-accent:hover{{background:var(--anthra);border-color:var(--anthra);color:var(--blanc)}}
.liens .t{{display:block;font-size:12.5px;letter-spacing:.22em;text-transform:uppercase;font-weight:600;margin-bottom:12px}}
.liste{{display:flex;flex-direction:column}}
.liste a{{display:grid;grid-template-columns:130px 1fr auto;align-items:baseline;gap:12px;padding:16px 0;border-top:1px solid var(--trait);text-decoration:none}}
.liste a:last-child{{border-bottom:1px solid var(--trait)}}
.liste .k{{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--texte-3)}}
.liste b{{font-family:'League Spartan',sans-serif;font-weight:800;font-size:22px;letter-spacing:-.01em}}
.liste i{{font-style:normal;color:var(--accent);transition:transform .2s}}
.liste a:hover i{{transform:translateX(4px)}}
footer{{background:var(--anthra);color:#A39C9E;font-size:13px;line-height:1.9}}
footer .in{{max-width:var(--max);margin:0 auto;padding:26px var(--pad) calc(26px + env(safe-area-inset-bottom));display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}}
footer b{{color:var(--blanc);font-family:'League Spartan',sans-serif;font-weight:800}}
:lang(zh) h1,:lang(zh) .liste b{{font-family:'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;font-weight:700;letter-spacing:0}}
/* téléphone : aucun défilement, tout tient sur un écran ; les liens en grille de deux colonnes */
@media(max-width:900px){{
  :root{{--pad:22px}}
  .top-in{{padding:10px var(--pad)}}
  main{{grid-template-columns:minmax(0,1fr);gap:26px;padding:26px var(--pad) 22px;align-content:start}}
  main>*{{min-width:0}}
  .grand{{font-size:84px;-webkit-text-stroke-width:1.5px}}
  .eyebrow{{margin-top:18px}}
  h1{{font-size:27px;margin-top:8px}}
  p.lede{{font-size:15.5px;margin-top:10px}}
  .row{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:20px}}
  .btn{{min-height:48px;padding:0 10px;font-size:11px;letter-spacing:.1em;text-align:center}}
  .liens .t{{margin-bottom:8px}}
  .liste{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
  .liste a,.liste a:last-child{{display:block;background:var(--blanc);border:0;border-top:2px solid var(--accent);padding:10px 12px}}
  .liste .k,.liste i{{display:none}}
  .liste b{{font-size:17px}}
  footer .in{{padding:14px var(--pad) calc(14px + env(safe-area-inset-bottom));font-size:12px}}
}}
/* petits téléphones (iPhone SE…) : encore plus serré pour rester sur un seul écran */
@media(max-width:900px) and (max-height:720px){{
  main{{gap:16px;padding-top:14px;padding-bottom:14px}}
  .grand{{font-size:58px}}
  .eyebrow{{margin-top:10px}}
  h1{{font-size:23px}}
  p.lede{{font-size:14.5px;line-height:1.5}}
  .row{{margin-top:14px}}.btn{{min-height:44px}}
  .liste a,.liste a:last-child{{padding:8px 10px}}
  .liste b{{font-size:15px}}
}}
@media(prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
</style>
<link rel="stylesheet" href="{base}season.css">
</head>
<body>

<header class="top">
  <div class="top-in">
    <a class="mark" href="{base}">UNSEEN.</a>
    <div class="lang"><button type="button" data-l="en" aria-pressed="true">EN</button><span>/</span><button type="button" data-l="fr" aria-pressed="false">FR</button><span>/</span><button type="button" data-l="zh" aria-pressed="false" lang="zh">中文</button></div>
  </div>
</header>

<main>
  <div>
    <div class="grand" aria-hidden="true">404</div>
    <div class="eyebrow"><span class="n">404</span>{t("Page not found", "Page introuvable", "页面不存在", attrs=' class="t"')}</div>
    {t("This page stayed unseen.", "Cette page est restée invisible.", "这一页，未曾现身。", "h1")}
    {t("The address you followed does not lead anywhere. It may have moved, or never existed at all.",
       "Ce lien ne mène nulle part. La page a peut-être été déplacée, ou n'a jamais existé.",
       "您访问的链接无法打开。页面可能已经移动，或者从未存在。", "p", ' class="lede"')}
    <div class="row">
      <a class="btn btn-accent" href="{base}">{t("Back to the site", "Retour au site", "返回网站")}</a>
      <a class="btn" href="https://wa.me/33613850733">{t("WhatsApp", "WhatsApp", "WhatsApp")}</a>
    </div>
  </div>
  <nav class="liens" aria-label="Pages">
    {t("Perhaps you were looking for", "Vous cherchiez peut-être", "您也许在找", attrs=' class="t"')}
    <div class="liste">{liens}</div>
  </nav>
</main>

<footer><div class="in"><span><b>UNSEEN.</b> {t("Private luxury concierge, Paris.", "Conciergerie privée de luxe, Paris.", "巴黎私人奢华礼宾服务。")}</span><a href="{base}legal.html">{t("Legal notice", "Mentions légales", "法律声明")}</a></div></footer>

<script>
/* Même mémoire de langue que le reste du site (localStorage « unseen-lang ») */
(function(){{
  var TITRES={{en:'UNSEEN. — Page not found',fr:'UNSEEN. — Page introuvable',zh:'UNSEEN. — 页面不存在'}};
  function setLang(l){{
    document.querySelectorAll('[data-en]').forEach(function(n){{var v=n.getAttribute('data-'+l);if(v!==null)n.textContent=v;}});
    document.documentElement.lang=l;document.title=TITRES[l];
    document.querySelectorAll('button[data-l]').forEach(function(b){{b.setAttribute('aria-pressed',b.dataset.l===l?'true':'false');}});
    try{{localStorage.setItem('unseen-lang',l);}}catch(e){{}}
  }}
  document.querySelectorAll('button[data-l]').forEach(function(b){{b.addEventListener('click',function(){{setLang(b.dataset.l);}});}});
  var s=null;try{{s=localStorage.getItem('unseen-lang');}}catch(e){{}}
  var nav=(navigator.language||'').toLowerCase();
  if(s==='fr'||s==='zh')setLang(s);else if(!s&&nav.indexOf('zh')===0)setLang('zh');else if(!s&&nav.indexOf('fr')===0)setLang('fr');
}})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    if sys.argv[1] == "maquette":
        MAQUETTE.write_text(page("../../site-unseen/"), encoding="utf-8")
        print("maquette :", MAQUETTE)
    else:
        (SITE / "404.html").write_text(page("/"), encoding="utf-8")
        print("404.html remplacée")
