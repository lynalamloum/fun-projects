import tkinter as tk
from tkinter import filedialog

import asyncio
from shazamio import Shazam

import requests
from PIL import Image, ImageTk
from io import BytesIO

import yt_dlp
import re

import pygame
pygame.mixer.init()

# État général du lecteur
en_pause = False
playlist = []        # liste des chemins de fichiers chargés
index_courant = 0    # quelle chanson on écoute
infos_playlist = {}  # titre, artiste, pochette pour chaque fichier


# Quand Shazam ne reconnaît pas la chanson, on demande à l'utilisateur
def saisie_manuelle(fichier):
    
    popup = tk.Toplevel(fenetre)
    popup.title("Saisie manuelle")
    popup.geometry("300x200")
    popup.configure(bg="#1a1a1a")

    tk.Label(popup, text="Titre :", fg="white", bg="#1a1a1a").pack(pady=5)
    entry_titre = tk.Entry(popup)
    entry_titre.pack(pady=5)

    tk.Label(popup, text="Artiste :", fg="white", bg="#1a1a1a").pack(pady=5)
    entry_artiste = tk.Entry(popup)
    entry_artiste.pack(pady=5)

    chemin_image = [None]  # liste à un élément pour pouvoir la modifier depuis les fonctions imbriquées

    def choisir_image():
        chemin = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if chemin:
            chemin_image[0] = chemin

    def valider():
        label_titre.configure(text=entry_titre.get())
        label_artiste.configure(text=entry_artiste.get())
        
        if chemin_image[0]:
            image = Image.open(chemin_image[0])
            image = image.resize((120, 120))
            photo = ImageTk.PhotoImage(image)
            label_pochette.configure(image=photo)
            label_pochette.image = photo  # on garde une référence sinon Python supprime l'image

            infos_playlist[fichier] = {
                "titre": entry_titre.get(),
                "artiste": entry_artiste.get(),
                "chemin_image": chemin_image[0]
            }

        popup.destroy()

    tk.Button(popup, text="Choisir une image", bg="#2a2a2a", fg="white", command=choisir_image).pack(pady=5)
    tk.Button(popup, text="OK", bg="#2a2a2a", fg="white", command=valider).pack(pady=10)


# Shazam identifie la chanson et on récupère titre, artiste et pochette
async def reconnaitre(fichier):

    shazam = Shazam()

    try:
        resultat = await shazam.recognize(fichier)
        titre = resultat["track"]["title"]
        artiste = resultat["track"]["subtitle"]
        pochette_url = resultat["track"]["images"]["coverart"]

    except:
        # Si Shazam rate ou que la chanson est inconnue, on laisse l'utilisateur remplir à la main
        saisie_manuelle(fichier)
        return

    # On sauvegarde les infos pour ne pas relancer Shazam si on revient sur cette chanson
    infos_playlist[fichier] = {
        "titre": titre,
        "artiste": artiste,
        "pochette_url": pochette_url
    }

    reponse = requests.get(pochette_url)
    image = Image.open(BytesIO(reponse.content))
    image = image.resize((120, 120))
    photo = ImageTk.PhotoImage(image)

    label_pochette.configure(image=photo)
    label_pochette.image = photo

    label_artiste.configure(text=artiste)

    # On tronque le titre s'il est trop long pour l'écran
    titre_affiche = titre[:25] + "..." if len(titre) > 25 else titre
    label_titre.configure(text=titre_affiche)


# Recherche sur YouTube et télécharge l'audio en MP3
def telecharger_youtube(titre, artiste):

    # On enlève les caractères interdits dans les noms de fichiers Windows
    titre_propre = re.sub(r'[\\/*?:"<>|]', '', titre)
    artiste_propre = re.sub(r'[\\/*?:"<>|]', '', artiste)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{titre_propre} - {artiste_propre}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # ytsearch1: = prend le premier résultat YouTube
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{titre} {artiste} official audio"])

    fichier = f'{titre_propre} - {artiste_propre}.mp3'
    playlist.append(fichier)
    global index_courant
    index_courant = len(playlist) - 1
    asyncio.run(reconnaitre(fichier))
    jouer_musique(fichier)


