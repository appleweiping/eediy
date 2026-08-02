PYTHON ?= python3

.PHONY: check check-required icarus verilator formal synthesis

check:
	$(PYTHON) run_checks.py

check-required:
	$(PYTHON) run_checks.py --require-tools all

icarus:
	$(PYTHON) run_checks.py --only icarus --require-tools all

verilator:
	$(PYTHON) run_checks.py --only verilator --require-tools all

formal:
	$(PYTHON) run_checks.py --only formal --require-tools all

synthesis:
	$(PYTHON) run_checks.py --only synthesis --require-tools all
