"""Tests for `api/main.py`."""

from src.api.main import app  # Changed import to use the FastAPI app
from src.api.main import health_check_route

from src.api.types import HealthRouteOutput

from fastapi.testclient import TestClient

# Initialize TestClient with the FastAPI app
client = TestClient(app)  # Updated initialization


def test_health_check_route() -> None:
    assert health_check_route() == HealthRouteOutput(status="ok")


def test_predict_valid_input() -> None:
    input_data = {
        "Time": 100000,
        "V1": 0.5,
        "V2": 1.2,
        "V3": 3.3,
        "V4": 0.0,
        "V5": 0.1,
        "V6": -1.2,
        "V7": 0.3,
        "V8": 1.1,
        "V9": -0.5,
        "V10": 0.2,
        "V11": -1.0,
        "V12": 0.4,
        "V13": 0.1,
        "V14": -0.3,
        "V15": 0.2,
        "V16": 0.0,
        "V17": 0.1,
        "V18": -0.2,
        "V19": 0.3,
        "V20": 0.0,
        "V21": 0.1,
        "V22": -0.1,
        "V23": 0.2,
        "V24": 0.3,
        "V25": 0.0,
        "V26": -0.2,
        "V27": 0.1,
        "V28": 0.0,
        "Amount": 100.0,
    }
    response = client.post("/predict_one", json=input_data)  # Changed to send JSON
    assert response.status_code == 200
    result = response.json()
    assert "prediction" in result
    assert isinstance(result["prediction"], int)


def test_predict_invalid_input_missing_field() -> None:
    input_data = {
        "Time": 100000,
        "V1": 0.5,
        "V2": 1.2,
        "V3": 3.3,
        "V4": 0.0,
        "V5": 0.1,
        "V6": -1.2,
        "V7": 0.3,
        "V8": 1.1,
        "V9": -0.5,
        "V10": 0.2,
        "V11": -1.0,
        "V12": 0.4,
        "V13": 0.1,
        "V14": -0.3,
        "V15": 0.2,
        "V16": 0.0,
        "V17": 0.1,
        "V18": -0.2,
        "V19": 0.3,
        "V20": 0.0,
        "V21": 0.1,
        "V22": -0.1,
        "V23": 0.2,
        "V24": 0.3,
        "V25": 0.0,
        "V26": -0.2,
        "V27": 0.1,
        "V28": 0.0,
        # "Amount" is missing
    }
    response = client.post("/predict_one", json=input_data)
    assert response.status_code == 422  # Unprocessable Entity


def test_predict_invalid_input_wrong_type() -> None:
    input_data = {
        "Time": 100000,
        "V1": 0.5,
        "V2": "invalid_type",  # Wrong type
        "V3": 3.3,
        "V4": 0.0,
        "V5": 0.1,
        "V6": -1.2,
        "V7": 0.3,
        "V8": 1.1,
        "V9": -0.5,
        "V10": 0.2,
        "V11": -1.0,
        "V12": 0.4,
        "V13": 0.1,
        "V14": -0.3,
        "V15": 0.2,
        "V16": 0.0,
        "V17": 0.1,
        "V18": -0.2,
        "V19": 0.3,
        "V20": 0.0,
        "V21": 0.1,
        "V22": -0.1,
        "V23": 0.2,
        "V24": 0.3,
        "V25": 0.0,
        "V26": -0.2,
        "V27": 0.1,
        "V28": 0.0,
        "Amount": 100.0,
    }
    response = client.post("/predict_one", json=input_data)
    assert response.status_code == 422  # Unprocessable Entity


def test_predict_batch_valid_input() -> None:
    input_data = {
        "inputs": [
            {
                "Time": 100000,
                "V1": 0.5,
                "V2": 1.2,
                "V3": 3.3,
                "V4": 0.0,
                "V5": 0.1,
                "V6": -1.2,
                "V7": 0.3,
                "V8": 1.1,
                "V9": -0.5,
                "V10": 0.2,
                "V11": -1.0,
                "V12": 0.4,
                "V13": 0.1,
                "V14": -0.3,
                "V15": 0.2,
                "V16": 0.0,
                "V17": 0.1,
                "V18": -0.2,
                "V19": 0.3,
                "V20": 0.0,
                "V21": 0.1,
                "V22": -0.1,
                "V23": 0.2,
                "V24": 0.3,
                "V25": 0.0,
                "V26": -0.2,
                "V27": 0.1,
                "V28": 0.0,
                "Amount": 100.0,
            },
            {
                "Time": 100001,
                "V1": 0.6,
                "V2": 1.5,
                "V3": 3.5,
                "V4": 0.1,
                "V5": 0.2,
                "V6": -1.1,
                "V7": 0.4,
                "V8": 1.2,
                "V9": -0.4,
                "V10": 0.3,
                "V11": -0.9,
                "V12": 0.5,
                "V13": 0.2,
                "V14": -0.2,
                "V15": 0.3,
                "V16": 0.1,
                "V17": 0.2,
                "V18": -0.1,
                "V19": 0.4,
                "V20": 0.1,
                "V21": 0.2,
                "V22": -0.2,
                "V23": 0.3,
                "V24": 0.4,
                "V25": 0.1,
                "V26": -0.1,
                "V27": 0.2,
                "V28": 0.1,
                "Amount": 150.0,
            },
        ]
    }
    response = client.post("/predict_batch", json=input_data)
    assert response.status_code == 200
    result = response.json()
    assert "predictions" in result
    assert len(result["predictions"]) == 2
    for prediction in result["predictions"]:
        assert isinstance(prediction, int)


def test_predict_batch_invalid_input_wrong_type() -> None:
    input_data = {
        "inputs": [
            {
                "Time": 100000,
                "V1": 0.5,
                "V2": "invalid_type",  # Wrong type
                "V3": 3.3,
                "V4": 0.0,
                "V5": 0.1,
                "V6": -1.2,
                "V7": 0.3,
                "V8": 1.1,
                "V9": -0.5,
                "V10": 0.2,
                "V11": -1.0,
                "V12": 0.4,
                "V13": 0.1,
                "V14": -0.3,
                "V15": 0.2,
                "V16": 0.0,
                "V17": 0.1,
                "V18": -0.2,
                "V19": 0.3,
                "V20": 0.0,
                "V21": 0.1,
                "V22": -0.1,
                "V23": 0.2,
                "V24": 0.3,
                "V25": 0.0,
                "V26": -0.2,
                "V27": 0.1,
                "V28": 0.0,
                "Amount": 100.0,
            }
        ]
    }
    response = client.post("/predict_batch", json=input_data)
    assert response.status_code == 422  # Unprocessable Entity
