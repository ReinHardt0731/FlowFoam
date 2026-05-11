from __future__ import annotations

import sys
from pathlib import Path


_SRC_DIR = Path(__file__).resolve().parents[1] / "src"
_PKG_DIR = _SRC_DIR / "aerodynamics"

if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

__path__ = [str(_PKG_DIR)]
