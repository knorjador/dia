
import pandas as pd
import os
from dotenv import load_dotenv
import menu

load_dotenv()

PATH_CSV_USERS = os.getenv('PATH_CSV_USERS')

def menu_admin(username, df):
    print('')
    print('  Consulter les statistiques --------------- [1]')
    print('  Retour menu principal  ------------------- [2]') 
    print('')
    set_choice(username, df, input('  Choix du menu : '))

def set_choice(username, df, choice):
    if (choice.isnumeric() and choice in ['1', '2', '3']):
        match choice:
            case '1':
                display_stats()
            case '2':
                menu.display_menu(username, df)

        print('')
        menu_admin(username, df)

    else:
        print('\n Il faut choisir parmi les options proposées.\n')
        menu_admin(username, df)

def display_stats():
    df = pd.read_csv(PATH_CSV_USERS)
    print('')
    print("  Nombre d'utilisateur(s) : " + str(len(df.index)))

def check_username(username):
    member = False
    df = pd.read_csv(PATH_CSV_USERS)
    length = len(df)
    for i in range(length):
        if (df.loc[i, 'username'] == username):
            member = True
            df.loc[i, 'connections'] = df.loc[i, 'connections'] + 1
            df.to_csv(PATH_CSV_USERS, mode='w', index=False, header=True)

    if (member == False):
        df = pd.DataFrame([[username, 1, [], []]])
        df.to_csv(PATH_CSV_USERS, mode='a', index=False, header=False)



