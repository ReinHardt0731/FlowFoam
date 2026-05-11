# Ribbon GUI Customization Guide

## Quick Start

The minimize button is created in `aerodynamics_app/ribbon_controller.py` in the `_create_minimize_button()` method. You can customize it by editing that method.

---

## Customize the Minimize Button

### 1. **Change Button Size**

```python
# Make button bigger
self.minimize_button.setMaximumWidth(48)      # width in pixels
self.minimize_button.setMaximumHeight(32)     # height in pixels

# Or use fixed size
self.minimize_button.setFixedSize(48, 32)
```

### 2. **Use an Icon Instead of Text**

```python
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize

# Load icon from file
icon = QIcon("path/to/your/icon.png")
self.minimize_button.setIcon(icon)
self.minimize_button.setIconSize(QSize(20, 20))

# Remove the text
self.minimize_button.setText("")
```

### 3. **Change Text Labels**

```python
# Current: uses "−" and "+"
# You can use any Unicode characters or emoji:

self.minimize_button.setText("▼")  # Chevron down
self.minimize_button.setText("▲")  # Chevron up
self.minimize_button.setText("◀")  # Left arrow
self.minimize_button.setText("▶")  # Right arrow
self.minimize_button.setText("↕")  # Up-down arrow
self.minimize_button.setText("≡")  # Hamburger menu
```

Update the `_update_minimize_button()` method to change the text for expanded state:

```python
def _update_minimize_button(self):
    if hasattr(self, 'minimize_button') and self.minimize_button is not None:
        if self.ribbon_minimized:
            self.minimize_button.setText("▲")  # Show up arrow when minimized
        else:
            self.minimize_button.setText("▼")  # Show down arrow when expanded
```

### 4. **Style the Button with CSS (Dark Mode Example)**

```python
self.minimize_button.setStyleSheet("""
    QPushButton {
        background-color: #31353d;
        color: #f0f0f0;
        border: 1px solid #4a4f59;
        border-radius: 3px;
        padding: 2px;
        font-weight: bold;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: #3a404b;
        border: 1px solid #5a6070;
    }
    QPushButton:pressed {
        background-color: #2b2f36;
        border: 1px solid #4a4f59;
    }
    QPushButton:focus {
        outline: none;
    }
""")
```

### 5. **Make Button Flat (No Border)**

```python
self.minimize_button.setFlat(True)  # Removes the button border
```

### 6. **Remove Focus Outline**

```python
self.minimize_button.setFocusPolicy(Qt.NoFocus)
```

### 7. **Change Font**

```python
from PySide6.QtGui import QFont

font = QFont()
font.setPointSize(10)
font.setBold(True)
self.minimize_button.setFont(font)
```

---

## Advanced: Create Multiple Ribbon Buttons

You can add more buttons next to the minimize button:

```python
def _create_minimize_button(self):
    """Create buttons in ribbon tab bar corner."""
    if self.ribbon_tabs is None or self.ribbon_tabs.tabBar() is None:
        return

    # Create a container widget to hold multiple buttons
    from PySide6.QtWidgets import QWidget, QHBoxLayout
    button_container = QWidget()
    layout = QHBoxLayout(button_container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(2)

    # Minimize/Expand button
    self.minimize_button = QPushButton("−")
    self.minimize_button.setMaximumSize(32, 24)
    self.minimize_button.clicked.connect(self.toggle_minimized_state)
    layout.addWidget(self.minimize_button)

    # Add more buttons as needed
    help_button = QPushButton("?")
    help_button.setMaximumSize(32, 24)
    help_button.setToolTip("Show ribbon help")
    # help_button.clicked.connect(some_function)
    layout.addWidget(help_button)

    # Add container to tab bar
    self.ribbon_tabs.setCornerWidget(button_container, Qt.TopRightCorner)
```

---

## Customize Ribbon Height

Edit the height measurements in `ribbon_controller.py`:

