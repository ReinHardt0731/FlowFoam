import os
import shutil
from copy import deepcopy
from datetime import datetime
from pathlib import Path
import math
import re
import subprocess
import time
import json

import numpy as np
import pandas as pd
import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtCore import QProcess, QProcessEnvironment, Qt, QTimer, QUrl
from PySide6.QtGui import QDesktopServices, QIcon, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure

    _MATPLOTLIB_AVAILABLE = True
except Exception:
    FigureCanvas = None
    Figure = None
    _MATPLOTLIB_AVAILABLE = False

from .state import (
    CFD_FIELDS,
    FIELD_DIMENSIONS,
    FIELD_INTERNAL_VALUES,
    FV_SCHEMES_PRESETS,
    FV_SOLUTION_PRESETS,
    FLOW_PATCHES,
    PATCH_TYPES,
    bootstrap_boundary_conditions,
    default_openfoam_state,
    ensure_openfoam_state,
)
from .snappy_help import SnappyHexMeshHelpDialog, create_help_button
from .foam_case_import import parse_openfoam_case
from project_paths import OPENFOAM_WINDOWS_BOOTSTRAP


def _bool_text(value):
    return "true" if bool(value) else "false"


_CONV_TIME_RE = re.compile(r"\bTime\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)")
_CONV_RESIDUAL_RE = re.compile(
    r"Solving for\s+([A-Za-z0-9_]+)\s*,\s*Initial residual\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
)
_CONV_COEFF_RE = re.compile(
    r"Cd\s*[:=]\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
    r".*?Cl\s*[:=]\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
    r".*?Cm\s*[:=]\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
)
_CONV_RESIDUAL_FIELDS = {"p", "Ux", "Uy", "Uz", "U", "k", "omega"}


def _parse_convergence_time(line):
    match = _CONV_TIME_RE.search(line)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def _parse_convergence_time(line):
    match = _CONV_TIME_RE.search(line)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def _parse_convergence_residual(line):
    match = _CONV_RESIDUAL_RE.search(line)
    if not match:
        return None
    field = match.group(1).strip()
    if field not in _CONV_RESIDUAL_FIELDS:
        return None
    try:
        value = float(match.group(2))
    except ValueError:
        return None
    if not math.isfinite(value) or value <= 0.0:
        return None
    return field, value


def _parse_convergence_coeffs(line):
    match = _CONV_COEFF_RE.search(line)
    if not match:
        return None
    try:
        cd = float(match.group(1))
        cl = float(match.group(2))
        cm = float(match.group(3))
    except ValueError:
        return None
    if not (math.isfinite(cd) and math.isfinite(cl) and math.isfinite(cm)):
        return None
    return cd, cl, cm


def _safe_float(text):
    try:
        return float(str(text).strip())
    except Exception:
        return None


def _foam_header(cls, obj):
    return (
        "FoamFile\n"
        "{\n"
        "    version     2.0;\n"
        "    format      ascii;\n"
        f"    class       {cls};\n"
        f"    object      {obj};\n"
        "}\n\n"
    )


def _fmt_float(value):
    return f"{float(value):.6g}"


def _set_combo_value(cmb, value):
    text = str(value)
    idx = cmb.findText(text)
    if idx < 0 and text:
        cmb.addItem(text)
        idx = cmb.findText(text)
    blocked = cmb.blockSignals(True)
    cmb.setCurrentIndex(idx if idx >= 0 else 0)
    cmb.blockSignals(blocked)


def _fv_schemes_defaults(preset):
    return deepcopy(FV_SCHEMES_PRESETS.get(preset, FV_SCHEMES_PRESETS["bounded steady RANS"]))


def _fv_solution_defaults(preset):
    return deepcopy(FV_SOLUTION_PRESETS.get(preset, FV_SOLUTION_PRESETS["SIMPLE-RANS"]))


def _override_present(overrides, key):
    if not isinstance(overrides, dict) or key not in overrides:
        return False
    value = overrides.get(key)
    if value is None:
        return False
    if isinstance(value, str) and not value.strip():
        return False
    return True


def _merge_overrides(base, overrides):
    if not isinstance(overrides, dict):
        return base
    for key, value in overrides.items():
        if value is None:
            continue
        if isinstance(value, str):
            if not value.strip():
                continue
            base[key] = value.strip()
        else:
            base[key] = value
    return base


