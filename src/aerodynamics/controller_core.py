from ._controller_common import *
from project_paths import WORKSPACE_CASES_DIR

class AerodynamicsTabCoreMixin:
    def __init__(self, ui, state=None):
        self.ui = ui
        self.state = state if state is not None else {}
        self.state.setdefault("aerodynamics", {})
        self.openfoam = ensure_openfoam_state(self.state["aerodynamics"])

        self.model = None
        self.current_data = None
        self.field_key_map = {}
        self.viewer_subwindow = None
        self.viewer_plotter = None
        self.viewer_mesh = None
        self._tripod_visible = True
        self._background_theme = "gradient_dark"
        self._lighting_profile = "balanced"
        self._cfd_surface_cache_path = ""
        self._cfd_surface_cache_scale = None
        self._cfd_surface_mesh = None
        self._vtk_mesh = None
        self._vtk_meshes = {}
        self._vtk_active_kind = None
        self._selected_path = []
        self._active_panel_key = "Geometry"
        self._highlight_patch = None
        self._of_process = None
        self._of_queue = []
        self._of_current = None
        self._of_log_file = None
        self._of_cancel_requested = False
        self._paraview_process = None
        self.console_output = None
        self._of_run_mode = "stage"
        self._of_requested_stage = ""
        self._conv_dialog = None
        self._conv_canvas = None
        self._conv_fig = None
        self._conv_resid_ax = None
        self._conv_coeff_ax = None
        self._conv_residuals = {}
        self._conv_coeffs = {"x": [], "Cd": [], "Cl": [], "Cm": []}
        self._conv_current_time = None
        self._conv_resid_iter = 0
        self._conv_coeff_iter = 0
        self._conv_log_buffer = ""
        self._conv_last_draw = 0.0
        self._conv_draw_interval = 0.7
        self._conv_pending_redraw = False
        self._conv_redraw_timer = None
        self._last_check_mesh_report = None
        self._viewer_render_mode = "surface"
        self._viewer_scalar_field = ""
        self._viewer_contours_enabled = False
        self._viewer_slice_enabled = False
        self._viewer_streamlines_enabled = False
        # Mesh quality visualization properties
        self._mesh_quality_data = None
        self._mesh_quality_visibility = False
        self._mesh_quality_field = "non_ortho"
        self._mesh_quality_mode = "gradient"  # "gradient" or "isolated"
        self._mesh_quality_severity = 1.0
        self._mesh_quality_render_mode = "smooth"  # "smooth", "mesh", or "smooth+mesh"
        self._mesh_quality_opacity = "high"  # "high" or "low"
        self._quality_mesh_actor = None
        self._quality_edges_actor = None

        self._setup_pressure_options()  # Initializes field_selector for post-process use
        self._setup_openfoam_task_panel()
        self._ensure_viewer()
        self._sync_widgets_from_state(refresh_viewer=False)

    def _setup_pressure_options(self):
        """Initialize pressure field selector for post-process use. Pressure buttons now in post-process panel."""
        if hasattr(self.ui, "cmb_aero_field") and hasattr(self.ui, "btn_refresh_aero_plot"):
            self.field_selector = self.ui.cmb_aero_field
            self.refresh_plot_btn = self.ui.btn_refresh_aero_plot
        else:
            self.field_selector = QComboBox()
            self.refresh_plot_btn = QPushButton("Refresh Plot")
        
        self.field_selector.setEnabled(False)
        self.refresh_plot_btn.setEnabled(False)
        self.field_selector.currentIndexChanged.connect(self._on_field_changed)
        self.refresh_plot_btn.clicked.connect(self._on_refresh_clicked)
        self.field_selector.setVisible(False)
        self.refresh_plot_btn.setVisible(False)
        if hasattr(self.ui, "lbl_aero_field"):
            self.ui.lbl_aero_field.setVisible(False)
        self._task_controls_visible = False

    def _setup_openfoam_task_panel(self):
        if not hasattr(self.ui, "task_task") or self.ui.task_task.layout() is None:
            return
        self.ui.task_task.layout().setAlignment(Qt.AlignTop)
        self.of_task_scroll = QScrollArea(self.ui.task_task)
        self.of_task_scroll.setWidgetResizable(True)
        self.of_task_root = QWidget(self.of_task_scroll)
        root_layout = QVBoxLayout(self.of_task_root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setAlignment(Qt.AlignTop)
        root_layout.setSpacing(8)
        self.panel_title = QLabel("OpenFOAM CFD Setup", self.of_task_root)
        root_layout.addWidget(self.panel_title)
        self.panel_widgets = {}
        self.panel_widgets["CFD Pipeline"] = self._build_case_panel()
        self.panel_widgets["Geometry"] = self._build_geometry_panel()
        self.panel_widgets["Solve Mesh"] = self._build_solve_mesh_panel()
        self.panel_widgets["Domain Mesh"] = self._build_mesh_panel()
        self.panel_widgets["SnappyHexMesh Settings"] = self._build_snappy_panel()
        self.panel_widgets["CheckMesh"] = self._build_checkmesh_panel()
        self.panel_widgets["Boundary Conditions"] = self._build_bc_panel()
        self.panel_widgets["Simulation Control"] = self._build_sim_panel()
        self.panel_widgets["Numerics"] = self._build_numerics_panel()
        self.panel_widgets["Solve"] = self._build_export_panel()
        self.panel_widgets["Post Process"] = self._build_post_process_panel()
        for panel in self.panel_widgets.values():
            root_layout.addWidget(panel)
            panel.setVisible(False)
        root_layout.addStretch(1)
        self.of_task_scroll.setWidget(self.of_task_root)
        self.ui.task_task.layout().addWidget(self.of_task_scroll)
        self.of_task_scroll.setVisible(False)
        self._show_panel("Geometry")

    def get_model(self):
        if self.model is None:
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(["Aerodynamics CFD"])
            
            # Define icons for different node types (using emoji)
            icons = {
                "CFD Pipeline": "🔧",
                "Geometry": "📐",
                "Domain Mesh": "🎯",
                "SnappyHexMesh Settings": "⚙️",
                "CheckMesh": "✓",
                "Solve Mesh": "🔨",
                "Boundary Conditions": "🚪",
                "Simulation Control": "⏱️",
                "Numerics": "🔢",
                "Post Process": "📊",
                "Solve": "▶️",
                "blockMesh": "📦",
                "Surface Feature Mesh": "🔲",
                "SnappyHexMesh": "🌐",
                "Pressure Field": "📈",
                "Velocity Field": "💨",
                "Other Fields": "📋",
            }
            
            root = QStandardItem(f"{icons.get('CFD Pipeline', '')} CFD Pipeline")
            geom = QStandardItem(f"{icons.get('Geometry', '')} Geometry")
            for name in ("Domain Mesh", "SnappyHexMesh Settings", "CheckMesh", "Solve Mesh"):
                geom.appendRow(QStandardItem(f"{icons.get(name, '')} {name}"))
            root.appendRow(geom)
            post = None
            for name in ("Boundary Conditions", "Simulation Control", "Numerics", "Solve", "Post Process"):
                item = QStandardItem(f"{icons.get(name, '')} {name}")
                root.appendRow(item)
                if name == "Post Process":
                    post = item
            for child in ("Pressure Field", "Velocity Field", "Other Fields"):
                if post is not None:
                    post.appendRow(QStandardItem(f"{icons.get(child, '')} {child}"))
            model.appendRow(root)
            self.model = model
        return self.model

    def sync_from_state(self):
        self.openfoam = ensure_openfoam_state(self.state.setdefault("aerodynamics", {}))
        self._sync_widgets_from_state(refresh_viewer=True)

    def set_task_controls_visible(self, visible):
        became_visible = bool(visible) and not bool(getattr(self, "_task_controls_visible", False))
        self._task_controls_visible = bool(visible)
        if hasattr(self, "of_task_scroll") and self.of_task_scroll is not None:
            self.of_task_scroll.setVisible(self._task_controls_visible)
        self._update_pressure_controls_visibility()
        if became_visible:
            self._refresh_viewer_scene()

    def _update_pressure_controls_visibility(self):
        has_fields = hasattr(self, "field_selector") and self.field_selector.count() > 0
        show = bool(getattr(self, "_task_controls_visible", False) and has_fields)
        if hasattr(self, "field_selector"):
            self.field_selector.setVisible(show)
        if hasattr(self, "refresh_plot_btn"):
            self.refresh_plot_btn.setVisible(show)
        if hasattr(self.ui, "lbl_aero_field"):
            self.ui.lbl_aero_field.setVisible(show)

    def on_tree_selection_changed(self, path):
        self._selected_path = path or []
        panel = "Geometry"
        if len(self._selected_path) == 1 and self._selected_path[0] == "CFD Pipeline":
            panel = "CFD Pipeline"
        elif len(self._selected_path) >= 3 and self._selected_path[0] == "CFD Pipeline" and self._selected_path[1] == "Geometry":
            panel = self._selected_path[2]
        elif len(self._selected_path) >= 3 and self._selected_path[0] == "CFD Pipeline" and self._selected_path[1] == "Post Process":
            panel = "Post Process"
            node = str(self._selected_path[2]).strip().lower()
            if hasattr(self, "cmb_vtk_mesh") and node.startswith("snappy"):
                idx = self.cmb_vtk_mesh.findText("snappy")
                if idx >= 0:
                    blocked = self.cmb_vtk_mesh.blockSignals(True)
                    self.cmb_vtk_mesh.setCurrentIndex(idx)
                    self.cmb_vtk_mesh.blockSignals(blocked)
        elif len(self._selected_path) >= 2 and self._selected_path[0] == "CFD Pipeline":
            panel = self._selected_path[1]
        self._show_panel(panel)

    def _show_panel(self, panel_key):
        post_children = {"Pressure Field", "Velocity Field", "Other Fields"}
        if panel_key in post_children:
            panel_key = "Post Process"
        if panel_key not in self.panel_widgets:
            panel_key = "Geometry"
        self._active_panel_key = panel_key
        for key, panel in self.panel_widgets.items():
            panel.setVisible(key == panel_key)

    def show_panel(self, panel_key):
        self._show_panel(panel_key)
        self._sync_widgets_from_state(refresh_viewer=False)

    def collect_property_rows(self, path):
        if not path:
            path = ["CFD Pipeline", self._active_panel_key]
        node = path[2] if len(path) > 2 and path[1] == "Geometry" else (path[1] if len(path) > 1 else "Geometry")
        rows = []
        if node == "Geometry":
            rows.extend(
                [
                    {"label": "STL Path", "value": self.openfoam["geometry"]["stl_path"], "editable": False},
                    {"label": "triSurface Name", "value": self.openfoam["geometry"]["tri_surface_name"], "key": "geometry.tri_surface_name", "editable": True},
                    {"label": "Scale", "value": self.openfoam["geometry"]["scale"], "key": "geometry.scale", "editable": True},
                ]
            )
        elif node == "Domain Mesh":
            m = self.openfoam["mesh"]
            rows.extend(
                [
                    {"label": "Preset", "value": m["preset"], "key": "mesh.preset", "choices": ["External Aerodynamics", "Coarse", "Medium", "Fine"]},
                    {"label": "Domain Min X", "value": m["domain_min"][0], "key": "mesh.domain_min.0", "editable": True},
                    {"label": "Domain Min Y", "value": m["domain_min"][1], "key": "mesh.domain_min.1", "editable": True},
                    {"label": "Domain Min Z", "value": m["domain_min"][2], "key": "mesh.domain_min.2", "editable": True},
                    {"label": "Domain Max X", "value": m["domain_max"][0], "key": "mesh.domain_max.0", "editable": True},
                    {"label": "Domain Max Y", "value": m["domain_max"][1], "key": "mesh.domain_max.1", "editable": True},
                    {"label": "Domain Max Z", "value": m["domain_max"][2], "key": "mesh.domain_max.2", "editable": True},
                    {"label": "Cells Nx", "value": m["base_cells"][0], "key": "mesh.base_cells.0", "editable": True},
                    {"label": "Cells Ny", "value": m["base_cells"][1], "key": "mesh.base_cells.1", "editable": True},
                    {"label": "Cells Nz", "value": m["base_cells"][2], "key": "mesh.base_cells.2", "editable": True},
                ]
            )
        elif node == "SnappyHexMesh Settings":
            m = self.openfoam["mesh"]
            rr = m.get("refinement_region", {})
            rr_min = rr.get("min", [-10.0, -20.0, -10.0])
            rr_max = rr.get("max", [50.0, 20.0, 10.0])
            if len(rr_min) != 3:
                rr_min = [-10.0, -20.0, -10.0]
            if len(rr_max) != 3:
                rr_max = [50.0, 20.0, 10.0]
            rows.extend(
                [
                    {"label": "Snappy Profile", "value": m.get("snappy_profile", "Balanced"), "key": "mesh.snappy_profile", "choices": ["Balanced", "Fast", "High Fidelity", "Custom"]},
                    {"label": "Snappy Parallel", "value": m.get("snappy_parallel_mode", "Off"), "key": "mesh.snappy_parallel_mode", "choices": ["Off", "Auto", "On"]},
                    {"label": "castellatedMesh", "value": m["castellated"], "key": "mesh.castellated", "choices": ["True", "False"]},
                    {"label": "snap", "value": m["snap"], "key": "mesh.snap", "choices": ["True", "False"]},
                    {"label": "addLayers", "value": m["layers"], "key": "mesh.layers", "choices": ["True", "False"]},
                    {"label": "refinement min", "value": m["refinement_min"], "key": "mesh.refinement_min", "editable": True},
                    {"label": "refinement max", "value": m["refinement_max"], "key": "mesh.refinement_max", "editable": True},
                    {"label": "resolveFeatureAngle", "value": m["feature_angle"], "key": "mesh.feature_angle", "editable": True},
                    {"label": "nSurfaceLayers", "value": m["n_surface_layers"], "key": "mesh.n_surface_layers", "editable": True},
                    {"label": "maxLocalCells", "value": m.get("max_local_cells", 100000), "key": "mesh.max_local_cells", "editable": True},
                    {"label": "maxGlobalCells", "value": m.get("max_global_cells", 2000000), "key": "mesh.max_global_cells", "editable": True},
                    {"label": "minRefinementCells", "value": m.get("min_refinement_cells", 10), "key": "mesh.min_refinement_cells", "editable": True},
                    {"label": "maxLoadUnbalance", "value": m.get("max_load_unbalance", 0.10), "key": "mesh.max_load_unbalance", "editable": True},
                    {"label": "locationInMesh X", "value": m.get("location_in_mesh", [4.0, 4.0, 0.0])[0], "key": "mesh.location_in_mesh.0", "editable": True},
                    {"label": "locationInMesh Y", "value": m.get("location_in_mesh", [4.0, 4.0, 0.0])[1], "key": "mesh.location_in_mesh.1", "editable": True},
                    {"label": "locationInMesh Z", "value": m.get("location_in_mesh", [4.0, 4.0, 0.0])[2], "key": "mesh.location_in_mesh.2", "editable": True},
                    {"label": "allowFreeStandingZoneFaces", "value": m.get("allow_free_standing_zone_faces", True), "key": "mesh.allow_free_standing_zone_faces", "choices": ["True", "False"]},
                    {"label": "nFeatureSnapIter", "value": m.get("n_feature_snap_iter", 10), "key": "mesh.n_feature_snap_iter", "editable": True},
                    {"label": "implicitFeatureSnap", "value": m.get("implicit_feature_snap", False), "key": "mesh.implicit_feature_snap", "choices": ["True", "False"]},
                    {"label": "explicitFeatureSnap", "value": m.get("explicit_feature_snap", True), "key": "mesh.explicit_feature_snap", "choices": ["True", "False"]},
                    {"label": "multiRegionFeatureSnap", "value": m.get("multi_region_feature_snap", False), "key": "mesh.multi_region_feature_snap", "choices": ["True", "False"]},
                    {"label": "expansionRatio", "value": m.get("expansion_ratio", 1.0), "key": "mesh.expansion_ratio", "editable": True},
                    {"label": "finalLayerThickness", "value": m.get("final_layer_thickness", 0.3), "key": "mesh.final_layer_thickness", "editable": True},
                    {"label": "minThickness", "value": m.get("min_thickness", 0.1), "key": "mesh.min_thickness", "editable": True},
                    {"label": "nGrow", "value": m.get("n_grow", 0), "key": "mesh.n_grow", "editable": True},
                    {"label": "layer featureAngle", "value": m.get("layer_feature_angle", 60.0), "key": "mesh.layer_feature_angle", "editable": True},
                    {"label": "slipFeatureAngle", "value": m.get("slip_feature_angle", 30.0), "key": "mesh.slip_feature_angle", "editable": True},
                    {"label": "layer nRelaxIter", "value": m.get("layer_n_relax_iter", 3), "key": "mesh.layer_n_relax_iter", "editable": True},
                    {"label": "nSmoothSurfaceNormals", "value": m.get("n_smooth_surface_normals", 1), "key": "mesh.n_smooth_surface_normals", "editable": True},
                    {"label": "nSmoothNormals", "value": m.get("n_smooth_normals", 3), "key": "mesh.n_smooth_normals", "editable": True},
                    {"label": "nSmoothThickness", "value": m.get("n_smooth_thickness", 10), "key": "mesh.n_smooth_thickness", "editable": True},
                    {"label": "maxFaceThicknessRatio", "value": m.get("max_face_thickness_ratio", 0.5), "key": "mesh.max_face_thickness_ratio", "editable": True},
                    {"label": "maxThicknessToMedialRatio", "value": m.get("max_thickness_to_medial_ratio", 0.3), "key": "mesh.max_thickness_to_medial_ratio", "editable": True},
                    {"label": "minMedialAxisAngle", "value": m.get("min_medial_axis_angle", 90.0), "key": "mesh.min_medial_axis_angle", "editable": True},
                    {"label": "nBufferCellsNoExtrude", "value": m.get("n_buffer_cells_no_extrude", 0), "key": "mesh.n_buffer_cells_no_extrude", "editable": True},
                    {"label": "nLayerIter", "value": m.get("n_layer_iter", 50), "key": "mesh.n_layer_iter", "editable": True},
                    {"label": "mergeTolerance", "value": m.get("merge_tolerance", 1e-6), "key": "mesh.merge_tolerance", "editable": True},
                    {"label": "Refine Region Enabled", "value": rr.get("enabled", False), "key": "mesh.refinement_region.enabled", "choices": ["True", "False"]},
                    {"label": "Refine Min X", "value": rr_min[0], "key": "mesh.refinement_region.min.0", "editable": True},
                    {"label": "Refine Min Y", "value": rr_min[1], "key": "mesh.refinement_region.min.1", "editable": True},
                    {"label": "Refine Min Z", "value": rr_min[2], "key": "mesh.refinement_region.min.2", "editable": True},
                    {"label": "Refine Max X", "value": rr_max[0], "key": "mesh.refinement_region.max.0", "editable": True},
                    {"label": "Refine Max Y", "value": rr_max[1], "key": "mesh.refinement_region.max.1", "editable": True},
                    {"label": "Refine Max Z", "value": rr_max[2], "key": "mesh.refinement_region.max.2", "editable": True},
                    {"label": "Refine Level", "value": rr.get("level", 4), "key": "mesh.refinement_region.level", "editable": True},
                ]
            )
        elif node == "CheckMesh":
            cm = self.openfoam["check_mesh"]
            rows.extend(
                [
                    {"label": "Enabled", "value": cm["enabled"], "key": "check_mesh.enabled", "choices": ["True", "False"]},
                    {"label": "maxNonOrtho", "value": cm["max_non_ortho"], "key": "check_mesh.max_non_ortho", "editable": True},
                    {"label": "maxBoundarySkewness", "value": cm["max_boundary_skewness"], "key": "check_mesh.max_boundary_skewness", "editable": True},
                    {"label": "minVol", "value": cm["min_vol"], "key": "check_mesh.min_vol", "editable": True},
                ]
            )
        elif node == "Boundary Conditions":
            bc = self.openfoam["boundary_conditions"]
            rows.append({"label": "Active Field", "value": bc.get("active_field", "U"), "key": "boundary_conditions.active_field", "choices": CFD_FIELDS})
            field = bc.get("active_field", "U")
            for patch in FLOW_PATCHES:
                pinfo = bc["patches"][patch]
                rows.append({"label": f"{patch}: enabled", "value": pinfo["enabled"], "key": f"boundary_conditions.patches.{patch}.enabled", "choices": ["True", "False"]})
                rows.append({"label": f"{patch}: patch type", "value": pinfo["type"], "key": f"boundary_conditions.patches.{patch}.type", "choices": PATCH_TYPES})
                bce = bc["fields"][field][patch]
                rows.append({"label": f"{patch}: {field} type", "value": bce.get("type", ""), "key": f"boundary_conditions.fields.{field}.{patch}.type", "editable": True})
                rows.append({"label": f"{patch}: {field} value", "value": bce.get("value", ""), "key": f"boundary_conditions.fields.{field}.{patch}.value", "editable": True})
        elif node == "Simulation Control":
            sim = self.openfoam["simulation"]
            rows.extend(
                [
                    {"label": "Solver", "value": self.openfoam["workflow"], "key": "workflow", "choices": ["simpleFoam", "potentialFoam"]},
                    {"label": "startTime", "value": sim["start_time"], "key": "simulation.start_time", "editable": True},
                    {"label": "endTime", "value": sim["end_time"], "key": "simulation.end_time", "editable": True},
                    {"label": "deltaT", "value": sim["delta_t"], "key": "simulation.delta_t", "editable": True},
                    {"label": "writeInterval", "value": sim["write_interval"], "key": "simulation.write_interval", "editable": True},
                    {"label": "purgeWrite", "value": sim["purge_write"], "key": "simulation.purge_write", "editable": True},
                    {"label": "Pseudo Transient", "value": sim["pseudo_transient"], "key": "simulation.pseudo_transient", "choices": ["True", "False"]},
                    {"label": "Run in Parallel", "value": sim.get("use_parallel", True), "key": "simulation.use_parallel", "choices": ["True", "False"]},
                    {"label": "MPI Cores", "value": sim.get("mpi_cores", 4), "key": "simulation.mpi_cores", "editable": True},
                ]
            )
        elif node == "Numerics":
            n = self.openfoam["numerics"]
            rows.extend(
                [
                    {"label": "fvSchemes Preset", "value": n["fv_schemes_preset"], "key": "numerics.fv_schemes_preset", "choices": ["bounded steady RANS", "potentialFoam basic"]},
                    {"label": "fvSolution Preset", "value": n["fv_solution_preset"], "key": "numerics.fv_solution_preset", "choices": ["SIMPLE-RANS", "Potential"]},
                    {"label": "Turbulence Model", "value": n["turbulence_model"], "key": "numerics.turbulence_model", "choices": ["kOmegaSST", "kEpsilon", "SpalartAllmaras"]},
                    {"label": "U Solver Tol", "value": n["u_solver_tol"], "key": "numerics.u_solver_tol", "editable": True},
                    {"label": "p Solver Tol", "value": n["p_solver_tol"], "key": "numerics.p_solver_tol", "editable": True},
                    {"label": "U Relax", "value": n["u_relax"], "key": "numerics.u_relax", "editable": True},
                    {"label": "p Relax", "value": n["p_relax"], "key": "numerics.p_relax", "editable": True},
                    {"label": "Residual Control", "value": n["simple_residual_control"], "key": "numerics.simple_residual_control", "editable": True},
                ]
            )
        elif node == "Post Process":
            pp = self.openfoam.get("post_process", {})
            fields = list(pp.get("available_fields", []))
            rows.extend(
                [
                    {"label": "Case Dir", "value": pp.get("case_dir", ""), "editable": False},
                    {"label": "Latest Time", "value": pp.get("latest_time", ""), "editable": False},
                    {"label": "Detected Fields", "value": ", ".join(fields) if fields else "(none)", "editable": False},
                    {"label": "Updated At", "value": pp.get("updated_at", ""), "editable": False},
                ]
            )
        elif len(path) >= 3 and path[1] == "Post Process":
            child = path[2]
            pp = self.openfoam.get("post_process", {})
            fields = [str(f) for f in pp.get("available_fields", [])]
            stage_logs = pp.get("stage_logs", {}) if isinstance(pp.get("stage_logs"), dict) else {}
            if child == "blockMesh":
                rows.append({"label": "blockMesh Log", "value": stage_logs.get("domain_mesh", ""), "editable": False})
            elif child == "Surface Feature Mesh":
                rows.append({"label": "Surface Features Log", "value": stage_logs.get("surface_features", ""), "editable": False})
            elif child == "SnappyHexMesh":
                rows.append({"label": "Snappy Log", "value": stage_logs.get("snappy_mesh", ""), "editable": False})
            elif child == "Pressure Field":
                rows.append({"label": "Pressure Field", "value": ("p" if "p" in fields else "not detected"), "editable": False})
            elif child == "Velocity Field":
                rows.append({"label": "Velocity Field", "value": ("U" if "U" in fields else "not detected"), "editable": False})
            elif child == "Other Fields":
                others = [f for f in fields if f not in {"p", "U"}]
                rows.append({"label": "Other Fields", "value": ", ".join(others) if others else "(none)", "editable": False})
        elif node == "Solve":
            e = self.openfoam["export"]
            s = self.openfoam["scripts"]
            rows.extend(
                [
                    {"label": "Output Path", "value": e["output_path"], "key": "export.output_path", "editable": True},
                    {"label": "Write Helper Scripts", "value": s["write_helper_scripts"], "key": "scripts.write_helper_scripts", "choices": ["True", "False"]},
                    {"label": "Include surfaceFeatureExtract", "value": s["include_surface_feature_extract"], "key": "scripts.include_surface_feature_extract", "choices": ["True", "False"]},
                    {"label": "Last Exported", "value": e.get("last_exported_at", ""), "editable": False},
                ]
            )
        return rows

    def apply_property_edit(self, key, raw_value):
        try:
            value = self._cast_property_value(key, raw_value)
            if key == "mesh.preset":
                self._set_openfoam_value(key, value)
                self._on_mesh_preset_changed(value)
            elif key == "mesh.snappy_profile":
                self._set_openfoam_value(key, value)
                self._on_snappy_profile_changed(value)
            elif key == "workflow":
                self._set_openfoam_value(key, value)
                self._on_solver_changed(value)
            else:
                self._set_openfoam_value(key, value)
            self._sync_widgets_from_state()
            return True, ""
        except Exception as exc:
            return False, str(exc)

    def _cast_property_value(self, key, raw):
        boolean_keys = {
            "check_mesh.enabled",
            "simulation.pseudo_transient",
            "simulation.use_parallel",
            "scripts.write_helper_scripts",
            "scripts.include_surface_feature_extract",
            "mesh.castellated",
            "mesh.snap",
            "mesh.layers",
            "mesh.allow_free_standing_zone_faces",
            "mesh.implicit_feature_snap",
            "mesh.explicit_feature_snap",
            "mesh.multi_region_feature_snap",
            "mesh.refinement_region.enabled",
        }
        if key.startswith("boundary_conditions.patches.") and key.endswith(".enabled"):
            boolean_keys.add(key)
        if key in boolean_keys:
            txt = str(raw).strip().lower()
            if txt in ("true", "1", "yes", "on"):
                return True
            if txt in ("false", "0", "no", "off"):
                return False
            raise ValueError("Expected True or False.")
        if key.endswith(".0") or key.endswith(".1") or key.endswith(".2"):
            if "base_cells" in key:
                return int(float(raw))
            return float(raw)
        int_suffix = (
            "refinement_min",
            "refinement_max",
            "n_surface_layers",
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
            "refinement_region.level",
        )
        if key in {"simulation.purge_write", "simulation.mpi_cores"} or key.endswith(int_suffix):
            return int(float(raw))
        if any(
            h in key
            for h in (
                "scale",
                "domain_min",
                "domain_max",
                "feature_angle",
                "max_non_ortho",
                "max_boundary_skewness",
                "min_vol",
                "start_time",
                "end_time",
                "delta_t",
                "write_interval",
                "solver_tol",
                "relax",
                "residual_control",
                "max_load_unbalance",
                "location_in_mesh",
                "expansion_ratio",
                "final_layer_thickness",
                "min_thickness",
                "slip_feature_angle",
                "max_face_thickness_ratio",
                "max_thickness_to_medial_ratio",
                "min_medial_axis_angle",
                "merge_tolerance",
            )
        ):
            return float(raw)
        return str(raw)

    def _set_openfoam_value(self, dotted_key, value):
        parts = dotted_key.split(".")
        cur = self.openfoam
        for i, part in enumerate(parts):
            last = i == len(parts) - 1
            if part.isdigit():
                idx = int(part)
                if last:
                    cur[idx] = value
                    break
                cur = cur[idx]
                continue
            if last:
                cur[part] = value
                break
            nxt = cur.get(part)
            if nxt is None:
                nxt = {}
                cur[part] = nxt
            cur = nxt
        if dotted_key == "numerics.simple_residual_control":
            numerics = self.openfoam.setdefault("numerics", {})
            fv_solution = numerics.setdefault("fv_solution", {})
            fv_solution["residual_control_p"] = value
            fv_solution["residual_control_u"] = value
        self.state.setdefault("aerodynamics", {})["openfoam"] = self.openfoam

    def _sync_widgets_from_state(self, refresh_viewer=True):
        self.openfoam = ensure_openfoam_state(self.state.setdefault("aerodynamics", {}))
        if hasattr(self, "lbl_required_case_root"):
            self.lbl_required_case_root.setText(f"Required case root: {self._required_case_root()}")
        if hasattr(self, "input_case_dir"):
            case_dir = str(self.openfoam.get("execution", {}).get("case_dir", "")).strip()
            if not case_dir:
                case_dir = str(self.openfoam.get("export", {}).get("output_path", "")).strip()
            self.input_case_dir.setText(case_dir)
        if hasattr(self, "input_cfd_stl"):
            self.input_cfd_stl.setText(str(self.openfoam["geometry"]["stl_path"]))
            self.input_tri_surface.setText(str(self.openfoam["geometry"]["tri_surface_name"]))
            self.input_cfd_scale.blockSignals(True)
            self.input_cfd_scale.setValue(float(self.openfoam["geometry"]["scale"]))
            self.input_cfd_scale.blockSignals(False)
        if hasattr(self, "cmb_mesh_preset"):
            idx = self.cmb_mesh_preset.findText(self.openfoam["mesh"]["preset"])
            blocked = self.cmb_mesh_preset.blockSignals(True)
            self.cmb_mesh_preset.setCurrentIndex(idx if idx >= 0 else 0)
            self.cmb_mesh_preset.blockSignals(blocked)
            m = self.openfoam["mesh"]
            vals = {"xmin": m["domain_min"][0], "ymin": m["domain_min"][1], "zmin": m["domain_min"][2], "xmax": m["domain_max"][0], "ymax": m["domain_max"][1], "zmax": m["domain_max"][2]}
            for name, spin in self.mesh_spin.items():
                spin.blockSignals(True)
                spin.setValue(float(vals[name]))
                spin.blockSignals(False)
            cells = {"nx": m["base_cells"][0], "ny": m["base_cells"][1], "nz": m["base_cells"][2]}
            for name, spin in self.mesh_cells.items():
                spin.blockSignals(True)
                spin.setValue(int(cells[name]))
                spin.blockSignals(False)
        if hasattr(self, "cmb_snappy_profile"):
            m = self.openfoam["mesh"]
            idx = self.cmb_snappy_profile.findText(str(m.get("snappy_profile", "Balanced")))
            blocked = self.cmb_snappy_profile.blockSignals(True)
            self.cmb_snappy_profile.setCurrentIndex(idx if idx >= 0 else 0)
            self.cmb_snappy_profile.blockSignals(blocked)
            idx = self.cmb_snappy_parallel.findText(str(m.get("snappy_parallel_mode", "Off")))
            blocked = self.cmb_snappy_parallel.blockSignals(True)
            self.cmb_snappy_parallel.setCurrentIndex(idx if idx >= 0 else 0)
            self.cmb_snappy_parallel.blockSignals(blocked)
            self.chk_castellated.setChecked(bool(m["castellated"]))
            self.chk_snap.setChecked(bool(m["snap"]))
            self.chk_layers.setChecked(bool(m["layers"]))
            self.spin_ref_min.setValue(int(m["refinement_min"]))
            self.spin_ref_max.setValue(int(m["refinement_max"]))
            self.spin_feature_angle.setValue(float(m["feature_angle"]))
            self.spin_layers.setValue(int(m["n_surface_layers"]))
            for key, spin in getattr(self, "snappy_spin", {}).items():
                spin.blockSignals(True)
                spin.setValue(float(m.get(key, spin.value())))
                spin.blockSignals(False)
            self.chk_implicit_snap.setChecked(bool(m.get("implicit_feature_snap", False)))
            self.chk_explicit_snap.setChecked(bool(m.get("explicit_feature_snap", True)))
            self.chk_multi_region_snap.setChecked(bool(m.get("multi_region_feature_snap", False)))
            self.chk_allow_free_faces.setChecked(bool(m.get("allow_free_standing_zone_faces", True)))
            if hasattr(self, "chk_refinement_region"):
                rr = m.get("refinement_region", {})
                enabled = bool(rr.get("enabled", False))
                self.chk_refinement_region.setChecked(enabled)
                rr_min = rr.get("min", [-10.0, -20.0, -10.0])
                rr_max = rr.get("max", [50.0, 20.0, 10.0])
                axis_keys = ("x", "y", "z")
                for idx, axis in enumerate(axis_keys):
                    key = f"min_{axis}"
                    spin = self.refinement_region_spin.get(key)
                    if spin is not None and idx < len(rr_min):
                        spin.blockSignals(True)
                        spin.setValue(float(rr_min[idx]))
                        spin.blockSignals(False)
                        spin.setEnabled(enabled)
                    key = f"max_{axis}"
                    spin = self.refinement_region_spin.get(key)
                    if spin is not None and idx < len(rr_max):
                        spin.blockSignals(True)
                        spin.setValue(float(rr_max[idx]))
                        spin.blockSignals(False)
                        spin.setEnabled(enabled)
                self.spin_refinement_level.blockSignals(True)
                self.spin_refinement_level.setValue(int(rr.get("level", 4)))
                self.spin_refinement_level.blockSignals(False)
                self.spin_refinement_level.setEnabled(enabled)
            self._sync_snappy_profile_editability()
        if hasattr(self, "chk_checkmesh_enabled"):
            cm = self.openfoam["check_mesh"]
            self.chk_checkmesh_enabled.setChecked(bool(cm["enabled"]))
            self.spin_max_non_ortho.setValue(float(cm["max_non_ortho"]))
            self.spin_max_skew.setValue(float(cm["max_boundary_skewness"]))
            self.spin_min_vol.setValue(float(cm["min_vol"]))
        if hasattr(self, "patch_enabled"):
            bc = self.openfoam["boundary_conditions"]
            for patch in FLOW_PATCHES:
                pinfo = bc["patches"][patch]
                self.patch_enabled[patch].setChecked(bool(pinfo["enabled"]))
                idx = self.patch_type[patch].findText(str(pinfo["type"]))
                self.patch_type[patch].setCurrentIndex(idx if idx >= 0 else 0)
            idx = self.cmb_bc_field.findText(str(bc.get("active_field", "U")))
            self.cmb_bc_field.setCurrentIndex(idx if idx >= 0 else 0)
            self._sync_bc_field_widgets()
        if hasattr(self, "cmb_solver"):
            idx = self.cmb_solver.findText(self.openfoam["workflow"])
            blocked = self.cmb_solver.blockSignals(True)
            self.cmb_solver.setCurrentIndex(idx if idx >= 0 else 0)
            self.cmb_solver.blockSignals(blocked)
            sim = self.openfoam["simulation"]
            self.spin_start.setValue(float(sim["start_time"]))
            self.spin_end.setValue(float(sim["end_time"]))
            self.spin_dt.setValue(float(sim["delta_t"]))
            self.spin_write_interval.setValue(float(sim["write_interval"]))
            self.spin_purge.setValue(int(sim["purge_write"]))
            self.chk_pseudo_transient.setChecked(bool(sim["pseudo_transient"]))
            self.chk_use_parallel.setChecked(bool(sim.get("use_parallel", True)))
            self.spin_mpi_cores.setValue(max(1, int(sim.get("mpi_cores", 4))))
        if hasattr(self, "cmb_fv_schemes"):
            n = self.openfoam["numerics"]
            blocked = self.cmb_fv_schemes.blockSignals(True)
            self.cmb_fv_schemes.setCurrentIndex(max(0, self.cmb_fv_schemes.findText(n["fv_schemes_preset"])))
            self.cmb_fv_schemes.blockSignals(blocked)
            blocked = self.cmb_fv_solution.blockSignals(True)
            self.cmb_fv_solution.setCurrentIndex(max(0, self.cmb_fv_solution.findText(n["fv_solution_preset"])))
            self.cmb_fv_solution.blockSignals(blocked)
            blocked = self.cmb_turb_model.blockSignals(True)
            self.cmb_turb_model.setCurrentIndex(max(0, self.cmb_turb_model.findText(n["turbulence_model"])))
            self.cmb_turb_model.blockSignals(blocked)
            self.spin_u_tol.setValue(float(n["u_solver_tol"]))
            self.spin_p_tol.setValue(float(n["p_solver_tol"]))
            self.spin_u_relax.setValue(float(n["u_relax"]))
            self.spin_p_relax.setValue(float(n["p_relax"]))
            schemes = _effective_fv_schemes(n)
            sol = _effective_fv_solution(n)
            if hasattr(self, "cmb_ddt_default"):
                _set_combo_value(self.cmb_ddt_default, schemes["ddt_default"])
                _set_combo_value(self.cmb_grad_default, schemes["grad_default"])
                _set_combo_value(self.cmb_div_phi_u, schemes["div_phi_u"])
                _set_combo_value(self.cmb_div_phi_turb, schemes["div_phi_turb"])
                _set_combo_value(self.cmb_laplacian_default, schemes["laplacian_default"])
                _set_combo_value(self.cmb_interpolation_default, schemes["interpolation_default"])
                _set_combo_value(self.cmb_sn_grad_default, schemes["sn_grad_default"])
                _set_combo_value(self.cmb_wall_dist_method, schemes["wall_dist_method"])
            if hasattr(self, "cmb_p_solver"):
                _set_combo_value(self.cmb_p_solver, sol["p_solver"])
                _set_combo_value(self.cmb_p_smoother, sol["p_smoother"])
                _set_combo_value(self.cmb_p_preconditioner, sol["p_preconditioner"])
                self.spin_p_rel_tol.setValue(float(sol["p_rel_tol"]))
                _set_combo_value(self.cmb_u_solver, sol["u_solver"])
                _set_combo_value(self.cmb_u_smoother, sol["u_smoother"])
                _set_combo_value(self.cmb_u_preconditioner, sol["u_preconditioner"])
                self.spin_u_rel_tol.setValue(float(sol["u_rel_tol"]))
                self.spin_simple_non_ortho.setValue(int(sol["simple_n_non_ortho"]))
                self.chk_simple_consistent.setChecked(bool(sol["simple_consistent"]))
                self.spin_residual_p.setValue(float(sol["residual_control_p"]))
                self.spin_residual_u.setValue(float(sol["residual_control_u"]))
                self._update_fv_solution_controls()
            self.cmb_turb_model.setEnabled(self.openfoam["workflow"] == "simpleFoam")
        if hasattr(self, "input_export_path"):
            e = self.openfoam["export"]
            s = self.openfoam["scripts"]
            x = self.openfoam["execution"]
            self.input_export_path.setText(str(e.get("output_path", "")))
            self.chk_write_scripts.setChecked(bool(s.get("write_helper_scripts", True)))
            self.chk_surface_feature_extract.setChecked(bool(s.get("include_surface_feature_extract", True)))
            files = e.get("generated_files", [])
            stamp = e.get("last_exported_at", "")
            action = str(e.get("last_action", "")).strip()
            if stamp:
                if action:
                    lowered = action.lower()
                    if lowered == "updated":
                        verb = "Updated"
                    elif lowered == "generated":
                        verb = "Generated"
                    else:
                        verb = action.capitalize()
                else:
                    verb = "Generated"
                self.lbl_export_status.setText(f"{verb} {len(files)} file(s). {stamp}")
            else:
                self.lbl_export_status.setText("")
            if hasattr(self, "btn_update_case"):
                case_dir = str(x.get("case_dir", "")).strip()
                if not case_dir:
                    case_dir = str(e.get("output_path", "")).strip()
                self.btn_update_case.setEnabled(bool(case_dir) and self._case_dir_is_allowed(case_dir))
            self.lbl_run_status.setText(
                f"Status: {x.get('status', 'idle')} | Stage: {x.get('active_stage', 'none')}"
            )
            result = x.get("results", {}) if isinstance(x.get("results"), dict) else {}
            summary = result.get("summary", {}) if isinstance(result.get("summary"), dict) else {}
            if summary:
                residual = result.get("residual_status", "n/a")
                self.lbl_force_coeffs.setText(
                    "CL/CD/CM: "
                    f"{summary.get('Cl', 'n/a')} / {summary.get('Cd', 'n/a')} / {summary.get('Cm', 'n/a')}"
                    f" | Residual: {residual}"
                )
            else:
                self.lbl_force_coeffs.setText("CL/CD/CM: n/a")
            self._set_execution_controls_running(x.get("status") == "running")
        if hasattr(self, "lbl_post_status"):
            pp = self.openfoam.get("post_process", {})
            latest = str(pp.get("latest_time", "")).strip() or "(none)"
            fields = pp.get("available_fields", [])
            self.lbl_post_status.setText(
                f"Latest time: {latest}\n"
                f"Detected fields: {', '.join(fields) if fields else '(none)'}"
            )
        if hasattr(self, "input_paraview_path"):
            pp = self.openfoam.get("post_process", {})
            path = str(pp.get("paraview_path", "")).strip()
            self.input_paraview_path.blockSignals(True)
            self.input_paraview_path.setText(path)
            self.input_paraview_path.blockSignals(False)
        if hasattr(self, "lbl_vtk_status"):
            pp = self.openfoam.get("post_process", {})
            status = str(pp.get("vtk_status", "")).strip() or "VTK: not exported"
            self.lbl_vtk_status.setText(status)
        if hasattr(self.ui, "cmb_ribbon_solver"):
            _set_combo_value(self.ui.cmb_ribbon_solver, self.openfoam["workflow"])
        if hasattr(self.ui, "cmb_ribbon_vtk_target"):
            target_kind = self._vtk_active_kind or (self.cmb_vtk_mesh.currentText() if hasattr(self, "cmb_vtk_mesh") else "snappy")
            _set_combo_value(self.ui.cmb_ribbon_vtk_target, target_kind)
        if hasattr(self.ui, "cmb_ribbon_result_field"):
            combo = self.ui.cmb_ribbon_result_field
            selected = str(self._viewer_scalar_field or "")
            blocked = combo.blockSignals(True)
            combo.clear()
            combo.addItem("Solid Color", "")
            for name in self.available_result_fields():
                combo.addItem(str(name), str(name))
            idx = combo.findData(selected)
            if idx < 0:
                idx = combo.findText(selected)
            combo.setCurrentIndex(idx if idx >= 0 else 0)
            combo.blockSignals(blocked)
        if hasattr(self.ui, "lbl_ribbon_run_status_value"):
            exe = self._execution_state()
            self.ui.lbl_ribbon_run_status_value.setText(str(exe.get("status", "idle")))
            self.ui.lbl_ribbon_active_stage_value.setText(str(exe.get("active_stage", "none")))
        if hasattr(self.ui, "btn_ribbon_surface_mode"):
            blocked = self.ui.btn_ribbon_surface_mode.blockSignals(True)
            self.ui.btn_ribbon_surface_mode.setChecked(self._viewer_render_mode == "surface")
            self.ui.btn_ribbon_surface_mode.blockSignals(blocked)
        if hasattr(self.ui, "btn_ribbon_wireframe_mode"):
            blocked = self.ui.btn_ribbon_wireframe_mode.blockSignals(True)
            self.ui.btn_ribbon_wireframe_mode.setChecked(self._viewer_render_mode == "wireframe")
            self.ui.btn_ribbon_wireframe_mode.blockSignals(blocked)
        if hasattr(self.ui, "btn_ribbon_toggle_contours"):
            blocked = self.ui.btn_ribbon_toggle_contours.blockSignals(True)
            self.ui.btn_ribbon_toggle_contours.setChecked(self._viewer_contours_enabled)
            self.ui.btn_ribbon_toggle_contours.blockSignals(blocked)
        if hasattr(self.ui, "btn_ribbon_toggle_slice"):
            blocked = self.ui.btn_ribbon_toggle_slice.blockSignals(True)
            self.ui.btn_ribbon_toggle_slice.setChecked(self._viewer_slice_enabled)
            self.ui.btn_ribbon_toggle_slice.blockSignals(blocked)
        if hasattr(self.ui, "btn_ribbon_toggle_streamlines"):
            blocked = self.ui.btn_ribbon_toggle_streamlines.blockSignals(True)
            self.ui.btn_ribbon_toggle_streamlines.setChecked(self._viewer_streamlines_enabled)
            self.ui.btn_ribbon_toggle_streamlines.blockSignals(blocked)
        if hasattr(self.ui, "btn_ribbon_toggle_tripod"):
            blocked = self.ui.btn_ribbon_toggle_tripod.blockSignals(True)
            self.ui.btn_ribbon_toggle_tripod.setChecked(self._tripod_visible)
            self.ui.btn_ribbon_toggle_tripod.blockSignals(blocked)
        self._update_pressure_controls_visibility()
        if refresh_viewer:
            self._refresh_viewer_scene()

    def _required_case_root(self):
        WORKSPACE_CASES_DIR.mkdir(parents=True, exist_ok=True)
        return WORKSPACE_CASES_DIR

    def _case_dir_is_allowed(self, case_dir):
        if not case_dir:
            return False
        try:
            case_path = Path(case_dir).resolve(strict=False)
            root = self._required_case_root().resolve(strict=False)
        except Exception:
            return False
        try:
            return case_path.is_relative_to(root)
        except AttributeError:
            try:
                case_path.relative_to(root)
                return True
            except Exception:
                return False

    def _require_allowed_case_dir(self, case_dir, action_label):
        if self._case_dir_is_allowed(case_dir):
            return True
        root = self._required_case_root()
        QMessageBox.warning(
            self.ui.aerodynamics_tab,
            "OpenFOAM Case Location",
            f"{action_label} requires a case folder under:\n{root}",
        )
        return False

    def _notify_property_refresh(self):
        parent = getattr(self.ui, "aerodynamics_tab", None)
        while parent is not None:
            if hasattr(parent, "_refresh_property_from_tree_selection"):
                try:
                    parent._refresh_property_from_tree_selection(sync_tab=False)
                except TypeError:
                    parent._refresh_property_from_tree_selection()
                return
            parent = parent.parentWidget() if hasattr(parent, "parentWidget") else None

    def _notify_case_opened(self, case_dir, source_kind="opened", template_id=""):
        parent = getattr(self.ui, "aerodynamics_tab", None)
        while parent is not None:
            if hasattr(parent, "_workspace_case_opened"):
                try:
                    parent._workspace_case_opened(case_dir, source_kind=source_kind, template_id=template_id)
                except TypeError:
                    parent._workspace_case_opened(case_dir)
                return
            parent = parent.parentWidget() if hasattr(parent, "parentWidget") else None
