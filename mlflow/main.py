
import mlflow
from mlflow.models import infer_signature

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score, r2_score
from sklearn.linear_model import LinearRegression

warnings.simplefilter(action = 'ignore', category = FutureWarning)

seed = 42 
np.random.seed(42)

mlflow.set_tracking_uri(uri = "http://127.0.0.1:4444")
mlflow.set_experiment("MLflow Salaries")

def display(to_display, message = ''):
    print()
    if (len(message ) > 0):
        print(' > ' + str(message) + ':')
        print()
    print(to_display)
    print()


job_categories = {

    "Principal Data Scientist": "Data Science & Machine Learning",
    "ML Engineer": "Data Science & Machine Learning",
    "Data Scientist": "Data Science & Machine Learning",
    "Applied Scientist": "Data Science & Machine Learning",
    "Research Scientist": "Data Science & Machine Learning",
    "Applied Machine Learning Engineer": "Data Science & Machine Learning",
    "Machine Learning Researcher": "Data Science & Machine Learning",
    "Machine Learning Scientist": "Data Science & Machine Learning",
    "Applied Machine Learning Scientist": "Data Science & Machine Learning",
    "Deep Learning Researcher": "Data Science & Machine Learning",
    "Machine Learning Infrastructure Engineer": "Data Science & Machine Learning",
    "NLP Engineer": "Data Science & Machine Learning",
    "Machine Learning Research Engineer": "Data Science & Machine Learning",
    "Principal Machine Learning Engineer": "Data Science & Machine Learning",
    "Machine Learning Manager": "Data Science & Machine Learning",
    "Lead Machine Learning Engineer": "Data Science & Machine Learning",
    "Machine Learning Developer": "Data Science & Machine Learning",
    "Data Analyst": "Data Analysis & Analytics",
    "Analytics Engineer": "Data Analysis & Analytics",
    "Data Analytics Manager": "Data Analysis & Analytics",
    "Business Data Analyst": "Data Analysis & Analytics",
    "Staff Data Analyst": "Data Analysis & Analytics",
    "Lead Data Analyst": "Data Analysis & Analytics",
    "BI Data Analyst": "Data Analysis & Analytics",
    "Insight Analyst": "Data Analysis & Analytics",
    "BI Analyst": "Data Analysis & Analytics",
    "Data Analytics Specialist": "Data Analysis & Analytics",
    "Data Analytics Lead": "Data Analysis & Analytics",
    "Product Data Analyst": "Data Analysis & Analytics",
    "Marketing Data Analyst": "Data Analysis & Analytics",
    "Finance Data Analyst": "Data Analysis & Analytics",
    "Data Modeler": "Data Engineering & Infrastructure",
    "Data Engineer": "Data Engineering & Infrastructure",
    "ETL Engineer": "Data Engineering & Infrastructure",
    "Data DevOps Engineer": "Data Engineering & Infrastructure",
    "Big Data Engineer": "Data Engineering & Infrastructure",
    "Cloud Database Engineer": "Data Engineering & Infrastructure",
    "Data Infrastructure Engineer": "Data Engineering & Infrastructure",
    "Software Data Engineer": "Data Engineering & Infrastructure",
    "Data Operations Engineer": "Data Engineering & Infrastructure",
    "Cloud Data Engineer": "Data Engineering & Infrastructure",
    "ETL Developer": "Data Engineering & Infrastructure",
    "Cloud Data Architect": "Data Engineering & Infrastructure",
    "Lead Data Engineer": "Data Engineering & Infrastructure",
    "Principal Data Engineer": "Data Engineering & Infrastructure",
    "Staff Data Scientist": "Data Engineering & Infrastructure",
    "Business Intelligence Engineer": "Business Intelligence (BI)",
    "BI Data Engineer": "Business Intelligence (BI)",
    "BI Developer": "Business Intelligence (BI)",
    "Head of Data Science": "Business Intelligence (BI)",
    "BI Data Analyst": "Business Intelligence (BI)",
    "Power BI Developer": "Business Intelligence (BI)",
    "Data Strategist": "Data Management",
    "Director of Data Science": "Data Management",
    "Head of Data": "Data Management",
    "Data Science Manager": "Data Management",
    "Data Manager": "Data Management",
    "Manager Data Management": "Data Management",
    "Data Management Specialist": "Data Management",
    "MLOps Engineer": "AI & Machine Learning Operations (MLOps)",
    "Computer Vision Engineer": "Computer Vision",
    "Computer Vision Software Engineer": "Computer Vision",
    "3D Computer Vision Researcher": "Computer Vision",
    "AI Developer": "Artificial Intelligence (AI)",
    "AI Scientist": "Artificial Intelligence (AI)",
    "Head of Machine Learning": "Artificial Intelligence (AI)",
    "AI Programmer": "Artificial Intelligence (AI)",
    "Data Quality Analyst": "Compliance & Quality Assurance",
    "Compliance Data Analyst": "Compliance & Quality Assurance",
    "Autonomous Vehicle Technician": "Compliance & Quality Assurance",  # Assumed mapping due to similarity
    "Applied Machine Learning Scientist": "Data Science & Machine Learning",  # Assumed mapping
    "Lead Data Scientist": "Data Science & Machine Learning",  # Assumed mapping
    "Data Architect": "Data Engineering & Infrastructure",  # Assumed mapping
    "Finance Data Analyst": "Data Analysis & Analytics",  # Duplicate mapping
    "Data Lead": "Data Management",  # Assumed mapping
    "Data Science Engineer": "Data Engineering & Infrastructure",  # Assumed mapping
    "Data Science Lead": "Data Science & Machine Learning",  # Assumed mapping
    "Deep Learning Engineer": "Data Science & Machine Learning",  # Assumed mapping
    "Machine Learning Software Engineer": "Data Science & Machine Learning",  # Assumed mapping
    "Big Data Architect": "Data Engineering & Infrastructure",  # Assumed mapping
    "Cloud Database Engineer": "Data Engineering & Infrastructure",  # Duplicate mapping
    "Data Analytics Engineer": "Data Analysis & Analytics",  # Assumed mapping
    "Data Management Specialist": "Data Management",  # Duplicate mapping
    "Data Scientist Lead": "Data Science & Machine Learning",  # Assumed mapping
    "Cloud Data Engineer": "Data Engineering & Infrastructure",  # Duplicate mapping
    "Data Operations Analyst": "Data Engineering & Infrastructure",  # Assumed mapping
    "Marketing Data Analyst": "Data Analysis & Analytics",  # Duplicate mapping
    "Power BI Developer": "Business Intelligence (BI)",  # Duplicate mapping
    "Product Data Scientist": "Product & Marketing Data",  # Duplicate mapping
    "Financial Data Analyst": "Data Analysis & Analytics",  # Assumed mapping
    "Data Science Consultant": "Data Management",  # Assumed mapping
    "AI Developer": "Artificial Intelligence (AI)",  # Duplicate mapping
    "Data Analytics Specialist": "Data Analysis & Analytics",  # Duplicate mapping
    "Business Data Analyst": "Data Analysis & Analytics",  # Duplicate mapping
    "Lead Data Engineer": "Data Engineering & Infrastructure",  # Duplicate mapping
    "BI Data Engineer": "Business Intelligence (BI)",  # Duplicate mapping
    "Data Engineer": "Data Engineering & Infrastructure",  # Duplicate mapping
    "BI Developer": "Business Intelligence (BI)",  # Duplicate mapping
    "Data Science Tech Lead": "Data Science & Machine Learning",  # Assumed mapping
    "Data Operations Engineer": "Data Engineering & Infrastructure",  # Duplicate mapping
    "BI Analyst": "Data Analysis & Analytics",  # Duplicate mapping
    "Data Science Consultant": "Data Science & Machine Learning",  # Assumed mapping
    "Data Science Lead": "Data Science & Machine Learning",  # Duplicate mapping
    "Lead Data Scientist": "Data Science & Machine Learning",  # Duplicate mapping
    "Data Scientist Lead": "Data Science & Machine Learning",  # Duplicate mapping
    "Data Operations Analyst": "Data Engineering & Infrastructure",  # Duplicate mapping
    "Marketing Data Engineer": "Product & Marketing Data",  # Duplicate mapping
    "AI Programmer": "Artificial Intelligence (AI)",  # Duplicate mapping
    "Computer Vision Software Engineer": "Computer Vision",  # Duplicate mapping
    "Azure Data Engineer": "Data Engineering & Infrastructure",  # Assumed mapping
    "Principal Data Architect": "Data Engineering & Infrastructure",  # Assumed mapping
    "Data Analytics Consultant": "Data Analysis & Analytics",  # Assumed mapping
    "Data Management Specialist": "Data Management",  # Duplicate mapping
    "Data Scientist": "Data Science & Machine Learning",  # Duplicate mapping
    "Data Manager": "Data Management",  # Assumed mapping
    "Software Data Engineer": "Data Engineering & Infrastructure",  # Duplicate mapping
    "Research Engineer": "Data Science & Machine Learning",
    "Machine Learning Engineer": "Data Science & Machine Learning",
    "Applied Data Scientist": "Data Science & Machine Learning",
    "Data Specialist": "Data Engineering & Infrastructure",
    "Principal Data Analyst": "Data Analysis & Analytics"

}

