
def welcome(message = 'Netflix HAART'):
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
    displayMenu()


def displayMenu():
    print('  Statistiques ----------------------------- [1]')
    print('  Recherche de film ------------------------ [2]')
    print('  Tous les films --------------------------- [3]')
    print('  Mon compte ------------------------------- [4]')
    print('\n')
    choice = input('  Choix du menu : ')
    print(choice)


welcome()