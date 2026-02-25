.PHONY: build run test clean deploy-minikube

build:
	docker build -t antigravity-load-test .

run:
	streamlit run streamlit_app/main.py

test:
	pytest app/tests

clean:
	rm -rf __pycache__ .pytest_cache
	find . -name "*.pyc" -delete

deploy-minikube:
	kubectl apply -f k8s/minio.yaml
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml

deploy-minio:
	kubectl apply -f k8s/minio.yaml

port-forward-minio:
	@echo "MinIO API: http://localhost:9000"
	@echo "MinIO Console: http://localhost:9001 (User: minioadmin, Pass: minioadmin)"
	kubectl port-forward svc/minio 9000:9000 9001:9001
