
import menu
import math
def menu_stats(username, df):
    print('  Nombre totale de films -------------------- [1]')
    print('  Durée totale ------------------------------ [2]')
    print('  Nombre et pourcentage film / pays --------- [3]')
    print('  Retour menu principal --------------------- [4]')
    print('\n')
    set_choice(username, df, input('  Choix du menu : '))

def set_choice(username, df, choice):
    if (choice.isnumeric() and choice in ['1', '2', '3', '4', '5']):
        match choice:
            case '1':
                count_all_movies(username, df)
            case '2':
                count_runtime(username, df)
            case '3':
                count_langue(username, df)
            case '4':
                menu.display_menu(username, df)
                
    else:
        print('\n Il faut choisir parmi les options proposées.\n')
        menu_stats(username, df)

def count_all_movies(username, df):
    # calculer le nombre total
    count_stat = df.describe()
    count_film = count_stat['id']
    countfilm = count_film['count']
    print('\n  Le nombre total des films est : '+  str(round(countfilm)) + '\n')
    menu_stats(username, df)

def count_runtime(username, df):
    # calculer le runtime total
    duree_total = df['runtime'].sum()
    duree_min = df['runtime'].min()
    duree_max = df['runtime'].max()
    duree_heure = duree_total//60
    duree_jour = duree_heure//24
    print('\n La duree total de nos films en minutes est : '+ str(round(duree_total)) + '  Minutes\n')
    print('\n La duree total de nos films en heures est : '+ str(round(duree_heure)) + '  Heures\n')
    print('\n La duree total de nos films en jours est : '+ str(round(duree_jour)) + '  Jours\n')
    print('\n Le film le plus long est : '+ str(round(duree_max)) + '  Minutes\n')
    print('\n Le film le plus court est : '+ str(round(duree_min)) + '  Minutes\n')
    menu_stats(username, df)

def count_langue(username, df):
    
     # calculer le count de chaque langue
    langue = df['original_language']
    language_count = langue.value_counts()
    
    print('\n Le nombre totale de film Americain est de '+str(language_count['en'])+ ' Films. Cela represente '+str(round((32316/45452)*100))+' % du catalogue.\n')
    print('\n Le nombre totale de film Francais est de '+str(language_count['fr'])+ ' Films. Cela represente '+str(round((2443/45452)*100))+' % du catalogue.\n')
    print('\n Le nombre totale de film Italien est de '+str(language_count['it'])+ ' Films. Cela represente '+str(round((1529/45452)*100))+' % du catalogue.\n')
    print('\n Le nombre totale de film Japonais est de '+str(language_count['ja'])+ ' Films. Cela represente '+str(round((1356/45452)*100))+' % du catalogue.\n')
    print('\n Le nombre totale de film Allemand est de '+str(language_count['de'])+ ' Films. Cela represente '+str(round((1083/45452)*100))+' % du catalogue.\n')
    print('\n Le nombre totale de film Espagnol est de '+str(language_count['es'])+ ' Films. Cela represente '+str(round((993/45452)*100))+' % du catalogue.\n')
    print('\n Le nombre totale de film Arabe est de '+str(language_count['ar'])+ ' Films. Cela represente '+str(math.ceil((39/45452)*100))+' % du catalogue.\n')
    menu_stats(username, df)

    # calculer le nombre total
    
    print('\n')