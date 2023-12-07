
import menu

def menu_stats(df):
    print('  Nombre total de films -------------------- [1]')
    print('  Durée totale ----------------------------- [2]')
    print('  Nombre de film en fonction de la langue -- [3]')
    print('  Mon compte ------------------------------- [4]')
    print('  Retour menu principal -------------------- [5]')
    print('\n')
    set_choice(df, input('  Choix du menu : '))

def set_choice(df, choice):
    if (choice.isnumeric() and choice in ['1', '2', '3', '4', '5']):
        match choice:
            case '1':
                count_all_movies(df)
            case '2':
                count_runtime(df)
            case '3':
                count_langue(df)
            case '4':
                print('faire function')
            case '5':
                menu.display_menu(df)
    else:
        print('\n Il faut choisir parmi les options proposées.\n')
        menu_stats(df)

def count_all_movies(df):
    # calculer le nombre total
    count_stat = df.describe()
    count_film = count_stat['id']
    countfilm = count_film['count']
    print('\n  Le nombre total des films est : '+  str(round(countfilm)) + '\n')

def count_runtime(df):
    # calculer le runtime total
    duree_total = df['runtime'].sum()
    duree_min = df['runtime'].min()
    duree_max = df['runtime'].max()
    duree_heure = duree_total//60
    duree_jour = duree_heure//24
    print('\n Le duree total de nos films en minutes est : '+ str(round(duree_total)) + '  Minutes\n')
    print('\n Le duree total de nos films en heures est : '+ str(round(duree_heure)) + '  Heures\n')
    print('\n Le duree total de nos films en jours est : '+ str(round(duree_jour)) + '  Jours\n')
    print('\n Le duree maximum de nos films en minutes est : '+ str(round(duree_max)) + '  Minutes\n')
    print('\n Le duree minimum de nos films en minutes est : '+ str(round(duree_min)) + '  Minutes\n')

def count_langue(df):
    
     # calculer le count de chaque langue
    langue = df['original_language']
    language_count = langue.value_counts()
    print(language_count)
    
    print('\n le nombre totale de film en langue Anglais: '+str(language_count['en'])+ '\n')
    print('\n le nombre totale de film en langue Francais: '+str(language_count['fr'])+ '\n')
    print('\n le nombre totale de film en langue Italien: '+str(language_count['it'])+ '\n')
    print('\n le nombre totale de film en langue Japonais: '+str(language_count['ja'])+ '\n')
    print('\n le nombre totale de film en langue Allemand: '+str(language_count['de'])+ '\n')
    print('\n le nombre totale de film en langue Arabe: '+str(language_count['ar'])+ '\n')
    print('\n le nombre totale de film en langue Espanol: '+str(language_count['es'])+ '\n')

    
    # calculer le nombre total
    
    print('\n')