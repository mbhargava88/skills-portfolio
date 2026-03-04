# Agents Specification

This document describes the architecture and agent responsibilities for the **Load‑Testing Automation System**. It follows **DDD**, **Clean Architecture**, and a **StateGraph‑based orchestration** to automate generation of k6 load‑testing bundles using traffic data from Grafana, code analysis from GitHub, LLM‑generated scripts, and packaging to S3.

---

## 🎯 **High‑Level Goal**

Given a backend service name and endpoint, the system:

1. Fetches traffic data (RPS, latency, datasize, error‑rate, etc.) from Grafana.
2. Fetches and analyzes the related GitHub repo codebase.
3. Uses Groq LLM to:

   * Analyze Grafana traffic pattern.
   * Analyze endpoint implementation.
   * Generate k6 load‑testing script.
   * Generate required dataset CSV.
   * Package these into a bundle.
4. Stores bundle into S3.
5. Streamlit FE triggers the process and allows users to download the generated bundle.

---

# 🧩 Domain‑Driven Design (DDD)

## **Domains & Subdomains**

### 1. **Traffic Analysis Domain**

Responsible for retrieving and modeling traffic pattern data from Grafana.

### 2. **Repo Analysis Domain**

Responsible for analyzing source code from GitHub and extracting endpoint‑specific logic.

### 3. **Script Generation Domain**

Uses Groq LLM to build load‑testing artifacts (k6 scripts + datasets).

### 4. **Bundling Domain**

Responsible for bundling output artifacts and pushing to S3.

### 5. **Orchestration Domain**

Uses StateGraph to execute each domain in the correct order.

---

# 🏗️ Clean Architecture Layers

## **1. Domain Layer (Core Business Logic)**

* Entities: `TrafficPattern`, `EndpointDetails`, `LoadTestScript`, `Dataset`, `Bundle`
* Use‑cases:

  * `FetchTrafficUseCase`
  * `AnalyzeRepoUseCase`
  * `GenerateLoadtestUseCase`
  * `BundleArtifactsUseCase`
  * `UploadToS3UseCase`

## **2. Application Layer**

Implements the **StateGraph flow**, invoking domain use‑cases.

## **3. Interface Layer (Ports)**

Interfaces that must be implemented by Infra layer:

```python
class GrafanaClient:
    def fetch_traffic(self, service: str, endpoint: str) -> TrafficPattern:
        raise NotImplementedError

class GitHubClient:
    def fetch_repo(self, repo_name: str):
        raise NotImplementedError

class GroqLLMClient:
    def analyze_and_generate(self, prompt: str) -> str:
        raise NotImplementedError

class S3Client:
    def upload(self, bundle_path: str, bucket: str, key: str):
        raise NotImplementedError
```

---

# 🔌 Infrastructure Layer Implementations

## **GrafanaClientImpl (Mock)**

Returns mock traffic patterns for development.

Example mock:

```json
{
  "rps": 250,
  "avg_latency_ms": 120,
  "p95_latency_ms": 200,
  "payload_size_bytes": 2100,
  "error_rate": 0.02
}
```

## **GitHubClientImpl**

* Uses GitHub API to fetch repo content or clones via `git`.

## **GroqLLMClientImpl**

Uses Groq Python SDK to:

* Analyze Grafana data
* Analyze codebase
* Generate k6 script
* Generate CSV dataset

## **S3ClientImpl**

* Uploads artifacts to specfied bucket
* Used in final StateGraph state

---

# 🔮 StateGraph Orchestration

## **States**

1. **FetchTraffic** → calls Grafana
2. **FetchRepo** → GitHub
3. **AnalyzeAndGenerate** → Groq
4. **Bundle** → zip artifacts
5. **Upload** → S3
6. **Done**

### Graph Flow

```
Start
  ↓
FetchTraffic
  ↓
FetchRepo
  ↓
AnalyzeAndGenerate
  ↓
Bundle
  ↓
Upload
  ↓
Done
```

---

# 🖥️ Streamlit FE

Features:

* Input fields: service, endpoint, repo name
* Trigger button → starts orchestrator
* Polling/loading indicator
* Once S3 upload is done → **Download button** linking to pre‑signed URL

---

# 🐳 Docker + Minikube

Project will include:

* `Dockerfile`
* `docker-compose.yaml`
* Kubernetes manifests (`deployment.yaml`, `service.yaml`)
* ConfigMap for environment variables

---

# 🔧 Makefile

Should include:

* `make build`
* `make run`
* `make test`
* `make clean`
* `make deploy-minikube`

---

# 📄 README

Must include:

* Architecture overview
* Steps to run locally
* Steps to deploy on Minikube
* Streamlit UI usage
* Environment variables

---

# 🧑‍🤝‍🧑 Agents Overview

## **Agent 1: TrafficAgent**

Purpose: Fetch & normalize Grafana traffic data.

Inputs: service name, endpoint
Outputs: `TrafficPattern`

## **Agent 2: RepoAgent**

Purpose: Fetch & analyze GitHub repo.

Inputs: repo name
Outputs: repo context + endpoint file tree

## **Agent 3: GroqGenerationAgent**

Purpose: Use LLM to generate artifacts.

Inputs: traffic pattern + repo analysis
Outputs: k6 script + dataset CSV

## **Agent 4: BundlingAgent**

Purpose: Package script + CSV
Outputs: `.zip` bundle

## **Agent 5: UploadAgent**

Purpose: Upload bundle to S3 and return URL

Outputs: s3 key + presigned URL

## **Agent 6: OrchestrationAgent**

Purpose: StateGraph executor

---

# 🧱 Directory Structure

```
./
├── app/
│   ├── domain/
│   │   ├── entities/
│   │   ├── usecases/
│   ├── application/
│   │   ├── orchestrator/
│   ├── interfaces/
│   ├── infra/
│   │   ├── grafana/
│   │   ├── github/
│   │   ├── groq/
│   │   ├── s3/
│   ├── utils/
├── streamlit_app/
├── Dockerfile
├── Makefile
├── README.md
└── k8s/
    ├── deployment.yaml
    └── service.yaml
```

---

# ✅ Summary

This Agents.md outlines the entire architecture, agents, responsibilities, DDD structure, clean architecture boundaries, orchestration steps, and expected project layout to implement the **Load‑Testing Automation System**.
