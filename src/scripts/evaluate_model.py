import sys
from pathlib import Path
import argparse  # Added import

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.fraud_detector.evaluate import evaluate_model
from src.fraud_detector.types import EvaluateModelParams  # Imported from schemas.py


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the fraud detection model.")
    parser.add_argument(
        "--model_path", type=str, required=True, help="Path to the trained model"
    )
    parser.add_argument(
        "--valid_csv", type=str, required=True, help="Path to validation CSV"
    )
    parser.add_argument(
        "--evaluation_path",
        type=str,
        required=True,
        help="Path to save evaluation metrics",
    )
    parser.add_argument("--seed", type=int, required=True, help="Random seed")
    args = parser.parse_args()

    params = EvaluateModelParams(
        model_path=args.model_path,
        valid_csv=args.valid_csv,
        evaluation_path=args.evaluation_path,
        seed=args.seed,
    )

    evaluate_model(params)


if __name__ == "__main__":
    main()  # type: ignore
