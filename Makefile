.PHONY: install test lint demo benchmark clean all

install:
	pip install -e cli/
	brainos add all

test:
	pytest tests/ -v

lint:
	ruff check cli/ tests/

demo:
	cd examples/01_memory_agent && python agent.py --mock

benchmark:
	cd examples/02_token_benchmark && python benchmark.py

clean:
	rm -rf cli/dist/ cli/*.egg-info/ __pycache__/ .pytest_cache/ brainos_plugins/ htmlcov/

all: install lint test
