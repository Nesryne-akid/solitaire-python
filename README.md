# 🃏 Solitaire en Python

Jeu de Solitaire (Klondike) jouable dans le terminal, développé en Python dans le cadre du cours *Algorithmique et programmation Python* (L3 MIAGE, Université Toulouse 1 Capitole).

## ✨ Fonctionnalités
- **Affichage des cartes en couleur** directement dans le terminal (cœurs et carreaux en rouge)
- **3 modes de jeu** : Classique, Débutant (toutes les cartes visibles) et Libre (aucune contrainte)
- **Vérification des coups** avec un message qui explique pourquoi un coup est refusé
- **`AIDE`** : un algorithme teste tous les coups possibles et propose les 3 meilleurs
- **`ANNULER`** : retour au coup précédent, autant de fois que souhaité
- **`SAUVER`** : enregistrement de la partie en cours dans un fichier JSON, reprise au lancement suivant

## ▶️ Lancer le jeu
Python 3 suffit, aucune bibliothèque à installer.

```bash
python3 solitaire.py
```

## 🎮 Commandes
| Commande | Action |
|---|---|
| `P` | Piocher une carte |
| `D C2` | Déplacer la carte de la défausse vers la colonne C2 |
| `D F1` | Déplacer la carte de la défausse vers la fondation F1 |
| `C1 C3` | Déplacer toute la suite visible de C1 vers C3 |
| `C1 C3 10` | Déplacer la suite de C1 vers C3 à partir du 10 (ou V, D, R, A) |
| `F1 C2` | Reposer une carte d'une fondation vers une colonne |
| `AIDE` | Proposer les meilleurs coups |
| `ANNULER` | Annuler le dernier coup |
| `SAUVER` | Enregistrer la partie |
| `GUIDE` | Afficher le guide des commandes |
| `QUITTER` | Quitter (avec proposition de sauvegarde) |

## 🧠 Choix techniques
- **Représentation du jeu** : un dictionnaire (`P` pioche, `D` défausse, `F` fondations, `C` colonnes), chaque carte étant un tuple `(valeur, symbole, visible)`.
- **Règles paramétrables** : chaque mode de jeu est un dictionnaire de règles, ce qui permet d'ajouter un mode sans modifier la logique du jeu.
- **Annulation** : une pile d'états du jeu, copiés avant chaque coup.
- **Aide** : chaque coup autorisé par `coup_valide` reçoit une note (fondation > carte cachée retournée > défausse), puis les coups sont triés.

## 📌 Évolutions
Les fonctionnalités `AIDE`, `ANNULER` et `SAUVER` ont été ajoutées après le projet de cours.
