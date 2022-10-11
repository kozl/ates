.PHONY: build-all
build-all:
	@echo "[+] Building all services"
	@echo
	$(MAKE) -C api-gateway build
	$(MAKE) -C task-tracker build
	@echo
	@echo "[+] All services built successfully"