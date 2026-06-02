import random

def mot_aleatoire() :
    
    mots = [
    "python", "ordinateur", "algorithme", "clavier", "variable",
    "fonction", "boucle", "condition", "terminal", "bibliotheque",
    "compilation", "debugger", "interface", "heritage", "recursion",
    "pointeur", "memoire", "processeur", "reseau", "architecture"
    ]
    
    return random.choice(mots)

def affichage_mot(mot) :
    
    mot_a_deviner = list(mot)
    affichage = []
    
    for i in range (len(mot_a_deviner)) :
        affichage.append("_")
    
    return affichage
        
def verif_lettre(lettre, mot) :
    
    for i in range (len(mot)) :
        if mot[i] == lettre :
            return True
    return False

def lettres_trouvees(mot) :
    trouvees = 0
    for i in range (len(mot)) :
        if mot[i] != "_" :
            trouvees += 1
    return trouvees

def nouveau_affichage(affichage, mot, lettre) :
    
    nv_affichage = []
    
    for i in range (len(mot)) :
        if mot[i] == lettre :
            nv_affichage.append(lettre)
        else :
            nv_affichage.append(affichage[i])
            
    return nv_affichage

def afficher_mot(affichage) :
    
    print(" ".join(affichage)) 
            
def bonhomme(tentatives) :
    
    etapes = [
        " ",
        "     |",
        "     |\n     O",
        "     |\n     O\n     |",
        "     |\n     O\n     |\n    \\ /",
        "     |\n     O\n     |\n    \\ /\n     |",
        "     |\n     O\n     |\n    \\ /\n     |\n    / \\ "
    ]
    print(etapes[tentatives])
    
def pendu() :
    
    mot = mot_aleatoire()
    affichage = affichage_mot(mot)
    tentatives = 0
    win = False
    trouvees = 0
    
    print("=== Jeu du Pendu ===\n")
    
    print(r"""     |
     O
     |
    \ /
     |
    / \ """)
    
    afficher_mot(affichage)
    
    while(tentatives <= 6 and not win) :
        
        print(" ")
        lettre = str(input("Choisissez une lettre : "))
        
        if verif_lettre(lettre, mot) == True :
            affichage = nouveau_affichage(affichage, mot, lettre)
            trouvees = lettres_trouvees(affichage)
            
        else :
            tentatives += 1
    
        if "_" not in affichage:
            win = True

        if not win:
            print(f"{tentatives}e tentative")
            print(" ")
            bonhomme(tentatives)
            print(" ")
            afficher_mot(affichage)
        
    print(" ")
    print(mot)
    print(" ")
    
    if win :
        print("Gagné!")
    else :
        print("Perdu..")
        
pendu()
