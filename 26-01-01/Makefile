ruff:
	uv run ruff check --select I --fix
	uv run ruff format .

pytest:
	uv run pytest .

run_all_solution_files:
	for file in *-solution.py; do \
		if [[ $$file == *"coverage"* ]]; then \
			uv run internal_coverage_runner.py $$file; \
		elif [[ $$file == *"type"* ]]; then \
			uv run internal_type_checker.py $$file; \
		else \
			uv run $$file; \
		fi \
	done

quality_gate:
	set +e; \
	$(MAKE) ruff; \
	$(MAKE) pytest; \
	$(MAKE) run_all_solution_files; \
	set -e
