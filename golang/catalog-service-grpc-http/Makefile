PROJECT_NAME := catalog-mgmt-app
DOCKER_IMAGE := $(PROJECT_NAME):latest

.PHONY: setup build docker-build deploy test run-local clean tunnel

setup:
	@echo "Checking for minikube..."
	@which minikube > /dev/null || (echo "Minikube not found. Installing via brew..." && brew install minikube)
	@echo "Checking for kubectl..."
	@which kubectl > /dev/null || (echo "Kubectl not found. Installing via brew..." && brew install kubectl)
	@echo "Starting minikube..."
	@minikube status > /dev/null || minikube start

build:
	go build -o bin/app cmd/app/main.go

docker-build:
	@eval $$(minikube docker-env) && docker build -t $(DOCKER_IMAGE) .

deploy: docker-build
	kubectl apply -f k8s/

test:
	go test ./... -v

run-local:
	go run cmd/app/main.go

clean:
	rm -rf bin
	kubectl delete -f k8s/ --ignore-not-found

tunnel:
	@echo "Forwarding HTTP port 8081->8080 and gRPC port 50051->50051..."
	@echo "Press Ctrl+C to stop."
	@trap 'kill %1; kill %2' SIGINT; \
	kubectl port-forward service/catalog-app 8081:8080 & \
	kubectl port-forward service/catalog-app 50051:50051 & \
	wait
