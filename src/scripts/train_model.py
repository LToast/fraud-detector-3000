import sys
from pathlib import Path
import argparse  # Added import

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.fraud_detector.train import train_model
from src.fraud_detector.types import TrainModelParams  # Imported from schemas.py


def main() -> None:
    """
    Entrypoint for training a random forest model using command-line parameters.
    """
    parser = argparse.ArgumentParser(description="Train the fraud detection model.")
    parser.add_argument(
        "--train_csv", type=str, required=True, help="Path to training CSV"
    )
    parser.add_argument(
        "--valid_csv", type=str, required=True, help="Path to validation CSV"
    )
    parser.add_argument(
        "--model_path", type=str, required=True, help="Path to save the model"
    )
    parser.add_argument("--split", type=float, required=True, help="Data split ratio")
    parser.add_argument("--seed", type=int, required=True, help="Random seed")
    parser.add_argument("--rfc_metric", type=str, required=True, help="Metric for RFC")
    parser.add_argument(
        "--n_estimators", type=int, required=True, help="Number of estimators for RFC"
    )
    parser.add_argument(
        "--n_jobs", type=int, required=True, help="Number of parallel jobs for RFC"
    )
    args = parser.parse_args()

    params = TrainModelParams(
        train_csv=args.train_csv,
        valid_csv=args.valid_csv,
        model_path=args.model_path,
        split=args.split,
        seed=args.seed,
        rfc_metric=args.rfc_metric,
        n_estimators=args.n_estimators,
        n_jobs=args.n_jobs,
    )

    train_model(params)  # Updated to pass the params object directly


if __name__ == "__main__":
    main()
