from mlflow.tracking import MlflowClient  # type: ignore


def promote_model(model_name: str, stage: str):
    client = MlflowClient()
    latest_version = client.get_latest_versions(model_name, stages=["None"])[0]
    client.transition_model_version_stage(
        name=model_name, version=latest_version.version, stage=stage
    )
    print(f"Promoted model {model_name} version {latest_version.version} to {stage}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Model name to promote")
    parser.add_argument(
        "--stage",
        required=True,
        choices=["Staging", "Production"],
        help="Stage to promote to",
    )
    args = parser.parse_args()

    promote_model(args.model, args.stage)
