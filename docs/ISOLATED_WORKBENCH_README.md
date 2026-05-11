# Isolated CFD Aerodynamics Workbench

## Overview
This directory now contains an **isolated CFD workbench** that is completely independent from other workbenches (Sketch, Structures, Propulsion, etc.). This isolation makes it easier to:
- Edit and maintain the UI without confusion from other components
- Build and test CFD features independently
- Integrate back into the main application later when ready

## New Files

### UI Files
- **`aerodynamics_workbench.ui`** - Clean, focused UI definition file containing only CFD-relevant elements
  - Ribbon toolbar with CFD-specific buttons (Case Management, Workspace, Camera)
  - Tree view for project structure
  - Properties/Task panel for CFD parameters
  - 3D viewer (MDI Area) for mesh/geometry visualization  
  - Console dock for CFD solver output
  - **No references to other workbenches or tabs**

### Generated Python Files
- **`aerodynamics_workbench.py`** - Auto-generated Python code from the .ui file
  - Contains `Ui_CFDAerodynamicsWindow` class
  - Manages all UI widget creation and layout
  - **Never edit directly** - regenerate from .ui file if changes needed

### Application Entry Points
- **`aerodynamics_app/main_isolated.py`** - New isolated main application
  - Clean, focused entry point for CFD workbench
  - Only imports and uses CFD-related components
  - Much simpler than the original `main.py` with its multi-workbench complexity
  - Contains all application initialization, menu setup, and event handlers

### Legacy Files (Still Available)
- **`aircraft_design.ui`** - Original multi-workbench UI (kept for reference/integration)
- **`aircraft_design.py`** - Generated code from aircraft_design.ui
- **`aerodynamics_app/main.py`** - Original entry point (kept for reference)

## Usage

### Run Isolated CFD Workbench
```bash
python aerodynamics_app/main_isolated.py
```

### Run Original Multi-Workbench Application
```bash
python aerodynamics_app/main.py
```

## Development Workflow

### To Modify CFD UI
1. **Edit the .ui file** (`aerodynamics_workbench.ui`)
   - Use Qt Designer or text editor
   - Focus only on CFD elements
   - No UI contamination from other workbenches

2. **Regenerate Python code** from .ui file:
   ```bash
   pyside6-uic aerodynamics_workbench.ui -o aerodynamics_workbench.py
   ```

3. **Update main_isolated.py** if needed
   - Add new button connections
   - Add new event handlers
   - Simple, focused code

4. **Test thoroughly**
   ```bash
   python aerodynamics_app/main_isolated.py
   ```

## Integration Plan

When ready to integrate back into main application:

1. **Extract working code** from `main_isolated.py`
2. **Merge UI elements** from `aerodynamics_workbench.ui` into `aircraft_design.ui`
3. **Update aircraft_design.py** with CFD improvements
4. **Test with original `main.py`**
5. **Archive isolated files** for reference

## File Structure

```
f:/ResearchFiles/Openfoam/
├── aerodynamics_workbench.ui          ← NEW: Isolated CFD UI
├── aerodynamics_workbench.py          ← NEW: Generated UI code
├── aircraft_design.ui                 ← LEGACY: Multi-workbench UI
├── aircraft_design.py                 ← LEGACY: Generated multi-workbench code
├── aerodynamics/
│   ├── __init__.py
│   ├── controller_legacy.py            ← Refactored CFD controller
│   ├── state.py
│   ├── execution.py
│   └── ...
├── aerodynamics_app/
│   ├── __init__.py
│   ├── main.py                         ← LEGACY: Multi-workbench entry point
│   ├── main_isolated.py                ← NEW: Isolated CFD entry point
│   ├── ribbon_controller.py
│   ├── file_organizer.py
│   ├── code_editor.py
│   ├── history_manager.py
│   └── ...
└── ...
```

## Key Differences: Isolated vs. Original

| Aspect | Isolated (`main_isolated.py`) | Original (`main.py`) |
|--------|------|----------|
| UI File | `aerodynamics_workbench.ui` (Simple) | `aircraft_design.ui` (Complex, multi-workbench) |
| Main Class | `CFDWorkbenchWindow` | `AeroWindow` |
| Workbenches Supported | CFD Only | Multiple (CFD, Sketch, Structures, Propulsion) |
| Code Complexity | Lower - focused | Higher - multi-workbench |
| Lines of Code | ~400 (main_isolated.py) | ~1200+ (main.py in original) |
| Dependencies | CFD modules only | All workbench modules |
| Focus | Clean, maintainable | Full-featured, but complex |

## Benefits of Isolation

✅ **Clarity**: No confusion from unrelated UI elements  
✅ **Maintainability**: Edit one focused UI file  
✅ **Testability**: Easier to test CFD features independently  
✅ **Development Speed**: Faster iteration on CFD workbench  
✅ **Error Isolation**: Bugs don't spread to other workbenches  
✅ **Reference**: Can study design without multi-workbench noise  

## Notes

- All CFD controller code in `aerodynamics/controller_legacy.py` is unchanged
- State management and file I/O work identically
- OpenFOAM execution remains the same
- RibbonController and other utilities work with both versions
- Can run both versions simultaneously for comparison/testing

## Future: Integration Back

When isolation phase is complete and CFD features are stable:

1. Merge improvements back to `aircraft_design.ui`
2. Clean up `aircraft_design.py`
3. Archive `aerodynamics_workbench.*` as reference
4. Maintain original entry point (`main.py`) for full app
5. Document lessons learned for next workbench
