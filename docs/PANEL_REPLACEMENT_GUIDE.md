# Panel Replacement Guide

Yes, you can completely replace the tree dock and task dock with your own custom widgets!

## Current Layout

```
┌─────────────────────────────────────────┐
│           Ribbon (Minimizable)          │
├──────────────────┬──────────────────────┤
│                  │                      │
│   Tree Dock      │   Viewer             │
│ (Model Tree)     │   (3D view)          │
│                  │                      │
├──────────────────┤                      │
│                  │                      │
│   Task Dock      │                      │
│  (Panels:        │                      │
│   Geometry,      │                      │
│   Mesh, etc)     │                      │
│                  │                      │
├──────────────────────────────────────────┤
│  CFD Console (Bottom)                    │
└──────────────────────────────────────────┘
```

## Option 1: File Organizer in Tree Dock + Code Editor in Task Dock

### Step 1: Create a File Organizer Widget

Add this to a new file: `aerodynamics_app/file_organizer.py`

```python
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, 
    QTreeWidgetItem, QPushButton
)
from PySide6.QtCore import Qt
from pathlib import Path


class FileOrganizerWidget(QWidget):
    """File browser widget showing project hierarchy."""
    
    def __init__(self, root_path=None, parent=None):
        super().__init__(parent)
        self.root_path = Path(root_path or ".")
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # File tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Files")
        self.tree.setColumnCount(1)
        layout.addWidget(self.tree)
        
        # Load files
        self._populate_tree()
    
    def _populate_tree(self):
        """Recursively populate tree with files and folders."""
        self.tree.clear()
        root_item = QTreeWidgetItem(self.tree)
        root_item.setText(0, self.root_path.name)
        root_item.setData(0, Qt.UserRole, str(self.root_path))
        
        self._add_files(root_item, self.root_path)
        self.tree.expandAll()
    
    def _add_files(self, parent_item, path):
        """Recursively add files and folders to tree."""
        try:
            for item in sorted(path.iterdir()):
                # Skip hidden files and common ignored folders
                if item.name.startswith('.') or item.name in ['__pycache__', 'node_modules']:
                    continue
                
                tree_item = QTreeWidgetItem(parent_item)
                tree_item.setText(0, item.name)
                tree_item.setData(0, Qt.UserRole, str(item))
                
                # Add folder icon indicator
                if item.is_dir():
                    tree_item.setText(0, f"📁 {item.name}")
                    self._add_files(tree_item, item)
                else:
                    # Get file extension icon
                    ext = item.suffix.lower()
                    icons = {
                        '.py': '🐍',
                        '.txt': '📄',
                        '.json': '⚙️',
                        '.ui': '🎨',
                        '.stl': '🔲',
                        '.foam': '💨',
                    }
                    icon = icons.get(ext, '📃')
                    tree_item.setText(0, f"{icon} {item.name}")
        except Exception as e:
            print(f"Error loading files: {e}")
    
    def get_selected_file(self):
        """Get the currently selected file path."""
        item = self.tree.currentItem()
        if item:
            return Path(item.data(0, Qt.UserRole))
        return None
    
    def on_file_selected(self, callback):
        """Connect file selection signal."""
        self.tree.itemSelectionChanged.connect(
            lambda: callback(self.get_selected_file())
        )
```

### Step 2: Create a Code Editor Widget

Add this to: `aerodynamics_app/code_editor.py`

```python
from PySide6.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QFont, QSyntaxHighlighter, QTextDocument
from PySide6.QtCore import Qt


class CodeEditorWidget(QPlainTextEdit):
    """Code editor with syntax highlighting."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        # Use monospace font
        font = QFont("Consolas")  # or "Monaco", "Courier New"
        font.setPointSize(10)
        self.setFont(font)
        
        # Enable line numbers (optional)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        
        # Syntax highlighting (basic)
        self._apply_dark_theme()
    
    def _apply_dark_theme(self):
        """Apply dark theme to editor."""
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1f22;
                color: #e6e6e6;
                border: 1px solid #3a3d44;
                padding: 4px;
                margin: 0px;
            }
        """)
    
    def load_file(self, file_path):
        """Load a file into the editor."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.setPlainText(content)
            self.document().setModified(False)
        except Exception as e:
            self.setPlainText(f"Error loading file: {e}")
    
    def save_file(self, file_path):
        """Save editor content to file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.toPlainText())
            self.document().setModified(False)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def is_modified(self):
        """Check if document has unsaved changes."""
        return self.document().isModified()


class CodeEditorContainerWidget(QWidget):
    """Container for code editor with controls."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # File info label
        self.file_label = QLabel("No file open")
        self.file_label.setStyleSheet("color: #888; padding: 4px;")
        layout.addWidget(self.file_label)
        
        # Code editor
        self.editor = CodeEditorWidget()
        layout.addWidget(self.editor)
    
    def load_file(self, file_path):
        """Load a file and update label."""
        if file_path:
            self.file_label.setText(f"📝 {file_path.name}")
            self.editor.load_file(file_path)
    
    def set_file_label(self, text):
        """Set the file info label."""
        self.file_label.setText(text)
```

