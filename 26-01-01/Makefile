CLI := uv run python ../cli.py

.PHONY: ruff test pack unpack run watch solution quality_gate

ruff:
	uv run ruff check --select I --fix .
	uv run ruff format .

test:
	uv run pytest .

pack:
	$(CLI) pack

unpack:
	$(CLI) unpack

run:
	@test -n "$(PREFIX)" || (echo "Usage: make run PREFIX=03-01"; exit 1)
	$(CLI) run $(PREFIX)

watch:
	@test -n "$(PREFIX)" || (echo "Usage: make watch PREFIX=03-01"; exit 1)
	$(CLI) watch $(PREFIX)

solution:
	@test -n "$(PREFIX)" || (echo "Usage: make solution PREFIX=03-01"; exit 1)
	$(CLI) solution $(PREFIX)

quality_gate: ruff test
