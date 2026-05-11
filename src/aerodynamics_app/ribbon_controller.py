"""Ribbon controller for Word-style collapsible ribbon behavior."""

from PySide6.QtCore import Qt, QEvent, QRect, QTimer, QObject
from PySide6.QtWidgets import QWidget, QApplication, QDockWidget, QTabBar, QPushButton, QHBoxLayout
from PySide6.QtGui import QMouseEvent


class RibbonTabBarEventFilter(QObject):
    """
    Detects tab bar interactions for ribbon minimize/expand behaviors.
    Must inherit from QObject to be installable as event filter.
    """
    def __init__(self, ribbon_controller):
        super().__init__()
        self.ribbon_controller = ribbon_controller
        self.last_click_time = 0
        self.double_click_timer = None

    def attach_to_tab_bar(self, tab_bar):
        """Install event filter on the ribbon tab bar."""
        if tab_bar is not None:
            self.tab_bar = tab_bar
            # Store reference to original event filter
            self.original_event_filter = tab_bar.parent

    def eventFilter(self, obj, event):
        """Handle tab bar events."""
        if not isinstance(obj, QTabBar):
            return False

        if event.type() == QEvent.MouseButtonDblClick and isinstance(event, QMouseEvent):
            # Double-click on tab bar toggles minimized state
            self.ribbon_controller.toggle_minimized_state()
            event.accept()
            return True
        elif event.type() == QEvent.MouseButtonPress and isinstance(event, QMouseEvent):
            # Single-click while minimized opens temporary expansion
            if self.ribbon_controller.ribbon_minimized and not self.ribbon_controller.is_temp_expanded:
                self.ribbon_controller.expand_temp_ribbon()
                event.accept()
                return True
        
        return False


class RibbonClickOutsideFilter(QWidget):
    """
    Event filter that detects clicks outside the ribbon and collapses temporary expansion.
    """
    def __init__(self, ribbon_controller):
        super().__init__()
        self.ribbon_controller = ribbon_controller

    def eventFilter(self, obj, event):
        """Intercept events to detect click-outside for ribbon."""
        if event.type() == QEvent.MouseButtonPress and isinstance(event, QMouseEvent):
            # If temporary ribbon is open, check if click is outside
            if self.ribbon_controller.is_temp_expanded:
                if not self.ribbon_controller._is_click_inside_ribbon(event.globalPos()):
                    self.ribbon_controller.collapse_temp_ribbon()
                    # Don't consume the event--let it pass through
                    return False
        elif event.type() == QEvent.WindowDeactivate:
            # Collapse when main window loses focus
            if self.ribbon_controller.is_temp_expanded:
                self.ribbon_controller.collapse_temp_ribbon()
        return False


