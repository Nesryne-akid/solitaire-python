from random import shuffle
import json
import os

# Fichier de sauvegarde, place dans le meme dossier que ce programme
FICHIER_SAUVEGARDE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sauvegarde_solitaire.json")


# ----------
# AFFICHAGE
# ----------

ROUGE = "\033[31m"
NOIR = "\033[30m"
FOND = "\033[47m"
RESET = "\033[0m"

LARGEUR = 4

CONVERSION = {1: 'A', 11: 'V', 12: 'D', 13: 'R'}


def affichage_val(valeur):
    if valeur in CONVERSION:
        return CONVERSION[valeur]
    return str(valeur)


def centrer(texte, LARGEUR = LARGEUR):
    return f"{texte:^{LARGEUR}}"


def carte_entiere(valeur, symbole, LARGEUR_INT = LARGEUR-2):
    if symbole in ['♥', '♦']:
        couleur = ROUGE
    else:
        couleur = NOIR
    carte = f"{affichage_val(valeur)}{symbole}"
    
    NO = f"{carte:<{LARGEUR_INT}}"
    SE = f"{carte:>{LARGEUR_INT}}"
    
    return [
        f"{FOND}{couleur}┌{'─' * LARGEUR_INT}┐{RESET}",
        f"{FOND}{couleur}│{NO}│{RESET}",
        f"{FOND}{couleur}│{' ' * LARGEUR_INT}│{RESET}",
        f"{FOND}{couleur}│{SE}│{RESET}",
        f"{FOND}{couleur}└{'─' * LARGEUR_INT}┘{RESET}"
    ]


def pioche_non_vide(LARGEUR_INT = LARGEUR - 2):
    return [
        f"{FOND}{NOIR}┌{'─' * LARGEUR_INT}┐{RESET}",
        f"{FOND}{NOIR}│{' ' * LARGEUR_INT}│{RESET}",
        f"{FOND}{NOIR}│{' ' * LARGEUR_INT}│{RESET}",
        f"{FOND}{NOIR}│{' ' * LARGEUR_INT}│{RESET}",
        f"{FOND}{NOIR}└{'─' * LARGEUR_INT}┘{RESET}"
    ]


def emplacement_vide(LARGEUR_INT = LARGEUR - 2):
    return [
        f"┌{'─' * LARGEUR_INT}┐",
        f"│{' ' * LARGEUR_INT}│",
        f"│{' ' * LARGEUR_INT}│",
        f"│{' ' * LARGEUR_INT}│",
        f"└{'─' * LARGEUR_INT}┘"
    ]


def bande_cachee(LARGEUR_INT = LARGEUR - 2):
    return f"┌{'─' * LARGEUR_INT}┐"


def bande_visible(valeur, symbole, LARGEUR_INT = LARGEUR - 2):
    if symbole in ['♥', '♦']:
        couleur = ROUGE 
    else: 
        couleur = NOIR
        
    carte = f"{affichage_val(valeur)}{symbole}"
    NO = f"{carte:<3}"
    return f"{FOND}{couleur}┌{NO}{'─' * (LARGEUR_INT - len(NO))}┐{RESET}"


def plateau(jeu):
    print(f"\n{'-' * (7 * (LARGEUR + 1))}\n")

    noms_part_sup = " ".join([
        centrer("P"),
        centrer("D"),
        " " * LARGEUR,
        centrer("F1"),
        centrer("F2"),
        centrer("F3"),
        centrer("F4")
    ])

    pioche = pioche_non_vide() if jeu['P'] else emplacement_vide()
    defausse = carte_entiere(jeu['D'][-1][0], jeu['D'][-1][1]) if jeu['D'] else emplacement_vide()

    fondations = []
    for place in ['F1', 'F2', 'F3', 'F4']:
        pile = jeu['F'][place]
        if pile:
            fondations.append(carte_entiere(pile[-1][0], pile[-1][1]))
        else:
            fondations.append(emplacement_vide())

    print(noms_part_sup)
    
    for strat in range(5):
        ligne = " ".join([
            pioche[strat],
            defausse[strat],
            " " * LARGEUR,
            fondations[0][strat],
            fondations[1][strat],
            fondations[2][strat],
            fondations[3][strat] 
        ])
        print(ligne)

    print("\n")

    noms_part_inf = " ".join([centrer(f"C{i}") for i in range(1, 8)])
    print(noms_part_inf)

    colonnes = []
    for col in jeu['C']:
        lignes = []
        if not col:
            lignes.extend(emplacement_vide())
        else:
            for carte in col[:-1]:
                val, symb, vis = carte
                if vis:
                    lignes.append(bande_visible(val, symb))
                else:
                    lignes.append(bande_cachee())
            
            der_val, der_symb, der_vis = col[-1]
            lignes.extend(carte_entiere(der_val, der_symb))
                
        colonnes.append(lignes)

    max_h = max(len(strat) for strat in colonnes)
    for niveau in range(max_h):
        ligne = []
        for col in range(7):
            strats = colonnes[col]
            if niveau < len(strats):
                ligne.append(strats[niveau])
            else:
                ligne.append(" " * LARGEUR)
        print(" ".join(ligne))

    print()


