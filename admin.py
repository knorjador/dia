
import pandas as pd

def menu_admin(df):
    print('\n')
    print(df)
    print('\n')
    print(' here menu admin')
    print('\n')

def check_username(username):
    member = False
    df = pd.read_csv("./data/users.csv")
    length = len(df)
    for i in range(length):
        if (df.loc[i, 'username'] == username):
            member = True
            df.loc[i, 'connections'] = df.loc[i, 'connections'] + 1
            # step = list(eval(df.loc[i, 'researches']))
            # step.append({ 'genre': 'comedy', 'runtime': 88, 'actor': 'bobby', 'country': 'fr' })
            # df.loc[i, 'researches'] = str(step)
            # df.to_csv('./data/users.csv', mode='w', index=False, header=True)

    if (member == False):
        df = pd.DataFrame([[username, 1, [], []]])
        df.to_csv('./data/users.csv', mode='a', index=False, header=False)



