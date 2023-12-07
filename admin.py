
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

PATH_CSV_USERS = os.getenv('PATH_CSV_USERS')

def menu_admin(df):
    print('\n')
    print(df)
    print('\n')
    print(' here menu admin')
    print('\n')

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



