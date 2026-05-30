import sys

import coverage
import pytest


def print_section(title: str) -> None:
    print(f"\n{title}")


def run_with_coverage(filepath: str) -> None:
    """Run a test file with coverage tracking and enforce 100% coverage."""
    print_section(f"Step 1: Running tests with coverage for {filepath}")
    cov = coverage.Coverage(branch=True)
    cov.start()

    exit_code = pytest.main([filepath, "-q", "-p", "no:warnings"])

    cov.stop()
    cov.save()

    if exit_code == 0:
        print("[PASS] All tests passed.")
    else:
        print(f"[FAIL] Pytest failed with exit code {exit_code}.")

    print_section("Step 2: Coverage Analysis")
    percent = cov.report(include=[filepath], show_missing=True)

    if percent < 95:
        print(f"\n[FAIL] Coverage is only {percent:.1f}%. You must reach 100%!")
        sys.exit(1)
    elif percent < 100:
        print(
            f"\n[FAIL] Close enough, but {percent:.1f}% coverage reached! (100% required)"
        )
        sys.exit(1)
    else:
        print("\n[PASS] 100% Coverage reached!")

    print_section("Summary")
    if exit_code == 0 and percent == 100:
        print("[PASS] All checks passed!")
        sys.exit(0)
    else:
        print("[FAIL] Some checks failed.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python coverage_runner.py <test_file.py>")
        sys.exit(1)

    run_with_coverage(sys.argv[1])
