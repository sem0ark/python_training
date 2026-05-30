import ast
import subprocess
import sys
from pathlib import Path

FORBIDDEN_TYPING_IMPORTS = {
    "Dict": "dict",
    "List": "list",
    "Tuple": "tuple",
    "Set": "set",
    "FrozenSet": "frozenset",
    "Type": "type",
    "Deque": "collections.deque",
    "DefaultDict": "collections.defaultdict",
    "OrderedDict": "collections.OrderedDict",
    "Counter": "collections.Counter",
    "ChainMap": "collections.ChainMap",
    "Any": "do not use at all",
}


class OldTypingVisitor(ast.NodeVisitor):
    """AST visitor that detects old-style typing annotations."""

    def __init__(self):
        self.violations: list[tuple[int, int, str]] = []
        self._typing_imports: dict[str, str] = {}  # local_name -> original_name

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Check 'from typing import ...' statements."""
        if node.module == "typing":
            for alias in node.names:
                original_name = alias.name
                local_name = alias.asname if alias.asname else alias.name

                if original_name in FORBIDDEN_TYPING_IMPORTS:
                    self._typing_imports[local_name] = original_name
                    replacement = FORBIDDEN_TYPING_IMPORTS[original_name]
                    self.violations.append(
                        (
                            node.lineno,
                            node.col_offset,
                            f"Forbidden import: 'from typing import {original_name}' "
                            f"-> use '{replacement}' instead",
                        )
                    )

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        """Check 'import typing' statements used with forbidden names."""
        for alias in node.names:
            if alias.name == "typing":
                local_name = alias.asname if alias.asname else "typing"
                self._typing_imports[local_name] = "typing"

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Check 'typing.Dict', 'typing.List', etc. usages."""
        if (
            isinstance(node.value, ast.Name)
            and node.value.id in self._typing_imports
            and self._typing_imports[node.value.id] == "typing"
            and node.attr in FORBIDDEN_TYPING_IMPORTS
        ):
            replacement = FORBIDDEN_TYPING_IMPORTS[node.attr]
            self.violations.append(
                (
                    node.lineno,
                    node.col_offset,
                    f"Forbidden usage: 'typing.{node.attr}' -> use '{replacement}' instead",
                )
            )

        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        """Check direct usage of imported forbidden names."""
        if (
            node.id in self._typing_imports
            and self._typing_imports[node.id] != "typing"
        ):
            replacement = FORBIDDEN_TYPING_IMPORTS[self._typing_imports[node.id]]
            self.violations.append(
                (
                    node.lineno,
                    node.col_offset,
                    f"Forbidden usage: '{node.id}' -> use '{replacement}' instead",
                )
            )

        self.generic_visit(node)


def check_old_typing(file_path: Path) -> list[tuple[int, int, str]]:
    """Parse and check file for old-style typing annotations."""
    source = file_path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError as e:
        print(f"[ERROR] Syntax error in {file_path}: {e}")
        sys.exit(1)

    visitor = OldTypingVisitor()
    visitor.visit(tree)

    return visitor.violations


def check_type_errors(file_path: Path) -> tuple[bool, str]:
    """Run mypy on the file to check for type errors."""
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "--pretty", str(file_path)],
        capture_output=True,
        text=True,
    )
    success = result.returncode == 0
    output = result.stdout + result.stderr
    return success, output


def run_tests(file_path: Path) -> tuple[bool, str]:
    """Run pytest on the file."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(file_path), "-v"],
        capture_output=True,
        text=True,
    )
    success = result.returncode == 0
    output = result.stdout + result.stderr
    return success, output


def print_section(title: str) -> None:
    print(f"\n{title}")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path_to_task_file.py>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)

    if not file_path.suffix == ".py":
        print(f"[ERROR] Expected a Python file, got: {file_path}")
        sys.exit(1)

    all_passed = True

    print_section(f"Step 1: Checking old-style typing for {file_path}")
    violations = check_old_typing(file_path)

    if violations:
        all_passed = False
        print(f"[FAIL] Found {len(violations)} forbidden typing usage(s):\n")
        for line, col, message in violations:
            print(f"  {file_path}:{line}:{col}  {message}")
    else:
        print("[PASS] No forbidden typing annotations found.")

    print_section("Step 2: Running mypy type checker")
    types_ok, mypy_output = check_type_errors(file_path)

    if not types_ok:
        all_passed = False
        print("[FAIL] mypy reported type errors:\n")
        print(mypy_output)
    else:
        print("[PASS] mypy found no type errors.")
        if mypy_output.strip():
            print(mypy_output)

    print_section("Step 3: Running pytest tests")
    tests_ok, pytest_output = run_tests(file_path)

    if not tests_ok:
        all_passed = False
        print("[FAIL] Some tests failed:\n")
    else:
        print("[PASS] All tests passed.\n")

    print(pytest_output)

    print_section("Summary")
    if all_passed:
        print("[PASS] All checks passed!")
        sys.exit(0)
    else:
        print("[FAIL] Some checks failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