# --------------------------
# DEBUT DE PARTIE ALEATOIRE
# --------------------------

def creer_paquet():
    symboles = ['♥', '♦', '♣', '♠']
    paquet = []
    for s in symboles:
        for val in range(1, 14):
            paquet.append((val, s, False))
    return paquet


def initialiser_jeu():
    pioche = creer_paquet()
    shuffle(pioche)

    colonnes = []
    for col in range(7):
        nb_cartes = col + 1
        colonne = []
        for car in range(nb_cartes):
            val, symb, vis = pioche.pop()
            vis = (car == nb_cartes - 1)
            colonne.append((val, symb, vis))
        colonnes.append(colonne)

    jeu = {
        'P': pioche,
        'D': [],
        'F': {'F1': [], 'F2': [], 'F3': [], 'F4': []},
        'C': colonnes,
    }

    return jeu


# -------------
# MODES DE JEU
# -------------

rgl_classique = {
    'nom': 'Classique',
    'cartes_toutes_visibles': False,
    'roi_seul_sur_colonne_vide': True,
    'alterner_couleurs_colonne': True,
    'mode_libre': False,
}

rgl_deb = {
    'nom': 'Débutant',
    'cartes_toutes_visibles': True,
    'roi_seul_sur_colonne_vide': False,
    'alterner_couleurs_colonne': True,
    'mode_libre': False,
}

rgl_libre = {
    'nom': 'Libre',
    'cartes_toutes_visibles': False,
    'roi_seul_sur_colonne_vide': False,
    'alterner_couleurs_colonne': False,
    'mode_libre': True,
}


def mode_jeu():
    print('\nMODES DE JEU')
    print('1. Solitaire Classique')
    print("2. Mode Débutant (Toutes les cartes des colonnes sont visibles et une colonne peut commencer par n'importe quelle carte)")
    print('3. Mode Libre (Aucune contrainte sur les coups)')

    choix = input('Votre choix (1, 2 ou 3) : ').strip()

    if choix == '2':
        print('Mode Débutant activé !\n')
        return rgl_deb
    elif choix == '3':
        print('Mode Libre activé !\n')
        return rgl_libre
    else:
        print('Mode Classique activé !\n')
        return rgl_classique


def mode_visibilite(jeu):
    if jeu['regles']['cartes_toutes_visibles']:
        for c in jeu['C']:
            for i in range(len(c)):
                val, symb, _ = c[i]
                c[i] = (val, symb, True)


# --------------------
# SAISIES UTILISATEUR
# --------------------

valeurs_saisies = {
    '1': 1,
    'A': 1,
    'AS': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    '11': 11,
    'V': 11,
    'VALET': 11,
    '12': 12,
    'D': 12,
    'DAME': 12,
    '13': 13,
    'R': 13,
    'ROI': 13,
}

zones = [
    'P',
    'D',
    'F1',
    'F2',
    'F3',
    'F4',
    'C1',
    'C2',
    'C3',
    'C4',
    'C5',
    'C6',
    'C7',
]


def guide_commandes():
    print('GUIDE DES COMMANDES DE JEU :\n')
    print('  P             : Piocher une carte (de la Pioche P vers la Défausse D)')
    print('  D C2          : Déplacer la carte de la Défausse vers la colonne C2')
    print('  D F1          : Déplacer la carte de la Défausse vers la Fondation F1')
    print('  C1 C3         : Déplacer toute la suite visible de C1 vers C3')
    print('  C1 C3 10      : Déplacer la suite de C1 vers C3 à partir du 10 (ou V, D, R, A)')
    print('  F1 C2         : Reposer une carte d\'une Fondation vers une Colonne')
    print('  AIDE          : Proposer les meilleurs coups possibles')
    print('  ANNULER       : Annuler le dernier coup')
    print('  SAUVER        : Enregistrer la partie en cours sur l\'ordinateur')
    print('  GUIDE         : Réafficher ce guide des commandes')
    print('  QUITTER       : Quitter la partie\n')


