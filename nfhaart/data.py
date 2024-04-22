
import pandas as pd 

def get_data_frame():
    csv_credits = pd.read_csv('./data/credits.csv')
    csv_movies_metadata = pd.read_csv('./data/movies_metadata.csv')

    df_credits = pd.DataFrame(csv_credits)
    df_movies_metadata = pd.DataFrame(csv_movies_metadata)

    df_credits['id'] = df_credits['id'].astype('int64')
    df_movies_metadata['id'] = df_movies_metadata['id'].astype('int64')

    return pd.merge(df_movies_metadata, df_credits, on="id")