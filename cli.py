#!/usr/bin/env python3
import subprocess
import sys
import time
from pathlib import Path

import click


EXERCISES_DIR = Path(__file__).parent / "26-01-01"
SOLUTIONS_DIR = EXERCISES_DIR / ".solutions"
OBFUSCATION_KEY = b"cli_secret_salt_2026"


def xor_crypt(data: bytes) -> bytes:
    return bytes(
        value ^ OBFUSCATION_KEY[index % len(OBFUSCATION_KEY)]
        for index, value in enumerate(data)
    )


def find_exercise_file(prefix: str, is_solution: bool = False) -> Path:
    if not EXERCISES_DIR.exists():
        raise click.ClickException(f"Exercises directory not found: {EXERCISES_DIR}")

    if is_solution:
        matches = list(EXERCISES_DIR.glob(f"{prefix}*-solution.py"))
        file_type = "solution"
    else:
        matches = [
            path
            for path in EXERCISES_DIR.glob(f"{prefix}*.py")
            if not path.name.endswith("-solution.py")
        ]
        file_type = "exercise"

    if not matches:
        raise click.ClickException(
            f"No {file_type} file found matching prefix: '{prefix}'"
        )
    if len(matches) > 1:
        names = "\n".join(f"  - {path.name}" for path in matches)
        raise click.ClickException(f"Multiple matches found for '{prefix}':\n{names}")
    return matches[0]


def run_validation(file_path: Path) -> bool:
    click.secho(f"\n--- Running checks for {file_path.name} ---", fg="cyan", bold=True)

    if "coverage" in file_path.name:
        commands = [
            [sys.executable, "-m", "coverage", "run", "-m", "pytest", str(file_path)],
            [sys.executable, "-m", "coverage", "report", "--fail-under=100"],
        ]
    elif "type" in file_path.name:
        commands = [
            [sys.executable, "-m", "mypy", "--strict", str(file_path)],
            [sys.executable, "-m", "pytest", str(file_path), "-v"],
        ]
    else:
        commands = [[sys.executable, "-m", "pytest", str(file_path), "-v"]]

    return all(
        subprocess.run(command, cwd=EXERCISES_DIR).returncode == 0
        for command in commands
    )


@click.group()
def cli() -> None:
    """Manage and test Python training exercises."""


@cli.command()
def pack() -> None:
    """Obfuscate solution files and remove their plain-text copies."""
    SOLUTIONS_DIR.mkdir(exist_ok=True)
    solution_files = list(EXERCISES_DIR.glob("*-solution.py"))

    if not solution_files:
        click.secho("No plain-text solution files found to pack.", fg="yellow")
        return

    for file_path in solution_files:
        binary_path = SOLUTIONS_DIR / file_path.name.replace("-solution.py", ".bin")
        binary_path.write_bytes(xor_crypt(file_path.read_bytes()))
        file_path.unlink()
        click.secho(f"Packed: {file_path.name} -> {binary_path.name}", fg="green")

    click.secho("All solutions packed.", fg="green", bold=True)


@cli.command()
def unpack() -> None:
    """Restore obfuscated solutions as plain-text files."""
    binaries = list(SOLUTIONS_DIR.glob("*.bin")) if SOLUTIONS_DIR.exists() else []
    if not binaries:
        click.secho("No packed solution binaries found to unpack.", fg="yellow")
        return

    for binary_path in binaries:
        solution_path = EXERCISES_DIR / binary_path.name.replace(".bin", "-solution.py")
        solution_path.write_bytes(xor_crypt(binary_path.read_bytes()))
        binary_path.unlink()
        click.secho(f"Unpacked: {binary_path.name} -> {solution_path.name}", fg="green")

    click.secho("All solutions restored.", fg="green", bold=True)


@cli.command()
@click.argument("prefix")
@click.option("--solution", "is_solution", "-s", is_flag=True)
def run(prefix: str, is_solution: bool) -> None:
    """Run checks for an exercise selected by PREFIX."""
    file_path = find_exercise_file(prefix, is_solution)
    success = run_validation(file_path)
    if success:
        click.secho("\nAll checks passed.", fg="green", bold=True)
    else:
        raise click.ClickException("Some checks failed.")


@cli.command()
@click.argument("prefix")
@click.option("--solution", "is_solution", "-s", is_flag=True)
def watch(prefix: str, is_solution: bool) -> None:
    """Re-run checks when the selected exercise changes."""
    file_path = find_exercise_file(prefix, is_solution)
    click.secho(
        f"Watching '{file_path.name}' for changes. Press Ctrl+C to stop.",
        fg="blue",
        bold=True,
    )

    last_mtime = file_path.stat().st_mtime_ns
    run_validation(file_path)
    try:
        while True:
            time.sleep(0.5)
            current_mtime = file_path.stat().st_mtime_ns
            if current_mtime != last_mtime:
                last_mtime = current_mtime
                run_validation(file_path)
    except KeyboardInterrupt:
        click.secho("\nStopped watching.", fg="yellow")


@cli.command()
@click.argument("prefix")
def solution(prefix: str) -> None:
    """Display the unpacked solution for an exercise."""
    exercise_path = find_exercise_file(prefix)
    binary_path = SOLUTIONS_DIR / exercise_path.name.replace(".py", ".bin")
    if not binary_path.exists():
        raise click.ClickException(
            f"No obfuscated solution found for {exercise_path.name}"
        )

    click.secho(f"\n--- Solution for {exercise_path.name} ---", fg="magenta", bold=True)
    click.echo(xor_crypt(binary_path.read_bytes()).decode("utf-8"), nl=False)


if __name__ == "__main__":
    cli()
