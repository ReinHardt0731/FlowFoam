from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path

from project_paths import PREFERENCES_PATH


DEFAULT_PREFERENCES_FILENAME = ".ad_gui_preferences.json"
MAX_RECENT_CASES = 10


def preferences_default_path(root: Path) -> Path:
    root_path = Path(root)
    if root_path == PREFERENCES_PATH or root_path == PREFERENCES_PATH.parent:
        PREFERENCES_PATH.parent.mkdir(parents=True, exist_ok=True)
        return PREFERENCES_PATH
    candidate = root_path / DEFAULT_PREFERENCES_FILENAME
    candidate.parent.mkdir(parents=True, exist_ok=True)
    return candidate


def _coerce_recent_case(entry: dict) -> dict | None:
    if not isinstance(entry, dict):
        return None
    raw_path = str(entry.get("path", "")).strip()
    if not raw_path:
        return None
    path = Path(raw_path)
    if not path.exists() or not path.is_dir():
        return None
    label = str(entry.get("label", "")).strip() or path.name
    return {
        "path": str(path),
        "label": label,
        "last_opened_at": str(entry.get("last_opened_at", "")).strip(),
        "source_kind": str(entry.get("source_kind", "")).strip() or "opened",
        "template_id": str(entry.get("template_id", "")).strip(),
    }


def normalize_recent_cases(entries: list[dict] | None, *, limit: int = MAX_RECENT_CASES) -> list[dict]:
    normalized = []
    seen = set()
    for entry in entries or []:
        item = _coerce_recent_case(entry)
        if item is None:
            continue
        key = str(Path(item["path"]).resolve(strict=False)).lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(item)
        if len(normalized) >= int(limit):
            break
    return normalized


def record_recent_case(
    entries: list[dict] | None,
    case_path: str | Path,
    *,
    label: str | None = None,
    source_kind: str = "opened",
    template_id: str = "",
    limit: int = MAX_RECENT_CASES,
    timestamp: str | None = None,
) -> list[dict]:
    path = Path(case_path)
    if not path.exists() or not path.is_dir():
        return normalize_recent_cases(entries, limit=limit)
    new_entry = {
        "path": str(path),
        "label": str(label).strip() if label else path.name,
        "last_opened_at": str(timestamp or datetime.now().isoformat(timespec="seconds")),
        "source_kind": str(source_kind or "opened").strip() or "opened",
        "template_id": str(template_id or "").strip(),
    }
    return normalize_recent_cases([new_entry] + list(entries or []), limit=limit)


def load_workspace_payload(path: str | Path) -> dict:
    pref_path = Path(path)
    if not pref_path.is_file():
        return {"settings": {}, "workspace": {"recent_cases": []}}
    try:
        payload = json.loads(pref_path.read_text(encoding="utf-8"))
    except Exception:
        return {"settings": {}, "workspace": {"recent_cases": []}}
    if not isinstance(payload, dict):
        return {"settings": {}, "workspace": {"recent_cases": []}}
    settings = payload.get("settings", payload)
    if not isinstance(settings, dict):
        settings = {}
    workspace = payload.get("workspace", {})
    if not isinstance(workspace, dict):
        workspace = {}
    workspace["recent_cases"] = normalize_recent_cases(workspace.get("recent_cases"))
    return {"settings": settings, "workspace": workspace}


def save_workspace_payload(path: str | Path, *, settings: dict, workspace: dict) -> None:
    pref_path = Path(path)
    pref_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "saved_at": datetime.now().isoformat(timespec="seconds"),
        "settings": settings if isinstance(settings, dict) else {},
        "workspace": {
            "recent_cases": normalize_recent_cases((workspace or {}).get("recent_cases")),
        },
    }
    pref_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
