"""Code editor widget with syntax highlighting and file management."""

from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QLineEdit, QMessageBox
)
from PySide6.QtGui import QFont, QSyntaxHighlighter, QTextDocument, QColor, QTextCharFormat
from PySide6.QtCore import Qt, Signal, QSize, QRegularExpression


class SimpleSyntaxHighlighter(QSyntaxHighlighter):
    """Basic syntax highlighter for Python, JSON, YAML."""
    
    def __init__(self, document, language='python'):
        super().__init__(document)
        self.language = language
        self._setup_formats()
    
    def _setup_formats(self):
        """Setup text formats for highlighting."""
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#569cd6"))  # Blue
        self.keyword_format.setFontWeight(700)
        
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#ce9178"))  # Orange
        
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#6a9955"))  # Green
        
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("#b5cea8"))  # Light green
        
        self.operator_format = QTextCharFormat()
        self.operator_format.setForeground(QColor("#d4d4d4"))  # Light gray
    
    def highlightBlock(self, text):
        """Syntax highlight a block of code."""
        if self.language == 'python':
            self._highlight_python(text)
        elif self.language in ('json', 'yaml'):
            self._highlight_json_yaml(text)
    
    def _highlight_python(self, text):
        """Highlight Python code."""
        # Keywords
        keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'return', 'import', 'from']
        for keyword in keywords:
            pattern = QRegularExpression(r'\b' + keyword + r'\b')
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword_format)
        
        # Strings
        string_pattern = QRegularExpression(r'"[^"]*"|\'[^\']*\'')
        iterator = string_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)
        
        # Comments
        comment_pattern = QRegularExpression(r'#.*')
        iterator = comment_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.comment_format)
    
    def _highlight_json_yaml(self, text):
        """Highlight JSON/YAML code."""
        # Strings (keys and values)
        string_pattern = QRegularExpression(r'"[^"]*"')
        iterator = string_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)
        
        # Comments (YAML)
        comment_pattern = QRegularExpression(r'#.*')
        iterator = comment_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.comment_format)
        
        # Numbers
        number_pattern = QRegularExpression(r'\b\d+\.?\d*\b')
        iterator = number_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.number_format)


