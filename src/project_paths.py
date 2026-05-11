from __future__ import annotations

import hashlib
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
ASSETS_DIR = PROJECT_ROOT / "assets"
UI_DIR = ASSETS_DIR / "ui"
ICONS_DIR = ASSETS_DIR / "icons"
IMAGES_DIR = ASSETS_DIR / "images"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
CONFIG_DIR = PROJECT_ROOT / "config"
DOCS_DIR = PROJECT_ROOT / "docs"
SAMPLES_DIR = PROJECT_ROOT / "samples"
TESTS_DIR = PROJECT_ROOT / "tests"
TEST_FIXTURES_DIR = TESTS_DIR / "fixtures"
VENDOR_DIR = PROJECT_ROOT / "vendor"
WORKSPACE_DIR = PROJECT_ROOT / "workspace"
WORKSPACE_CASES_DIR = WORKSPACE_DIR / "cases"
WORKSPACE_RUNTIME_DIR = WORKSPACE_DIR / ".ad_gui_runtime"

PREFERENCES_PATH = WORKSPACE_DIR / ".ad_gui_preferences.json"
DEBUG_LOG_PATH = WORKSPACE_DIR / "app_debug.log"

FLIGHTFORGE_ICON_PATH = ICONS_DIR / "flightforge.ico"
CHECKBOX_CHECK_WHITE_PATH = IMAGES_DIR / "checkbox_check_white.png"
AIRCRAFT_DESIGN_UI_PATH = UI_DIR / "aircraft_design.ui"
AERODYNAMICS_WORKBENCH_UI_PATH = UI_DIR / "aerodynamics_workbench.ui"
OPENFOAM_CONFIG_PATH = CONFIG_DIR / "openfoam_config.json"

SAMPLE_OPENFOAM_CASE_DIR = SAMPLES_DIR / "openfoam_case"
OPENFOAM_VENDOR_DIR = VENDOR_DIR / "openfoam"
OPENFOAM_WINDOWS_V2412_DIR = OPENFOAM_VENDOR_DIR / "v2412"
OPENFOAM_WINDOWS_BOOTSTRAP = OPENFOAM_WINDOWS_V2412_DIR / "setEnvVariables-v2412.bat"


def ensure_workspace_dirs() -> None:
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    WORKSPACE_CASES_DIR.mkdir(parents=True, exist_ok=True)
    WORKSPACE_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


def default_workspace_case_dir(name: str = "openfoam_case") -> Path:
    ensure_workspace_dirs()
    return WORKSPACE_CASES_DIR / str(name or "openfoam_case")


def workspace_runtime_dir_for_case(case_dir: str | Path) -> Path:
    ensure_workspace_dirs()
    case_path = Path(case_dir)
    label = re.sub(r"[^A-Za-z0-9._-]+", "_", case_path.name or "case").strip("._") or "case"
    digest = hashlib.sha1(str(case_path.resolve(strict=False)).encode("utf-8")).hexdigest()[:12]
    target = WORKSPACE_RUNTIME_DIR / f"{label}_{digest}"
    target.mkdir(parents=True, exist_ok=True)
    return target
