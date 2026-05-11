from ._controller_common import *
from .foam_case_files import build_case_files, build_run_scripts
from project_paths import OPENFOAM_CONFIG_PATH

class CaseManagementMixin:
    def _detect_mesh_preset(self):
        mesh = self.openfoam.get("mesh", {})
        for name in ("External Aerodynamics", "Coarse", "Medium", "Fine"):
            preset = _mesh_for_preset(name)
            if (
                mesh.get("base_cells") == preset.get("base_cells")
                and mesh.get("refinement_min") == preset.get("refinement_min")
                and mesh.get("refinement_max") == preset.get("refinement_max")
                and mesh.get("n_surface_layers") == preset.get("n_surface_layers")
            ):
                return name
        return mesh.get("preset", "External Aerodynamics")

    def _detect_snappy_profile(self):
        mesh = self.openfoam.get("mesh", {})
        for name in ("Balanced", "Fast", "High Fidelity"):
            profile = _snappy_profile_for(name)
            matches = True
            for key, value in profile.items():
                current = mesh.get(key)
                if current is None:
                    matches = False
                    break
                if isinstance(value, float):
                    if abs(float(current) - value) > 1.0e-6:
                        matches = False
                        break
                else:
                    if int(current) != int(value):
                        matches = False
                        break
            if matches:
                return name
        return "Custom"

    def import_openfoam_case_from_dialog(self):
        root = self._required_case_root()
        start_dir = str(root) if root.exists() else str(root.parent)
        folder = QFileDialog.getExistingDirectory(self.ui.aerodynamics_tab, "Select OpenFOAM Case Folder", start_dir)
        if folder:
            return self.import_openfoam_case(folder)
        return False

    def import_openfoam_case(self, case_dir):
        case_path = Path(case_dir)
        if not case_path.is_dir():
            QMessageBox.warning(self.ui.aerodynamics_tab, "OpenFOAM Import", f"Case not found:\n{case_path}")
            return False
        if not self._require_allowed_case_dir(case_path, "Import"):
            return False
        if not (case_path / "system" / "controlDict").is_file():
            QMessageBox.warning(self.ui.aerodynamics_tab, "OpenFOAM Import", f"controlDict not found:\n{case_path}")
            return False
        try:
            openfoam_state, warnings = parse_openfoam_case(case_path, self.openfoam)
        except Exception as exc:
            QMessageBox.critical(self.ui.aerodynamics_tab, "OpenFOAM Import Failed", str(exc))
            return False
        self.openfoam = openfoam_state
        self.state.setdefault("aerodynamics", {})["openfoam"] = self.openfoam
        self._set_openfoam_value("execution.case_dir", str(case_path))
        self._set_openfoam_value("export.output_path", str(case_path))
        self._set_openfoam_value("execution.status", "idle")
        self._set_openfoam_value("execution.active_stage", "none")
        self._set_openfoam_value("execution.last_run_started_at", "")
        self._set_openfoam_value("execution.last_run_finished_at", "")
        self._set_openfoam_value("execution.last_error", "")
        self._set_openfoam_value("execution.last_logs", {})
        self._set_openfoam_value("execution.results", {})
        self._set_openfoam_value("post_process.vtk_status", "VTK: not exported")
        self._set_openfoam_value("post_process.latest_time", "")
        self._set_openfoam_value("post_process.available_fields", [])
        self._set_openfoam_value("post_process.updated_at", "")
        self.openfoam["mesh"]["preset"] = self._detect_mesh_preset()
        self.openfoam["mesh"]["snappy_profile"] = self._detect_snappy_profile()
        self.state.setdefault("aerodynamics", {})["openfoam"] = self.openfoam
        self._refresh_post_process_state(case_path)
        self._sync_widgets_from_state()
        self._notify_property_refresh()
        self._notify_case_opened(case_path)
        if warnings:
            QMessageBox.information(
                self.ui.aerodynamics_tab,
                "OpenFOAM Import",
                "Case imported with warnings:\n" + "\n".join(warnings),
            )
        return True

    def clear_openfoam_case(self):
        self._set_openfoam_value("execution.case_dir", "")
        self._set_openfoam_value("export.output_path", "")
        self._set_openfoam_value("export.generated_files", [])
        self._set_openfoam_value("export.last_exported_at", "")
        self._set_openfoam_value("export.last_action", "")
        self._set_openfoam_value("execution.status", "idle")
        self._set_openfoam_value("execution.active_stage", "none")
        self._set_openfoam_value("execution.last_run_started_at", "")
        self._set_openfoam_value("execution.last_run_finished_at", "")
        self._set_openfoam_value("execution.last_error", "")
        self._set_openfoam_value("execution.last_logs", {})
        self._set_openfoam_value("execution.results", {})
        self._set_openfoam_value("post_process.case_dir", "")
        self._set_openfoam_value("post_process.available_fields", [])
        self._set_openfoam_value("post_process.latest_time", "")
        self._set_openfoam_value("post_process.updated_at", "")
        self._set_openfoam_value("post_process.vtk_status", "VTK: not exported")
        self._set_openfoam_value("post_process.stage_logs", {})
        self._sync_widgets_from_state()
        self._notify_property_refresh()

    def clean_openfoam_case(self):
        if self._of_process is not None or self._of_queue:
            QMessageBox.warning(self._dialog_parent(), "OpenFOAM Clean", "Stop the current run before cleaning the case.")
            return
        case_dir = self._execution_case_dir()
        if not self._require_allowed_case_dir(case_dir, "Clean case"):
            return
        if not case_dir.exists():
            QMessageBox.information(self._dialog_parent(), "OpenFOAM Clean", f"Case directory not found:\n{case_dir}")
            return
        answer = QMessageBox.question(
            self._dialog_parent(),
            "Clean OpenFOAM Case",
            "Remove generated mesh, run logs, VTK exports, time folders, and solver results from this case?\n\n"
            f"{case_dir}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return

        removed = []

        def remove_path(target):
            target_path = Path(target)
            if not target_path.exists():
                return
            try:
                if target_path.is_dir():
                    shutil.rmtree(target_path)
                else:
                    target_path.unlink()
                removed.append(str(target_path))
            except Exception:
                pass

        def is_time_dir(name):
            try:
                float(str(name))
                return True
            except Exception:
                return False

        constant_dir = case_dir / "constant"
        for child_name in ("polyMesh", "extendedFeatureEdgeMesh", "surfaceFeatures"):
            remove_path(constant_dir / child_name)

        for child in case_dir.iterdir():
            name = child.name
            if child.is_dir() and (name.startswith("processor") or name in {"postProcessing", "VTK", "VTK_blockMesh", "VTK_snappy"} or is_time_dir(name)):
                remove_path(child)
                continue
            if child.is_file() and (name.startswith("log") or name.endswith(".foam")):
                remove_path(child)

        self._vtk_mesh = None
        self._vtk_meshes = {}
        self._vtk_active_kind = None
        self._viewer_scalar_field = ""
        self._viewer_contours_enabled = False
        self._viewer_slice_enabled = False
        self._viewer_streamlines_enabled = False
        self._set_openfoam_value("execution.last_logs", {})
        self._set_openfoam_value("execution.status", "idle")
        self._set_openfoam_value("execution.active_stage", "none")
        self._set_openfoam_value("execution.last_error", "")
        self._set_openfoam_value("post_process.vtk_status", "VTK: not exported")
        self._refresh_post_process_state(case_dir)
        self._sync_widgets_from_state()
        self._notify_property_refresh()
        self._append_run_log(f"[info] Cleaned {len(removed)} generated path(s) under {case_dir}.")

    def _pick_export_dir(self):
        cur = self.openfoam["export"].get("output_path", "")
        root = self._required_case_root()
        if cur and self._case_dir_is_allowed(cur):
            start_dir = cur
        else:
            start_dir = str(root) if root.exists() else str(root.parent)
        path = QFileDialog.getExistingDirectory(self.ui.aerodynamics_tab, "Select OpenFOAM Case Output", start_dir)
        if path:
            if not self._require_allowed_case_dir(path, "Output selection"):
                return
            self._set_openfoam_value("export.output_path", path)
            self._sync_widgets_from_state()

    def _clear_cfd_stl(self):
        self._set_openfoam_value("geometry.stl_path", "")
        self._sync_widgets_from_state()

    def import_cfd_stl_from_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.ui.aerodynamics_tab,
            "Import CFD STL",
            "",
            "STL Files (*.stl);;All Files (*.*)",
        )
        if not file_path:
            return
        self.import_cfd_stl(file_path)

    def import_cfd_stl(self, file_path):
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"STL file not found: {path}")
        tri_name = path.stem.replace(" ", "_")
        self._set_openfoam_value("geometry.stl_path", str(path))
        self._set_openfoam_value("geometry.tri_surface_name", tri_name or "aircraft")
        self._sync_widgets_from_state()

    def _check_stl_watertightness(self):
        """Check if the loaded STL is watertight (closed, no holes).
        
        This uses multiple checks aligned with MeshLab's watertightness criteria:
        1. No boundary edges (all edges shared by exactly 2 faces)
        2. Manifold property (locally consistent topology)
        3. No duplicate/degenerate faces
        """
        stl_path = self.openfoam.get("geometry", {}).get("stl_path", "")
        if not stl_path or not Path(stl_path).exists():
            self.lbl_watertight_status.setText("No STL loaded")
            self.lbl_watertight_status.setStyleSheet("color: #999; font-size: 10px;")
            return
        
        try:
            # Load STL with PyVista
            mesh = pv.read(str(stl_path))
            
            # Clean mesh first to remove degenerate faces
            mesh_clean = mesh.clean()
            
            # Check 1: Count boundary edges by analyzing face adjacency
            # A watertight mesh has no edges with < 2 adjacent faces
            n_cells = mesh_clean.n_cells
            n_points = mesh_clean.n_points
            
            # Get all faces and build edge-to-face mapping
            faces = mesh_clean.faces.reshape(-1, 4)[:, 1:]  # Skip face size indicator
            edge_count = {}
            
            for face_idx, face in enumerate(faces):
                # For each triangle, get the 3 edges
                edges = [(face[0], face[1]), (face[1], face[2]), (face[2], face[0])]
                for e0, e1 in edges:
                    # Normalize edge (smaller index first) for consistent counting
                    edge = tuple(sorted([e0, e1]))
                    edge_count[edge] = edge_count.get(edge, 0) + 1
            
            # Find boundary edges (shared by only 1 face, not 2)
            boundary_edges_count = sum(1 for count in edge_count.values() if count != 2)
            is_watertight = boundary_edges_count == 0
            
            # Check 2: Verify manifold property (optional but informative)
            has_non_manifold = any(count > 2 for count in edge_count.values())
            
            # Format status message
            if is_watertight and not has_non_manifold:
                status = f"✓ WATERTIGHT | {n_cells:,} faces, {n_points:,} points"
                self.lbl_watertight_status.setStyleSheet("color: #4caf50; font-size: 10px; font-weight: bold;")
            else:
                issues = []
                if boundary_edges_count > 0:
                    issues.append(f"{boundary_edges_count} boundary edges")
                if has_non_manifold:
                    issues.append("non-manifold edges")
                status = f"✗ NOT WATERTIGHT | {n_cells:,} faces | {', '.join(issues)}"
                self.lbl_watertight_status.setStyleSheet("color: #f44336; font-size: 10px; font-weight: bold;")
            
            self.lbl_watertight_status.setText(status)
            self._append_run_log(f"[info] STL watertightness check: {status}")
            
        except Exception as e:
            status = f"Error checking watertightness: {str(e)}"
            self.lbl_watertight_status.setText(status)
            self.lbl_watertight_status.setStyleSheet("color: #ff9800; font-size: 10px;")
            self._append_run_log(f"[error] {status}")

    def _preview_case_files(self):
        errors = self._validate_openfoam_state()
        if errors:
            QMessageBox.warning(self.ui.aerodynamics_tab, "OpenFOAM Setup", "\n".join(errors))
            return
        files = build_case_files(self.openfoam)
        names = sorted(list(files.keys()))
        scripts = build_run_scripts(self.openfoam) if self.openfoam["scripts"]["write_helper_scripts"] else {}
        names.extend(sorted(list(scripts.keys())))
        QMessageBox.information(self.ui.aerodynamics_tab, "OpenFOAM Case Preview", "Generated files:\n" + "\n".join(names))

    def _openfoam_config_payload(self):
        payload = deepcopy(self.openfoam)
        execution = payload.get("execution", {})
        if isinstance(execution, dict):
            execution["status"] = "idle"
            execution["active_stage"] = "none"
            execution["last_run_started_at"] = ""
            execution["last_run_finished_at"] = ""
            execution["last_error"] = ""
            execution["last_logs"] = {}
            execution["results"] = {}
        return payload

    def save_openfoam_config(self, file_path):
        target = Path(file_path)
        if target.suffix.lower() not in (".json", ".ofcfg"):
            target = target.with_suffix(".json")
        payload = {
            "format": "ad_gui_openfoam_config",
            "version": 1,
            "saved_at": datetime.now().isoformat(timespec="seconds"),
            "openfoam": self._openfoam_config_payload(),
        }
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return str(target)

    def save_openfoam_config_from_dialog(self):
        initial = self.openfoam.get("export", {}).get("output_path", "") or str(OPENFOAM_CONFIG_PATH.parent)
        file_path, _ = QFileDialog.getSaveFileName(
            self.ui.aerodynamics_tab,
            "Save OpenFOAM Config",
            str(Path(initial) / "openfoam_config.json"),
            "OpenFOAM Config (*.json *.ofcfg);;JSON Files (*.json);;All Files (*.*)",
        )
        if not file_path:
            return
        try:
            target = self.save_openfoam_config(file_path)
            QMessageBox.information(self.ui.aerodynamics_tab, "OpenFOAM Config", f"Configuration saved:\n{target}")
        except Exception as exc:
            QMessageBox.critical(self.ui.aerodynamics_tab, "OpenFOAM Config Save Failed", str(exc))

    def load_openfoam_config(self, file_path):
        source = Path(file_path)
        raw = source.read_text(encoding="utf-8")
        payload = json.loads(raw)
        if isinstance(payload, dict) and "openfoam" in payload and isinstance(payload["openfoam"], dict):
            openfoam_payload = payload["openfoam"]
        elif isinstance(payload, dict):
            openfoam_payload = payload
        else:
            raise ValueError("Invalid config payload.")
        aero_state = self.state.setdefault("aerodynamics", {})
        aero_state["openfoam"] = deepcopy(openfoam_payload)
        self.openfoam = ensure_openfoam_state(aero_state)
        self._set_openfoam_value("execution.status", "idle")
        self._set_openfoam_value("execution.active_stage", "none")
        self._set_openfoam_value("execution.last_run_started_at", "")
        self._set_openfoam_value("execution.last_run_finished_at", "")
        self._set_openfoam_value("execution.last_error", "")
        self._set_openfoam_value("execution.last_logs", {})
        self._set_openfoam_value("execution.results", {})
        self._vtk_mesh = None
        self._vtk_meshes = {}
        self._vtk_active_kind = None
        self._sync_widgets_from_state()
        self._notify_property_refresh()
        return True

    def load_openfoam_config_from_dialog(self):
        initial = self.openfoam.get("export", {}).get("output_path", "") or str(OPENFOAM_CONFIG_PATH.parent)
        file_path, _ = QFileDialog.getOpenFileName(
            self.ui.aerodynamics_tab,
            "Load OpenFOAM Config",
            str(initial),
            "OpenFOAM Config (*.json *.ofcfg);;JSON Files (*.json);;All Files (*.*)",
        )
        if not file_path:
            return
        try:
            self.load_openfoam_config(file_path)
            QMessageBox.information(self.ui.aerodynamics_tab, "OpenFOAM Config", f"Configuration loaded:\n{file_path}")
        except Exception as exc:
            QMessageBox.critical(self.ui.aerodynamics_tab, "OpenFOAM Config Load Failed", str(exc))

    def export_openfoam_case_from_dialog(self):
        target = self.openfoam["export"].get("output_path", "")
        root = self._required_case_root()
        if target and self._case_dir_is_allowed(target):
            start_dir = target
        else:
            start_dir = str(root) if root.exists() else str(root.parent)
        folder = QFileDialog.getExistingDirectory(self.ui.aerodynamics_tab, "Select OpenFOAM Case Folder", start_dir)
        if not folder:
            return
        if not self._require_allowed_case_dir(folder, "Export"):
            return
        try:
            self.export_openfoam_case(folder)
            QMessageBox.information(self.ui.aerodynamics_tab, "OpenFOAM Case", f"Case generated:\n{folder}")
        except Exception as exc:
            QMessageBox.critical(self.ui.aerodynamics_tab, "OpenFOAM Case Export Failed", str(exc))

    def update_openfoam_case_from_ui(self):
        target = str(self.openfoam.get("execution", {}).get("case_dir", "")).strip()
        if not target:
            target = str(self.openfoam.get("export", {}).get("output_path", "")).strip()
        if not target:
            QMessageBox.warning(
                self.ui.aerodynamics_tab,
                "OpenFOAM Case Update",
                "No case folder set. Import or generate a case first.",
            )
            return
        if not self._require_allowed_case_dir(target, "Update"):
            return
        try:
            self.export_openfoam_case(target, action="updated")
        except Exception as exc:
            QMessageBox.critical(self.ui.aerodynamics_tab, "OpenFOAM Case Update Failed", str(exc))

    def _validate_openfoam_state(self):
        errors = []
        stl = self.openfoam["geometry"].get("stl_path", "")
        if not stl:
            errors.append("Geometry STL is required.")
        elif not Path(stl).is_file():
            errors.append(f"Geometry STL not found: {stl}")
        dmin = self.openfoam["mesh"]["domain_min"]
        dmax = self.openfoam["mesh"]["domain_max"]
        for i, axis in enumerate(("x", "y", "z")):
            if dmin[i] >= dmax[i]:
                errors.append(f"Mesh domain invalid: {axis}min must be < {axis}max.")
        return errors

    def export_openfoam_case(self, target_dir, action="generated"):
        errors = self._validate_openfoam_state()
        if errors:
            raise ValueError("\n".join(errors))
        target = Path(target_dir)
        target.mkdir(parents=True, exist_ok=True)
        files = build_case_files(self.openfoam)
        generated = []
        for rel, content in files.items():
            out = target / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(content, encoding="utf-8")
            generated.append(rel)
        stl_src = Path(self.openfoam["geometry"]["stl_path"])
        tri_out = target / "constant" / "triSurface" / stl_src.name
        tri_out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(stl_src, tri_out)
        generated.append(f"constant/triSurface/{stl_src.name}")
        geo_out = target / "constant" / "geometry" / stl_src.name
        geo_out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(stl_src, geo_out)
        generated.append(f"constant/geometry/{stl_src.name}")
        if self.openfoam["scripts"]["write_helper_scripts"]:
            scripts = build_run_scripts(self.openfoam)
            for rel, content in scripts.items():
                out = target / rel
                out.write_text(content, encoding="utf-8", newline="\n")
                generated.append(rel)
        stamp = datetime.now().isoformat(timespec="seconds")
        self._set_openfoam_value("export.output_path", str(target))
        self._set_openfoam_value("export.last_exported_at", stamp)
        self._set_openfoam_value("export.last_action", str(action))
        self._set_openfoam_value("export.generated_files", sorted(generated))
        self._sync_widgets_from_state()
        return sorted(generated)
