"""
Vérifie les pages du site dans le VRAI Safari du Mac, dans une fenêtre de la largeur d'un iPhone.

Safari du Mac utilise le même moteur (WebKit) que Safari sur iPhone : c'est le test le plus
proche de ce que voient les visiteurs. Rien à installer : safaridriver est fourni avec macOS
(activé une fois par Jay avec « safaridriver --enable »).

Pour chaque page, le script prend des captures en descendant écran par écran, puis les
assemble en une planche par page, dans le dossier de sortie.

Lancer, depuis le dossier du projet :
    safaridriver -p 4447 &
    assistant-prospection/venv/bin/python site-unseen/outils/verifier_safari.py [en ligne|local] [dossier] [pages...]
    pkill -f "safaridriver -p 4447"
"""
import base64
import io
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

SITE = Path(__file__).resolve().parent.parent
PAGES = [p for p in sys.argv[3:]] or ["index.html", "professionals.html", "paris.html", "riviera.html", "ocean-indien.html",
         "saison-ski-2026-2027.html", "formule-1.html", "legal.html"]
LARGEUR, HAUTEUR = 390, 844          # iPhone 14 / 15
PORT = 4447


def appel(methode, chemin, donnees=None):
    req = urllib.request.Request(f"http://localhost:{PORT}{chemin}", method=methode,
                                 data=json.dumps(donnees).encode() if donnees is not None else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read() or b"{}")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "en ligne"
    sortie = Path(sys.argv[2]) if len(sys.argv) > 2 else SITE / "outils" / "captures_safari"
    sortie.mkdir(parents=True, exist_ok=True)
    base = "https://unseenconciergerie.com/" if mode == "en ligne" else f"file://{SITE}/"

    # Le pilote se lance depuis le Terminal (lancé depuis Python, macOS le refuse parfois) :
    #   safaridriver -p 4447 &   puis ce script
    try:
        deja = appel("GET", "/status")["value"].get("ready")
    except OSError:
        deja = False
    pilote = None if deja else subprocess.Popen(["safaridriver", "-p", str(PORT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):                      # on attend que le pilote soit prêt (jusqu'à 15 s)
        try:
            if appel("GET", "/status")["value"].get("ready"):
                break
        except OSError:
            pass
        time.sleep(0.5)
    try:
        sid = appel("POST", "/session", {"capabilities": {"alwaysMatch": {"browserName": "safari"}}})["value"]["sessionId"]
        try:
            appel("POST", f"/session/{sid}/window/rect", {"x": 0, "y": 0, "width": LARGEUR, "height": HAUTEUR})
            for page in PAGES:
                appel("POST", f"/session/{sid}/url", {"url": base + page + ("?v=%d" % time.time() if mode == "en ligne" else "")})
                time.sleep(3)
                total = appel("POST", f"/session/{sid}/execute/sync", {"script": "return document.documentElement.scrollHeight", "args": []})["value"]
                vue = appel("POST", f"/session/{sid}/execute/sync", {"script": "return window.innerHeight", "args": []})["value"]
                images, y = [], 0
                while y < total and len(images) < 30:
                    appel("POST", f"/session/{sid}/execute/sync", {"script": f"window.scrollTo(0,{y})", "args": []})
                    time.sleep(1.2)
                    png = appel("GET", f"/session/{sid}/screenshot")["value"]
                    images.append(Image.open(io.BytesIO(base64.b64decode(png))).convert("RGB"))
                    y += vue
                # planche : les écrans côte à côte, comme une bande dessinée
                w, h = images[0].size
                colonnes = min(len(images), 6)
                lignes = (len(images) + colonnes - 1) // colonnes
                planche = Image.new("RGB", (colonnes * (w + 12), lignes * (h + 12)), "white")
                for i, im in enumerate(images):
                    planche.paste(im, ((i % colonnes) * (w + 12), (i // colonnes) * (h + 12)))
                planche.thumbnail((2400, 2400))
                planche.save(sortie / f"{page.replace('.html', '')}.png")
                print(f"ok {page} : {len(images)} écrans, largeur réelle {w}px")
        finally:
            appel("DELETE", f"/session/{sid}")
    finally:
        if pilote:
            pilote.terminate()


if __name__ == "__main__":
    main()
