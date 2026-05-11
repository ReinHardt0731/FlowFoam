# Implementation Plan: File Organizer + Code Editor

## Phase Overview

Transform the UI from:
- **Left panel** (Tree Dock): Model tree → File organizer
- **Right panel** (Task Dock): Aerodynamics panels (Geometry, Mesh, etc.) → Code editor with History/Input editing

---

## Phase 1: Analysis & Planning (Current State)

### Current Architecture

```
aerodynamics_app/main.py
├── AeroWindow (QMainWindow)
│   ├── _init_tree_view()
│   │   └── self.ui.treeView (QTreeView) → Model from aerodynamics_tab.get_model()
│   ├── _init_ribbon_dock()
│   │   └── ribbon_dock (QDockWidget)
│   ├── tree_dock (QDockWidget) ← TARGET: Replace with FileOrganizerWidget
│   ├── task_dock (QDockWidget) ← TARGET: Replace with CodeEditorWidget
│   └── cfd_console_dock (QDockWidget) (Keep unchanged)
│
aerodynamics/controller_legacy.py
├── AerodynamicsTab
│   ├── get_model() → Returns aerodynamics data tree model
│   ├── show_panel(key) → Shows different panels (Geometry, Mesh, etc.)
│   └── on_tree_selection_changed()
```

### Current Tree Dock Contents
- **Object**: `self.ui.tree` (QDockWidget)
- **Widget**: `self.ui.treeView` (QTreeView)
- **Data Source**: `aerodynamics_tab.get_model()` (hierarchical CFD parameters)
- **Function**: Shows/selects aerodynamic configuration options

### Current Task Dock Contents
- **Object**: `self.ui.task` (QDockWidget)
- **Panels**: Geometry, Mesh, SnappyHexMesh, CheckMesh, BoundaryConditions, Simulation, Numerics, PostProcess, Export
- **Widget**: Built dynamically by `aerodynamics_tab`
- **Function**: Displays input forms for selected tree item

---

## Phase 2: Design & Architecture

### Target Layout

```
┌─────────────────────────────────────────────┐
│              Ribbon (Toggle −/+)            │
├──────────────────┬──────────────────────────┤
│                  │                          │
│  File Organizer  │                          │
│  ├── 📁 Folder A │      3D Viewer           │
│  │   ├── 📄 file │      (Unchanged)         │
│  │   └── 📄 file │                          │
│  ├── 📁 Folder B │                          │
│  │   └── 📄 file │                          │
│  ├── 📄 config   │                          │
│  └── 📄 README   │                          │
│                  │                          │
│ [Save] [Reload]  │                          │
├──────────────────────────────────────────────┤
│         Code Editor (Tab: History/Input)     │
│                                              │
│ 📝 config.json                               │
│ ┌──────────────────────────────────────────┐│
│ │{                                         ││
│ │  "workflow": "simpleFoam",               ││
│ │  "geometry": {...}                       ││
│ │}                                         ││
│ └──────────────────────────────────────────┘│
│ [Modified: Yes] [Save] [Reload] [Find...]   │
├──────────────────────────────────────────────┤
│  CFD Console (Unchanged)                     │
└──────────────────────────────────────────────┘
```

### New Component Structure

```
aerodynamics_app/
├── main.py                    (Modified - integrate new widgets)
├── file_organizer.py          (New - FileOrganizerWidget)
├── code_editor.py             (New - CodeEditorWidget)
├── history_manager.py         (New - Track file edits)
└── ribbon_controller.py        (Unchanged)
```

---

## Phase 3: Implementation Steps

### Step 1: Create File Organizer Widget (Week 1, Day 1)

**File**: `aerodynamics_app/file_organizer.py`

**Features**:
- [ ] Tree view of project files
- [ ] Icon support (folders, file types)
- [ ] Filter by extension (*.py, *.json, *.cfg, *.yaml)
- [ ] Context menu (open, delete, rename)
- [ ] Refresh button
- [ ] Selection signal (file_selected)

**Code structure**:
```python
class FileOrganizerWidget(QWidget):
    file_selected = Signal(Path)
    file_double_clicked = Signal(Path)
    
    def __init__(self, root_path: Path):
        # Setup UI
        # Load files
        # Connect signals
    
    def _populate_tree(self, path: Path, parent_item: QTreeWidgetItem):
        # Recursively add files/folders
    
    def _get_file_icon(self, path: Path) -> str:
        # Return emoji based on file type
    
    def on_file_selected(self, callback):
        self.file_selected.connect(callback)
```

**Success Criteria**:
- [ ] Can browse all project files
- [ ] Shows folder/file icons
- [ ] Emits signals when files are selected
- [ ] Single file can be opened without errors

---

### Step 2: Create Code Editor Widget (Week 1, Day 2)

**File**: `aerodynamics_app/code_editor.py`

