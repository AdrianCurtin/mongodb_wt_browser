.PHONY: help install install-dev test demo clean

help:
	@echo "MongoDB WiredTiger Browser - Makefile Commands"
	@echo "================================================"
	@echo "make install      - Install production dependencies"
	@echo "make install-dev  - Install development dependencies"
	@echo "make test         - Run test suite"
	@echo "make demo         - Run demo/test script"
	@echo "make clean        - Clean up generated files"
	@echo "make help         - Show this help message"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	python test_demo.py

demo:
	python test_demo.py

clean:
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleaned up generated files"
