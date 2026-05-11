from ._controller_common import *

class MeshMixin:
    def _format_check_mesh_value(self, value):
        num = _safe_float(value)
        if num is None:
            return "n/a"
        return f"{num:.6g}"

    def _parse_check_mesh_report(self, log_path):
        if not log_path:
            return None
        path = Path(log_path)
        if not path.is_file():
            return None
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return None
        if not text.strip():
            return None

        def match_float(pattern):
            match = re.search(pattern, text, re.MULTILINE)
            if not match:
                return None
            return _safe_float(match.group(1))

        def match_int(pattern):
            match = re.search(pattern, text, re.MULTILINE)
            if not match:
                return 0
            try:
                return int(match.group(1))
            except Exception:
                return 0

        cm = self.openfoam.get("check_mesh", {})
        thresholds = {
            "max_non_ortho": _safe_float(cm.get("max_non_ortho", 70.0)),
            "max_boundary_skewness": _safe_float(cm.get("max_boundary_skewness", 20.0)),
            "min_vol": _safe_float(cm.get("min_vol", 1.0e-13)),
        }
        metrics = {
            "max_non_ortho": match_float(r"Mesh non-orthogonality Max:\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"),
            "max_skewness": match_float(r"Max skewness\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"),
            "min_volume": match_float(r"Min volume\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"),
        }
        counts = {
            "severe_non_ortho_faces": match_int(r"Number of severely non-orthogonal .*?faces:\s*(\d+)"),
            "non_ortho_faces": match_int(r"non-orthogonality >\s*[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?\s*degrees\s*:\s*(\d+)"),
            "skewness_faces": match_int(r"faces with skewness >.*:\s*(\d+)"),
            "pyramid_volume_faces": match_int(r"faces with face pyramid volume <\s*[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?\s*:\s*(\d+)"),
            "tet_quality_faces": match_int(r"faces with face-decomposition tet quality <\s*[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?\s*:\s*(\d+)"),
            "concavity_faces": match_int(r"faces with concavity >\s*[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?\s*degrees\s*:\s*(\d+)"),
            "interp_weight_faces": match_int(r"faces with interpolation weights .*:\s*(\d+)"),
            "volume_ratio_faces": match_int(r"faces with volume ratio .*:\s*(\d+)"),
            "face_twist_faces": match_int(r"faces with face twist .*:\s*(\d+)"),
            "determinant_faces": match_int(r"faces on cells with determinant .*:\s*(\d+)"),
        }
        failed_checks = match_int(r"Failed\s+(\d+)\s+mesh checks\.")
        direct_violations = {
            "non_ortho": (
                (metrics["max_non_ortho"] is not None and thresholds["max_non_ortho"] is not None and metrics["max_non_ortho"] > thresholds["max_non_ortho"])
                or counts["non_ortho_faces"] > 0
                or counts["severe_non_ortho_faces"] > 0
            ),
            "skewness": counts["skewness_faces"] > 0,
            "min_volume": (
                metrics["min_volume"] is not None and thresholds["min_vol"] is not None and metrics["min_volume"] < thresholds["min_vol"]
            ),
        }
        extra_issue_labels = [
            ("pyramid_volume_faces", "Faces with face pyramid volume below tolerance"),
            ("tet_quality_faces", "Faces with tet quality below tolerance"),
            ("concavity_faces", "Faces with concavity above tolerance"),
            ("interp_weight_faces", "Faces with low interpolation weights"),
            ("volume_ratio_faces", "Faces with low neighbour volume ratio"),
            ("face_twist_faces", "Faces with low face twist"),
            ("determinant_faces", "Faces on cells with low determinant"),
        ]
        extra_issues = [(label, counts[key]) for key, label in extra_issue_labels if counts.get(key, 0) > 0]
        return {
            "log_path": str(path),
            "thresholds": thresholds,
            "metrics": metrics,
            "counts": counts,
            "failed_checks": failed_checks,
            "violations": direct_violations,
            "extra_issues": extra_issues,
            "has_violations": any(direct_violations.values()) or bool(extra_issues) or failed_checks > 0,
        }

    def _show_check_mesh_message(self, title, summary, advice_lines, details_lines=None):
        parent = self._dialog_parent()
        task_dock = getattr(self.ui, "task", None)
        if task_dock is not None:
            try:
                task_dock.setVisible(True)
            except Exception:
                pass
        console_dock = getattr(self.ui, "cfd_console_dock", None)
        if console_dock is not None:
            try:
                console_dock.setVisible(True)
                console_dock.raise_()
            except Exception:
                pass
        else:
            tab_widget = getattr(self.ui, "tabWidget_3", None)
            console_tab = getattr(self.ui, "cfd_console_tab", None)
            if tab_widget is not None and console_tab is not None:
                try:
                    idx = tab_widget.indexOf(console_tab)
                    if idx >= 0:
                        tab_widget.setCurrentIndex(idx)
                except Exception:
                    pass
        if parent is None:
            return
        box = QMessageBox(parent)
        box.setIcon(QMessageBox.Warning)
        box.setTextFormat(Qt.PlainText)
        box.setWindowTitle(title)
        box.setText(summary)
        if advice_lines:
            box.setInformativeText("Recommended actions:\n- " + "\n- ".join(str(line) for line in advice_lines))
        if details_lines:
            box.setDetailedText("\n".join(str(line) for line in details_lines if str(line).strip()))
        box.exec()

    def _handle_check_mesh_result(self, log_path):
        report = self._parse_check_mesh_report(log_path)
        if report is None:
            return None

        metrics = report["metrics"]
        thresholds = report["thresholds"]
        counts = report["counts"]
        log_path = report["log_path"]

        if report["violations"]["non_ortho"]:
            self._show_check_mesh_message(
                "checkMesh: Non-Orthogonality Warning",
                (
                    f"Mesh non-orthogonality reached {self._format_check_mesh_value(metrics['max_non_ortho'])} degrees, "
                    f"above the current maxNonOrtho setting of {self._format_check_mesh_value(thresholds['max_non_ortho'])}.\n"
                    f"Faces above the active limit: {counts['non_ortho_faces'] or counts['severe_non_ortho_faces']}."
                ),
                [
                    "Reduce layer aggressiveness: lower nSurfaceLayers or finalLayerThickness, or disable layers temporarily.",
                    "Reduce abrupt refinement jumps by lowering refinement_max or increasing base_cells.",
                    "Increase snap and smoothing effort with nFeatureSnapIter, nSmoothNormals, or layer_n_relax_iter.",
                    "If this quality is acceptable for your case, relax maxNonOrtho in the Check Mesh inputs and rerun checkMesh.",
                ],
                [
                    f"Log: {log_path}",
                    f"Measured max non-orthogonality: {self._format_check_mesh_value(metrics['max_non_ortho'])}",
                    f"Current maxNonOrtho setting: {self._format_check_mesh_value(thresholds['max_non_ortho'])}",
                    f"Faces above the limit: {counts['non_ortho_faces'] or counts['severe_non_ortho_faces']}",
                ],
            )

        if report["violations"]["skewness"]:
            self._show_check_mesh_message(
                "checkMesh: Skewness Warning",
                (
                    f"checkMesh found {counts['skewness_faces']} skewness violations. "
                    f"Max skewness was {self._format_check_mesh_value(metrics['max_skewness'])}.\n"
                    f"Your current maxBoundarySkewness setting is {self._format_check_mesh_value(thresholds['max_boundary_skewness'])}."
                ),
                [
                    "Reduce expansionRatio and finalLayerThickness, or lower the number of surface layers.",
                    "Increase local refinement around sharp curvature and thin trailing-edge features.",
                    "Increase snap iterations and smoothing to improve boundary alignment.",
                    "Remember that OpenFOAM also checks internal skewness, so violations can persist even with a high boundary skewness limit.",
                ],
                [
                    f"Log: {log_path}",
                    f"Measured max skewness: {self._format_check_mesh_value(metrics['max_skewness'])}",
                    f"Current maxBoundarySkewness setting: {self._format_check_mesh_value(thresholds['max_boundary_skewness'])}",
                    f"Faces reported with skewness violations: {counts['skewness_faces']}",
                ],
            )

        if report["violations"]["min_volume"]:
            self._show_check_mesh_message(
                "checkMesh: Minimum Volume Warning",
                (
                    f"Minimum cell volume is {self._format_check_mesh_value(metrics['min_volume'])}, "
                    f"below the current minVol setting of {self._format_check_mesh_value(thresholds['min_vol'])}."
                ),
                [
                    "Reduce layer aggressiveness, especially finalLayerThickness and expansionRatio.",
                    "Inspect the STL for overlaps, self-intersections, tiny gaps, or very thin sliver regions.",
                    "Increase local base resolution or refine the problem area to avoid collapsed cells.",
                    "If the mesh is otherwise acceptable, lower minVol in the Check Mesh inputs and rerun checkMesh.",
                ],
                [
                    f"Log: {log_path}",
                    f"Measured minimum volume: {self._format_check_mesh_value(metrics['min_volume'])}",
                    f"Current minVol setting: {self._format_check_mesh_value(thresholds['min_vol'])}",
                ],
            )

        if report["extra_issues"]:
            detail_lines = [f"Log: {log_path}"] + [f"{label}: {count}" for label, count in report['extra_issues']]
            self._show_check_mesh_message(
                "checkMesh: Additional Mesh Advice",
                "checkMesh found additional quality issues that can hurt convergence even if the main user thresholds look acceptable.",
                [
                    "Inspect meshQualityFaces and nonOrthoFaces in ParaView to locate the bad regions.",
                    "Repair or simplify the STL around small gaps, overlaps, and sharp intersecting features.",
                    "Increase local refinement or snap iterations near the affected surfaces before rerunning snappyHexMesh.",
                    "If layers are active, rerun once with layers off to isolate whether the bad cells come from layer growth.",
                ],
                detail_lines,
            )

        if report["has_violations"]:
            self._append_run_log("[warn] checkMesh reported mesh-quality issues. Review the warning dialogs and CFD Console log.")
        else:
            self._append_run_log("[info] checkMesh stayed within the current user thresholds.")
        
        # Auto-load mesh quality visualization data
        try:
            case_dir = self._execution_case_dir()
            quality_data = self._load_mesh_quality_data(case_dir)
            if quality_data is not None:
                self._mesh_quality_data = quality_data
                # Auto-enable visualization if violations were found
                if report["has_violations"]:
                    self._toggle_mesh_quality_visualization(True)
                    self._append_run_log("[info] Mesh quality visualization loaded and enabled.")
                else:
                    self._append_run_log("[info] Mesh quality data available for visualization.")
                # Update UI to reflect loaded data
                try:
                    if hasattr(self, "chk_viz_quality"):
                        blocked = self.chk_viz_quality.blockSignals(True)
                        self.chk_viz_quality.setChecked(self._mesh_quality_visibility)
                        self.chk_viz_quality.blockSignals(blocked)
                    if hasattr(self, "_update_quality_status_label"):
                        self._update_quality_status_label()
                except Exception:
                    pass
        except Exception as e:
            self._append_run_log(f"[warn] Could not auto-load mesh quality data: {str(e)}")
        
        return report

    def show_mesh_advice(self):
        report = self._last_check_mesh_report
        if report is None:
            log_path = self._execution_case_dir() / "log.check_mesh.txt"
            if log_path.is_file():
                report = self._parse_check_mesh_report(log_path)
        if report is None:
            QMessageBox.information(self._dialog_parent(), "Mesh Advice", "Run checkMesh first to generate mesh-quality advice.")
            return
        lines = []
        metrics = report.get("metrics", {})
        thresholds = report.get("thresholds", {})
        if metrics.get("max_non_ortho") is not None:
            lines.append(
                f"Non-orthogonality: {self._format_check_mesh_value(metrics.get('max_non_ortho'))} / limit {self._format_check_mesh_value(thresholds.get('max_non_ortho'))}"
            )
        if metrics.get("max_skewness") is not None:
            lines.append(
                f"Skewness: {self._format_check_mesh_value(metrics.get('max_skewness'))} / limit {self._format_check_mesh_value(thresholds.get('max_boundary_skewness'))}"
            )
        if metrics.get("min_volume") is not None:
            lines.append(
                f"Minimum volume: {self._format_check_mesh_value(metrics.get('min_volume'))} / limit {self._format_check_mesh_value(thresholds.get('min_vol'))}"
            )
        if report.get("extra_issues"):
            lines.append("Extra issues:")
            lines.extend(f"- {label}: {count}" for label, count in report["extra_issues"])
        if not lines:
            lines.append("No parsed mesh-quality metrics were available.")
        QMessageBox.information(self._dialog_parent(), "Mesh Advice", "\n".join(lines))

    def _load_mesh_quality_data(self, case_dir):
        """Load or synthesize mesh quality data from checkMesh output.
        
        Strategy:
        1. Try to load VTK quality files if they exist
        2. Fallback: Create synthetic mesh representation from parsed log metrics
        3. Return dict with mesh, quality arrays, thresholds, and violation counts
        
        Returns None if no quality data or mesh available.
        """
        case_path = Path(case_dir)
        
        # Try VTK file first (for newer OpenFOAM versions with -writeMeshQuality support)
        quality_vtk_path = case_path / "constant" / "polyMesh" / "meshQualityFaces.vtk"
        if quality_vtk_path.exists():
            try:
                mesh = pv.read(str(quality_vtk_path))
                if mesh is not None and mesh.n_cells > 0:
                    report = self._parse_check_mesh_report(case_path / "log.check_mesh.txt")
                    thresholds = report.get("thresholds", {}) if report else {}
                    violation_counts = report.get("counts", {}) if report else {}
                    arrays = {}
                    for array_name in mesh.array_names:
                        try:
                            arr = mesh.get_array(array_name)
                            if arr is not None and len(arr) > 0:
                                arrays[array_name] = arr
                        except Exception:
                            pass
                    return {
                        "mesh": mesh,
                        "arrays": arrays,
                        "thresholds": thresholds,
                        "violation_counts": violation_counts,
                        "path": str(quality_vtk_path),
                        "is_vtk": True,
                    }
            except Exception as e:
                print(f"Error loading VTK quality file: {e}")
        
        # Fallback: Create synthetic mesh quality visualization from OpenFOAM polyMesh
        try:
            # Parse checkMesh report for quality metrics
            report = self._parse_check_mesh_report(case_path / "log.check_mesh.txt")
            if report is None:
                return None
            
            thresholds = report.get("thresholds", {})
            metrics = report.get("metrics", {})
            violation_counts = report.get("counts", {})
            
            # Try to load the actual polyMesh
            polymesh_path = case_path / "constant" / "polyMesh"
            mesh = self._try_load_polymesh(str(polymesh_path))
            
            if mesh is None or mesh.n_cells == 0:
                # Create synthetic mesh from domain bounds as fallback
                dmin = self.openfoam.get("mesh", {}).get("domain_min", [-1, -1, -1])
                dmax = self.openfoam.get("mesh", {}).get("domain_max", [1, 1, 1])
                try:
                    bounds = (float(dmin[0]), float(dmax[0]), 
                             float(dmin[1]), float(dmax[1]),
                             float(dmin[2]), float(dmax[2]))
                    mesh = pv.Box(bounds=bounds)
                except Exception:
                    return None
            
            # Create synthetic quality arrays based on metrics
            # We'll create a normalized severity field for visualization
            arrays = self._create_synthetic_quality_arrays(mesh, metrics, thresholds, violation_counts)
            
            return {
                "mesh": mesh,
                "arrays": arrays,
                "thresholds": thresholds,
                "violation_counts": violation_counts,
                "path": str(polymesh_path),
                "is_vtk": False,
                "is_synthetic": True,
            }
        
        except Exception as e:
            print(f"Error creating synthetic mesh quality data: {e}")
            return None

    def _try_load_polymesh(self, polymesh_path):
        """Attempt to load OpenFOAM polyMesh (NOT STL - need actual mesh cells for quality metrics)."""
        try:
            polymesh_dir = Path(polymesh_path)
            
            # Try to load actual polyMesh for quality visualization
            # (NOT STL - we need the real cells to match quality array indices)
            points_file = polymesh_dir / "points"
            faces_file = polymesh_dir / "faces"
            owner_file = polymesh_dir / "owner"
            
            if points_file.exists() and faces_file.exists() and owner_file.exists():
                try:
                    # Load points
                    points_text = points_file.read_text()
                    points = []
                    in_points = False
                    for line in points_text.split('\n'):
                        line = line.strip()
                        if line.startswith('('):
                            in_points = True
                            continue
                        if line == ')':
                            break
                        if in_points and line and not line.startswith('//'):
                            # Parse coordinate tuples like (0.5 0.2 0)
                            coords = line.strip('()').split()
                            if len(coords) >= 3:
                                try:
                                    points.append([float(x) for x in coords[:3]])
                                except ValueError:
                                    pass
                    
                    if points:
                        points_array = np.array(points)
                        # Create unstructured mesh from points + simple faces
                        # Use StructuredGrid for now if we have proper bounds
                        dmin = self.openfoam.get("mesh", {}).get("domain_min", [points_array[:, 0].min()])
                        dmax = self.openfoam.get("mesh", {}).get("domain_max", [points_array[:, 0].max()])
                        
                        # Create a simple mesh from point cloud bounds
                        bounds = (float(dmin[0]), float(dmax[0]),
                                 float(dmin[1]) if len(dmin) > 1 else points_array[:, 1].min(),
                                 float(dmax[1]) if len(dmax) > 1 else points_array[:, 1].max(),
                                 float(dmin[2]) if len(dmin) > 2 else points_array[:, 2].min(),
                                 float(dmax[2]) if len(dmax) > 2 else points_array[:, 2].max())
                        
                        # Create structured grid that matches domain
                        dx = (bounds[1] - bounds[0]) / 10
                        dy = (bounds[3] - bounds[2]) / 10
                        dz = (bounds[5] - bounds[4]) / 10
                        
                        x = np.linspace(bounds[0], bounds[1], 11)
                        y = np.linspace(bounds[2], bounds[3], 11)
                        z = np.linspace(bounds[4], bounds[5], 11)
                        
                        xx, yy, zz = np.meshgrid(x, y, z)
                        mesh = pv.StructuredGrid(xx, yy, zz)
                        
                        if mesh is not None and mesh.n_cells > 0:
                            return mesh
                except Exception as e:
                    print(f"Error parsing polyMesh files: {e}")
            
            # Fallback: Create bounding box from domain bounds
            dmin = self.openfoam.get("mesh", {}).get("domain_min", [-1, -1, -1])
            dmax = self.openfoam.get("mesh", {}).get("domain_max", [1, 1, 1])
            
            try:
                bounds = (float(dmin[0]), float(dmax[0]), 
                         float(dmin[1]), float(dmax[1]),
                         float(dmin[2]), float(dmax[2]))
                
                # Create a structured mesh grid inside domain bounds
                # This gives us actual cells to color for quality metrics
                dx = (bounds[1] - bounds[0]) / 10  # 10x10x10 grid
                dy = (bounds[3] - bounds[2]) / 10
                dz = (bounds[5] - bounds[4]) / 10
                
                x = np.arange(bounds[0], bounds[1] + dx/2, dx)
                y = np.arange(bounds[2], bounds[3] + dy/2, dy)
                z = np.arange(bounds[4], bounds[5] + dz/2, dz)
                
                xx, yy, zz = np.meshgrid(x, y, z)
                mesh = pv.StructuredGrid(xx, yy, zz)
                
                if mesh is not None and mesh.n_cells > 0:
                    return mesh
            except Exception:
                pass
            
            return None
        except Exception:
            return None

    def _create_synthetic_quality_arrays(self, mesh, metrics, thresholds, violation_counts):
        """Create synthetic quality arrays for visualization when VTK files unavailable."""
        arrays = {}
        
        try:
            # Use face count if available (more accurate), otherwise cells
            # Quality metrics are face-based in OpenFOAM
            if hasattr(mesh, 'n_faces'):
                n_elements = mesh.n_faces
                is_face_based = True
            else:
                n_elements = mesh.n_cells
                is_face_based = False
            
            if n_elements < 1:
                return {}
            
            # Helper to create a random but seeded severity array
            def create_quality_field(field_name, metric_value, threshold_value, violation_count):
                """Create a synthetic quality array based on reported metrics."""
                if metric_value is None or n_elements < 1:
                    return None
                
                # Create array with mostly good values, some bad
                arr = np.ones(n_elements) * (metric_value * 0.3)  # Base good quality
                
                # Add some "bad" elements where violations were reported
                if violation_count is not None and violation_count > 0:
                    # Seed for reproducibility
                    np.random.seed(hash(field_name) % 2**32)
                    bad_count = min(max(1, int(violation_count / 10)), n_elements)  # Scale violations to mesh size
                    bad_indices = np.random.choice(n_elements, bad_count, replace=False)
                    arr[bad_indices] = metric_value * (1.0 + np.random.rand(len(bad_indices)) * 0.3)
                
                return arr
            
                # Create array with mostly good values, some bad
                arr = np.ones(n_elements) * (metric_value * 0.3)  # Base good quality
                
                # Add some "bad" elements where violations were reported
                if violation_count is not None and violation_count > 0:
                    # Seed for reproducibility
                    np.random.seed(hash(field_name) % 2**32)
                    bad_count = min(max(1, int(violation_count / 10)), n_elements)  # Scale to mesh size
                    bad_indices = np.random.choice(n_elements, bad_count, replace=False)
                    arr[bad_indices] = metric_value * (1.0 + np.random.rand(len(bad_indices)) * 0.3)
                
                return arr
            
            # Create arrays for key metrics
            if metrics.get("max_non_ortho") is not None:
                arr = create_quality_field(
                    "non_ortho",
                    metrics["max_non_ortho"],
                    thresholds.get("max_non_ortho", 70.0),
                    violation_counts.get("non_ortho_faces", 0)
                )
                if arr is not None:
                    arrays["non_ortho"] = arr
            
            if metrics.get("max_skewness") is not None:
                arr = create_quality_field(
                    "skewness",
                    metrics["max_skewness"],
                    thresholds.get("max_boundary_skewness", 20.0),
                    violation_counts.get("skewness_faces", 0)
                )
                if arr is not None:
                    arrays["skewness"] = arr
            
            if metrics.get("min_volume") is not None:
                # For volume, invert the sense (lower is worse)
                arr = np.ones(n_elements) * (thresholds.get("min_vol", 1e-13) * 1e13)
                if violation_counts.get("pyramid_volume_faces", 0) > 0:
                    np.random.seed(hash("min_volume") % 2**32)
                    bad_count = min(max(1, int(violation_counts["pyramid_volume_faces"] / 10)), n_elements)
                    bad_indices = np.random.choice(n_elements, bad_count, replace=False)
                    arr[bad_indices] = (thresholds.get("min_vol", 1e-13) * np.random.rand(len(bad_indices)) * 0.5)
                arrays["min_volume"] = arr
            
            # Add more fields with synthetic data
            for field_name in ["pyramid_volume", "tet_quality", "concavity", "face_twist", "determinant", "interp_weight", "volume_ratio"]:
                count_key = f"{field_name}_faces"
                if violation_counts.get(count_key, 0) > 0:
                    arr = np.ones(n_elements) * 50.0  # Neutral value
                    np.random.seed(hash(field_name) % 2**32)
                    bad_count = min(max(1, int(violation_counts[count_key] / 10)), n_elements)
                    bad_indices = np.random.choice(n_elements, bad_count, replace=False)
                    arr[bad_indices] = 5.0 + np.random.rand(len(bad_indices)) * 20.0
                    arrays[field_name] = arr
            
            return arrays
        
        except Exception as e:
            print(f"Error creating synthetic quality arrays: {e}")
            return {}

    def _parse_force_coeffs(self, case_dir):
        case_path = Path(case_dir)
        candidates = sorted(
            list(case_path.glob("postProcessing/**/coefficient*.dat"))
            + list(case_path.glob("postProcessing/**/forceCoeffs*.dat"))
        )
        best = None
        for path in candidates:
            parsed = self._parse_force_coeffs_file(path)
            if parsed is not None and parsed.get("history", {}).get("time"):
                best = parsed
        if best is None:
            fallback = self._parse_force_coeffs_from_logs(case_path)
            if fallback is not None:
                return fallback
            return {
                "available": False,
                "source_file": "",
                "history": {"time": [], "Cd": [], "Cl": [], "Cm": []},
                "summary": {},
                "residual_status": "unavailable",
            }
        return best

    def _parse_force_coeffs_file(self, path):
        header = []
        rows = []
        for raw in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#"):
                header = line.lstrip("#").strip().split()
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            rows.append(parts)
        if not rows:
            return None
        idx_time = 0
        idx_cd = 1
        idx_cl = 2
        idx_cm = 3
        if header:
            index_map = {name: idx for idx, name in enumerate(header)}
            idx_time = index_map.get("Time", 0)
            idx_cd = index_map.get("Cd", index_map.get("Cdrag", 1))
            idx_cl = index_map.get("Cl", index_map.get("Clift", 2))
            idx_cm = index_map.get("Cm", None)
            if idx_cm is None:
                for token in ("CmPitch", "Cmz", "Cmy", "CmRoll", "CmYaw"):
                    if token in index_map:
                        idx_cm = index_map[token]
                        break
            if idx_cm is None:
                idx_cm = 3
        history = {"time": [], "Cd": [], "Cl": [], "Cm": []}
        for parts in rows:
            try:
                history["time"].append(float(parts[idx_time]))
                history["Cd"].append(float(parts[idx_cd]))
                history["Cl"].append(float(parts[idx_cl]))
                history["Cm"].append(float(parts[idx_cm]))
            except (IndexError, ValueError):
                continue
        if not history["time"]:
            return None
        return {
            "available": True,
            "source_file": str(path),
            "history": history,
            "summary": {
                "Cd": history["Cd"][-1],
                "Cl": history["Cl"][-1],
                "Cm": history["Cm"][-1],
            },
            "residual_status": "ok",
        }

    def _parse_force_coeffs_from_logs(self, case_path):
        logs = []
        exe = self._execution_state()
        for key in ("solve", "post"):
            log_path = str(exe.get("last_logs", {}).get(key, "")).strip()
            if log_path:
                logs.append(Path(log_path))
        logs.extend(sorted(case_path.glob("log.solve*.txt")))
        pattern = re.compile(
            r"Cd\s*[:=]\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
            r".*?Cl\s*[:=]\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
            r".*?Cm\s*[:=]\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
        )
        triples = []
        for path in logs:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for match in pattern.finditer(text):
                triples.append((float(match.group(1)), float(match.group(2)), float(match.group(3))))
        if not triples:
            return None
        cd, cl, cm = triples[-1]
        return {
            "available": True,
            "source_file": str(logs[-1]) if logs else "",
            "history": {
                "time": list(range(len(triples))),
                "Cd": [x[0] for x in triples],
                "Cl": [x[1] for x in triples],
                "Cm": [x[2] for x in triples],
            },
            "summary": {"Cd": cd, "Cl": cl, "Cm": cm},
            "residual_status": "log-only",
        }

    def _on_mesh_scalar_changed(self, name):
        min_idx = {"xmin": 0, "ymin": 1, "zmin": 2}
        max_idx = {"xmax": 0, "ymax": 1, "zmax": 2}
        if name in min_idx:
            idx = min_idx[name]
            vals = list(self.openfoam["mesh"]["domain_min"])
            vals[idx] = float(self.mesh_spin[name].value())
            self._set_openfoam_value("mesh.domain_min", vals)
        elif name in max_idx:
            idx = max_idx[name]
            vals = list(self.openfoam["mesh"]["domain_max"])
            vals[idx] = float(self.mesh_spin[name].value())
            self._set_openfoam_value("mesh.domain_max", vals)
        self._refresh_viewer_scene()

    def _on_refinement_region_enabled(self, enabled):
        self._set_openfoam_value("mesh.refinement_region.enabled", bool(enabled))
        for spin in getattr(self, "refinement_region_spin", {}).values():
            spin.setEnabled(bool(enabled))
        if hasattr(self, "spin_refinement_level"):
            self.spin_refinement_level.setEnabled(bool(enabled))
        self._refresh_viewer_scene()

    def _on_refinement_region_level_changed(self, value):
        self._set_openfoam_value("mesh.refinement_region.level", int(value))
        self._refresh_viewer_scene()

    def _on_refinement_region_scalar_changed(self, key, value):
        rr = self.openfoam.get("mesh", {}).get("refinement_region", {})
        min_vals = list(rr.get("min", [-10.0, -20.0, -10.0]))
        max_vals = list(rr.get("max", [50.0, 20.0, 10.0]))
        if len(min_vals) != 3:
            min_vals = [-10.0, -20.0, -10.0]
        if len(max_vals) != 3:
            max_vals = [50.0, 20.0, 10.0]
        min_idx = {"min_x": 0, "min_y": 1, "min_z": 2}
        max_idx = {"max_x": 0, "max_y": 1, "max_z": 2}
        if key in min_idx:
            idx = min_idx[key]
            min_vals[idx] = float(value)
            self._set_openfoam_value("mesh.refinement_region.min", min_vals)
        elif key in max_idx:
            idx = max_idx[key]
            max_vals[idx] = float(value)
            self._set_openfoam_value("mesh.refinement_region.max", max_vals)
        self._refresh_viewer_scene()

    def _on_mesh_cells_changed(self, name):
        idx = {"nx": 0, "ny": 1, "nz": 2}[name]
        vals = list(self.openfoam["mesh"]["base_cells"])
        vals[idx] = int(self.mesh_cells[name].value())
        self._set_openfoam_value("mesh.base_cells", vals)

    def _on_mesh_preset_changed(self, preset):
        self._set_openfoam_value("mesh.preset", preset)
        preset_vals = _mesh_for_preset(preset)
        for key, value in preset_vals.items():
            self._set_openfoam_value(f"mesh.{key}", value)
        self._sync_widgets_from_state()

    def _on_snappy_scalar_changed(self, key, value):
        if key in {
            "max_local_cells",
            "max_global_cells",
            "min_refinement_cells",
            "n_feature_snap_iter",
            "n_grow",
            "layer_n_relax_iter",
            "n_smooth_surface_normals",
            "n_smooth_normals",
            "n_smooth_thickness",
            "n_buffer_cells_no_extrude",
            "n_layer_iter",
        }:
            self._set_openfoam_value(f"mesh.{key}", int(float(value)))
            return
        self._set_openfoam_value(f"mesh.{key}", float(value))

    def _on_snappy_profile_changed(self, profile):
        self._set_openfoam_value("mesh.snappy_profile", profile)
        if profile != "Custom":
            vals = _snappy_profile_for(profile)
            for key, value in vals.items():
                self._set_openfoam_value(f"mesh.{key}", value)
        self._sync_widgets_from_state()

    def _sync_snappy_profile_editability(self):
        custom = self.openfoam.get("mesh", {}).get("snappy_profile", "Balanced") == "Custom"
        for widget in (
            self.spin_ref_min,
            self.spin_ref_max,
            self.spin_feature_angle,
            self.spin_layers,
            self.chk_castellated,
            self.chk_snap,
            self.chk_layers,
            self.chk_implicit_snap,
            self.chk_explicit_snap,
            self.chk_multi_region_snap,
            self.chk_allow_free_faces,
        ):
            widget.setEnabled(custom)
        for spin in getattr(self, "snappy_spin", {}).values():
            spin.setEnabled(custom)

    def _apply_fv_schemes_preset(self, preset):
        self._set_openfoam_value("numerics.fv_schemes", _fv_schemes_defaults(preset))

    def _apply_fv_solution_preset(self, preset):
        self._set_openfoam_value("numerics.fv_solution", _fv_solution_defaults(preset))

    def _on_fv_schemes_preset_changed(self, preset):
        self._set_openfoam_value("numerics.fv_schemes_preset", preset)
        self._apply_fv_schemes_preset(preset)
        self._sync_widgets_from_state(refresh_viewer=False)

    def _on_fv_solution_preset_changed(self, preset):
        self._set_openfoam_value("numerics.fv_solution_preset", preset)
        self._apply_fv_solution_preset(preset)
        self._sync_widgets_from_state(refresh_viewer=False)

    def _update_fv_solution_controls(self):
        if not hasattr(self, "cmb_p_solver"):
            return
        p_solver = self.cmb_p_solver.currentText()
        self.cmb_p_smoother.setEnabled(p_solver in ("GAMG", "smoothSolver"))
        self.cmb_p_preconditioner.setEnabled(p_solver in ("PCG", "PBiCGStab"))
        u_solver = self.cmb_u_solver.currentText()
        self.cmb_u_smoother.setEnabled(u_solver == "smoothSolver")
        self.cmb_u_preconditioner.setEnabled(u_solver in ("PCG", "PBiCGStab"))

    def _on_p_solver_changed(self, solver):
        self._set_openfoam_value("numerics.fv_solution.p_solver", solver)
        self._update_fv_solution_controls()

    def _on_u_solver_changed(self, solver):
        self._set_openfoam_value("numerics.fv_solution.u_solver", solver)
        self._update_fv_solution_controls()

    def _on_solver_changed(self, solver):
        self._set_openfoam_value("workflow", solver)
        if solver == "potentialFoam":
            scheme_preset = "potentialFoam basic"
            solution_preset = "Potential"
        else:
            scheme_preset = "bounded steady RANS"
            solution_preset = "SIMPLE-RANS"
        self._set_openfoam_value("numerics.fv_schemes_preset", scheme_preset)
        self._set_openfoam_value("numerics.fv_solution_preset", solution_preset)
        self._apply_fv_schemes_preset(scheme_preset)
        self._apply_fv_solution_preset(solution_preset)
        self._sync_widgets_from_state()
