"""Tests for `api/main.py`."""

from src.api.main import health_check_route, hello_world, predict, predict_batch
from src.fraud_detector.types import (
    PredictionInput,
    PredictionOutput,
    PredictionInputBatch,
    PredictionOutputBatch,
)
from src.api.types import HealthRouteOutput, HelloWorldRouteInput, HelloWorldRouteOutput

import pytest
from pydantic import ValidationError  # Added import
from fastapi.testclient import TestClient  # Added import

# Initialize TestClient with the FastAPI app
client = TestClient(hello_world)  # ...existing initialization...


def test_health_check_route() -> None:
    assert health_check_route() == HealthRouteOutput(status="ok")


def test_hello_world() -> None:
    assert hello_world(HelloWorldRouteInput(name="World")) == HelloWorldRouteOutput(
        message="Hello, World!"
    )


def test_predict_valid_input() -> None:
    input_data = PredictionInput(
        time=100000,  # Changed from 'Time' to 'time'
        v1=0.5,  # Changed from 'V1' to 'v1'
        v2=1.2,  # Changed from 'V2' to 'v2'
        v3=3.3,
        v4=0.0,
        v5=0.1,
        v6=-1.2,
        v7=0.3,
        v8=1.1,
        v9=-0.5,
        v10=0.2,
        v11=-1.0,
        v12=0.4,
        v13=0.1,
        v14=-0.3,
        v15=0.2,
        v16=0.0,
        v17=0.1,
        v18=-0.2,
        v19=0.3,
        v20=0.0,
        v21=0.1,
        v22=-0.1,
        v23=0.2,
        v24=0.3,
        v25=0.0,
        v26=-0.2,
        v27=0.1,
        v28=0.0,
        amount=100.0,  # Changed from 'Amount' to 'amount'
    )  # Populate all required fields
    result = predict(input_data)
    assert isinstance(result, PredictionOutput)
    assert isinstance(result.prediction, int)  # Assuming binary classification


def test_predict_invalid_input_missing_field() -> None:
    with pytest.raises(ValidationError):  # Changed from ValueError to ValidationError
        # Missing 'amount'
        PredictionInput(
            time=100000,
            v1=0.5,
            v2=1.2,
            v3=3.3,
            v4=0.0,
            v5=0.1,
            v6=-1.2,
            v7=0.3,
            v8=1.1,
            v9=-0.5,
            v10=0.2,
            v11=-1.0,
            v12=0.4,
            v13=0.1,
            v14=-0.3,
            v15=0.2,
            v16=0.0,
            v17=0.1,
            v18=-0.2,
            v19=0.3,
            v20=0.0,
            v21=0.1,
            v22=-0.1,
            v23=0.2,
            v24=0.3,
            v25=0.0,
            v26=-0.2,
            v27=0.1,  # 'amount' is missing
        )  # type: ignore


def test_predict_invalid_input_wrong_type() -> None:
    with pytest.raises(ValidationError):  # Changed from TypeError to ValidationError
        # 'v2' should be a float
        PredictionInput(
            time=100000,
            v1=0.5,
            v2="invalid_type",
            v3=3.3,
            v4=0.0,
            v5=0.1,
            v6=-1.2,
            v7=0.3,
            v8=1.1,
            v9=-0.5,
            v10=0.2,
            v11=-1.0,
            v12=0.4,
            v13=0.1,
            v14=-0.3,
            v15=0.2,
            v16=0.0,
            v17=0.1,
            v18=-0.2,
            v19=0.3,
            v20=0.0,
            v21=0.1,
            v22=-0.1,
            v23=0.2,
            v24=0.3,
            v25=0.0,
            v26=-0.2,
            v27=0.1,
            v28=0.0,
            amount=100.0,
        )  # type: ignore


def test_predict_batch_valid_input() -> None:
    input_data = PredictionInputBatch(
        inputs=[  # Changed from 'data' to 'inputs'
            {
                "time": 100000,
                "v1": 0.5,
                "v2": 1.2,
                "v3": 3.3,
                "v4": 0.0,
                "v5": 0.1,
                "v6": -1.2,
                "v7": 0.3,
                "v8": 1.1,
                "v9": -0.5,
                "v10": 0.2,
                "v11": -1.0,
                "v12": 0.4,
                "v13": 0.1,
                "v14": -0.3,
                "v15": 0.2,
                "v16": 0.0,
                "v17": 0.1,
                "v18": -0.2,
                "v19": 0.3,
                "v20": 0.0,
                "v21": 0.1,
                "v22": -0.1,
                "v23": 0.2,
                "v24": 0.3,
                "v25": 0.0,
                "v26": -0.2,
                "v27": 0.1,
                "v28": 0.0,
                "amount": 100.0,
            },
            {
                "time": 100001,
                "v1": 0.6,
                "v2": 1.5,
                "v3": 3.5,
                "v4": 0.1,
                "v5": 0.2,
                "v6": -1.1,
                "v7": 0.4,
                "v8": 1.2,
                "v9": -0.4,
                "v10": 0.3,
                "v11": -0.9,
                "v12": 0.5,
                "v13": 0.2,
                "v14": -0.2,
                "v15": 0.3,
                "v16": 0.1,
                "v17": 0.2,
                "v18": -0.1,
                "v19": 0.4,
                "v20": 0.1,
                "v21": 0.2,
                "v22": -0.2,
                "v23": 0.3,
                "v24": 0.4,
                "v25": 0.1,
                "v26": -0.1,
                "v27": 0.2,
                "v28": 0.1,
                "amount": 150.0,
            },
        ]
    )
    result = predict_batch(input_data)
    assert isinstance(result, PredictionOutputBatch)
    assert len(result.predictions) == 2
    for prediction in result.predictions:
        assert isinstance(prediction, int)  # Assuming binary classification


def test_predict_batch_invalid_input_wrong_type() -> None:
    with pytest.raises(ValidationError):  # Changed from TypeError to ValidationError
        input_data = PredictionInputBatch(
            inputs=[  # Changed from 'data' to 'inputs'
                {
                    "time": 100000,
                    "v1": 0.5,
                    "v2": "invalid_type",
                    "v3": 3.3,
                    "v4": 0.0,
                    "v5": 0.1,
                    "v6": -1.2,
                    "v7": 0.3,
                    "v8": 1.1,
                    "v9": -0.5,
                    "v10": 0.2,
                    "v11": -1.0,
                    "v12": 0.4,
                    "v13": 0.1,
                    "v14": -0.3,
                    "v15": 0.2,
                    "v16": 0.0,
                    "v17": 0.1,
                    "v18": -0.2,
                    "v19": 0.3,
                    "v20": 0.0,
                    "v21": 0.1,
                    "v22": -0.1,
                    "v23": 0.2,
                    "v24": 0.3,
                    "v25": 0.0,
                    "v26": -0.2,
                    "v27": 0.1,
                    "v28": 0.0,
                    "amount": 100.0,
                }
            ]
        )
        predict_batch(input_data)
