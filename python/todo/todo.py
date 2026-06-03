import json
import os
import datetime


def charger_taches():
    if not os.path.exists("tasks.json"):
        return []
    with open("tasks.json", "r") as f:
        donnees = json.load(f)
    return donnees


def sauvegarde_taches(taches):
    with open("tasks.json", "w") as f:
        json.dump(taches, f)


def affichage_taches(taches):
    for tache in taches:
        date = tache.get("date", "inconnue")
        priorite = tache.get("priorité", "inconnue")
        statut = "[✓]" if tache["fait"] else "[✗]"
        print(f'{tache["id"]}. {statut} {tache["tache"]} (ajoutée le {date}) {priorite}')


def ajouter_tache(taches):
    nom = ""
    choix_priorite = 0
    liste_priorite = [1, 2, 3]
    date = datetime.datetime.now().strftime("%x")

    while nom == "":
        nom = input("Ajouter une nouvelle tâche : ")
        if nom == "":
            print("La tâche est vide ! Veuillez recommencer.")

    print(" ")
    print("Priorité : 1. Haute  2. Moyenne  3. Basse")
    print(" ")

    while choix_priorite not in liste_priorite:
        try:
            choix_priorite = int(input("Priorité : "))
        except ValueError:
            print("Ce n'est pas un chiffre ! Veuillez réessayer.")
        if choix_priorite not in liste_priorite:
            print("Cette priorité n'existe pas ! Veuillez réessayer.")

    if choix_priorite == 1:
        priorite = "!!!"
    elif choix_priorite == 2:
        priorite = "!!"
    else:
        priorite = "!"

    nouvelle_tache = {
        "id": len(taches) + 1,
        "tache": nom,
        "fait": False,
        "date": date,
        "priorité": priorite
    }

    taches.append(nouvelle_tache)
    sauvegarde_taches(taches)
    print("Tâche ajoutée !")


def tache_faite(taches):
    affichage_taches(taches)
    liste = [tache["id"] for tache in taches]
    faite = 0

    while faite not in liste:
        try:
            faite = int(input("Quelle tâche a été faite ? "))
        except ValueError:
            print("Ce n'est pas un chiffre ! Veuillez réessayer.")
        if faite not in liste:
            print("Cette tâche n'existe pas ! Veuillez réessayer.")

    for tache in taches:
        if tache["id"] == faite:
            tache["fait"] = True

    sauvegarde_taches(taches)
    print("Tâche marquée comme faite !")


def supprimer_tache(taches):
    affichage_taches(taches)
    liste = [tache["id"] for tache in taches]
    supprimer = 0
    verif = False

    while supprimer not in liste or not verif:
        try:
            supprimer = int(input("Quelle tâche voulez-vous supprimer ? "))
        except ValueError:
            print("Ce n'est pas un chiffre ! Veuillez réessayer.")
        if supprimer not in liste:
            print("Cette tâche n'existe pas ! Veuillez réessayer.")
        if supprimer in liste:
            oui_ou_non = input("Voulez-vous vraiment supprimer cette tâche ? (o/n) : ")
            if oui_ou_non == "o":
                verif = True

    for tache in taches:
        if tache["id"] == supprimer:
            taches.remove(tache)

    sauvegarde_taches(taches)
    print("Tâche supprimée !")


def menu(taches):
    print("""=== TO DO LIST ===
1. Afficher les tâches
2. Ajouter une tâche
3. Marquer comme faite
4. Supprimer une tâche
5. Quitter""")
    print(" ")

    choix = 0
    liste = [1, 2, 3, 4, 5]

    while choix not in liste:
        try:
            choix = int(input("Votre choix : "))
        except ValueError:
            print("Ce n'est pas un chiffre ! Veuillez réessayer.")

    print(" ")

    if choix == 1:
        affichage_taches(taches)
    elif choix == 2:
        ajouter_tache(taches)
    elif choix == 3:
        tache_faite(taches)
    elif choix == 4:
        supprimer_tache(taches)
    elif choix == 5:
        return 0

    print(" ")


liste = charger_taches()
continuer = True

while continuer:
    if menu(liste) == 0:
        oui_ou_non = input("Voulez-vous vraiment quitter ? (o/n) : ")
        if oui_ou_non == "o":
            continuer = False
