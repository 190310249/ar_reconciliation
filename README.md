# AR Reconciliation

This project provides tools and scripts for automating and managing Accounts Receivable (AR) reconciliation.

---

## Overview

The AR Reconciliation module is an asynchronous workflow engine designed to automate ERP reconciliation processes. It leverages:

- **Django REST Framework** for API endpoints
- **Celery** for distributed async task execution
- **Redis** as a message broker
- **PostgreSQL** for persistent workflow state
- **Docker** and **Nginx** for containerized deployment

---

## Features

- Automated AR data processing
- Modular workflow stages: Ingestion, Matching, Validation, Decision Routing
- Asynchronous execution with retry and failure recovery
- Persistent workflow state and resumability
- Duplicate-safe submissions and idempotency
- Parallel execution with Celery workers
- Error handling and logging

---

## Architecture

```text
Dataset
    ↓
Django Loader Script
    ↓
Workflow DB Entry
    ↓
Celery Async Tasks
    ↓
INGESTION
    ↓
MATCHING
    ↓
VALIDATION
    ↓
DECISION ROUTING
    ↓
Workflow Completion
```

---

## Tech Stack

| Component        | Technology            |
| ---------------- | --------------------- |
| Backend          | Django REST Framework |
| Async Processing | Celery                |
| Message Broker   | Redis                 |
| Database         | PostgreSQL            |
| Reverse Proxy    | Nginx                 |
| Containerization | Docker                |
| Dataset Source   | KaggleHub             |

---

## Project Structure

```text
ar_reconciliation/
│
├── config/
├── workflows/
├── reconciliation/
├── nginx/
├── scripts/
├── data/
│   ├── postgres/
│   └── raw/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
└── .env
```

---

## .env Structure

Example `.env` file:

```env (should be hidden)
DEBUG=True
SECRET_KEY='django-insecure-)g(z@8rh4qg^+6ut@4$qri&lanuc31hejnq6#s)ou=^^7+xv0e'
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
POSTGRES_DB=ar_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
TIME_ZONE=Asia/Kolkata
```

---

## Workflow Stages

1. **Ingestion**: Reads ERP records, creates workflow entries, stores payload.
2. **Matching**: Performs reconciliation logic.
3. **Validation**: Checks required fields, invalid values, negative amounts.
4. **Decision Routing**: Routes to AUTO_APPROVED, MANUAL_REVIEW, or REJECTED.

---

## Database Models

- **Workflow Model**: Tracks state, retries, stage progress, payload.
- **StageExecution Model**: Tracks execution history, failures, retries, timestamps.

---

## API Endpoints

- **Create Workflow**: `POST /workflows/submit/`
- **List Workflows**: `GET /workflows/`
- **Workflow Details**: `GET /workflows/<workflow_id>/`

**Example Request:**
```json
{
  "external_id": "INV-1001",
  "Customer ID": "CUST-1001",
  "Invoice Total": 2000,
  "Invoice applied amount": 500,
  "Payment Total": 1400,
  "Payment applied amount": 0,
  "Customer Balance": 100
}
```

---

## Dataset

Source: [Kaggle - AI Powered ERP AR Reconciliation](https://www.kaggle.com/datasets/asiryi/ai-powered-erp-ar-reconciliation)  
Automatically downloaded using KaggleHub.

---

## Getting Started

1. **Clone the repository:**
     ```bash
     git clone <https://github.com/190310249/ar_reconciliation.git>
     ```
2. **Install dependencies:**
     ```bash
     pip install -r requirements.txt
     ```
3. **Run the main script:**
     ```bash
     python main.py
     ```

---

## Setup Instructions

1. **Clone Repository**
     ```bash
     git clone <https://github.com/190310249/ar_reconciliation.git>
     ```
2. **Start Containers**
     ```bash
     docker compose up --build
     ```
3. **Create Superuser**
     ```bash
     docker compose exec django python manage.py createsuperuser
     ```

---

## Admin Dashboard

Visit [http://localhost/admin](http://localhost/admin) for workflow monitoring, retry visibility, stage tracking, payload inspection, and error debugging.

---

## Example Workflow Lifecycle

```text
INGESTION → SUCCESS
MATCHING → SUCCESS
VALIDATION → FAILED
VALIDATION → SUCCESS
DECISION → SUCCESS
```

---

## Retry Behaviour

- Each stage: max 3 retries, automatic scheduling, persisted retry count

---

## Concurrency

- Celery workers run with `--concurrency=4` for parallel workflow execution

---

## Production Considerations

Potential improvements:

- Distributed tracing
- Prometheus metrics
- Kafka integration
- Workflow dashboards
- Multi-worker scaling
- Dead-letter queues
- Audit pipelines

---

## Folder Structure

- `src/` - Source code
- `data/` - Input and output files
- `tests/` - Test cases

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## License

This project is licensed under the MIT License.

---

## Author

Pratik Kumar

