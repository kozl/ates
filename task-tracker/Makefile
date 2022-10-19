IMAGE=task-tracker
TAG=latest

.PHONY: build
build:
	@echo "[+] Building Task Tracker"
	@echo
	@docker build -t $(IMAGE):$(TAG) .
	@echo
	@echo "[+] Task Tracker built successfully"

.PHONY: run
run:
	PYTHONPATH="./src" uvicorn app:app --reload