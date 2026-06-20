#!/usr/bin/env python
"""Build a standalone compiler.exe using Nuitka."""
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    dist_dir = root / "dist"
    dist_dir.mkdir(exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "nuitka",
        "--standalone",
        "--onefile",
        "--output-filename=compiler.exe",
        "--output-dir=dist",
        "--windows-console-mode=force",
        "--windows-icon-from-ico=assets/logo/helios-logo.ico",
        "--assume-yes-for-downloads",
        "compiler.py",
    ]

    print("Building compiler.exe with Nuitka...")
    print(" ".join(cmd))
    result = subprocess.run(cmd, cwd=root)

    if result.returncode == 0:
        exe_path = dist_dir / "compiler.exe"
        # Clean up Nuitka intermediate folders
        for folder in dist_dir.glob("compiler.build"):
            shutil.rmtree(folder)
        for folder in dist_dir.glob("compiler.dist"):
            shutil.rmtree(folder)
        for folder in dist_dir.glob("compiler.onefile-build"):
            shutil.rmtree(folder)
        if exe_path.exists():
            size = exe_path.stat().st_size
            print(f"\nSuccess: {exe_path} ({size / 1024 / 1024:.2f} MB)")
            print("\nTry it out:")
            print(f"  {exe_path} run examples/hello.helios")
    else:
        print("Build failed.", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
