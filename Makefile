########################################################################################################################
# 🚀 Project Installation
########################################################################################################################

.PHONY: install
install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv..."
	@uv sync

########################################################################################################################
# 🚀 Quality Checks
########################################################################################################################

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code with pytest..."
	@uv run pytest tests

.PHONY: format-check
format-check: ## Check the formatting of the code
	@echo "🚀 Checking code formatting with ruff..."
	@uvx ruff format --check src tests

.PHONY: format-fix
format-fix: ## Fix the formatting of the code
	@echo "🚀 Fixing code formatting with ruff..."
	@uvx ruff format src tests

.PHONY: lint-check
lint-check: ## Check the code with ruff
	@echo "🚀 Checking code lint with ruff..."
	@uvx ruff check src tests

.PHONY: lint-fix
lint-fix: ## Fix the code with ruff
	@echo "🚀 Fixing code lint with ruff..."
	@uvx ruff check src tests --fix

.PHONY: type-check
type-check: ## Check the types of the code with mypy
	@echo "🚀 Checking code types with mypy..."
	@uvx mypy src


########################################################################################################################
# 🚀 API
########################################################################################################################

.PHONY: start-api
start-api: ## Start the API
	@echo "🚀 Starting the API..."
	@docker-compose up -d


########################################################################################################################
# 🚀 Deployment
########################################################################################################################

AWS_ACCOUNT_URL=072425947059.dkr.ecr.us-east-2.amazonaws.com
AWS_REGION=us-east-2
ECR_REPOSITORY_NAME=default_api_image
ECS_CLUSTER_NAME=default_api_cluster
ECS_SERVICE_NAME=default_api_service
IMAGE_URL=${AWS_ACCOUNT_URL}/${ECR_REPOSITORY_NAME}

.PHONY: ecr-login
ecr-login: ## Log in to AWS ECR
	@echo "🚀 Logging in to AWS ECR..."
	@aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_URL}

.PHONY: redeploy-ecs-service
redeploy-ecs-service: ## Force redeployment of ECS service
	@echo "🚀 Redeploying ECS service..."
	@aws ecs update-service --cluster ${ECS_CLUSTER_NAME} --service ${ECS_SERVICE_NAME} --force-new-deployment --region=${AWS_REGION}

.PHONY: deploy-api-from-x86
deploy-api-from-x86: ## Deploy the API using a standard x86 build
	@echo "🚀 Deploying API from x86..."
	make ecr-login
	docker build . -t api
	docker tag api ${IMAGE_URL}:latest
	docker push ${IMAGE_URL}:latest
	make redeploy-ecs-service

.PHONY: deploy-api-from-arm
deploy-api-from-arm: ## Deploy the API using an ARM build (Mac M1, M2)
	@echo "🚀 Deploying API from ARM..."
	make ecr-login
	docker buildx build --platform linux/amd64 --push -t ${IMAGE_URL}:latest .
	make redeploy-ecs-service

########################################################################################################################
# 🚀 DVC
########################################################################################################################

.PHONY: repro
repro: ## Reproduce DVC pipeline
	@echo "🚀 Running DVC repro..."
	@uv run dvc repro

########################################################################################################################
# 🚀 MLFLOW
########################################################################################################################

.PHONY: mlflow-start
mlflow-start: ## Start the MLflow server
	@echo "🚀 Starting MLflow server..."
	@mlflow server --host 127.0.0.1 --port 8080
########################################################################################################################
# 🚀 Help
########################################################################################################################

.PHONY: help
help:
	@echo "================================================="
	@echo "🚀 Fraud Detector 3000 – Available Make Targets:"
	@echo "================================================="
	@uv run python -c "import re; [print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z-]+):.*?## (.*)$$', open('Makefile').read(), re.M)]"

.DEFAULT_GOAL := help
