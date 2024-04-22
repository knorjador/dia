
import os
import pandas as pd
import menu

from collections import Counter
from dotenv import load_dotenv

load_dotenv()

PATH_CSV_MOVIES_METADATA = os.getenv('PATH_CSV_MOVIES_METADATA')
PATH_CSV_USERS = os.getenv('PATH_CSV_USERS')

def menu_users(username, df):
    print('')
    print('  Mes statistiques ------------------------- [1]')
    print('  Supprimer mes données -------------------- [2]')
    print('  Retour menu principal  ------------------- [3]')
    print('')
    set_choice(username, df, input('  Choix du menu : '))

def set_choice(username, df, choice):
    if (choice.isnumeric() and choice in ['1', '2', '3']):
        match choice:
            case '1':
                lecture_researches(username)
            case '2':
                delete_user_data(username)
            case '3':
                menu.display_menu(username, df)

        print('')
        user_input = input("  Voulez-vous retourner à votre compte ? (oui/non) ")
        if user_input.lower() == 'oui':
            menu_users(username, df)
            return
        else:
            quit_input = input("  Voulez-vous quitter le logiciel ? (oui/non) ")
            if quit_input.lower() == 'oui':
                print('\n  À bientôt ' + username +  '\n')
                exit(1)
            else:
                menu.display_menu(username, df)
                return
    else:
        print('\n Il faut choisir parmi les options proposées.\n')
        menu_users(username, df)

def lecture_researches(username):
    # Charger le fichier CSV des utilisateurs
    df_users = pd.read_csv(PATH_CSV_USERS)

    # Rechercher l'utilisateur par son nom d'utilisateur
    user_row = df_users[df_users['username'] == username]
    user_connections = user_row.iloc[0]['connections']

    # Vérifier si l'utilisateur a été trouvé
    if not user_row.empty:
        # Extraire la liste de recherches de l'utilisateur
        researches_list = eval(user_row.iloc[0]['researches'])
        df_movies = pd.read_csv(PATH_CSV_MOVIES_METADATA)

        # Initialiser des listes pour stocker les résultats
        resultat_genres = []
        resultat_runtime = []  # Pour stocker les 'runtime'
        resultat_pays = []  # Pour stocker les 'production_countries'

        # Parcourir la liste de recherches
        for numero in researches_list:
            # Rechercher la ligne correspondante dans la colonne 'id' du fichier movies_metadata.csv
            ligne = df_movies[df_movies['id'] == numero]

            # Vérifier si une ligne correspondante a été trouvée
            if not ligne.empty:
                # Extraire le genre de la colonne 'genres' et l'ajouter à la liste 'resultat_genres'
                genre = ligne['genres'].values[0]
                resultat_genres.append(genre)

                # Ajouter la valeur de 'runtime' à resultat_runtime
                resultat_runtime.append(ligne['runtime'].values[0])

                # Ajouter la valeur de 'production_countries' à resultat_pays
                resultat_pays.append(ligne['production_countries'].values[0])
            else:
                resultat_genres.append(0)  # Ajouter une valeur par défaut si aucune correspondance n'est trouvée
                resultat_runtime.append(0)
                resultat_pays.append(0)

        # Calculer la moyenne des 'runtime' et convertir en heures
        moyenne_runtime_minutes = sum(resultat_runtime) / len(resultat_runtime) if resultat_runtime and len(resultat_runtime) > 0 else 0
        moyenne_runtime_heures = convertir_minutes_en_heures(moyenne_runtime_minutes)

        return display_user_stats(username, user_connections, resultat_genres, moyenne_runtime_heures, resultat_pays)
    else:
        print(f"Utilisateur {username} non trouvé.")

def display_user_stats(username, user_connections, resultat_genres, moyenne_runtime_heures, resultat_pays):
    print('')
    print('  ' + username + ', voici tes statistiques :')
    print('')
    print('  * Nombre de connexion(s) : ' + str(user_connections))
    print('')
    print('  * Tes tendances préférées : ')


    # Utiliser la fonction extraire_genres avec la variable resultat_genres
    noms_genres_extraits = [genre for sublist in [extraire_genres(str(chaine)) for chaine in resultat_genres] for genre in sublist]

    # Ajouter le bout de code pour calculer l'occurrence en pourcentage des genres
    resultats_genres = pourcentage_occurrence(noms_genres_extraits)

    # Trier par ordre décroissant
    resultats_genres_tries = sorted(resultats_genres, key=lambda x: x['pourcentage'], reverse=True)

    # Affichage des tendances par genre
    print('')
    print('    - Par genre :')
    print('')
    for i, resultat_genre in enumerate(resultats_genres_tries[:len(resultats_genres_tries)]):
        print(f"        {resultat_genre['item']}: {resultat_genre['pourcentage']:.2f}%")
    print('')

    # print(resultat_pays)
    # Utiliser la fonction extraire_pays avec la variable resultat_pays
    noms_pays_extraits = extraire_pays(resultat_pays)

    # Ajouter le bout de code pour calculer l'occurrence en pourcentage des pays
    resultats_pays = pourcentage_occurrence(noms_pays_extraits)

    # Tri des résultats par ordre décroissant des pourcentages
    resultats_pays_tries = sorted(resultats_pays, key=lambda x: x['pourcentage'], reverse=True)

    # Affichage des tendances par pays
    print('    - Par pays :')
    print('')
    for i, resultat_pays in enumerate(resultats_pays_tries[:len(resultats_pays_tries)]):
        print(f"        {resultat_pays['item']}: {resultat_pays['pourcentage']:.2f}%")
    print('')

    # Affichage durée moyenne
    print('  * Durée moyenne des films visionnés : ' + moyenne_runtime_heures)
    print('')


def convertir_minutes_en_heures(minutes):
    heures = round(minutes // 60)
    minutes_restes = int(minutes % 60)
    return f"{heures}h{minutes_restes:02d}"

def pourcentage_occurrence(data):
    total = len(data)
    compteur = Counter(data)

    pourcentages = [
        {'item': item, 'pourcentage': (occurrences / total) * 100}
        for item, occurrences in compteur.items()
    ]

    return pourcentages

def extraire_genres(chaine_caractere):
    # Supprimer les crochets et les accolades
    chaine_caractere = chaine_caractere.replace("[", "").replace("]", "").replace("{", "").replace("}", "")

    # Diviser la chaîne en une liste de paires clé-valeur
    paires = [pair.strip() for pair in chaine_caractere.split(',')]

    # Extraire les valeurs associées à la clé 'name'
    noms_genres = [pair.split(':')[-1].strip().strip("'") for pair in paires if 'name' in pair]

    return noms_genres

def extraire_pays(dictionnaires_liste):
    # Liste pour stocker les noms de pays extraits
    noms_pays = []
 
    # Parcourir chaque dictionnaire dans la liste
    for dictionnaire in dictionnaires_liste:
        # Extraire la valeur associée à la clé 'name'
        if (type(dictionnaire) != int):
            nom_pays = [item['name'] for item in eval(dictionnaire)]
            noms_pays.extend(nom_pays)

    return noms_pays

def delete_user_data(username):
    df = pd.read_csv(PATH_CSV_USERS)
    df.drop(df[df['username'] == username].index, inplace = True)
    df.to_csv(PATH_CSV_USERS, mode='w', index=False, header=True)

    print('')
    print('  Au revoir ' + username + ', vos données ont bien été supprimées.')
    print('')
    exit(1)