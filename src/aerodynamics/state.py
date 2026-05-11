from copy import deepcopy

from copy import deepcopy
from pathlib import Path

from tabs._shared import deep_merge_missing, ensure_dict


PATCH_TYPES = ["patch", "wall", "symmetryPlane", "farField"]
FLOW_PATCHES = ["inlet", "outlet", "farfield", "aircraft", "symmetry"]
CFD_FIELDS = ["U", "p", "k", "omega", "nut"]
FIELD_DIMENSIONS = {
    "U": "[0 1 -1 0 0 0 0]",
    "p": "[0 2 -2 0 0 0 0]",
    "k": "[0 2 -2 0 0 0 0]",
    "omega": "[0 0 -1 0 0 0 0]",
    "nut": "[0 2 -1 0 0 0 0]",
}
FIELD_INTERNAL_VALUES = {
    "U": "uniform (50 0 0)",
    "p": "uniform 0",
    "k": "uniform 0.01",
    "omega": "uniform 1",
    "nut": "uniform 0",
}


FV_SCHEMES_PRESETS = {
    "bounded steady RANS": {
        "ddt_default": "steadyState",
        "grad_default": "Gauss linear",
        "div_phi_u": "bounded Gauss upwind",
        "div_phi_turb": "bounded Gauss upwind",
        "div_nu_eff_dev2": "Gauss linear",
        "laplacian_default": "Gauss linear corrected",
        "interpolation_default": "linear",
        "sn_grad_default": "corrected",
        "wall_dist_method": "meshWave",
    },
    "potentialFoam basic": {
        "ddt_default": "steadyState",
        "grad_default": "Gauss linear",
        "div_phi_u": "Gauss linearUpwind grad(U)",
        "div_phi_turb": "bounded Gauss upwind",
        "div_nu_eff_dev2": "Gauss linear",
        "laplacian_default": "Gauss linear corrected",
        "interpolation_default": "linear",
        "sn_grad_default": "corrected",
        "wall_dist_method": "meshWave",
    },
}


FV_SOLUTION_PRESETS = {
    "SIMPLE-RANS": {
        "p_solver": "GAMG",
        "p_smoother": "GaussSeidel",
        "p_preconditioner": "DIC",
        "p_rel_tol": 0.01,
        "u_solver": "smoothSolver",
        "u_smoother": "symGaussSeidel",
        "u_preconditioner": "DILU",
        "u_rel_tol": 0.1,
        "simple_n_non_ortho": 0,
        "simple_consistent": False,
        "residual_control_p": 1.0e-5,
        "residual_control_u": 1.0e-5,
    },
    "Potential": {
        "p_solver": "GAMG",
        "p_smoother": "GaussSeidel",
        "p_preconditioner": "DIC",
        "p_rel_tol": 0.01,
        "u_solver": "smoothSolver",
        "u_smoother": "symGaussSeidel",
        "u_preconditioner": "DILU",
        "u_rel_tol": 0.1,
        "simple_n_non_ortho": 0,
        "simple_consistent": False,
        "residual_control_p": 1.0e-5,
        "residual_control_u": 1.0e-5,
    },
}


def _bc_default(field, patch_name):
    if field == "U":
        if patch_name == "inlet":
            return {"type": "fixedValue", "value": "uniform (50 0 0)"}
        if patch_name == "outlet":
            return {"type": "inletOutlet", "inlet_value": "uniform (0 0 0)", "value": "$internalField"}
        if patch_name == "farfield":
            return {"type": "zeroGradient", "value": ""}
        if patch_name == "symmetry":
            return {"type": "symmetryPlane", "value": ""}
        return {"type": "noSlip", "value": "uniform (0 0 0)"}
    if field == "p":
        if patch_name == "outlet":
            return {"type": "fixedValue", "value": "uniform 0"}
        if patch_name == "farfield":
            return {"type": "zeroGradient", "value": ""}
        if patch_name == "symmetry":
            return {"type": "symmetryPlane", "value": ""}
        return {"type": "zeroGradient", "value": ""}
    if field == "k":
        if patch_name == "aircraft":
            return {"type": "kqRWallFunction", "value": "uniform 0.01"}
        if patch_name == "symmetry":
            return {"type": "symmetryPlane", "value": ""}
        return {"type": "fixedValue", "value": "uniform 0.01"}
    if field == "omega":
        if patch_name == "aircraft":
            return {"type": "omegaWallFunction", "value": "uniform 1"}
        if patch_name == "symmetry":
            return {"type": "symmetryPlane", "value": ""}
        return {"type": "fixedValue", "value": "uniform 1"}
    if field == "nut":
        if patch_name == "aircraft":
            return {"type": "nutkWallFunction", "value": "uniform 0"}
        if patch_name == "symmetry":
            return {"type": "symmetryPlane", "value": ""}
        return {"type": "calculated", "value": "uniform 0"}
    return {"type": "zeroGradient", "value": ""}