**Features**:
- [ ] QPlainTextEdit-based editor
- [ ] Syntax highlighting (Python, JSON)
- [ ] Line numbers
- [ ] Dark mode styling
- [ ] Load/save files
- [ ] Modified state tracking
- [ ] Find/Replace (Ctrl+H)
- [ ] Tab support (open multiple files)

**Code structure**:
```python
class CodeEditorWidget(QPlainTextEdit):
    file_changed = Signal()
    
    def load_file(self, path: Path):
        # Read file, detect syntax, highlight
    
    def save_file(self, path: Path) -> bool:
        # Write file, update status
    
    def apply_syntax_highlighting(self, lang: str):
        # Python, JSON, YAML, etc.
    
    def is_modified(self) -> bool:
        # Check for unsaved changes


class CodeEditorTabWidget(QWidget):
    # Tab bar with multiple files
    # each tab has CodeEditorWidget
    
    def add_file_tab(self, path: Path):
        # Create editor, load file, add tab
    
    def on_tab_changed(self, index: int):
        # Update current editor displays
    
    def save_all(self):
        # Save all open tabs
```

**Success Criteria**:
- [ ] Can open and display file content
- [ ] Dark mode matches current theme
- [ ] Save/load works without data loss
- [ ] Modified indicator shows properly
- [ ] Can handle large files (>1MB)

---

### Step 3: Create History Manager (Week 1, Day 3)

**File**: `aerodynamics_app/history_manager.py`

**Features**:
- [ ] Track file changes (timestamps)
- [ ] Store edit history
- [ ] Undo/Redo support
- [ ] Revert to previous state
- [ ] Auto-save functionality

**Code structure**:
```python
class HistoryManager:
    def __init__(self, code_editor: CodeEditorWidget):
        self.editor = code_editor
        self.history = []
        self.current_index = -1
    
    def record_change(self, text: str, path: Path):
        # Add snapshot to history
    
    def undo(self):
        # Restore previous version
    
    def redo(self):
        # Restore next version
    
    def get_history_list(self) -> List[HistoryRecord]:
        # Return all changes for this file
```

**Success Criteria**:
- [ ] Can undo 10+ changes
- [ ] History persists across session
- [ ] Can revert to any previous state
- [ ] No data corruption on undo/redo

---

### Step 4: Integrate into Main Window (Week 1, Day 4)

**File**: `aerodynamics_app/main.py` (modifications)

**Changes**:
- [ ] Import new widgets
- [ ] Disable `_init_tree_view()` (old model tree)
- [ ] Add `_setup_file_organizer()` method
- [ ] Add `_setup_code_editor()` method
- [ ] Connect file organizer signals to code editor
- [ ] Update preferences to include editor state
- [ ] Preserve existing ribbon, viewer, console
- [ ] Move aerodynamics panels to separate location (or save to menu)

**Integration code**:
```python
class AeroWindow(QMainWindow):
    def __init__(self):
        # ... existing init code ...
        
        # Replace tree dock
        self._setup_file_organizer()  # NEW
        
        # Replace task dock
        self._setup_code_editor()     # NEW
        
        # Keep everything else
        self._init_ribbon()
        self._init_view_actions()
    
    def _setup_file_organizer(self):
        """Replace tree dock with file organizer."""
        tree_dock = getattr(self.ui, "tree", None)
        if tree_dock is None:
            return
        
        self.file_organizer = FileOrganizerWidget(ROOT)
        tree_dock.setWidget(self.file_organizer)
        tree_dock.setWindowTitle("Project Files")
        
        # Connect signals
        self.file_organizer.file_selected.connect(self._on_file_selected)
    
    def _setup_code_editor(self):
        """Replace task dock with code editor."""
        task_dock = getattr(self.ui, "task", None)
        if task_dock is None:
            return
        
        self.code_editor_widget = CodeEditorTabWidget()
        task_dock.setWidget(self.code_editor_widget)
        task_dock.setWindowTitle("Code Editor")
    
    def _on_file_selected(self, file_path: Path):
        """Handle file selection from organizer."""
        if file_path.suffix in ['.py', '.json', '.yaml', '.txt', '.cfg']:
            self.code_editor_widget.add_file_tab(file_path)
```

**Success Criteria**:
- [ ] App starts without errors
- [ ] File organizer shows in left panel
- [ ] Code editor shows in right panel
- [ ] Can select files and see content
- [ ] Preferences are preserved

---

### Step 5: Move Aerodynamics Panels (Week 2, Day 1)

**Options** (choose one):

**Option A: Menu Bar Addon**
- [ ] Add "Tools → Aerodynamics Panels" menu
- [ ] Opens aerodynamics panels in new dialog/dock

**Option B: Tab in Code Editor**
- [ ] Add "Panels" tab next to "History"
- [ ] Keep aerodynamics functionality

**Option C: Toggle Button in Ribbon**
- [ ] Add "Show Panels" button to ribbon
- [ ] Opens aerodynamics panel as temporary overlay

