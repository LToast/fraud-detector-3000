# mypy: ignore-errors
from pydantic import BaseModel, Field, ConfigDict, Extra
from typing import List


class PrepareModelParams(BaseModel):
    raw_data: str
    split: float
    seed: int


class TrainModelParams(BaseModel):
    train_csv: str
    valid_csv: str
    model_path: str
    split: float
    seed: int
    rfc_metric: str
    n_estimators: int
    n_jobs: int


class EvaluateModelParams(BaseModel):
    model_path: str
    valid_csv: str
    evaluation_path: str
    seed: int


# Added API Prediction Models
class PredictionInput(BaseModel):
    model_config = ConfigDict(extra=Extra.forbid)

    time: int = Field(..., alias="Time")
    v1: float = Field(..., alias="V1")
    v2: float = Field(..., alias="V2")
    v3: float = Field(..., alias="V3")
    v4: float = Field(..., alias="V4")
    v5: float = Field(..., alias="V5")
    v6: float = Field(..., alias="V6")
    v7: float = Field(..., alias="V7")
    v8: float = Field(..., alias="V8")
    v9: float = Field(..., alias="V9")
    v10: float = Field(..., alias="V10")
    v11: float = Field(..., alias="V11")
    v12: float = Field(..., alias="V12")
    v13: float = Field(..., alias="V13")
    v14: float = Field(..., alias="V14")
    v15: float = Field(..., alias="V15")
    v16: float = Field(..., alias="V16")
    v17: float = Field(..., alias="V17")
    v18: float = Field(..., alias="V18")
    v19: float = Field(..., alias="V19")
    v20: float = Field(..., alias="V20")
    v21: float = Field(..., alias="V21")
    v22: float = Field(..., alias="V22")
    v23: float = Field(..., alias="V23")
    v24: float = Field(..., alias="V24")
    v25: float = Field(..., alias="V25")
    v26: float = Field(..., alias="V26")
    v27: float = Field(..., alias="V27")
    v28: float = Field(..., alias="V28")
    amount: float = Field(..., alias="Amount")


class PredictionOutput(BaseModel):
    prediction: int  # or the appropriate type based on your model's output


# Added Batch Prediction Models
class PredictionInputBatch(BaseModel):
    model_config = ConfigDict(extra=Extra.forbid)
    inputs: List[PredictionInput]


class PredictionOutputBatch(BaseModel):
    predictions: List[int]  # or the appropriate type based on your model's output
