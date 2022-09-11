# Ml Playground Api

Provide ML services base structure.

- Analysis jupyter notebook
- Train model
- Publish ml model via api.

## Getting Started

### Setup

setup local virtual env

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/dev_requirements.txt
```

or setup via docker

```shell
docker-compose up
```

### Datasets

Download dataset from kaggle and place under datasets directory

### Generate Model

```shell
python -m ml_models.{ domain }.generate_model
```

### Run server

```shell
uvicorn api.main:app --reload
```

### Run unit test

```shell
pytest tests
```

## Deploy to Google Cloud via Terraform

### Setup

download `keyfile.json` for authentication from google platform.

add `terraform.tfvars` and set google iam info.

### Deploy

```shell
terraform init
terraform apply
```

### Clean up

```shell
terraform destroy
```