#### ---- ---- DATA PREPARATION && CLEANING ---- ---- ####

df = pd.read_csv('./data/salaries.csv')

"""
display(' > Shape:' + str(df.shape))
display(df.dtypes, ' > Types:')
display(df.isna().sum(), ' > ISNA:')
display(df.duplicated(), ' > Duplications:')
display(df.select_dtypes(include=['object']).nunique(), ' > Unique values:')
"""

#### ---- ---- DATA PREPROCESSING ---- ---- ####

"""
categorical_columns = df.columns[df.dtypes == 'object']

display(categorical_columns, 'Categorical columns')

# extract sub categories of each category
for column in categorical_columns:
    unique_values = df[column].unique()
    print(f"{column} : {unique_values}\n")
"""

X = df.copy()
y = X.pop("salary_in_usd")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 42)

#### CUSTOM TRANSFORMERS

class CommonAttributeSelector(BaseEstimator, TransformerMixin):
    def __init__(self, columns: list[str], top_k: list[int]):
        self.top_k = top_k
        self.columns = columns
    def fit(self, X, y = None):
        return self
    def transform(self, X: pd.DataFrame, y = None):
        X_changed = X.copy()
        for k, attr in zip(self.top_k, self.columns):
            top_values = list(X_changed[attr].value_counts().to_dict().keys())[:k]
            X_changed[attr] = X_changed[attr].map(lambda x: x if x in top_values else "OTHER")
        return X_changed

