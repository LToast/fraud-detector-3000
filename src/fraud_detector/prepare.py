import pandas as pd  # type: ignore
from sklearn.model_selection import train_test_split  # type: ignore
import os
from src.fraud_detector.constants import PROJECT_ROOT_PATH
from src.fraud_detector.types import PrepareModelParams  # Imported from schemas.py
import argparse


def prepare_data(params: PrepareModelParams) -> None:
    os.makedirs(os.path.join(PROJECT_ROOT_PATH, "data", "processed"), exist_ok=True)

    data_df = pd.read_csv(params.raw_data)
    data_df.columns = data_df.columns.str.lower()  # Normalize column names to lowercase

    train_df, test_df = train_test_split(
        data_df, test_size=params.split, random_state=params.seed, shuffle=True
    )

    train_df, valid_df = train_test_split(
        train_df, test_size=params.split, random_state=params.seed, shuffle=True
    )
    train_df.to_csv(
        os.path.join(PROJECT_ROOT_PATH, "data/processed/train.csv"), index=False
    )
    test_df.to_csv(
        os.path.join(PROJECT_ROOT_PATH, "data/processed/test.csv"), index=False
    )
    valid_df.to_csv(
        os.path.join(PROJECT_ROOT_PATH, "data/processed/valid.csv"), index=False
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare the fraud detection dataset.")
    parser.add_argument(
        "--raw_data", type=str, required=True, help="Path to raw CSV data"
    )
    parser.add_argument("--split", type=float, required=True, help="Data split ratio")
    parser.add_argument("--seed", type=int, required=True, help="Random seed")
    args = parser.parse_args()

    params = PrepareModelParams(
        raw_data=args.raw_data, split=args.split, seed=args.seed
    )

    prepare_data(params)


if __name__ == "__main__":
    main()
