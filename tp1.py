# ANALYSEUR D’INSCRIPTIONS, DE NOTES ET DE COHERENCE

# DONNEES
donnees = [
    ("Sara", "Math", 12, "G1"),
    ("Sara", "Info", 14, "G1"),
    ("Ahmed", "Math", 9, "G2"),
    ("Adam", "Chimie", 18, "G1"),
    ("Sara", "Math", 11, "G1"),
    ("Bouchra", "Info", "abc", "G2"),
    ("", "Math", 10, "G1"),
    ("Yassine", "Info", 22, "G2"),
    ("Ahmed", "Info", 13, "G2"),
    ("Adam", "Math", None, "G1"),
    ("Sara", "Chimie", 16, "G1"),
    ("Adam", "Info", 7, "G1"),
    ("Ahmed", "Math", 9, "G2"),
    ("Hana", "Physique", 15, "G3"),
    ("Hana", "Math", 8, "G3"),
]

# PARTIE 1 : VALIDATION
def valider(enregistrement):
    nom, matiere, note, groupe = enregistrement

    if not nom:
        return False, "Nom vide"

    if not matiere:
        return False, "Matière vide"

    if not groupe:
        return False, "Groupe vide"

    if not isinstance(note, (int, float)):
        return False, "Note non numérique"

    if note < 0 or note > 20:
        return False, "Note hors intervalle"

    return True, ""

# PARTIE 2 : STRUCTURATION
def somme_recursive(liste):
    if not liste:
        return 0
    return liste[0] + somme_recursive(liste[1:])


def moyenne(liste):
    if not liste:
        return 0
    return somme_recursive(liste) / len(liste)



valides = []
erreurs = []
doublons_exact = set()
vus = set()

#Nettoyage
for ligne in donnees:

    if ligne in vus:
        doublons_exact.add(ligne)
        continue

    vus.add(ligne)

    ok, raison = valider(ligne)

    if ok:
        nom, matiere, note, groupe = ligne
        valides.append((nom, matiere, float(note), groupe))
    else:
        erreurs.append({"ligne": ligne, "raison": raison})


#Matières distinctes
matieres = set()

for nom, matiere, note, groupe in valides:
    matieres.add(matiere)


#Organisation par étudiant 
etudiants = {}

for nom, matiere, note, groupe in valides:

    if nom not in etudiants:
        etudiants[nom] = {}

    if matiere not in etudiants[nom]:
        etudiants[nom][matiere] = []

    etudiants[nom][matiere].append(note)


# Moyennes des étudiants
moyennes_etudiants = {}

for nom in etudiants:

    toutes_notes = []

    for matiere in etudiants[nom]:
        notes = etudiants[nom][matiere]
        moy = moyenne(notes)

        etudiants[nom][matiere] = {
            "notes": notes,
            "moyenne": moy
        }

        toutes_notes.extend(notes)

    moyennes_etudiants[nom] = moyenne(toutes_notes)


# PARTIE 4 : ALERTES
alertes = {
    "doublons_matiere": [],
    "profil_incomplet": [],
    "ecart_eleve": []
}


# Plusieurs notes même matière
for nom in etudiants:
    for matiere in etudiants[nom]:
        if len(etudiants[nom][matiere]["notes"]) > 1:
            alertes["doublons_matiere"].append((nom, matiere))


# Profil incomplet
for nom in etudiants:
    if len(etudiants[nom]) < len(matieres):
        alertes["profil_incomplet"].append(nom)

# Ecart élevé
for nom in etudiants:

    toutes_notes = []

    for matiere in etudiants[nom]:
        toutes_notes.extend(etudiants[nom][matiere]["notes"])

    if max(toutes_notes) - min(toutes_notes) > 10:
        alertes["ecart_eleve"].append(nom)

# AFFICHAGE FINAL
print("Etudiants :", etudiants)
print("Erreurs :", erreurs)
print("Doublons exacts :", doublons_exact)
print("Alertes :", alertes)