def analyser_valeur(texte):
    return valeurs_saisies.get(texte.upper(), None)


def lire_commande():
    # Renvoie toujours un triplet : (type_action, parametres, message_erreur)

    saisie = input('\nVotre coup : ').strip().upper()
    mots = saisie.split()

    if not mots:
        return 'PIOCHER', None, None

    if len(mots) == 1:
        if mots[0] == 'P':
            return 'PIOCHER', None, None
        elif mots[0] in ['GUIDE']:
            return 'GUIDE', None, None
        elif mots[0] in ['AIDE']:
            return 'AIDE', None, None
        elif mots[0] in ['ANNULER']:
            return 'ANNULER', None, None
        elif mots[0] in ['SAUVER']:
            return 'SAUVER', None, None
        elif mots[0] in ['QUITTER']:
            return 'QUITTER', None, None
        else:
            return (None, None, f"Commande '{mots[0]}' inconnue. Tapez 'GUIDE' pour afficher le guide des commandes.")

    if len(mots) in [2, 3]:
        src = mots[0]
        dest = mots[1]
        
        if src == 'P':
            return (None, None, "Vous vouliez sûrement sélectionner la carte de la défausse (D)")

        if src not in zones:
            return (None, None, f"Zone source '{src}' invalide ! (Zones : P, D, F1..F4, C1..C7)")
        if dest not in zones or dest == 'P' or dest == 'D':
            return (None, None, f"Zone destination '{dest}' invalide ! (Zones : F1..F4, C1..C7)")
        if src == dest:
            return (None, None, 'La zone de départ et de destination doivent être différentes !')

        val_depart = None
        if len(mots) == 3:
            val_depart = analyser_valeur(mots[2])
            if val_depart is None:
                return (None, None, f"Valeur de carte '{mots[2]}' invalide !")

        return 'DEPLACER', (src, dest, val_depart), None

    return (None, None, "Format invalide ! Tapez 'GUIDE' pour voir les exemples de commandes.")


def piocher(jeu):

    if not jeu["P"] and jeu["D"]:
        nvl_pioche = []

        for i in range(len(jeu["D"]) - 1, -1, -1):
            val, symb, _ = jeu["D"][i]
            nvl_pioche.append((val, symb, False))

        jeu["P"] = nvl_pioche
        jeu["D"] = []

    if jeu["P"]:
        val, symb, vis = jeu["P"].pop()
        jeu["D"].append((val, symb, True))
    else:
        print("Il n'y a plus de carte à piocher...")

    return jeu


def deplacer(jeu, src, dest, val_depart=None):

    a_deplacer = []

    if src == "D":
        a_deplacer.append(jeu["D"].pop())

    elif src.startswith("F"):
        a_deplacer.append(jeu["F"][src].pop())

    elif src.startswith("C"):
        i_s = int(src[1]) - 1
        col_s = jeu["C"][i_s]
        pos = -1
        
        if val_depart != None:
            i = len(col_s) - 1
            while i >= 0 and pos == -1:
                val, symb, vis = col_s[i]
                if vis and val == val_depart:
                    pos = i
                i -= 1
        else:
            i = 0
            while i < len(col_s) and pos == -1:
                val, symb, vis = col_s[i]
                if vis:
                    pos = i
                i += 1

        if pos != -1:
            a_deplacer = col_s[pos:]
            jeu["C"][i_s] = col_s[:pos]

            # On retourne la nouvelle derniere carte de la colonne source
            if jeu["C"][i_s]:
                v, s, vis = jeu["C"][i_s][-1]
                jeu["C"][i_s][-1] = (v, s, True)

    if dest.startswith("F"):
        for carte in a_deplacer:
            jeu["F"][dest].append(carte)

    elif dest.startswith("C"):
        i_d = int(dest[1:]) - 1
        for carte in a_deplacer:
            jeu["C"][i_d].append(carte)

    return jeu


def est_rouge(symbole):
    return symbole in ["♥", "♦"]