def ouvrir_recherche():
    popup = tk.Toplevel(fenetre)
    popup.title("Rechercher une chanson")
    popup.geometry("300x200")
    popup.configure(bg="#1a1a1a")

    tk.Label(popup, text="Titre :", fg="white", bg="#1a1a1a").pack(pady=5)
    entry_titre = tk.Entry(popup)
    entry_titre.pack(pady=5)

    tk.Label(popup, text="Artiste :", fg="white", bg="#1a1a1a").pack(pady=5)
    entry_artiste = tk.Entry(popup)
    entry_artiste.pack(pady=5)

    tk.Button(popup, text="Télécharger", bg="#2a2a2a", fg="white",
        command=lambda: telecharger_youtube(entry_titre.get(), entry_artiste.get())
    ).pack(pady=10)


def jouer_musique(fichier):
    pygame.mixer.music.load(fichier)
    pygame.mixer.music.play()  # non-bloquant, la musique tourne en arrière-plan


def toggle_pause():
    global en_pause
    if en_pause:
        pygame.mixer.music.unpause()
        en_pause = False
    else:
        pygame.mixer.music.pause()
        en_pause = True


def suivant():
    global index_courant
    if index_courant < len(playlist) - 1:
        index_courant += 1
        fichier = playlist[index_courant]
        # Si on a déjà les infos en mémoire, pas besoin de relancer Shazam
        if fichier in infos_playlist:
            label_titre.configure(text=infos_playlist[fichier]["titre"])
            label_artiste.configure(text=infos_playlist[fichier]["artiste"])
            if "chemin_image" in infos_playlist[fichier]:
                image = Image.open(infos_playlist[fichier]["chemin_image"])
                image = image.resize((120, 120))
                photo = ImageTk.PhotoImage(image)
                label_pochette.configure(image=photo)
                label_pochette.image = photo
            elif "pochette_url" in infos_playlist[fichier]:
                reponse = requests.get(infos_playlist[fichier]["pochette_url"])
                image = Image.open(BytesIO(reponse.content))
                image = image.resize((120, 120))
                photo = ImageTk.PhotoImage(image)
                label_pochette.configure(image=photo)
                label_pochette.image = photo
        else:
            asyncio.run(reconnaitre(fichier))
        jouer_musique(fichier)


def precedent():
    global index_courant
    if index_courant > 0:
        index_courant -= 1
        fichier = playlist[index_courant]
        if fichier in infos_playlist:
            label_titre.configure(text=infos_playlist[fichier]["titre"])
            label_artiste.configure(text=infos_playlist[fichier]["artiste"])
            if "chemin_image" in infos_playlist[fichier]:
                image = Image.open(infos_playlist[fichier]["chemin_image"])
                image = image.resize((120, 120))
                photo = ImageTk.PhotoImage(image)
                label_pochette.configure(image=photo)
                label_pochette.image = photo
            elif "pochette_url" in infos_playlist[fichier]:
                reponse = requests.get(infos_playlist[fichier]["pochette_url"])
                image = Image.open(BytesIO(reponse.content))
                image = image.resize((120, 120))
                photo = ImageTk.PhotoImage(image)
                label_pochette.configure(image=photo)
                label_pochette.image = photo
        else:
            asyncio.run(reconnaitre(fichier))
        jouer_musique(fichier)


def charger_musique():
    fichier = filedialog.askopenfilename()
    asyncio.run(reconnaitre(fichier))
    jouer_musique(fichier)
    playlist.append(fichier)
    global index_courant
    index_courant = len(playlist) - 1