class CodeEditorWidget(QPlainTextEdit):
    """Code editor with syntax highlighting."""
    
    content_changed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None
        self.current_language = 'python'
        self.highlighter = None
        self.auto_save_enabled = True
        self._init_ui()
    
    def _init_ui(self):
        """Setup the UI."""
        # Use monospace font
        font = QFont("Consolas")
        if not font.fixedPitch():
            font = QFont("Courier New")
        font.setPointSize(10)
        self.setFont(font)
        
        # Dark theme
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1f22;
                color: #e6e6e6;
                border: none;
                padding: 4px;
                margin: 0px;
            }
        """)
        
        # Tab width
        self.setTabStopDistance(40)
        
        # Connect signals
        self.textChanged.connect(self.content_changed.emit)
    
    def load_file(self, file_path: Path) -> bool:
        """Load a file into the editor. Returns True if successful, False otherwise."""
        import os
        
        MAX_FILE_SIZE = 500 * 1024  # 500 KB limit
        
        try:
            # Check file size first
            file_size = os.path.getsize(file_path)
            
            if file_size > MAX_FILE_SIZE:
                raise ValueError(f"File is too large ({file_size / 1024 / 1024:.1f} MB). Maximum supported size is {MAX_FILE_SIZE / 1024 / 1024:.1f} MB.")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.file_path = file_path
            self.setPlainText(content)
            self.document().setModified(False)
            
            # Detect language
            ext = file_path.suffix.lower()
            if ext == '.py':
                self.current_language = 'python'
            elif ext in {'.json', '.yaml', '.yml'}:
                self.current_language = 'json' if ext == '.json' else 'yaml'
            
            # Apply syntax highlighting
            self._apply_highlighting()
            return True
        except ValueError:
            # Re-raise ValueError (expected errors)
            raise
        except UnicodeDecodeError:
            raise ValueError(f"File is not human-readable (binary data). Cannot open {file_path.name}")
        except Exception as e:
            raise ValueError(f"Error loading file: {e}")
    
    def _apply_highlighting(self):
        """Apply syntax highlighting to the document."""
        if self.highlighter:
            self.highlighter.setDocument(None)
        
        self.highlighter = SimpleSyntaxHighlighter(self.document(), self.current_language)
    
    def save_file(self, file_path: Path = None) -> bool:
        """Save editor content to file."""
        target_path = file_path or self.file_path
        if not target_path:
            return False
        
        try:
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(self.toPlainText())
            
            self.file_path = target_path
            self.document().setModified(False)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def is_modified(self) -> bool:
        """Check if document has unsaved changes."""
        return self.document().isModified()
    
    def get_file_name(self) -> str:
        """Get current file name."""
        if self.file_path:
            return self.file_path.name
        return "Untitled"


class CodeEditorTabWidget(QWidget):
    """Tab widget for managing multiple open code files."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editors = {}  # Map file_path -> CodeEditorWidget
        self._init_ui()
    
    def _init_ui(self):
        """Setup the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Status bar
        status_layout = QHBoxLayout()
        self.status_label = QLabel("No file open")
        self.status_label.setStyleSheet("color: #888; padding: 4px 8px; background-color: #232428;")
        status_layout.addWidget(self.status_label)
        
        # Save button
        save_btn = QPushButton("Save")
        save_btn.setMaximumWidth(60)
        save_btn.clicked.connect(self.save_current_file)
        status_layout.addWidget(save_btn)
        
        # Find button
        find_btn = QPushButton("Find...")
        find_btn.setMaximumWidth(60)
        find_btn.setToolTip("Ctrl+F")
        find_btn.clicked.connect(self.show_find_dialog)
        status_layout.addWidget(find_btn)
        
        layout.addLayout(status_layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self._on_tab_close)
        self.tabs.currentChanged.connect(self._on_tab_changed)
        layout.addWidget(self.tabs)
    
    def add_file_tab(self, file_path: Path) -> bool:
        """Add or switch to a file tab. Returns True if successful, False otherwise."""
        try:
            # Check if already open
            if file_path in self.editors:
                self.tabs.setCurrentWidget(self.editors[file_path])
                return True
            
            # Create new editor
            editor = CodeEditorWidget(self)
            try:
                editor.load_file(file_path)
            except ValueError as e:
                # Show error dialog and don't add the tab
                QMessageBox.warning(self, "Cannot Open File", str(e))
                return False
            
            # Add to tab
            tab_name = file_path.name
            self.tabs.addTab(editor, tab_name)
            self.editors[file_path] = editor
            
            # Switch to new tab
            self.tabs.setCurrentWidget(editor)
            
            # Update status
            self._update_status()
            return True
        except Exception as e:
            try:
                QMessageBox.warning(self, "Unexpected Error", f"An unexpected error occurred:\n{str(e)}")
            except:
                print(f"Error: {e}")
            return False
    
    def save_current_file(self) -> bool:
        """Save the current editor's file."""
        editor = self.tabs.currentWidget()
        if isinstance(editor, CodeEditorWidget) and editor.file_path:
            return editor.save_file()
        return False
    
    def save_all_files(self) -> bool:
        """Save all open files."""
        all_saved = True
        for editor in self.editors.values():
            if editor.is_modified():
                if not editor.save_file():
                    all_saved = False
        return all_saved
    
    def _on_tab_changed(self, index):
        """Handle tab change."""
        self._update_status()
    
    def _on_tab_close(self, index):
        """Handle tab close."""
        editor = self.tabs.widget(index)
        if isinstance(editor, CodeEditorWidget):
            # Check for unsaved changes
            if editor.is_modified():
                result = QMessageBox.question(
                    self, "Unsaved Changes",
                    f"Save changes to {editor.get_file_name()}?",
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                )
                if result == QMessageBox.Cancel:
                    return
                elif result == QMessageBox.Save:
                    editor.save_file()
            
            # Remove tab
            self.tabs.removeTab(index)
            if editor.file_path in self.editors:
                del self.editors[editor.file_path]
    
    def _update_status(self):
        """Update status bar."""
        editor = self.tabs.currentWidget()
        if isinstance(editor, CodeEditorWidget):
            file_name = editor.get_file_name()
            modified = " *" if editor.is_modified() else ""
            self.status_label.setText(f"📝 {file_name}{modified}")
        else:
            self.status_label.setText("No editor")
    
    def show_find_dialog(self):
        """Show find and replace dialog."""
        editor = self.tabs.currentWidget()
        if isinstance(editor, CodeEditorWidget):
            # Simple implementation: select all matching text
            cursor = editor.textCursor()
            cursor.movePosition(cursor.Start)
            editor.setTextCursor(cursor)
            editor.find("TODO")  # Placeholder for full find/replace
    
    def on_window_focus_changed(self, has_focus: bool):
        """Handle window focus change (for auto-save)."""
        if not has_focus:
            self.save_all_files()