def coup_valide(jeu, src, dest, val_depart=None):
    # Renvoie toujours un couple : (coup_autorise, message)

    regles = jeu["regles"]

    if src == "D":
        if not jeu["D"]:
            return False, "Il n'y a pas de carte à prendre dans la défausse..."
        carte_src = jeu["D"][-1]

    elif src.startswith("F"):
        if not jeu["F"][src]:
            return False, f"Il n'y a pas de carte à prendre dans la fondation {src}..."
        carte_src = jeu["F"][src][-1]

    elif src.startswith("C"):
        i_s = int(src[1]) - 1
        col_s = jeu["C"][i_s]
        if not col_s:
            return False, f"Il n'y a pas de carte à prendre dans la colonne {src}..."

        carte_src = None
        if val_depart != None:
            i = len(col_s) - 1
            while i >= 0 and carte_src == None:
                val, symb, vis = col_s[i]
                if vis and val == val_depart:
                    carte_src = (val, symb, vis)
                i -= 1

            if carte_src == None:
                return False, f"La carte {affichage_val(val_depart)} n'est pas visible dans {src}."

        else:
            i = 0
            while i < len(col_s) and carte_src is None:
                val, symb, vis = col_s[i]
                if vis:
                    carte_src = (val, symb, vis)
                i += 1

    val_s, symb_s, vis_s = carte_src

    if dest.startswith("F"):

        if src.startswith("C") and carte_src != col_s[-1]:
            return False, "Il ne peut y avoir qu'une carte à déplacer vers une fondation..."

        pile_f = jeu["F"][dest]
        if not pile_f:
            if val_s == 1:
                return True, ""
            return False, "Une fondation commence toujours par un As..."
        else:
            val_f, symb_f, vis_f = pile_f[-1]
            if symb_s == symb_f and val_s == val_f + 1:
                return True, ""
            return False, f"Sur {dest}, vous devez poser le {affichage_val(val_f + 1)}{symb_f}..."

    if dest.startswith("C"):
        i_d = int(dest[1]) - 1
        col_d = jeu["C"][i_d]

        if not col_d:
            if regles["roi_seul_sur_colonne_vide"] and val_s != 13:
                return False, "Une colonne vide ne peut commencer que par un Roi..."
            return True, ""

        val_d, symb_d, vis_d = col_d[-1]

        if not regles["mode_libre"]:
            if val_s != val_d - 1:
                return False, f"Il ne peut y avoir qu'un {affichage_val(val_d - 1)} sur un {affichage_val(val_d)}..."
    
            if regles["alterner_couleurs_colonne"]:
                if est_rouge(symb_s) == est_rouge(symb_d):
                    return False, "Il faut alterner les couleurs..."

    return True, ""


def est_gagne(jeu):
    # La partie est gagnee quand la pioche et la defausse sont vides
    # et que toutes les cartes des colonnes sont retournees

    if jeu["P"] or jeu["D"]:
        return False

    for col in jeu["C"]:
        for val, symb, vis in col:
            if not vis:
                return False

    return True


# ---------------------
# ANNULATION D'UN COUP
# ---------------------

def copier_jeu(jeu):
    # Copie independante du jeu : les cartes sont des tuples (non modifiables),
    # il suffit donc de recopier chaque liste pour ne pas partager les memes listes
    copie = {
        'P': jeu['P'][:],
        'D': jeu['D'][:],
        'F': {},
        'C': [],
        'regles': jeu['regles'],
    }
    for place in ['F1', 'F2', 'F3', 'F4']:
        copie['F'][place] = jeu['F'][place][:]
    for col in jeu['C']:
        copie['C'].append(col[:])
    return copie


# ----------------------------
# SAUVEGARDE ET CHARGEMENT
# ----------------------------

def sauvegarder(jeu):
    # JSON ne connait pas les tuples : il les enregistre comme des listes
    with open(FICHIER_SAUVEGARDE, 'w', encoding='utf-8') as fichier:
        json.dump(jeu, fichier, ensure_ascii=False)
    print(f"Partie enregistrée dans : {FICHIER_SAUVEGARDE}")


def liste_en_cartes(liste):
    # Retransforme les cartes lues dans le fichier en tuples (valeur, symbole, visible)
    cartes = []
    for carte in liste:
        cartes.append(tuple(carte))
    return cartes


def charger():
    with open(FICHIER_SAUVEGARDE, 'r', encoding='utf-8') as fichier:
        donnees = json.load(fichier)

    jeu = {
        'P': liste_en_cartes(donnees['P']),
        'D': liste_en_cartes(donnees['D']),
        'F': {},
        'C': [],
        'regles': donnees['regles'],
    }
    for place in ['F1', 'F2', 'F3', 'F4']:
        jeu['F'][place] = liste_en_cartes(donnees['F'][place])
    for col in donnees['C']:
        jeu['C'].append(liste_en_cartes(col))
    return jeu


