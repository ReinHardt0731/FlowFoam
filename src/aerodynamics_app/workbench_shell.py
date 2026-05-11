from pathlib import Path
import re
import warnings

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QMessageBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from aerodynamics_app.code_editor import CodeEditorTabWidget
from aerodynamics_app.file_organizer import FileOrganizerWidget
from aerodynamics_app.new_case_window import (
    NewCaseWindow,
    copy_tutorial_case,
    resolve_tutorial_manifest,
    validate_tutorial_destination,
)
from aerodynamics_app.workspace_state import (
    load_workspace_payload,
    preferences_default_path,
    record_recent_case,
    save_workspace_payload,
)
from project_paths import FLIGHTFORGE_ICON_PATH, PROJECT_ROOT, WORKSPACE_CASES_DIR


TEXT_FILE_SUFFIXES = {
    ".py", ".json", ".yaml", ".yml", ".txt", ".cfg",
    ".foam", ".stl", ".dict", ".sh", ".bat", ".md",
}
def load_icon(root: Path | None = None):
    icon_path = Path(root) / "flightforge.ico" if root else FLIGHTFORGE_ICON_PATH
    if not icon_path.is_file():
        return None
    icon = QIcon(str(icon_path))
    return icon if not icon.isNull() else None


def ensure_settings_section(state, *path):
    settings = state.setdefault("settings", {})
    cur = settings
    for key in path:
        cur = cur.setdefault(key, {})
    return cur


class AerodynamicsPreferencesDialog(QDialog):
    def __init__(
        self,
        parent=None,
        *,
        settings_path=("tabs", "aerodynamics"),
        background_label="Aerodynamics background",
        lighting_label="Aerodynamics lighting",
        render_mode_label="Surface Mesh Render",
        mesh_opacity_label="Surface Mesh Opacity",
        include_ribbon=False,
    ):
        super().__init__(parent)
        self.settings_path = tuple(settings_path)
        self.background_label = background_label
        self.lighting_label = lighting_label
        self.render_mode_label = render_mode_label
        self.mesh_opacity_label = mesh_opacity_label
        self.include_ribbon = bool(include_ribbon)
        self.setWindowTitle("Preferences")
        self._build_ui()

    def _build_ui(self):
        layout = QFormLayout(self)
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.chk_dark_mode = QCheckBox("Enable dark mode theme", self)
        layout.addRow(self.chk_dark_mode)

        layout.addRow(QLabel(""))
        layout.addRow(QLabel("<b>Visualization</b>"))

        self.cmb_aero_background = QComboBox(self)
        for label, value in (
            ("Gradient Dark", "gradient_dark"),
            ("Gradient Sky", "gradient_sky"),
            ("Gradient Studio", "gradient_studio"),
            ("Gradient Sunset", "gradient_sunset"),
            ("Solid Light", "solid_light"),
        ):
            self.cmb_aero_background.addItem(label, value)
        layout.addRow(QLabel(self.background_label), self.cmb_aero_background)

        self.cmb_aero_lighting = QComboBox(self)
        for label, value in (("Balanced", "balanced"), ("Soft", "soft"), ("Contrast", "contrast")):
            self.cmb_aero_lighting.addItem(label, value)
        layout.addRow(QLabel(self.lighting_label), self.cmb_aero_lighting)

        self.cmb_mesh_render_mode = QComboBox(self)
        self.cmb_mesh_render_mode.addItems(["Smooth", "Mesh", "Smooth + Mesh"])
        layout.addRow(QLabel(self.render_mode_label), self.cmb_mesh_render_mode)

        self.cmb_mesh_opacity = QComboBox(self)
        self.cmb_mesh_opacity.addItems(["High", "Low"])
        layout.addRow(QLabel(self.mesh_opacity_label), self.cmb_mesh_opacity)

        self.chk_ribbon_minimized = None
        if self.include_ribbon:
            layout.addRow(QLabel(""))
            layout.addRow(QLabel("<b>Interface</b>"))
            self.chk_ribbon_minimized = QCheckBox("Start with ribbon minimized", self)
            layout.addRow(self.chk_ribbon_minimized)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def _settings_section(self, state):
        return ensure_settings_section(state, *self.settings_path)

    def load_from_state(self, state):
        general = state.get("settings", {}).get("general", {})
        self.chk_dark_mode.setChecked(bool(general.get("dark_mode", False)))
        section = self._settings_section(state)
        self._set_combo_value(self.cmb_aero_background, section.get("background_theme", "gradient_dark"))
        self._set_combo_value(self.cmb_aero_lighting, section.get("lighting_profile", "balanced"))
        self._set_combo_value(self.cmb_mesh_render_mode, section.get("mesh_render_mode", "Smooth"))
        self._set_combo_value(self.cmb_mesh_opacity, section.get("mesh_opacity", "High"))
        if self.chk_ribbon_minimized is not None:
            self.chk_ribbon_minimized.setChecked(bool(section.get("ribbon_minimized", False)))

    def apply_to_state(self, state):
        general = ensure_settings_section(state, "general")
        general["dark_mode"] = bool(self.chk_dark_mode.isChecked())
        section = self._settings_section(state)
        section["background_theme"] = self.cmb_aero_background.currentData() or "gradient_dark"
        section["lighting_profile"] = self.cmb_aero_lighting.currentData() or "balanced"
        section["mesh_render_mode"] = self.cmb_mesh_render_mode.currentText() or "Smooth"
        section["mesh_opacity"] = self.cmb_mesh_opacity.currentText() or "High"
        if self.chk_ribbon_minimized is not None:
            section["ribbon_minimized"] = bool(self.chk_ribbon_minimized.isChecked())

    def _set_combo_value(self, combo, value):
        val = str(value or "")
        idx = combo.findData(val)
        if idx < 0:
            idx = combo.findText(val)
        combo.setCurrentIndex(idx if idx >= 0 else 0)


