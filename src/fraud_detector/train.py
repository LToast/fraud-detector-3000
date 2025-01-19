from sklearn.ensemble import RandomForestClassifier  # type: ignore
import pandas as pd  # type: ignore
import pickle
import mlflow  # type: ignore
import mlflow.sklearn  # type: ignore
import os
from mlflow.tracking import MlflowClient  # type: ignore
from src.fraud_detector.types import TrainModelParams

import logging

logger = logging.getLogger(__name__)


def train_model(params: TrainModelParams) -> None:
    # Create the MLflow directory if it doesn't exist
    os.makedirs("mlflow", exist_ok=True)

    # Configure MLflow tracking server URI
    mlflow.set_tracking_uri("http://localhost:5000")  # type: ignore
    # Start an MLflow run
    with mlflow.start_run() as run:  # type: ignore
        # Log training parameters to MLflow
        mlflow.log_param("n_jobs", params.n_jobs)  # type: ignore
        mlflow.log_param("seed", params.seed)  # type: ignore
        mlflow.log_param("rfc_metric", params.rfc_metric)  # type: ignore
        mlflow.log_param("n_estimators", params.n_estimators)  # type: ignore

        target: str = "class"
        predictors: list[str] = [
            "time",
            "v1",
            "v2",
            "v3",
            "v4",
            "v5",
            "v6",
            "v7",
            "v8",
            "v9",
            "v10",
            "v11",
            "v12",
            "v13",
            "v14",
            "v15",
            "v16",
            "v17",
            "v18",
            "v19",
            "v20",
            "v21",
            "v22",
            "v23",
            "v24",
            "v25",
            "v26",
            "v27",
            "v28",
            "amount",
        ]

        # Load training data
        train_df: pd.DataFrame = pd.read_csv(params.train_csv)

        # Initialize and train the RandomForestClassifier
        clf: RandomForestClassifier = RandomForestClassifier(
            n_jobs=params.n_jobs,
            random_state=params.seed,
            criterion=params.rfc_metric,
            n_estimators=params.n_estimators,
            verbose=False,
        )
        clf.fit(train_df[predictors], train_df[target].values)

        # Log the trained model to MLflow
        mlflow.sklearn.log_model(clf, "model")

        # Initialize MLflow client for model registry operations
        client: MlflowClient = MlflowClient()
        model_name: str = "fraud-detector"

        try:
            # Register the model in MLflow Model Registry
            registered_model = mlflow.register_model(  # type: ignore
                model_uri=f"runs:/{run.info.run_id}/model", name=model_name
            )
            logger.info(
                f"Registered model with name: {model_name} and version: {registered_model.version}"
            )
        except Exception as e:
            logger.error(f"Model registration failed: {e}")
            raise e

        try:
            # Transition the registered model to Production stage
            client.transition_model_version_stage(
                name=model_name,
                version=registered_model.version,
                stage="Production",
                archive_existing_versions=True,
            )
            logger.info(
                f"Model version {registered_model.version} transitioned to Production"
            )
        except Exception as e:
            logger.error(f"Model stage transition failed: {e}")
            raise e

        # Ensure the model path directory exists
        os.makedirs(os.path.dirname(params.model_path), exist_ok=True)

        # Save the trained model locally
        with open(params.model_path, "wb") as f:
            pickle.dump(clf, f)