def bootstrap_boundary_conditions(workflow):
    fields = {}
    for field in CFD_FIELDS:
        fields[field] = {patch: _bc_default(field, patch) for patch in FLOW_PATCHES}
    return {
        "patches": {
            "inlet": {"enabled": True, "type": "patch"},
            "outlet": {"enabled": True, "type": "patch"},
            "farfield": {"enabled": True, "type": "farField"},
            "aircraft": {"enabled": True, "type": "wall"},
            "symmetry": {"enabled": False, "type": "symmetryPlane"},
        },
        "fields": fields,
        "active_field": "U",
        "workflow": workflow,
    }


def default_openfoam_state():
    return {
        "workflow": "simpleFoam",
        "geometry": {
            "stl_path": "",
            "tri_surface_name": "aircraft",
            "scale": 1.0,
            "patches": {"aircraft": "wall"},
        },
        "mesh": {
            "preset": "External Aerodynamics",
            "snappy_profile": "Balanced",
            "snappy_parallel_mode": "Off",
            "domain_min": [-15.0, -15.0, -10.0],
            "domain_max": [35.0, 15.0, 10.0],
            "base_cells": [80, 48, 32],
            "castellated": True,
            "snap": True,
            "layers": True,
            "refinement_min": 2,
            "refinement_max": 4,
            "feature_angle": 30.0,
            "n_surface_layers": 3,
            "max_local_cells": 100000,
            "max_global_cells": 2000000,
            "min_refinement_cells": 10,
            "max_load_unbalance": 0.10,
            "location_in_mesh": [4.0, 4.0, 0.0],
            "allow_free_standing_zone_faces": True,
            "n_feature_snap_iter": 10,
            "implicit_feature_snap": False,
            "explicit_feature_snap": True,
            "multi_region_feature_snap": False,
            "expansion_ratio": 1.0,
            "final_layer_thickness": 0.3,
            "min_thickness": 0.1,
            "n_grow": 0,
            "layer_feature_angle": 60.0,
            "slip_feature_angle": 30.0,
            "layer_n_relax_iter": 3,
            "n_smooth_surface_normals": 1,
            "n_smooth_normals": 3,
            "n_smooth_thickness": 10,
            "max_face_thickness_ratio": 0.5,
            "max_thickness_to_medial_ratio": 0.3,
            "min_medial_axis_angle": 90.0,
            "n_buffer_cells_no_extrude": 0,
            "n_layer_iter": 50,
            "merge_tolerance": 1e-6,
            "refinement_region": {
                "enabled": True,
                "min": [-10.0, -20.0, -10.0],
                "max": [50.0, 20.0, 10.0],
                "level": 4,
            },
        },
        "check_mesh": {
            "enabled": True,
            "max_non_ortho": 70.0,
            "max_boundary_skewness": 20.0,
            "min_vol": 1.0e-13,
        },
        "boundary_conditions": bootstrap_boundary_conditions("simpleFoam"),
        "simulation": {
            "start_time": 0.0,
            "end_time": 1000.0,
            "delta_t": 1.0,
            "write_interval": 100.0,
            "purge_write": 0,
            "pseudo_transient": False,
            "use_parallel": True,
            "mpi_cores": 4,
        },
        "numerics": {
            "fv_schemes_preset": "bounded steady RANS",
            "fv_solution_preset": "SIMPLE-RANS",
            "turbulence_model": "kOmegaSST",
            "fv_schemes": deepcopy(FV_SCHEMES_PRESETS["bounded steady RANS"]),
            "fv_solution": deepcopy(FV_SOLUTION_PRESETS["SIMPLE-RANS"]),
            "u_solver_tol": 1.0e-6,
            "p_solver_tol": 1.0e-6,
            "u_relax": 0.7,
            "p_relax": 0.3,
            "simple_residual_control": 1.0e-5,
        },
        "export": {"output_path": "", "last_exported_at": "", "last_action": "", "generated_files": []},
        "scripts": {
            "write_helper_scripts": True,
            "allrun": "Allrun",
            "allclean": "Allclean",
            "allrun_bat": "Allrun.bat",
            "allclean_bat": "Allclean.bat",
            "include_surface_feature_extract": True,
        },
        "post_process": {
            "case_dir": "",
            "latest_time": "",
            "available_fields": [],
            "stage_logs": {},
            "updated_at": "",
            "vtk_status": "VTK: not exported",
            "paraview_path": "",
        },
        "execution": {
            "case_dir": "",
            "status": "idle",
            "active_stage": "none",
            "last_run_started_at": "",
            "last_run_finished_at": "",
            "last_error": "",
            "last_logs": {},
            "results": {},
            "windows_bootstrap": "",
        },
    }