# Dessine un rectangle avec des coins arrondis sur le canvas
# tkinter ne supporte pas ça nativement donc on assemble des arcs et des rectangles
def arrondi(canvas, x1, y1, x2, y2, rayon=30, **kwargs):
    canvas.create_arc(x1, y1, x1+2*rayon, y1+2*rayon, start=90, extent=90, style="pieslice", **kwargs)
    canvas.create_arc(x2-2*rayon, y1, x2, y1+2*rayon, start=0, extent=90, style="pieslice", **kwargs)
    canvas.create_arc(x1, y2-2*rayon, x1+2*rayon, y2, start=180, extent=90, style="pieslice", **kwargs)
    canvas.create_arc(x2-2*rayon, y2-2*rayon, x2, y2, start=270, extent=90, style="pieslice", **kwargs)
    canvas.create_rectangle(x1+rayon, y1, x2-rayon, y2, **kwargs)
    canvas.create_rectangle(x1, y1+rayon, x2, y2-rayon, **kwargs)


def jouer_depuis_playlist(i, fichier, popup):
    global index_courant
    index_courant = i
    popup.destroy()
    if fichier in infos_playlist:
        label_titre.configure(text=infos_playlist[fichier]["titre"][:25])
        label_artiste.configure(text=infos_playlist[fichier]["artiste"])
        if "chemin_image" in infos_playlist[fichier]:
            image = Image.open(infos_playlist[fichier]["chemin_image"])
            image = image.resize((120, 120))
            photo = ImageTk.PhotoImage(image)
            label_pochette.configure(image=photo)
            label_pochette.image = photo
        elif "pochette_url" in infos_playlist[fichier]:
            reponse = requests.get(infos_playlist[fichier]["pochette_url"])
            image = Image.open(BytesIO(reponse.content))
            image = image.resize((120, 120))
            photo = ImageTk.PhotoImage(image)
            label_pochette.configure(image=photo)
            label_pochette.image = photo
    jouer_musique(fichier)


def voir_playlist():
    popup = tk.Toplevel(fenetre)
    popup.title("Playlist")
    popup.geometry("300x400")
    popup.configure(bg="#1a1a1a")
    
    for i, fichier in enumerate(playlist):
        if fichier in infos_playlist:
            titre = infos_playlist[fichier]["titre"]
            artiste = infos_playlist[fichier]["artiste"]
            tk.Button(popup, text=f"{i+1}. {titre} - {artiste}", fg="white", bg="#1a1a1a",
                # lambda i=i capture la valeur actuelle de i, sinon tous les boutons joueraient la dernière chanson
                command=lambda i=i, f=fichier: jouer_depuis_playlist(i, f, popup)
            ).pack(pady=5)
        else:
            tk.Button(popup, text=f"{i+1}. {fichier}", fg="white", bg="#1a1a1a",
                command=lambda i=i, f=fichier: jouer_depuis_playlist(i, f, popup)
            ).pack(pady=5)


def changer_couleur(couleur):

    # Chaque couleur de corps a sa version plus foncée pour la roue
    couleurs_roue = {
        "white": "#e0e0e0",
        "black": "#222222",
        "#cc0000": "#aa0000",
        "#0055cc": "#0044aa",
        "#006600": "#004400"
    }

    # Et une couleur harmonieuse pour le texte
    couleurs_texte = {
        "white": "#555555",
        "black": "#aaaaaa",
        "#cc0000": "#ffaaaa",
        "#0055cc": "#aaccff",
        "#006600": "#aaffaa"
    }

    # itemconfig("tag", ...) modifie tous les éléments qui ont ce tag
    canvas.itemconfig("corps", fill=couleur)
    canvas.itemconfig("roue", fill=couleurs_roue[couleur])
    canvas.itemconfig("texte_roue", fill=couleurs_texte[couleur])


def ouvrir_couleurs():
    popup = tk.Toplevel(fenetre)
    popup.title("Couleur")
    popup.geometry("200x250")
    popup.configure(bg="#1a1a1a")

    couleurs = [
        ("Blanc", "white"),
        ("Noir", "black"),
        ("Rouge", "#cc0000"),
        ("Bleu", "#0055cc"),
        ("Vert", "#006600")
    ]

    for nom, code in couleurs:
        tk.Button(popup, text=nom, bg=code, fg="white",
            command=lambda c=code: [changer_couleur(c), popup.destroy()]
        ).pack(pady=5, fill="x", padx=20)


