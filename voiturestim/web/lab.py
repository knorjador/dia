
import os
import numpy as np 
import pandas as pd
from passlib.context import CryptContext
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def get_nb_unique_values(dataset):
    for column in dataset.columns:
        # print(f"{column}:")
        # print(dataset[column].value_counts())
        print(f"{column}: " + str(df[column].nunique()))

basedir = os.path.abspath(os.path.dirname(__file__))
data = os.path.join(basedir, "../data/train.csv")

df = pd.read_csv(data)
# df['Name'] = df['Name'].str.split().str[0]

print()
print('    > DF SHAPE: ', df.shape)
print('    > NULL VALUES: \n')
print(df.isnull().sum())
print()
print(df.head())
print()
get_nb_unique_values(df)
print()

# nb_nulls = df.isnull().sum()
# print(nb_nulls)
# df.head()
# df.info()



# X = df.drop(columns=["Price"])
# y = df["Price"]

# numeric_features = X.select_dtypes(include=["float64", "int64"]).columns
# categorical_features = X.select_dtypes(include=["object"]).columns

# print(numeric_features)
# print(categorical_features)

"""
Name,Location,Year,Kilometers_Driven,Fuel_Type,Transmission,Owner_Type,Mileage,Engine,Power,Seats,New_Price,Price
Maruti Wagon R LXI CNG,Mumbai,2010,72000,CNG,Manual,First,26.6 km/kg,998 CC,58.16 bhp,5,,1.75
Hyundai Creta 1.6 CRDi SX Option,Pune,2015,41000,Diesel,Manual,First,19.67 kmpl,1582 CC,126.2 bhp,5,,12.5
Honda Jazz V,Chennai,2011,46000,Petrol,Manual,First,18.2 kmpl,1199 CC,88.7 bhp,5,8.61 Lakh,4.5
Maruti Ertiga VDI,Chennai,2012,87000,Diesel,Manual,First,20.77 kmpl,1248 CC,88.76 bhp,7,,6

Index(['Year', 'Kilometers_Driven', 'Seats'], dtype='object')
Index(['Name', 'Location', 'Fuel_Type', 'Transmission', 'Owner_Type',
       'Mileage', 'Engine', 'Power', 'New_Price'],
      dtype='object')



"""

# df_dummies = pd.get_dummies(df, columns=['Name', 'Location', 'Fuel_Type', 'Transmission', 'Owner_Type', 'Mileage', 'Engine', 'Power', 'New_Price', 'Price'])

# print(df_dummies.shape)

# corr = df_dummies.corr()
# mask = np.triu(np.ones_like(corr, dtype=bool))
# f, ax = plt.subplots(figsize=(11, 9))
# cmap = sns.diverging_palette(230, 20, as_cmap=True)
 
# sns.heatmap(corr, mask=mask, cmap=cmap,  center=0, square=True, linewidths=.5,cbar_kws={"shrink": .5},  annot=True)

"""
X = df.drop(["Name", "New_Price"], axis=1)
y = df["Price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns
categorical_features = X_train.select_dtypes(include=['object']).columns

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')), 
    ('scaler', StandardScaler())
]) 

categorical_transformer = Pipeline(steps=[
    #('imputer', SimpleImputer(strategy='most_frequent')), 
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numeric_features), 
    ('cat', categorical_transformer, categorical_features)
]) 

X_train_encoded = preprocessor.fit_transform(X_train)
X_train_encoded_df = pd.DataFrame(X_train_encoded, columns=preprocessor.get_feature_names_out())

print(X_train_encoded_df)
"""

# pipeline = Pipeline(steps=[
#     ('preprocessor', preprocessor),
#     ('model', LinearRegression())
# ])

# print(pipeline)

# corr = X_train_processed.corr()
# mask = np.triu(np.ones_like(corr, dtype=bool))
# f, ax = plt.subplots(figsize=(11, 9))
# cmap = sns.diverging_palette(230, 20, as_cmap=True)
 
# sns.heatmap(corr, mask=mask, cmap=cmap,  center=0, square=True, linewidths=.5,cbar_kws={"shrink": .5},  annot=True)





# brands = np.sort(df['Name'].unique())
# years = np.sort(df['Year'].unique(), kind='mergesort')[::-1]
# fuels = np.sort(df['Fuel_Type'].unique(), kind='mergesort')[::-1]

# Name,Location,Year,Kilometers_Driven,Fuel_Type,Transmission,Owner_Type,Mileage,Engine,Power,Seats,New_Price,Price

# brands = np.sort(df['Name'].unique())
# transmission = np.sort(df['Transmission'].unique())
# fuel = np.sort(df['Fuel_Type'].unique())

# print(brands)
# print(transmission)
# print(fuel)

# hashed_password = pwd_context.hash("ok")