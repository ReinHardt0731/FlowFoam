from ._controller_common import *

def viewer_actions():
    return ["set_standard_view", "set_background_theme", "set_lighting_profile", "set_tripod_visible"]


class ViewerMixin:
    def _refresh_viewer_scene(self):
        if self._viewer_scalar_field and self._result_source_mesh() is not None:
            self._render_viewer_scene()
            return
        key = self._current_field_key()
        if self.current_data is not None and key:
            self._render_viewer_scene(self.current_data, key)
            return
        self._render_viewer_scene()

    def _vtk_focus_kind(self):
        if (
            len(self._selected_path) >= 3
            and self._selected_path[0] == "CFD Pipeline"
            and self._selected_path[1] == "Post Process"
        ):
            node = str(self._selected_path[2]).strip().lower()
            if node.startswith("block"):
                return "blockMesh"
            if node.startswith("snappy"):
                return "snappy"
        return None

    def _ensure_viewer(self):
        if self.viewer_plotter is not None:
            return
        viewer_host = getattr(self.ui, "viewer_host", None)
        if viewer_host is not None:
            host_layout = viewer_host.layout()
            if host_layout is None:
                host_layout = QVBoxLayout(viewer_host)
                host_layout.setContentsMargins(0, 0, 0, 0)
            self.viewer_plotter = QtInteractor(viewer_host)
            host_layout.addWidget(self.viewer_plotter)
        else:
            if hasattr(self.ui, "mdiArea_2") and self.ui.mdiArea_2 is not None:
                try:
                    self.ui.gridLayout_4.removeWidget(self.ui.mdiArea_2)
                except Exception:
                    pass
                self.ui.mdiArea_2.setVisible(False)
                self.ui.mdiArea_2.setParent(None)
            self.viewer_plotter = QtInteractor(self.ui.aerodynamics_tab)
            self.ui.gridLayout_4.addWidget(self.viewer_plotter, 1, 0, 1, 1)
            self.ui.gridLayout_4.setRowStretch(1, 1)
        self._apply_viewer_background()

    def set_tripod_visible(self, visible):
        self._tripod_visible = bool(visible)
        if hasattr(self, "chk_show_tripod"):
            blocked = self.chk_show_tripod.blockSignals(True)
            self.chk_show_tripod.setChecked(self._tripod_visible)
            self.chk_show_tripod.blockSignals(blocked)
        if hasattr(self.ui, "btn_ribbon_toggle_tripod"):
            blocked = self.ui.btn_ribbon_toggle_tripod.blockSignals(True)
            self.ui.btn_ribbon_toggle_tripod.setChecked(self._tripod_visible)
            self.ui.btn_ribbon_toggle_tripod.blockSignals(blocked)
        self._refresh_viewer_scene()

    def set_standard_view(self, view_name):
        self._ensure_viewer()
        if self.viewer_plotter is None:
            return
        name = str(view_name or "").strip().lower()
        try:
            if name == "top":
                self.viewer_plotter.view_xy()
            elif name == "side":
                self.viewer_plotter.view_xz()
            elif name == "front":
                self.viewer_plotter.view_yz()
            else:
                self.viewer_plotter.view_isometric()
            self.viewer_plotter.render()
        except Exception:
            pass

    def reset_viewer_camera(self):
        self._ensure_viewer()
        if self.viewer_plotter is None:
            return
        try:
            self.viewer_plotter.reset_camera()
            self.viewer_plotter.render()
        except Exception:
            pass

    def set_workflow_solver(self, solver):
        self._on_solver_changed(str(solver or "simpleFoam"))
        self._sync_widgets_from_state(refresh_viewer=False)

    def set_vtk_target(self, kind):
        normalized = self._normalize_vtk_kind(kind)
        label = "snappy" if normalized == "snappy" else "blockMesh"
        for combo_name in ("cmb_vtk_mesh", "cmb_ribbon_vtk_target"):
            combo = getattr(self, combo_name, None) or getattr(self.ui, combo_name, None)
            if combo is None:
                continue
            idx = combo.findText(label)
            blocked = combo.blockSignals(True)
            combo.setCurrentIndex(idx if idx >= 0 else 0)
            combo.blockSignals(blocked)

    def _result_source_mesh(self):
        focus_kind = self._vtk_focus_kind()
        if focus_kind and isinstance(self._vtk_meshes, dict) and focus_kind in self._vtk_meshes:
            return self._vtk_meshes[focus_kind]
        if self._vtk_active_kind and isinstance(self._vtk_meshes, dict) and self._vtk_active_kind in self._vtk_meshes:
            return self._vtk_meshes[self._vtk_active_kind]
        if self._vtk_mesh is not None:
            return self._vtk_mesh
        if isinstance(self._vtk_meshes, dict) and self._vtk_meshes:
            return next(iter(self._vtk_meshes.values()))
        return None

    def available_result_fields(self):
        names = []
        mesh = self._result_source_mesh()
        if mesh is not None:
            try:
                names.extend(str(name) for name in mesh.array_names if str(name).strip())
            except Exception:
                pass
        if self.current_data is not None:
            labels = self.current_data.get("field_labels", {})
            for key in self.current_data.get("fields", {}).keys():
                names.append(str(labels.get(key, key)))
        ordered = []
        seen = set()
        for name in names:
            text = str(name).strip()
            if text and text not in seen:
                seen.add(text)
                ordered.append(text)
        return ordered

    def _mesh_has_vector_field(self, field_name):
        mesh = self._result_source_mesh()
        if mesh is None or not field_name:
            return False
        try:
            arr = mesh[str(field_name)]
            shape = getattr(arr, "shape", ())
            return len(shape) > 1 and int(shape[-1]) in (2, 3)
        except Exception:
            return False

    def _match_result_field(self, tokens, require_vector=False):
        for name in self.available_result_fields():
            text = str(name).strip()
            lowered = text.lower()
            if any(lowered == token or lowered.startswith(token) or token in lowered for token in tokens):
                if require_vector and not self._mesh_has_vector_field(text):
                    continue
                return text
        return ""

    def set_viewer_scalar_field(self, field_name):
        self._viewer_scalar_field = str(field_name or "").strip()
        self._sync_widgets_from_state(refresh_viewer=False)
        self._refresh_viewer_scene()

    def apply_result_preset(self, preset):
        name = str(preset or "").strip().lower()
        if name == "pressure":
            field = self._match_result_field(("pressure", " p", "p"), require_vector=False)
        elif name == "velocity":
            field = self._match_result_field(("velocity", "u", "vel"), require_vector=True)
            if not field:
                field = self._match_result_field(("velocity", "u", "vel"), require_vector=False)
        else:
            field = ""
        if not field:
            QMessageBox.information(self._dialog_parent(), "Results", "No matching result field is loaded yet.")
            return
        self.set_viewer_scalar_field(field)

    def set_viewer_render_mode(self, mode):
        value = str(mode or "surface").strip().lower()
        if value not in {"surface", "wireframe"}:
            value = "surface"
        self._viewer_render_mode = value
        self._sync_widgets_from_state(refresh_viewer=False)
        self._refresh_viewer_scene()

    def toggle_viewer_contours(self, enabled):
        self._viewer_contours_enabled = bool(enabled)
        self._sync_widgets_from_state(refresh_viewer=False)
        self._refresh_viewer_scene()

    def toggle_viewer_slice(self, enabled):
        self._viewer_slice_enabled = bool(enabled)
        self._sync_widgets_from_state(refresh_viewer=False)
        self._refresh_viewer_scene()

    def toggle_viewer_streamlines(self, enabled):
        self._viewer_streamlines_enabled = bool(enabled)
        self._sync_widgets_from_state(refresh_viewer=False)
        self._refresh_viewer_scene()

    def capture_viewer_screenshot(self):
        self._ensure_viewer()
        if self.viewer_plotter is None:
            return
        start_path = self._execution_case_dir() / "viewer.png"
        file_path, _ = QFileDialog.getSaveFileName(
            self._dialog_parent(),
            "Save Viewer Screenshot",
            str(start_path),
            "PNG (*.png);;JPEG (*.jpg *.jpeg)",
        )
        if not file_path:
            return
        self.viewer_plotter.screenshot(file_path)

    def set_background_theme(self, theme):
        val = str(theme or "gradient_dark").strip().lower()
        if val not in ("gradient_sky", "gradient_studio", "gradient_sunset", "gradient_dark", "solid_light"):
            val = "gradient_dark"
        self._background_theme = val
        self._apply_viewer_background()
        if getattr(self, "_task_controls_visible", False):
            try:
                self.viewer_plotter.render()
            except Exception:
                pass

    def set_lighting_profile(self, profile):
        val = str(profile or "balanced").strip().lower()
        if val not in ("balanced", "soft", "contrast"):
            val = "balanced"
        self._lighting_profile = val
        if getattr(self, "_task_controls_visible", False):
            self._refresh_viewer_scene()

    def set_mesh_render_mode(self, mode_text):
        """Set mesh render mode from preference (Smooth, Mesh, or Smooth + Mesh)."""
        mode_map = {
            "Smooth": "smooth",
            "Mesh": "mesh",
            "Smooth + Mesh": "smooth+mesh",
        }
        mode = mode_map.get(str(mode_text or "Smooth").strip(), "smooth")
        self._set_mesh_quality_render_mode(mode)

    def set_mesh_opacity(self, opacity_text):
        """Set mesh opacity from preference (High or Low)."""
        opacity_map = {
            "High": "high",
            "Low": "low",
        }
        opacity = opacity_map.get(str(opacity_text or "High").strip(), "high")
        self._set_mesh_quality_opacity(opacity)

    def _apply_viewer_background(self):
        if self.viewer_plotter is None:
            return
        palette = {
            "gradient_sky": ("#e9f3ff", "#f9fcff"),
            "gradient_studio": ("#dde3ec", "#f4f6f9"),
            "gradient_sunset": ("#ffd8be", "#fff0e4"),
            "gradient_dark": ("#12161f", "#2a3344"),
            "solid_light": ("#f6f8fb", None),
        }
        bottom, top = palette.get(self._background_theme, palette["gradient_dark"])
        try:
            if top:
                self.viewer_plotter.set_background(bottom, top=top)
            else:
                self.viewer_plotter.set_background(bottom)
        except TypeError:
            if top:
                self.viewer_plotter.set_background(bottom, top)
            else:
                self.viewer_plotter.set_background(bottom)
        except Exception:
            pass

    def _viewer_lighting_kwargs(self):
        profiles = {
            "balanced": {"ambient": 0.22, "diffuse": 0.72, "specular": 0.20, "specular_power": 14.0},
            "soft": {"ambient": 0.34, "diffuse": 0.58, "specular": 0.10, "specular_power": 8.0},
            "contrast": {"ambient": 0.10, "diffuse": 0.88, "specular": 0.32, "specular_power": 22.0},
        }
        return profiles.get(self._lighting_profile, profiles["balanced"])

    def _load_cfd_surface_mesh(self):
        geo = self.openfoam.get("geometry", {})
        path = str(geo.get("stl_path", "")).strip()
        scale = float(geo.get("scale", 1.0))
        if not path or not Path(path).is_file():
            self._cfd_surface_cache_path = ""
            self._cfd_surface_cache_scale = None
            self._cfd_surface_mesh = None
            return None
        if (
            self._cfd_surface_mesh is not None
            and path == self._cfd_surface_cache_path
            and scale == self._cfd_surface_cache_scale
        ):
            return self._cfd_surface_mesh
        try:
            mesh = pv.read(path)
            if abs(scale - 1.0) > 1.0e-12:
                mesh = mesh.copy(deep=True)
                mesh.points *= scale
            self._cfd_surface_cache_path = path
            self._cfd_surface_cache_scale = scale
            self._cfd_surface_mesh = mesh
            return mesh
        except Exception:
            self._cfd_surface_cache_path = ""
            self._cfd_surface_cache_scale = None
            self._cfd_surface_mesh = None
            return None

    def _toggle_mesh_quality_visualization(self, enabled=None):
        """Toggle mesh quality visualization on/off."""
        if enabled is None:
            self._mesh_quality_visibility = not self._mesh_quality_visibility
        else:
            self._mesh_quality_visibility = bool(enabled)
        self._update_mesh_quality_visualization()

    def _set_mesh_quality_field(self, field_name):
        """Switch to a different mesh quality metric."""
        self._mesh_quality_field = str(field_name or "non_ortho").strip()
        if self._mesh_quality_visibility:
            self._update_mesh_quality_visualization()

    def _set_mesh_quality_mode(self, mode):
        """Switch between 'gradient' and 'isolated' visualization modes."""
        valid_modes = {"gradient", "isolated"}
        mode_str = str(mode or "gradient").strip().lower()
        if mode_str not in valid_modes:
            mode_str = "gradient"
        self._mesh_quality_mode = mode_str
        if self._mesh_quality_visibility:
            self._update_mesh_quality_visualization()

    def _set_mesh_quality_severity(self, factor):
        """Set severity threshold multiplier (0.5-2.0) for filtering."""
        try:
            severity = float(factor)
            severity = max(0.5, min(2.0, severity))
            self._mesh_quality_severity = severity
            if self._mesh_quality_visibility and self._mesh_quality_mode == "isolated":
                self._update_mesh_quality_visualization()
        except (ValueError, TypeError):
            pass

    def _set_mesh_quality_render_mode(self, mode):
        """Set render mode: 'smooth', 'mesh', or 'smooth+mesh'."""
        valid_modes = {"smooth", "mesh", "smooth+mesh"}
        mode_str = str(mode or "smooth").strip().lower()
        if mode_str not in valid_modes:
            mode_str = "smooth"
        self._mesh_quality_render_mode = mode_str
        if self._mesh_quality_visibility:
            self._update_mesh_quality_visualization()
            if self.viewer_plotter is not None:
                try:
                    self.viewer_plotter.render()
                except Exception:
                    pass

    def _set_mesh_quality_opacity(self, opacity):
        """Set opacity level: 'high' or 'low'."""
        valid_opacities = {"high", "low"}
        opacity_str = str(opacity or "high").strip().lower()
        if opacity_str not in valid_opacities:
            opacity_str = "high"
        self._mesh_quality_opacity = opacity_str
        if self._mesh_quality_visibility:
            self._update_mesh_quality_visualization()
            if self.viewer_plotter is not None:
                try:
                    self.viewer_plotter.render()
                except Exception:
                    pass

    def _update_mesh_quality_visualization(self):
        """Main method to render mesh quality visualization in the viewer."""
        self._ensure_viewer()
        
        # Remove any previously added quality mesh and edges
        if hasattr(self, "_quality_mesh_actor") and self._quality_mesh_actor is not None:
            try:
                self.viewer_plotter.remove_actor(self._quality_mesh_actor)
            except Exception:
                pass
            self._quality_mesh_actor = None
        
        if hasattr(self, "_quality_edges_actor") and self._quality_edges_actor is not None:
            try:
                self.viewer_plotter.remove_actor(self._quality_edges_actor)
            except Exception:
                pass
            self._quality_edges_actor = None
        
        # If visibility is off, we're done
        if not self._mesh_quality_visibility:
            return
        
        # Load quality data if not already cached
        if self._mesh_quality_data is None:
            case_dir = self._execution_case_dir()
            self._mesh_quality_data = self._load_mesh_quality_data(case_dir)
        
        if self._mesh_quality_data is None:
            self._append_run_log("[warn] Mesh quality data not available. Run checkMesh -writeMeshQuality first.")
            self._mesh_quality_visibility = False
            return
        
        mesh = self._mesh_quality_data.get("mesh")
        arrays = self._mesh_quality_data.get("arrays", {})
        thresholds = self._mesh_quality_data.get("thresholds", {})
        
        if mesh is None or len(arrays) == 0:
            self._append_run_log("[warn] No quality arrays found in mesh quality data.")
            return
        
        # Get the active field
        field_name = self._mesh_quality_field
        if field_name not in arrays:
            # Try to find a close match or use first available
            if "non_ortho" in arrays:
                field_name = "non_ortho"
            elif len(arrays) > 0:
                field_name = list(arrays.keys())[0]
            else:
                self._append_run_log("[warn] No suitable quality field found to visualize.")
                return
        
        field_array = arrays.get(field_name)
        if field_array is None or len(field_array) == 0:
            self._append_run_log(f"[warn] Quality field '{field_name}' is empty or invalid.")
            return
        
        # Get threshold for this field
        threshold = thresholds.get(field_name, None)
        
        try:
            # Create a copy to avoid modifying original data
            display_mesh = mesh.copy(deep=False)
            
            if self._mesh_quality_mode == "gradient":
                # Gradient mode: color entire mesh by field values
                self._render_quality_gradient(display_mesh, field_array, field_name, threshold)
            
            elif self._mesh_quality_mode == "isolated":
                # Isolated mode: show only cells exceeding threshold
                self._render_quality_isolated(display_mesh, field_array, field_name, threshold)
            
            self._append_run_log(f"[info] Mesh quality visualization loaded: {field_name} ({self._mesh_quality_mode} mode)")
        
        except Exception as e:
            self._append_run_log(f"[error] Mesh quality visualization failed: {str(e)}")
            print(f"Error rendering mesh quality: {e}")

    def _render_quality_gradient(self, mesh, field_array, field_name, threshold):
        """Render mesh surfaces colored by quality metric (gradient mode)."""
        try:
            # Extract surface only (no volume)
            if hasattr(mesh, 'extract_surface'):
                surface_mesh = mesh.extract_surface(algorithm='dataset_surface')
            else:
                surface_mesh = mesh
            
            # Assign scalar data to mesh
            surface_mesh["quality"] = field_array[:surface_mesh.n_cells] if len(field_array) >= surface_mesh.n_cells else field_array
            surface_mesh.set_active_scalars("quality")
            
            # CFD-optimized colormap: blue (good) to red (bad)
            cmap = "RdYlGn_r"  # Red-Yellow-Green reversed (red=bad, green=good)
            
            # Determine opacity values based on preference
            opacity_high = 1.0
            opacity_low = 0.3
            current_opacity = opacity_high if self._mesh_quality_opacity == "high" else opacity_low
            
            # Determine rendering style
            show_edges_smooth = self._mesh_quality_render_mode in ("smooth+mesh",)
            style_smooth = "surface"
            
            # Add smooth shaded mesh first
            self._quality_mesh_actor = self.viewer_plotter.add_mesh(
                surface_mesh,
                scalars="quality",
                cmap=cmap,
                show_edges=show_edges_smooth,
                edge_color="darkgray",
                line_width=0.5,
                show_scalar_bar=True,
                scalar_bar_args={
                    "title": field_name.replace("_", " ").title(),
                    "position_x": 0.15,
                    "position_y": 0.05,
                    "width": 0.7,
                    "height": 0.1,
                },
                style=style_smooth,
                opacity=current_opacity if self._mesh_quality_render_mode != "mesh" else 1.0,
            )
            
            # Add mesh (wireframe) if requested
            if self._mesh_quality_render_mode in ("mesh", "smooth+mesh"):
                mesh_opacity = 1.0 if self._mesh_quality_render_mode == "mesh" else (opacity_low if self._mesh_quality_opacity == "low" else 0.5)
                self._quality_edges_actor = self.viewer_plotter.add_mesh(
                    surface_mesh,
                    style="wireframe",
                    color="white" if self._mesh_quality_render_mode == "mesh" else "black",
                    line_width=1.0 if self._mesh_quality_render_mode == "mesh" else 0.5,
                    opacity=mesh_opacity,
                )
        
        except Exception as e:
            print(f"Error rendering quality gradient: {e}")

    def _render_quality_isolated(self, mesh, field_array, field_name, threshold):
        """Render only surfaces exceeding threshold (isolated mode)."""
        if threshold is None or field_array is None:
            # Fallback: show all surfaces
            self._render_quality_gradient(mesh, field_array, field_name, threshold)
            return
        
        try:
            # Apply severity multiplier
            effective_threshold = float(threshold) * float(self._mesh_quality_severity)
            
            # Create masks for cells above and below threshold (on full mesh, not surface)
            bad_mask = field_array > effective_threshold
            
            # Extract bad cells from FULL MESH (before surface extraction)
            if bad_mask.sum() > 0:
                # Extract bad cells from full mesh
                bad_mesh_full = mesh.extract_cells(bad_mask)
                
                # Now extract surfaces from the bad mesh
                if hasattr(bad_mesh_full, 'extract_surface'):
                    bad_mesh = bad_mesh_full.extract_surface(algorithm='dataset_surface')
                else:
                    bad_mesh = bad_mesh_full
                
                # Determine opacity values based on preference
                opacity_high = 0.9
                opacity_low = 0.6
                current_opacity = opacity_high if self._mesh_quality_opacity == "high" else opacity_low
                
                # Add bad cells in red with edges for visibility
                show_edges_red = self._mesh_quality_render_mode in ("smooth+mesh", "mesh")
                self._quality_mesh_actor = self.viewer_plotter.add_mesh(
                    bad_mesh,
                    color="red",
                    opacity=current_opacity,
                    show_edges=show_edges_red,
                    edge_color="darkred",
                    line_width=1.5,
                )
                
                # Add mesh (wireframe) if requested
                if self._mesh_quality_render_mode in ("mesh", "smooth+mesh"):
                    mesh_opacity = 1.0 if self._mesh_quality_render_mode == "mesh" else 0.4
                    self._quality_edges_actor = self.viewer_plotter.add_mesh(
                        bad_mesh,
                        style="wireframe",
                        color="black",
                        line_width=1.0,
                        opacity=mesh_opacity,
                    )
                
                # Add good cells in light gray with transparency for context
                good_mask = ~bad_mask
                if good_mask.sum() > 0:
                    good_mesh_full = mesh.extract_cells(good_mask)
                    
                    # Extract surfaces from good mesh
                    if hasattr(good_mesh_full, 'extract_surface'):
                        good_mesh = good_mesh_full.extract_surface(algorithm='dataset_surface')
                    else:
                        good_mesh = good_mesh_full
                    
                    self.viewer_plotter.add_mesh(
                        good_mesh,
                        color="lightgray",
                        opacity=0.03,
                        show_edges=False,
                    )
                
                bad_count = bad_mask.sum()
                total_count = len(bad_mask)
                self._append_run_log(
                    f"[info] {field_name}: {bad_count}/{total_count} cells exceed threshold "
                    f"({effective_threshold:.4f}x severity)"
                )
            else:
                # No violations
                self._append_run_log(f"[info] {field_name}: All cells pass threshold")
        
        except Exception as e:
            print(f"Error rendering isolated quality mesh: {e}")
            # Fallback to gradient mode
            self._render_quality_gradient(mesh, field_array, field_name, threshold)

    def _render_viewer_scene(self, data_dict=None, field_key=None):
        self._ensure_viewer()
        if self.viewer_plotter is None:
            return
        self.viewer_plotter.clear()
        self._apply_viewer_background()
        self.viewer_plotter.add_axes()
        style = self._viewer_lighting_kwargs()

        dmin = self.openfoam["mesh"]["domain_min"]
        dmax = self.openfoam["mesh"]["domain_max"]
        if all(float(dmin[i]) < float(dmax[i]) for i in range(3)):
            bounds = (
                float(dmin[0]),
                float(dmax[0]),
                float(dmin[1]),
                float(dmax[1]),
                float(dmin[2]),
                float(dmax[2]),
            )
            domain = pv.Box(bounds=bounds)
            self.viewer_plotter.add_mesh(domain, style="wireframe", color="#ff8c00", line_width=2, **style)
            self.viewer_plotter.add_mesh(domain, color="#ff8c00", opacity=0.06, **style)

        rr = self.openfoam.get("mesh", {}).get("refinement_region", {})
        if rr.get("enabled", False):
            try:
                rr_min = rr.get("min", [])
                rr_max = rr.get("max", [])
                if (
                    isinstance(rr_min, (list, tuple))
                    and isinstance(rr_max, (list, tuple))
                    and len(rr_min) == 3
                    and len(rr_max) == 3
                    and all(float(rr_min[i]) < float(rr_max[i]) for i in range(3))
                ):
                    rr_bounds = (
                        float(rr_min[0]),
                        float(rr_max[0]),
                        float(rr_min[1]),
                        float(rr_max[1]),
                        float(rr_min[2]),
                        float(rr_max[2]),
                    )
                    region = pv.Box(bounds=rr_bounds)
                    self.viewer_plotter.add_mesh(region, style="wireframe", color="#00bcd4", line_width=2, **style)
                    self.viewer_plotter.add_mesh(region, color="#00bcd4", opacity=0.08, **style)
            except Exception:
                pass

        surface = self._load_cfd_surface_mesh()
        if surface is not None:
            self.viewer_plotter.add_mesh(surface, color="lightgray", opacity=0.55, show_edges=False, **style)
        vtk_meshes = dict(self._vtk_meshes) if isinstance(self._vtk_meshes, dict) else {}
        if not vtk_meshes and self._vtk_mesh is not None:
            kind = self._vtk_active_kind or "blockMesh"
            vtk_meshes[kind] = self._vtk_mesh
        if vtk_meshes:
            focus_kind = self._vtk_focus_kind()
            missing_focus = None
            if focus_kind and focus_kind not in vtk_meshes:
                missing_focus = focus_kind
                focus_kind = None
            palette = {
                "blockMesh": {"color": "#ffb347", "edge": "#ffcb8a"},
                "snappy": {"color": "#4aa3ff", "edge": "#8ac1ff"},
            }
            active_scalar = str(self._viewer_scalar_field or "").strip()
            stream_vector = active_scalar if self._mesh_has_vector_field(active_scalar) else self._match_result_field(("velocity", "u", "vel"), require_vector=True)
            scalar_bar_added = False
            for kind, mesh in vtk_meshes.items():
                cfg = palette.get(kind, palette["snappy"])
                if focus_kind:
                    active = kind == focus_kind
                    opacity = 0.38 if active else 0.12
                    show_edges = True if active else False
                    line_width = 2 if active else 1
                else:
                    active = True
                    opacity = 0.24
                    show_edges = True
                    line_width = 1
                scalar_field = ""
                try:
                    if active_scalar and active_scalar in getattr(mesh, "array_names", []):
                        scalar_field = active_scalar
                except Exception:
                    scalar_field = ""
                dataset_to_draw = mesh
                if scalar_field and self._viewer_slice_enabled:
                    try:
                        dataset_to_draw = mesh.slice_orthogonal()
                    except Exception:
                        dataset_to_draw = mesh
                mesh_kwargs = dict(style)
                if scalar_field:
                    mesh_kwargs.update(
                        {
                            "scalars": scalar_field,
                            "cmap": "viridis",
                            "show_scalar_bar": (not scalar_bar_added) and active,
                            "scalar_bar_args": {"title": scalar_field},
                        }
                    )
                else:
                    mesh_kwargs["color"] = cfg["color"]
                if self._viewer_render_mode == "wireframe":
                    mesh_kwargs.update(
                        {
                            "style": "wireframe",
                            "show_edges": True,
                            "line_width": 2 if active else 1,
                            "opacity": 0.95 if active else 0.55,
                        }
                    )
                    if not scalar_field:
                        mesh_kwargs["color"] = cfg["edge"]
                else:
                    mesh_kwargs.update(
                        {
                            "opacity": opacity,
                            "show_edges": show_edges,
                            "edge_color": cfg["edge"],
                            "line_width": line_width,
                        }
                    )
                try:
                    self.viewer_plotter.add_mesh(dataset_to_draw, **mesh_kwargs)
                    if scalar_field and mesh_kwargs.get("show_scalar_bar"):
                        scalar_bar_added = True
                except Exception:
                    pass
                if scalar_field and self._viewer_contours_enabled:
                    try:
                        contour = mesh.contour(isosurfaces=10, scalars=scalar_field)
                        if contour is not None and getattr(contour, "n_points", 0) > 0:
                            self.viewer_plotter.add_mesh(
                                contour,
                                scalars=scalar_field,
                                cmap="viridis",
                                line_width=3,
                                show_scalar_bar=not scalar_bar_added,
                                scalar_bar_args={"title": f"{scalar_field} contours"},
                                **style,
                            )
                            scalar_bar_added = True
                    except Exception:
                        pass
                if stream_vector and self._viewer_streamlines_enabled and active:
                    try:
                        bounds = mesh.bounds
                        span = max(
                            abs(float(bounds[1]) - float(bounds[0])),
                            abs(float(bounds[3]) - float(bounds[2])),
                            abs(float(bounds[5]) - float(bounds[4])),
                            1.0,
                        )
                        stream = mesh.streamlines(
                            vectors=stream_vector,
                            source_radius=0.12 * span,
                            n_points=36,
                            max_time=span,
                        )
                        if stream is not None and getattr(stream, "n_points", 0) > 0:
                            self.viewer_plotter.add_mesh(
                                stream.tube(radius=max(0.002 * span, 1.0e-4)),
                                color="#ffe066",
                                opacity=0.9,
                                **style,
                            )
                    except Exception:
                        pass
            if self._active_panel_key == "Post Process":
                loaded = []
                if "blockMesh" in vtk_meshes:
                    loaded.append("blockMesh")
                if "snappy" in vtk_meshes:
                    loaded.append("snappy")
                if loaded:
                    suffix = f" (focus: {focus_kind})" if focus_kind else ""
                    self.viewer_plotter.add_text(
                        f"VTK: {' + '.join(loaded)}{suffix}",
                        position="upper_left",
                        font_size=10,
                        color="#e6e6e6",
                    )
                if missing_focus:
                    self.viewer_plotter.add_text(
                        f"VTK {missing_focus} not loaded",
                        position="lower_left",
                        font_size=10,
                        color="#ffb347",
                        viewport=True,
                        name="vtk_missing_notice",
                    )

        self._add_selected_patch_overlay(dmin, dmax, surface)

        if self._tripod_visible:
            dx = float(dmax[0]) - float(dmin[0])
            dy = float(dmax[1]) - float(dmin[1])
            dz = float(dmax[2]) - float(dmin[2])
            diag = float(np.sqrt(max(dx * dx + dy * dy + dz * dz, 0.0)))
            length = max(1.0, 0.12 * diag)
            radius = max(0.02, 0.01 * length)
            self.viewer_plotter.add_mesh(pv.Line((0.0, 0.0, 0.0), (length, 0.0, 0.0)), color="red", line_width=4)
            self.viewer_plotter.add_mesh(pv.Line((0.0, 0.0, 0.0), (0.0, length, 0.0)), color="green", line_width=4)
            self.viewer_plotter.add_mesh(pv.Line((0.0, 0.0, 0.0), (0.0, 0.0, length)), color="blue", line_width=4)
            self.viewer_plotter.add_mesh(pv.Sphere(radius=radius, center=(0.0, 0.0, 0.0)), color="white", opacity=0.9)

        self.viewer_mesh = None
        if data_dict is not None and field_key is not None:
            x = data_dict["x"]
            y = data_dict["y"] if data_dict["y"] is not None else np.zeros_like(x)
            z = data_dict["z"] if data_dict["z"] is not None else np.zeros_like(x)
            values = data_dict["fields"][field_key]
            label = data_dict["field_labels"].get(field_key, field_key)
            points = np.column_stack((x, y, z))
            cloud = pv.PolyData(points)
            cloud[field_key] = values
            self.viewer_plotter.add_mesh(
                cloud,
                scalars=field_key,
                cmap="viridis",
                point_size=6,
                render_points_as_spheres=True,
                show_scalar_bar=True,
                scalar_bar_args={"title": label},
                **style,
            )
            self.viewer_mesh = cloud
        self.viewer_plotter.reset_camera()

    def _render_field_plot(self, data_dict, field_key):
        self._render_viewer_scene(data_dict, field_key)
