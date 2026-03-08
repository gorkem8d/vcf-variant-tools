.PHONY: install test test-cov clean docker-build docker-test help

help:
	@echo "Available commands:"
	@echo "  make install       Install package with dev dependencies"
	@echo "  make test          Run test suite"
	@echo "  make test-cov      Run tests with coverage report"
	@echo "  make clean         Remove build artifacts"
	@echo "  make docker-build  Build Docker image"
	@echo "  make docker-test   Run tests inside Docker"

install:
	pip install -e ".[dev]"

test:
	pytest -v

test-cov:
	pip install pytest-cov --quiet
	pytest --cov=vcf_variant_tools --cov-report=term-missing -v

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

docker-build:
	docker build -t vcf-variant-tools .

docker-test:
	docker run --rm vcf-variant-tools pytest -v