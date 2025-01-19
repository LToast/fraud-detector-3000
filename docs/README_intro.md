# Fraud Detector 3000

## Project Overview
Fraud Detector 3000 is a comprehensive credit card fraud detection system designed with a robust machine learning pipeline. The project leverages modern technologies to ensure scalable data processing, model training, deployment, and monitoring, making it suitable for real-world financial applications.

## Technologies Used
- **Programming Language:** Python 3.12
- **Web Framework:** FastAPI
- **Machine Learning:** Scikit-learn, MLflow
- **Data Management:** DVC (Data Version Control)
- **Containerization:** Docker
- **Infrastructure as Code:** Terraform
- **Version Control:** Git
- **Static Analysis & Formatting:** Ruff, Mypy
- **Logging:** Loguru
- **Testing:** Pytest
- **Dependency Management:** uv

## Project Structure
```markdown
fraud-detector-3000/
├── Dockerfile
├── Makefile
├── README.md
├── data/
│   ├── external/
│   ├── interim/
│   ├── processed/
│   └── raw/
├── docs/
├── models/
├── notebooks/
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── main.py
│   │   └── routes.py
│   ├── data/
│   │   └── make_dataset.py
│   ├── features/
│   │   └── build_features.py
│   ├── fraud_detector/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── prepare.py
│   │   └── train.py
│   └── scripts/
│       ├── prepare_model.py
│       └── __init__.py
├── tests/
│   └── __init__.py
├── tox.ini
├── pyproject.toml
└── uv.lock
```

## Overall Pipeline

1. **Data Preparation**
   - Raw data is stored in the `data/raw/` directory.
   - The `prepare_model.py` script processes raw data, normalizes column names, and splits the data into training, validation, and testing sets using parameters defined in `PrepareModelParams`.
   - Processed data is saved in the `data/processed/` directory.

2. **Model Training**
   - The `train_model.py` script handles model training using Scikit-learn.
   - Training parameters are managed through `TrainModelParams`.
   - MLflow is integrated for experiment tracking, parameter logging, and model registration.
   - Trained models are saved locally and registered in the MLflow Model Registry, transitioning to the Production stage upon successful training.


3. **Model Evaluation**
   - The `evaluate_model.py` script handles model training using Scikit-learn.
   - Training parameters are managed through `params.yaml`.
   - MLflow is integrated for experiment tracking, parameter logging, and model registration.
   - Trained models are saved locally and registered in the MLflow Model Registry, transitioning to the Production stage upon successful training.

4. **API Deployment**
   - A FastAPI-based API is developed to serve the trained model for batch predictions.
   - The API code resides in the `src/api/` directory.
   - Docker is used to containerize the API, with a multi-stage `Dockerfile` ensuring a lightweight image.
   - The API is deployed using Docker Compose, with health checks to ensure reliability.

5. **Infrastructure Management**
   - Terraform is utilized to provision and manage AWS infrastructure required for the project.
   - Infrastructure code is organized within the `terraform/` directory, enabling reproducible deployments.

6. **Data Versioning**
   - DVC manages data versioning, ensuring that data transformations and model versions are tracked and reproducible.

7. **Testing and Quality Assurance**
   - Pytest is used for unit testing, ensuring code reliability.
   - Ruff and Mypy enforce code formatting and type checking, maintaining code quality.
   - Git hooks are installed to automate checks before commits and pushes.

8. **Continuous Integration and Deployment**
   - Makefile scripts facilitate common tasks such as installing dependencies, running tests, formatting code, and deploying the API.
   - The pipeline ensures that changes are consistently tested and deployed, minimizing downtime and errors.

## GitHub Secrets
Ensure the following secrets are added to your GitHub repository to securely inject credentials into the workflow:

* ``AWS_ACCESS_KEY_ID``: Your AWS access key ID.
* ``AWS_SECRET_ACCESS_KEY``: Your AWS secret access key.
* ``AWS_REGION``: The AWS region where your ECR and ECS services are hosted.
* ``ECR_URL``: The URL of your AWS Elastic Container Registry.
* ``MODEL_NAME``: The name of the model to promote.
* ``STAGE``: The stage to which the model should be promoted (e.g., staging, production).

## Conclusion
Fraud Detector 3000 exemplifies a modern machine learning project with end-to-end capabilities, from data processing and model training to deployment and infrastructure management. The integration of tools like MLflow, DVC, Docker, and Terraform ensures scalability, reproducibility, and maintainability, making it a strong candidate for technical evaluations and real-world applications.
