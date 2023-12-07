import pandas as pd
import sys
import menu
import random

# def load_data():
#     csv_credits = pd.read_csv('C:/Users/meuni/Desktop/Projet/nfhaart/data/credits.csv')
#     csv_movies_metadata = pd.read_csv('C:/Users/meuni/Desktop/Projet/nfhaart/data/movies_metadata.csv')
#     df_credits = pd.DataFrame(csv_credits)
#     df_movies_metadata = pd.DataFrame(csv_movies_metadata)
#     df_credits['id'] = df_credits['id'].astype('int64')
#     df_movies_metadata['id'] = df_movies_metadata['id'].astype('int64')
#     return pd.merge(df_movies_metadata, df_credits, on="id")

def menu_principal(username, df):
    menu.display_menu(username, df)

def menu_researches(username, df):
    print('')
    print('  Genre ------------------------------ [1]')
    print('  Durée------------------------------- [2]')
    print('  Acteur ----------------------------- [3]')
    print('  Langue ----------------------------- [4]')
    print('  Recherche combinée ----------------- [5]')
    print('  Retour menu principal -------------- [6]')
    print('\n')
    set_choice(username, df, input('  Recherche par : '))
    

def set_choice(username, df, choice):
    while True:
        if choice.isnumeric() and choice in ['1', '2', '3', '4', '5', '6']:
            match choice:
                case '1':
                    result = search_movies(df, genre=get_genre(df))
                case '2':
                    result = search_movies(df, duration=get_duration(df))
                case '3':
                    result = search_movies(df, actor=get_actor(df))
                case '4':
                    result = search_movies(df, language=get_language(df))
                case '5':
                    result = search_combined_movies(df)
                case '6':
                    menu_principal(username, df)
                    return

            if result is not None and not result.empty:
                movies_ids = result['id'].tolist() 
                print('')
                for title in result['title']:
                    print(title)
                print('')
                add_history_researches(username, movies_ids)
            else:
                print('')
                print("Aucun film trouvé avec les critères donnés.")
                break

            user_input = input("Voulez-vous continuer votre recherche ? (oui/non) ")
            if user_input.lower() == 'oui':
                menu_researches(username, df)
                return
            else:
                quit_input = input("Voulez-vous quitter le logiciel ? (oui/non) ")
                if quit_input.lower() == 'oui':
                    print('')
                    sys.exit("Fin du programme.")
                else:
                    menu_principal(username, df)
                    return
        else:
            print('\n Il faut choisir parmi les options proposées.\n')
            menu_researches(username, df)
            return



# Fonction pour obtenir une saisie de l'utilisateur
def get_input(prompt, allow_back=False):
    while True:
        response = input(prompt).strip()
        if allow_back and response.lower() in ['back', 'b']:
            return 'back'
        elif response.lower() in ['quit', 'q']:
            sys.exit("Programme terminé.")
        else:
            return response

# Fonctions pour obtenir chaque critère
def get_genre(df):
    print('')
    return get_input("Quel est votre genre de film  ? ", True)


def get_duration(df):
    while True:
        print('')
        duration_input = get_input("Quelle est la durée de film que vous souhaitez regarder (en minutes) ? ", True)
        if duration_input == 'back':
            return None
        try:
            return int(duration_input)
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def get_actor(df):
    print('')
    return get_input("Un acteur particulier ? ", True)


def get_language(df):
    print('')
    return get_input("Langue du film  ? ", True)



def search_combined_movies(df):
    genre = get_genre(df)
    duration = get_duration(df)
    actor = get_actor(df)
    language = get_language(df)
    criteria = [(genre, 'genre'), (duration, 'duration'), (actor, 'actor'), (language, 'language')]
    while criteria:
        args = {name: val for val, name in criteria if val is not None}
        result = search_movies(df, **args)
        if result is not None and not result.empty:
            return result
        criteria.pop()
        print("Ajustement des critères de recherche...")
    return None

# Fonction de recherche de films
def search_movies(df, genre=None, duration=None, actor=None, language=None):
    filtered_df = df.copy()  # Créer une copie pour éviter les modifications sur le DataFrame original

    # Appliquer les filtres
    if genre:
        filtered_df = filtered_df[filtered_df['genres'].str.contains(genre, case=False, na=False)]
    if actor:
        filtered_df = filtered_df[filtered_df['cast'].str.contains(actor, case=False, na=False)]
    if language:
        filtered_df = filtered_df[filtered_df['original_language'] == language]
    if duration:
        filtered_df['duration_diff'] = (filtered_df['runtime'] - duration).abs()
        filtered_df = filtered_df.sort_values('duration_diff')

    # Vérifier si des films ont été trouvés avant de tenter de les échantillonner
    if not filtered_df.empty:
        # Sélection aléatoire de 5 films, ou moins si moins de 5 films sont disponibles
        result = filtered_df.sample(n=min(5, len(filtered_df)), random_state=None)
        result.drop(columns=['duration_diff'], errors='ignore', inplace=True)
        return result
    else:
        return None
    
def add_history_researches(username, ids):
    try:
        df = pd.read_csv("C:/Users/meuni/Desktop/Projet/nfhaart/data/users.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=['username', 'researches'])

    # Trouver l'utilisateur ou ajouter une nouvelle entrée
    if username in df['username'].values:
        user_row = df[df['username'] == username].index[0]
        existing_ids = eval(df.loc[user_row, 'researches'])
        df.loc[user_row, 'researches'] = str(existing_ids + ids)
    else:
        df = df.append({'username': username, 'researches': str(ids)}, ignore_index=True)

    df.to_csv('C:/Users/meuni/Desktop/Projet/nfhaart/data/users.csv', index=False, header=True)



# def main(username):
#     df = load_data()
#     menu_principal(username, df)

# if __name__ == "__main__":
#     main()