def ouvrir_menu():
    popup = tk.Toplevel(fenetre)
    popup.title("Menu")
    popup.geometry("200x180")
    popup.configure(bg="#1a1a1a")

    tk.Button(popup, text="Rechercher sur YouTube", bg="#2a2a2a", fg="white",
        command=lambda: [popup.destroy(), ouvrir_recherche()]).pack(pady=10)
    tk.Button(popup, text="Voir la playlist", bg="#2a2a2a", fg="white",
        command=lambda: [popup.destroy(), voir_playlist()]).pack(pady=10)
    tk.Button(popup, text="Changer la couleur", bg="#2a2a2a", fg="white",
        command=lambda: [popup.destroy(), ouvrir_couleurs()]).pack(pady=10)


# --- Interface ---

fenetre = tk.Tk()
fenetre.title("iPod")
fenetre.geometry("300x600")
fenetre.configure(bg="#f0f0f0")
fenetre.resizable(False, False)

canvas = tk.Canvas(fenetre, width=300, height=600, bg="#f0f0f0", highlightthickness=0)
canvas.pack()

# Corps de l'iPod (tag "corps" pour pouvoir changer la couleur plus tard)
arrondi(canvas, 20, 20, 280, 580, rayon=30, fill="white", outline="", tags="corps")

# Écran noir
arrondi(canvas, 40, 40, 260, 280, rayon=10, fill="#111111", outline="")

# Roue et cercle central
canvas.create_oval(60, 320, 240, 500, fill="#d0d0d0", outline="", tags="roue")
canvas.create_oval(110, 370, 190, 450, fill="white", outline="", tags="corps")

# Labels de la roue (tag "texte_roue" pour adapter la couleur selon le thème)
canvas.create_text(150, 345, text="MENU", fill="#555555", font=("Helvetica", 9, "bold"), tags="texte_roue")
canvas.create_text(85, 410, text="<<", fill="#555555", font=("Helvetica", 11, "bold"), tags="texte_roue")
canvas.create_text(215, 410, text=">>", fill="#555555", font=("Helvetica", 11, "bold"), tags="texte_roue")
canvas.create_text(150, 475, text="▶ ‖", fill="#555555", font=("Helvetica", 10, "bold"), tags="texte_roue")

# Éléments de l'écran (intégrés au canvas avec create_window)
label_pochette = tk.Label(fenetre, bg="#111111")
canvas.create_window(150, 130, window=label_pochette)

label_titre = tk.Label(fenetre, text="Titre", fg="white", bg="#111111", font=("Helvetica", 10, "bold"))
canvas.create_window(150, 220, window=label_titre)

label_artiste = tk.Label(fenetre, text="Artiste", fg="#aaaaaa", bg="#111111", font=("Helvetica", 9))
canvas.create_window(150, 240, window=label_artiste)

# Zones invisibles cliquables sur la roue
zone_menu = canvas.create_oval(100, 310, 200, 380, fill="", outline="")
canvas.tag_bind(zone_menu, "<Button-1>", lambda e: ouvrir_menu())

zone_precedent = canvas.create_oval(60, 360, 130, 460, fill="", outline="")
canvas.tag_bind(zone_precedent, "<Button-1>", lambda e: precedent())

zone_suivant = canvas.create_oval(170, 360, 240, 460, fill="", outline="")
canvas.tag_bind(zone_suivant, "<Button-1>", lambda e: suivant())

zone_pause = canvas.create_oval(100, 440, 200, 510, fill="", outline="")
canvas.tag_bind(zone_pause, "<Button-1>", lambda e: toggle_pause())

# Le centre de la roue charge une nouvelle chanson
zone_centre = canvas.create_oval(110, 370, 190, 450, fill="", outline="")
canvas.tag_bind(zone_centre, "<Button-1>", lambda e: charger_musique())

fenetre.mainloop()