**Recommendation**: Option B (least disruptive)

**Code**:
```python
def _setup_code_editor(self):
    self.code_editor_widget = CodeEditorTabWidget()
    
    # Add aerodynamics panels as a tab
    self.aerodynamics_panels = AerodynamicsPanelsWidget(self.aerodynamics_tab)
    self.code_editor_widget.add_tab(self.aerodynamics_panels, "Panels")
```

**Success Criteria**:
- [ ] Aerodynamics panels still accessible
- [ ] All panel functions work as before
- [ ] No data loss during transition

---

### Step 6: Testing & Refinement (Week 2, Day 2-3)

**Manual Testing**:
- [ ] Browse files in organizer
- [ ] Open different file types
- [ ] Edit file content
- [ ] Save changes
- [ ] Reload files
- [ ] Test history/undo
- [ ] Check dark mode styling
- [ ] Verify ribbon still works
- [ ] Verify viewer still works
- [ ] Verify console still works
- [ ] Verify ribbon persistence settings
- [ ] Test with large files

**Bug Fixes**:
- [ ] Address any file loading errors
- [ ] Fix styling issues
- [ ] Optimize for performance
- [ ] Ensure proper cleanup on close

**Success Criteria**:
- [ ] All manual tests pass
- [ ] No crashes on edge cases
- [ ] Dark mode consistent
- [ ] Performance acceptable (<100ms load)

---

### Step 7: Documentation & Deployment (Week 2, Day 4)

- [ ] Document new features
- [ ] Update RIBBON_CUSTOMIZATION_GUIDE.md
- [ ] Add CODE_EDITOR_GUIDE.md
- [ ] Create user tutorial
- [ ] Commit to git with message

---

## Phase 4: Fallback Plan

If issues arise, maintain backward compatibility:

```python
# In main.py, keep a toggle:
USE_FILE_ORGANIZER = True  # Set to False to use old tree view

if USE_FILE_ORGANIZER:
    self._setup_file_organizer()
else:
    self._init_tree_view()  # Old behavior
```

---

## Phase 5: Timeline & Estimates

| Phase | Task | Est. Time | Owner |
|-------|------|-----------|-------|
| 1 | Analysis | 2 hours | You |
| 2 | FileOrganizerWidget | 4 hours | You |
| 3 | CodeEditorWidget | 6 hours | You |
| 4 | HistoryManager | 3 hours | You |
| 5 | Integration | 4 hours | You |
| 6 | Move Aerodynamics Panels | 2 hours | You |
| 7 | Testing & Fixes | 6 hours | You |
| 8 | Documentation | 2 hours | You |
| **Total** | | **29 hours** | |

**Suggested Schedule**:
- Week 1: Core widgets (File organizer + Code editor)
- Week 2: Integration + Testing + Deployment

---

## Phase 6: Success Metrics

- [ ] File organizer fully functional
- [ ] Code editor can open/edit/save files
- [ ] No crashes or data loss
- [ ] Performance < 200ms for typical operations
- [ ] Dark mode styling consistent
- [ ] All existing features still work
- [ ] User can toggle back to old layout (optional)
- [ ] Documentation complete

---

## Code Files to Create

```
1. aerodynamics_app/file_organizer.py
   - FileOrganizerWidget class
   - ~250 lines

2. aerodynamics_app/code_editor.py
   - CodeEditorWidget class
   - CodeEditorTabWidget class
   - SyntaxHighlighter helper
   - ~400 lines

3. aerodynamics_app/history_manager.py
   - HistoryManager class
   - HistoryRecord data class
   - ~150 lines

4. aerodynamics_app/main.py (modifications)
   - New methods: _setup_file_organizer(), _setup_code_editor()
   - Signal connections
   - ~50 lines added
```

---

## Files to Modify

```
1. aerodynamics_app/main.py
   - Add imports
   - Add setup methods
   - Modify __init__
   - Add signal handlers

2. RIBBON_CUSTOMIZATION_GUIDE.md (optional)
   - Add notes about new layout
```

---

## Rollback Procedure

If needed to revert:

```bash
git revert HEAD~7  # Revert last 7 commits
# OR reset to old version:
git checkout <commit-hash> -- aerodynamics_app/main.py
```

---

## Questions Before Starting

1. **Keep aerodynamics panels?** Where should they go?
   - A: Yes, in code editor tab / B: No, remove / C: In ribbon
   
2. **File organizer root path?**
   - Current: `F:\ResearchFiles\Openfoam`
   - Alternative: `openfoam_case/` folder only?
   
3. **Syntax highlighting importance?**
   - Basic (Python, JSON, YAML) / Advanced (full LSP support)
   
4. **Auto-save feature?**
   - Yes / No / On-focus-lost only?
   
5. **Keep old tree view accessible?**
   - Toggle button in ribbon / Settings option / Remove completely

