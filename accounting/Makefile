IMAGE=task-tracker
TAG=latest

.PHONY: build
build:
	@echo "[+] Building Accounting"
	@echo
	@docker build -t $(IMAGE):$(TAG) .
	@echo
	@echo "[+] Accounting built successfully"

.PHONY: run
run:
	PYTHONPATH="./src" uvicorn app:app --reload