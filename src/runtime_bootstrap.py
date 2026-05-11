from __future__ import annotations

import os
import sys
import threading
from pathlib import Path


def _candidate_dll_dirs(env_root: Path) -> list[Path]:
    return [
        env_root,
        env_root / "Library" / "mingw-w64" / "bin",
        env_root / "Library" / "usr" / "bin",
        env_root / "Library" / "bin",
        env_root / "Scripts",
        env_root / "bin",
    ]


def _env_flag(name: str) -> bool:
    return str(os.environ.get(name, "")).strip().lower() in ("1", "true", "yes", "y", "on")


def _maybe_enable_call_tracing(project_root: Path) -> None:
    if not _env_flag("AD_GUI_TRACE_CALLS"):
        return

    raw_filters = str(os.environ.get("AD_GUI_TRACE_FILTER", "")).strip()
    filters = [part.strip().replace("\\", "/").lower() for part in raw_filters.split(",") if part.strip()]
    root = project_root.resolve()

    def _should_trace(filename: str) -> tuple[bool, str]:
        if not filename:
            return False, ""
        try:
            path = Path(filename).resolve()
            relative = path.relative_to(root)
        except Exception:
            return False, ""
        rel_text = str(relative).replace("\\", "/")
        rel_norm = rel_text.lower()
        if rel_norm.startswith((".conda-occ/", ".venv", "__pycache__/")):
            return False, rel_text
        if filters and not any(token in rel_norm for token in filters):
            return False, rel_text
        return True, rel_text

    def _trace(frame, event, arg):
        if event != "call":
            return _trace
        should_trace, rel_text = _should_trace(frame.f_code.co_filename)
        if should_trace:
            thread_name = threading.current_thread().name
            func_name = frame.f_code.co_name
            line_no = frame.f_code.co_firstlineno
            print(f"[TRACE][{thread_name}] {rel_text}:{line_no} -> {func_name}", flush=True)
        return _trace

    sys.setprofile(_trace)
    threading.setprofile(_trace)
    filter_text = ", ".join(filters) if filters else "project files"
    print(f"[TRACE] Python call tracing enabled for {filter_text}", flush=True)


def bootstrap_runtime(anchor_file: str | os.PathLike[str]) -> dict[str, object]:
    anchor_path = Path(anchor_file).resolve()
    project_root = anchor_path if anchor_path.is_dir() else anchor_path.parent
    env_root = project_root / ".conda-occ"
    dll_dirs = [path for path in _candidate_dll_dirs(env_root) if path.is_dir()]

    if dll_dirs:
        existing_path = os.environ.get("PATH", "")
        existing_parts = [part for part in existing_path.split(os.pathsep) if part]
        existing_norm = {os.path.normcase(os.path.normpath(part)) for part in existing_parts}
        prepend_parts = []
        for path in dll_dirs:
            path_str = str(path)
            norm = os.path.normcase(os.path.normpath(path_str))
            if norm not in existing_norm:
                prepend_parts.append(path_str)
                existing_norm.add(norm)
        if prepend_parts:
            os.environ["PATH"] = os.pathsep.join(prepend_parts + existing_parts)

        add_dll_directory = getattr(os, "add_dll_directory", None)
        if callable(add_dll_directory):
            handles = []
            for path in dll_dirs:
                try:
                    handles.append(add_dll_directory(str(path)))
                except OSError:
                    continue
            if handles:
                globals()["_DLL_HANDLES"] = handles

    os.environ.setdefault("QT_OPENGL", "desktop")
    os.environ.setdefault("QT_ANGLE_PLATFORM", "desktop")
    os.environ.setdefault("QSG_RHI_BACKEND", "opengl")
    _maybe_enable_call_tracing(project_root)

    return {
        "project_root": project_root,
        "env_root": env_root,
        "dll_dirs": dll_dirs,
    }