```python
def measure_heights(self):
    """Measure and cache the expanded and tab-strip-only heights."""
    if self.expanded_height is None:
        self.ribbon_frame.layout().update()
        self.expanded_height = self.ribbon_frame.sizeHint().height() + 6
        if self.expanded_height < 120:
            self.expanded_height = 120  # CHANGE THIS: minimum expanded height

    if self.tab_strip_height is None:
        tab_bar_height = self.ribbon_tabs.tabBar().sizeHint().height()
        self.tab_strip_height = tab_bar_height + 4  # CHANGE THIS: minimized ribbon height
```

---

## Customize Tab Bar Styling

Edit `aerodynamics_app/main.py` in the `_compact_ribbon_shell()` method to change tab appearance:

```python
def _compact_ribbon_shell(self, ribbon_frame):
    """Customize ribbon styling here."""
    ribbon_frame.setStyleSheet("""
        QTabBar::tab {
            padding: 3px 8px;               /* CHANGE: tab padding */
            min-height: 16px;               /* CHANGE: tab height */
            background-color: #2a2d33;      /* CHANGE: tab background */
            color: #dfe3ea;                 /* CHANGE: tab text color */
            border: 1px solid #43474f;      /* CHANGE: tab border */
        }
        QTabBar::tab:selected {
            background-color: #3a414d;      /* CHANGE: selected tab color */
            color: #ffffff;                 /* CHANGE: selected text color */
        }
        QTabBar::tab:hover {
            background-color: #353c47;      /* CHANGE: hover color */
        }
    """)
```

---

## PySide6 Widget Methods Reference

### Button Methods
- `setText(text)` - Set button text
- `setIcon(icon)` - Set button icon
- `setIconSize(QSize)` - Set icon size
- `setMaximumWidth(w)` - Max width
- `setMaximumHeight(h)` - Max height
- `setMinimumWidth(w)` / `setMinimumHeight(h)` - Min dimensions
- `setFixedSize(w, h)` - Fixed size
- `setFlat(bool)` - Remove button border
- `setStyleSheet(str)` - Apply CSS styling
- `setToolTip(str)` - Hover text
- `setFocusPolicy(policy)` - Focus behavior
- `setEnabled(bool)` - Enable/disable

### Common Icon Paths
```python
# Look for existing icons in your project
icon_path = "path/to/icon.png"
icon = QIcon(icon_path)
button.setIcon(icon)
```

### Unicode Symbols for Buttons
- `"−"` (minus) / `"+"` (plus)
- `"▼"` (down chevron) / `"▲"` (up chevron)
- `"◀"` (left) / `"▶"` (right)
- `"☰"` (hamburger) / `"≡"` (horizontal lines)
- `"⊖"` (circled minus) / `"⊕"` (circled plus)
- `"↕"` (up-down arrow)

---

## Example: Modern Minimize Button

```python
def _create_minimize_button(self):
    if self.ribbon_tabs is None or self.ribbon_tabs.tabBar() is None:
        return

    self.minimize_button = QPushButton()
    self.minimize_button.setFixedSize(36, 28)
    self.minimize_button.setFlat(True)
    self.minimize_button.setText("▼")
    self.minimize_button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: #e6e6e6;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            font-weight: bold;
            padding: 2px;
        }
        QPushButton:hover {
            background-color: #3a404b;
        }
        QPushButton:pressed {
            background-color: #2b2f36;
        }
    """)
    self.minimize_button.setFocusPolicy(Qt.NoFocus)
    self.minimize_button.setToolTip("Collapse/expand ribbon")
    self.minimize_button.clicked.connect(self.toggle_minimized_state)
    
    self.ribbon_tabs.setCornerWidget(self.minimize_button, Qt.TopRightCorner)
```

---

## Troubleshooting

**Button not showing?**
- Check if `self.ribbon_tabs` is not None
- Check if tab bar exists: `self.ribbon_tabs.tabBar()`

**Styling not working?**
- Make sure stylesheet string is complete (no unmatched braces)
- Check color hex codes are valid
- Use `print()` to debug

**Icon not loading?**
- Verify file path exists
- Use absolute paths or check working directory
- Make sure image format is supported (PNG, JPG, SVG, etc.)