class RibbonController:
    """
    Manages Word-style ribbon behavior: expanded, minimized, and temporary-popup modes.
    
    State:
      - ribbon_minimized: Persistent boolean saved in preferences (True = minimized, False = expanded)
      - is_temp_expanded: Transient boolean only during this session (True = temp popup visible)
      - expanded_height: Full ribbon height when expanded
      - tab_strip_height: Height of just the tab bar (minimized mode)
    """

    def __init__(self, main_window, ribbon_dock, ribbon_frame, ribbon_tabs, preferences_getter, preferences_setter):
        """
        Initialize the ribbon controller.

        Args:
            main_window: The QMainWindow instance
            ribbon_dock: The QDockWidget that contains the ribbon
            ribbon_frame: The QFrame/QWidget that is the ribbon content
            ribbon_tabs: The QTabWidget for the ribbon tabs
            preferences_getter: Callable that returns current preferences dict
            preferences_setter: Callable that accepts preferences dict and saves it
        """
        self.main_window = main_window
        self.ribbon_dock = ribbon_dock
        self.ribbon_frame = ribbon_frame
        self.ribbon_tabs = ribbon_tabs
        self.preferences_getter = preferences_getter
        self.preferences_setter = preferences_setter

        # State
        self.ribbon_minimized = False  # Will be set from preferences
        self.is_temp_expanded = False

        # Precomputed heights
        self.expanded_height = None
        self.tab_strip_height = None

        # Create event filters
        self.tab_bar_filter = RibbonTabBarEventFilter(self)
        self.click_outside_filter = RibbonClickOutsideFilter(self)

        # Install tab bar event filter
        if self.ribbon_tabs is not None and self.ribbon_tabs.tabBar() is not None:
            self.ribbon_tabs.tabBar().installEventFilter(self.tab_bar_filter)

        # Install click-outside event filter on the application
        if QApplication.instance() is not None:
            QApplication.instance().installEventFilter(self.click_outside_filter)

        # Create and add minimize button
        self._create_minimize_button()

    def _create_minimize_button(self):
        """Create and add a minimize/expand button to the ribbon tab bar.
        
        CUSTOMIZATION OPTIONS:
        =====================
        
        1. BUTTON SIZE:
           - setMaximumWidth(width_in_pixels)
           - setMaximumHeight(height_in_pixels)
           - setMinimumWidth() / setMinimumHeight()
           - setFixedSize(width, height)
        
        2. ICON INSTEAD OF TEXT:
           - from PySide6.QtGui import QIcon, QPixmap
           - icon = QIcon("path/to/icon.png")
           - self.minimize_button.setIcon(icon)
           - self.minimize_button.setIconSize(QSize(16, 16))
        
        3. STYLING (QSS - Qt Style Sheets):
           - self.minimize_button.setStyleSheet("...")
           - Example: "background-color: #2a2d33; color: #e6e6e6; border: 1px solid #43474f;"
        
        4. TOOLTIPS:
           - setToolTip("text to show on hover")
        
        5. TEXT vs ICON:
           - setText() for text labels
           - setIcon() for images
           - Can use both together
        
        6. BUTTON APPEARANCE:
           - setFlat(True) - removes button border
           - setCheckable(True) - makes it toggleable
           - setFocusPolicy(Qt.NoFocus) - removes focus rectangle
        """
        if self.ribbon_tabs is None or self.ribbon_tabs.tabBar() is None:
            return

        # ========== CUSTOMIZE HERE ==========
        
        # Create the minimize button
        self.minimize_button = QPushButton()
        
        # Size customization
        self.minimize_button.setMaximumWidth(32)      # Change this: wider/narrower button
        self.minimize_button.setMaximumHeight(24)     # Change this: taller/shorter button
        self.minimize_button.setFixedSize(32, 24)     # Or use fixed size instead
        
        # Text/Icon customization - CHOOSE ONE:
        self.minimize_button.setText("−")             # Unicode minus sign (or use "+"/"-")
        # OR use an icon:
        # from PySide6.QtGui import QIcon, QPixmap
        # icon = QIcon("path/to/your/icon.png")
        # self.minimize_button.setIcon(icon)
        # self.minimize_button.setIconSize(QSize(16, 16))
        
        # Appearance customization
        self.minimize_button.setFlat(False)           # Set to True for borderless look
        self.minimize_button.setToolTip("Minimize/expand ribbon (or double-click tab)")
        self.minimize_button.setFocusPolicy(Qt.NoFocus)  # Remove focus outline
        
        # Style customization - uncomment to use dark mode style:
        # self.minimize_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #31353d;
        #         color: #f0f0f0;
        #         border: 1px solid #4a4f59;
        #         border-radius: 3px;
        #         padding: 2px;
        #         font-weight: bold;
        #     }
        #     QPushButton:hover {
        #         background-color: #3a404b;
        #     }
        #     QPushButton:pressed {
        #         background-color: #2b2f36;
        #     }
        # """)
        
        # Connect to toggle function
        self.minimize_button.clicked.connect(self.toggle_minimized_state)
        
        # ========== END CUSTOMIZATION ==========

        # Add button to the corner of the tab bar
        self.ribbon_tabs.setCornerWidget(self.minimize_button, Qt.TopRightCorner)

    def _update_minimize_button(self):
        """Update the minimize button appearance based on current state."""
        if hasattr(self, 'minimize_button') and self.minimize_button is not None:
            if self.ribbon_minimized:
                self.minimize_button.setText("+")
                self.minimize_button.setToolTip("Expand ribbon")
            else:
                self.minimize_button.setText("−")
                self.minimize_button.setToolTip("Minimize ribbon")

    def load_from_preferences(self):
        """Load the ribbon_minimized state from preferences."""
        prefs = self.preferences_getter()
        aero_prefs = prefs.get("settings", {}).get("tabs", {}).get("aerodynamics", {})
        self.ribbon_minimized = bool(aero_prefs.get("ribbon_minimized", False))

    def measure_heights(self):
        """Measure and cache the expanded and tab-strip-only heights."""
        if self.ribbon_frame is None or self.ribbon_tabs is None:
            return

        # Measure current full height
        if self.expanded_height is None:
            # Force layout update to get accurate size hint
            self.ribbon_frame.layout().update()
            self.expanded_height = self.ribbon_frame.sizeHint().height() + 6
            if self.expanded_height < 80:
                self.expanded_height = 80

        # Measure tab-strip-only height (tabBar + minimal content)
        if self.tab_strip_height is None:
            tab_bar_height = self.ribbon_tabs.tabBar().sizeHint().height()
            self.tab_strip_height = tab_bar_height + 4  # Add minimal padding

    def apply_current_state(self):
        """Apply the current ribbon_minimized state to the UI."""
        self.measure_heights()
        if self.ribbon_minimized:
            self._apply_minimized_view()
        else:
            self._apply_expanded_view()
        self._update_minimize_button()

    def _apply_expanded_view(self):
        """Show the ribbon fully expanded."""
        if self.ribbon_dock is None or self.ribbon_frame is None:
            return
        
        self.is_temp_expanded = False
        
        if self.expanded_height is None:
            self.measure_heights()

        # Show all ribbon tab content pages
        if self.ribbon_tabs is not None:
            # Hide the stacked widget's stack to show the current tab content
            stack = self.ribbon_tabs.findChild(QWidget, "qt_tabwidget_stackedwidget")
            if stack is not None:
                stack.setVisible(True)
            # Make sure all tab pages are visible
            for i in range(self.ribbon_tabs.count()):
                widget = self.ribbon_tabs.widget(i)
                if widget is not None:
                    widget.setVisible(True)

        # Set heights to expanded
        height = self.expanded_height or 100
        self.ribbon_frame.setMaximumHeight(16777215)  # Reset to max possible
        self.ribbon_dock.setMaximumHeight(16777215)
        self.ribbon_frame.setMinimumHeight(height)
        self.ribbon_dock.setMinimumHeight(height)

    def _apply_minimized_view(self):
        """Show only the ribbon tab bar (hide tab content)."""
        if self.ribbon_dock is None or self.ribbon_frame is None:
            return

        self.is_temp_expanded = False

        if self.tab_strip_height is None:
            self.measure_heights()

        # Hide the tab content stacked widget
        if self.ribbon_tabs is not None:
            stack = self.ribbon_tabs.findChild(QWidget, "qt_tabwidget_stackedwidget")
            if stack is not None:
                stack.setVisible(False)

        # Set to tab-strip height only
        height = self.tab_strip_height or 32
        self.ribbon_frame.setMaximumHeight(height)
        self.ribbon_dock.setMaximumHeight(height)
        self.ribbon_frame.setMinimumHeight(height)
        self.ribbon_dock.setMinimumHeight(height)

    def toggle_minimized_state(self):
        """Toggle between minimized and expanded states (persistent)."""
        self.ribbon_minimized = not self.ribbon_minimized
        self.apply_current_state()
        self._update_minimize_button()
        self._save_ribbon_state()

    def expand_temp_ribbon(self):
        """Temporarily expand the ribbon (while minimized) in place."""
        if not self.ribbon_minimized or self.is_temp_expanded:
            return

        self.is_temp_expanded = True
        self.measure_heights()

        # Show the current tab's content
        height = self.expanded_height or 100
        self.ribbon_frame.setMaximumHeight(height)
        self.ribbon_dock.setMaximumHeight(height)
        self.ribbon_frame.setMinimumHeight(height)
        self.ribbon_dock.setMinimumHeight(height)

        # Show all content (let tab widget handle which is visible)
        for i in range(self.ribbon_tabs.count()):
            widget = self.ribbon_tabs.widget(i)
            if widget is not None:
                widget.setVisible(True)

    def collapse_temp_ribbon(self):
        """Collapse the temporarily expanded ribbon back to tab-strip."""
        if not self.is_temp_expanded:
            return

        self.is_temp_expanded = False
        self._apply_minimized_view()

    def _is_click_inside_ribbon(self, global_pos):
        """Check if a global position is inside the ribbon area."""
        if self.ribbon_dock is None:
            return False
        
        ribbon_rect = self.ribbon_dock.rect()
        ribbon_global_rect = QRect(
            self.ribbon_dock.mapToGlobal(ribbon_rect.topLeft()),
            ribbon_rect.size()
        )
        return ribbon_global_rect.contains(global_pos)

    def _save_ribbon_state(self):
        """Save ribbon_minimized state to preferences."""
        prefs = self.preferences_getter()
        settings = prefs.setdefault("settings", {})
        tabs = settings.setdefault("tabs", {})
        aero = tabs.setdefault("aerodynamics", {})
        aero["ribbon_minimized"] = self.ribbon_minimized
        self.preferences_setter(prefs)

    def cleanup(self):
        """Clean up event filters and connections."""
        if self.ribbon_tabs is not None and self.ribbon_tabs.tabBar() is not None:
            self.ribbon_tabs.tabBar().removeEventFilter(self.tab_bar_filter)
        if QApplication.instance() is not None:
            QApplication.instance().removeEventFilter(self.click_outside_filter)
