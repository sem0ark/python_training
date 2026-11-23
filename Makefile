.PHONY: website-install website-dev website-test website-build website-quality \
	website-quality-quiet \
	python-format python-test python-quality python-run python-watch python-solution \
	python-pack python-unpack quality test

website-install:
	cd website && pnpm install --frozen-lockfile

website-dev:
	cd website && pnpm dev

website-test:
	cd website && pnpm test-ci

website-build:
	cd website && pnpm build

website-quality:
	cd website && pnpm quality_gate

website-quality-quiet:
	@tmp=$$(mktemp); trap 'rm -f "$$tmp"' EXIT; \
	if (cd website && pnpm quality_gate >"$$tmp" 2>&1); then \
		echo "Website quality gate passed."; \
	else \
		status=$$?; cat "$$tmp"; exit $$status; \
	fi

python-format:
	cd 26-01-01 && uv run ruff check --select I --fix . && uv run ruff format .

python-test:
	cd 26-01-01 && uv run pytest .

python-quality:
	cd 26-01-01 && uv run ruff check . && uv run pytest .

python-run:
	@test -n "$(PREFIX)" || (echo "Usage: make python-run PREFIX=03-01"; exit 1)
	uv run --project 26-01-01 python cli.py run $(PREFIX)

python-watch:
	@test -n "$(PREFIX)" || (echo "Usage: make python-watch PREFIX=03-01"; exit 1)
	uv run --project 26-01-01 python cli.py watch $(PREFIX)

python-solution:
	@test -n "$(PREFIX)" || (echo "Usage: make python-solution PREFIX=03-01"; exit 1)
	uv run --project 26-01-01 python cli.py solution $(PREFIX)

python-pack:
	uv run --project 26-01-01 python cli.py pack

python-unpack:
	uv run --project 26-01-01 python cli.py unpack

quality: python-quality website-quality

test: python-test website-test
