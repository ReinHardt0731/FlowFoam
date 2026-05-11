from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "assets" / "ui"
GENERATED_DIR = ROOT / "src" / "ui_generated"


def build_ui() -> int:
    targets = [
        (UI_DIR / "aircraft_design.ui", GENERATED_DIR / "aircraft_design.py"),
        (UI_DIR / "aerodynamics_workbench.ui", GENERATED_DIR / "aerodynamics_workbench.py"),
    ]
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    for source, target in targets:
        result = subprocess.run(
            ["pyside6-uic", str(source), "-o", str(target)],
            check=False,
        )
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(build_ui())
