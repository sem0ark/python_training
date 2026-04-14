ruff:
	uv run ruff check --select I --fix
	uv run ruff format .

pytest:
	uv run pytest .

run_all_solution_files:
	find . -type f -name "*-solution.py" -exec uv run python {} \;

quality_gate:
	set +e; \
	$(MAKE) ruff; \
	$(MAKE) pytest; \
	$(MAKE) run_all_solution_files; \
	set -e
