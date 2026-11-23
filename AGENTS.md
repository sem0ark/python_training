# Repository Guidance

## Validation

Use the quiet project wrapper for website validation:

```bash
make website-quality-quiet
```

It runs the website lint, Astro checks, coverage tests, and production build while suppressing successful tool logs. On failure, it prints the captured log and preserves the failing exit code.

Use the direct commands only when debugging a specific stage:

```bash
cd website && pnpm lint
cd website && pnpm exec astro check
cd website && pnpm test-coverage
cd website && pnpm build
```

Do not paste generated Vite/Pyodide bundles, coverage HTML, or full successful build logs into the working context. Summarize the result and include captured output only for failures.

## Python Validation

```bash
make python-quality
make python-run PREFIX=03-01
```
