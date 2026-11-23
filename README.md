# J.A.R.V.I.S. MK-1

- `index.html` : website (avatar + offline dimaag + AI). GitHub Pages par jayegi.
- `jarvis_pc.py` : laptop control + AQ key bridge. Sirf aapke PC par chalega.
- `start_jarvis_pc.bat` : double-click se bridge chalu.
- `requirements.txt` : screenshot ke liye `pillow`.

## GitHub par live karna
1. github.com par New Repository banao (naam: jarvis, Public).
2. "uploading an existing file" se `index.html` aur `README.md` upload karo, Commit karo.
   (`jarvis_pc.py` upload karna zaruri nahi. Ye sirf PC ke liye hai.)
3. Settings > Pages > Source: "Deploy from a branch", Branch: main, folder: / (root) > Save.
4. 1-2 minute baad site: https://USERNAME.github.io/jarvis/

## Pehli baar setup
1. Site kholo (Chrome ya Edge) > Settings > apni AQ key paste karo > Save. Key sirf aapke browser mein save hoti hai.
2. Mic permission Allow karo.

## Laptop control (optional, Windows)
1. Python install karo (python.org, "Add to PATH" tick karo).
2. `jarvis_pc.py` aur `start_jarvis_pc.bat` ek folder mein rakho, `pip install pillow` chalao.
3. `start_jarvis_pc.bat` double-click karo. Site par badge "PC: CONNECTED" ho jayega.
4. Chrome/Edge chahiye. Firefox/Safari live site se localhost ko block kar sakte hain.

## Zaruri suraksha
- Apni API key kabhi `index.html` mein likh kar GitHub par mat daalo. Repo public hai.
- Jo key pehle share hui, Google Cloud mein delete karke nayi banao.
- Google Cloud mein key par "API restriction" lagao aur budget alert set karo.
