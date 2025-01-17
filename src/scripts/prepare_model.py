import sys
from pathlib import Path
import argparse  # Added import

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.fraud_detector.prepare import prepare_data
from src.fraud_detector.types import PrepareModelParams  # Imported from schemas.py


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare model data.")
    parser.add_argument(
        "--raw_data-path", type=str, required=True, help="Path to raw data"
    )
    parser.add_argument("--split", type=float, required=True, help="Data split ratio")
    parser.add_argument("--seed", type=int, required=True, help="Random seed")
    args = parser.parse_args()

    params = PrepareModelParams(
        raw_data=args.raw_data_path, split=args.split, seed=args.seed
    )

    prepare_data(params)


if __name__ == "__main__":
    main()
