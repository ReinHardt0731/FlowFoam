from ._controller_common import *

class BoundaryConditionMixin:
    def _current_field_key(self):
        if self.current_data is None or not hasattr(self, "field_selector"):
            return None
        display = self.field_selector.currentText()
        return self.field_key_map.get(display)

    def _on_preview_patch_changed(self, patch_name):
        name = str(patch_name or "").strip()
        self._highlight_patch = None if name in ("", "(None)") else name
        self._refresh_viewer_scene()

    def _add_selected_patch_overlay(self, dmin, dmax, surface_mesh):
        patch = self._highlight_patch
        if not patch:
            return
        style = self._viewer_lighting_kwargs()

        x0, y0, z0 = float(dmin[0]), float(dmin[1]), float(dmin[2])
        x1, y1, z1 = float(dmax[0]), float(dmax[1]), float(dmax[2])

        def add_face(points, color="#00ccff", opacity=0.35):
            # Build a single quad exactly on the blockMesh face.
            arr = np.array(points, dtype=float)
            faces = np.hstack([[4, 0, 1, 2, 3]])
            quad = pv.PolyData(arr, faces)
            self.viewer_plotter.add_mesh(quad, color=color, opacity=opacity, show_edges=False, **style)

        if patch == "aircraft" and surface_mesh is not None:
            self.viewer_plotter.add_mesh(surface_mesh, color="#ff5555", opacity=0.9, show_edges=True, **style)
            return
        if patch == "inlet":
            add_face([(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], opacity=0.45)
            return
        if patch == "outlet":
            add_face([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], opacity=0.45)
            return
        if patch == "farfield":
            add_face([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], opacity=0.25)  # y min
            add_face([(x0, y1, z0), (x0, y1, z1), (x1, y1, z1), (x1, y1, z0)], opacity=0.25)  # y max
            add_face([(x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (x1, y0, z0)], opacity=0.25)  # z min
            add_face([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], opacity=0.25)  # z max
            return
        if patch == "symmetry":
            y_mid = 0.5 * (y0 + y1)
            add_face([(x0, y_mid, z0), (x0, y_mid, z1), (x1, y_mid, z1), (x1, y_mid, z0)], opacity=0.35)
            return

    def _on_patch_enabled_changed(self, patch, enabled):
        self._set_openfoam_value(f"boundary_conditions.patches.{patch}.enabled", bool(enabled))
        self._sync_bc_field_widgets()

    def _on_patch_type_changed(self, patch, patch_type):
        self._set_openfoam_value(f"boundary_conditions.patches.{patch}.type", patch_type)

    def _reset_boundary_templates(self):
        workflow = self.openfoam.get("workflow", "simpleFoam")
        self._set_openfoam_value("boundary_conditions", bootstrap_boundary_conditions(workflow))
        self._sync_widgets_from_state()

    def _on_bc_entry_changed(self, patch, key, value):
        field = self.cmb_bc_field.currentText()
        self._set_openfoam_value(f"boundary_conditions.fields.{field}.{patch}.{key}", value)

    def _sync_bc_field_widgets(self):
        bc = self.openfoam["boundary_conditions"]
        field = self.cmb_bc_field.currentText() or bc.get("active_field", "U")
        self._set_openfoam_value("boundary_conditions.active_field", field)
        choices = {
            "U": ["fixedValue", "noSlip", "slip", "inletOutlet", "freestream", "symmetryPlane", "zeroGradient"],
            "p": ["fixedValue", "zeroGradient", "freestreamPressure", "symmetryPlane"],
            "k": ["fixedValue", "kqRWallFunction", "zeroGradient", "symmetryPlane"],
            "omega": ["fixedValue", "omegaWallFunction", "zeroGradient", "symmetryPlane"],
            "nut": ["calculated", "nutkWallFunction", "zeroGradient", "symmetryPlane"],
        }.get(field, ["fixedValue", "zeroGradient"])
        for patch in FLOW_PATCHES:
            enabled = bc["patches"][patch]["enabled"]
            cmb = self.bc_type_widgets[patch]
            val = self.bc_value_widgets[patch]
            cmb.blockSignals(True)
            cmb.clear()
            cmb.addItems(choices)
            entry = bc["fields"][field][patch]
            idx = cmb.findText(entry.get("type", ""))
            if idx < 0:
                cmb.addItem(entry.get("type", ""))
                idx = cmb.findText(entry.get("type", ""))
            cmb.setCurrentIndex(max(0, idx))
            cmb.blockSignals(False)
            val.setText(str(entry.get("value", "")))
            cmb.setEnabled(enabled)
            val.setEnabled(enabled)
