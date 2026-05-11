"""
CFD Aerodynamics Workbench - Isolated UI
Focused application for OpenFOAM CFD simulation and mesh generation.
No references to other workbenches or tabs.
"""
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDockWidget, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget

from project_paths import PROJECT_ROOT, SRC_DIR, ensure_workspace_dirs

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from runtime_bootstrap import bootstrap_runtime

ensure_workspace_dirs()
bootstrap_runtime(PROJECT_ROOT)

from ui_generated.aerodynamics_workbench import Ui_CFDAerodynamicsWindow
from aerodynamics import AerodynamicsTab
from aerodynamics.state import ensure_openfoam_state
from aerodynamics_app.workbench_shell import (
    AerodynamicsPreferencesDialog,
    WorkbenchShellMixin,
    load_icon,
)


class CFDWorkbenchWindow(WorkbenchShellMixin, QMainWindow):
    """Main window for isolated CFD aerodynamics workbench."""

    def __init__(self):
        super().__init__()
        self.preferences_dialog = None
        self.ribbon_controller = None
        self.file_organizer = None
        self.code_editor = None
        self.history_manager = None
        self.aerodynamics_tab = None
        self.cfd_console_dock = None
        self.cfd_console_output = None
        self._new_case_window = None
        self._workspace_focus_connected = False

        self.ui = Ui_CFDAerodynamicsWindow()
        self.ui.setupUi(self)

        self._ensure_cfd_console_dock()
        self._configure_ribbon()
        self._init_preferences()

        self.state = {"aerodynamics": {}, "settings": {}, "workspace": {}}
        self._ensure_settings_state()
        self._load_shell_state()
        self._ensure_settings_state()
        ensure_openfoam_state(self.state["aerodynamics"])

        self.aerodynamics_tab = AerodynamicsTab(self.ui, self.state)
        self.aerodynamics_tab.set_console_output(self.cfd_console_output)

        self._apply_cfd_settings()
        self._init_tree_view()
        self._setup_view_menu()
        self._setup_docks()
        self._initialize_workspace_shell()
        self._init_view_actions()
        self._init_case_actions()
        self._init_file_actions(auto_show=True)

        self.aerodynamics_tab.set_task_controls_visible(True)
        self._ensure_task_panels_visible()

        if hasattr(self.ui, "properties") and self.ui.properties is not None:
            self.ui.properties.setVisible(True)
        if hasattr(self.ui, "properties_tab_widget") and self.ui.properties_tab_widget is not None:
            self.ui.properties_tab_widget.setCurrentIndex(0)

    def _ensure_cfd_console_dock(self):
        """Ensure CFD console dock is available."""
        self.cfd_console_dock = getattr(self.ui, "cfd_console_dock", None)
        self.cfd_console_output = getattr(self.ui, "cfd_console_output", None)
        
        if self.cfd_console_output is None:
            # Create console dock if not in UI
            self.cfd_console_dock = QDockWidget("CFD Console", self)
            self.cfd_console_dock.setObjectName("cfd_console_dock")
            console_root = QWidget(self.cfd_console_dock)
            layout = QVBoxLayout(console_root)
            layout.setContentsMargins(8, 8, 8, 8)
            self.cfd_console_output = QPlainTextEdit(console_root)
            self.cfd_console_output.setReadOnly(True)
            layout.addWidget(self.cfd_console_output)
            self.cfd_console_dock.setWidget(console_root)
            self.addDockWidget(Qt.BottomDockWidgetArea, self.cfd_console_dock)
        else:
            self.cfd_console_output.setReadOnly(True)
        
        if self.cfd_console_dock is not None:
            self.cfd_console_dock.setVisible(False)

    def _configure_ribbon(self):
        """Configure ribbon toolbar."""
        ribbon_frame = getattr(self.ui, "ribbon_frame", None)
        if ribbon_frame is None:
            return
        ribbon_frame.setVisible(True)

    def _init_preferences(self):
        """Initialize preferences system."""
        self.preferences_dialog = self._create_preferences_dialog()

    def _ensure_settings_state(self):
        """Ensure settings state is properly initialized."""
        settings = self.state.setdefault("settings", {})
        settings.setdefault("general", {})
        settings.setdefault("cfd", {})

    def _apply_cfd_settings(self):
        """Apply CFD visualization settings."""
        cfd_settings = self.state.get("settings", {}).get("cfd", {})
        self.aerodynamics_tab.set_background_theme(cfd_settings.get("background_theme", "gradient_dark"))
        self.aerodynamics_tab.set_lighting_profile(cfd_settings.get("lighting_profile", "balanced"))
        self.aerodynamics_tab.set_mesh_render_mode(cfd_settings.get("mesh_render_mode", "Smooth"))
        self.aerodynamics_tab.set_mesh_opacity(cfd_settings.get("mesh_opacity", "High"))

    def _apply_dark_mode(self, enabled):
        """Apply dark mode theme."""
        # Dark mode styling is now defined in the .ui file via stylesheets
        # Keep this method for compatibility but don't override palette
        pass

    def _setup_view_menu(self):
        """Setup View menu with console toggle."""
        menu_bar = self.menuBar()
        
        # Find or create View menu
        view_menu = None
        for action in menu_bar.actions():
            if action.text() == "View":
                view_menu = action.menu()
                break
        
        if view_menu is None:
            view_menu = menu_bar.addMenu("View")
        
        # Add console toggle action
        console_action = view_menu.addAction("Show Console")
        console_action.setCheckable(True)
        console_action.setChecked(False)
        console_action.triggered.connect(self._toggle_console_visibility)
        
        # Add preferences
        view_menu.addSeparator()
        pref_action = view_menu.addAction("Preferences...")
        pref_action.triggered.connect(self._show_preferences)

    def _toggle_console_visibility(self, checked):
        """Toggle console dock visibility."""
        if self.cfd_console_dock is not None:
            self.cfd_console_dock.setVisible(checked)

    def _show_preferences(self):
        """Show preferences dialog."""
        if self.preferences_dialog is None:
            self.preferences_dialog = self._create_preferences_dialog()
        
        self.preferences_dialog.load_from_state(self.state)
        if self.preferences_dialog.exec():
            self.preferences_dialog.apply_to_state(self.state)
            self._apply_cfd_settings()
            self._apply_dark_mode(self.state.get("settings", {}).get("general", {}).get("dark_mode", False))
            self._save_shell_state()

    def _setup_docks(self):
        """Setup dock widget visibility toggles."""
        # Connect ribbon buttons to dock visibility
        if hasattr(self.ui, "btn_ribbon_toggle_tree"):
            self.ui.btn_ribbon_toggle_tree.clicked.connect(
                lambda checked: self._toggle_dock_visibility(self.ui.tree, checked)
            )
        
        if hasattr(self.ui, "btn_ribbon_toggle_properties"):
            self.ui.btn_ribbon_toggle_properties.clicked.connect(
                lambda checked: self._toggle_dock_visibility(self.ui.properties, checked)
            )
        
        if hasattr(self.ui, "btn_ribbon_toggle_task"):
            self.ui.btn_ribbon_toggle_task.clicked.connect(
                lambda checked: self._toggle_dock_visibility(self.ui.properties, checked)
            )
        
        if hasattr(self.ui, "btn_ribbon_show_console"):
            self.ui.btn_ribbon_show_console.clicked.connect(
                lambda checked: self._toggle_dock_visibility(self.cfd_console_dock, checked)
            )
        
        if hasattr(self.ui, "btn_ribbon_reset_layout"):
            self.ui.btn_ribbon_reset_layout.clicked.connect(self._reset_layout)

    def _toggle_dock_visibility(self, dock, visible):
        """Toggle dock widget visibility."""
        if dock is not None:
            dock.setVisible(visible)

    def _reset_layout(self):
        """Reset window layout to defaults."""
        if hasattr(self.ui, "tree") and self.ui.tree is not None:
            self.ui.tree.setVisible(True)
        if hasattr(self.ui, "properties") and self.ui.properties is not None:
            self.ui.properties.setVisible(True)
        if self.cfd_console_dock is not None:
            self.cfd_console_dock.setVisible(False)

    def _init_view_actions(self):
        """Initialize view action connections."""
        # Camera controls
        if hasattr(self.ui, "btn_ribbon_reset_camera"):
            self.ui.btn_ribbon_reset_camera.clicked.connect(self.aerodynamics_tab.reset_viewer_camera)
        
        if hasattr(self.ui, "btn_ribbon_view_front"):
            self.ui.btn_ribbon_view_front.clicked.connect(lambda: self.aerodynamics_tab.set_standard_view("front"))
        
        if hasattr(self.ui, "btn_ribbon_view_top"):
            self.ui.btn_ribbon_view_top.clicked.connect(lambda: self.aerodynamics_tab.set_standard_view("top"))
        
        if hasattr(self.ui, "btn_ribbon_view_side"):
            self.ui.btn_ribbon_view_side.clicked.connect(lambda: self.aerodynamics_tab.set_standard_view("side"))

    def _init_case_actions(self):
        mapping = {
            "btn_ribbon_import_case": self.aerodynamics_tab.import_openfoam_case_from_dialog,
            "btn_ribbon_load_geometry": self.aerodynamics_tab.import_cfd_stl_from_dialog,
            "btn_ribbon_save_config": self.aerodynamics_tab.save_openfoam_config_from_dialog,
            "btn_ribbon_load_config": self.aerodynamics_tab.load_openfoam_config_from_dialog,
            "btn_ribbon_export_case": self.aerodynamics_tab.export_openfoam_case_from_dialog,
            "btn_ribbon_open_case_folder": self.aerodynamics_tab.open_case_folder,
        }
        for widget_name, handler in mapping.items():
            widget = getattr(self.ui, widget_name, None)
            if widget is not None:
                widget.clicked.connect(handler)

    def _ensure_task_panels_visible(self):
        """Ensure task panels are fully visible and initialized."""
        # Make sure the scroll area with task panels is visible
        if hasattr(self.aerodynamics_tab, "of_task_scroll") and self.aerodynamics_tab.of_task_scroll is not None:
            self.aerodynamics_tab.of_task_scroll.setVisible(True)
        
        # Ensure the task tab widget exists and is set to Task tab
        if hasattr(self.ui, "properties_tab_widget") and self.ui.properties_tab_widget is not None:
            # Find the task_task widget or set to index 0 (Task tab)
            self.ui.properties_tab_widget.setCurrentIndex(0)
        
        # Force update of layout and display
        if hasattr(self.ui, "properties") and self.ui.properties is not None:
            self.ui.properties.raise_()
            self.ui.properties.activateWindow()

    def _create_preferences_dialog(self):
        return AerodynamicsPreferencesDialog(
            self,
            settings_path=("cfd",),
            background_label="3D Background",
            lighting_label="Lighting Profile",
            render_mode_label="Surface Render Mode",
            mesh_opacity_label="Surface Opacity",
            include_ribbon=True,
        )

    def closeEvent(self, event):
        if getattr(self, 'ribbon_controller', None) is not None:
            self.ribbon_controller.cleanup()
        self._save_shell_state()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    icon = load_icon()
    if icon is not None:
        app.setWindowIcon(icon)
    window = CFDWorkbenchWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
