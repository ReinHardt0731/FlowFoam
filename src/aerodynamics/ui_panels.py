from ._controller_common import *

def panel_keys():
    return [
        "geometry",
        "mesh",
        "snappy",
        "check_mesh",
        "boundary_conditions",
        "simulation",
        "numerics",
        "post_process",
        "export",
    ]


class UIPanelMixin:
    def _build_case_panel(self):
        box = QGroupBox("CFD Pipeline", self.of_task_root)
        layout = QVBoxLayout(box)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)
        self.lbl_required_case_root = QLabel("", box)
        self.lbl_required_case_root.setWordWrap(True)
        layout.addWidget(self.lbl_required_case_root)
        row = QHBoxLayout()
        self.input_case_dir = QLineEdit(box)
        self.input_case_dir.setReadOnly(True)
        self.input_case_dir.setPlaceholderText("No case selected")
        row.addWidget(self.input_case_dir, 1)
        self.btn_import_case = QPushButton("Import Case", box)
        self.btn_clear_case = QPushButton("Clear Case", box)
        row.addWidget(self.btn_import_case)
        row.addWidget(self.btn_clear_case)
        layout.addLayout(row)
        self.btn_import_case.clicked.connect(self.import_openfoam_case_from_dialog)
        self.btn_clear_case.clicked.connect(self.clear_openfoam_case)
        
        # Output Folder field (moved from Solve panel)
        layout.addSpacing(12)
        layout.addWidget(QLabel("<b>Case Management</b>", box))
        self.input_export_path = QLineEdit(box)
        export_row = QHBoxLayout()
        self.btn_pick_export_path = QPushButton("Browse...", box)
        export_row.addWidget(self.input_export_path, 1)
        export_row.addWidget(self.btn_pick_export_path)
        export_holder = QWidget()
        export_holder.setLayout(export_row)
        form_layout = QFormLayout()
        form_layout.addRow("Output Folder", export_holder)
        
        # Config and case generation buttons (moved from Solve panel)
        self.btn_save_cfd_config = QPushButton("Save CFD Config", box)
        self.btn_load_cfd_config = QPushButton("Load CFD Config", box)
        self.btn_generate_case = QPushButton("Generate Case", box)
        form_layout.addRow(self.btn_save_cfd_config)
        form_layout.addRow(self.btn_load_cfd_config)
        form_layout.addRow(self.btn_generate_case)
        
        layout.addLayout(form_layout)
        
        # Signal connections for Output Folder and config buttons
        self.btn_pick_export_path.clicked.connect(self._pick_export_dir)
        self.input_export_path.editingFinished.connect(lambda: self._set_openfoam_value("export.output_path", self.input_export_path.text()))
        self.btn_save_cfd_config.clicked.connect(self.save_openfoam_config_from_dialog)
        self.btn_load_cfd_config.clicked.connect(self.load_openfoam_config_from_dialog)
        self.btn_generate_case.clicked.connect(self.export_openfoam_case_from_dialog)
        
        return box

    def _build_geometry_panel(self):
        box = QGroupBox("Geometry")
        layout = QFormLayout(box)
        self.input_cfd_stl = QLineEdit(box)
        self.input_cfd_stl.setReadOnly(True)
        self.input_tri_surface = QLineEdit(box)
        self.input_cfd_scale = QDoubleSpinBox(box)
        self.input_cfd_scale.setRange(0.001, 1000.0)
        self.input_cfd_scale.setDecimals(6)
        btn_row = QHBoxLayout()
        self.btn_import_cfd_stl = QPushButton("Import STL", box)
        self.btn_clear_cfd_stl = QPushButton("Clear STL", box)
        btn_row.addWidget(self.btn_import_cfd_stl)
        btn_row.addWidget(self.btn_clear_cfd_stl)
        
        # Watertightness check
        check_row = QHBoxLayout()
        self.btn_check_watertight = QPushButton("Check Watertightness", box)
        self.lbl_watertight_status = QLabel("Load STL to check", box)
        self.lbl_watertight_status.setStyleSheet("color: #999; font-size: 10px;")
        check_row.addWidget(self.btn_check_watertight)
        check_row.addStretch()
        
        layout.addRow("STL Path", self.input_cfd_stl)
        layout.addRow("triSurface Name", self.input_tri_surface)
        layout.addRow("Scale", self.input_cfd_scale)
        layout.addRow(btn_row)
        layout.addRow(check_row)
        layout.addRow("Status", self.lbl_watertight_status)
        
        self.btn_import_cfd_stl.clicked.connect(self.import_cfd_stl_from_dialog)
        self.btn_clear_cfd_stl.clicked.connect(self._clear_cfd_stl)
        self.btn_check_watertight.clicked.connect(self._check_stl_watertightness)
        self.input_tri_surface.editingFinished.connect(
            lambda: self._set_openfoam_value("geometry.tri_surface_name", self.input_tri_surface.text())
        )
        self.input_cfd_scale.valueChanged.connect(lambda v: self._set_openfoam_value("geometry.scale", float(v)))
        return box

    def _build_mesh_panel(self):
        box = QGroupBox("Domain Mesh (blockMesh)")
        layout = QGridLayout(box)
        self.cmb_mesh_preset = QComboBox(box)
        self.cmb_mesh_preset.addItems(["External Aerodynamics", "Coarse", "Medium", "Fine"])
        layout.addWidget(QLabel("Preset"), 0, 0)
        layout.addWidget(self.cmb_mesh_preset, 0, 1, 1, 2)
        self.mesh_spin = {}
        labels = [("xmin", -9999.0, 9999.0), ("ymin", -9999.0, 9999.0), ("zmin", -9999.0, 9999.0), ("xmax", -9999.0, 9999.0), ("ymax", -9999.0, 9999.0), ("zmax", -9999.0, 9999.0)]
        for idx, (name, mn, mx) in enumerate(labels, start=1):
            spin = QDoubleSpinBox(box)
            spin.setRange(mn, mx)
            spin.setDecimals(4)
            self.mesh_spin[name] = spin
            layout.addWidget(QLabel(name), idx, 0)
            layout.addWidget(spin, idx, 1)
        self.mesh_cells = {}
        for idx, name in enumerate(["nx", "ny", "nz"], start=1):
            spin = QSpinBox(box)
            spin.setRange(2, 2000)
            self.mesh_cells[name] = spin
            layout.addWidget(QLabel(name), idx, 2)
            layout.addWidget(spin, idx, 3)
        self.chk_show_tripod = QCheckBox("Show XYZ tripod at origin", box)
        self.chk_show_tripod.setChecked(True)
        layout.addWidget(self.chk_show_tripod, 8, 0, 1, 3)
        self.cmb_mesh_preset.currentTextChanged.connect(self._on_mesh_preset_changed)
        for n, sp in self.mesh_spin.items():
            sp.valueChanged.connect(lambda _v, name=n: self._on_mesh_scalar_changed(name))
        for n, sp in self.mesh_cells.items():
            sp.valueChanged.connect(lambda _v, name=n: self._on_mesh_cells_changed(name))
        self.chk_show_tripod.toggled.connect(self.set_tripod_visible)
        return box

    def _build_snappy_panel(self):
        box = QGroupBox("SnappyHexMesh Settings")
        layout = QGridLayout(box)

        self.cmb_snappy_profile = QComboBox(box)
        self.cmb_snappy_profile.addItems(["Balanced", "Fast", "High Fidelity", "Custom"])
        self.cmb_snappy_profile.setMaximumWidth(150)
        profile_layout = QHBoxLayout()
        profile_layout.addWidget(self.cmb_snappy_profile)
        profile_layout.addWidget(create_help_button("snappy_profile", box))
        profile_layout.addStretch()
        layout.addWidget(QLabel("Snappy Profile"), 0, 0)
        layout.addLayout(profile_layout, 0, 1, 1, 1)
        
        self.cmb_snappy_parallel = QComboBox(box)
        self.cmb_snappy_parallel.addItems(["Off", "Auto", "On"])
        self.cmb_snappy_parallel.setMaximumWidth(150)
        parallel_layout = QHBoxLayout()
        parallel_layout.addWidget(self.cmb_snappy_parallel)
        parallel_layout.addWidget(create_help_button("snappy_parallel", box))
        parallel_layout.addStretch()
        layout.addWidget(QLabel("Snappy Parallel"), 1, 0)
        layout.addLayout(parallel_layout, 1, 1, 1, 1)

        self.chk_castellated = QCheckBox("castellatedMesh", box)
        self.chk_snap = QCheckBox("snap", box)
        self.chk_layers = QCheckBox("addLayers", box)
        
        castellated_layout = QHBoxLayout()
        castellated_layout.addWidget(self.chk_castellated)
        castellated_layout.addWidget(create_help_button("castellatedMesh", box))
        castellated_layout.addStretch()
        
        snap_layout = QHBoxLayout()
        snap_layout.addWidget(self.chk_snap)
        snap_layout.addWidget(create_help_button("snap", box))
        snap_layout.addStretch()
        
        layers_layout = QHBoxLayout()
        layers_layout.addWidget(self.chk_layers)
        layers_layout.addWidget(create_help_button("addLayers", box))
        layers_layout.addStretch()
        
        layout.addLayout(castellated_layout, 2, 0)
        layout.addLayout(snap_layout, 2, 1)
        layout.addLayout(layers_layout, 2, 2)

        self.spin_ref_min = QSpinBox(box)
        self.spin_ref_max = QSpinBox(box)
        self.spin_ref_min.setRange(0, 10)
        self.spin_ref_max.setRange(0, 10)
        self.spin_ref_min.setMaximumWidth(100)
        self.spin_ref_max.setMaximumWidth(100)
        
        self.spin_feature_angle = QDoubleSpinBox(box)
        self.spin_feature_angle.setRange(0.0, 180.0)
        self.spin_feature_angle.setDecimals(2)
        self.spin_feature_angle.setMaximumWidth(100)
        
        self.spin_layers = QSpinBox(box)
        self.spin_layers.setRange(0, 20)
        self.spin_layers.setMaximumWidth(100)
        
        layout.addWidget(QLabel("Refinement Min"), 3, 0)
        layout.addWidget(self.spin_ref_min, 3, 1)
        layout.addWidget(QLabel("Refinement Max"), 3, 2)
        layout.addWidget(self.spin_ref_max, 3, 3)
        
        ref_angle_layout = QHBoxLayout()
        ref_angle_layout.addWidget(self.spin_feature_angle)
        ref_angle_layout.addWidget(create_help_button("featureAngle", box))
        ref_angle_layout.addStretch()
        layout.addWidget(QLabel("Resolve Feature Angle"), 4, 0)
        layout.addLayout(ref_angle_layout, 4, 1, 1, 1)
        
        layers_layout = QHBoxLayout()
        layers_layout.addWidget(self.spin_layers)
        layers_layout.addWidget(create_help_button("nSurfaceLayers", box))
        layers_layout.addStretch()
        layout.addWidget(QLabel("nSurfaceLayers"), 4, 2)
        layout.addLayout(layers_layout, 4, 3, 1, 1)

        self.snappy_spin = {}
        cfg = [
            ("max_local_cells", "maxLocalCells", 1, 100000000, 0, 5),
            ("max_global_cells", "maxGlobalCells", 1, 200000000, 0, 6),
            ("min_refinement_cells", "minRefinementCells", 0, 1000000, 0, 7),
            ("max_load_unbalance", "maxLoadUnbalance", 0.0, 1.0, 4, 8),
            ("n_feature_snap_iter", "nFeatureSnapIter", 0, 100, 0, 9),
            ("expansion_ratio", "expansionRatio", 0.1, 5.0, 3, 10),
            ("final_layer_thickness", "finalLayerThickness", 0.001, 5.0, 4, 11),
            ("min_thickness", "minThickness", 0.0001, 5.0, 4, 12),
            ("n_grow", "nGrow", 0, 50, 0, 13),
            ("layer_feature_angle", "layer featureAngle", 0.0, 180.0, 2, 14),
            ("slip_feature_angle", "slipFeatureAngle", 0.0, 180.0, 2, 15),
            ("layer_n_relax_iter", "layer nRelaxIter", 0, 50, 0, 16),
            ("n_smooth_surface_normals", "nSmoothSurfaceNormals", 0, 50, 0, 17),
            ("n_smooth_normals", "nSmoothNormals", 0, 50, 0, 18),
            ("n_smooth_thickness", "nSmoothThickness", 0, 100, 0, 19),
            ("max_face_thickness_ratio", "maxFaceThicknessRatio", 0.0, 2.0, 3, 20),
            ("max_thickness_to_medial_ratio", "maxThicknessToMedialRatio", 0.0, 2.0, 3, 21),
            ("min_medial_axis_angle", "minMedialAxisAngle", 0.0, 180.0, 2, 22),
            ("n_buffer_cells_no_extrude", "nBufferCellsNoExtrude", 0, 50, 0, 23),
            ("n_layer_iter", "nLayerIter", 1, 200, 0, 24),
            ("merge_tolerance", "mergeTolerance", 1.0e-10, 1.0e-2, 10, 25),
        ]
        for key, label, mn, mx, dec, row in cfg:
            spin = QDoubleSpinBox(box)
            spin.setRange(float(mn), float(mx))
            spin.setDecimals(int(dec))
            spin.setMaximumWidth(120)
            if int(dec) == 0:
                spin.setSingleStep(1.0)
            self.snappy_spin[key] = spin
            
            layout.addWidget(QLabel(label), row, 0)
            spin_layout = QHBoxLayout()
            spin_layout.addWidget(spin)
            spin_layout.addWidget(create_help_button(label.replace(" ", "_"), box))
            spin_layout.addStretch()
            layout.addLayout(spin_layout, row, 1, 1, 1)
            
            spin.valueChanged.connect(lambda v, k=key: self._on_snappy_scalar_changed(k, v))

        self.chk_implicit_snap = QCheckBox("implicitFeatureSnap", box)
        self.chk_explicit_snap = QCheckBox("explicitFeatureSnap", box)
        self.chk_multi_region_snap = QCheckBox("multiRegionFeatureSnap", box)
        self.chk_allow_free_faces = QCheckBox("allowFreeStandingZoneFaces", box)
        
        implicit_layout = QHBoxLayout()
        implicit_layout.addWidget(self.chk_implicit_snap)
        implicit_layout.addWidget(create_help_button("implicitFeatureSnap", box))
        implicit_layout.addStretch()
        
        explicit_layout = QHBoxLayout()
        explicit_layout.addWidget(self.chk_explicit_snap)
        explicit_layout.addWidget(create_help_button("explicitFeatureSnap", box))
        explicit_layout.addStretch()
        
        multi_layout = QHBoxLayout()
        multi_layout.addWidget(self.chk_multi_region_snap)
        multi_layout.addWidget(create_help_button("multiRegionFeatureSnap", box))
        multi_layout.addStretch()
        
        allow_layout = QHBoxLayout()
        allow_layout.addWidget(self.chk_allow_free_faces)
        allow_layout.addWidget(create_help_button("allowFreeStandingZoneFaces", box))
        allow_layout.addStretch()
        
        layout.addLayout(implicit_layout, 26, 0)
        layout.addLayout(explicit_layout, 26, 1)
        layout.addLayout(multi_layout, 26, 2)
        layout.addLayout(allow_layout, 27, 0, 1, 2)

        self.chk_refinement_region = QCheckBox("Enable refinementBox", box)
        refinement_layout = QHBoxLayout()
        refinement_layout.addWidget(self.chk_refinement_region)
        refinement_layout.addWidget(create_help_button("refinementBox_enable", box))
        refinement_layout.addStretch()
        layout.addLayout(refinement_layout, 28, 0, 1, 1)
        
        self.refinement_region_spin = {}
        region_cfg = [
            ("min_x", "Refine Min X", -9999.0, 9999.0, 4, 29),
            ("min_y", "Refine Min Y", -9999.0, 9999.0, 4, 30),
            ("min_z", "Refine Min Z", -9999.0, 9999.0, 4, 31),
            ("max_x", "Refine Max X", -9999.0, 9999.0, 4, 32),
            ("max_y", "Refine Max Y", -9999.0, 9999.0, 4, 33),
            ("max_z", "Refine Max Z", -9999.0, 9999.0, 4, 34),
        ]
        for key, label, mn, mx, dec, row in region_cfg:
            spin = QDoubleSpinBox(box)
            spin.setRange(float(mn), float(mx))
            spin.setDecimals(int(dec))
            spin.setMaximumWidth(120)
            self.refinement_region_spin[key] = spin
            layout.addWidget(QLabel(label), row, 0)
            spin_layout = QHBoxLayout()
            spin_layout.addWidget(spin)
            spin_layout.addWidget(create_help_button(label.replace(" ", "_"), box))
            spin_layout.addStretch()
            layout.addLayout(spin_layout, row, 1, 1, 1)
            spin.valueChanged.connect(lambda v, k=key: self._on_refinement_region_scalar_changed(k, v))
        
        self.spin_refinement_level = QSpinBox(box)
        self.spin_refinement_level.setRange(0, 10)
        self.spin_refinement_level.setMaximumWidth(100)
        level_layout = QHBoxLayout()
        level_layout.addWidget(self.spin_refinement_level)
        level_layout.addWidget(create_help_button("refinement_level", box))
        level_layout.addStretch()
        layout.addWidget(QLabel("Refine Level"), 35, 0)
        layout.addLayout(level_layout, 35, 1, 1, 1)

        self.cmb_snappy_profile.currentTextChanged.connect(self._on_snappy_profile_changed)
        self.cmb_snappy_parallel.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("mesh.snappy_parallel_mode", str(t))
        )
        self.chk_castellated.toggled.connect(lambda v: self._set_openfoam_value("mesh.castellated", bool(v)))
        self.chk_snap.toggled.connect(lambda v: self._set_openfoam_value("mesh.snap", bool(v)))
        self.chk_layers.toggled.connect(lambda v: self._set_openfoam_value("mesh.layers", bool(v)))
        self.spin_ref_min.valueChanged.connect(lambda v: self._set_openfoam_value("mesh.refinement_min", int(v)))
        self.spin_ref_max.valueChanged.connect(lambda v: self._set_openfoam_value("mesh.refinement_max", int(v)))
        self.spin_feature_angle.valueChanged.connect(lambda v: self._set_openfoam_value("mesh.feature_angle", float(v)))
        self.spin_layers.valueChanged.connect(lambda v: self._set_openfoam_value("mesh.n_surface_layers", int(v)))
        self.chk_implicit_snap.toggled.connect(lambda v: self._set_openfoam_value("mesh.implicit_feature_snap", bool(v)))
        self.chk_explicit_snap.toggled.connect(lambda v: self._set_openfoam_value("mesh.explicit_feature_snap", bool(v)))
        self.chk_multi_region_snap.toggled.connect(lambda v: self._set_openfoam_value("mesh.multi_region_feature_snap", bool(v)))
        self.chk_allow_free_faces.toggled.connect(lambda v: self._set_openfoam_value("mesh.allow_free_standing_zone_faces", bool(v)))
        self.chk_refinement_region.toggled.connect(self._on_refinement_region_enabled)
        self.spin_refinement_level.valueChanged.connect(self._on_refinement_region_level_changed)
        return box

    def _build_checkmesh_panel(self):
        box = QGroupBox("CheckMesh")
        layout = QFormLayout(box)
        self.chk_checkmesh_enabled = QCheckBox("Run checkMesh in helper script", box)
        self.spin_max_non_ortho = QDoubleSpinBox(box)
        self.spin_max_non_ortho.setRange(0.0, 180.0)
        self.spin_max_non_ortho.setDecimals(2)
        self.spin_max_skew = QDoubleSpinBox(box)
        self.spin_max_skew.setRange(0.0, 100.0)
        self.spin_max_skew.setDecimals(2)
        self.spin_min_vol = QDoubleSpinBox(box)
        self.spin_min_vol.setRange(0.0, 1.0)
        self.spin_min_vol.setDecimals(8)
        self.spin_min_vol.setSingleStep(1e-6)
        layout.addRow(self.chk_checkmesh_enabled)
        layout.addRow("maxNonOrtho", self.spin_max_non_ortho)
        layout.addRow("maxBoundarySkewness", self.spin_max_skew)
        layout.addRow("minVol", self.spin_min_vol)
        self.chk_checkmesh_enabled.toggled.connect(lambda v: self._set_openfoam_value("check_mesh.enabled", bool(v)))
        self.spin_max_non_ortho.valueChanged.connect(lambda v: self._set_openfoam_value("check_mesh.max_non_ortho", float(v)))
        self.spin_max_skew.valueChanged.connect(lambda v: self._set_openfoam_value("check_mesh.max_boundary_skewness", float(v)))
        self.spin_min_vol.valueChanged.connect(lambda v: self._set_openfoam_value("check_mesh.min_vol", float(v)))
        
        # Mesh Quality Visualization Section
        layout.addRow(QLabel("─" * 50))
        layout.addRow(QLabel("<b>Visualization</b>"))
        
        # Toggle visualization
        self.chk_viz_quality = QCheckBox("Show Mesh Quality in Viewer", box)
        layout.addRow(self.chk_viz_quality)
        self.chk_viz_quality.toggled.connect(self._on_quality_viz_toggled)
        
        # Quality metric selector
        self.cmb_quality_field = QComboBox(box)
        self.cmb_quality_field.addItems([
            "non_ortho",
            "skewness",
            "min_volume",
            "pyramid_volume",
            "tet_quality",
            "concavity",
            "face_twist",
            "determinant",
            "interp_weight",
            "volume_ratio",
        ])
        self.cmb_quality_field.setCurrentText("non_ortho")
        layout.addRow("Metric", self.cmb_quality_field)
        self.cmb_quality_field.currentTextChanged.connect(self._on_quality_field_changed)
        
        # Visualization mode
        self.cmb_quality_mode = QComboBox(box)
        self.cmb_quality_mode.addItems(["Gradient", "Isolated Bad Cells"])
        layout.addRow("Mode", self.cmb_quality_mode)
        self.cmb_quality_mode.currentTextChanged.connect(self._on_quality_mode_changed)
        
        # Severity slider
        self.spin_quality_severity = QDoubleSpinBox(box)
        self.spin_quality_severity.setRange(0.5, 2.0)
        self.spin_quality_severity.setValue(1.0)
        self.spin_quality_severity.setSingleStep(0.1)
        self.spin_quality_severity.setDecimals(1)
        layout.addRow("Severity (isolated mode)", self.spin_quality_severity)
        self.spin_quality_severity.valueChanged.connect(lambda v: self._set_mesh_quality_severity(v))
        
        # Violation count label
        self.lbl_quality_count = QLabel("No quality data loaded")
        self.lbl_quality_count.setStyleSheet("color: #999; font-size: 10px;")
        layout.addRow("Status", self.lbl_quality_count)
        
        # Mesh Advice Button
        layout.addRow(QLabel("─" * 50))
        self.btn_mesh_advice = QPushButton("💡 Show Mesh Advice", box)
        self.btn_mesh_advice.setToolTip("View mesh quality warnings and recommendations")
        self.btn_mesh_advice.clicked.connect(self.show_mesh_advice)
        layout.addRow(self.btn_mesh_advice)
        
        return box

    def _on_quality_viz_toggled(self, enabled):
        """Handle mesh quality visualization toggle."""
        self._toggle_mesh_quality_visualization(enabled)
        self._update_quality_status_label()

    def _on_quality_field_changed(self, field_name):
        """Handle quality metric field change."""
        self._set_mesh_quality_field(field_name.lower().strip())
        self._update_quality_status_label()

    def _on_quality_mode_changed(self, mode_text):
        """Handle visualization mode change."""
        mode = "isolated" if "Isolated" in mode_text else "gradient"
        self._set_mesh_quality_mode(mode)
        self._update_quality_status_label()

    def _on_quality_render_mode_changed(self, mode_text):
        """Handle render mode change (smooth/mesh)."""
        mode_map = {
            "Smooth": "smooth",
            "Mesh": "mesh",
            "Smooth + Mesh": "smooth+mesh",
        }
        mode = mode_map.get(mode_text, "smooth")
        self._set_mesh_quality_render_mode(mode)
        self._update_quality_status_label()

    def _on_quality_opacity_changed(self, opacity_text):
        """Handle opacity change (high/low)."""
        opacity_map = {
            "High": "high",
            "Low": "low",
        }
        opacity = opacity_map.get(opacity_text, "high")
        self._set_mesh_quality_opacity(opacity)
        self._update_quality_status_label()

    def _update_quality_status_label(self):
        """Update the quality visualization status label."""
        if not self._mesh_quality_visibility:
            self.lbl_quality_count.setText("Visualization: OFF")
            self.lbl_quality_count.setStyleSheet("color: #999; font-size: 10px;")
        elif self._mesh_quality_data is None:
            self.lbl_quality_count.setText("No quality data loaded")
            self.lbl_quality_count.setStyleSheet("color: #999; font-size: 10px;")
        else:
            violations = self._mesh_quality_data.get("violation_counts", {})
            field = self._mesh_quality_field
            count = violations.get(field, 0)
            self.lbl_quality_count.setText(f"Violations: {count} | Mode: {self._mesh_quality_mode}")
            color = "#ff6666" if count > 0 else "#66ff66"
            self.lbl_quality_count.setStyleSheet(f"color: {color}; font-size: 10px;")

    def _build_bc_panel(self):
        box = QGroupBox("Boundary Conditions")
        layout = QVBoxLayout(box)
        patch_grid = QGridLayout()
        self.patch_enabled = {}
        self.patch_type = {}
        for row, patch in enumerate(FLOW_PATCHES):
            chk = QCheckBox(patch, box)
            cmb = QComboBox(box)
            cmb.addItems(PATCH_TYPES)
            self.patch_enabled[patch] = chk
            self.patch_type[patch] = cmb
            patch_grid.addWidget(chk, row, 0)
            patch_grid.addWidget(cmb, row, 1)
            chk.toggled.connect(lambda v, p=patch: self._on_patch_enabled_changed(p, v))
            cmb.currentTextChanged.connect(lambda txt, p=patch: self._on_patch_type_changed(p, txt))
        layout.addLayout(patch_grid)
        row = QHBoxLayout()
        self.cmb_bc_field = QComboBox(box)
        self.cmb_bc_field.addItems(CFD_FIELDS)
        self.btn_reset_bc = QPushButton("Reset BC Template", box)
        row.addWidget(QLabel("Field", box))
        row.addWidget(self.cmb_bc_field)
        row.addWidget(self.btn_reset_bc)
        layout.addLayout(row)
        self.cmb_bc_field.currentTextChanged.connect(self._sync_bc_field_widgets)
        self.btn_reset_bc.clicked.connect(self._reset_boundary_templates)
        preview_row = QHBoxLayout()
        self.cmb_preview_patch = QComboBox(box)
        self.cmb_preview_patch.addItems(["(None)"] + FLOW_PATCHES)
        preview_row.addWidget(QLabel("Preview Patch", box))
        preview_row.addWidget(self.cmb_preview_patch)
        layout.addLayout(preview_row)
        self.cmb_preview_patch.currentTextChanged.connect(self._on_preview_patch_changed)
        self.bc_type_widgets = {}
        self.bc_value_widgets = {}
        form = QFormLayout()
        for patch in FLOW_PATCHES:
            inner = QWidget(box)
            inner_layout = QHBoxLayout(inner)
            inner_layout.setContentsMargins(0, 0, 0, 0)
            cmb = QComboBox(inner)
            cmb.setEditable(True)
            val = QLineEdit(inner)
            self.bc_type_widgets[patch] = cmb
            self.bc_value_widgets[patch] = val
            inner_layout.addWidget(cmb)
            inner_layout.addWidget(val)
            form.addRow(f"{patch}", inner)
            cmb.currentTextChanged.connect(lambda txt, p=patch: self._on_bc_entry_changed(p, "type", txt))
            val.editingFinished.connect(lambda p=patch, w=val: self._on_bc_entry_changed(p, "value", w.text()))
        layout.addLayout(form)
        return box

    def _build_sim_panel(self):
        box = QGroupBox("Simulation Control")
        layout = QFormLayout(box)
        self.cmb_solver = QComboBox(box)
        self.cmb_solver.addItems(["simpleFoam", "potentialFoam"])
        self.spin_start = QDoubleSpinBox(box)
        self.spin_end = QDoubleSpinBox(box)
        self.spin_dt = QDoubleSpinBox(box)
        self.spin_write_interval = QDoubleSpinBox(box)
        for spin in (self.spin_start, self.spin_end, self.spin_dt, self.spin_write_interval):
            spin.setRange(0.0, 1.0e12)
            spin.setDecimals(6)
        self.spin_purge = QSpinBox(box)
        self.spin_purge.setRange(0, 10000)
        self.chk_pseudo_transient = QCheckBox("Pseudo transient (steady runs)", box)
        self.chk_use_parallel = QCheckBox("Run in parallel (MPI)", box)
        self.spin_mpi_cores = QSpinBox(box)
        self.spin_mpi_cores.setRange(1, 1024)
        layout.addRow("Solver", self.cmb_solver)
        layout.addRow("startTime", self.spin_start)
        layout.addRow("endTime", self.spin_end)
        layout.addRow("deltaT", self.spin_dt)
        layout.addRow("writeInterval", self.spin_write_interval)
        layout.addRow("purgeWrite", self.spin_purge)
        layout.addRow(self.chk_pseudo_transient)
        layout.addRow(self.chk_use_parallel)
        layout.addRow("MPI Cores", self.spin_mpi_cores)
        self.cmb_solver.currentTextChanged.connect(self._on_solver_changed)
        self.spin_start.valueChanged.connect(lambda v: self._set_openfoam_value("simulation.start_time", float(v)))
        self.spin_end.valueChanged.connect(lambda v: self._set_openfoam_value("simulation.end_time", float(v)))
        self.spin_dt.valueChanged.connect(lambda v: self._set_openfoam_value("simulation.delta_t", float(v)))
        self.spin_write_interval.valueChanged.connect(lambda v: self._set_openfoam_value("simulation.write_interval", float(v)))
        self.spin_purge.valueChanged.connect(lambda v: self._set_openfoam_value("simulation.purge_write", int(v)))
        self.chk_pseudo_transient.toggled.connect(lambda v: self._set_openfoam_value("simulation.pseudo_transient", bool(v)))
        self.chk_use_parallel.toggled.connect(lambda v: self._set_openfoam_value("simulation.use_parallel", bool(v)))
        self.spin_mpi_cores.valueChanged.connect(lambda v: self._set_openfoam_value("simulation.mpi_cores", int(v)))
        return box

    def _build_numerics_panel(self):
        box = QGroupBox("Numerics")
        layout = QFormLayout(box)
        self.cmb_fv_schemes = QComboBox(box)
        self.cmb_fv_schemes.addItems(["bounded steady RANS", "potentialFoam basic"])
        self.cmb_fv_solution = QComboBox(box)
        self.cmb_fv_solution.addItems(["SIMPLE-RANS", "Potential"])
        self.cmb_turb_model = QComboBox(box)
        self.cmb_turb_model.addItems(["kOmegaSST", "kEpsilon", "SpalartAllmaras"])
        self.spin_u_tol = QDoubleSpinBox(box)
        self.spin_p_tol = QDoubleSpinBox(box)
        self.spin_u_relax = QDoubleSpinBox(box)
        self.spin_p_relax = QDoubleSpinBox(box)
        for spin in (self.spin_u_tol, self.spin_p_tol, self.spin_u_relax, self.spin_p_relax):
            spin.setDecimals(8)
            spin.setRange(0.0, 1.0)
        self.spin_u_tol.setRange(1e-12, 1.0)
        self.spin_p_tol.setRange(1e-12, 1.0)
        layout.addRow("fvSchemes Preset", self.cmb_fv_schemes)
        layout.addRow("fvSolution Preset", self.cmb_fv_solution)
        layout.addRow("Turbulence Model", self.cmb_turb_model)
        layout.addRow("U Solver Tolerance", self.spin_u_tol)
        layout.addRow("p Solver Tolerance", self.spin_p_tol)
        layout.addRow("U Relaxation", self.spin_u_relax)
        layout.addRow("p Relaxation", self.spin_p_relax)
        self.cmb_fv_schemes.currentTextChanged.connect(self._on_fv_schemes_preset_changed)
        self.cmb_fv_solution.currentTextChanged.connect(self._on_fv_solution_preset_changed)
        self.cmb_turb_model.currentTextChanged.connect(lambda t: self._set_openfoam_value("numerics.turbulence_model", t))
        self.spin_u_tol.valueChanged.connect(lambda v: self._set_openfoam_value("numerics.u_solver_tol", float(v)))
        self.spin_p_tol.valueChanged.connect(lambda v: self._set_openfoam_value("numerics.p_solver_tol", float(v)))
        self.spin_u_relax.valueChanged.connect(lambda v: self._set_openfoam_value("numerics.u_relax", float(v)))
        self.spin_p_relax.valueChanged.connect(lambda v: self._set_openfoam_value("numerics.p_relax", float(v)))

        fv_box = QGroupBox("fvSchemes", box)
        fv_layout = QFormLayout(fv_box)
        self.cmb_ddt_default = QComboBox(fv_box)
        self.cmb_ddt_default.addItems(["steadyState", "Euler", "backward", "CrankNicolson 0.9"])
        self.cmb_grad_default = QComboBox(fv_box)
        self.cmb_grad_default.addItems(["Gauss linear", "leastSquares", "fusedGauss linear", "none"])
        self.cmb_div_phi_u = QComboBox(fv_box)
        self.cmb_div_phi_u.addItems(
            [
                "bounded Gauss upwind",
                "bounded Gauss linearUpwind grad(U)",
                "Gauss linearUpwind grad(U)",
                "Gauss upwind",
                "Gauss linear",
                "bounded Gauss limitedLinear 1",
            ]
        )
        self.cmb_div_phi_turb = QComboBox(fv_box)
        self.cmb_div_phi_turb.addItems(["bounded Gauss upwind", "Gauss upwind", "Gauss limitedLinear 1"])
        self.cmb_laplacian_default = QComboBox(fv_box)
        self.cmb_laplacian_default.addItems(
            [
                "Gauss linear corrected",
                "Gauss linear uncorrected",
                "Gauss linear limited 0.333",
                "Gauss linear orthogonal",
                "fusedGauss linear corrected",
            ]
        )
        self.cmb_interpolation_default = QComboBox(fv_box)
        self.cmb_interpolation_default.addItems(["linear", "skewCorrected linear"])
        self.cmb_sn_grad_default = QComboBox(fv_box)
        self.cmb_sn_grad_default.addItems(["corrected", "uncorrected", "limited 0.333", "limited corrected 0.33", "orthogonal"])
        self.cmb_wall_dist_method = QComboBox(fv_box)
        self.cmb_wall_dist_method.addItems(["meshWave", "Poisson", "advectionDiffusion", "exactDistance"])
        fv_layout.addRow("ddtSchemes/default", self.cmb_ddt_default)
        fv_layout.addRow("gradSchemes/default", self.cmb_grad_default)
        fv_layout.addRow("divSchemes/div(phi,U)", self.cmb_div_phi_u)
        fv_layout.addRow("divSchemes/turbulence", self.cmb_div_phi_turb)
        fv_layout.addRow("laplacianSchemes/default", self.cmb_laplacian_default)
        fv_layout.addRow("interpolationSchemes/default", self.cmb_interpolation_default)
        fv_layout.addRow("snGradSchemes/default", self.cmb_sn_grad_default)
        fv_layout.addRow("wallDist/method", self.cmb_wall_dist_method)
        layout.addRow(fv_box)

        self.cmb_ddt_default.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("numerics.fv_schemes.ddt_default", t)
        )
        self.cmb_grad_default.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("numerics.fv_schemes.grad_default", t)
        )
        self.cmb_div_phi_u.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("numerics.fv_schemes.div_phi_u", t)
        )
        self.cmb_div_phi_turb.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("numerics.fv_schemes.div_phi_turb", t)
        )
        self.cmb_laplacian_default.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("numerics.fv_schemes.laplacian_default", t)
        )
        self.cmb_interpolation_default.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("numerics.fv_schemes.interpolation_default", t)
        )
        self.cmb_sn_grad_default.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("numerics.fv_schemes.sn_grad_default", t)
        )
        self.cmb_wall_dist_method.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("numerics.fv_schemes.wall_dist_method", t)
        )

        sol_box = QGroupBox("fvSolution", box)
        sol_layout = QFormLayout(sol_box)
        self.cmb_p_solver = QComboBox(sol_box)
        self.cmb_p_solver.addItems(["GAMG", "PCG", "PBiCGStab", "smoothSolver"])
        self.cmb_p_smoother = QComboBox(sol_box)
        self.cmb_p_smoother.addItems(["GaussSeidel", "DIC", "DICGaussSeidel", "symGaussSeidel"])
        self.cmb_p_preconditioner = QComboBox(sol_box)
        self.cmb_p_preconditioner.addItems(["DIC", "DILU", "FDIC", "ShermanMorrison"])
        self.spin_p_rel_tol = QDoubleSpinBox(sol_box)
        self.spin_p_rel_tol.setDecimals(8)
        self.spin_p_rel_tol.setRange(0.0, 1.0)
        self.cmb_u_solver = QComboBox(sol_box)
        self.cmb_u_solver.addItems(["smoothSolver", "PBiCGStab", "PCG"])
        self.cmb_u_smoother = QComboBox(sol_box)
        self.cmb_u_smoother.addItems(["symGaussSeidel", "GaussSeidel", "DILU"])
        self.cmb_u_preconditioner = QComboBox(sol_box)
        self.cmb_u_preconditioner.addItems(["DILU", "DIC", "FDIC", "ShermanMorrison"])
        self.spin_u_rel_tol = QDoubleSpinBox(sol_box)
        self.spin_u_rel_tol.setDecimals(8)
        self.spin_u_rel_tol.setRange(0.0, 1.0)
        self.spin_simple_non_ortho = QSpinBox(sol_box)
        self.spin_simple_non_ortho.setRange(0, 100)
        self.chk_simple_consistent = QCheckBox("consistent", sol_box)
        self.spin_residual_p = QDoubleSpinBox(sol_box)
        self.spin_residual_u = QDoubleSpinBox(sol_box)
        for spin in (self.spin_residual_p, self.spin_residual_u):
            spin.setDecimals(8)
            spin.setRange(0.0, 1.0)
        self.spin_residual_p.setRange(1e-12, 1.0)
        self.spin_residual_u.setRange(1e-12, 1.0)

        sol_layout.addRow("p/solver", self.cmb_p_solver)
        sol_layout.addRow("p/smoother", self.cmb_p_smoother)
        sol_layout.addRow("p/preconditioner", self.cmb_p_preconditioner)
        sol_layout.addRow("p/relTol", self.spin_p_rel_tol)
        sol_layout.addRow("U/solver", self.cmb_u_solver)
        sol_layout.addRow("U/smoother", self.cmb_u_smoother)
        sol_layout.addRow("U/preconditioner", self.cmb_u_preconditioner)
        sol_layout.addRow("U/relTol", self.spin_u_rel_tol)
        sol_layout.addRow("SIMPLE nNonOrthogonalCorrectors", self.spin_simple_non_ortho)
        sol_layout.addRow("SIMPLE consistent", self.chk_simple_consistent)
        sol_layout.addRow("residualControl/p", self.spin_residual_p)
        sol_layout.addRow("residualControl/U", self.spin_residual_u)
        layout.addRow(sol_box)

        self.cmb_p_solver.currentTextChanged.connect(self._on_p_solver_changed)
        self.cmb_p_smoother.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("numerics.fv_solution.p_smoother", t)
        )
        self.cmb_p_preconditioner.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("numerics.fv_solution.p_preconditioner", t)
        )
        self.spin_p_rel_tol.valueChanged.connect(
            lambda v: self._set_openfoam_value("numerics.fv_solution.p_rel_tol", float(v))
        )
        self.cmb_u_solver.currentTextChanged.connect(self._on_u_solver_changed)
        self.cmb_u_smoother.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("numerics.fv_solution.u_smoother", t)
        )
        self.cmb_u_preconditioner.currentTextChanged.connect(
            lambda t: self._set_openfoam_value("numerics.fv_solution.u_preconditioner", t)
        )
        self.spin_u_rel_tol.valueChanged.connect(
            lambda v: self._set_openfoam_value("numerics.fv_solution.u_rel_tol", float(v))
        )
        self.spin_simple_non_ortho.valueChanged.connect(
            lambda v: self._set_openfoam_value("numerics.fv_solution.simple_n_non_ortho", int(v))
        )
        self.chk_simple_consistent.toggled.connect(
            lambda v: self._set_openfoam_value("numerics.fv_solution.simple_consistent", bool(v))
        )
        self.spin_residual_p.valueChanged.connect(
            lambda v: self._set_openfoam_value("numerics.fv_solution.residual_control_p", float(v))
        )
        self.spin_residual_u.valueChanged.connect(
            lambda v: self._set_openfoam_value("numerics.fv_solution.residual_control_u", float(v))
        )
        return box

    def _build_post_process_panel(self):
        box = QGroupBox("Post Process")
        layout = QVBoxLayout(box)
        self.input_paraview_path = QLineEdit(box)
        self.btn_pick_paraview_path = QPushButton("Browse...", box)
        self.btn_open_paraview = QPushButton("Open in ParaView", box)
        self.btn_scan_post_fields = QPushButton("Scan Case Fields", box)
        self.lbl_post_status = QLabel("No case scanned.", box)
        self.lbl_post_status.setWordWrap(True)
        self.cmb_vtk_mesh = QComboBox(box)
        self.cmb_vtk_mesh.addItems(["snappy"])
        self.btn_export_vtk = QPushButton("Export VTK", box)
        self.btn_load_vtk = QPushButton("Load VTK", box)
        self.lbl_vtk_status = QLabel("VTK: not exported", box)
        self.lbl_vtk_status.setWordWrap(True)
        self.btn_load_pressure_data_post = QPushButton("Load Pressure Data", box)
        self.btn_clear_pressure_data_post = QPushButton("Clear Pressure Data", box)
        self.btn_clear_pressure_data_post.setEnabled(False)
        paraview_row = QHBoxLayout()
        paraview_row.addWidget(self.input_paraview_path, 1)
        paraview_row.addWidget(self.btn_pick_paraview_path)
        target_row = QHBoxLayout()
        target_row.addWidget(QLabel("VTK Target", box))
        target_row.addWidget(self.cmb_vtk_mesh, 1)
        btn_row = QHBoxLayout()
        btn_row.addWidget(self.btn_export_vtk)
        btn_row.addWidget(self.btn_load_vtk)
        pressure_row = QHBoxLayout()
        pressure_row.addWidget(self.btn_load_pressure_data_post)
        pressure_row.addWidget(self.btn_clear_pressure_data_post)
        layout.addWidget(QLabel("ParaView Path", box))
        layout.addLayout(paraview_row)
        layout.addWidget(self.btn_open_paraview)
        layout.addWidget(self.btn_scan_post_fields)
        layout.addWidget(self.lbl_post_status)
        layout.addLayout(target_row)
        layout.addLayout(btn_row)
        layout.addWidget(self.lbl_vtk_status)
        layout.addSpacing(10)
        layout.addLayout(pressure_row)
        self.input_paraview_path.editingFinished.connect(self._sync_paraview_path_from_input)
        self.btn_pick_paraview_path.clicked.connect(self.pick_paraview_path)
        self.btn_open_paraview.clicked.connect(self.open_paraview_from_ui)
        self.btn_scan_post_fields.clicked.connect(self.scan_post_process_case)
        self.btn_export_vtk.clicked.connect(self.export_vtk_from_ui)
        self.btn_load_vtk.clicked.connect(self.load_vtk_from_ui)
        self.btn_load_pressure_data_post.clicked.connect(self.load_pressure_csv_from_dialog)
        self.btn_clear_pressure_data_post.clicked.connect(self.clear_pressure_plot)
        return box

    def _build_solve_mesh_panel(self):
        """Build the Solve Mesh panel with mesh execution commands."""
        box = QGroupBox("Solve Mesh", self.of_task_root)
        layout = QVBoxLayout(box)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)
        
        # Helper script options
        self.chk_write_scripts = QCheckBox("Write helper scripts", box)
        self.chk_surface_feature_extract = QCheckBox("Include surfaceFeatureExtract command", box)
        layout.addWidget(self.chk_write_scripts)
        layout.addWidget(self.chk_surface_feature_extract)
        
        # Mesh execution buttons
        self.btn_preview_files = QPushButton("Preview Files", box)
        self.btn_update_case = QPushButton("Update Case", box)
        self.btn_run_pipeline = QPushButton("Run Full Pipeline", box)
        self.btn_run_domain_mesh = QPushButton("Run Domain Mesh", box)
        self.btn_run_surface_features = QPushButton("Run Surface Features", box)
        self.btn_run_snappy_mesh = QPushButton("Run SnappyHexMesh", box)
        self.btn_run_checkmesh = QPushButton("Run CheckMesh", box)
        
        layout.addWidget(self.btn_preview_files)
        layout.addWidget(self.btn_update_case)
        
        # Mesh execution grid
        mesh_grid = QGridLayout()
        mesh_grid.setSpacing(4)
        mesh_grid.addWidget(self.btn_run_pipeline, 0, 0, 1, 2)
        mesh_grid.addWidget(self.btn_run_domain_mesh, 1, 0)
        mesh_grid.addWidget(self.btn_run_surface_features, 1, 1)
        mesh_grid.addWidget(self.btn_run_snappy_mesh, 2, 0)
        mesh_grid.addWidget(self.btn_run_checkmesh, 2, 1)
        layout.addLayout(mesh_grid)
        
        layout.addStretch(1)
        
        # Signal connections
        self.chk_write_scripts.toggled.connect(lambda v: self._set_openfoam_value("scripts.write_helper_scripts", bool(v)))
        self.chk_surface_feature_extract.toggled.connect(
            lambda v: self._set_openfoam_value("scripts.include_surface_feature_extract", bool(v))
        )
        self.btn_preview_files.clicked.connect(self._preview_case_files)
        self.btn_update_case.clicked.connect(self.update_openfoam_case_from_ui)
        self.btn_run_pipeline.clicked.connect(self.run_openfoam_pipeline)
        self.btn_run_domain_mesh.clicked.connect(lambda: self.run_openfoam_stage("domain_mesh"))
        self.btn_run_surface_features.clicked.connect(lambda: self.run_openfoam_stage("surface_features"))
        self.btn_run_snappy_mesh.clicked.connect(lambda: self.run_openfoam_stage("snappy_mesh"))
        self.btn_run_checkmesh.clicked.connect(lambda: self.run_openfoam_stage("check_mesh"))
        
        return box

    def _build_export_panel(self):
        """Build the Solve panel with solver-only execution commands."""
        box = QGroupBox("Solve")
        layout = QFormLayout(box)
        
        # Solver execution buttons (Run Solve, Run Post only)
        self.btn_run_solve = QPushButton("Run Solve", box)
        self.btn_run_post = QPushButton("Run Post", box)
        self.btn_cancel_run = QPushButton("Cancel", box)
        self.btn_open_convergence_plot = QPushButton("Open Convergence Plot", box)
        
        # Convergence and status labels
        self.lbl_run_status = QLabel("Status: idle", box)
        self.lbl_force_coeffs = QLabel("CL/CD/CM: n/a", box)
        self.lbl_export_status = QLabel("", box)
        
        # Solver execution grid
        run_row = QWidget(box)
        run_layout = QGridLayout(run_row)
        run_layout.setContentsMargins(0, 0, 0, 0)
        run_layout.addWidget(self.btn_run_solve, 0, 0)
        run_layout.addWidget(self.btn_run_post, 0, 1)
        run_layout.addWidget(self.btn_cancel_run, 1, 0, 1, 2)
        
        layout.addRow("Execution", run_row)
        layout.addRow(self.btn_open_convergence_plot)
        layout.addRow("Run Status", self.lbl_run_status)
        layout.addRow("Coefficients", self.lbl_force_coeffs)
        layout.addRow("Status", self.lbl_export_status)
        
        # Signal connections
        self.btn_run_solve.clicked.connect(lambda: self.run_openfoam_stage("solve"))
        self.btn_run_post.clicked.connect(lambda: self.run_openfoam_stage("post"))
        self.btn_cancel_run.clicked.connect(self.cancel_openfoam_run)
        self.btn_cancel_run.setEnabled(False)
        self.btn_open_convergence_plot.clicked.connect(self.open_convergence_plot)
        if not _MATPLOTLIB_AVAILABLE:
            self.btn_open_convergence_plot.setEnabled(False)
        
        return box