class WorkbenchShellMixin:
    def _initialize_workspace_shell(self):
        self._ensure_workspace_state()
        self._setup_code_editor()
        self.refresh_file_organizer(sync_tab=False)
        app = QApplication.instance()
        if app is not None and not bool(getattr(self, "_workspace_focus_connected", False)):
            app.focusChanged.connect(self._on_app_focus_changed)
            self._workspace_focus_connected = True

    def _deep_merge_dict(self, dst, src, overwrite=False):
        if not isinstance(dst, dict) or not isinstance(src, dict):
            return
        for key, value in src.items():
            if isinstance(value, dict):
                current = dst.get(key)
                if not isinstance(current, dict):
                    current = {}
                    dst[key] = current
                self._deep_merge_dict(current, value, overwrite=overwrite)
                continue
            if overwrite or key not in dst:
                dst[key] = value

    def _shell_preferences_path(self):
        return preferences_default_path(PROJECT_ROOT)

    def _ensure_workspace_state(self):
        workspace = self.state.setdefault("workspace", {})
        recent_cases = workspace.get("recent_cases", [])
        if not isinstance(recent_cases, list):
            recent_cases = []
        workspace["recent_cases"] = recent_cases
        return workspace

    def _load_shell_state(self):
        payload = load_workspace_payload(self._shell_preferences_path())
        settings = self.state.setdefault("settings", {})
        self._deep_merge_dict(settings, payload.get("settings", {}), overwrite=True)
        workspace = self._ensure_workspace_state()
        workspace_payload = payload.get("workspace", {})
        if isinstance(workspace_payload, dict):
            workspace["recent_cases"] = list(workspace_payload.get("recent_cases", []))

    def _save_shell_state(self):
        save_workspace_payload(
            self._shell_preferences_path(),
            settings=self.state.get("settings", {}),
            workspace=self.state.get("workspace", {}),
        )

    def _recent_cases(self):
        return list(self._ensure_workspace_state().get("recent_cases", []))

    def _record_recent_case(self, case_path, *, label=None, source_kind="opened", template_id=""):
        workspace = self._ensure_workspace_state()
        workspace["recent_cases"] = record_recent_case(
            workspace.get("recent_cases", []),
            case_path,
            label=label,
            source_kind=source_kind,
            template_id=template_id,
        )
        self._save_shell_state()

    def _workspace_case_opened(self, case_dir, source_kind="opened", template_id=""):
        path = Path(str(case_dir or "").strip())
        if not path.is_dir():
            return
        self._record_recent_case(
            path,
            label=path.name,
            source_kind=source_kind,
            template_id=template_id,
        )
        dialog = getattr(self, "_new_case_window", None)
        if dialog is not None:
            dialog.set_recent_cases(self._recent_cases())

    def _required_case_root(self):
        if getattr(self, "aerodynamics_tab", None) is None:
            WORKSPACE_CASES_DIR.mkdir(parents=True, exist_ok=True)
            return WORKSPACE_CASES_DIR
        try:
            return self.aerodynamics_tab._required_case_root()
        except Exception:
            WORKSPACE_CASES_DIR.mkdir(parents=True, exist_ok=True)
            return WORKSPACE_CASES_DIR

    def _tutorial_entries(self):
        return resolve_tutorial_manifest(PROJECT_ROOT)

    def _refresh_new_case_window(self):
        dialog = getattr(self, "_new_case_window", None)
        if dialog is None:
            return None
        dialog.set_recent_cases(self._recent_cases())
        dialog.set_tutorials(self._tutorial_entries())
        dialog.set_default_parent(self._required_case_root())
        return dialog

    def _show_new_case_window(self):
        dialog = getattr(self, "_new_case_window", None)
        if dialog is None:
            dialog = NewCaseWindow(
                self,
                tutorials=self._tutorial_entries(),
                recent_cases=self._recent_cases(),
                default_parent=self._required_case_root(),
                required_root=self._required_case_root(),
            )
            dialog.open_existing_requested.connect(self._open_existing_case_from_menu)
            dialog.open_recent_requested.connect(self._open_recent_case_from_dialog)
            dialog.create_tutorial_requested.connect(self._create_tutorial_case_from_dialog)
            self._new_case_window = dialog
        self._refresh_new_case_window()
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

    def _maybe_show_new_case_window(self):
        case_dir = str(
            self.state.get("aerodynamics", {})
            .get("openfoam", {})
            .get("execution", {})
            .get("case_dir", "")
        ).strip()
        if case_dir:
            return
        self._show_new_case_window()

    def _init_file_actions(self, *, auto_show=False):
        action_new = getattr(self.ui, "actionNew", None)
        if action_new is not None:
            try:
                action_new.triggered.disconnect()
            except Exception:
                pass
            action_new.triggered.connect(self._show_new_case_window)
        action_open = getattr(self.ui, "actionOpen", None)
        if action_open is not None:
            try:
                action_open.triggered.disconnect()
            except Exception:
                pass
            action_open.triggered.connect(self._open_existing_case_from_menu)
        if auto_show:
            QTimer.singleShot(0, self._maybe_show_new_case_window)

    def _open_existing_case_from_menu(self):
        if getattr(self, "aerodynamics_tab", None) is None:
            return False
        opened = bool(self.aerodynamics_tab.import_openfoam_case_from_dialog())
        if opened:
            dialog = getattr(self, "_new_case_window", None)
            if dialog is not None:
                dialog.accept()
        return opened

    def _open_recent_case_from_dialog(self, case_dir):
        if getattr(self, "aerodynamics_tab", None) is None:
            return False
        opened = bool(self.aerodynamics_tab.import_openfoam_case(case_dir))
        if opened:
            dialog = getattr(self, "_new_case_window", None)
            if dialog is not None:
                dialog.accept()
        return opened

    def _create_tutorial_case_from_dialog(self, template_id, case_name, destination_parent):
        entries = {entry["id"]: entry for entry in self._tutorial_entries()}
        entry = entries.get(str(template_id))
        dialog = getattr(self, "_new_case_window", None)
        if entry is None:
            QMessageBox.warning(self, "New File", "Selected tutorial template is no longer available.")
            return False
        target_dir, error = validate_tutorial_destination(destination_parent, case_name)
        if error:
            QMessageBox.warning(self, "New File", error)
            return False
        if target_dir is None:
            return False
        required_root = self._required_case_root()
        try:
            allowed = self.aerodynamics_tab._case_dir_is_allowed(target_dir)
        except Exception:
            allowed = False
        if not allowed:
            QMessageBox.warning(
                self,
                "New File",
                f"Tutorial cases must be created under:\n{required_root}",
            )
            return False
        try:
            copy_tutorial_case(entry["source_path"], target_dir)
        except Exception as exc:
            QMessageBox.critical(self, "New File", str(exc))
            return False
        opened = bool(self.aerodynamics_tab.import_openfoam_case(target_dir))
        if not opened:
            return False
        self._record_recent_case(
            target_dir,
            label=target_dir.name,
            source_kind="tutorial",
            template_id=entry["id"],
        )
        if dialog is not None:
            dialog.accept()
        return True

    def _placeholder_widget(self, text, *, color="#999"):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"color: {color}; font-size: 11px; padding: 20px;")
        return label

    def _replace_layout_contents(self, layout, widget):
        while layout.count():
            item = layout.takeAt(0)
            old_widget = item.widget()
            if old_widget is not None:
                old_widget.setParent(None)
                old_widget.deleteLater()
        layout.addWidget(widget)

    def _ensure_files_tab(self):
        tab_widget = getattr(self.ui, "properties_tab_widget", None)
        if tab_widget is None:
            return None, None
        container = getattr(self, "_files_tab_container", None)
        layout = getattr(self, "_files_tab_layout", None)
        if container is None or layout is None:
            container = QWidget(tab_widget)
            container.setObjectName("files_tab")
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            tab_widget.addTab(container, "Files")
            self._files_tab_container = container
            self._files_tab_layout = layout
        return container, layout

    def _set_files_surface_widget(self, widget):
        tab_widget = getattr(self.ui, "properties_tab_widget", None)
        if tab_widget is not None:
            _container, layout = self._ensure_files_tab()
            if layout is not None:
                self._replace_layout_contents(layout, widget)
                return
        properties_dock = getattr(self.ui, "properties", None)
        if properties_dock is not None:
            properties_dock.setWidget(widget)
            properties_dock.setWindowTitle("Files")

    def _activate_files_surface(self, sync_tab):
        properties_dock = getattr(self.ui, "properties", None)
        if properties_dock is not None:
            properties_dock.setVisible(True)
            properties_dock.raise_()
        if not sync_tab:
            return
        tab_widget = getattr(self.ui, "properties_tab_widget", None)
        container = getattr(self, "_files_tab_container", None)
        if tab_widget is not None and container is not None:
            idx = tab_widget.indexOf(container)
            if idx >= 0:
                tab_widget.setCurrentIndex(idx)

    def _setup_code_editor(self):
        if getattr(self, "code_editor", None) is not None:
            return
        
        # Try to add to the code editor dock if it exists
        code_editor_dock = getattr(self, "code_editor_dock", None)
        code_editor_dock_layout = getattr(self, "code_editor_dock_layout", None)
        if code_editor_dock is not None and code_editor_dock_layout is not None:
            editor = CodeEditorTabWidget(self)
            code_editor_dock_layout.addWidget(editor)
            self.code_editor = editor
            return
        
        # Fallback: Try tab widget approach
        tab_widget = getattr(self.ui, "tabWidget_3", None)
        if tab_widget is not None:
            tab_widget.setTabPosition(QTabWidget.South)
            editor = CodeEditorTabWidget(self)
            tab_widget.addTab(editor, "Code Editor")
            self.code_editor = editor
            return

        # Fallback: Try frame approach
        frame = getattr(self.ui, "codeEditorFrame", None)
        layout = getattr(self.ui, "codeEditorLayout", None)
        if layout is None and frame is not None and hasattr(frame, "layout"):
            layout = frame.layout()
        if frame is None or layout is None:
            return

        existing = getattr(self.ui, "codeEditorTabs", None)
        if existing is not None:
            layout.removeWidget(existing)
            existing.setParent(None)
            existing.deleteLater()

        editor = CodeEditorTabWidget(frame)
        layout.addWidget(editor)
        self.code_editor = editor

    def refresh_file_organizer(self, sync_tab=False):
        case_dir = str(
            self.state.get("aerodynamics", {})
            .get("openfoam", {})
            .get("execution", {})
            .get("case_dir", "")
        ).strip()

        if case_dir:
            organizer = FileOrganizerWidget(Path(case_dir))
        else:
            organizer = FileOrganizerWidget(PROJECT_ROOT)
        organizer.file_selected.connect(self._on_file_selected_auto_open)
        self.file_organizer = organizer
        widget = organizer

        self._set_files_surface_widget(widget)
        self._activate_files_surface(sync_tab=sync_tab)

    def _refresh_property_from_tree_selection(self, sync_tab=True):
        self.refresh_file_organizer(sync_tab=sync_tab)

    def _activate_code_editor_surface(self):
        code_editor_dock = getattr(self, "code_editor_dock", None)
        if code_editor_dock is not None:
            code_editor_dock.setVisible(True)
            code_editor_dock.raise_()
            toggle_action = getattr(self, "code_editor_toggle_action", None)
            if toggle_action is not None:
                blocked = toggle_action.blockSignals(True)
                toggle_action.setChecked(True)
                toggle_action.blockSignals(blocked)
        tab_widget = getattr(self.ui, "tabWidget_3", None)
        if tab_widget is None:
            return
        for idx in range(tab_widget.count()):
            if tab_widget.tabText(idx) == "Code Editor":
                tab_widget.setCurrentIndex(idx)
                break

    def _on_file_selected_auto_open(self, file_path):
        if getattr(self, "code_editor", None) is None:
            return
        path = Path(file_path) if isinstance(file_path, str) else file_path
        if path is None or not getattr(path, "suffix", ""):
            return
        if path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            return
        if self.code_editor.add_file_tab(path):
            self._activate_code_editor_surface()

    def _on_app_focus_changed(self, _old_widget, new_widget):
        if getattr(self, "code_editor", None) is None:
            return
        if new_widget is None:
            self.code_editor.save_all_files()

    def _init_tree_view(self):
        tree_view = getattr(self.ui, "treeView", None)
        if tree_view is None:
            return
        model = self.aerodynamics_tab.get_model()
        if model is None:
            return
        tree_view.setModel(model)
        tree_view.expandAll()
        sel_model = tree_view.selectionModel()
        if sel_model is not None:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                try:
                    sel_model.selectionChanged.disconnect(self._on_tree_selection_changed)
                except Exception:
                    pass
            sel_model.selectionChanged.connect(self._on_tree_selection_changed)
        index = model.index(0, 0)
        if index.isValid():
            tree_view.setCurrentIndex(index)
            self.aerodynamics_tab.on_tree_selection_changed(self._tree_index_path(index))

    def _on_tree_selection_changed(self, selected, _deselected=None):
        tree_view = getattr(self.ui, "treeView", None)
        if tree_view is None:
            return
        if hasattr(selected, "indexes") and selected.indexes():
            index = selected.indexes()[0]
        else:
            index = tree_view.currentIndex()
        path = self._tree_index_path(index)
        self.aerodynamics_tab.on_tree_selection_changed(path)

    def _tree_index_path(self, index):
        if not index or not index.isValid():
            return []
        tree_view = getattr(self.ui, "treeView", None)
        model = tree_view.model() if tree_view is not None else None
        if model is None:
            return []
        path = []
        cur = index
        while cur.isValid():
            data = model.data(cur, Qt.UserRole)
            if data is None or (isinstance(data, str) and not str(data).strip()):
                data = model.data(cur, Qt.DisplayRole)
            text = str(data) if data is not None else ""
            try:
                text = re.sub(r'^[^\w"]+', '', text).strip()
            except Exception:
                text = text.strip()
            path.append(text)
            cur = cur.parent()
        path.reverse()
        return path
