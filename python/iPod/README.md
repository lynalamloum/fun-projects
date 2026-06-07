# iPod - v1

*A trip down memory lane. / Un retour en enfance.*

---

## EN

I'm a beginner Python developer and this is one of my first real projects. The goal was to build something I'd actually want to use, learn along the way and not be too perfectionist about the result. So here's an iPod Classic built in Python, functional and a little rough around the edges.

Load an MP3, Shazam identifies it and fetches the album cover automatically. If it doesn't recognize the song, you can fill in the info yourself. You can also search for songs by title and artist and download them straight from YouTube. The wheel is clickable : MENU opens the settings, the center button loads a file and the rest does what you'd expect.

Feel free to try it or build on it.

**Features**

- Clickable iPod wheel (MENU, play/pause, previous, next, load)
- Automatic song recognition via Shazam
- Album art fetched automatically
- YouTube search and download (audio only)
- Manual entry when Shazam doesn't recognize a track
- Clickable playlist
- Color customization (white, black, red, blue, green)

**Requirements**

- Python 3.12
- ffmpeg installed and added to PATH

```bash
pip install -r requirements.txt
```

**Run**

```bash
py -3.12 ipod.py
```

This is v1. A v2 with a proper web interface is planned with the same features but a much better design.

---

## FR

Je suis développeuse Python débutante et c'est l'un de mes premiers vrais projets. L'objectif était de construire quelque chose que j'aurais envie d'utiliser, qui me permettrait d'apprendre en chemin et de ne pas trop me prendre la tête sur le résultat. Voilà donc un iPod Classic fait en Python, fonctionnel et encore améliorable.

Charge un MP3, Shazam l'identifie et récupère la pochette automatiquement. Si la chanson n'est pas reconnue, vous pouvez remplir les infos vous-même. Vous pouvez aussi rechercher une chanson par titre et artiste et la télécharger directement depuis YouTube. La roue est cliquable : MENU ouvre les paramètres, le bouton central charge un fichier et le reste fait ce qu'on attend.

N'hésitez pas à le tester ou à vous en inspirer.

**Fonctionnalités**

- Roue iPod cliquable (MENU, play/pause, précédent, suivant, charger)
- Reconnaissance automatique des chansons via Shazam
- Récupération automatique des pochettes
- Recherche et téléchargement depuis YouTube (audio uniquement)
- Saisie manuelle si Shazam ne reconnaît pas la chanson
- Playlist cliquable
- Personnalisation de la couleur (blanc, noir, rouge, bleu, vert)

**Prérequis**

- Python 3.12
- ffmpeg installé et ajouté au PATH

```bash
pip install -r requirements.txt
```

**Lancer**

```bash
py -3.12 ipod.py
```

C'est la v1. Une v2 avec une vraie interface web est prévue avec les mêmes fonctionnalités et un meilleur design.

---

*Built with Python, tkinter, pygame, Shazam and yt-dlp.*

---
 
## Author / Auteur
 
Projet réalisé dans le cadre d'un apprentissage personnel de Python.  
Personal Python learning project.
