import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def run(cmd: list[str]) -> None:
    print(f"+ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)


def format() -> None:
    run(["autoflake", "--config", "pyproject.toml", "."])
    run(["isort", "."])
    run(["black", "."])


def lint() -> None:
    # format first (optional; remove this call if you want lint-only)
    format()
    run(["flake8", ".", "--exclude", ".venv,build,dist"])
    run(["mypy", "."])