def _effective_fv_schemes(numerics):
    preset = str(numerics.get("fv_schemes_preset", "bounded steady RANS"))
    base = _fv_schemes_defaults(preset)
    return _merge_overrides(base, numerics.get("fv_schemes"))


def _effective_fv_solution(numerics):
    preset = str(numerics.get("fv_solution_preset", "SIMPLE-RANS"))
    overrides = numerics.get("fv_solution")
    base = _fv_solution_defaults(preset)
    base = _merge_overrides(base, overrides)
    simple_residual = numerics.get("simple_residual_control")
    if simple_residual is not None:
        if not _override_present(overrides, "residual_control_p"):
            base["residual_control_p"] = simple_residual
        if not _override_present(overrides, "residual_control_u"):
            base["residual_control_u"] = simple_residual
    return base


def _mesh_for_preset(preset):
    values = {
        "External Aerodynamics": {"base_cells": [80, 48, 32], "refinement_min": 2, "refinement_max": 4, "n_surface_layers": 3},
        "Coarse": {"base_cells": [48, 28, 20], "refinement_min": 1, "refinement_max": 2, "n_surface_layers": 1},
        "Medium": {"base_cells": [72, 40, 28], "refinement_min": 2, "refinement_max": 3, "n_surface_layers": 2},
        "Fine": {"base_cells": [120, 72, 48], "refinement_min": 3, "refinement_max": 5, "n_surface_layers": 4},
    }
    return deepcopy(values.get(preset, values["External Aerodynamics"]))


OPENFOAM_COMMANDS = {
    "blockMesh",
    "snappyHexMesh",
    "surfaceFeatureExtract",
    "checkMesh",
    "simpleFoam",
    "potentialFoam",
    "createPatch",
    "decomposePar",
    "reconstructPar",
    "reconstructParMesh",
}


def _find_windows_openfoam_bootstrap(configured_path=""):
    file_name = "setEnvVariables-v2412.bat"
    module_dir = Path(__file__).resolve().parent
    candidates = []

    configured = str(configured_path or "").strip()
    if configured:
        candidates.append(Path(configured).expanduser())

    candidates.extend(
        [
            OPENFOAM_WINDOWS_BOOTSTRAP,
            module_dir / "openfoam" / "v2412" / file_name,
            module_dir.parent / "openfoam" / "v2412" / file_name,
        ]
    )

    seen = set()
    for path in candidates:
        key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        if path.is_file():
            return path
    return None


def _snappy_profile_for(name):
    profiles = {
        "Balanced": {
            "refinement_min": 3,
            "refinement_max": 5,
            "n_surface_layers": 3,
            "n_feature_snap_iter": 10,
            "expansion_ratio": 1.0,
            "final_layer_thickness": 0.3,
            "min_thickness": 0.1,
            "layer_n_relax_iter": 3,
            "n_smooth_surface_normals": 1,
            "n_smooth_normals": 3,
            "n_smooth_thickness": 10,
            "max_face_thickness_ratio": 0.5,
            "max_thickness_to_medial_ratio": 0.3,
            "min_medial_axis_angle": 90.0,
            "n_layer_iter": 50,
        },
        "Fast": {
            "refinement_min": 2,
            "refinement_max": 4,
            "n_surface_layers": 1,
            "n_feature_snap_iter": 6,
            "expansion_ratio": 1.0,
            "final_layer_thickness": 0.2,
            "min_thickness": 0.05,
            "layer_n_relax_iter": 2,
            "n_smooth_surface_normals": 1,
            "n_smooth_normals": 2,
            "n_smooth_thickness": 6,
            "max_face_thickness_ratio": 0.6,
            "max_thickness_to_medial_ratio": 0.5,
            "min_medial_axis_angle": 90.0,
            "n_layer_iter": 20,
        },
        "High Fidelity": {
            "refinement_min": 5,
            "refinement_max": 6,
            "n_surface_layers": 5,
            "n_feature_snap_iter": 12,
            "expansion_ratio": 1.0,
            "final_layer_thickness": 0.35,
            "min_thickness": 0.1,
            "layer_n_relax_iter": 4,
            "n_smooth_surface_normals": 2,
            "n_smooth_normals": 4,
            "n_smooth_thickness": 12,
            "max_face_thickness_ratio": 0.45,
            "max_thickness_to_medial_ratio": 0.25,
            "min_medial_axis_angle": 90.0,
            "n_layer_iter": 60,
        },
    }
    return deepcopy(profiles.get(name, profiles["Balanced"]))



__all__ = [name for name in globals() if not name.startswith("__")]