class JobCategorizer(BaseEstimator, TransformerMixin):
    def __init__(self, column: str, category_dict: dict):
        self.category_dict = category_dict
        self.column = column
    def fit(self, X, y = None):
        return self
    def transform(self, X: pd.DataFrame, y = None):
        X_changed = X.copy()
        X_changed[self.column] = X_changed[self.column].map(lambda x: self.category_dict[x])
        return X_changed

#### PIPELINES

one_hot_cols = ["employment_type"]
ordinal_cols = ["work_year", "experience_level", "remote_ratio", "company_size"]

currency_pipeline = Pipeline([

    ("common_attr_filter", CommonAttributeSelector(["salary_currency"], [5])),
    ("one_hot_encoder", OneHotEncoder())

])

job_pipeline = Pipeline([

    ("job_categorizer", JobCategorizer("job_title", job_categories)),
    ("one_hot_encoder", OneHotEncoder())

])

full_pipeline = ColumnTransformer([

    ("currency_pipeline", currency_pipeline, ["salary_currency"]),
    ("job_pipeline", job_pipeline, ["job_title"]),
    ("one_hot_encoder", OneHotEncoder(), one_hot_cols),
    ("ordinal_encoder", OrdinalEncoder(categories = [

        [2020, 2021, 2022, 2023],
        ["EN", "MI", "SE", "EX"],
        [0, 50, 100],
        ["S", "M", "L"]

    ]), ordinal_cols)

], remainder = "drop", sparse_threshold = 0)

X_train_transformed = full_pipeline.fit_transform(X_train)

# display(X_train_transformed.shape, 'X_train_transformed shape')
# display(full_pipeline.named_transformers_["ordinal_encoder"].categories_, 'Ordinal encoder categories')

X_test_transformed = full_pipeline.transform(X_test)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_transformed)
X_test_scaled = scaler.transform(X_test_transformed)

#### ---- ---- MODELS BUILDING ---- ---- ####

#### LINEAR REGRESSION

lr = LinearRegression()
lr.fit(X_train_transformed, y_train)

lr_train_preds = lr.predict(X_train_transformed)
mae_lr_train_preds = mean_absolute_error(y_train, lr_train_preds)
mse_lr_train_preds = mean_squared_error(y_train, lr_train_preds)

lr_test_preds = lr.predict(X_test_transformed)
mae_lr_test_preds = mean_absolute_error(y_test, lr_test_preds)
mse_lr_test_preds = mean_squared_error(y_test, lr_test_preds)

# display(mae_lr_train_preds, 'MAE linear regression train predictions')
# display(mae_lr_test_preds, 'MAE linear regression test predictions')

params = {

   "model": "Linear Regression"

}

metrics = {

    "mae_train": mae_lr_train_preds, 
    "mse_train": mse_lr_train_preds, 
    "rmse_train": np.sqrt(mse_lr_train_preds), 
    "mae_test": mae_lr_test_preds, 
    "mse_test": mse_lr_test_preds, 
    "rmse_test": np.sqrt(mse_lr_test_preds),
    "r2_score_test": r2_score(y_test, lr_test_preds)

}

# start an MLflow run
with mlflow.start_run():
    mlflow.log_params(params)
    # mlflow.log_metric("MAE test", mae_lr_test_preds)
    mlflow.log_metrics(metrics)
    mlflow.set_tag("First set_tag", "Second set_tag")
    # infer model signature
    signature = infer_signature(X_train_transformed, lr.predict(X_train_transformed))
    # log model
    model_info = mlflow.sklearn.log_model(

        sk_model = lr,
        artifact_path = "data_salaries",
        signature = signature,
        input_example = X_train_transformed,
        registered_model_name = "linear_regression"

    )

