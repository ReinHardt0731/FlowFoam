# PLANS AND ADDITIONAL FEATURES

## 1. File Sample Tutorials
```
|HOME| Recent Files
|    |--- , ----, ----,
|NEW |Tutorial Cases
|    |
|OPEN|
|    |
```
This is a feature that allows user to use template cases from tutorials

## 2. Animated Pre View
This allows the user to visualize the Result, This should be based on how the boundary condition was implemented and if there are rotations, it would be animated as well.

- Note that this should also inform the user wether it would transient or not wether its rotating or not wether its multiphase or not.

## 3. Improve the Ribbon and Tree Icons
The current icons for the ribbon as well as the tree is something I can't stomach. It uses emoji which is cringe. Future updates should allow seamless integration of thematic colors of the logo to the icons.

## 4. Include and widen the application of other solvers.



| Category | Solver Name | Type | Description | Typical Use Case |
|----------|------------|------|-------------|------------------|
| Incompressible | icoFoam | Transient, Laminar | Solves incompressible laminar flow using PISO | Low-speed, simple flows |
| Incompressible | simpleFoam | Steady-state | Uses SIMPLE algorithm | Steady aerodynamics |
| Incompressible | pisoFoam | Transient | Uses PISO algorithm | Time-dependent flows |
| Compressible | rhoSimpleFoam | Steady-state | Compressible flow (density varies) | High-speed steady flows |
| Compressible | rhoPisoFoam | Transient | Compressible transient solver | Unsteady compressible flows |
| Compressible | sonicFoam | Transient | Designed for transonic/supersonic | Shock waves, high Mach |
| Multiphase | interFoam | Transient | VOF method for two immiscible fluids | Air-water interface, waves |
| Multiphase | twoPhaseEulerFoam | Transient | Two continuous phases | Bubbly flows |
| Multiphase | reactingTwoPhaseEulerFoam | Transient | Multiphase with reactions | Combustion + multiphase |
| Heat Transfer | buoyantSimpleFoam | Steady-state | Natural convection (buoyancy effects) | Thermal flows |
| Heat Transfer | chtMultiRegionFoam | Transient | Conjugate heat transfer | Fluid + solid interaction |
| Combustion | reactingFoam | Transient | Combustion with chemistry | Flames, burners |
| Combustion | rhoReactingFoam | Transient | Compressible reacting flow | High-speed combustion |
| Lagrangian | sprayFoam | Transient | Particle tracking (sprays) | Fuel injection |
| Lagrangian | coalChemistryFoam | Transient | Coal particle combustion | Energy systems |
| Solid Mechanics | solidDisplacementFoam | Transient | Structural deformation | Solid stress analysis |

---

### 🔍 Naming Convention Cheat Sheet

| Keyword | Meaning |
|--------|--------|
| rho | Compressible flow |
| simple | Steady-state (SIMPLE algorithm) |
| piso | Transient (PISO algorithm) |
| inter | Interface capturing (VOF) |
| reacting | Includes chemistry |
| buoyant | Includes gravity/thermal effects |

---

### ⚠️ Key Insight

OpenFOAM solvers are not completely separate tools—they are combinations of:
- Mass conservation
- Momentum equations
- Energy equations
- Additional physics (multiphase, combustion, etc.)


## 3. Interactive Console
Users can use commands within the console

## 4. Allow user to have a space for Solver Creation

