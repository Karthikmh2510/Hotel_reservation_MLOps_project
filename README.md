# Hotel Reservation MLOps Project

<img alt="CI" src="https://img.shields.io/badge/build-passing-brightgreen">  <img alt="License" src="https://img.shields.io/badge/license-CC%20BY--NC%204.0-blue">

Predict booking **cancellations** in real time while showcasing an end‑to‑end, production‑ready **MLOps** workflow—data & code versioning, automated training, experiment management, containerised serving, and CI/CD deployment to **Google Cloud Run**.

---

## Table of Contents

1. [Project Features](#project-features)
2. [Repository Structure](#repository-structure)
3. [Quick Start](#quick-start)
4. [Detailed Setup](#detailed-setup)
   
      4.1 [Environment & Dependencies](#41-environment--dependencies)
   
      4.2 [Data Versioning (DVC)](#42-data-versioning-dvc)
   
      4.3 [Model Training Pipeline](#43-model-training-pipeline)
   
      4.4 [Experiment Tracking (MLflow)](#44-experiment-tracking-mlflow)
   
      4.5 [Containerisation & API Service](#45-containerisation--api-service)
   
      4.6 [CI/CD with Jenkins → Cloud Run](#46-cicd-with-jenkins--cloud-run)
   
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Local Reproducibility Checklist](#local-reproducibility-checklist)
8. [Road‑Map](#road-map)
9. [Acknowledgements](#acknowledgements)
10. [License](#license)

---

## Project Features

* **Binary cancellation classifier** using a Kaggle dataset (\~40 k bookings, 31 features).
* **Fully version‑controlled** datasets & models via [DVC](https://dvc.org).
* **Experiment lineage** captured with [MLflow](https://mlflow.org).
* **Dockerised micro‑service** built on Flask + Gunicorn (< 200 MB).
* **Declarative Jenkins pipeline** for Build → Test → Package → Deploy.
* **Managed serving** on Google Cloud Run with zero‑downtime roll‑outs.
* **KS‑stat drift alerts** and Slack notifications.
* **Unit & integration tests** ensuring data‑schema and model API integrity.

---

## Repository Structure

```text
├── src/                       # Core Python packages
│   └── components/
│       └── data_processing.py # Cleaning, encoding, splitting
├── pipeline/
│   ├── training_pipeline.py   # End‑to‑end DAG
│   └── params.yaml            # Hyper‑parameters & environment vars
├── notebooks/                 # EDA & validation notebooks
├── tests/                     # PyTest suites
├── application.py             # Flask prediction service
├── templates/index.html       # Simple UI
├── static/                    # CSS/JS assets
├── Dockerfile                 # Multi‑stage build
├── Jenkinsfile                # CI/CD pipeline
├── data/                      # DVC‑tracked raw & processed data
├── models/                    # Versioned model binaries
├── reports/                   # Auto‑generated diagnostics
├── mlruns/                    # Local MLflow store
└── README.md                  # You are here.
```

---

## Quick Start

```bash
git clone https://github.com/Karthikmh2510/Hotel_reservation_MLOps_project.git
cd Hotel_reservation_MLOps_project
make install          # optional helper—creates venv & installs reqs
make pipeline         # runs full training DAG & logs to MLflow
make serve-docker     # builds image & serves on http://localhost:8080/
```

---

## Detailed Setup

### 4.1 Environment & Dependencies

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 4.2 Data Versioning (DVC)

```bash
# Download raw CSV via Kaggle API
kaggle datasets download ...

# Track with DVC
dvc add data/raw/hotel.csv
dvc push               # remote defined in .dvc/config
```

### 4.3 Model Training Pipeline

```bash
python pipeline/training_pipeline.py
# Steps: ingest → process → split → train → evaluate → register
```

Artifacts & metrics land in **`mlruns/`** and the best model is placed in **`models/`**.

### 4.4 Experiment Tracking (MLflow)

```bash
mlflow ui              # http://localhost:5000
```

View parameter grids, metric curves, and ROC charts.

### 4.5 Containerisation & API Service

```bash
docker build -t hotel-ml:latest .
docker run -p 8080:8080 hotel-ml:latest
```

Submit JSON or use the simple web form at `/`.

### 4.6 CI/CD with Jenkins → Cloud Run

1. **Build** – Python setup, PyTest, `dvc pull`.
2. **Package** – Docker build & tag `gcr.io/$PROJECT/hotel-ml:$BUILD_ID`.
3. **Deploy** – `gcloud run deploy hotel-ml`.

Logs & images archived to **Artifact Registry**.

---

## Monitoring & Maintenance

* **KS‑stat drift detector** scheduled via Cloud Scheduler; Slack alert at > 0.20.
* **Cloud Logging** & **Cloud Monitoring** dashboards for latency, 5xx rates, CPU & memory.
* **Canary roll‑outs**: 10 % traffic for 30 min; automatic rollback on error‑budget breach.

---

## Local Reproducibility Checklist

```bash
cp .env.example .env        # add Postgres creds & MLflow URI
dvc pull                    # fetch data & model blobs
pytest                      # run unit tests
```

---

## Road‑Map

* [ ] Switch Flask → **FastAPI** for async throughput & OpenAPI docs.
* [ ] Integrate **Feast** feature store for on‑line/off‑line parity.
* [ ] Achieve > 90 % test coverage; add Codecov badge.
* [ ] Migrate PR checks to **GitHub Actions**.

---

## Acknowledgements

Project completed with guidance from the Udemy course:
“Simply streamline ML pipelines with Kubernetes, GitLab CI, Jenkins, Prometheus, Grafana, Kubeflow & Minikube on GCP” (4.5 ⭐, 112 lectures, 54.5 h, updated March 2025) by Krish AI Technologies / Sudhanshu Gusain 
udemy.com.

Concepts around scalable CI/CD, Kubernetes workflows, and observability learned there informed the design and automation choices in this repository.


---

## License

This repository is released under the MIT License. Kaggle data retains its original CC BY-NC 4.0 terms; please ensure non-commercial use when training or deploying derivative models.
