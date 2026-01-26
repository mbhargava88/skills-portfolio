.PHONY: install run test clean docker-build docker-run

setup-poetry:
	@command -v python3 >/dev/null 2>&1 || { echo >&2 "Python 3 is required but not installed. Aborting."; exit 1; }
	@python3 -m pip show poetry >/dev/null 2>&1 || { \
		echo "Installing Poetry..."; \
		python3 -m pip install poetry; \
	}

install: setup-poetry
	python3 -m poetry install

run:
	PYTHONPATH=. python3 -m poetry run streamlit run src/interface/streamlit_app.py

test:
	python3 -m poetry run pytest tests/


clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t smartcart-ai .

docker-run:
	docker run -p 8501:8501 --env-file .env smartcart-ai
