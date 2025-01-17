"""FastAPI app creation, logger configuration and main API routes."""

import sys
import mlflow
import mlflow.pyfunc  # type: ignore
from fastapi import FastAPI, HTTPException  # type: ignore
from loguru import logger  # type: ignore

from src.api.types import HealthRouteOutput
from src.fraud_detector.types import (
    PredictionInput,
    PredictionOutput,
    PredictionInputBatch,
    PredictionOutputBatch,
)
import pandas as pd  # type: ignore
from mlflow.pyfunc import PyFuncModel  # Added import

# Remove pre-configured logging handler
logger.remove(0)
# Create a new logging handler same as the pre-configured one but with the extra
# attribute `request_id`
logger.add(
    sys.stdout,
    level="INFO",
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "ID: {extra[request_id]} - <level>{message}</level>"
    ),
)


def get_latest_model() -> PyFuncModel:
    """Get the latest model from MLflow Model Registry."""
    client = mlflow.tracking.MlflowClient()
    latest_version = client.get_latest_versions("fraud-detector")[0]
    return mlflow.pyfunc.load_model(f"models:/fraud-detector/{latest_version.version}")  # type: ignore


app = FastAPI()

# Load the trained model at startup from MLflow registry
try:
    model = get_latest_model()
    logger.info(
        f"Loaded model version: {mlflow.get_run(model.metadata.run_id).data.tags.get('version', 'unknown')}"  # type: ignore
    )  # type: ignore
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise RuntimeError("Could not load model from MLflow registry")


@app.get("/health")  # type: ignore
def health_check_route() -> HealthRouteOutput:
    """Health check route to check that the API is up.

    Returns:
        a dict with a "status" key
    """
    return HealthRouteOutput(status="ok")


@app.post("/predict_one", response_model=PredictionOutput)  # type: ignore
def predict(input_data: PredictionInput) -> PredictionOutput:
    """Predicts fraud based on single input data.

    Args:
        input_data: A JSON object with the same columns as the raw data.

    Returns:
        A JSON object with the prediction result.
    """
    try:
        # Convert input data to a DataFrame or the format expected by the model
        input_dict = input_data.model_dump()
        input_df = pd.DataFrame([input_dict])

        # Make prediction
        prediction = model.predict(input_df)[0]

        return PredictionOutput(prediction=int(prediction))
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed.")


@app.post("/predict_batch", response_model=PredictionOutputBatch)  # type: ignore
def predict_batch(input_data: PredictionInputBatch) -> PredictionOutputBatch:
    """Predicts fraud based on batch input data.

    Args:
        input_data: A list of input data objects.

    Returns:
        A JSON object with the list of prediction results.
    """
    try:
        # Convert input data to a DataFrame or the format expected by the model
        input_dicts = [item.model_dump() for item in input_data.inputs]
        input_df = pd.DataFrame(input_dicts)

        # Make predictions
        predictions = model.predict(input_df)

        return PredictionOutputBatch(predictions=[int(pred) for pred in predictions])
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail="Batch prediction failed.")