def proposer_reprise():
    # Si une sauvegarde existe, on propose de la reprendre ; sinon on renvoie None
    if not os.path.exists(FICHIER_SAUVEGARDE):
        return None

    choix = input('Une partie sauvegardée existe. La reprendre ? (O/N) : ').strip().upper()
    if choix == 'O':
        try:
            jeu = charger()
            print(f"Partie reprise (mode {jeu['regles']['nom']}) !\n")
            return jeu
        except (OSError, ValueError, KeyError):
            print('La sauvegarde est illisible, une nouvelle partie va commencer.\n')
    return None


# --------------------------
# AIDE : PROPOSER DES COUPS
# --------------------------

def coups_possibles(jeu):
    # Teste tous les deplacements avec coup_valide et note chacun :
    #   3 = vers une fondation, 2 = retourne une carte cachee,
    #   1 = depuis la defausse,  0 = autre coup autorise
    destinations = ['F1', 'F2', 'F3', 'F4', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7']
    coups = []

    # Coups depuis la defausse
    if jeu['D']:
        for dest in destinations:
            valide, _ = coup_valide(jeu, 'D', dest)
            if valide:
                if dest.startswith('F'):
                    coups.append((3, f"D {dest}"))
                else:
                    coups.append((1, f"D {dest}"))

    # Coups depuis les colonnes : on essaie de partir de chaque carte visible
    for i in range(7):
        src = f"C{i + 1}"
        col_s = jeu['C'][i]
        for pos in range(len(col_s)):
            val, symb, vis = col_s[pos]
            if vis:
                for dest in destinations:
                    if dest != src:
                        valide, _ = coup_valide(jeu, src, dest, val)
                        # Deplacer toute une colonne vers une colonne vide ne sert a rien
                        inutile = (pos == 0 and dest.startswith('C') and not jeu['C'][int(dest[1]) - 1])
                        if valide and not inutile:
                            commande = f"{src} {dest} {affichage_val(val)}"
                            if dest.startswith('F'):
                                coups.append((3, commande))
                            elif pos > 0 and not col_s[pos - 1][2]:
                                coups.append((2, commande))
                            else:
                                coups.append((0, commande))

    # Les meilleurs coups en premier
    coups.sort(reverse=True)
    return coups


def aide(jeu):
    coups = coups_possibles(jeu)
    if not coups:
        if jeu['P'] or jeu['D']:
            print('Aucun déplacement possible : piochez une carte (P).')
        else:
            print('Aucun coup possible...')
        return

    explications = {
        3: 'monte une carte sur une fondation',
        2: 'retourne une carte cachée',
        1: 'libère la défausse',
        0: 'déplacement possible',
    }
    print('Coups conseillés :')
    for score, commande in coups[:3]:
        print(f"  {commande:<12} -> {explications[score]}")


# -------------------------
# BOUCLE PRINCIPALE DU JEU
# -------------------------


def jouer():
    print('BIENVENUE DANS LE JEU DU SOLITAIRE !\n')

    jeu = proposer_reprise()
    if jeu is None:
        regles = mode_jeu()
        jeu = initialiser_jeu()
        jeu['regles'] = regles
        mode_visibilite(jeu)

    guide_commandes()

    historique = []     # pile des etats precedents, pour ANNULER

    while True:
        plateau(jeu)

        if est_gagne(jeu):
            print("\nFÉLICITATIONS ! Vous avez gagné la partie !")
            # La partie est finie : on supprime la sauvegarde pour ne pas la reprendre
            if os.path.exists(FICHIER_SAUVEGARDE):
                os.remove(FICHIER_SAUVEGARDE)
            break

        action, para, erreur = lire_commande()

        if erreur:
            print(f'{erreur}')
            continue

        if action == 'GUIDE':
            guide_commandes()

        elif action == 'AIDE':
            aide(jeu)

        elif action == 'SAUVER':
            sauvegarder(jeu)

        elif action == 'ANNULER':
            if historique:
                jeu = historique.pop()
                print('Dernier coup annulé.')
            else:
                print('Aucun coup à annuler.')

        elif action == 'QUITTER':
            choix = input('Enregistrer la partie avant de quitter ? (O/N) : ').strip().upper()
            if choix == 'O':
                sauvegarder(jeu)
            print('\nMerci d\'avoir joué ! À bientôt.')
            break

        elif action == "PIOCHER":
            historique.append(copier_jeu(jeu))
            jeu = piocher(jeu)

        elif action == 'DEPLACER':
            src, dest, val_depart = para

            valide, message = coup_valide(jeu, src, dest, val_depart)
            if valide:
                historique.append(copier_jeu(jeu))
                jeu = deplacer(jeu, src, dest, val_depart)
            else:
                print(f"\nCe déplacement n'est pas autorisé : {message}")


if __name__ == "__main__":
    jouer()
