# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aerodynamics_workbench.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDockWidget, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMdiArea, QMenu,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QSplitter, QStatusBar, QTabWidget,
    QTreeView, QVBoxLayout, QWidget)

class Ui_CFDAerodynamicsWindow(object):
    def setupUi(self, CFDAerodynamicsWindow):
        if not CFDAerodynamicsWindow.objectName():
            CFDAerodynamicsWindow.setObjectName(u"CFDAerodynamicsWindow")
        CFDAerodynamicsWindow.resize(1400, 850)
        self.actionToggle_Tree_View = QAction(CFDAerodynamicsWindow)
        self.actionToggle_Tree_View.setObjectName(u"actionToggle_Tree_View")
        self.actionToggle_Properties_Panel = QAction(CFDAerodynamicsWindow)
        self.actionToggle_Properties_Panel.setObjectName(u"actionToggle_Properties_Panel")
        self.actionToggle_Task_Panel = QAction(CFDAerodynamicsWindow)
        self.actionToggle_Task_Panel.setObjectName(u"actionToggle_Task_Panel")
        self.actionToggle_Console = QAction(CFDAerodynamicsWindow)
        self.actionToggle_Console.setObjectName(u"actionToggle_Console")
        self.actionReset_Layout = QAction(CFDAerodynamicsWindow)
        self.actionReset_Layout.setObjectName(u"actionReset_Layout")
        self.actionNew = QAction(CFDAerodynamicsWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOpen = QAction(CFDAerodynamicsWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(CFDAerodynamicsWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(CFDAerodynamicsWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionExit = QAction(CFDAerodynamicsWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionUndo = QAction(CFDAerodynamicsWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(CFDAerodynamicsWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionCut = QAction(CFDAerodynamicsWindow)
        self.actionCut.setObjectName(u"actionCut")
        self.actionCopy = QAction(CFDAerodynamicsWindow)
        self.actionCopy.setObjectName(u"actionCopy")
        self.actionPaste = QAction(CFDAerodynamicsWindow)
        self.actionPaste.setObjectName(u"actionPaste")
        self.actionPreferences = QAction(CFDAerodynamicsWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.actionRecalculate = QAction(CFDAerodynamicsWindow)
        self.actionRecalculate.setObjectName(u"actionRecalculate")
        self.actionInspect = QAction(CFDAerodynamicsWindow)
        self.actionInspect.setObjectName(u"actionInspect")
        self.actionDocumentation = QAction(CFDAerodynamicsWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionAbout = QAction(CFDAerodynamicsWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(CFDAerodynamicsWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralLayout = QGridLayout(self.centralwidget)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setObjectName(u"centralLayout")
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.ribbon_frame = QFrame(self.centralwidget)
        self.ribbon_frame.setObjectName(u"ribbon_frame")
        self.ribbon_frame.setFrameShape(QFrame.NoFrame)
        self.ribbonLayout = QVBoxLayout(self.ribbon_frame)
        self.ribbonLayout.setSpacing(6)
        self.ribbonLayout.setObjectName(u"ribbonLayout")
        self.ribbonLayout.setContentsMargins(8, 6, 8, 6)
        self.ribbonToolsLayout = QHBoxLayout()
        self.ribbonToolsLayout.setSpacing(12)
        self.ribbonToolsLayout.setObjectName(u"ribbonToolsLayout")
        self.group_case_tools = QGroupBox(self.ribbon_frame)
        self.group_case_tools.setObjectName(u"group_case_tools")
        self.gridLayout_case = QGridLayout(self.group_case_tools)
        self.gridLayout_case.setObjectName(u"gridLayout_case")
        self.btn_ribbon_import_case = QPushButton(self.group_case_tools)
        self.btn_ribbon_import_case.setObjectName(u"btn_ribbon_import_case")

        self.gridLayout_case.addWidget(self.btn_ribbon_import_case, 0, 0, 1, 1)

        self.btn_ribbon_load_geometry = QPushButton(self.group_case_tools)
        self.btn_ribbon_load_geometry.setObjectName(u"btn_ribbon_load_geometry")

        self.gridLayout_case.addWidget(self.btn_ribbon_load_geometry, 0, 1, 1, 1)

        self.btn_ribbon_save_config = QPushButton(self.group_case_tools)
        self.btn_ribbon_save_config.setObjectName(u"btn_ribbon_save_config")

        self.gridLayout_case.addWidget(self.btn_ribbon_save_config, 1, 0, 1, 1)

        self.btn_ribbon_load_config = QPushButton(self.group_case_tools)
        self.btn_ribbon_load_config.setObjectName(u"btn_ribbon_load_config")

        self.gridLayout_case.addWidget(self.btn_ribbon_load_config, 1, 1, 1, 1)

        self.btn_ribbon_export_case = QPushButton(self.group_case_tools)
        self.btn_ribbon_export_case.setObjectName(u"btn_ribbon_export_case")

        self.gridLayout_case.addWidget(self.btn_ribbon_export_case, 2, 0, 1, 1)

        self.btn_ribbon_open_case_folder = QPushButton(self.group_case_tools)
        self.btn_ribbon_open_case_folder.setObjectName(u"btn_ribbon_open_case_folder")

        self.gridLayout_case.addWidget(self.btn_ribbon_open_case_folder, 2, 1, 1, 1)


        self.ribbonToolsLayout.addWidget(self.group_case_tools)

        self.group_workspace_tools = QGroupBox(self.ribbon_frame)
        self.group_workspace_tools.setObjectName(u"group_workspace_tools")
        self.gridLayout_workspace = QGridLayout(self.group_workspace_tools)
        self.gridLayout_workspace.setObjectName(u"gridLayout_workspace")
        self.btn_ribbon_toggle_tree = QPushButton(self.group_workspace_tools)
        self.btn_ribbon_toggle_tree.setObjectName(u"btn_ribbon_toggle_tree")
        self.btn_ribbon_toggle_tree.setCheckable(True)
        self.btn_ribbon_toggle_tree.setChecked(True)

        self.gridLayout_workspace.addWidget(self.btn_ribbon_toggle_tree, 0, 0, 1, 1)

        self.btn_ribbon_toggle_properties = QPushButton(self.group_workspace_tools)
        self.btn_ribbon_toggle_properties.setObjectName(u"btn_ribbon_toggle_properties")
        self.btn_ribbon_toggle_properties.setCheckable(True)
        self.btn_ribbon_toggle_properties.setChecked(True)

        self.gridLayout_workspace.addWidget(self.btn_ribbon_toggle_properties, 0, 1, 1, 1)

        self.btn_ribbon_toggle_task = QPushButton(self.group_workspace_tools)
        self.btn_ribbon_toggle_task.setObjectName(u"btn_ribbon_toggle_task")
        self.btn_ribbon_toggle_task.setCheckable(True)
        self.btn_ribbon_toggle_task.setChecked(True)

        self.gridLayout_workspace.addWidget(self.btn_ribbon_toggle_task, 0, 2, 1, 1)

        self.btn_ribbon_show_console = QPushButton(self.group_workspace_tools)
        self.btn_ribbon_show_console.setObjectName(u"btn_ribbon_show_console")
        self.btn_ribbon_show_console.setCheckable(True)

        self.gridLayout_workspace.addWidget(self.btn_ribbon_show_console, 1, 0, 1, 1)

        self.btn_ribbon_reset_layout = QPushButton(self.group_workspace_tools)
        self.btn_ribbon_reset_layout.setObjectName(u"btn_ribbon_reset_layout")

        self.gridLayout_workspace.addWidget(self.btn_ribbon_reset_layout, 1, 1, 1, 2)


        self.ribbonToolsLayout.addWidget(self.group_workspace_tools)

        self.group_camera_tools = QGroupBox(self.ribbon_frame)
        self.group_camera_tools.setObjectName(u"group_camera_tools")
        self.gridLayout_camera = QGridLayout(self.group_camera_tools)
        self.gridLayout_camera.setObjectName(u"gridLayout_camera")
        self.btn_ribbon_reset_camera = QPushButton(self.group_camera_tools)
        self.btn_ribbon_reset_camera.setObjectName(u"btn_ribbon_reset_camera")

        self.gridLayout_camera.addWidget(self.btn_ribbon_reset_camera, 0, 0, 1, 1)

        self.btn_ribbon_view_front = QPushButton(self.group_camera_tools)
        self.btn_ribbon_view_front.setObjectName(u"btn_ribbon_view_front")

        self.gridLayout_camera.addWidget(self.btn_ribbon_view_front, 0, 1, 1, 1)

        self.btn_ribbon_view_top = QPushButton(self.group_camera_tools)
        self.btn_ribbon_view_top.setObjectName(u"btn_ribbon_view_top")

        self.gridLayout_camera.addWidget(self.btn_ribbon_view_top, 1, 0, 1, 1)

        self.btn_ribbon_view_side = QPushButton(self.group_camera_tools)
        self.btn_ribbon_view_side.setObjectName(u"btn_ribbon_view_side")

        self.gridLayout_camera.addWidget(self.btn_ribbon_view_side, 1, 1, 1, 1)


        self.ribbonToolsLayout.addWidget(self.group_camera_tools)

        self.ribbonSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.ribbonToolsLayout.addItem(self.ribbonSpacer)


        self.ribbonLayout.addLayout(self.ribbonToolsLayout)


        self.centralLayout.addWidget(self.ribbon_frame, 0, 0, 1, 1)

        self.mainContent = QFrame(self.centralwidget)
        self.mainContent.setObjectName(u"mainContent")
        self.mainContent.setFrameShape(QFrame.NoFrame)
        self.mainContentLayout = QGridLayout(self.mainContent)
        self.mainContentLayout.setSpacing(0)
        self.mainContentLayout.setObjectName(u"mainContentLayout")
        self.mainContentLayout.setContentsMargins(0, 0, 0, 0)
        self.mainSplitter = QSplitter(self.mainContent)
        self.mainSplitter.setObjectName(u"mainSplitter")
        self.mainSplitter.setOrientation(Qt.Horizontal)
        self.mdiArea = QMdiArea(self.mainSplitter)
        self.mdiArea.setObjectName(u"mdiArea")
        brush = QBrush(QColor(40, 40, 40, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.mdiArea.setBackground(brush)
        self.mainSplitter.addWidget(self.mdiArea)
        self.codeEditorFrame = QFrame(self.mainSplitter)
        self.codeEditorFrame.setObjectName(u"codeEditorFrame")
        self.codeEditorFrame.setFrameShape(QFrame.NoFrame)
        self.codeEditorLayout = QVBoxLayout(self.codeEditorFrame)
        self.codeEditorLayout.setSpacing(0)
        self.codeEditorLayout.setObjectName(u"codeEditorLayout")
        self.codeEditorLayout.setContentsMargins(0, 0, 0, 0)
        self.codeEditorTabs = QTabWidget(self.codeEditorFrame)
        self.codeEditorTabs.setObjectName(u"codeEditorTabs")
        self.defaultCodeTab = QWidget()
        self.defaultCodeTab.setObjectName(u"defaultCodeTab")
        self.verticalLayout_defaultTab = QVBoxLayout(self.defaultCodeTab)
        self.verticalLayout_defaultTab.setSpacing(0)
        self.verticalLayout_defaultTab.setObjectName(u"verticalLayout_defaultTab")
        self.verticalLayout_defaultTab.setContentsMargins(0, 0, 0, 0)
        self.codeEditor_default = QPlainTextEdit(self.defaultCodeTab)
        self.codeEditor_default.setObjectName(u"codeEditor_default")
        font = QFont()
        font.setFamilies([u"Courier New"])
        font.setPointSize(10)
        self.codeEditor_default.setFont(font)

        self.verticalLayout_defaultTab.addWidget(self.codeEditor_default)

        self.codeEditorTabs.addTab(self.defaultCodeTab, "")

        self.codeEditorLayout.addWidget(self.codeEditorTabs)

        self.mainSplitter.addWidget(self.codeEditorFrame)

        self.mainContentLayout.addWidget(self.mainSplitter, 0, 0, 1, 1)


        self.centralLayout.addWidget(self.mainContent, 1, 0, 1, 1)

        CFDAerodynamicsWindow.setCentralWidget(self.centralwidget)
        self.tree = QDockWidget(CFDAerodynamicsWindow)
        self.tree.setObjectName(u"tree")
        self.tree_view_contents = QWidget()
        self.tree_view_contents.setObjectName(u"tree_view_contents")
        self.treeLayout = QGridLayout(self.tree_view_contents)
        self.treeLayout.setObjectName(u"treeLayout")
        self.treeView = QTreeView(self.tree_view_contents)
        self.treeView.setObjectName(u"treeView")

        self.treeLayout.addWidget(self.treeView, 0, 0, 1, 1)

        self.tree.setWidget(self.tree_view_contents)
        CFDAerodynamicsWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.tree)
        self.properties = QDockWidget(CFDAerodynamicsWindow)
        self.properties.setObjectName(u"properties")
        self.properties_contents = QWidget()
        self.properties_contents.setObjectName(u"properties_contents")
        self.propertiesLayout = QVBoxLayout(self.properties_contents)
        self.propertiesLayout.setObjectName(u"propertiesLayout")
        self.properties_tab_widget = QTabWidget(self.properties_contents)
        self.properties_tab_widget.setObjectName(u"properties_tab_widget")
        self.task_task = QWidget()
        self.task_task.setObjectName(u"task_task")
        self.verticalLayout_task_task = QVBoxLayout(self.task_task)
        self.verticalLayout_task_task.setSpacing(0)
        self.verticalLayout_task_task.setObjectName(u"verticalLayout_task_task")
        self.verticalLayout_task_task.setContentsMargins(0, 0, 0, 0)
        self.lbl_aero_field = QLabel(self.task_task)
        self.lbl_aero_field.setObjectName(u"lbl_aero_field")
        self.lbl_aero_field.setVisible(False)

        self.verticalLayout_task_task.addWidget(self.lbl_aero_field)

        self.cmb_aero_field = QComboBox(self.task_task)
        self.cmb_aero_field.setObjectName(u"cmb_aero_field")
        self.cmb_aero_field.setVisible(False)

        self.verticalLayout_task_task.addWidget(self.cmb_aero_field)

        self.btn_refresh_aero_plot = QPushButton(self.task_task)
        self.btn_refresh_aero_plot.setObjectName(u"btn_refresh_aero_plot")
        self.btn_refresh_aero_plot.setVisible(False)

        self.verticalLayout_task_task.addWidget(self.btn_refresh_aero_plot)

        self.properties_tab_widget.addTab(self.task_task, "")

        self.propertiesLayout.addWidget(self.properties_tab_widget)

        self.properties.setWidget(self.properties_contents)
        CFDAerodynamicsWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties)
        self.cfd_console_dock = QDockWidget(CFDAerodynamicsWindow)
        self.cfd_console_dock.setObjectName(u"cfd_console_dock")
        self.cfd_console_dock_contents = QWidget()
        self.cfd_console_dock_contents.setObjectName(u"cfd_console_dock_contents")
        self.verticalLayout_cfd_console_dock = QVBoxLayout(self.cfd_console_dock_contents)
        self.verticalLayout_cfd_console_dock.setSpacing(8)
        self.verticalLayout_cfd_console_dock.setObjectName(u"verticalLayout_cfd_console_dock")
        self.verticalLayout_cfd_console_dock.setContentsMargins(8, 8, 8, 8)
        self.cfd_console_output = QPlainTextEdit(self.cfd_console_dock_contents)
        self.cfd_console_output.setObjectName(u"cfd_console_output")
        self.cfd_console_output.setReadOnly(True)

        self.verticalLayout_cfd_console_dock.addWidget(self.cfd_console_output)

        self.cfd_console_dock.setWidget(self.cfd_console_dock_contents)
        CFDAerodynamicsWindow.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.cfd_console_dock)
        self.menubar = QMenuBar(CFDAerodynamicsWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1400, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        CFDAerodynamicsWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(CFDAerodynamicsWindow)
        self.statusbar.setObjectName(u"statusbar")
        CFDAerodynamicsWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuView.addAction(self.actionToggle_Tree_View)
        self.menuView.addAction(self.actionToggle_Properties_Panel)
        self.menuView.addAction(self.actionToggle_Task_Panel)
        self.menuView.addAction(self.actionToggle_Console)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionReset_Layout)
        self.menuSettings.addAction(self.actionPreferences)
        self.menuTools.addAction(self.actionRecalculate)
        self.menuTools.addAction(self.actionInspect)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(CFDAerodynamicsWindow)

        self.codeEditorTabs.setCurrentIndex(0)
        self.properties_tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CFDAerodynamicsWindow)
    # setupUi

    def retranslateUi(self, CFDAerodynamicsWindow):
        CFDAerodynamicsWindow.setWindowTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"CFD Aerodynamics Workbench", None))
        self.actionToggle_Tree_View.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Toggle Tree View", None))
        self.actionToggle_Properties_Panel.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Toggle Properties Panel", None))
        self.actionToggle_Task_Panel.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Toggle Task Panel", None))
        self.actionToggle_Console.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Toggle Console", None))
        self.actionReset_Layout.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Reset Layout", None))
        self.actionNew.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"New", None))
#if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_As.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Save As", None))
#if QT_CONFIG(shortcut)
        self.actionSave_As.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionUndo.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Undo", None))
#if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Redo", None))
#if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"Ctrl+Y", None))
#endif // QT_CONFIG(shortcut)
        self.actionCut.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Cut", None))
#if QT_CONFIG(shortcut)
        self.actionCut.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.actionCopy.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Copy", None))
#if QT_CONFIG(shortcut)
        self.actionCopy.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.actionPaste.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Paste", None))
#if QT_CONFIG(shortcut)
        self.actionPaste.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"Ctrl+V", None))
#endif // QT_CONFIG(shortcut)
        self.actionPreferences.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Preferences", None))
#if QT_CONFIG(shortcut)
        self.actionPreferences.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"Ctrl+,", None))
#endif // QT_CONFIG(shortcut)
        self.actionRecalculate.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Recalculate", None))
#if QT_CONFIG(shortcut)
        self.actionRecalculate.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.actionInspect.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Inspect", None))
        self.actionDocumentation.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Documentation", None))
#if QT_CONFIG(shortcut)
        self.actionDocumentation.setShortcut(QCoreApplication.translate("CFDAerodynamicsWindow", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"About CFD Workbench", None))
        self.centralwidget.setStyleSheet(QCoreApplication.translate("CFDAerodynamicsWindow", u"background-color: #2b2b2b;", None))
        self.group_case_tools.setTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"Case Management", None))
        self.btn_ribbon_import_case.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Import Case", None))
        self.btn_ribbon_load_geometry.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Load Geometry", None))
        self.btn_ribbon_save_config.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Save Config", None))
        self.btn_ribbon_load_config.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Load Config", None))
        self.btn_ribbon_export_case.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Generate Case", None))
        self.btn_ribbon_open_case_folder.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Open Folder", None))
        self.group_workspace_tools.setTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"Workspace", None))
        self.btn_ribbon_toggle_tree.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"\U0001f333 Tree", None))
        self.btn_ribbon_toggle_properties.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"\u2699\ufe0f Properties", None))
        self.btn_ribbon_toggle_task.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"\U0001f4cb Task Panel", None))
        self.btn_ribbon_show_console.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"\U0001f4bb Console", None))
        self.btn_ribbon_reset_layout.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Reset Layout", None))
        self.group_camera_tools.setTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"Camera", None))
        self.btn_ribbon_reset_camera.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Reset", None))
        self.btn_ribbon_view_front.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Front", None))
        self.btn_ribbon_view_top.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Top", None))
        self.btn_ribbon_view_side.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Side", None))
        self.codeEditorTabs.setStyleSheet(QCoreApplication.translate("CFDAerodynamicsWindow", u"QTabWidget::pane { border: 1px solid #555; }\n"
"QTabBar::tab { background-color: #3c3c3c; color: #fff; padding: 4px 10px; border: 1px solid #555; }\n"
"QTabBar::tab:selected { background-color: #555; }", None))
        self.codeEditor_default.setStyleSheet(QCoreApplication.translate("CFDAerodynamicsWindow", u"QPlainTextEdit { background-color: #1e1e1e; color: #d4d4d4; font-family: 'Courier New', monospace; font-size: 10pt; border: none; }", None))
        self.codeEditorTabs.setTabText(self.codeEditorTabs.indexOf(self.defaultCodeTab), QCoreApplication.translate("CFDAerodynamicsWindow", u"+ New File", None))
        self.tree.setWindowTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"Project Tree", None))
        self.properties.setWindowTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"Properties", None))
        self.lbl_aero_field.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Aero Field:", None))
        self.btn_refresh_aero_plot.setText(QCoreApplication.translate("CFDAerodynamicsWindow", u"Refresh Plot", None))
        self.properties_tab_widget.setTabText(self.properties_tab_widget.indexOf(self.task_task), QCoreApplication.translate("CFDAerodynamicsWindow", u"Task", None))
        self.cfd_console_dock.setWindowTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"CFD Console", None))
        self.menuFile.setTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"View", None))
        self.menuSettings.setTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"Settings", None))
        self.menuTools.setTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"Tools", None))
        self.menuHelp.setTitle(QCoreApplication.translate("CFDAerodynamicsWindow", u"Help", None))
    # retranslateUi

