# Catalog Management App

A robust CRUD application for managing products, built with Go. This project demonstrates a clean architecture approach, supporting both HTTP and gRPC interfaces, backed by a PostgreSQL database.

## Features

- **Dual Interfaces**: Exposes both RESTful HTTP and gRPC APIs.
- **Clean Architecture**: Follows Domain-Driven Design (DDD) principles with separate layers for handlers, services, and repositories.
- **Database**: Uses PostgreSQL for persistent storage.
- **Containerization**: Fully Dockerized for easy deployment.
- **Orchestration**: Includes Kubernetes manifests for deployment.
- **Testing**: Comprehensive test suite using Ginkgo and Gomega.

## Prerequisites

- [Go](https://go.dev/) (1.22+)
- [Docker](https://www.docker.com/)
- [Minikube](https://minikube.sigs.k8s.io/docs/) (for Kubernetes deployment)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/)

## Getting Started

A `Makefile` is provided to simplify common tasks.

### 1. Setup

Check for dependencies and install using Homebrew if missing (macOS):

```bash
make setup
```

### 2. running Locally

To run the application locally (ensure you have a PostgreSQL instance running on port 5470 or update configuration):
```bash
make run-local
```

### 3. Testing

Run the test suite:

```bash
make test
```

## Build & Deploy

### Build Binary

```bash
make build
```

The binary will be placed in `bin/app`.

### Docker Build

Build the Docker image:

```bash
make docker-build
```

### Deploy to Kubernetes

Deploy the application to a running Minikube cluster:

```bash
make deploy
```

### Platform Specific Notes (macOS/Minikube)

On macOS with the Docker driver, Minikube's IP is not reachable directly. You must use port forwarding to access the services.

**1. Automated Tunnel**
Run the following make target to forward both HTTP (8081->8080) and gRPC (50051->50051) ports:
```bash
make tunnel
```

**2. Manual Port Forwarding**
Forward HTTP port:
```bash
kubectl port-forward service/catalog-app 8081:8080
```
Forward gRPC port:
```bash
kubectl port-forward service/catalog-app 50051:50051
```

**3. Verification**
HTTP Request:
```bash
curl -X POST http://localhost:8081/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 100.0}'
```

gRPC Request (using grpcurl):
```bash
grpcurl -plaintext -import-path ./proto -proto product.proto -d '{"name": "gRPC Product", "price": 199.99}' localhost:50051 product.ProductService/CreateProduct
```

## Project Structure

- `cmd/app`: Main entry point.
- `internal/domain`: Domain models.
- `internal/handler`: HTTP and gRPC handlers.
- `internal/repository`: Database access layer.
- `internal/service`: Business logic.
- `proto`: Protocol Buffer definitions.
- `k8s`: Kubernetes manifests.
