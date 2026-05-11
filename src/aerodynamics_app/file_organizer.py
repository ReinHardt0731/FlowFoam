"""File organizer widget for browsing project files."""

from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont


class FileOrganizerWidget(QWidget):
    """File browser widget showing project hierarchy."""
    
    file_selected = Signal(str)  # Changed from Signal(Path) for PySide6 compatibility
    
    # Common file extensions to show
    DEFAULT_EXTENSIONS = {'.py', '.json', '.yaml', '.yml', '.txt', '.cfg', 
                         '.foam', '.stl', '.dict', '.sh', '.bat', '.md'}
    IGNORE_PATTERNS = {
        '.git',
        '__pycache__',
        '.pytest_cache',
        'node_modules',
        '.venv',
        'venv',
        'vendor',
        'workspace',
    }
    
    def __init__(self, root_path=None, parent=None):
        super().__init__(parent)
        self.root_path = Path(root_path or ".")
        self.current_filter = None
        self._init_ui()
        self._populate_tree()
    
    def _init_ui(self):
        """Setup the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Controls
        controls = QHBoxLayout()
        
        # Filter dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("All Files", None)
        self.filter_combo.addItem("Python (.py)", {'.py'})
        self.filter_combo.addItem("JSON (.json)", {'.json'})
        self.filter_combo.addItem("Config (.yaml, .yml)", {'.yaml', '.yml'})
        self.filter_combo.addItem("OpenFOAM (.foam, .dict)", {'.foam', '.dict'})
        self.filter_combo.currentIndexChanged.connect(self._on_filter_changed)
        controls.addWidget(self.filter_combo)
        
        # Refresh button
        refresh_btn = QPushButton("↻")
        refresh_btn.setMaximumWidth(32)
        refresh_btn.setToolTip("Refresh file list")
        refresh_btn.clicked.connect(self._populate_tree)
        controls.addWidget(refresh_btn)
        
        layout.addLayout(controls)
        
        # File tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Project Files")
        self.tree.setColumnCount(1)
        self.tree.itemDoubleClicked.connect(self._on_item_double_click)
        self.tree.itemSelectionChanged.connect(self._on_item_selected)
        layout.addWidget(self.tree)
    
    def _populate_tree(self):
        """Recursively populate tree with files and folders."""
        self.tree.clear()
        root_item = QTreeWidgetItem(self.tree)
        root_item.setText(0, self.root_path.name or str(self.root_path))
        root_item.setData(0, Qt.UserRole, str(self.root_path))
        root_item.setFont(0, self._get_bold_font())
        
        self._add_files(root_item, self.root_path)
        self.tree.expandAll()
    
    def _add_files(self, parent_item, path):
        """Recursively add files and folders to tree."""
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            for item in items:
                # Skip hidden and ignored
                if item.name.startswith('.') or item.name in self.IGNORE_PATTERNS:
                    continue
                if item.is_dir() and path.name == 'tests' and item.name == 'fixtures':
                    continue
                
                # Apply filter if set
                if self.current_filter and item.is_file():
                    if item.suffix not in self.current_filter:
                        continue
                
                tree_item = QTreeWidgetItem(parent_item)
                
                # Set text with icon
                if item.is_dir():
                    tree_item.setText(0, f"📁 {item.name}")
                    tree_item.setData(0, Qt.UserRole, str(item))
                    # Recursively add folder contents
                    self._add_files(tree_item, item)
                else:
                    # Get file icon based on extension
                    icon = self._get_file_icon(item)
                    tree_item.setText(0, f"{icon} {item.name}")
                    tree_item.setData(0, Qt.UserRole, str(item))
        except (PermissionError, OSError):
            pass
    
    def _get_file_icon(self, path: Path) -> str:
        """Get emoji icon for file type."""
        ext = path.suffix.lower()
        icons = {
            '.py': '🐍',
            '.json': '⚙️',
            '.yaml': '📋',
            '.yml': '📋',
            '.txt': '📄',
            '.cfg': '⚙️',
            '.foam': '💨',
            '.stl': '🔲',
            '.dict': '📖',
            '.sh': '🔧',
            '.bat': '🔧',
            '.md': '📝',
            '.ui': '🎨',
            '.iso': '💿',
        }
        return icons.get(ext, '📃')
    
    def _get_bold_font(self) -> QFont:
        """Get bold font."""
        font = QFont()
        font.setBold(True)
        return font
    
    def _on_filter_changed(self, index):
        """Handle filter change."""
        self.current_filter = self.filter_combo.currentData()
        self._populate_tree()
    
    def _on_item_selected(self):
        """Handle item selection."""
        item = self.tree.currentItem()
        if item:
            path_str = item.data(0, Qt.UserRole)
            if path_str:
                # Strip whitespace from path
                path_str = path_str.strip()
                path = Path(path_str)
                if path.is_file():
                    self.file_selected.emit(str(path))  # Emit as string for PySide6 compatibility
    
    def _on_item_double_click(self, item, column):
        """Handle double-click (same as single for files)."""
        path_str = item.data(0, Qt.UserRole)
        if path_str:
            # Strip whitespace from path
            path_str = path_str.strip()
            path = Path(path_str)
            if path.is_file():
                self.file_selected.emit(str(path))  # Emit as string for PySide6 compatibility
    
    def get_selected_file(self) -> Path:
        """Get the currently selected file path."""
        item = self.tree.currentItem()
        if item:
            path_str = item.data(Qt.UserRole)
            if path_str:
                path = Path(path_str)
                if path.is_file():
                    return path
        return None
