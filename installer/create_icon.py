#!/usr/bin/env python
"""Create the .jaon file association icon matching the Jaon logo."""
import importlib.util
import sys
from pathlib import Path


# Load create_logo from the main logo generator so the file icon stays in sync.
_LOGO_SCRIPT = Path(__file__).resolve().parent.parent / "assets" / "logo" / "design_logo.py"
_spec = importlib.util.spec_from_file_location("design_logo", _LOGO_SCRIPT)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Could not load logo generator: {_LOGO_SCRIPT}")
_design_logo = importlib.util.module_from_spec(_spec)
sys.modules["design_logo"] = _design_logo
_spec.loader.exec_module(_design_logo)

create_logo = _design_logo.create_logo
save_ico = _design_logo.save_ico


def main():
    out_dir = Path(__file__).resolve().parent
    sizes = [16, 32, 48, 64, 128, 256]
    images = [create_logo(s) for s in sizes]
    save_ico(images, out_dir / "jaon-file.ico")
    print("Created jaon-file.ico with sizes:", [img.size for img in images])


if __name__ == "__main__":
    main()