def _ensure_bc_fields(of_state):
    bc = of_state.setdefault("boundary_conditions", {})
    bc.setdefault("patches", {})
    for patch in FLOW_PATCHES:
        if patch not in bc["patches"]:
            bc["patches"][patch] = {
                "enabled": True if patch in ("inlet", "outlet", "farfield", "aircraft") else False,
                "type": "wall" if patch == "aircraft" else ("symmetryPlane" if patch == "symmetry" else "patch"),
            }
    fields = bc.setdefault("fields", {})
    template = bootstrap_boundary_conditions(of_state.get("workflow", "simpleFoam"))["fields"]
    for field in CFD_FIELDS:
        if field not in fields or not isinstance(fields[field], dict):
            fields[field] = deepcopy(template[field])
        for patch in FLOW_PATCHES:
            if patch not in fields[field]:
                fields[field][patch] = deepcopy(template[field][patch])


def ensure_openfoam_state(aero_state):
    if not isinstance(aero_state, dict):
        aero_state = {}
    of_state = ensure_dict(aero_state, "openfoam")
    deep_merge_missing(of_state, default_openfoam_state())
    geo = of_state.get("geometry", {})
    stl_path = str(geo.get("stl_path", "")).strip()
    tri_name = str(geo.get("tri_surface_name", "")).strip()
    if stl_path:
        stem = Path(stl_path).stem.replace(" ", "_")
        if stem and (not tri_name or tri_name == "aircraft"):
            geo["tri_surface_name"] = stem
    _ensure_bc_fields(of_state)
    numerics = of_state.get("numerics", {})
    fv_solution = numerics.get("fv_solution", {})
    if isinstance(fv_solution, dict):
        preset_key = str(numerics.get("fv_solution_preset", "SIMPLE-RANS"))
        preset = FV_SOLUTION_PRESETS.get(preset_key, FV_SOLUTION_PRESETS["SIMPLE-RANS"])
        p_solver = str(fv_solution.get("p_solver", preset.get("p_solver", "GAMG")))
        u_solver = str(fv_solution.get("u_solver", preset.get("u_solver", "smoothSolver")))
        if p_solver in ("GAMG", "smoothSolver") and not fv_solution.get("p_smoother"):
            fv_solution["p_smoother"] = preset.get("p_smoother", "GaussSeidel")
        if u_solver == "smoothSolver" and not fv_solution.get("u_smoother"):
            fv_solution["u_smoother"] = preset.get("u_smoother", "symGaussSeidel")
        if "residual_control_p" not in fv_solution:
            fv_solution["residual_control_p"] = numerics.get("simple_residual_control", 1.0e-5)
        if "residual_control_u" not in fv_solution:
            fv_solution["residual_control_u"] = numerics.get("simple_residual_control", 1.0e-5)
    return of_state


__all__ = [
    "PATCH_TYPES",
    "FLOW_PATCHES",
    "CFD_FIELDS",
    "FIELD_DIMENSIONS",
    "FIELD_INTERNAL_VALUES",
    "FV_SCHEMES_PRESETS",
    "FV_SOLUTION_PRESETS",
    "default_openfoam_state",
    "ensure_openfoam_state",
    "bootstrap_boundary_conditions",
]
