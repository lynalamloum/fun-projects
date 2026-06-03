# To Do List
 
> A command-line task manager built in Python.  
> Une application de gestion de tâches en ligne de commande, développée en Python.
 
---
 
## Features / Fonctionnalités
 
- Display all tasks with their status, date and priority / Afficher toutes les tâches avec leur statut, date et priorité
- Add a task with a priority level / Ajouter une tâche avec un niveau de priorité (Haute / Moyenne / Basse)
- Mark a task as done / Marquer une tâche comme faite
- Delete a task with confirmation / Supprimer une tâche avec confirmation
- Auto-save to a JSON file / Sauvegarde automatique dans un fichier JSON
---
 
## Requirements / Prérequis
 
- Python 3.x
---
 
## Getting started / Lancement
 
```bash
python todo.py
```
 
---
 
## Usage / Utilisation
 
```
=== TO DO LIST ===
1. Afficher les tâches
2. Ajouter une tâche
3. Marquer comme faite
4. Supprimer une tâche
5. Quitter
```
 
Tasks are automatically saved in a `tasks.json` file created on first launch.  
Les tâches sont sauvegardées automatiquement dans un fichier `tasks.json` créé au premier lancement.
 
---
 
## Task structure / Structure d'une tâche
 
```json
{
  "id": 1,
  "tache": "Apprendre Python",
  "fait": false,
  "date": "06/03/26",
  "priorité": "!!!"
}
```
 
---
 
## Author / Auteur
 
Projet réalisé dans le cadre d'un apprentissage personnel de Python.  
Personal Python learning project.
