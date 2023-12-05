
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
    display_menu(df)


def display_menu(df):
    print('  Statistiques ----------------------------- [1]')
    print('  Recherche de film ------------------------ [2]')
    print('  Tous les films --------------------------- [3]')
    print('  Mon compte ------------------------------- [4]')
    print('  Quitter ---------------------------------- [5]')
    print('\n')
    set_choice(df, input('  Choix du menu : '))

def set_choice(df, choice):
    if (choice.isnumeric() and choice in ['1', '2', '3', '4', '5', '6']):
        if (choice != '6'):
            match choice:
                case '1':
                    stats.menu_stats(df)
                case '2':
                    researches.menu_researches(df)
                case '3':
                    filters.menu_filters(df)
                case '4':
                    users.menu_users(df)
                case '5':
                    print('\n  À bientôt sur Netflix HAART \n')
                    exit(1)
        else:
            admin.menu_admin(df)
    else:
        print('\n Il faut choisir parmi les options proposées.\n')
        display_menu(df)
       