## 5. Improve the Ribon Options like Mesh Regions
```
┌─ Import ──────────────────────┐
│ • Import STL/CAD              │
│ • Import OpenFOAM Case        │
│ • Import Template Case        │
│ • Recent Cases (dropdown)     │
├─ Export ──────────────────────┤
│ • Export Full Case            │
│ • Export Mesh (VTK/STL)       │
│ • Export Config JSON          │
├─ Case Tools ──────────────────┤
│ • New Case (wizard)           │
│ • Duplicate Case              │
│ • Clean Case                  │
│ • Case Properties             │
└────────────────────────────────┘
┌─ Geometry Operations ─────────┐
│ • Load STL                    │
│ • View STL                    │
│ • Scale/Translate             │
│ • Rotate STL                  │
│ • Boolean Ops (union, cut)    │
│ • Simplify Mesh               │
├─ Domain ──────────────────────┤
│ • Create Domain Box           │
│ • Domain Bounds (input fields)│
│ • Refinement Region           │
│ • Domain Symmetry             │
├─ Visual ──────────────────────┤
│ • STL Transparency            │
│ • STL Color                   │
│ • Domain Wireframe Toggle     │
└────────────────────────────────┘
┌─ Mesh Strategy ───────────────┐
│ • Mesh Type (blockMesh/snappy)│
│ • Automatic Mesh (one-click)  │
│ • Advanced Settings           │
│ • Mesh Advisor               │
├─ Domain Mesh Settings ────────┤
│ • Cell Size (base)            │
│ • Cells X,Y,Z (show preview)  │
│ • Domain Expansion            │
│ • Mesh Aspects Ratio          │

┌─ Domain Shape Creator ─────────────┐
│ Select Preset Shape:               │
│ ┌──────────────────────────┐       │
│ │ ▼ Simple Box            │       │
│ │  • Simple Box           │       │
│ │  • Channel              │       │
│ │  • Pipe (O-Grid)        │       │
│ │  • Backward Step        │       │
│ │  • Cavity               │       │
│ │  • Expanding Duct       │       │
│ │  • L-Bend               │       │
│ │  • T-Junction           │       │
│ │  • Custom (Advanced)    │       │
│ └──────────────────────────┘       │
│                                    │
├─ Domain Parameters ───────────────┤
│ Min Point:  [-5]  [-3]  [-2] [m]  │
│ Max Point:  [15]  [ 3]  [ 5] [m]  │
│                                    │
│ Base Cell Size: [0.5] [m]          │
│ Cell Count:    [100]×[60]×[70]     │
│ Total Cells: ~420,000             │
│                                    │
├─ Refinement ──────────────────────┤
│ [✓] Add Inner Refinement Region   │
│ Inner Min: [-2] [-2] [-2]         │
│ Inner Max: [ 8] [ 2] [ 2]         │
│ Inner Cell Size: [0.2]            │
│                                    │
│ Inner: 8000, Outer: 412,000       │
│ Total: ~420,000 cells             │
├─ Preview ────────────────────────┤
│ [Show Domain] [Show Cells Count]  │
├─ Actions ────────────────────────┤
│ [✓ Create Mesh] [Copy Template]   │
│ [Save to blockMeshDict]           │
└────────────────────────────────────┘

├─ Surface Refinement ──────────┤
│ • STL Refinement Level [||]   │
│ • Edge Refinement             │
│ • Min/Max levels              │
│ • Feature Detection           │
├─ Boundary Layers ─────────────┤
│ • Enable/Disable              │
│ • Layer Height (y+)           │
│ • Growth Ratio                │
│ • Number of Layers            │
├─ Refinement Regions ──────────┤
│ • Add Region Button           │
│ • Region List (name, levels)  │
│ • Edit/Delete Region          │
├─ Mesh Quality ────────────────┤
│ • Generate Mesh Button        │
│ • Check Mesh                  │
│ • Mesh Info                   │
│ • Cell Count Display          │
├─ Sketch Tools ────────────────┤
│ • Reset View                  │
│ • Zoom Fit                    │
│ • Toggle Edges                │
└────────────────────────────────┘
┌─ Patch Selection ─────────────┐
│ • List of Available Patches   │
│ • Click/Select Patch          │
│ • Highlight Selected Patch    │
│ • Patch Properties            │
├─ Boundary Condition Type ─────┤
│ • Dropdown: [inlet  ▼]        │
│ •  - inlet                    │
│ •  - outlet                   │
│ •  - wall/slip                │
│ •  - symmetry                 │
│ •  - cyclic                   │
│ •  - wedge (2D 3D)            │
├─ Condition Parameters ────────┤
│ • Velocity (magnitude/vector) │
│ • Pressure reference          │
│ • Turbulence (k, ω, ε)        │
│ • Temperature (if thermal)    │
│ • Volatile Fields             │
├─ Advanced ────────────────────┤
│ • Velocity Profile (uniform,  │
│   parabolic, power law)       │
│ • Pressure Gradient           │
│ • Wall Functions              │
├─ Quick Assign ────────────────┤
│ • Common Presets              │
│ •  - Low Speed Inlet          │
│ •  - Pressure Outlet          │
│ •  - Zero Gradient            │
│ •  - Fixed Slip               │
│ • Copy From Another Patch     │
│ • Undo Recent Changes         │
└────────────────────────────────┘
┌─ Solver Selection ─────────────┐
│ • Solver: [simpleFoam  ▼]      │
│ •  - simpleFoam (steady)       │
│ *  - pisoFoam (transient)      │
│ •  - rhoSimpleFoam (compress)  │
│ • Advanced Solver Options      │
├─ Flow Type ───────────────────┤
│ • Compressibility: [O Incomp]  │
│ • Viscosity Model: [Laminar▼]  │
│ •  - Laminar                   │
│ •  - k-epsilon                 │
│ •  - k-omega (SST)             │
│ •  - Spalart-Allmaras          │
│ •  - LES                       │
├─ Fluid Properties ──────────── ┤
│ • Density                      │
│ • Dynamic Viscosity            │
│ • Reference Pressure           │
│ • Gravity Vector               │
├─ Solver Parameters ────────────┐
│ • Tolerance (residuals)        │
│ • Max Iterations               │
│ • Relaxation Factors           │
│ • Schemes (discretization)     │
├─ Transient Settings ────────── ┤
│ • Time Step (Δt)               │
│ • End Time                     │
│ • Write Interval               │
│ • Courant Number (auto Δt)     │
└────────────────────────────────┘

┌─ Run Control ──────────────────┐
│ • [►] Run Full Pipeline        │
│ • [►] Run Mesh Only            │
│ • [►] Run Solver Only          │
│ • [⏹] Cancel Run               │
├─ Quick Actions ────────────────┤
│ • Domain Mesh                  │
│ • Surface Features             │
│ • SnappyHexMesh                │
│ • Check Mesh                   │
│ • Run Solver                   │
├─ Parallel Computing ──────────┤
│ • Decompose: [O Serial, O 4P,  │
│    O 8P, O 16P]                │
│ • Parallel Options             │
├─ Monitoring ──────────────────┤
│ • [📊] Show Console            │
│ • [📈] Show Residuals Plot     │
│ • [⏱] Elapsed Time             │
│ • Case Speed (cells/sec)       │
└────────────────────────────────┘
┌─ Results Browsing ─────────────┐
│ • Load Results                 │
│ • Time Step Slider: ◄──|══►    │
│ • Available Fields: [dropdown] │
│ • Animate Time Series          │
├─ Field Visualization ─────────┤
│ • Field: [Pressure  ▼]         │
│ • Color Bar Bounds (auto/set)  │
│ • Contour Levels               │
│ • Iso-surfaces                 │
├─ Vector Fields ───────────────┤
│ • Streamlines                  │
│ • Velocity Vectors             │
│ • Vector Density               │
│ • Scale Factor                 │
├─ Geometry Slicing ────────────┤
│ • Slice Plane                  │
│ • Normal Direction [X/Y/Z]     │
│ • Position Slider              │
├─ Export Results ───────────────┤
│ • Export VTK/Ensight           │
│ • Screenshot                   │
│ • Animation (MP4/frames)       │
│ • Pressure CSV                 │
├─ Quick Presets ───────────────┤
│ • Load Pressure               │
│ • Load Velocity Magnitude      │
│ • Load Turbulence             │
│ • Load Combined (velocity+p)   │
└────────────────────────────────┘
```
