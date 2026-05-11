from ._controller_common import *
from project_paths import PROJECT_ROOT

class PostProcessMixin:
    def scan_post_process_case(self):
        try:
            case_dir = self._execution_case_dir()
            self._refresh_post_process_state(case_dir)
            self._sync_widgets_from_state()
            pp = self.openfoam.get("post_process", {})
            fields = pp.get("available_fields", [])
            QMessageBox.information(
                self.ui.aerodynamics_tab,
                "Post Process Scan",
                f"Scanned case:\n{case_dir}\n\nDetected fields: {', '.join(fields) if fields else '(none)'}",
            )
        except Exception as exc:
            QMessageBox.critical(self.ui.aerodynamics_tab, "Post Process Scan Failed", str(exc))

    def _sync_paraview_path_from_input(self):
        if not hasattr(self, "input_paraview_path"):
            return
        path = str(self.input_paraview_path.text()).strip()
        self._set_openfoam_value("post_process.paraview_path", path)

    def pick_paraview_path(self):
        current = str(self.openfoam.get("post_process", {}).get("paraview_path", "")).strip()
        start_dir = str(Path(current).parent) if current else ""
        if not start_dir or not Path(start_dir).exists():
            start_dir = str(PROJECT_ROOT)
        file_path, _ = QFileDialog.getOpenFileName(
            self.ui.aerodynamics_tab,
            "Select ParaView Executable",
            start_dir,
            "ParaView (paraview.exe);;Executables (*.exe);;All Files (*.*)",
        )
        if not file_path:
            return
        self._set_openfoam_value("post_process.paraview_path", str(file_path))
        self._sync_widgets_from_state()

    def _resolve_paraview_exe(self):
        pp = self.openfoam.get("post_process", {})
        raw = str(pp.get("paraview_path", "")).strip()
        candidates = []
        if raw:
            path = Path(raw)
            candidates.extend([path, path / "paraview.exe", path / "bin" / "paraview.exe"])
        for env_key in ("PARAVIEW_HOME", "PARAVIEW_ROOT"):
            env_val = str(os.environ.get(env_key, "")).strip()
            if env_val:
                root = Path(env_val)
                candidates.extend([root / "paraview.exe", root / "bin" / "paraview.exe"])
        known_roots = [
            Path("F:/OpenFoam/ParaView-5.12.0-Windows-Python3.10-msvc2017-AMD64"),
        ]
        for root in known_roots:
            candidates.extend([root / "paraview.exe", root / "bin" / "paraview.exe"])
        for cand in candidates:
            if cand.is_file():
                if raw != str(cand):
                    self._set_openfoam_value("post_process.paraview_path", str(cand))
                return cand
        return None

    def open_paraview_from_ui(self):
        case_dir = Path(str(self.openfoam.get("post_process", {}).get("case_dir", "")).strip())
        if not case_dir.is_dir():
            case_dir = self._execution_case_dir()
        if not case_dir.is_dir():
            QMessageBox.warning(self.ui.aerodynamics_tab, "ParaView", f"Case directory not found:\n{case_dir}")
            return
        exe = self._resolve_paraview_exe()
        if exe is None:
            QMessageBox.warning(
                self.ui.aerodynamics_tab,
                "ParaView",
                "ParaView executable not found. Set the path and try again.",
            )
            return
        foam_file = case_dir / f"{case_dir.name}.foam"
        if not foam_file.exists():
            try:
                foam_file.write_text("", encoding="utf-8")
            except Exception:
                pass
        process = QProcess(self.ui.aerodynamics_tab)
        process.setProgram(str(exe))
        process.setArguments([str(foam_file)])
        process.setWorkingDirectory(str(case_dir))
        process.start()
        self._paraview_process = process

    def _normalize_vtk_kind(self, value):
        text = str(value or "").strip().lower()
        if text.startswith("snappy"):
            return "snappy"
        return "blockMesh"

    def _vtk_export_dir(self, case_dir, kind):
        kind_name = "snappy" if kind == "snappy" else "blockMesh"
        return Path(case_dir) / f"VTK_{kind_name}"

    def export_vtk_from_ui(self):
        kind = self._normalize_vtk_kind(self.cmb_vtk_mesh.currentText() if hasattr(self, "cmb_vtk_mesh") else "snappy")
        self.run_vtk_export(kind)

    def load_vtk_from_ui(self):
        kind = self._normalize_vtk_kind(self.cmb_vtk_mesh.currentText() if hasattr(self, "cmb_vtk_mesh") else "blockMesh")
        self.load_vtk_mesh(kind)

    def run_vtk_export(self, kind):
        if self._of_process is not None or self._of_queue:
            QMessageBox.warning(self.ui.aerodynamics_tab, "OpenFOAM Run", "A run is already in progress.")
            return
        case_dir = self._execution_case_dir()
        if not self._require_allowed_case_dir(case_dir, "VTK export"):
            return
        if not (case_dir / "system" / "controlDict").is_file():
            QMessageBox.warning(self.ui.aerodynamics_tab, "OpenFOAM Run", f"Case not found: {case_dir}")
            return
        kind = self._normalize_vtk_kind(kind)
        log_path = case_dir / f"log.foamToVTK.{kind}.txt"
        plan = [
            {
                "kind": "process",
                "stage": "vtk_export",
                "cmd": ["foamToVTK", "-constant"],
                "desc": f"foamToVTK ({kind})",
                "log_path": str(log_path),
            },
            {
                "kind": "callable",
                "stage": "vtk_export",
                "fn": lambda: self._finalize_vtk_export(case_dir, kind),
            },
        ]
        self._set_openfoam_value("execution.case_dir", str(case_dir))
        self._set_openfoam_value("execution.status", "running")
        self._set_openfoam_value("execution.active_stage", "vtk_export")
        self._set_openfoam_value("execution.last_run_started_at", datetime.now().isoformat(timespec="seconds"))
        self._set_openfoam_value("execution.last_run_finished_at", "")
        self._set_openfoam_value("execution.last_error", "")
        self._set_openfoam_value("execution.last_logs", {})
        self._of_cancel_requested = False
        self._of_run_mode = "vtk-export"
        self._of_requested_stage = f"vtk-export-{kind}"
        self._of_queue = plan
        self._of_current = None
        self._clear_run_log_output()
        self._append_run_log(f"[{datetime.now().isoformat(timespec='seconds')}] Started VTK export: {kind}")
        self._set_execution_controls_running(True)
        self._sync_widgets_from_state()
        self._run_next_openfoam_entry()

    def _finalize_vtk_export(self, case_dir, kind):
        case_path = Path(case_dir)
        src = case_path / "VTK"
        dest = self._vtk_export_dir(case_path, kind)
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()
        if not src.is_dir():
            raise FileNotFoundError("VTK output folder not found after foamToVTK.")
        shutil.move(str(src), str(dest))
        status = f"VTK {kind} exported: {dest}"
        self._set_openfoam_value("post_process.vtk_status", status)
        self._append_run_log(f"[info] {status}")
        self._sync_widgets_from_state(refresh_viewer=False)
        return str(dest)

    def load_vtk_mesh(self, kind):
        case_dir = self._execution_case_dir()
        kind = self._normalize_vtk_kind(kind)
        vtk_root = self._vtk_export_dir(case_dir, kind)
        dataset = self._find_vtk_dataset(vtk_root)
        if dataset is None:
            msg = f"VTK dataset not found in:\n{vtk_root}"
            self._set_openfoam_value("post_process.vtk_status", f"VTK {kind} load failed: not found")
            self._sync_widgets_from_state(refresh_viewer=False)
            QMessageBox.warning(self.ui.aerodynamics_tab, "VTK Load", msg)
            return
        try:
            mesh = self._read_vtk_dataset(dataset)
        except Exception as exc:
            self._set_openfoam_value("post_process.vtk_status", f"VTK {kind} load failed: {exc}")
            self._sync_widgets_from_state(refresh_viewer=False)
            QMessageBox.critical(self.ui.aerodynamics_tab, "VTK Load Failed", str(exc))
            return
        self._vtk_mesh = mesh
        self._vtk_meshes[kind] = mesh
        self._vtk_active_kind = kind
        self._set_openfoam_value("post_process.vtk_status", f"VTK loaded ({kind}): {dataset}")
        self._sync_widgets_from_state(refresh_viewer=False)
        self._refresh_viewer_scene()

    def _find_vtk_dataset(self, vtk_root):
        root = Path(vtk_root)
        if not root.is_dir():
            return None
        time_dirs = [d for d in root.iterdir() if d.is_dir()]
        target_dir = root
        if time_dirs:
            def sort_key(d):
                try:
                    return (0, float(d.name))
                except Exception:
                    return (1, d.name)
            time_dirs.sort(key=sort_key)
            target_dir = time_dirs[-1]
        candidate = target_dir / "internalMesh.vtu"
        if candidate.is_file():
            return candidate
        for found in target_dir.rglob("internalMesh.vtu"):
            if found.is_file():
                return found
        for pattern in ("*.vtm", "*.vtu", "*.vtk"):
            files = sorted(target_dir.glob(pattern))
            if files:
                return files[0]
        for pattern in ("*.vtm", "*.vtu", "*.vtk"):
            files = sorted(target_dir.rglob(pattern))
            if files:
                return files[0]
        return None

    def _read_vtk_dataset(self, path):
        mesh = pv.read(str(path))
        try:
            if isinstance(mesh, pv.MultiBlock):
                combined = None
                try:
                    combined = mesh.combine()
                except Exception:
                    combined = None
                if combined is None or getattr(combined, "n_points", 0) <= 0:
                    for block in mesh:
                        if block is not None and getattr(block, "n_points", 0) > 0:
                            combined = block
                            break
                if combined is None:
                    raise ValueError("VTK dataset is empty.")
                mesh = combined
        except Exception:
            pass
        return mesh

    def _refresh_post_process_state(self, case_dir):
        case_path = Path(case_dir)
        pp = self.openfoam.setdefault("post_process", {})
        pp["case_dir"] = str(case_path)
        pp["latest_time"] = ""
        pp["available_fields"] = []
        pp["stage_logs"] = {}
        log_map = {
            "domain_mesh": case_path / "log.domain_mesh.txt",
            "surface_features": case_path / "log.surface_features.txt",
            "snappy_mesh": case_path / "log.snappy_mesh.txt",
            "check_mesh": case_path / "log.check_mesh.txt",
            "solve": case_path / "log.solve.txt",
        }
        pp["stage_logs"] = {k: str(v) for k, v in log_map.items() if v.is_file()}
        time_dirs = []
        if case_path.is_dir():
            for child in case_path.iterdir():
                if child.is_dir():
                    try:
                        tval = float(child.name)
                        time_dirs.append((tval, child))
                    except Exception:
                        continue
        if time_dirs:
            _, latest = sorted(time_dirs, key=lambda x: x[0])[-1]
            pp["latest_time"] = latest.name
            fields = []
            for item in latest.iterdir():
                if item.is_file() and item.name not in {"uniform"}:
                    fields.append(item.name)
            pp["available_fields"] = sorted(set(fields))
        pp["updated_at"] = datetime.now().isoformat(timespec="seconds")
        self.state.setdefault("aerodynamics", {})["openfoam"] = self.openfoam
