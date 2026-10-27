"""
Protège les adresses e-mail du site contre les robots qui les relèvent pour envoyer du spam
(27/10/2026). Le visiteur voit et clique exactement comme avant ; seul le code brut change :
- liens « mailto: » : l'adresse est découpée dans des attributs (data-u / data-d) et reconstituée
  par un petit script à l'ouverture de la page ;
- adresses écrites dans le texte ou dans les attributs de langue : « @ » codé en &#64; ;
- adresses dans les scripts (formulaire, données pour Google) : « @ » écrit \\u0040.

À relancer si une adresse est ajoutée à une page :
    python3 site-unseen/outils/proteger_emails.py
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "professionals.html", "paris.html", "riviera.html", "ocean-indien.html",
         "saison-ski-2026-2027.html", "formule-1.html", "legal.html"]
DOMAINE = r"unseenconciergerie\.(?:com|fr)"
SCRIPT_FINAL = ("<script>/* Adresses e-mail reconstituées à l'ouverture (protection contre les robots) */"
                "document.querySelectorAll('a[data-u]').forEach(function(a){a.href='mailto:'+a.dataset.u+'\\u0040'+a.dataset.d+(a.dataset.q||'');});</script>\n")


def proteger(page):
    morceaux = re.split(r"(<script[^>]*>.*?</script>)", page, flags=re.S)
    for i, m in enumerate(morceaux):
        if m.startswith("<script"):
            morceaux[i] = re.sub(r"@(" + DOMAINE + ")", r"\\u0040\1", m)
            continue
        # liens mailto
        m = re.sub(r'href="mailto:([\w.+-]+)@(' + DOMAINE + r')(\?[^"]*)?"',
                   lambda x: f'href="#" data-u="{x.group(1)}" data-d="{x.group(2)}"' + (f' data-q="{x.group(3)}"' if x.group(3) else ""), m)
        # adresses restantes, dans le texte ou les attributs
        m = re.sub(r"([\w.+-]+)@(" + DOMAINE + ")", r"\1&#64;\2", m)
        morceaux[i] = m
    page = "".join(morceaux)
    if "data-u=" in page and "Adresses e-mail reconstituées" not in page:
        i = page.rindex("</body>")
        page = page[:i] + SCRIPT_FINAL + page[i:]
    return page


if __name__ == "__main__":
    for nom in PAGES:
        chemin = SITE / nom
        avant = chemin.read_text(encoding="utf-8")
        apres = proteger(avant)
        chemin.write_text(apres, encoding="utf-8")
        reste = re.findall(r"[\w.+-]+@" + DOMAINE, apres)
        print(f"{nom:28} liens {apres.count('data-u=')}, adresses encore lisibles par un robot : {len(reste)}")
