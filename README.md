# FlowFoam

Run:
`python aerodynamics_app/main.py`

Repo layout:
- `src/` contains the active Python source and generated Qt modules.
- `assets/ui/` contains the editable `.ui` files.
- `assets/icons/` and `assets/images/` contain static assets.
- `scripts/` contains helper entrypoints such as `run_aerodynamics.py` and `build_ui.py`.
- `samples/openfoam_case/` contains the bundled sample case template.
- Generated mesh output under `samples/openfoam_case/constant/polyMesh/` is kept local and is not committed to Git.
- `vendor/openfoam/` is reserved for an optional local OpenFOAM runtime install and is not committed to Git.
- `workspace/` contains local preferences, runtime helpers, and generated working cases and is not committed to Git.
- `docs/` contains the project notes and implementation guides moved out of the repo root.

Notes:
- The compatibility launcher at `aerodynamics_app/main.py` now forwards into the `src/` layout.
- The main window reuses the generated UI module built from `assets/ui/aircraft_design.ui`.
- Configure `openfoam.execution.windows_bootstrap` to point at your local OpenFOAM `setEnvVariables-*.bat` file.