### Step 3: Integrate into Main Window

Edit `aerodynamics_app/main.py`:

```python
# At the top with other imports:
from aerodynamics_app.file_organizer import FileOrganizerWidget
from aerodynamics_app.code_editor import CodeEditorContainerWidget

# In the AeroWindow class, add new method:
def _replace_tree_dock_with_file_organizer(self):
    """Replace tree dock with file organizer."""
    tree_dock = getattr(self.ui, "tree", None)
    if tree_dock is None:
        return
    
    # Create file organizer
    self.file_organizer = FileOrganizerWidget(Path.cwd())
    tree_dock.setWidget(self.file_organizer)
    tree_dock.setWindowTitle("File Organizer")
    
    # Connect file selection to code editor
    self.file_organizer.on_file_selected(self._on_file_selected)

def _replace_task_dock_with_code_editor(self):
    """Replace task dock with code editor."""
    task_dock = getattr(self.ui, "task", None)
    if task_dock is None:
        return
    
    # Create code editor
    self.code_editor = CodeEditorContainerWidget()
    task_dock.setWidget(self.code_editor)
    task_dock.setWindowTitle("Code Editor")

def _on_file_selected(self, file_path):
    """Handle file selection from organizer."""
    if file_path and file_path.is_file():
        # Auto-load into code editor if it's a text file
        if file_path.suffix in ['.py', '.txt', '.json', '.cfg', '.yaml', '.yml']:
            self.code_editor.load_file(file_path)

# In __init__, after ribbon setup, add:
self._replace_tree_dock_with_file_organizer()
self._replace_task_dock_with_code_editor()
```

---

## Option 2: Keep Panels But Add Code Editor Tab

If you want to keep the aerodynamics panels but add a code editor:

```python
# In _init_ribbon_controller or similar place:
def _add_code_editor_to_task_dock(self):
    """Add code editor as another tab in task dock."""
    from PySide6.QtWidgets import QTabWidget
    
    task_dock = getattr(self.ui, "task", None)
    if task_dock is None:
        return
    
    # Create tab widget if not existing
    if not isinstance(task_dock.widget(), QTabWidget):
        current_widget = task_dock.takeWidget()
        tab_widget = QTabWidget()
        tab_widget.addTab(current_widget, "Panels")
        task_dock.setWidget(tab_widget)
    else:
        tab_widget = task_dock.widget()
    
    # Add code editor tab
    self.code_editor = CodeEditorContainerWidget()
    tab_widget.addTab(self.code_editor, "Code Editor")
```

---

## Option 3: Custom Properties Panel + File Browser

Replace properties/tree with a split view:

```python
from PySide6.QtWidgets import QSplitter, Qt

def _replace_docks_with_split_view(self):
    """Create split view: file organizer on left, code editor on bottom."""
    splitter = QSplitter(Qt.Vertical)
    
    # Top: File organizer
    self.file_organizer = FileOrganizerWidget()
    splitter.addWidget(self.file_organizer)
    
    # Bottom: Code editor
    self.code_editor = CodeEditorContainerWidget()
    splitter.addWidget(self.code_editor)
    
    # Set size proportions
    splitter.setSizes([300, 400])
    
    # Replace tree dock widget
    tree_dock = getattr(self.ui, "tree", None)
    if tree_dock:
        tree_dock.setWidget(splitter)
        tree_dock.setWindowTitle("Project Browser")
```

---

## Quick Start Checklist

1. **Create the widget files:**
   - `aerodynamics_app/file_organizer.py`
   - `aerodynamics_app/code_editor.py`

2. **Import in main.py:**
   ```python
   from aerodynamics_app.file_organizer import FileOrganizerWidget
   from aerodynamics_app.code_editor import CodeEditorContainerWidget
   from pathlib import Path
   ```

3. **Add method to AeroWindow:**
   ```python
   def _replace_tree_dock_with_file_organizer(self):
       # ... from Option 1 above
   
   def _replace_task_dock_with_code_editor(self):
       # ... from Option 1 above
   ```

4. **Call in __init__:**
   ```python
   self._replace_tree_dock_with_file_organizer()
   self._replace_task_dock_with_code_editor()
   ```

---

## Customization Ideas

- **File icons:** Use emojis or `QFileIconProvider`
- **Syntax highlighting:** Use `QSyntaxHighlighter` + language rules
- **File filters:** Only show `.py`, `.json`, etc.
- **Search/filter:** Add search bar above file tree
- **Recent files:** Add favorites or recent files list
- **Line numbers:** Add `QTextEdit.LineNumberArea`
- **Auto-complete:** Use `QCompleter` for code completion

---

## Before/After Comparison

| Feature | Current | With Module |
|---------|---------|-------------|
| Left panel | Model tree | File organizer |
| Right panel | Aerodynamics panels | Code editor |
| Customizable | Limited | Full control |
| File editing | No | Yes |
| Code display | No | Yes |

