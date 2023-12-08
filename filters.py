import menu
import random
import pandas as pd
import ast
import rich
from rich import print

def menu_filters(username, df):
    print('  Navigueur dans les films ----------- [1]')
    print('  Filtrer par genre------------------- [2]')
    print('  Filtrer par durée ------------------ [3]')
    print('  Filtrer par pays ------------------- [4]')
    print('  Retour menu principal -------------- [5]')
    print('\n')
    set_choice(username, df, input('  Choix du menu : '))

def set_choice(username, df, choice):
    if(choice.isnumeric() and choice in ['1', '2', '3', '4','5']):
        match choice:
            case '1':
                afficheFilm(df)
            case '2':
                choisir_genre(df)
            case '3':
                choisir_duree(df)
            case '4':
                choisir_pays(df)
            case '5':
                menu.display_menu(df)
    else:
        print('\n Il faut choisir parmi les options proposées.\n')
        menu_filters(username, df)

def afficheFilm(df):
    df_film = df['title']
    # Position initiale
    current_position = 0
    while True:
        # Afficher les 5 lignes à partir de la position actuelle
        group = df_film.iloc[current_position:current_position + 5]
        print('')
        for i, x in group.items():
            print('  > ' + x)
        print('')

        # Demander à l'utilisateur d'entrer "+", "-", ou "q"
        user_input = input("Entrez '+' pour afficher les 5 suivants, '-' pour afficher les 5 précédents, ou 'q' pour quitter: ")

        if user_input == '+':
            current_position += 5
        elif user_input == '-':
            current_position -= 5
            if current_position < 0:
                current_position = 0
        elif user_input == 'q':
            break
        else:
            print("Entrée non valide. Veuillez entrer '+', '-', ou 'q'.")



# Fonction pour extraire l'id et les valeurs de la clé 'name'
def extract_names(row):
    genre_list = row['genres']
    id_value = row['id']
    
    # Utilise une liste en compréhension pour extraire les valeurs 'name'
    names = [genre['name'] for genre in genre_list]
    
    return id_value, names

def choisir_genre(df):
    df_genres = pd.DataFrame({
        'id': df['id'],
        'genres': df['genres']
    })
    
    # Appliquation de la fonction à chaque ligne du DataFrame
    result = df_genres.apply(extract_names, axis=1, result_type='expand')
    result.columns = ['id', 'genre_names']

    # On affiche le résultat
    print(result)

def choisir_duree(df):
    df_runtime = pd.DataFrame({
        'id': df['id'],
        'runtime': df['runtime']
    })

    print('  Entre 0h et 1h ---------------------------- [1]')
    print('  Entre 1h et 1h30 -------------------------- [2]')
    print('  Entre 1h30 et 2h -------------------------- [3]')
    print('  2h et plus long --------------------------- [4]')
    print('\n')
    choice_runtime(df_runtime, input('  Choix de la durée : '))

def choisir_pays(df):
    df_pays = pd.DataFrame({
    'id': df['id'],
    'pays': df['production_countries']
    })
    # Convertir la colonne 'pays' en listes de dictionnaires
    df_pays['pays'] = df_pays['pays'].apply(ast.literal_eval)
    # Utilisation de apply pour extraire l'id et la valeur de la première clé 'iso_3166_1'
    df_pays[['id', 'iso_3166_1']] = df_pays.apply(lambda row: pd.Series([row['id'], row['pays'][0]['iso_3166_1']] if row['pays'] and 'iso_3166_1' in row['pays'][0] else [row['id'], None]), axis=1)
    # On affiche le résultat
    print(df_pays[['id', 'iso_3166_1']])



def choice_runtime(df_runtime, choice):
    if(choice.isnumeric() and choice in ['1', '2', '3', '4']):
        match choice:
            case '1':
                # Pour 0 à 1h
                # Filtrer les valeurs en fonction de la condition (runtime inférieur à 60)
                valeurs_filtrées = [(id_val, runtime_val) for id_val, runtime_val in zip(df_runtime['id'], df_runtime['runtime']) if runtime_val < 60]
                # Sélectionner aléatoirement 5 ids parmi les résultats filtrés
                valeurs_aleatoires = random.sample(valeurs_filtrées, 5)
                # Afficher les résultats
                print("Valeurs aléatoires dans la colonne 'id' avec un 'runtime' inférieur à 60 :")
                for id_val, runtime_val in valeurs_aleatoires:
                    print(f"id: {id_val}, runtime: {runtime_val}")

            case '2':
                # Pour 1h à 1h30
                # Filtrer les valeurs en fonction de la condition (runtime supérieur à 60 et inférieur à 90 )
                valeurs_filtrées = [(id_val, runtime_val) for id_val, runtime_val in zip(df_runtime['id'], df_runtime['runtime']) if runtime_val > 60 and runtime_val < 90]
                # Sélectionner aléatoirement 5 ids parmi les résultats filtrés
                valeurs_aleatoires = random.sample(valeurs_filtrées, 5)
                # Afficher les résultats
                print("Valeurs aléatoires dans la colonne 'id' avec un 'runtime' supérieur à 60 et inférieur à 90 :")
                for id_val, runtime_val in valeurs_aleatoires:
                    print(f"id: {id_val}, runtime: {runtime_val}")

            case '3':
                # Pour 1h30 à 2h
                # Filtrer les valeurs en fonction de la condition (runtime supérieur à 90 et inférieur à 120)
                valeurs_filtrées = [(id_val, runtime_val) for id_val, runtime_val in zip(df_runtime['id'], df_runtime['runtime']) if runtime_val > 90 and runtime_val < 120]
                # Sélectionner aléatoirement 5 ids parmi les résultats filtrés
                valeurs_aleatoires = random.sample(valeurs_filtrées, 5)
                # Afficher les résultats
                print("Valeurs aléatoires dans la colonne 'id' avec un 'runtime' supérieur à 90 et inférieur à 120 :")
                for id_val, runtime_val in valeurs_aleatoires:
                    print(f"id: {id_val}, runtime: {runtime_val}")

            case '4':
                # Pour 2h+
                # Filtrer les valeurs en fonction de la condition (runtime supérieur à 120)
                valeurs_filtrées = [(id_val, runtime_val) for id_val, runtime_val in zip(df_runtime['id'], df_runtime['runtime']) if runtime_val > 120]
                # Sélectionner aléatoirement 5 ids parmi les résultats filtrés
                valeurs_aleatoires = random.sample(valeurs_filtrées, 5)
                # Afficher les résultats
                print("Valeurs aléatoires dans la colonne 'id' avec un 'runtime' supérieur à 120 :")
                for id_val, runtime_val in valeurs_aleatoires:
                    print(f"id: {id_val}, runtime: {runtime_val}")

    else:
        print('\n Il faut choisir parmi les options proposées.\n')