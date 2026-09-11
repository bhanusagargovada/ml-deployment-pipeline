# ML Model Deployment Pipeline

An end-to-end MLOps pipeline: train a churn-prediction model, serve it via a
Flask REST API, containerize it with Docker, and deploy it to AWS EC2 with
CI/CD via GitHub Actions.

## Architecture

```
 ┌──────────────┐      ┌─────────────┐      ┌────────────┐      ┌───────────┐
 │  train.py     │ -->  │ model.pkl   │ -->  │ Flask API  │ -->  │  Docker    │
 │ (scikit-learn)│      │ (artifact)  │      │ /predict   │      │  Image     │
 └──────────────┘      └─────────────┘      └────────────┘      └─────┬─────┘
                                                                        │
                                                    ┌───────────────────┘
                                                    ▼
                                     ┌─────────────────────────────┐
                                     │ GitHub Actions CI           │
                                     │ build -> push -> deploy      │
                                     └──────────────┬──────────────┘
                                                    ▼
                                     ┌─────────────────────────────┐
                                     │ AWS EC2 (Terraform-provisioned)│
                                     │ running the container        │
                                     └─────────────────────────────┘
```

## Tech Stack

- **Model:** scikit-learn (RandomForestClassifier)
- **API:** Flask + Gunicorn
- **Containerization:** Docker
- **Infra:** Terraform (AWS EC2) — see [terraform-aws-infrastructure](#)
- **CI/CD:** GitHub Actions

## Problem

Predicts whether a customer will churn based on tenure, billing, contract
type, and support interaction history — a common business ML use case.

## Project Structure

```
ml-deployment-pipeline/
├── model/
│   ├── train.py           # trains and saves the model
│   ├── model.pkl          # serialized model + feature list
│   └── requirements.txt
├── app/
│   ├── app.py              # Flask API
│   └── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/deploy.yml
└── README.md
```

## Running Locally

### 1. Train the model
```bash
cd model
pip install -r requirements.txt
python train.py
```

### 2. Run the API
```bash
cd app
pip install -r requirements.txt
python app.py
```

### 3. Run with Docker
```bash
docker compose up --build
```

## API Reference

### `GET /health`
Returns `{"status": "ok"}`.

### `POST /predict`
Request body:
```json
{
  "tenure_months": 3,
  "monthly_charges": 95.5,
  "total_charges": 300.0,
  "contract_type": 0,
  "support_calls": 5,
  "has_internet_service": 1
}
```

Response:
```json
{
  "churn_prediction": 1,
  "churn_probability": 0.9266,
  "label": "will churn"
}
```

`contract_type`: `0` = month-to-month, `1` = one-year, `2` = two-year.

## Model Performance

- Accuracy: ~90%
- Precision (churn class): ~0.87
- Recall (churn class): ~0.66

## Deployment

The GitHub Actions workflow builds the Docker image on every push to `main`
and pushes it to Docker Hub. Deployment to EC2 can be enabled by uncommenting
the `Deploy to EC2` step in `.github/workflows/deploy.yml` and adding the
relevant secrets.

### Infra (cost-controlled)

The `infra/` folder provisions the EC2 instance via Terraform, gated behind
a `create_ec2` variable that defaults to `false` — no instance is created,
so there's no cost, until you explicitly turn it on:

```bash
cd infra
terraform init
terraform plan                                   # create_ec2 = false, nothing created
terraform apply -var="create_ec2=true"            # spins up the instance for a demo
terraform apply -var="create_ec2=false"           # tears it back down when done
```

Always run the teardown command after a demo to avoid ongoing EC2 charges.

## Author

Bhanu Sagar Govada — B.Tech CSE, DevOps/Cloud/Backend focus.
