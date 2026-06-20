#!/usr/bin/env python
"""Run the Helios language test suite."""
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "tests"],
        cwd=root,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
