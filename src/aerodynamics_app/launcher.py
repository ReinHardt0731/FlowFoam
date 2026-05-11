import sys
import json
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDockWidget,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QTreeView,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
)

from project_paths import CHECKBOX_CHECK_WHITE_PATH, PROJECT_ROOT, SRC_DIR, ensure_workspace_dirs

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from runtime_bootstrap import bootstrap_runtime

ensure_workspace_dirs()
bootstrap_runtime(PROJECT_ROOT)

from ui_generated.aircraft_design import Ui_MainWindow
from aerodynamics import AerodynamicsTab
from aerodynamics.state import ensure_openfoam_state
from aerodynamics_app.workbench_shell import (
    AerodynamicsPreferencesDialog,
    WorkbenchShellMixin,
    load_icon,
)


class AeroWindow(WorkbenchShellMixin, QMainWindow):
    def __init__(self):
        super().__init__()
        self.preferences_dialog = None
        self.file_organizer = None
        self.code_editor = None
        self.ribbon_controller = None
        self._new_case_window = None
        self._workspace_focus_connected = False
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Flight Forge - Aerodynamics")
        self.setMinimumSize(900, 600)

        self._init_cfd_console_dock()
        self._init_code_editor_dock()
        self._disable_dock_background_fill()
        self._configure_viewer_first_shell()
        self._init_preferences_actions()

        self.state = {"aerodynamics": {}, "settings": {}, "workspace": {}}
        self._ensure_settings_state()
        self._apply_aerodynamics_preferences()
        self._ensure_settings_state()
        ensure_openfoam_state(self.state["aerodynamics"])

        self.aerodynamics_tab = AerodynamicsTab(self.ui, self.state)
        self.aerodynamics_tab.set_console_output(self.cfd_console_output)

        aero_settings = self.state.get("settings", {}).get("tabs", {}).get("aerodynamics", {})
        self.aerodynamics_tab.set_background_theme(aero_settings.get("background_theme", "gradient_dark"))
        self.aerodynamics_tab.set_lighting_profile(aero_settings.get("lighting_profile", "balanced"))
        self.aerodynamics_tab.set_mesh_render_mode(aero_settings.get("mesh_render_mode", "Smooth"))
        self.aerodynamics_tab.set_mesh_opacity(aero_settings.get("mesh_opacity", "High"))
        self._apply_dark_mode(self.state.get("settings", {}).get("general", {}).get("dark_mode", False))

        self._init_tree_view()
        self._setup_view_menu()
        self._initialize_workspace_shell()
        self._init_view_actions()
        self._init_file_actions(auto_show=False)
        self._restore_viewer_first_layout()
        self.aerodynamics_tab.set_task_controls_visible(True)

    def _init_cfd_console_dock(self):
        self.cfd_console_dock = getattr(self.ui, "cfd_console_dock", None)
        self.cfd_console_output = getattr(self.ui, "cfd_console_output", None)
        if self.cfd_console_output is None:
            self.cfd_console_dock = QDockWidget("CFD Console", self)
            self.cfd_console_dock.setObjectName("cfd_console_dock")
            console_root = QWidget(self.cfd_console_dock)
            console_root.setObjectName("cfd_console_dock_contents")
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

    def _init_code_editor_dock(self):
        self.code_editor_dock = QDockWidget("Code Editor", self)
        self.code_editor_dock.setObjectName("code_editor_dock")
        editor_root = QWidget(self.code_editor_dock)
        editor_root.setObjectName("code_editor_dock_contents")
        layout = QVBoxLayout(editor_root)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(0)
        # Placeholder - the actual editor will be added by _setup_code_editor
        self.code_editor_dock_layout = layout
        self.code_editor_dock.setWidget(editor_root)
        self.addDockWidget(Qt.RightDockWidgetArea, self.code_editor_dock)
        self.code_editor_dock.setVisible(False)

    def _setup_view_menu(self):
        """Setup View menu with console and code editor toggle options."""
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
        self.console_toggle_action = console_action
        
        # Add code editor toggle action
        editor_action = view_menu.addAction("Show Code Editor")
        editor_action.setCheckable(True)
        editor_action.setChecked(False)
        editor_action.triggered.connect(self._toggle_code_editor_visibility)
        self.code_editor_toggle_action = editor_action

    def _toggle_console_visibility(self, checked):
        """Toggle console dock visibility."""
        if self.cfd_console_dock is not None:
            self.cfd_console_dock.setVisible(checked)

    def _toggle_code_editor_visibility(self, checked):
        """Toggle code editor dock visibility."""
        if self.code_editor_dock is not None:
            self.code_editor_dock.setVisible(checked)

    def _disable_dock_background_fill(self):
        """Disable auto-fill background on dock content wrapper widgets to allow transparency."""
        dock_wrappers = [
            getattr(self.ui, "tree_view_tree", None),
            getattr(self.ui, "properties_view_prop", None),
            getattr(self.ui, "task_view", None),
            getattr(self, "cfd_console_dock", None),
            getattr(self, "code_editor_dock", None),
        ]
        for wrapper in dock_wrappers:
            if wrapper is not None:
                wrapper.setAutoFillBackground(False)
                if hasattr(wrapper, "setStyleSheet"):
                    wrapper.setStyleSheet(
                        wrapper.styleSheet() + "\nQWidget { background: transparent; }"
                    )
        if self.cfd_console_dock is not None:
            console_widget = self.cfd_console_dock.widget()
            if console_widget is not None:
                console_widget.setAutoFillBackground(False)
        if self.code_editor_dock is not None:
            editor_widget = self.code_editor_dock.widget()
            if editor_widget is not None:
                editor_widget.setAutoFillBackground(False)

    def _configure_viewer_first_shell(self):
        viewer_workspace = getattr(self.ui, "viewer_workspace_frame", None)
        if viewer_workspace is not None:
            viewer_workspace.setVisible(True)
        if hasattr(self.ui, "tabWidget") and self.ui.tabWidget is not None:
            self.ui.tabWidget.setVisible(False)
        layout = getattr(self.ui, "gridLayout_8", None)
        if layout is not None and viewer_workspace is not None:
            layout.addWidget(viewer_workspace, 0, 0, 3, 1)
            layout.setRowStretch(0, 1)
            layout.setRowStretch(1, 0)
            layout.setRowStretch(2, 0)
            layout.setContentsMargins(0, 0, 0, 0)

    def _create_viewer_toolbar(self, viewer_workspace):
        """Create a transparent toolbar with viewer controls positioned above the 3D viewer."""
        # Get the layout and viewer_host
        layout = viewer_workspace.findChild(QVBoxLayout)
        if layout is None:
            return
        
        # Create toolbar frame
        toolbar = QWidget(viewer_workspace)
        toolbar.setObjectName("viewer_toolbar")
        toolbar.setAutoFillBackground(False)
        toolbar.setStyleSheet("""
            QWidget#viewer_toolbar {
                background-color: transparent;
                border: none;
            }
        """)
        toolbar.setFixedHeight(40)
        
        toolbar_layout = QVBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(8, 4, 8, 4)
        toolbar_layout.setSpacing(0)
        
        # Create button container
        button_container = QWidget()
        button_container.setAutoFillBackground(False)
        button_container.setStyleSheet("QWidget { background-color: transparent; }")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(4)
        
        # Add leading stretch to center buttons
        button_layout.addStretch()
        
        # Define viewer control buttons
        viewer_buttons = [
            ("📷", "Reset Camera", self.aerodynamics_tab.reset_viewer_camera),
            ("👁️ F", "Front View", lambda: self.aerodynamics_tab.set_standard_view("front")),
            ("👁️ T", "Top View", lambda: self.aerodynamics_tab.set_standard_view("top")),
            ("👁️ S", "Side View", lambda: self.aerodynamics_tab.set_standard_view("side")),
            ("|", None, None),  # Separator
            ("🎨", "Surface", lambda: self.aerodynamics_tab.set_viewer_render_mode("surface")),
            ("⚡", "Wireframe", lambda: self.aerodynamics_tab.set_viewer_render_mode("wireframe")),
            ("|", None, None),  # Separator
            ("〜", "Contours", self.aerodynamics_tab.toggle_viewer_contours),
            ("↗️", "Streamlines", self.aerodynamics_tab.toggle_viewer_streamlines),
            ("📸", "Screenshot", self.aerodynamics_tab.capture_viewer_screenshot),
        ]
        
        # Create buttons
        for emoji, tooltip, callback in viewer_buttons:
            if emoji == "|":  # Separator
                separator = QLabel("|")
                separator.setStyleSheet("color: #3a3d44; margin: 0 4px;")
                button_layout.addWidget(separator)
            else:
                btn = QPushButton(emoji)
                btn.setFlat(True)
                btn.setFixedSize(32, 32)
                btn.setAutoFillBackground(False)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #e6e6e6;
                        border: none;
                        padding: 0px;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: rgba(100, 100, 100, 0.10);
                        border-radius: 4px;
                    }
                    QPushButton:pressed {
                        background-color: rgba(100, 100, 100, 0.15);
                    }
                """)
                if tooltip:
                    btn.setToolTip(tooltip)
                if callback:
                    btn.clicked.connect(callback)
                button_layout.addWidget(btn)
        
        button_layout.addStretch()
        toolbar_layout.addWidget(button_container)
        
        # Insert toolbar at the top of the viewer layout
        layout.insertWidget(0, toolbar)

    def _bind_dock_toggle_controls(self, dock, action=None, button=None):
        if dock is None:
            return

        if action is not None:
            action.setCheckable(True)
            action.setChecked(dock.isVisible())
            action.toggled.connect(dock.setVisible)
        if button is not None:
            button.setCheckable(True)
            button.setChecked(dock.isVisible())
            button.toggled.connect(dock.setVisible)

        def sync_state(visible):
            if action is not None:
                blocked = action.blockSignals(True)
                action.setChecked(bool(visible))
                action.blockSignals(blocked)
            if button is not None:
                blocked = button.blockSignals(True)
                button.setChecked(bool(visible))
                button.blockSignals(blocked)

        dock.visibilityChanged.connect(sync_state)
        sync_state(dock.isVisible())

    def _init_view_actions(self):
        self._bind_dock_toggle_controls(
            getattr(self.ui, "tree", None),
            getattr(self.ui, "actionToggle_Tree_View", None),
            None,
        )
        self._bind_dock_toggle_controls(
            getattr(self.ui, "properties", None),
            getattr(self.ui, "actionToggle_Properties", None),
            None,
        )
        self._bind_dock_toggle_controls(
            getattr(self.ui, "task", None),
            getattr(self.ui, "actionToggle_Task", None),
            None,
        )
        self._bind_dock_toggle_controls(
            self.cfd_console_dock,
            None,
            None,
        )

    def _restore_viewer_first_layout(self):
        viewer_workspace = getattr(self.ui, "viewer_workspace_frame", None)
        if viewer_workspace is not None:
            viewer_workspace.setVisible(True)
            self._create_viewer_toolbar(viewer_workspace)
        if hasattr(self.ui, "tabWidget") and self.ui.tabWidget is not None:
            self.ui.tabWidget.setVisible(False)

        tree_dock = getattr(self.ui, "tree", None)
        properties_dock = getattr(self.ui, "properties", None)
        task_dock = getattr(self.ui, "task", None)
        if tree_dock is not None:
            tree_dock.setVisible(True)
            tree_dock.raise_()
        if properties_dock is not None:
            properties_dock.setVisible(True)
            properties_dock.raise_()
        if task_dock is not None:
            task_dock.setVisible(True)
            task_dock.raise_()
        if self.cfd_console_dock is not None:
            self.cfd_console_dock.setVisible(True)
            self.cfd_console_dock.raise_()

        if tree_dock is not None and properties_dock is not None:
            self.tabifyDockWidget(tree_dock, properties_dock)
            tree_dock.raise_()
        if tree_dock is not None and task_dock is not None:
            try:
                self.resizeDocks([tree_dock, task_dock], [280, 520], Qt.Horizontal)
            except Exception:
                pass
        if self.cfd_console_dock is not None and task_dock is not None:
            try:
                self.resizeDocks([self.cfd_console_dock, task_dock], [180, 420], Qt.Vertical)
            except Exception:
                pass

    def _show_task_and_tree_docks(self):
        self._restore_viewer_first_layout()

    def _init_preferences_actions(self):
        if hasattr(self.ui, "actionPreference") and self.ui.actionPreference is not None:
            self.ui.actionPreference.triggered.connect(self.open_preferences_dialog)
        if hasattr(self.ui, "actionPreference_2") and self.ui.actionPreference_2 is not None:
            self.ui.actionPreference_2.triggered.connect(self.open_preferences_dialog)

    def open_preferences_dialog(self):
        self._ensure_settings_state()
        if self.preferences_dialog is None:
            self.preferences_dialog = self._create_preferences_dialog()
        self.preferences_dialog.load_from_state(self.state)
        if self.preferences_dialog.exec() != QDialog.Accepted:
            return
        self.preferences_dialog.apply_to_state(self.state)
        self._ensure_settings_state()
        self._save_default_preferences()
        aero_settings = self.state.get("settings", {}).get("tabs", {}).get("aerodynamics", {})
        self.aerodynamics_tab.set_background_theme(aero_settings.get("background_theme", "gradient_dark"))
        self.aerodynamics_tab.set_lighting_profile(aero_settings.get("lighting_profile", "balanced"))
        self._apply_dark_mode(self.state.get("settings", {}).get("general", {}).get("dark_mode", False))
        # Apply visualization preferences
        self.aerodynamics_tab.set_mesh_render_mode(aero_settings.get("mesh_render_mode", "Smooth"))
        self.aerodynamics_tab.set_mesh_opacity(aero_settings.get("mesh_opacity", "High"))
        # Reload and apply ribbon state if it changed
        if hasattr(self, 'ribbon_controller') and self.ribbon_controller is not None:
            self.ribbon_controller.load_from_preferences()
            self.ribbon_controller.apply_current_state()

    def _ensure_settings_state(self):
        settings = self.state.setdefault("settings", {})
        general = settings.setdefault("general", {})
        general.setdefault("dark_mode", False)
        general.setdefault("center_tree_branches", True)
        tabs = settings.setdefault("tabs", {})
        aero = tabs.setdefault("aerodynamics", {})
        aero.setdefault("background_theme", "gradient_dark")
        aero.setdefault("lighting_profile", "balanced")
        aero.setdefault("ribbon_minimized", False)
        aero.setdefault("mesh_render_mode", "Smooth")
        aero.setdefault("mesh_opacity", "High")

    def _preferences_default_path(self):
        from project_paths import PREFERENCES_PATH

        return PREFERENCES_PATH

    def _load_default_preferences(self):
        path = self._preferences_default_path()
        if not path.is_file():
            return {}
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
        if not isinstance(payload, dict):
            return {}
        settings = payload.get("settings", payload)
        return settings if isinstance(settings, dict) else {}

    def _save_default_preferences(self):
        self._save_shell_state()

    def _deep_merge_dict(self, dst, src, overwrite=False):
        if not isinstance(dst, dict) or not isinstance(src, dict):
            return
        for key, value in src.items():
            if isinstance(value, dict):
                cur = dst.get(key)
                if not isinstance(cur, dict):
                    cur = {}
                    dst[key] = cur
                self._deep_merge_dict(cur, value, overwrite=overwrite)
                continue
            if overwrite or key not in dst:
                dst[key] = value

    def _apply_aerodynamics_preferences(self):
        self._load_shell_state()

    def _apply_dark_mode(self, enabled):
        app = QApplication.instance()
        if app is None:
            return
        if not bool(enabled):
            app.setPalette(app.style().standardPalette())
            app.setStyleSheet("")
            center_tree_branches = bool(
                self.state.get("settings", {}).get("general", {}).get("center_tree_branches", True)
            )
            self._apply_tree_branch_styles(False, center_tree_branches)
            return
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#1e1f22"))
        palette.setColor(QPalette.WindowText, QColor("#e6e6e6"))
        palette.setColor(QPalette.Base, QColor("#2a2d33"))
        palette.setColor(QPalette.AlternateBase, QColor("#25262a"))
        palette.setColor(QPalette.Text, QColor("#e6e6e6"))
        palette.setColor(QPalette.Button, QColor("#31353d"))
        palette.setColor(QPalette.ButtonText, QColor("#f0f0f0"))
        palette.setColor(QPalette.ToolTipBase, QColor("#2a2d33"))
        palette.setColor(QPalette.ToolTipText, QColor("#f0f0f0"))
        palette.setColor(QPalette.Highlight, QColor("#3b5f8a"))
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        app.setPalette(palette)
        checkbox_path = CHECKBOX_CHECK_WHITE_PATH.as_posix()
        stylesheet = """
            QMainWindow, QDialog, QDockWidget, QStatusBar, QToolBar {
                background-color: #1e1f22;
                color: #e6e6e6;
            }
            QLabel {
                color: #e6e6e6;
                background-color: transparent;
            }
            QMenuBar, QMenu { background-color: #25262a; color: #e6e6e6; font-size: 12px; }
            QMenuBar::item { background: transparent; padding: 4px 8px; }
            QMenuBar::item:selected { background: #313844; color: #ffffff; }
            QMenu { border: 1px solid #3a3d44; }
            QMenu::item { background: transparent; padding: 6px 24px 6px 20px; }
            QMenu::item:selected { background: #3b5f8a; color: #ffffff; }
            QDockWidget {
                background-color: transparent;
                border: none;
            }
            QDockWidget::title {
                background-color: #2a2d33;
                color: #dfe3ea;
                padding: 6px 8px;
                font-weight: 600;
                border: 1px solid #3a3d44;
                border-bottom: 2px solid #3a3d44;
            }
            QDockWidget::close-button, QDockWidget::float-button {
                subcontrol-position: top right;
                margin: 2px;
            }
            QMainWindow::separator {
                background-color: #3a3d44;
                width: 4px;
                height: 4px;
            }
            QMainWindow::separator:hover {
                background-color: #4a5059;
            }
            QFrame#ribbon_frame {
                background-color: #232428;
                border: 1px solid #3a3d44;
                border-radius: 4px;
            }
            QFrame#viewer_workspace_frame {
                background-color: transparent;
                border: none;
                border-radius: 0px;
            }
            QDockWidget > QWidget,
            QWidget#tree_view_tree, QWidget#properties_view_prop, QWidget#task_view, QWidget#cfd_console_dock_contents {
                background-color: transparent;
            }
            QTabWidget#ribbon_tabs::pane {
                margin-top: 4px;
            }
            QToolBar {
                background-color: transparent;
                border: none;
                padding: 2px;
                spacing: 4px;
            }
            QToolButton, QToolBar QToolButton {
                background-color: transparent;
                color: #f0f0f0;
                border: none;
                padding: 4px 8px;
            }
            QToolButton:hover, QToolBar QToolButton:hover { 
                background-color: rgba(100, 100, 100, 0.10);
                border-radius: 4px;
            }
            QToolButton:pressed, QToolBar QToolButton:pressed { 
                background-color: rgba(100, 100, 100, 0.15);
            }
            QToolButton:disabled, QToolBar QToolButton:disabled {
                background-color: transparent;
                color: #707783;
                border: none;
            }
            QTabWidget::pane, QStackedWidget, QFrame[frameShape="StyledPanel"] {
                background-color: #232428;
                border: 1px solid #3a3d44;
                border-radius: 4px;
            }
            QTabWidget QWidget, QToolBox QWidget { color: #e6e6e6; }
            QTabBar::tab {
                background-color: #2a2d33;
                color: #dfe3ea;
                border: 1px solid #43474f;
                padding: 8px 12px;
                min-height: 24px;
                font-weight: 500;
            }
            QTabBar::tab:selected { background-color: #3a414d; color: #ffffff; }
            QTabBar::tab:hover { background-color: #353c47; }
            QToolBox::tab {
                background-color: #2a2d33;
                color: #dfe3ea;
                border: 1px solid #43474f;
                padding: 8px 10px;
                min-height: 22px;
                font-weight: 500;
            }
            QToolBox::tab:selected { background-color: #3a414d; color: #ffffff; }
            QGroupBox {
                border: 1px solid #3a3d44;
                border-radius: 4px;
                margin-top: 12px;
                padding: 10px 8px 8px 8px;
                background-color: #232428;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 6px;
                font-weight: 600;
                color: #dfe3ea;
            }
            QLineEdit, QPlainTextEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox, QListWidget, QTableView, QTreeView, QTreeWidget, QTableWidget {
                background-color: #2a2d33;
                color: #e6e6e6;
                border: 1px solid #43474f;
                selection-background-color: #3b5f8a;
                selection-color: #ffffff;
                padding: 4px 6px;
            }
            QComboBox::drop-down {
                background-color: #2a2d33;
                border-left: 1px solid #43474f;
                width: 20px;
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #2a2d33;
                color: #e6e6e6;
                border: 1px solid #43474f;
                selection-background-color: #3b5f8a;
                selection-color: #ffffff;
                padding: 2px 0px;
            }
            QComboBox QAbstractItemView::item {
                padding: 4px 6px;
                background-color: #2a2d33;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #353c47;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #3b5f8a;
            }
            QCheckBox { color: #e6e6e6; }
            QCheckBox::indicator,
            QTreeView::indicator,
            QTreeWidget::indicator,
            QTableView::indicator,
            QListView::indicator {
                image: none;
                width: 16px;
                height: 16px;
                border: 1px solid #5a6070;
                background-color: #232428;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked,
            QTreeView::indicator:checked,
            QTreeWidget::indicator:checked,
            QTableView::indicator:checked,
            QListView::indicator:checked {
                background-color: #232428;
                border: 1px solid #cfd5dd;
                image: url("__CHECKBOX_PATH__");
            }
            QCheckBox::indicator:indeterminate,
            QTreeView::indicator:indeterminate,
            QTreeWidget::indicator:indeterminate,
            QTableView::indicator:indeterminate,
            QListView::indicator:indeterminate {
                background-color: #4a4f59;
                border: 1px solid #6a6f7a;
            }
            QCheckBox::indicator:disabled,
            QTreeView::indicator:disabled,
            QTreeWidget::indicator:disabled,
            QTableView::indicator:disabled,
            QListView::indicator:disabled {
                background-color: #25282e;
                border: 1px solid #343841;
            }
            QScrollArea, QAbstractScrollArea, QAbstractScrollArea::viewport, QMdiArea, QMdiSubWindow {
                background-color: #232428;
                color: #e6e6e6;
            }
            QScrollArea > QWidget,
            QAbstractScrollArea > QWidget,
            QAbstractScrollArea QWidget {
                background-color: #232428;
                color: #e6e6e6;
            }
            QScrollArea::corner {
                background-color: #232428;
            }
            QViewport {
                background-color: #232428;
                color: #e6e6e6;
            }
            QWidget#task_task, QWidget#task {
                background-color: #232428;
                color: #e6e6e6;
            }
            QToolBar QWidget,
            QToolBar QLabel,
            QToolBar QFrame {
                background-color: transparent;
                color: #e6e6e6;
            }
            QPushButton {
                background-color: #31353d;
                color: #f0f0f0;
                border: 1px solid #4a4f59;
                padding: 4px 8px;
                border-radius: 2px;
            }
            QPushButton:hover { 
                background-color: #454d57;
                border: 1px solid #6a7080;
            }
            QPushButton:pressed { background-color: #2b2f36; }
            QPushButton:checked {
                background-color: #3b5f8a;
                color: #ffffff;
                border: 1px solid #6289bc;
            }
            QPushButton:disabled {
                background-color: #25282e;
                color: #707783;
                border: 1px solid #343841;
            }
            QComboBox:disabled, QLineEdit:disabled, QPlainTextEdit:disabled, QTextEdit:disabled,
            QSpinBox:disabled, QDoubleSpinBox:disabled {
                background-color: #25282e;
                color: #8a919b;
                border: 1px solid #343841;
            }
            QCheckBox:disabled, QGroupBox:disabled, QLabel:disabled {
                color: #8a919b;
            }
            QHeaderView::section {
                background-color: #2f333a;
                color: #e6e6e6;
                border: 1px solid #43474f;
                padding: 4px;
                font-weight: 600;
            }
            QTableView::item, QTreeView::item, QListView::item {
                padding: 4px 6px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #232428;
                border: 1px solid #3a3d44;
                margin: 0px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #4a4f59;
                border: 1px solid #5a6070;
                border-radius: 4px;
                min-height: 18px;
                min-width: 18px;
            }
            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
                background: #5a6070;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: #232428;
                border: 1px solid #3a3d44;
                width: 0px;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: #232428;
            }
            """
        app.setStyleSheet(stylesheet.replace("__CHECKBOX_PATH__", checkbox_path))
        center_tree_branches = bool(
            self.state.get("settings", {}).get("general", {}).get("center_tree_branches", True)
        )
        self._apply_tree_branch_styles(True, center_tree_branches)

    def _apply_tree_branch_styles(self, dark_mode, center_lines=True):
        branch = "#4a4f59" if bool(dark_mode) else "#b8c0cc"
        if not bool(center_lines):
            for tree in self.findChildren(QTreeView):
                tree.setStyleSheet("")
                tree.setRootIsDecorated(True)
            for tree in self.findChildren(QTreeWidget):
                tree.setStyleSheet("")
                tree.setRootIsDecorated(True)
            return
        midline = (
            "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 transparent, stop:0.49 transparent, stop:0.5 {branch}, "
            f"stop:0.52 {branch}, stop:0.53 transparent, stop:1 transparent)"
        )
        tree_style = f"""
            QTreeView::branch:has-siblings:!adjoins-item,
            QTreeWidget::branch:has-siblings:!adjoins-item {{
                border-left: 1px solid {branch};
            }}
            QTreeView::branch:has-siblings:adjoins-item,
            QTreeWidget::branch:has-siblings:adjoins-item {{
                border-left: 1px solid {branch};
                background: {midline};
            }}
            QTreeView::branch:!has-children:!has-siblings:adjoins-item,
            QTreeWidget::branch:!has-children:!has-siblings:adjoins-item {{
                background: {midline};
            }}
            QTreeView::branch:closed:has-children,
            QTreeWidget::branch:closed:has-children {{
                image: url(:/qt-project.org/styles/commonstyle/images/branch-closed.png);
            }}
            QTreeView::branch:open:has-children,
            QTreeWidget::branch:open:has-children {{
                image: url(:/qt-project.org/styles/commonstyle/images/branch-open.png);
            }}
        """
        for tree in self.findChildren(QTreeView):
            tree.setStyleSheet(tree_style)
            tree.setRootIsDecorated(True)
            tree.setIndentation(max(16, int(tree.indentation())))
        for tree in self.findChildren(QTreeWidget):
            tree.setStyleSheet(tree_style)
            tree.setRootIsDecorated(True)
            tree.setIndentation(max(16, int(tree.indentation())))

    def closeEvent(self, event):
        """Clean up resources when window closes."""
        if hasattr(self, 'ribbon_controller') and self.ribbon_controller is not None:
            self.ribbon_controller.cleanup()
        self._save_shell_state()
        super().closeEvent(event)

    def _create_preferences_dialog(self):
        return AerodynamicsPreferencesDialog(
            self,
            settings_path=("tabs", "aerodynamics"),
            background_label="Aerodynamics background",
            lighting_label="Aerodynamics lighting",
            render_mode_label="Surface Mesh Render",
            mesh_opacity_label="Surface Mesh Opacity",
        )


def main():
    app = QApplication(sys.argv)
    icon = load_icon()
    if icon is not None:
        app.setWindowIcon(icon)
    window = AeroWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
