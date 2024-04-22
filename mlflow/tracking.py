
import mlflow
from mlflow.models import infer_signature

import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

mlflow.set_tracking_uri(uri = "http://127.0.0.1:4444")
mlflow.set_experiment("MLflow Init")

# load iris dataset
X, y = datasets.load_iris(return_X_y = True)

# split train && test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.2, random_state = 42
)

params = {

    "solver": "lbfgs",
    "max_iter": 1000,
    "multi_class": "auto",
    "random_state": 8888

}

# train
lr = LogisticRegression(**params)
lr.fit(X_train, y_train)

# predict
y_pred = lr.predict(X_test)

# metrics
accuracy = accuracy_score(y_test, y_pred)

# start an MLflow run
with mlflow.start_run():
    # log hyperparameters
    mlflow.log_params(params)

    # log the loss metric
    mlflow.log_metric("accuracy", accuracy)

    # set tag
    mlflow.set_tag("Training Info", "Basic LR model for iris data")

    # infer model signature
    signature = infer_signature(X_train, lr.predict(X_train))

    # log model
    model_info = mlflow.sklearn.log_model(

        sk_model = lr,
        artifact_path = "iris_model",
        signature = signature,
        input_example = X_train,
        registered_model_name = "tracking-quickstart"

    )

