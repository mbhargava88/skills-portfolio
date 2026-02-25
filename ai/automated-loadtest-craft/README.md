# Antigravity Load-Testing Automation System

This system automates the generation of k6 load-testing bundles using traffic data from Grafana, code analysis from GitHub, and LLM-generated scripts via Groq.

## Architecture

The system follows Domain-Driven Design (DDD) and Clean Architecture principles, orchestrated by a StateGraph.

- **Domain Layer**: Core entities and use cases.
- **Infrastructure Layer**: Clients for Grafana, GitHub, Groq, and S3.
- **Application Layer**: Orchestrator using LangGraph.
- **Frontend**: Streamlit application.

## Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Groq API Key
- GitHub Token
- AWS Credentials (for S3)

## Setup

1. **Clone the repository** (if not already done).

2. **Environment Variables**:
   Copy `.env.example` to `.env` and fill in your credentials.
   ```bash
   cp .env.example .env
   # Edit .env
   ```

3. **Install Dependencies (Local)**:
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

### Using Streamlit directly
```bash
make run
```
Access the UI at `http://localhost:8501`.

### Using Docker
```bash
make build
docker-compose up
```

## Deployment (Minikube)

1. Ensure Minikube is running.
2. Deploy manifests:
   ```bash
   make deploy-minikube
   ```
   *Note: You'll need to create ConfigMaps/Secrets for environment variables in K8s first.*

## Usage

1. Open the Streamlit UI.
2. Enter the Service Name, Endpoint, and GitHub Repo.
3. Click "Generate Load Test Bundle".
4. Monitor the process and download the generated bundle once complete.
