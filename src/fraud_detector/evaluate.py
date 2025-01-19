import pandas as pd  # type: ignore
import pickle
from sklearn.metrics import (  # type: ignore
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
import os
import mlflow  # type: ignore
from src.fraud_detector.types import EvaluateModelParams  # Already centralized


def evaluate_model(params: EvaluateModelParams) -> None:
    # Set MLflow tracking URI
    mlflow.set_tracking_uri("http://localhost:5000")  # type: ignore

    # Load the trained model
    with open(params.model_path, "rb") as f:
        model = pickle.load(f)

    # Load validation data
    data = pd.read_csv(params.valid_csv)
    X = data.drop("class", axis=1)
    target = "class"  # Changed from 'Class' to 'class'
    y_true = data[target]

    # Make predictions
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]

    # Calculate metrics
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1_score": f1_score(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, y_proba),
    }

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(params.evaluation_path), exist_ok=True)

    # Save metrics to a JSON file
    with open(params.evaluation_path, "w") as f:
        import json

        json.dump(metrics, f, indent=4)

    # Start MLflow run for evaluation
    with mlflow.start_run():  # type: ignore
        # Log metrics
        mlflow.log_metrics(metrics)  # type: ignore

        # Log the metrics JSON file as an artifact
        mlflow.log_artifact(params.evaluation_path)  # type: ignore
