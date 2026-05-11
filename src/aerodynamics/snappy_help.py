"""SnappyHexMesh Help System - Provides tooltips and guidance for mesh parameters."""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QPlainTextEdit


class SnappyHexMeshHelpDialog(QDialog):
    """Help dialog for snappyHexMesh parameters."""
    
    HELP_TEXT = {
        # Main flags
        "castellatedMesh": "Enable/disable castellation mesh generation.",
        "snap": "Enable/disable snapping to surface geometry.",
        "addLayers": "Enable/disable boundary layer (prism) generation.",
        
        # Globals
        "maxLocalCells": "Maximum number of cells per processor domain.",
        "maxGlobalCells": "Maximum total cells across all processors.",
        "minRefinementCells": "Minimum cells before stopping refinement.",
        
        # Castellation
        "nCellsBetweenLevels": "[Placeholder] Number of cells between refinement levels.",
        "maxLoadUnbalance": "[Placeholder] Maximum load imbalance between processors.",
        "features": "[Placeholder] Feature edge extraction level.",
        
        # Surface refinement
        "level": "[Placeholder] Surface refinement level (min max).",
        "gapLevelIncrement": "[Placeholder] Gap level increment for features.",
        "gapMode": "[Placeholder] Gap mode (resolve/uniform).",
        "angle": "[Placeholder] Feature angle threshold.",
        
        # Snapping
        "nSmooth": "[Placeholder] Number of smoothing iterations.",
        "nSnapIter": "[Placeholder] Number of snapping iterations.",
        "nSmoothPatch": "[Placeholder] Smooth patch iterations.",
        "nRelaxIter": "[Placeholder] Number of smoothing relaxation iterations.",
        "nFeatureSnapIter": "[Placeholder] Feature snapping iterations.",
        "implicitFeatureSnap": "[Placeholder] Use implicit feature snapping.",
        "explicitFeatureSnap": "[Placeholder] Use explicit feature snapping.",
        "multiRegionFeatureSnap": "[Placeholder] Multi-region feature snapping.",
        
        # Layers
        "nSurfaceLayers": "[Placeholder] Number of boundary layers to generate.",
        "expansionRatio": "[Placeholder] Expansion ratio between successive layers.",
        "finalLayerThickness": "[Placeholder] Thickness of outermost layer (as ratio).",
        "minThickness": "[Placeholder] Minimum layer thickness.",
        "nGrow": "[Placeholder] Number of cells to grow layers into.",
        "featureAngle": "[Placeholder] Feature angle for layer orientation.",
        "slipFeatureAngle": "[Placeholder] Slip feature angle threshold.",
        "nRelaxIterLayer": "[Placeholder] Layer relaxation iterations.",
        "nSmoothSurfaceNormals": "[Placeholder] Surface normal smoothing iterations.",
        "nSmoothNormals": "[Placeholder] Normal smoothing iterations.",
        "nSmoothThickness": "[Placeholder] Thickness smoothing iterations.",
        "maxFaceThicknessRatio": "[Placeholder] Maximum face to layer thickness ratio.",
        "maxThicknessToMedialRatio": "[Placeholder] Maximum thickness to medial ratio.",
        "minMedialAxisAngle": "[Placeholder] Minimum medial axis angle.",
        "nBufferCellsNoExtrude": "[Placeholder] Buffer cells without extrusion.",
        "nLayerIter": "[Placeholder] Maximum layer iterations.",
        "mergeTolerance": "[Placeholder] Merge tolerance for geometry.",
        
        # Refinement box
        "refinementBox_enable": "[Placeholder] Enable refinement box for targeted refinement.",
        "refinement_level": "[Placeholder] Refinement level in box (0-10).",
        "Refine_Min_X": "[Placeholder] Refinement box minimum X coordinate.",
        "Refine_Min_Y": "[Placeholder] Refinement box minimum Y coordinate.",
        "Refine_Min_Z": "[Placeholder] Refinement box minimum Z coordinate.",
        "Refine_Max_X": "[Placeholder] Refinement box maximum X coordinate.",
        "Refine_Max_Y": "[Placeholder] Refinement box maximum Y coordinate.",
        "Refine_Max_Z": "[Placeholder] Refinement box maximum Z coordinate.",
        
        # Profile and parallel
        "snappy_profile": "[Placeholder] Mesh profile: Balanced/Fast/High Fidelity/Custom.",
        "snappy_parallel": "[Placeholder] Parallel execution mode.",
        
        # Mesh limits
        "refinement_min": "[Placeholder] Minimum refinement level.",
        "refinement_max": "[Placeholder] Maximum refinement level.",
        "Resolve_Feature_Angle": "[Placeholder] Angle threshold for feature resolution.",
        
        # Additional parameters
        "maxLocalCells": "[Placeholder] Max local cells per processor.",
        "maxGlobalCells": "[Placeholder] Max global cells total.",
        "minRefinementCells": "[Placeholder] Min refinement cells.",
        "maxLoadUnbalance": "[Placeholder] Max load unbalance.",
        "nFeatureSnapIter": "[Placeholder] Number of feature snap iterations.",
        "expansionRatio": "[Placeholder] Expansion ratio for layers.",
        "finalLayerThickness": "[Placeholder] Final layer thickness.",
        "minThickness": "[Placeholder] Minimum layer thickness.",
        "nGrow": "[Placeholder] Growth control.",
        "layer_featureAngle": "[Placeholder] Layer feature angle.",
        "slipFeatureAngle": "[Placeholder] Slip feature angle.",
        "layer_nRelaxIter": "[Placeholder] Layer relaxation iterations.",
        "nSmoothSurfaceNormals": "[Placeholder] Surface normal smoothing.",
        "nSmoothNormals": "[Placeholder] Normal smoothing.",
        "nSmoothThickness": "[Placeholder] Thickness smoothing.",
        "maxFaceThicknessRatio": "[Placeholder] Max face thickness ratio.",
        "maxThicknessToMedialRatio": "[Placeholder] Max thickness to medial ratio.",
        "minMedialAxisAngle": "[Placeholder] Min medial axis angle.",
        "nBufferCellsNoExtrude": "[Placeholder] Buffer cells no extrude.",
        "nLayerIter": "[Placeholder] Max layer iterations.",
        "mergeTolerance": "[Placeholder] Merge tolerance.",
        "allowFreeStandingZoneFaces": "[Placeholder] Allow free standing zone faces.",
    }
    
    def __init__(self, parameter_key: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Help - {parameter_key}")
        self.setGeometry(100, 100, 500, 250)
        self.setup_ui(parameter_key)
    
    def setup_ui(self, param_key: str):
        layout = QVBoxLayout(self)
        
        # Get help text, use placeholder if not found
        help_text = self.HELP_TEXT.get(param_key, f"[Documentation for '{param_key}' - Add here]")
        
        title_label = QLabel(param_key)
        title_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(title_label)
        
        text_display = QPlainTextEdit()
        text_display.setPlainText(help_text)
        text_display.setReadOnly(True)
        text_display.setMaximumHeight(150)
        layout.addWidget(text_display)
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)


def create_help_button(param_key: str, parent=None):
    """Create a help button that opens a help dialog."""
    btn = QPushButton("?", parent)
    btn.setMaximumWidth(30)
    btn.setStyleSheet("""
        QPushButton {
            background-color: #4a7ba7;
            color: white;
            font-weight: bold;
            border-radius: 4px;
            padding: 2px;
            min-height: 20px;
        }
        QPushButton:hover {
            background-color: #5a8bb7;
        }
        QPushButton:pressed {
            background-color: #3a6b97;
        }
    """)
    btn.clicked.connect(lambda: SnappyHexMeshHelpDialog(param_key, parent).exec())
    return btn
