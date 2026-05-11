# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aircraft_design.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QColumnView, QComboBox, QDockWidget,
    QDoubleSpinBox, QFormLayout, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMdiArea, QMenu, QMenuBar, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QStatusBar, QTabWidget, QTableView,
    QTableWidget, QTableWidgetItem, QToolBox, QTreeView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1097, 702)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionImport = QAction(MainWindow)
        self.actionImport.setObjectName(u"actionImport")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionCopy = QAction(MainWindow)
        self.actionCopy.setObjectName(u"actionCopy")
        self.actionPaste = QAction(MainWindow)
        self.actionPaste.setObjectName(u"actionPaste")
        self.actionToggle_Tree_View = QAction(MainWindow)
        self.actionToggle_Tree_View.setObjectName(u"actionToggle_Tree_View")
        self.actionToggle_Properties = QAction(MainWindow)
        self.actionToggle_Properties.setObjectName(u"actionToggle_Properties")
        self.actionToggle_Task = QAction(MainWindow)
        self.actionToggle_Task.setObjectName(u"actionToggle_Task")
        self.actionPreference = QAction(MainWindow)
        self.actionPreference.setObjectName(u"actionPreference")
        self.actionPreference_2 = QAction(MainWindow)
        self.actionPreference_2.setObjectName(u"actionPreference_2")
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionAbout_AerGenesis = QAction(MainWindow)
        self.actionAbout_AerGenesis.setObjectName(u"actionAbout_AerGenesis")
        self.actionRefresh = QAction(MainWindow)
        self.actionRefresh.setObjectName(u"actionRefresh")
        self.actionRecalculate = QAction(MainWindow)
        self.actionRecalculate.setObjectName(u"actionRecalculate")
        self.actionFind = QAction(MainWindow)
        self.actionFind.setObjectName(u"actionFind")
        self.actionInspect = QAction(MainWindow)
        self.actionInspect.setObjectName(u"actionInspect")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_8 = QGridLayout(self.centralwidget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.ribbon_frame = QFrame(self.centralwidget)
        self.ribbon_frame.setObjectName(u"ribbon_frame")
        self.ribbon_frame.setVisible(False)
        self.ribbon_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ribbon_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_ribbon_frame = QVBoxLayout(self.ribbon_frame)
        self.verticalLayout_ribbon_frame.setSpacing(6)
        self.verticalLayout_ribbon_frame.setObjectName(u"verticalLayout_ribbon_frame")
        self.verticalLayout_ribbon_frame.setContentsMargins(8, 8, 8, 8)
        self.ribbon_tabs = QTabWidget(self.ribbon_frame)
        self.ribbon_tabs.setObjectName(u"ribbon_tabs")
        self.ribbon_tabs.setDocumentMode(True)
        self.ribbon_home_tab = QWidget()
        self.ribbon_home_tab.setObjectName(u"ribbon_home_tab")
        self.horizontalLayout_ribbon_home = QHBoxLayout(self.ribbon_home_tab)
        self.horizontalLayout_ribbon_home.setSpacing(8)
        self.horizontalLayout_ribbon_home.setObjectName(u"horizontalLayout_ribbon_home")
        self.group_ribbon_home_case = QGroupBox(self.ribbon_home_tab)
        self.group_ribbon_home_case.setObjectName(u"group_ribbon_home_case")
        self.gridLayout_ribbon_home_case = QGridLayout(self.group_ribbon_home_case)
        self.gridLayout_ribbon_home_case.setObjectName(u"gridLayout_ribbon_home_case")
        self.btn_ribbon_import_case = QPushButton(self.group_ribbon_home_case)
        self.btn_ribbon_import_case.setObjectName(u"btn_ribbon_import_case")

        self.gridLayout_ribbon_home_case.addWidget(self.btn_ribbon_import_case, 0, 0, 1, 1)

        self.btn_ribbon_load_geometry = QPushButton(self.group_ribbon_home_case)
        self.btn_ribbon_load_geometry.setObjectName(u"btn_ribbon_load_geometry")

        self.gridLayout_ribbon_home_case.addWidget(self.btn_ribbon_load_geometry, 0, 1, 1, 1)

        self.btn_ribbon_save_config = QPushButton(self.group_ribbon_home_case)
        self.btn_ribbon_save_config.setObjectName(u"btn_ribbon_save_config")

        self.gridLayout_ribbon_home_case.addWidget(self.btn_ribbon_save_config, 1, 0, 1, 1)

        self.btn_ribbon_load_config = QPushButton(self.group_ribbon_home_case)
        self.btn_ribbon_load_config.setObjectName(u"btn_ribbon_load_config")

        self.gridLayout_ribbon_home_case.addWidget(self.btn_ribbon_load_config, 1, 1, 1, 1)

        self.btn_ribbon_export_case = QPushButton(self.group_ribbon_home_case)
        self.btn_ribbon_export_case.setObjectName(u"btn_ribbon_export_case")

        self.gridLayout_ribbon_home_case.addWidget(self.btn_ribbon_export_case, 2, 0, 1, 1)

        self.btn_ribbon_open_case_folder = QPushButton(self.group_ribbon_home_case)
        self.btn_ribbon_open_case_folder.setObjectName(u"btn_ribbon_open_case_folder")

        self.gridLayout_ribbon_home_case.addWidget(self.btn_ribbon_open_case_folder, 2, 1, 1, 1)


        self.horizontalLayout_ribbon_home.addWidget(self.group_ribbon_home_case)

        self.group_ribbon_home_workspace = QGroupBox(self.ribbon_home_tab)
        self.group_ribbon_home_workspace.setObjectName(u"group_ribbon_home_workspace")
        self.gridLayout_ribbon_home_workspace = QGridLayout(self.group_ribbon_home_workspace)
        self.gridLayout_ribbon_home_workspace.setObjectName(u"gridLayout_ribbon_home_workspace")
        self.btn_ribbon_toggle_tree = QPushButton(self.group_ribbon_home_workspace)
        self.btn_ribbon_toggle_tree.setObjectName(u"btn_ribbon_toggle_tree")
        self.btn_ribbon_toggle_tree.setCheckable(True)

        self.gridLayout_ribbon_home_workspace.addWidget(self.btn_ribbon_toggle_tree, 0, 0, 1, 1)

        self.btn_ribbon_toggle_properties = QPushButton(self.group_ribbon_home_workspace)
        self.btn_ribbon_toggle_properties.setObjectName(u"btn_ribbon_toggle_properties")
        self.btn_ribbon_toggle_properties.setCheckable(True)

        self.gridLayout_ribbon_home_workspace.addWidget(self.btn_ribbon_toggle_properties, 0, 1, 1, 1)

        self.btn_ribbon_toggle_task = QPushButton(self.group_ribbon_home_workspace)
        self.btn_ribbon_toggle_task.setObjectName(u"btn_ribbon_toggle_task")
        self.btn_ribbon_toggle_task.setCheckable(True)

        self.gridLayout_ribbon_home_workspace.addWidget(self.btn_ribbon_toggle_task, 0, 2, 1, 1)

        self.btn_ribbon_show_console = QPushButton(self.group_ribbon_home_workspace)
        self.btn_ribbon_show_console.setObjectName(u"btn_ribbon_show_console")
        self.btn_ribbon_show_console.setCheckable(True)

        self.gridLayout_ribbon_home_workspace.addWidget(self.btn_ribbon_show_console, 1, 0, 1, 1)

        self.btn_ribbon_reset_layout = QPushButton(self.group_ribbon_home_workspace)
        self.btn_ribbon_reset_layout.setObjectName(u"btn_ribbon_reset_layout")

        self.gridLayout_ribbon_home_workspace.addWidget(self.btn_ribbon_reset_layout, 1, 1, 1, 2)


        self.horizontalLayout_ribbon_home.addWidget(self.group_ribbon_home_workspace)

        self.group_ribbon_home_camera = QGroupBox(self.ribbon_home_tab)
        self.group_ribbon_home_camera.setObjectName(u"group_ribbon_home_camera")
        self.gridLayout_ribbon_home_camera = QGridLayout(self.group_ribbon_home_camera)
        self.gridLayout_ribbon_home_camera.setObjectName(u"gridLayout_ribbon_home_camera")
        self.btn_ribbon_reset_camera = QPushButton(self.group_ribbon_home_camera)
        self.btn_ribbon_reset_camera.setObjectName(u"btn_ribbon_reset_camera")

        self.gridLayout_ribbon_home_camera.addWidget(self.btn_ribbon_reset_camera, 0, 0, 1, 1)

        self.btn_ribbon_view_front = QPushButton(self.group_ribbon_home_camera)
        self.btn_ribbon_view_front.setObjectName(u"btn_ribbon_view_front")

        self.gridLayout_ribbon_home_camera.addWidget(self.btn_ribbon_view_front, 0, 1, 1, 1)

        self.btn_ribbon_view_top = QPushButton(self.group_ribbon_home_camera)
        self.btn_ribbon_view_top.setObjectName(u"btn_ribbon_view_top")

        self.gridLayout_ribbon_home_camera.addWidget(self.btn_ribbon_view_top, 1, 0, 1, 1)

        self.btn_ribbon_view_side = QPushButton(self.group_ribbon_home_camera)
        self.btn_ribbon_view_side.setObjectName(u"btn_ribbon_view_side")

        self.gridLayout_ribbon_home_camera.addWidget(self.btn_ribbon_view_side, 1, 1, 1, 1)


        self.horizontalLayout_ribbon_home.addWidget(self.group_ribbon_home_camera)

        self.horizontalSpacer_ribbon_home = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_ribbon_home.addItem(self.horizontalSpacer_ribbon_home)

        self.ribbon_tabs.addTab(self.ribbon_home_tab, "")
        self.ribbon_mesh_tab = QWidget()
        self.ribbon_mesh_tab.setObjectName(u"ribbon_mesh_tab")
        self.horizontalLayout_ribbon_mesh = QHBoxLayout(self.ribbon_mesh_tab)
        self.horizontalLayout_ribbon_mesh.setSpacing(8)
        self.horizontalLayout_ribbon_mesh.setObjectName(u"horizontalLayout_ribbon_mesh")
        self.group_ribbon_mesh_panels = QGroupBox(self.ribbon_mesh_tab)
        self.group_ribbon_mesh_panels.setObjectName(u"group_ribbon_mesh_panels")
        self.gridLayout_ribbon_mesh_panels = QGridLayout(self.group_ribbon_mesh_panels)
        self.gridLayout_ribbon_mesh_panels.setObjectName(u"gridLayout_ribbon_mesh_panels")
        self.btn_ribbon_show_geometry_panel = QPushButton(self.group_ribbon_mesh_panels)
        self.btn_ribbon_show_geometry_panel.setObjectName(u"btn_ribbon_show_geometry_panel")

        self.gridLayout_ribbon_mesh_panels.addWidget(self.btn_ribbon_show_geometry_panel, 0, 0, 1, 1)

        self.btn_ribbon_show_mesh_panel = QPushButton(self.group_ribbon_mesh_panels)
        self.btn_ribbon_show_mesh_panel.setObjectName(u"btn_ribbon_show_mesh_panel")

        self.gridLayout_ribbon_mesh_panels.addWidget(self.btn_ribbon_show_mesh_panel, 0, 1, 1, 1)

        self.btn_ribbon_show_snappy_panel = QPushButton(self.group_ribbon_mesh_panels)
        self.btn_ribbon_show_snappy_panel.setObjectName(u"btn_ribbon_show_snappy_panel")

        self.gridLayout_ribbon_mesh_panels.addWidget(self.btn_ribbon_show_snappy_panel, 1, 0, 1, 1)

        self.btn_ribbon_show_checkmesh_panel = QPushButton(self.group_ribbon_mesh_panels)
        self.btn_ribbon_show_checkmesh_panel.setObjectName(u"btn_ribbon_show_checkmesh_panel")

        self.gridLayout_ribbon_mesh_panels.addWidget(self.btn_ribbon_show_checkmesh_panel, 1, 1, 1, 1)


        self.horizontalLayout_ribbon_mesh.addWidget(self.group_ribbon_mesh_panels)

        self.group_ribbon_mesh_case = QGroupBox(self.ribbon_mesh_tab)
        self.group_ribbon_mesh_case.setObjectName(u"group_ribbon_mesh_case")
        self.gridLayout_ribbon_mesh_case = QGridLayout(self.group_ribbon_mesh_case)
        self.gridLayout_ribbon_mesh_case.setObjectName(u"gridLayout_ribbon_mesh_case")
        self.btn_ribbon_generate_case = QPushButton(self.group_ribbon_mesh_case)
        self.btn_ribbon_generate_case.setObjectName(u"btn_ribbon_generate_case")

        self.gridLayout_ribbon_mesh_case.addWidget(self.btn_ribbon_generate_case, 0, 0, 1, 1)

        self.btn_ribbon_update_case = QPushButton(self.group_ribbon_mesh_case)
        self.btn_ribbon_update_case.setObjectName(u"btn_ribbon_update_case")

        self.gridLayout_ribbon_mesh_case.addWidget(self.btn_ribbon_update_case, 0, 1, 1, 1)

        self.btn_ribbon_clean_case = QPushButton(self.group_ribbon_mesh_case)
        self.btn_ribbon_clean_case.setObjectName(u"btn_ribbon_clean_case")

        self.gridLayout_ribbon_mesh_case.addWidget(self.btn_ribbon_clean_case, 1, 0, 1, 1)

        self.btn_ribbon_mesh_advice = QPushButton(self.group_ribbon_mesh_case)
        self.btn_ribbon_mesh_advice.setObjectName(u"btn_ribbon_mesh_advice")

        self.gridLayout_ribbon_mesh_case.addWidget(self.btn_ribbon_mesh_advice, 1, 1, 1, 1)


        self.horizontalLayout_ribbon_mesh.addWidget(self.group_ribbon_mesh_case)

        self.group_ribbon_mesh_execute = QGroupBox(self.ribbon_mesh_tab)
        self.group_ribbon_mesh_execute.setObjectName(u"group_ribbon_mesh_execute")
        self.gridLayout_ribbon_mesh_execute = QGridLayout(self.group_ribbon_mesh_execute)
        self.gridLayout_ribbon_mesh_execute.setObjectName(u"gridLayout_ribbon_mesh_execute")
        self.btn_ribbon_run_domain_mesh = QPushButton(self.group_ribbon_mesh_execute)
        self.btn_ribbon_run_domain_mesh.setObjectName(u"btn_ribbon_run_domain_mesh")

        self.gridLayout_ribbon_mesh_execute.addWidget(self.btn_ribbon_run_domain_mesh, 0, 0, 1, 1)

        self.btn_ribbon_run_surface_features = QPushButton(self.group_ribbon_mesh_execute)
        self.btn_ribbon_run_surface_features.setObjectName(u"btn_ribbon_run_surface_features")

        self.gridLayout_ribbon_mesh_execute.addWidget(self.btn_ribbon_run_surface_features, 0, 1, 1, 1)

        self.btn_ribbon_run_snappy_mesh = QPushButton(self.group_ribbon_mesh_execute)
        self.btn_ribbon_run_snappy_mesh.setObjectName(u"btn_ribbon_run_snappy_mesh")

        self.gridLayout_ribbon_mesh_execute.addWidget(self.btn_ribbon_run_snappy_mesh, 1, 0, 1, 1)

        self.btn_ribbon_run_checkmesh = QPushButton(self.group_ribbon_mesh_execute)
        self.btn_ribbon_run_checkmesh.setObjectName(u"btn_ribbon_run_checkmesh")

        self.gridLayout_ribbon_mesh_execute.addWidget(self.btn_ribbon_run_checkmesh, 1, 1, 1, 1)


        self.horizontalLayout_ribbon_mesh.addWidget(self.group_ribbon_mesh_execute)

        self.horizontalSpacer_ribbon_mesh = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_ribbon_mesh.addItem(self.horizontalSpacer_ribbon_mesh)

        self.ribbon_tabs.addTab(self.ribbon_mesh_tab, "")
        self.ribbon_run_tab = QWidget()
        self.ribbon_run_tab.setObjectName(u"ribbon_run_tab")
        self.horizontalLayout_ribbon_run = QHBoxLayout(self.ribbon_run_tab)
        self.horizontalLayout_ribbon_run.setSpacing(8)
        self.horizontalLayout_ribbon_run.setObjectName(u"horizontalLayout_ribbon_run")
        self.group_ribbon_run_stage = QGroupBox(self.ribbon_run_tab)
        self.group_ribbon_run_stage.setObjectName(u"group_ribbon_run_stage")
        self.gridLayout_ribbon_run_stage = QGridLayout(self.group_ribbon_run_stage)
        self.gridLayout_ribbon_run_stage.setObjectName(u"gridLayout_ribbon_run_stage")
        self.lbl_ribbon_solver = QLabel(self.group_ribbon_run_stage)
        self.lbl_ribbon_solver.setObjectName(u"lbl_ribbon_solver")

        self.gridLayout_ribbon_run_stage.addWidget(self.lbl_ribbon_solver, 0, 0, 1, 1)

        self.cmb_ribbon_solver = QComboBox(self.group_ribbon_run_stage)
        self.cmb_ribbon_solver.setObjectName(u"cmb_ribbon_solver")

        self.gridLayout_ribbon_run_stage.addWidget(self.cmb_ribbon_solver, 0, 1, 1, 1)

        self.lbl_ribbon_stage = QLabel(self.group_ribbon_run_stage)
        self.lbl_ribbon_stage.setObjectName(u"lbl_ribbon_stage")

        self.gridLayout_ribbon_run_stage.addWidget(self.lbl_ribbon_stage, 1, 0, 1, 1)

        self.cmb_ribbon_stage = QComboBox(self.group_ribbon_run_stage)
        self.cmb_ribbon_stage.setObjectName(u"cmb_ribbon_stage")

        self.gridLayout_ribbon_run_stage.addWidget(self.cmb_ribbon_stage, 1, 1, 1, 1)

        self.btn_ribbon_run_selected = QPushButton(self.group_ribbon_run_stage)
        self.btn_ribbon_run_selected.setObjectName(u"btn_ribbon_run_selected")

        self.gridLayout_ribbon_run_stage.addWidget(self.btn_ribbon_run_selected, 2, 0, 1, 1)

        self.btn_ribbon_run_pipeline = QPushButton(self.group_ribbon_run_stage)
        self.btn_ribbon_run_pipeline.setObjectName(u"btn_ribbon_run_pipeline")

        self.gridLayout_ribbon_run_stage.addWidget(self.btn_ribbon_run_pipeline, 2, 1, 1, 1)

        self.btn_ribbon_run_solve = QPushButton(self.group_ribbon_run_stage)
        self.btn_ribbon_run_solve.setObjectName(u"btn_ribbon_run_solve")

        self.gridLayout_ribbon_run_stage.addWidget(self.btn_ribbon_run_solve, 3, 0, 1, 1)

        self.btn_ribbon_run_post = QPushButton(self.group_ribbon_run_stage)
        self.btn_ribbon_run_post.setObjectName(u"btn_ribbon_run_post")

        self.gridLayout_ribbon_run_stage.addWidget(self.btn_ribbon_run_post, 3, 1, 1, 1)


        self.horizontalLayout_ribbon_run.addWidget(self.group_ribbon_run_stage)

        self.group_ribbon_run_logs = QGroupBox(self.ribbon_run_tab)
        self.group_ribbon_run_logs.setObjectName(u"group_ribbon_run_logs")
        self.gridLayout_ribbon_run_logs = QGridLayout(self.group_ribbon_run_logs)
        self.gridLayout_ribbon_run_logs.setObjectName(u"gridLayout_ribbon_run_logs")
        self.btn_ribbon_stop_run = QPushButton(self.group_ribbon_run_logs)
        self.btn_ribbon_stop_run.setObjectName(u"btn_ribbon_stop_run")

        self.gridLayout_ribbon_run_logs.addWidget(self.btn_ribbon_stop_run, 0, 0, 1, 1)

        self.btn_ribbon_clear_console = QPushButton(self.group_ribbon_run_logs)
        self.btn_ribbon_clear_console.setObjectName(u"btn_ribbon_clear_console")

        self.gridLayout_ribbon_run_logs.addWidget(self.btn_ribbon_clear_console, 0, 1, 1, 1)

        self.btn_ribbon_open_latest_log = QPushButton(self.group_ribbon_run_logs)
        self.btn_ribbon_open_latest_log.setObjectName(u"btn_ribbon_open_latest_log")

        self.gridLayout_ribbon_run_logs.addWidget(self.btn_ribbon_open_latest_log, 1, 0, 1, 2)


        self.horizontalLayout_ribbon_run.addWidget(self.group_ribbon_run_logs)

        self.group_ribbon_run_status = QGroupBox(self.ribbon_run_tab)
        self.group_ribbon_run_status.setObjectName(u"group_ribbon_run_status")
        self.formLayout_ribbon_run_status = QFormLayout(self.group_ribbon_run_status)
        self.formLayout_ribbon_run_status.setObjectName(u"formLayout_ribbon_run_status")
        self.lbl_ribbon_run_status_label = QLabel(self.group_ribbon_run_status)
        self.lbl_ribbon_run_status_label.setObjectName(u"lbl_ribbon_run_status_label")

        self.formLayout_ribbon_run_status.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_ribbon_run_status_label)

        self.lbl_ribbon_run_status_value = QLabel(self.group_ribbon_run_status)
        self.lbl_ribbon_run_status_value.setObjectName(u"lbl_ribbon_run_status_value")

        self.formLayout_ribbon_run_status.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lbl_ribbon_run_status_value)

        self.lbl_ribbon_active_stage_label = QLabel(self.group_ribbon_run_status)
        self.lbl_ribbon_active_stage_label.setObjectName(u"lbl_ribbon_active_stage_label")

        self.formLayout_ribbon_run_status.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_ribbon_active_stage_label)

        self.lbl_ribbon_active_stage_value = QLabel(self.group_ribbon_run_status)
        self.lbl_ribbon_active_stage_value.setObjectName(u"lbl_ribbon_active_stage_value")

        self.formLayout_ribbon_run_status.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lbl_ribbon_active_stage_value)


        self.horizontalLayout_ribbon_run.addWidget(self.group_ribbon_run_status)

        self.horizontalSpacer_ribbon_run = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_ribbon_run.addItem(self.horizontalSpacer_ribbon_run)

        self.ribbon_tabs.addTab(self.ribbon_run_tab, "")
        self.ribbon_results_tab = QWidget()
        self.ribbon_results_tab.setObjectName(u"ribbon_results_tab")
        self.horizontalLayout_ribbon_results = QHBoxLayout(self.ribbon_results_tab)
        self.horizontalLayout_ribbon_results.setSpacing(8)
        self.horizontalLayout_ribbon_results.setObjectName(u"horizontalLayout_ribbon_results")
        self.group_ribbon_results_data = QGroupBox(self.ribbon_results_tab)
        self.group_ribbon_results_data.setObjectName(u"group_ribbon_results_data")
        self.gridLayout_ribbon_results_data = QGridLayout(self.group_ribbon_results_data)
        self.gridLayout_ribbon_results_data.setObjectName(u"gridLayout_ribbon_results_data")
        self.btn_ribbon_scan_results = QPushButton(self.group_ribbon_results_data)
        self.btn_ribbon_scan_results.setObjectName(u"btn_ribbon_scan_results")

        self.gridLayout_ribbon_results_data.addWidget(self.btn_ribbon_scan_results, 0, 0, 1, 1)

        self.btn_ribbon_open_paraview = QPushButton(self.group_ribbon_results_data)
        self.btn_ribbon_open_paraview.setObjectName(u"btn_ribbon_open_paraview")

        self.gridLayout_ribbon_results_data.addWidget(self.btn_ribbon_open_paraview, 0, 1, 1, 1)

        self.cmb_ribbon_vtk_target = QComboBox(self.group_ribbon_results_data)
        self.cmb_ribbon_vtk_target.setObjectName(u"cmb_ribbon_vtk_target")

        self.gridLayout_ribbon_results_data.addWidget(self.cmb_ribbon_vtk_target, 1, 0, 1, 1)

        self.btn_ribbon_export_vtk = QPushButton(self.group_ribbon_results_data)
        self.btn_ribbon_export_vtk.setObjectName(u"btn_ribbon_export_vtk")

        self.gridLayout_ribbon_results_data.addWidget(self.btn_ribbon_export_vtk, 1, 1, 1, 1)

        self.btn_ribbon_load_vtk = QPushButton(self.group_ribbon_results_data)
        self.btn_ribbon_load_vtk.setObjectName(u"btn_ribbon_load_vtk")

        self.gridLayout_ribbon_results_data.addWidget(self.btn_ribbon_load_vtk, 2, 0, 1, 2)


        self.horizontalLayout_ribbon_results.addWidget(self.group_ribbon_results_data)

        self.group_ribbon_results_fields = QGroupBox(self.ribbon_results_tab)
        self.group_ribbon_results_fields.setObjectName(u"group_ribbon_results_fields")
        self.gridLayout_ribbon_results_fields = QGridLayout(self.group_ribbon_results_fields)
        self.gridLayout_ribbon_results_fields.setObjectName(u"gridLayout_ribbon_results_fields")
        self.btn_ribbon_result_pressure = QPushButton(self.group_ribbon_results_fields)
        self.btn_ribbon_result_pressure.setObjectName(u"btn_ribbon_result_pressure")

        self.gridLayout_ribbon_results_fields.addWidget(self.btn_ribbon_result_pressure, 0, 0, 1, 1)

        self.btn_ribbon_result_velocity = QPushButton(self.group_ribbon_results_fields)
        self.btn_ribbon_result_velocity.setObjectName(u"btn_ribbon_result_velocity")

        self.gridLayout_ribbon_results_fields.addWidget(self.btn_ribbon_result_velocity, 0, 1, 1, 1)

        self.cmb_ribbon_result_field = QComboBox(self.group_ribbon_results_fields)
        self.cmb_ribbon_result_field.setObjectName(u"cmb_ribbon_result_field")

        self.gridLayout_ribbon_results_fields.addWidget(self.cmb_ribbon_result_field, 1, 0, 1, 2)

        self.btn_ribbon_apply_field = QPushButton(self.group_ribbon_results_fields)
        self.btn_ribbon_apply_field.setObjectName(u"btn_ribbon_apply_field")

        self.gridLayout_ribbon_results_fields.addWidget(self.btn_ribbon_apply_field, 2, 0, 1, 2)


        self.horizontalLayout_ribbon_results.addWidget(self.group_ribbon_results_fields)

        self.group_ribbon_results_view = QGroupBox(self.ribbon_results_tab)
        self.group_ribbon_results_view.setObjectName(u"group_ribbon_results_view")
        self.gridLayout_ribbon_results_view = QGridLayout(self.group_ribbon_results_view)
        self.gridLayout_ribbon_results_view.setObjectName(u"gridLayout_ribbon_results_view")
        self.btn_ribbon_surface_mode = QPushButton(self.group_ribbon_results_view)
        self.btn_ribbon_surface_mode.setObjectName(u"btn_ribbon_surface_mode")
        self.btn_ribbon_surface_mode.setCheckable(True)

        self.gridLayout_ribbon_results_view.addWidget(self.btn_ribbon_surface_mode, 0, 0, 1, 1)

        self.btn_ribbon_wireframe_mode = QPushButton(self.group_ribbon_results_view)
        self.btn_ribbon_wireframe_mode.setObjectName(u"btn_ribbon_wireframe_mode")
        self.btn_ribbon_wireframe_mode.setCheckable(True)

        self.gridLayout_ribbon_results_view.addWidget(self.btn_ribbon_wireframe_mode, 0, 1, 1, 1)

        self.btn_ribbon_toggle_contours = QPushButton(self.group_ribbon_results_view)
        self.btn_ribbon_toggle_contours.setObjectName(u"btn_ribbon_toggle_contours")
        self.btn_ribbon_toggle_contours.setCheckable(True)

        self.gridLayout_ribbon_results_view.addWidget(self.btn_ribbon_toggle_contours, 1, 0, 1, 1)

        self.btn_ribbon_toggle_slice = QPushButton(self.group_ribbon_results_view)
        self.btn_ribbon_toggle_slice.setObjectName(u"btn_ribbon_toggle_slice")
        self.btn_ribbon_toggle_slice.setCheckable(True)

        self.gridLayout_ribbon_results_view.addWidget(self.btn_ribbon_toggle_slice, 1, 1, 1, 1)

        self.btn_ribbon_toggle_streamlines = QPushButton(self.group_ribbon_results_view)
        self.btn_ribbon_toggle_streamlines.setObjectName(u"btn_ribbon_toggle_streamlines")
        self.btn_ribbon_toggle_streamlines.setCheckable(True)

        self.gridLayout_ribbon_results_view.addWidget(self.btn_ribbon_toggle_streamlines, 2, 0, 1, 1)

        self.btn_ribbon_toggle_tripod = QPushButton(self.group_ribbon_results_view)
        self.btn_ribbon_toggle_tripod.setObjectName(u"btn_ribbon_toggle_tripod")
        self.btn_ribbon_toggle_tripod.setCheckable(True)
        self.btn_ribbon_toggle_tripod.setChecked(True)

        self.gridLayout_ribbon_results_view.addWidget(self.btn_ribbon_toggle_tripod, 2, 1, 1, 1)

        self.btn_ribbon_screenshot = QPushButton(self.group_ribbon_results_view)
        self.btn_ribbon_screenshot.setObjectName(u"btn_ribbon_screenshot")

        self.gridLayout_ribbon_results_view.addWidget(self.btn_ribbon_screenshot, 3, 0, 1, 2)


        self.horizontalLayout_ribbon_results.addWidget(self.group_ribbon_results_view)

        self.horizontalSpacer_ribbon_results = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_ribbon_results.addItem(self.horizontalSpacer_ribbon_results)

        self.ribbon_tabs.addTab(self.ribbon_results_tab, "")

        self.verticalLayout_ribbon_frame.addWidget(self.ribbon_tabs)


        self.gridLayout_8.addWidget(self.ribbon_frame, 0, 0, 1, 1)

        self.viewer_workspace_frame = QFrame(self.centralwidget)
        self.viewer_workspace_frame.setObjectName(u"viewer_workspace_frame")
        self.viewer_workspace_frame.setVisible(False)
        self.viewer_workspace_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.viewer_workspace_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_viewer_workspace = QVBoxLayout(self.viewer_workspace_frame)
        self.verticalLayout_viewer_workspace.setObjectName(u"verticalLayout_viewer_workspace")
        self.verticalLayout_viewer_workspace.setContentsMargins(0, 0, 0, 0)
        self.viewer_host = QWidget(self.viewer_workspace_frame)
        self.viewer_host.setObjectName(u"viewer_host")

        self.verticalLayout_viewer_workspace.addWidget(self.viewer_host)


        self.gridLayout_8.addWidget(self.viewer_workspace_frame, 1, 0, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.prelim_tab = QWidget()
        self.prelim_tab.setObjectName(u"prelim_tab")
        self.gridLayout_15 = QGridLayout(self.prelim_tab)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.toolbox_preliminary_sizing = QToolBox(self.prelim_tab)
        self.toolbox_preliminary_sizing.setObjectName(u"toolbox_preliminary_sizing")
        self.page_constraints = QWidget()
        self.page_constraints.setObjectName(u"page_constraints")
        self.page_constraints.setGeometry(QRect(0, 0, 628, 414))
        self.gridLayout_6 = QGridLayout(self.page_constraints)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.input_k_ld = QLineEdit(self.page_constraints)
        self.input_k_ld.setObjectName(u"input_k_ld")

        self.gridLayout_6.addWidget(self.input_k_ld, 17, 2, 1, 1)

        self.lbl_takeoff_distance = QLabel(self.page_constraints)
        self.lbl_takeoff_distance.setObjectName(u"lbl_takeoff_distance")

        self.gridLayout_6.addWidget(self.lbl_takeoff_distance, 6, 0, 1, 1)

        self.input_stall_speed = QLineEdit(self.page_constraints)
        self.input_stall_speed.setObjectName(u"input_stall_speed")

        self.gridLayout_6.addWidget(self.input_stall_speed, 4, 2, 1, 1)

        self.lbl_swet_sref_ratio = QLabel(self.page_constraints)
        self.lbl_swet_sref_ratio.setObjectName(u"lbl_swet_sref_ratio")

        self.gridLayout_6.addWidget(self.lbl_swet_sref_ratio, 18, 0, 1, 1)

        self.input_payload_weight = QLineEdit(self.page_constraints)
        self.input_payload_weight.setObjectName(u"input_payload_weight")

        self.gridLayout_6.addWidget(self.input_payload_weight, 8, 2, 1, 1)

        self.input_rate_of_climb = QLineEdit(self.page_constraints)
        self.input_rate_of_climb.setObjectName(u"input_rate_of_climb")

        self.gridLayout_6.addWidget(self.input_rate_of_climb, 9, 2, 1, 1)

        self.lbl_payload_weight = QLabel(self.page_constraints)
        self.lbl_payload_weight.setObjectName(u"lbl_payload_weight")

        self.gridLayout_6.addWidget(self.lbl_payload_weight, 8, 0, 1, 1)

        self.lbl_maximum_velocity_unit = QLabel(self.page_constraints)
        self.lbl_maximum_velocity_unit.setObjectName(u"lbl_maximum_velocity_unit")

        self.gridLayout_6.addWidget(self.lbl_maximum_velocity_unit, 5, 3, 1, 1)

        self.lbl_stall_speed = QLabel(self.page_constraints)
        self.lbl_stall_speed.setObjectName(u"lbl_stall_speed")

        self.gridLayout_6.addWidget(self.lbl_stall_speed, 4, 0, 1, 1)

        self.lbl_geometric_constraints_section = QLabel(self.page_constraints)
        self.lbl_geometric_constraints_section.setObjectName(u"lbl_geometric_constraints_section")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_geometric_constraints_section.sizePolicy().hasHeightForWidth())
        self.lbl_geometric_constraints_section.setSizePolicy(sizePolicy)
        self.lbl_geometric_constraints_section.setMinimumSize(QSize(6, 8))
        self.lbl_geometric_constraints_section.setFrameShape(QFrame.Shape.NoFrame)

        self.gridLayout_6.addWidget(self.lbl_geometric_constraints_section, 14, 0, 1, 1)

        self.input_swet_sref_ratio = QLineEdit(self.page_constraints)
        self.input_swet_sref_ratio.setObjectName(u"input_swet_sref_ratio")

        self.gridLayout_6.addWidget(self.input_swet_sref_ratio, 18, 2, 1, 1)

        self.lbl_maximum_velocity = QLabel(self.page_constraints)
        self.lbl_maximum_velocity.setObjectName(u"lbl_maximum_velocity")

        self.gridLayout_6.addWidget(self.lbl_maximum_velocity, 5, 0, 1, 1)

        self.btn_calculate_constraints = QPushButton(self.page_constraints)
        self.btn_calculate_constraints.setObjectName(u"btn_calculate_constraints")

        self.gridLayout_6.addWidget(self.btn_calculate_constraints, 0, 4, 1, 1)

        self.line_geometric_constraints = QFrame(self.page_constraints)
        self.line_geometric_constraints.setObjectName(u"line_geometric_constraints")
        self.line_geometric_constraints.setFrameShape(QFrame.Shape.HLine)
        self.line_geometric_constraints.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_6.addWidget(self.line_geometric_constraints, 15, 0, 1, 5)

        self.lbl_stall_speed_unit = QLabel(self.page_constraints)
        self.lbl_stall_speed_unit.setObjectName(u"lbl_stall_speed_unit")

        self.gridLayout_6.addWidget(self.lbl_stall_speed_unit, 4, 3, 1, 1)

        self.lbl_payload_weight_unit = QLabel(self.page_constraints)
        self.lbl_payload_weight_unit.setObjectName(u"lbl_payload_weight_unit")

        self.gridLayout_6.addWidget(self.lbl_payload_weight_unit, 8, 3, 1, 1)

        self.input_aspect_ratio = QLineEdit(self.page_constraints)
        self.input_aspect_ratio.setObjectName(u"input_aspect_ratio")

        self.gridLayout_6.addWidget(self.input_aspect_ratio, 16, 2, 1, 1)

        self.input_crew_passenger_weight = QLineEdit(self.page_constraints)
        self.input_crew_passenger_weight.setObjectName(u"input_crew_passenger_weight")

        self.gridLayout_6.addWidget(self.input_crew_passenger_weight, 7, 2, 1, 1)

        self.lbl_crew_passenger_weight = QLabel(self.page_constraints)
        self.lbl_crew_passenger_weight.setObjectName(u"lbl_crew_passenger_weight")

        self.gridLayout_6.addWidget(self.lbl_crew_passenger_weight, 7, 0, 1, 1)

        self.input_range = QLineEdit(self.page_constraints)
        self.input_range.setObjectName(u"input_range")

        self.gridLayout_6.addWidget(self.input_range, 2, 2, 1, 1)

        self.input_maximum_velocity = QLineEdit(self.page_constraints)
        self.input_maximum_velocity.setObjectName(u"input_maximum_velocity")

        self.gridLayout_6.addWidget(self.input_maximum_velocity, 5, 2, 1, 1)

        self.lbl_aspect_ratio = QLabel(self.page_constraints)
        self.lbl_aspect_ratio.setObjectName(u"lbl_aspect_ratio")

        self.gridLayout_6.addWidget(self.lbl_aspect_ratio, 16, 0, 1, 1)

        self.lbl_endurance_unit = QLabel(self.page_constraints)
        self.lbl_endurance_unit.setObjectName(u"lbl_endurance_unit")

        self.gridLayout_6.addWidget(self.lbl_endurance_unit, 3, 3, 1, 1)

        self.line_performance_constraints = QFrame(self.page_constraints)
        self.line_performance_constraints.setObjectName(u"line_performance_constraints")
        self.line_performance_constraints.setFrameShape(QFrame.Shape.HLine)
        self.line_performance_constraints.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_6.addWidget(self.line_performance_constraints, 1, 0, 1, 5)

        self.lbl_performance_constraints_section = QLabel(self.page_constraints)
        self.lbl_performance_constraints_section.setObjectName(u"lbl_performance_constraints_section")
        sizePolicy.setHeightForWidth(self.lbl_performance_constraints_section.sizePolicy().hasHeightForWidth())
        self.lbl_performance_constraints_section.setSizePolicy(sizePolicy)

        self.gridLayout_6.addWidget(self.lbl_performance_constraints_section, 0, 0, 1, 1)

        self.lbl_crew_passenger_weight_unit = QLabel(self.page_constraints)
        self.lbl_crew_passenger_weight_unit.setObjectName(u"lbl_crew_passenger_weight_unit")

        self.gridLayout_6.addWidget(self.lbl_crew_passenger_weight_unit, 7, 3, 1, 1)

        self.lbl_endurance = QLabel(self.page_constraints)
        self.lbl_endurance.setObjectName(u"lbl_endurance")

        self.gridLayout_6.addWidget(self.lbl_endurance, 3, 0, 1, 1)

        self.lbl_takeoff_distance_unit = QLabel(self.page_constraints)
        self.lbl_takeoff_distance_unit.setObjectName(u"lbl_takeoff_distance_unit")

        self.gridLayout_6.addWidget(self.lbl_takeoff_distance_unit, 6, 3, 1, 1)

        self.lbl_range_unit = QLabel(self.page_constraints)
        self.lbl_range_unit.setObjectName(u"lbl_range_unit")

        self.gridLayout_6.addWidget(self.lbl_range_unit, 2, 3, 1, 1)

        self.lbl_range = QLabel(self.page_constraints)
        self.lbl_range.setObjectName(u"lbl_range")

        self.gridLayout_6.addWidget(self.lbl_range, 2, 0, 1, 1)

        self.label_k_ld = QLabel(self.page_constraints)
        self.label_k_ld.setObjectName(u"label_k_ld")

        self.gridLayout_6.addWidget(self.label_k_ld, 17, 0, 1, 1)

        self.input_takeoff_distance = QLineEdit(self.page_constraints)
        self.input_takeoff_distance.setObjectName(u"input_takeoff_distance")

        self.gridLayout_6.addWidget(self.input_takeoff_distance, 6, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer, 2, 1, 8, 1)

        self.label_k_ld_unit = QLabel(self.page_constraints)
        self.label_k_ld_unit.setObjectName(u"label_k_ld_unit")

        self.gridLayout_6.addWidget(self.label_k_ld_unit, 17, 3, 1, 1)

        self.input_endurance = QLineEdit(self.page_constraints)
        self.input_endurance.setObjectName(u"input_endurance")

        self.gridLayout_6.addWidget(self.input_endurance, 3, 2, 1, 1)

        self.line_before_geometric_constraints = QFrame(self.page_constraints)
        self.line_before_geometric_constraints.setObjectName(u"line_before_geometric_constraints")
        self.line_before_geometric_constraints.setFrameShape(QFrame.Shape.HLine)
        self.line_before_geometric_constraints.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_6.addWidget(self.line_before_geometric_constraints, 12, 0, 1, 5)

        self.input_service_ceiling = QLineEdit(self.page_constraints)
        self.input_service_ceiling.setObjectName(u"input_service_ceiling")

        self.gridLayout_6.addWidget(self.input_service_ceiling, 10, 2, 1, 1)

        self.lbl_rate_of_climb_unit = QLabel(self.page_constraints)
        self.lbl_rate_of_climb_unit.setObjectName(u"lbl_rate_of_climb_unit")

        self.gridLayout_6.addWidget(self.lbl_rate_of_climb_unit, 9, 3, 1, 1)

        self.lbl_service_ceiling_unit = QLabel(self.page_constraints)
        self.lbl_service_ceiling_unit.setObjectName(u"lbl_service_ceiling_unit")

        self.gridLayout_6.addWidget(self.lbl_service_ceiling_unit, 10, 3, 1, 1)

        self.lbl_rate_of_climb = QLabel(self.page_constraints)
        self.lbl_rate_of_climb.setObjectName(u"lbl_rate_of_climb")

        self.gridLayout_6.addWidget(self.lbl_rate_of_climb, 9, 0, 1, 1)

        self.lbl_service_ceiling = QLabel(self.page_constraints)
        self.lbl_service_ceiling.setObjectName(u"lbl_service_ceiling")

        self.gridLayout_6.addWidget(self.lbl_service_ceiling, 10, 0, 1, 1)

        self.toolbox_preliminary_sizing.addItem(self.page_constraints, u"Constraints")
        self.page_mission_segment = QWidget()
        self.page_mission_segment.setObjectName(u"page_mission_segment")
        self.page_mission_segment.setGeometry(QRect(0, 0, 628, 414))
        self.gridLayout_3 = QGridLayout(self.page_mission_segment)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.view_mission_segments = QColumnView(self.page_mission_segment)
        self.view_mission_segments.setObjectName(u"view_mission_segments")

        self.gridLayout_3.addWidget(self.view_mission_segments, 0, 0, 1, 1)

        self.toolbox_preliminary_sizing.addItem(self.page_mission_segment, u"Mission Segment")
        self.page_initial_weight_estimates = QWidget()
        self.page_initial_weight_estimates.setObjectName(u"page_initial_weight_estimates")
        self.page_initial_weight_estimates.setGeometry(QRect(0, 0, 628, 414))
        self.verticalLayout_page_7 = QVBoxLayout(self.page_initial_weight_estimates)
        self.verticalLayout_page_7.setObjectName(u"verticalLayout_page_7")
        self.lbl_initial_weight_output = QLabel(self.page_initial_weight_estimates)
        self.lbl_initial_weight_output.setObjectName(u"lbl_initial_weight_output")

        self.verticalLayout_page_7.addWidget(self.lbl_initial_weight_output)

        self.table_initial_weight_output = QTableWidget(self.page_initial_weight_estimates)
        if (self.table_initial_weight_output.columnCount() < 2):
            self.table_initial_weight_output.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_initial_weight_output.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_initial_weight_output.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.table_initial_weight_output.setObjectName(u"table_initial_weight_output")

        self.verticalLayout_page_7.addWidget(self.table_initial_weight_output)

        self.toolbox_preliminary_sizing.addItem(self.page_initial_weight_estimates, u"Initial Weight Estimates")
        self.page_initial_drag_polar = QWidget()
        self.page_initial_drag_polar.setObjectName(u"page_initial_drag_polar")
        self.page_initial_drag_polar.setGeometry(QRect(0, 0, 611, 1697))
        self.verticalLayout_page_4 = QVBoxLayout(self.page_initial_drag_polar)
        self.verticalLayout_page_4.setObjectName(u"verticalLayout_page_4")
        self.group_xfoil_settings = QGroupBox(self.page_initial_drag_polar)
        self.group_xfoil_settings.setObjectName(u"group_xfoil_settings")
        self.form_xfoil_settings = QFormLayout(self.group_xfoil_settings)
        self.form_xfoil_settings.setObjectName(u"form_xfoil_settings")
        self.lbl_xf_re = QLabel(self.group_xfoil_settings)
        self.lbl_xf_re.setObjectName(u"lbl_xf_re")

        self.form_xfoil_settings.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_xf_re)

        self.xf_re = QSpinBox(self.group_xfoil_settings)
        self.xf_re.setObjectName(u"xf_re")

        self.form_xfoil_settings.setWidget(0, QFormLayout.ItemRole.FieldRole, self.xf_re)

        self.lbl_xf_panels = QLabel(self.group_xfoil_settings)
        self.lbl_xf_panels.setObjectName(u"lbl_xf_panels")

        self.form_xfoil_settings.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_xf_panels)

        self.xf_panels = QSpinBox(self.group_xfoil_settings)
        self.xf_panels.setObjectName(u"xf_panels")

        self.form_xfoil_settings.setWidget(1, QFormLayout.ItemRole.FieldRole, self.xf_panels)

        self.lbl_xf_mach = QLabel(self.group_xfoil_settings)
        self.lbl_xf_mach.setObjectName(u"lbl_xf_mach")

        self.form_xfoil_settings.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_xf_mach)

        self.xf_mach = QDoubleSpinBox(self.group_xfoil_settings)
        self.xf_mach.setObjectName(u"xf_mach")

        self.form_xfoil_settings.setWidget(2, QFormLayout.ItemRole.FieldRole, self.xf_mach)

        self.lbl_xf_ncrit = QLabel(self.group_xfoil_settings)
        self.lbl_xf_ncrit.setObjectName(u"lbl_xf_ncrit")

        self.form_xfoil_settings.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_xf_ncrit)

        self.xf_ncrit = QSpinBox(self.group_xfoil_settings)
        self.xf_ncrit.setObjectName(u"xf_ncrit")

        self.form_xfoil_settings.setWidget(3, QFormLayout.ItemRole.FieldRole, self.xf_ncrit)

        self.lbl_xf_iter = QLabel(self.group_xfoil_settings)
        self.lbl_xf_iter.setObjectName(u"lbl_xf_iter")

        self.form_xfoil_settings.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lbl_xf_iter)

        self.xf_iter = QSpinBox(self.group_xfoil_settings)
        self.xf_iter.setObjectName(u"xf_iter")

        self.form_xfoil_settings.setWidget(4, QFormLayout.ItemRole.FieldRole, self.xf_iter)


        self.verticalLayout_page_4.addWidget(self.group_xfoil_settings)

        self.group_naca_bounds = QGroupBox(self.page_initial_drag_polar)
        self.group_naca_bounds.setObjectName(u"group_naca_bounds")
        self.form_naca_bounds = QFormLayout(self.group_naca_bounds)
        self.form_naca_bounds.setObjectName(u"form_naca_bounds")
        self.lbl_naca_camber_min = QLabel(self.group_naca_bounds)
        self.lbl_naca_camber_min.setObjectName(u"lbl_naca_camber_min")

        self.form_naca_bounds.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_naca_camber_min)

        self.naca_camber_min = QSpinBox(self.group_naca_bounds)
        self.naca_camber_min.setObjectName(u"naca_camber_min")

        self.form_naca_bounds.setWidget(0, QFormLayout.ItemRole.FieldRole, self.naca_camber_min)

        self.lbl_naca_camber_max = QLabel(self.group_naca_bounds)
        self.lbl_naca_camber_max.setObjectName(u"lbl_naca_camber_max")

        self.form_naca_bounds.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_naca_camber_max)

        self.naca_camber_max = QSpinBox(self.group_naca_bounds)
        self.naca_camber_max.setObjectName(u"naca_camber_max")

        self.form_naca_bounds.setWidget(1, QFormLayout.ItemRole.FieldRole, self.naca_camber_max)

        self.lbl_naca_camber_loc_min = QLabel(self.group_naca_bounds)
        self.lbl_naca_camber_loc_min.setObjectName(u"lbl_naca_camber_loc_min")

        self.form_naca_bounds.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_naca_camber_loc_min)

        self.naca_camber_loc_min = QSpinBox(self.group_naca_bounds)
        self.naca_camber_loc_min.setObjectName(u"naca_camber_loc_min")

        self.form_naca_bounds.setWidget(2, QFormLayout.ItemRole.FieldRole, self.naca_camber_loc_min)

        self.lbl_naca_camber_loc_max = QLabel(self.group_naca_bounds)
        self.lbl_naca_camber_loc_max.setObjectName(u"lbl_naca_camber_loc_max")

        self.form_naca_bounds.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_naca_camber_loc_max)

        self.naca_camber_loc_max = QSpinBox(self.group_naca_bounds)
        self.naca_camber_loc_max.setObjectName(u"naca_camber_loc_max")

        self.form_naca_bounds.setWidget(3, QFormLayout.ItemRole.FieldRole, self.naca_camber_loc_max)

        self.lbl_naca_thickness_min = QLabel(self.group_naca_bounds)
        self.lbl_naca_thickness_min.setObjectName(u"lbl_naca_thickness_min")

        self.form_naca_bounds.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lbl_naca_thickness_min)

        self.naca_thickness_min = QSpinBox(self.group_naca_bounds)
        self.naca_thickness_min.setObjectName(u"naca_thickness_min")

        self.form_naca_bounds.setWidget(4, QFormLayout.ItemRole.FieldRole, self.naca_thickness_min)

        self.lbl_naca_thickness_max = QLabel(self.group_naca_bounds)
        self.lbl_naca_thickness_max.setObjectName(u"lbl_naca_thickness_max")

        self.form_naca_bounds.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lbl_naca_thickness_max)

        self.naca_thickness_max = QSpinBox(self.group_naca_bounds)
        self.naca_thickness_max.setObjectName(u"naca_thickness_max")

        self.form_naca_bounds.setWidget(5, QFormLayout.ItemRole.FieldRole, self.naca_thickness_max)


        self.verticalLayout_page_4.addWidget(self.group_naca_bounds)

        self.group_weight_application = QGroupBox(self.page_initial_drag_polar)
        self.group_weight_application.setObjectName(u"group_weight_application")
        self.form_weight_application = QFormLayout(self.group_weight_application)
        self.form_weight_application.setObjectName(u"form_weight_application")
        self.lbl_w_cl = QLabel(self.group_weight_application)
        self.lbl_w_cl.setObjectName(u"lbl_w_cl")

        self.form_weight_application.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_w_cl)

        self.w_cl = QDoubleSpinBox(self.group_weight_application)
        self.w_cl.setObjectName(u"w_cl")

        self.form_weight_application.setWidget(1, QFormLayout.ItemRole.FieldRole, self.w_cl)

        self.lbl_w_cd = QLabel(self.group_weight_application)
        self.lbl_w_cd.setObjectName(u"lbl_w_cd")

        self.form_weight_application.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_w_cd)

        self.w_cd = QDoubleSpinBox(self.group_weight_application)
        self.w_cd.setObjectName(u"w_cd")

        self.form_weight_application.setWidget(2, QFormLayout.ItemRole.FieldRole, self.w_cd)

        self.lbl_w_ld = QLabel(self.group_weight_application)
        self.lbl_w_ld.setObjectName(u"lbl_w_ld")

        self.form_weight_application.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_w_ld)

        self.w_ld = QDoubleSpinBox(self.group_weight_application)
        self.w_ld.setObjectName(u"w_ld")

        self.form_weight_application.setWidget(3, QFormLayout.ItemRole.FieldRole, self.w_ld)

        self.lbl_w_cm = QLabel(self.group_weight_application)
        self.lbl_w_cm.setObjectName(u"lbl_w_cm")

        self.form_weight_application.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lbl_w_cm)

        self.w_cm = QDoubleSpinBox(self.group_weight_application)
        self.w_cm.setObjectName(u"w_cm")

        self.form_weight_application.setWidget(4, QFormLayout.ItemRole.FieldRole, self.w_cm)

        self.lbl_w_tc = QLabel(self.group_weight_application)
        self.lbl_w_tc.setObjectName(u"lbl_w_tc")

        self.form_weight_application.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lbl_w_tc)

        self.w_tc = QDoubleSpinBox(self.group_weight_application)
        self.w_tc.setObjectName(u"w_tc")

        self.form_weight_application.setWidget(5, QFormLayout.ItemRole.FieldRole, self.w_tc)

        self.lbl_w_aoa = QLabel(self.group_weight_application)
        self.lbl_w_aoa.setObjectName(u"lbl_w_aoa")

        self.form_weight_application.setWidget(7, QFormLayout.ItemRole.LabelRole, self.lbl_w_aoa)

        self.w_aoa = QDoubleSpinBox(self.group_weight_application)
        self.w_aoa.setObjectName(u"w_aoa")

        self.form_weight_application.setWidget(7, QFormLayout.ItemRole.FieldRole, self.w_aoa)

        self.lbl_ideal_tc = QLabel(self.group_weight_application)
        self.lbl_ideal_tc.setObjectName(u"lbl_ideal_tc")

        self.form_weight_application.setWidget(8, QFormLayout.ItemRole.LabelRole, self.lbl_ideal_tc)

        self.ideal_tc = QDoubleSpinBox(self.group_weight_application)
        self.ideal_tc.setObjectName(u"ideal_tc")

        self.form_weight_application.setWidget(8, QFormLayout.ItemRole.FieldRole, self.ideal_tc)

        self.lbl_tc_deviation = QLabel(self.group_weight_application)
        self.lbl_tc_deviation.setObjectName(u"lbl_tc_deviation")

        self.form_weight_application.setWidget(10, QFormLayout.ItemRole.LabelRole, self.lbl_tc_deviation)

        self.tc_deviation = QDoubleSpinBox(self.group_weight_application)
        self.tc_deviation.setObjectName(u"tc_deviation")

        self.form_weight_application.setWidget(10, QFormLayout.ItemRole.FieldRole, self.tc_deviation)

        self.lbl_weight_total = QLabel(self.group_weight_application)
        self.lbl_weight_total.setObjectName(u"lbl_weight_total")

        self.form_weight_application.setWidget(11, QFormLayout.ItemRole.SpanningRole, self.lbl_weight_total)

        self.mdiArea_6 = QMdiArea(self.group_weight_application)
        self.mdiArea_6.setObjectName(u"mdiArea_6")
        self.mdiArea_6.setMinimumSize(QSize(0, 500))

        self.form_weight_application.setWidget(12, QFormLayout.ItemRole.SpanningRole, self.mdiArea_6)


        self.verticalLayout_page_4.addWidget(self.group_weight_application)

        self.layout_drag_buttons = QHBoxLayout()
        self.layout_drag_buttons.setObjectName(u"layout_drag_buttons")
        self.btn_run_airfoil_opt = QPushButton(self.page_initial_drag_polar)
        self.btn_run_airfoil_opt.setObjectName(u"btn_run_airfoil_opt")

        self.layout_drag_buttons.addWidget(self.btn_run_airfoil_opt)

        self.btn_apply_airfoil_weights = QPushButton(self.page_initial_drag_polar)
        self.btn_apply_airfoil_weights.setObjectName(u"btn_apply_airfoil_weights")

        self.layout_drag_buttons.addWidget(self.btn_apply_airfoil_weights)

        self.btn_use_top_airfoil = QPushButton(self.page_initial_drag_polar)
        self.btn_use_top_airfoil.setObjectName(u"btn_use_top_airfoil")

        self.layout_drag_buttons.addWidget(self.btn_use_top_airfoil)


        self.verticalLayout_page_4.addLayout(self.layout_drag_buttons)

        self.airfoil_result_table = QTableWidget(self.page_initial_drag_polar)
        self.airfoil_result_table.setObjectName(u"airfoil_result_table")

        self.verticalLayout_page_4.addWidget(self.airfoil_result_table)

        self.lbl_top_airfoil = QLabel(self.page_initial_drag_polar)
        self.lbl_top_airfoil.setObjectName(u"lbl_top_airfoil")

        self.verticalLayout_page_4.addWidget(self.lbl_top_airfoil)

        self.group_drag_polar_estimates = QGroupBox(self.page_initial_drag_polar)
        self.group_drag_polar_estimates.setObjectName(u"group_drag_polar_estimates")
        self.verticalLayout_drag_polar_estimates = QVBoxLayout(self.group_drag_polar_estimates)
        self.verticalLayout_drag_polar_estimates.setObjectName(u"verticalLayout_drag_polar_estimates")
        self.form_drag_polar_base = QFormLayout()
        self.form_drag_polar_base.setObjectName(u"form_drag_polar_base")
        self.lbl_drag_cd0_clean = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_cd0_clean.setObjectName(u"lbl_drag_cd0_clean")

        self.form_drag_polar_base.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_drag_cd0_clean)

        self.drag_cd0_clean = QDoubleSpinBox(self.group_drag_polar_estimates)
        self.drag_cd0_clean.setObjectName(u"drag_cd0_clean")

        self.form_drag_polar_base.setWidget(0, QFormLayout.ItemRole.FieldRole, self.drag_cd0_clean)

        self.lbl_drag_dcd0_takeoff = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_dcd0_takeoff.setObjectName(u"lbl_drag_dcd0_takeoff")

        self.form_drag_polar_base.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_drag_dcd0_takeoff)

        self.drag_dcd0_takeoff = QDoubleSpinBox(self.group_drag_polar_estimates)
        self.drag_dcd0_takeoff.setObjectName(u"drag_dcd0_takeoff")

        self.form_drag_polar_base.setWidget(1, QFormLayout.ItemRole.FieldRole, self.drag_dcd0_takeoff)

        self.lbl_drag_dcd0_landing = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_dcd0_landing.setObjectName(u"lbl_drag_dcd0_landing")

        self.form_drag_polar_base.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_drag_dcd0_landing)

        self.drag_dcd0_landing = QDoubleSpinBox(self.group_drag_polar_estimates)
        self.drag_dcd0_landing.setObjectName(u"drag_dcd0_landing")

        self.form_drag_polar_base.setWidget(2, QFormLayout.ItemRole.FieldRole, self.drag_dcd0_landing)

        self.lbl_drag_mu_ground = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_mu_ground.setObjectName(u"lbl_drag_mu_ground")

        self.form_drag_polar_base.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_drag_mu_ground)

        self.drag_mu_ground = QDoubleSpinBox(self.group_drag_polar_estimates)
        self.drag_mu_ground.setObjectName(u"drag_mu_ground")

        self.form_drag_polar_base.setWidget(3, QFormLayout.ItemRole.FieldRole, self.drag_mu_ground)


        self.verticalLayout_drag_polar_estimates.addLayout(self.form_drag_polar_base)

        self.grid_drag_polar_rows = QGridLayout()
        self.grid_drag_polar_rows.setObjectName(u"grid_drag_polar_rows")
        self.lbl_drag_cfg = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_cfg.setObjectName(u"lbl_drag_cfg")

        self.grid_drag_polar_rows.addWidget(self.lbl_drag_cfg, 0, 0, 1, 1)

        self.lbl_drag_cl = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_cl.setObjectName(u"lbl_drag_cl")

        self.grid_drag_polar_rows.addWidget(self.lbl_drag_cl, 0, 1, 1, 1)

        self.lbl_drag_e = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_e.setObjectName(u"lbl_drag_e")

        self.grid_drag_polar_rows.addWidget(self.lbl_drag_e, 0, 2, 1, 1)

        self.lbl_drag_k = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_k.setObjectName(u"lbl_drag_k")

        self.grid_drag_polar_rows.addWidget(self.lbl_drag_k, 0, 3, 1, 1)

        self.lbl_drag_cd = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_cd.setObjectName(u"lbl_drag_cd")

        self.grid_drag_polar_rows.addWidget(self.lbl_drag_cd, 0, 4, 1, 1)

        self.lbl_drag_clean = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_clean.setObjectName(u"lbl_drag_clean")

        self.grid_drag_polar_rows.addWidget(self.lbl_drag_clean, 1, 0, 1, 1)

        self.drag_cl_clean = QDoubleSpinBox(self.group_drag_polar_estimates)
        self.drag_cl_clean.setObjectName(u"drag_cl_clean")

        self.grid_drag_polar_rows.addWidget(self.drag_cl_clean, 1, 1, 1, 1)

        self.drag_e_clean = QDoubleSpinBox(self.group_drag_polar_estimates)
        self.drag_e_clean.setObjectName(u"drag_e_clean")

        self.grid_drag_polar_rows.addWidget(self.drag_e_clean, 1, 2, 1, 1)

        self.drag_k_clean_out = QLineEdit(self.group_drag_polar_estimates)
        self.drag_k_clean_out.setObjectName(u"drag_k_clean_out")

        self.grid_drag_polar_rows.addWidget(self.drag_k_clean_out, 1, 3, 1, 1)

        self.drag_cd_clean_out = QLineEdit(self.group_drag_polar_estimates)
        self.drag_cd_clean_out.setObjectName(u"drag_cd_clean_out")

        self.grid_drag_polar_rows.addWidget(self.drag_cd_clean_out, 1, 4, 1, 1)

        self.lbl_drag_takeoff = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_takeoff.setObjectName(u"lbl_drag_takeoff")

        self.grid_drag_polar_rows.addWidget(self.lbl_drag_takeoff, 2, 0, 1, 1)

        self.drag_cl_takeoff = QDoubleSpinBox(self.group_drag_polar_estimates)
        self.drag_cl_takeoff.setObjectName(u"drag_cl_takeoff")

        self.grid_drag_polar_rows.addWidget(self.drag_cl_takeoff, 2, 1, 1, 1)

        self.drag_e_takeoff = QDoubleSpinBox(self.group_drag_polar_estimates)
        self.drag_e_takeoff.setObjectName(u"drag_e_takeoff")

        self.grid_drag_polar_rows.addWidget(self.drag_e_takeoff, 2, 2, 1, 1)

        self.drag_k_takeoff_out = QLineEdit(self.group_drag_polar_estimates)
        self.drag_k_takeoff_out.setObjectName(u"drag_k_takeoff_out")

        self.grid_drag_polar_rows.addWidget(self.drag_k_takeoff_out, 2, 3, 1, 1)

        self.drag_cd_takeoff_out = QLineEdit(self.group_drag_polar_estimates)
        self.drag_cd_takeoff_out.setObjectName(u"drag_cd_takeoff_out")

        self.grid_drag_polar_rows.addWidget(self.drag_cd_takeoff_out, 2, 4, 1, 1)

        self.lbl_drag_landing = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_landing.setObjectName(u"lbl_drag_landing")

        self.grid_drag_polar_rows.addWidget(self.lbl_drag_landing, 3, 0, 1, 1)

        self.drag_cl_landing = QDoubleSpinBox(self.group_drag_polar_estimates)
        self.drag_cl_landing.setObjectName(u"drag_cl_landing")

        self.grid_drag_polar_rows.addWidget(self.drag_cl_landing, 3, 1, 1, 1)

        self.drag_e_landing = QDoubleSpinBox(self.group_drag_polar_estimates)
        self.drag_e_landing.setObjectName(u"drag_e_landing")

        self.grid_drag_polar_rows.addWidget(self.drag_e_landing, 3, 2, 1, 1)

        self.drag_k_landing_out = QLineEdit(self.group_drag_polar_estimates)
        self.drag_k_landing_out.setObjectName(u"drag_k_landing_out")

        self.grid_drag_polar_rows.addWidget(self.drag_k_landing_out, 3, 3, 1, 1)

        self.drag_cd_landing_out = QLineEdit(self.group_drag_polar_estimates)
        self.drag_cd_landing_out.setObjectName(u"drag_cd_landing_out")

        self.grid_drag_polar_rows.addWidget(self.drag_cd_landing_out, 3, 4, 1, 1)


        self.verticalLayout_drag_polar_estimates.addLayout(self.grid_drag_polar_rows)

        self.form_drag_ground = QFormLayout()
        self.form_drag_ground.setObjectName(u"form_drag_ground")
        self.lbl_drag_cd_ground = QLabel(self.group_drag_polar_estimates)
        self.lbl_drag_cd_ground.setObjectName(u"lbl_drag_cd_ground")

        self.form_drag_ground.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_drag_cd_ground)

        self.drag_cd_ground_out = QLineEdit(self.group_drag_polar_estimates)
        self.drag_cd_ground_out.setObjectName(u"drag_cd_ground_out")

        self.form_drag_ground.setWidget(0, QFormLayout.ItemRole.FieldRole, self.drag_cd_ground_out)


        self.verticalLayout_drag_polar_estimates.addLayout(self.form_drag_ground)

        self.btn_estimate_drag_polar = QPushButton(self.group_drag_polar_estimates)
        self.btn_estimate_drag_polar.setObjectName(u"btn_estimate_drag_polar")

        self.verticalLayout_drag_polar_estimates.addWidget(self.btn_estimate_drag_polar)

        self.drag_estimate_table = QTableWidget(self.group_drag_polar_estimates)
        self.drag_estimate_table.setObjectName(u"drag_estimate_table")

        self.verticalLayout_drag_polar_estimates.addWidget(self.drag_estimate_table)


        self.verticalLayout_page_4.addWidget(self.group_drag_polar_estimates)

        self.toolbox_preliminary_sizing.addItem(self.page_initial_drag_polar, u"Initial Drag Polar Estimate")
        self.page_wing_power_loading_sizing = QWidget()
        self.page_wing_power_loading_sizing.setObjectName(u"page_wing_power_loading_sizing")
        self.page_wing_power_loading_sizing.setGeometry(QRect(0, 0, 611, 451))
        self.verticalLayout_page_2 = QVBoxLayout(self.page_wing_power_loading_sizing)
        self.verticalLayout_page_2.setObjectName(u"verticalLayout_page_2")
        self.group_sizing_controls = QGroupBox(self.page_wing_power_loading_sizing)
        self.group_sizing_controls.setObjectName(u"group_sizing_controls")
        self.verticalLayout_sizing_controls = QVBoxLayout(self.group_sizing_controls)
        self.verticalLayout_sizing_controls.setObjectName(u"verticalLayout_sizing_controls")
        self.btn_run_sizing = QPushButton(self.group_sizing_controls)
        self.btn_run_sizing.setObjectName(u"btn_run_sizing")

        self.verticalLayout_sizing_controls.addWidget(self.btn_run_sizing)


        self.verticalLayout_page_2.addWidget(self.group_sizing_controls)

        self.group_sizing_summary = QGroupBox(self.page_wing_power_loading_sizing)
        self.group_sizing_summary.setObjectName(u"group_sizing_summary")
        self.group_sizing_summary.setMinimumSize(QSize(0, 0))
        self.gridLayout_16 = QGridLayout(self.group_sizing_summary)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.sizing_summary_table = QTableWidget(self.group_sizing_summary)
        if (self.sizing_summary_table.columnCount() < 2):
            self.sizing_summary_table.setColumnCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.sizing_summary_table.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.sizing_summary_table.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        self.sizing_summary_table.setObjectName(u"sizing_summary_table")
        self.sizing_summary_table.setMinimumSize(QSize(0, 0))

        self.gridLayout_16.addWidget(self.sizing_summary_table, 0, 0, 1, 1)


        self.verticalLayout_page_2.addWidget(self.group_sizing_summary)

        self.group_sizing_plot = QGroupBox(self.page_wing_power_loading_sizing)
        self.group_sizing_plot.setObjectName(u"group_sizing_plot")
        self.verticalLayout_sizing_plot = QVBoxLayout(self.group_sizing_plot)
        self.verticalLayout_sizing_plot.setObjectName(u"verticalLayout_sizing_plot")
        self.sizing_plot_container = QWidget(self.group_sizing_plot)
        self.sizing_plot_container.setObjectName(u"sizing_plot_container")

        self.verticalLayout_sizing_plot.addWidget(self.sizing_plot_container)


        self.verticalLayout_page_2.addWidget(self.group_sizing_plot)

        self.group_sizing_stall = QGroupBox(self.page_wing_power_loading_sizing)
        self.group_sizing_stall.setObjectName(u"group_sizing_stall")
        self.gridLayout_12 = QGridLayout(self.group_sizing_stall)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.sizing_stall_plot_container = QWidget(self.group_sizing_stall)
        self.sizing_stall_plot_container.setObjectName(u"sizing_stall_plot_container")

        self.gridLayout_12.addWidget(self.sizing_stall_plot_container, 0, 0, 1, 1)


        self.verticalLayout_page_2.addWidget(self.group_sizing_stall)

        self.group_sizing_rate_of_climb = QGroupBox(self.page_wing_power_loading_sizing)
        self.group_sizing_rate_of_climb.setObjectName(u"group_sizing_rate_of_climb")
        self.gridLayout_13 = QGridLayout(self.group_sizing_rate_of_climb)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.sizing_rate_of_climb_plot_container = QWidget(self.group_sizing_rate_of_climb)
        self.sizing_rate_of_climb_plot_container.setObjectName(u"sizing_rate_of_climb_plot_container")

        self.gridLayout_13.addWidget(self.sizing_rate_of_climb_plot_container, 0, 0, 1, 1)


        self.verticalLayout_page_2.addWidget(self.group_sizing_rate_of_climb)

        self.group_sizing_takeoff = QGroupBox(self.page_wing_power_loading_sizing)
        self.group_sizing_takeoff.setObjectName(u"group_sizing_takeoff")
        self.gridLayout_11 = QGridLayout(self.group_sizing_takeoff)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.sizing_takeoff_plot_container = QWidget(self.group_sizing_takeoff)
        self.sizing_takeoff_plot_container.setObjectName(u"sizing_takeoff_plot_container")

        self.gridLayout_11.addWidget(self.sizing_takeoff_plot_container, 0, 0, 1, 1)


        self.verticalLayout_page_2.addWidget(self.group_sizing_takeoff)

        self.group_sizing_service_ceiling = QGroupBox(self.page_wing_power_loading_sizing)
        self.group_sizing_service_ceiling.setObjectName(u"group_sizing_service_ceiling")
        self.gridLayout_14 = QGridLayout(self.group_sizing_service_ceiling)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.sizing_service_ceiling_plot_container = QWidget(self.group_sizing_service_ceiling)
        self.sizing_service_ceiling_plot_container.setObjectName(u"sizing_service_ceiling_plot_container")

        self.gridLayout_14.addWidget(self.sizing_service_ceiling_plot_container, 0, 0, 1, 1)


        self.verticalLayout_page_2.addWidget(self.group_sizing_service_ceiling)

        self.toolbox_preliminary_sizing.addItem(self.page_wing_power_loading_sizing, u"Wing Loading and Power Loading Sizing")
        self.page_v_speeds_empennage = QWidget()
        self.page_v_speeds_empennage.setObjectName(u"page_v_speeds_empennage")
        self.toolbox_preliminary_sizing.addItem(self.page_v_speeds_empennage, u"V-Speeds and Empennage Sizing")

        self.gridLayout_15.addWidget(self.toolbox_preliminary_sizing, 0, 0, 1, 1)

        self.tabWidget.addTab(self.prelim_tab, "")
        self.geometry_modeler_tab = QWidget()
        self.geometry_modeler_tab.setObjectName(u"geometry_modeler_tab")
        self.geometry_modeler_tab.setMouseTracking(True)
        self.geometry_modeler_tab.setTabletTracking(False)
        self.tabWidget.addTab(self.geometry_modeler_tab, "")
        self.aerodynamics_tab = QWidget()
        self.aerodynamics_tab.setObjectName(u"aerodynamics_tab")
        self.gridLayout_4 = QGridLayout(self.aerodynamics_tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.mdiArea_2 = QMdiArea(self.aerodynamics_tab)
        self.mdiArea_2.setObjectName(u"mdiArea_2")

        self.gridLayout_4.addWidget(self.mdiArea_2, 1, 0, 1, 1)

        self.btn_load_pressure_data = QPushButton(self.aerodynamics_tab)
        self.btn_load_pressure_data.setObjectName(u"btn_load_pressure_data")

        self.gridLayout_4.addWidget(self.btn_load_pressure_data, 0, 0, 1, 1)

        self.tabWidget.addTab(self.aerodynamics_tab, "")
        self.structures_tab = QWidget()
        self.structures_tab.setObjectName(u"structures_tab")
        self.verticalLayout_3 = QVBoxLayout(self.structures_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lbl_structures_workspace_title = QLabel(self.structures_tab)
        self.lbl_structures_workspace_title.setObjectName(u"lbl_structures_workspace_title")

        self.verticalLayout_3.addWidget(self.lbl_structures_workspace_title)

        self.lbl_structures_workspace_subtitle = QLabel(self.structures_tab)
        self.lbl_structures_workspace_subtitle.setObjectName(u"lbl_structures_workspace_subtitle")
        self.lbl_structures_workspace_subtitle.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.lbl_structures_workspace_subtitle)

        self.lbl_structures_panel_title = QLabel(self.structures_tab)
        self.lbl_structures_panel_title.setObjectName(u"lbl_structures_panel_title")

        self.verticalLayout_3.addWidget(self.lbl_structures_panel_title)

        self.structures_panel_stack = QStackedWidget(self.structures_tab)
        self.structures_panel_stack.setObjectName(u"structures_panel_stack")

        self.verticalLayout_3.addWidget(self.structures_panel_stack)

        self.tabWidget.addTab(self.structures_tab, "")
        self.propulsion_tab = QWidget()
        self.propulsion_tab.setObjectName(u"propulsion_tab")
        self.verticalLayout_propulsion = QVBoxLayout(self.propulsion_tab)
        self.verticalLayout_propulsion.setObjectName(u"verticalLayout_propulsion")
        self.lbl_propulsion_workspace_title = QLabel(self.propulsion_tab)
        self.lbl_propulsion_workspace_title.setObjectName(u"lbl_propulsion_workspace_title")

        self.verticalLayout_propulsion.addWidget(self.lbl_propulsion_workspace_title)

        self.lbl_propulsion_workspace_subtitle = QLabel(self.propulsion_tab)
        self.lbl_propulsion_workspace_subtitle.setObjectName(u"lbl_propulsion_workspace_subtitle")
        self.lbl_propulsion_workspace_subtitle.setWordWrap(True)

        self.verticalLayout_propulsion.addWidget(self.lbl_propulsion_workspace_subtitle)

        self.lbl_propulsion_panel_title = QLabel(self.propulsion_tab)
        self.lbl_propulsion_panel_title.setObjectName(u"lbl_propulsion_panel_title")

        self.verticalLayout_propulsion.addWidget(self.lbl_propulsion_panel_title)

        self.propulsion_panel_stack = QStackedWidget(self.propulsion_tab)
        self.propulsion_panel_stack.setObjectName(u"propulsion_panel_stack")

        self.verticalLayout_propulsion.addWidget(self.propulsion_panel_stack)

        self.tabWidget.addTab(self.propulsion_tab, "")
        self.performance_tab = QWidget()
        self.performance_tab.setObjectName(u"performance_tab")
        self.gridLayout_9 = QGridLayout(self.performance_tab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.toolBox_performance = QToolBox(self.performance_tab)
        self.toolBox_performance.setObjectName(u"toolBox_performance")
        self.power_required = QWidget()
        self.power_required.setObjectName(u"power_required")
        self.power_required.setGeometry(QRect(0, 0, 414, 91))
        self.horizontalLayout = QHBoxLayout(self.power_required)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tableWidget = QTableWidget(self.power_required)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(8)
        font.setBold(True)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignJustify|Qt.AlignVCenter);
        __qtablewidgetitem4.setFont(font);
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignJustify|Qt.AlignVCenter);
        __qtablewidgetitem5.setFont(font);
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        if (self.tableWidget.rowCount() < 10):
            self.tableWidget.setRowCount(10)
        font1 = QFont()
        font1.setPointSize(7)
        font1.setBold(True)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem6.setFont(font1);
        self.tableWidget.setItem(0, 0, __qtablewidgetitem6)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QSize(230, 0))
        self.tableWidget.setFrameShape(QFrame.Shape.WinPanel)
        self.tableWidget.setFrameShadow(QFrame.Shadow.Raised)
        self.tableWidget.setRowCount(10)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)

        self.horizontalLayout.addWidget(self.tableWidget)

        self.mdiArea_3 = QMdiArea(self.power_required)
        self.mdiArea_3.setObjectName(u"mdiArea_3")

        self.horizontalLayout.addWidget(self.mdiArea_3)

        self.toolBox_performance.addItem(self.power_required, u"Power Required/Thrust Required")
        self.power_available = QWidget()
        self.power_available.setObjectName(u"power_available")
        self.power_available.setGeometry(QRect(0, 0, 255, 89))
        self.horizontalLayout_2 = QHBoxLayout(self.power_available)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tableWidget_2 = QTableWidget(self.power_available)
        self.tableWidget_2.setObjectName(u"tableWidget_2")

        self.horizontalLayout_2.addWidget(self.tableWidget_2)

        self.mdiArea = QMdiArea(self.power_available)
        self.mdiArea.setObjectName(u"mdiArea")

        self.horizontalLayout_2.addWidget(self.mdiArea)

        self.toolBox_performance.addItem(self.power_available, u"Power Available/Thrust Available")
        self.excess_power = QWidget()
        self.excess_power.setObjectName(u"excess_power")
        self.excess_power.setGeometry(QRect(0, 0, 255, 89))
        self.horizontalLayout_3 = QHBoxLayout(self.excess_power)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tableWidget_3 = QTableWidget(self.excess_power)
        self.tableWidget_3.setObjectName(u"tableWidget_3")

        self.horizontalLayout_3.addWidget(self.tableWidget_3)

        self.mdiArea_4 = QMdiArea(self.excess_power)
        self.mdiArea_4.setObjectName(u"mdiArea_4")

        self.horizontalLayout_3.addWidget(self.mdiArea_4)

        self.toolBox_performance.addItem(self.excess_power, u"Excess Power and Climb Performance")
        self.service_ceiling = QWidget()
        self.service_ceiling.setObjectName(u"service_ceiling")
        self.service_ceiling.setGeometry(QRect(0, 0, 628, 474))
        self.horizontalLayout_4 = QHBoxLayout(self.service_ceiling)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.tableWidget_4 = QTableWidget(self.service_ceiling)
        self.tableWidget_4.setObjectName(u"tableWidget_4")

        self.horizontalLayout_4.addWidget(self.tableWidget_4)

        self.mdiArea_5 = QMdiArea(self.service_ceiling)
        self.mdiArea_5.setObjectName(u"mdiArea_5")

        self.horizontalLayout_4.addWidget(self.mdiArea_5)

        self.toolBox_performance.addItem(self.service_ceiling, u"Service Ceiling and Absolute Ceiling")

        self.gridLayout_9.addWidget(self.toolBox_performance, 0, 0, 1, 1)

        self.tabWidget.addTab(self.performance_tab, "")
        self.result_tab = QWidget()
        self.result_tab.setObjectName(u"result_tab")
        self.gridLayout_5 = QGridLayout(self.result_tab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.toolBox_2 = QToolBox(self.result_tab)
        self.toolBox_2.setObjectName(u"toolBox_2")
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.page_5.setGeometry(QRect(0, 0, 98, 91))
        self.gridLayout_10 = QGridLayout(self.page_5)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.listWidget = QListWidget(self.page_5)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")

        self.gridLayout_10.addWidget(self.listWidget, 0, 0, 1, 1)

        self.toolBox_2.addItem(self.page_5, u"Metric")
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.page_6.setGeometry(QRect(0, 0, 628, 534))
        self.toolBox_2.addItem(self.page_6, u"Page 2")

        self.gridLayout_5.addWidget(self.toolBox_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.result_tab, "")

        self.gridLayout_8.addWidget(self.tabWidget, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1097, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.tree = QDockWidget(MainWindow)
        self.tree.setObjectName(u"tree")
        self.tree_view_tree = QWidget()
        self.tree_view_tree.setObjectName(u"tree_view_tree")
        self.gridLayout = QGridLayout(self.tree_view_tree)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(8, 8, 8, 8)
        self.treeView = QTreeView(self.tree_view_tree)
        self.treeView.setObjectName(u"treeView")

        self.gridLayout.addWidget(self.treeView, 0, 0, 1, 1)

        self.tree.setWidget(self.tree_view_tree)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.tree)
        self.properties = QDockWidget(MainWindow)
        self.properties.setObjectName(u"properties")
        self.properties_view_prop = QWidget()
        self.properties_view_prop.setObjectName(u"properties_view_prop")
        self.gridLayout_2 = QGridLayout(self.properties_view_prop)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(8, 8, 8, 8)
        self.tableView = QTableView(self.properties_view_prop)
        self.tableView.setObjectName(u"tableView")

        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)

        self.properties.setWidget(self.properties_view_prop)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.properties)
        self.task = QDockWidget(MainWindow)
        self.task.setObjectName(u"task")
        self.task.setFloating(False)
        self.task_view = QWidget()
        self.task_view.setObjectName(u"task_view")
        self.gridLayout_7 = QGridLayout(self.task_view)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(8, 8, 8, 8)
        self.tabWidget_3 = QTabWidget(self.task_view)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.task_task = QWidget()
        self.task_task.setObjectName(u"task_task")
        self.verticalLayout_task_task = QVBoxLayout(self.task_task)
        self.verticalLayout_task_task.setSpacing(8)
        self.verticalLayout_task_task.setObjectName(u"verticalLayout_task_task")
        self.verticalLayout_task_task.setContentsMargins(6, 6, 6, 6)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(8)
        self.formLayout.setVerticalSpacing(6)
        self.lbl_aero_field = QLabel(self.task_task)
        self.lbl_aero_field.setObjectName(u"lbl_aero_field")
        self.lbl_aero_field.setVisible(False)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_aero_field)

        self.cmb_aero_field = QComboBox(self.task_task)
        self.cmb_aero_field.setObjectName(u"cmb_aero_field")
        self.cmb_aero_field.setVisible(False)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cmb_aero_field)

        self.btn_refresh_aero_plot = QPushButton(self.task_task)
        self.btn_refresh_aero_plot.setObjectName(u"btn_refresh_aero_plot")
        self.btn_refresh_aero_plot.setVisible(False)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.btn_refresh_aero_plot)


        self.verticalLayout_task_task.addLayout(self.formLayout)

        self.prelim_task_tools = QWidget(self.task_task)
        self.prelim_task_tools.setObjectName(u"prelim_task_tools")
        self.prelim_task_tools.setVisible(False)
        self.verticalLayout_prelim_task_tools = QVBoxLayout(self.prelim_task_tools)
        self.verticalLayout_prelim_task_tools.setSpacing(6)
        self.verticalLayout_prelim_task_tools.setObjectName(u"verticalLayout_prelim_task_tools")
        self.lbl_prelim_task_tools = QLabel(self.prelim_task_tools)
        self.lbl_prelim_task_tools.setObjectName(u"lbl_prelim_task_tools")

        self.verticalLayout_prelim_task_tools.addWidget(self.lbl_prelim_task_tools)

        self.btn_prelim_snap_grid = QPushButton(self.prelim_task_tools)
        self.btn_prelim_snap_grid.setObjectName(u"btn_prelim_snap_grid")
        self.btn_prelim_snap_grid.setCheckable(True)
        self.btn_prelim_snap_grid.setChecked(True)

        self.verticalLayout_prelim_task_tools.addWidget(self.btn_prelim_snap_grid)

        self.btn_prelim_snap_endpoint = QPushButton(self.prelim_task_tools)
        self.btn_prelim_snap_endpoint.setObjectName(u"btn_prelim_snap_endpoint")
        self.btn_prelim_snap_endpoint.setCheckable(True)
        self.btn_prelim_snap_endpoint.setChecked(True)

        self.verticalLayout_prelim_task_tools.addWidget(self.btn_prelim_snap_endpoint)

        self.btn_prelim_clear_sketch = QPushButton(self.prelim_task_tools)
        self.btn_prelim_clear_sketch.setObjectName(u"btn_prelim_clear_sketch")

        self.verticalLayout_prelim_task_tools.addWidget(self.btn_prelim_clear_sketch)


        self.verticalLayout_task_task.addWidget(self.prelim_task_tools)

        self.tabWidget_3.addTab(self.task_task, "")

        self.gridLayout_7.addWidget(self.tabWidget_3, 0, 0, 1, 1)

        self.task.setWidget(self.task_view)
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.task)
        self.cfd_console_dock = QDockWidget(MainWindow)
        self.cfd_console_dock.setObjectName(u"cfd_console_dock")
        self.cfd_console_dock.setVisible(False)
        self.cfd_console_dock_contents = QWidget()
        self.cfd_console_dock_contents.setObjectName(u"cfd_console_dock_contents")
        self.verticalLayout_cfd_console_dock = QVBoxLayout(self.cfd_console_dock_contents)
        self.verticalLayout_cfd_console_dock.setSpacing(6)
        self.verticalLayout_cfd_console_dock.setObjectName(u"verticalLayout_cfd_console_dock")
        self.verticalLayout_cfd_console_dock.setContentsMargins(8, 8, 8, 8)
        self.cfd_console_output = QPlainTextEdit(self.cfd_console_dock_contents)
        self.cfd_console_output.setObjectName(u"cfd_console_output")
        self.cfd_console_output.setReadOnly(True)

        self.verticalLayout_cfd_console_dock.addWidget(self.cfd_console_output)

        self.cfd_console_dock.setWidget(self.cfd_console_dock_contents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.cfd_console_dock)
        self.tree.raise_()

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuView.addAction(self.actionToggle_Tree_View)
        self.menuView.addAction(self.actionToggle_Properties)
        self.menuView.addAction(self.actionToggle_Task)
        self.menuSettings.addAction(self.actionPreference_2)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionAbout_AerGenesis)
        self.menuTools.addAction(self.actionRecalculate)
        self.menuTools.addAction(self.actionFind)
        self.menuTools.addAction(self.actionInspect)

        self.retranslateUi(MainWindow)

        self.ribbon_tabs.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(4)
        self.toolbox_preliminary_sizing.setCurrentIndex(5)
        self.toolBox_performance.setCurrentIndex(3)
        self.toolBox_2.setCurrentIndex(1)
        self.tabWidget_3.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.actionImport.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
        self.actionCopy.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        self.actionPaste.setText(QCoreApplication.translate("MainWindow", u"Paste", None))
        self.actionToggle_Tree_View.setText(QCoreApplication.translate("MainWindow", u"Toggle Tree View", None))
        self.actionToggle_Properties.setText(QCoreApplication.translate("MainWindow", u"Toggle Properties", None))
        self.actionToggle_Task.setText(QCoreApplication.translate("MainWindow", u"Toggle Task", None))
        self.actionPreference.setText(QCoreApplication.translate("MainWindow", u"Preference", None))
        self.actionPreference_2.setText(QCoreApplication.translate("MainWindow", u"Preference", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionAbout_AerGenesis.setText(QCoreApplication.translate("MainWindow", u"About AerGenesis", None))
        self.actionRefresh.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.actionRecalculate.setText(QCoreApplication.translate("MainWindow", u"Recalculate", None))
        self.actionFind.setText(QCoreApplication.translate("MainWindow", u"Find", None))
        self.actionInspect.setText(QCoreApplication.translate("MainWindow", u"Inspect", None))
        self.group_ribbon_home_case.setTitle(QCoreApplication.translate("MainWindow", u"Case", None))
        self.btn_ribbon_import_case.setText("📥")  # Import Case
        self.btn_ribbon_load_geometry.setText("🔺")  # Load Geometry
        self.btn_ribbon_save_config.setText("💾")  # Save Config
        self.btn_ribbon_load_config.setText("📂")  # Load Config
        self.btn_ribbon_export_case.setText("📤")  # Export Case
        self.btn_ribbon_open_case_folder.setText("📁")  # Open Folder
        self.group_ribbon_home_workspace.setTitle(QCoreApplication.translate("MainWindow", u"Workspace", None))
        self.btn_ribbon_toggle_tree.setText("🌳")  # Tree
        self.btn_ribbon_toggle_properties.setText("⚙️")  # Properties
        self.btn_ribbon_toggle_task.setText("📋")  # Task Panel
        self.btn_ribbon_show_console.setText("💬")  # Console
        self.btn_ribbon_reset_layout.setText("⟲")  # Reset Layout
        self.group_ribbon_home_camera.setTitle(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.btn_ribbon_reset_camera.setText("🎥")  # Reset Camera
        self.btn_ribbon_view_front.setText("⬇️")  # Front
        self.btn_ribbon_view_top.setText("⬆️")  # Top
        self.btn_ribbon_view_side.setText("⬅️")  # Side
        self.ribbon_tabs.setTabText(self.ribbon_tabs.indexOf(self.ribbon_home_tab), QCoreApplication.translate("MainWindow", u"Home", None))
        self.group_ribbon_mesh_panels.setTitle(QCoreApplication.translate("MainWindow", u"Setup Panels", None))
        self.btn_ribbon_show_geometry_panel.setText("📐")  # Geometry
        self.btn_ribbon_show_mesh_panel.setText("📦")  # blockMesh
        self.btn_ribbon_show_snappy_panel.setText("🌐")  # Snappy
        self.btn_ribbon_show_checkmesh_panel.setText("✓")  # CheckMesh
        self.group_ribbon_mesh_case.setTitle(QCoreApplication.translate("MainWindow", u"Case Build", None))
        self.btn_ribbon_generate_case.setText("⚡")  # Generate Case
        self.btn_ribbon_update_case.setText("🔄")  # Update Case
        self.btn_ribbon_clean_case.setText("🧹")  # Clean Case
        self.btn_ribbon_mesh_advice.setText("💡")  # Mesh Advice
        self.group_ribbon_mesh_execute.setTitle(QCoreApplication.translate("MainWindow", u"Run Mesh Stages", None))
        self.btn_ribbon_run_domain_mesh.setText("📦")  # blockMesh
        self.btn_ribbon_run_surface_features.setText("🔲")  # surfaceFeatureExtract
        self.btn_ribbon_run_snappy_mesh.setText("🌐")  # snappyHexMesh
        self.btn_ribbon_run_checkmesh.setText("✓")  # checkMesh
        self.ribbon_tabs.setTabText(self.ribbon_tabs.indexOf(self.ribbon_mesh_tab), QCoreApplication.translate("MainWindow", u"Mesh", None))
        self.group_ribbon_run_stage.setTitle(QCoreApplication.translate("MainWindow", u"Execution", None))
        self.lbl_ribbon_solver.setText(QCoreApplication.translate("MainWindow", u"Solver", None))
        self.lbl_ribbon_stage.setText(QCoreApplication.translate("MainWindow", u"Selected Stage", None))
        self.btn_ribbon_run_selected.setText("▶️")  # Run Selected
        self.btn_ribbon_run_pipeline.setText("🔗")  # Run Pipeline
        self.btn_ribbon_run_solve.setText("📊")  # Run Solve
        self.btn_ribbon_run_post.setText("📈")  # Run Post
        self.group_ribbon_run_logs.setTitle(QCoreApplication.translate("MainWindow", u"Logs", None))
        self.btn_ribbon_stop_run.setText("⏹️")  # Stop
        self.btn_ribbon_clear_console.setText("🗑️")  # Clear Console
        self.btn_ribbon_open_latest_log.setText("📄")  # Open Latest Log
        self.group_ribbon_run_status.setTitle(QCoreApplication.translate("MainWindow", u"Status", None))
        self.lbl_ribbon_run_status_label.setText(QCoreApplication.translate("MainWindow", u"Run Status", None))
        self.lbl_ribbon_run_status_value.setText(QCoreApplication.translate("MainWindow", u"idle", None))
        self.lbl_ribbon_active_stage_label.setText(QCoreApplication.translate("MainWindow", u"Active Stage", None))
        self.lbl_ribbon_active_stage_value.setText(QCoreApplication.translate("MainWindow", u"none", None))
        self.ribbon_tabs.setTabText(self.ribbon_tabs.indexOf(self.ribbon_run_tab), QCoreApplication.translate("MainWindow", u"Run", None))
        self.group_ribbon_results_data.setTitle(QCoreApplication.translate("MainWindow", u"Case Data", None))
        self.btn_ribbon_scan_results.setText(QCoreApplication.translate("MainWindow", u"Scan Results", None))
        self.btn_ribbon_open_paraview.setText(QCoreApplication.translate("MainWindow", u"Open ParaView", None))
        self.btn_ribbon_export_vtk.setText(QCoreApplication.translate("MainWindow", u"Export VTK", None))
        self.btn_ribbon_load_vtk.setText(QCoreApplication.translate("MainWindow", u"Load VTK", None))
        self.group_ribbon_results_fields.setTitle(QCoreApplication.translate("MainWindow", u"Field Display", None))
        self.btn_ribbon_result_pressure.setText(QCoreApplication.translate("MainWindow", u"Pressure", None))
        self.btn_ribbon_result_velocity.setText(QCoreApplication.translate("MainWindow", u"Velocity", None))
        self.btn_ribbon_apply_field.setText(QCoreApplication.translate("MainWindow", u"Apply Field", None))
        self.group_ribbon_results_view.setTitle(QCoreApplication.translate("MainWindow", u"Viewer", None))
        self.btn_ribbon_surface_mode.setText(QCoreApplication.translate("MainWindow", u"Surface", None))
        self.btn_ribbon_wireframe_mode.setText(QCoreApplication.translate("MainWindow", u"Wireframe", None))
        self.btn_ribbon_toggle_contours.setText(QCoreApplication.translate("MainWindow", u"Contours", None))
        self.btn_ribbon_toggle_slice.setText(QCoreApplication.translate("MainWindow", u"Slice", None))
        self.btn_ribbon_toggle_streamlines.setText(QCoreApplication.translate("MainWindow", u"Streamlines", None))
        self.btn_ribbon_toggle_tripod.setText(QCoreApplication.translate("MainWindow", u"XYZ Tripod", None))
        self.btn_ribbon_screenshot.setText(QCoreApplication.translate("MainWindow", u"Screenshot", None))
        self.ribbon_tabs.setTabText(self.ribbon_tabs.indexOf(self.ribbon_results_tab), QCoreApplication.translate("MainWindow", u"Results", None))
        self.input_k_ld.setText(QCoreApplication.translate("MainWindow", u"10.5", None))
        self.lbl_takeoff_distance.setText(QCoreApplication.translate("MainWindow", u"Take off Distance", None))
        self.lbl_swet_sref_ratio.setText(QCoreApplication.translate("MainWindow", u"Swet_Sref Ratio", None))
        self.lbl_payload_weight.setText(QCoreApplication.translate("MainWindow", u"Payload Weight", None))
        self.lbl_maximum_velocity_unit.setText(QCoreApplication.translate("MainWindow", u"ft/s", None))
        self.lbl_stall_speed.setText(QCoreApplication.translate("MainWindow", u"Stall Speed", None))
        self.lbl_geometric_constraints_section.setText(QCoreApplication.translate("MainWindow", u"Geometric Constraints", None))
        self.lbl_maximum_velocity.setText(QCoreApplication.translate("MainWindow", u"Maximum Velocity", None))
        self.btn_calculate_constraints.setText(QCoreApplication.translate("MainWindow", u"Calculate", None))
        self.lbl_stall_speed_unit.setText(QCoreApplication.translate("MainWindow", u"ft/s", None))
        self.lbl_payload_weight_unit.setText(QCoreApplication.translate("MainWindow", u"lbf", None))
        self.lbl_crew_passenger_weight.setText(QCoreApplication.translate("MainWindow", u"Crew/Passenger's Weight", None))
        self.lbl_aspect_ratio.setText(QCoreApplication.translate("MainWindow", u"Aspect Ratio", None))
        self.lbl_endurance_unit.setText(QCoreApplication.translate("MainWindow", u"s", None))
        self.lbl_performance_constraints_section.setText(QCoreApplication.translate("MainWindow", u"Performance Constraints", None))
        self.lbl_crew_passenger_weight_unit.setText(QCoreApplication.translate("MainWindow", u"lbf", None))
        self.lbl_endurance.setText(QCoreApplication.translate("MainWindow", u"Endurance", None))
        self.lbl_takeoff_distance_unit.setText(QCoreApplication.translate("MainWindow", u"ft", None))
        self.lbl_range_unit.setText(QCoreApplication.translate("MainWindow", u"ft", None))
        self.lbl_range.setText(QCoreApplication.translate("MainWindow", u"Range", None))
        self.label_k_ld.setText(QCoreApplication.translate("MainWindow", u"K_LD", None))
        self.label_k_ld_unit.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.lbl_rate_of_climb_unit.setText(QCoreApplication.translate("MainWindow", u"ft/s", None))
        self.lbl_service_ceiling_unit.setText(QCoreApplication.translate("MainWindow", u"ft", None))
        self.lbl_rate_of_climb.setText(QCoreApplication.translate("MainWindow", u"Rate of Climb", None))
        self.lbl_service_ceiling.setText(QCoreApplication.translate("MainWindow", u"Service Ceiling", None))
        self.toolbox_preliminary_sizing.setItemText(self.toolbox_preliminary_sizing.indexOf(self.page_constraints), QCoreApplication.translate("MainWindow", u"Constraints", None))
        self.toolbox_preliminary_sizing.setItemText(self.toolbox_preliminary_sizing.indexOf(self.page_mission_segment), QCoreApplication.translate("MainWindow", u"Mission Segment", None))
        self.lbl_initial_weight_output.setText(QCoreApplication.translate("MainWindow", u"Initial Weight Estimate Output", None))
        ___qtablewidgetitem = self.table_initial_weight_output.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Parameter", None));
        ___qtablewidgetitem1 = self.table_initial_weight_output.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Value", None));
        self.toolbox_preliminary_sizing.setItemText(self.toolbox_preliminary_sizing.indexOf(self.page_initial_weight_estimates), QCoreApplication.translate("MainWindow", u"Initial Weight Estimates", None))
        self.group_xfoil_settings.setTitle(QCoreApplication.translate("MainWindow", u"XFOIL Settings", None))
        self.lbl_xf_re.setText(QCoreApplication.translate("MainWindow", u"Reynolds Number", None))
        self.lbl_xf_panels.setText(QCoreApplication.translate("MainWindow", u"Panels", None))
        self.lbl_xf_mach.setText(QCoreApplication.translate("MainWindow", u"Mach Number", None))
        self.lbl_xf_ncrit.setText(QCoreApplication.translate("MainWindow", u"Ncrit", None))
        self.lbl_xf_iter.setText(QCoreApplication.translate("MainWindow", u"Iterations", None))
        self.group_naca_bounds.setTitle(QCoreApplication.translate("MainWindow", u"NACA 4-Digit Bounds", None))
        self.lbl_naca_camber_min.setText(QCoreApplication.translate("MainWindow", u"Camber Min", None))
        self.lbl_naca_camber_max.setText(QCoreApplication.translate("MainWindow", u"Camber Max", None))
        self.lbl_naca_camber_loc_min.setText(QCoreApplication.translate("MainWindow", u"Camber Loc Min", None))
        self.lbl_naca_camber_loc_max.setText(QCoreApplication.translate("MainWindow", u"Camber Loc Max", None))
        self.lbl_naca_thickness_min.setText(QCoreApplication.translate("MainWindow", u"Thickness Min", None))
        self.lbl_naca_thickness_max.setText(QCoreApplication.translate("MainWindow", u"Thickness Max", None))
        self.group_weight_application.setTitle(QCoreApplication.translate("MainWindow", u"Weight Application", None))
        self.lbl_w_cl.setText(QCoreApplication.translate("MainWindow", u"Weight Cl", None))
        self.lbl_w_cd.setText(QCoreApplication.translate("MainWindow", u"Weight Cd", None))
        self.lbl_w_ld.setText(QCoreApplication.translate("MainWindow", u"Weight L/Dmax", None))
        self.lbl_w_cm.setText(QCoreApplication.translate("MainWindow", u"Weight Cm", None))
        self.lbl_w_tc.setText(QCoreApplication.translate("MainWindow", u"Weight t/c", None))
        self.lbl_w_aoa.setText(QCoreApplication.translate("MainWindow", u"Weight AoA Margin", None))
        self.lbl_ideal_tc.setText(QCoreApplication.translate("MainWindow", u"Ideal t/c", None))
        self.lbl_tc_deviation.setText(QCoreApplication.translate("MainWindow", u"t/c Deviation", None))
        self.lbl_weight_total.setText(QCoreApplication.translate("MainWindow", u"Total Weight: 1.000", None))
        self.btn_run_airfoil_opt.setText(QCoreApplication.translate("MainWindow", u"Run Airfoil Optimization", None))
        self.btn_apply_airfoil_weights.setText(QCoreApplication.translate("MainWindow", u"Apply Weights / Rank", None))
        self.btn_use_top_airfoil.setText(QCoreApplication.translate("MainWindow", u"Use Top Airfoil", None))
        self.lbl_top_airfoil.setText(QCoreApplication.translate("MainWindow", u"Top Airfoil: (none)", None))
        self.group_drag_polar_estimates.setTitle(QCoreApplication.translate("MainWindow", u"Initial Drag Polar Estimates", None))
        self.lbl_drag_cd0_clean.setText(QCoreApplication.translate("MainWindow", u"Cd0 clean", None))
        self.lbl_drag_dcd0_takeoff.setText(QCoreApplication.translate("MainWindow", u"dCd0 takeoff", None))
        self.lbl_drag_dcd0_landing.setText(QCoreApplication.translate("MainWindow", u"dCd0 landing", None))
        self.lbl_drag_mu_ground.setText(QCoreApplication.translate("MainWindow", u"Ground factor (mu)", None))
        self.lbl_drag_cfg.setText(QCoreApplication.translate("MainWindow", u"Config", None))
        self.lbl_drag_cl.setText(QCoreApplication.translate("MainWindow", u"Cl", None))
        self.lbl_drag_e.setText(QCoreApplication.translate("MainWindow", u"Oswald e", None))
        self.lbl_drag_k.setText(QCoreApplication.translate("MainWindow", u"K = 1/(pi*AR*e)", None))
        self.lbl_drag_cd.setText(QCoreApplication.translate("MainWindow", u"Cd", None))
        self.lbl_drag_clean.setText(QCoreApplication.translate("MainWindow", u"Clean", None))
        self.lbl_drag_takeoff.setText(QCoreApplication.translate("MainWindow", u"Takeoff", None))
        self.lbl_drag_landing.setText(QCoreApplication.translate("MainWindow", u"Landing", None))
        self.lbl_drag_cd_ground.setText(QCoreApplication.translate("MainWindow", u"Cd ground-roll estimate (takeoff)", None))
        self.btn_estimate_drag_polar.setText(QCoreApplication.translate("MainWindow", u"Estimate Drag Polar", None))
        self.toolbox_preliminary_sizing.setItemText(self.toolbox_preliminary_sizing.indexOf(self.page_initial_drag_polar), QCoreApplication.translate("MainWindow", u"Initial Drag Polar Estimate", None))
        self.group_sizing_controls.setTitle(QCoreApplication.translate("MainWindow", u"Sizing Controls", None))
        self.btn_run_sizing.setText(QCoreApplication.translate("MainWindow", u"Run Sizing", None))
        self.group_sizing_summary.setTitle(QCoreApplication.translate("MainWindow", u"Sizing Summary", None))
        ___qtablewidgetitem2 = self.sizing_summary_table.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Parameter", None));
        ___qtablewidgetitem3 = self.sizing_summary_table.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Value", None));
        self.group_sizing_plot.setTitle(QCoreApplication.translate("MainWindow", u"Wing Loading vs Power Loading", None))
        self.group_sizing_stall.setTitle(QCoreApplication.translate("MainWindow", u"Sizing to Stall", None))
        self.group_sizing_rate_of_climb.setTitle(QCoreApplication.translate("MainWindow", u"Sizing to Rate of Climb", None))
        self.group_sizing_takeoff.setTitle(QCoreApplication.translate("MainWindow", u"Sizing to Take off", None))
        self.group_sizing_service_ceiling.setTitle(QCoreApplication.translate("MainWindow", u"Sizing to Service Ceiling", None))
        self.toolbox_preliminary_sizing.setItemText(self.toolbox_preliminary_sizing.indexOf(self.page_wing_power_loading_sizing), QCoreApplication.translate("MainWindow", u"Wing Loading and Power Loading Sizing", None))
        self.toolbox_preliminary_sizing.setItemText(self.toolbox_preliminary_sizing.indexOf(self.page_v_speeds_empennage), QCoreApplication.translate("MainWindow", u"V-Speeds and Empennage Sizing", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.prelim_tab), QCoreApplication.translate("MainWindow", u"Preliminary Sizing", None))
#if QT_CONFIG(whatsthis)
        self.geometry_modeler_tab.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.geometry_modeler_tab), QCoreApplication.translate("MainWindow", u"Geometry Modeler", None))
        self.btn_load_pressure_data.setText(QCoreApplication.translate("MainWindow", u"Load Pressure Data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.aerodynamics_tab), QCoreApplication.translate("MainWindow", u"Aerodynamics", None))
        self.lbl_structures_workspace_title.setText(QCoreApplication.translate("MainWindow", u"Structures Workspace", None))
        self.lbl_structures_workspace_subtitle.setText(QCoreApplication.translate("MainWindow", u"Select an item in the left tree to open its structural analysis panel.", None))
        self.lbl_structures_panel_title.setText(QCoreApplication.translate("MainWindow", u"External Loads", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.structures_tab), QCoreApplication.translate("MainWindow", u"Structures", None))
        self.lbl_propulsion_workspace_title.setText(QCoreApplication.translate("MainWindow", u"Propulsion Catalog Workspace", None))
        self.lbl_propulsion_workspace_subtitle.setText(QCoreApplication.translate("MainWindow", u"Manage engine and propeller catalogs for concept trade studies.", None))
        self.lbl_propulsion_panel_title.setText(QCoreApplication.translate("MainWindow", u"Engine Catalog", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.propulsion_tab), QCoreApplication.translate("MainWindow", u"Propulsion", None))
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Power Req HP", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Velocity (ft/s)", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.toolBox_performance.setItemText(self.toolBox_performance.indexOf(self.power_required), QCoreApplication.translate("MainWindow", u"Power Required/Thrust Required", None))
        self.toolBox_performance.setItemText(self.toolBox_performance.indexOf(self.power_available), QCoreApplication.translate("MainWindow", u"Power Available/Thrust Available", None))
        self.toolBox_performance.setItemText(self.toolBox_performance.indexOf(self.excess_power), QCoreApplication.translate("MainWindow", u"Excess Power and Climb Performance", None))
        self.toolBox_performance.setItemText(self.toolBox_performance.indexOf(self.service_ceiling), QCoreApplication.translate("MainWindow", u"Service Ceiling and Absolute Ceiling", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.performance_tab), QCoreApplication.translate("MainWindow", u"Performance Analysis", None))

        __sortingEnabled1 = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        self.listWidget.setSortingEnabled(__sortingEnabled1)

        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_5), QCoreApplication.translate("MainWindow", u"Metric", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_6), QCoreApplication.translate("MainWindow", u"Page 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.result_tab), QCoreApplication.translate("MainWindow", u"Result", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.tree.setWindowTitle(QCoreApplication.translate("MainWindow", u"Tree View", None))
        self.properties.setWindowTitle(QCoreApplication.translate("MainWindow", u"Properties", None))
        self.task.setWindowTitle("")
        self.lbl_aero_field.setText(QCoreApplication.translate("MainWindow", u"Aero Field:", None))
        self.btn_refresh_aero_plot.setText(QCoreApplication.translate("MainWindow", u"Refresh Plot", None))
        self.lbl_prelim_task_tools.setText(QCoreApplication.translate("MainWindow", u"Prelim Sketch Tools", None))
        self.btn_prelim_snap_grid.setText(QCoreApplication.translate("MainWindow", u"Snap Grid: On", None))
        self.btn_prelim_snap_endpoint.setText(QCoreApplication.translate("MainWindow", u"Snap Endpoint: On", None))
        self.btn_prelim_clear_sketch.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.task_task), QCoreApplication.translate("MainWindow", u"Task", None))
        self.cfd_console_dock.setWindowTitle(QCoreApplication.translate("MainWindow", u"CFD Console", None))
    # retranslateUi

