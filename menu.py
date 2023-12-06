
import stats 
import researches
import filters
import users
import admin

def welcome(df, message = 'Netflix HAART'):
    ascii = ''

    for char in message:
        ascii += "/---\\"
    ascii += "\n"

    for char in message:
        ascii += f"| {char} |"
    ascii += "\n"

    for char in message:
        ascii += "\\---/"

    print('\n' + ascii + '\n')
    username = ask_credentials()
    print('')
    print('  Bienvenue ' + username)
    print('')
    display_menu(username, df)

def ask_credentials():
    username = input('  Nom d\'utilisateur : ')
    admin.check_username(username)
    return username

def display_menu(username, df):
    print('  Recherche de film ------------------------ [1]')  
    print('  Tous les films --------------------------- [2]')
    print('  Mon compte ------------------------------- [3]')
    print('  Statistiques ----------------------------- [4]')
    print('  Quitter ---------------------------------- [5]')
    print('')
    set_choice(username, df, input('  Choix du menu : '))

def set_choice(username, df, choice):
    if (choice.isnumeric() and choice in ['1', '2', '3', '4', '5', '6']):
        if (choice != '6'):
            match choice:
                case '1':
                    researches.menu_researches(username, df)
                case '2':
                    filters.menu_filters(username, df)
                case '3':
                    users.menu_users(username, df)
                case '4':
                    stats.menu_stats(username, df)
                case '5':
                    print('\n  À bientôt ' + username +  '\n')
                    exit(1)
        else:
            admin.menu_admin(username, df)
    else:
        print('')
        print('  ' + username + ', il faut choisir parmi les options proposées.')
        print('')
        display_menu(username, df)
       