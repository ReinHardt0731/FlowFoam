from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re

from .state import default_openfoam_state, ensure_openfoam_state


_NUMBER = r"[-+]?(?:\d+\.\d*|\d*\.\d+|\d+)(?:[eE][-+]?\d+)?"


def _strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//.*", "", text)
    return text


def _read_text(path: Path) -> str:
    return _strip_comments(path.read_text(encoding="utf-8", errors="ignore"))


def _find_brace_block(text: str, key: str) -> str:
    match = re.search(rf"\b{re.escape(key)}\b\s*\{{", text)
    if not match:
        return ""
    start = match.end() - 1
    depth = 0
    for idx in range(start, len(text)):
        ch = text[idx]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : idx]
    return ""


def _find_paren_block(text: str, key: str) -> str:
    match = re.search(rf"\b{re.escape(key)}\b\s*\(", text)
    if not match:
        return ""
    start = match.end() - 1
    depth = 0
    for idx in range(start, len(text)):
        ch = text[idx]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start + 1 : idx]
    return ""


def _parse_number(text: str, key: str) -> float | None:
    match = re.search(rf"\b{re.escape(key)}\b\s+({_NUMBER})", text)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def _parse_bool(text: str, key: str) -> bool | None:
    match = re.search(rf"\b{re.escape(key)}\b\s+(true|false|yes|no|on|off)\b", text, flags=re.I)
    if not match:
        return None
    return match.group(1).strip().lower() in {"true", "yes", "on"}


def _parse_vector(text: str, key: str, variables: dict[str, float] | None = None) -> list[float] | None:
    match = re.search(rf"\b{re.escape(key)}\b\s*\(([^)]+)\)", text)
    if not match:
        return None
    raw = match.group(1).strip().split()
    if len(raw) < 3:
        return None
    values: list[float] = []
    for token in raw[:3]:
        val = _resolve_token(token, variables or {})
        if val is None:
            return None
        values.append(val)
    return values


def _resolve_token(token: str, variables: dict[str, float]) -> float | None:
    token = token.strip()
    if token.startswith("$"):
        key = token[1:]
        if key in variables:
            return float(variables[key])
        return None
    try:
        return float(token)
    except ValueError:
        return None


def _parse_scalar_definitions(text: str) -> dict[str, float]:
    results: dict[str, float] = {}
    for match in re.finditer(rf"^\s*([A-Za-z]\w*)\s+({_NUMBER})\s*;", text, flags=re.M):
        key = match.group(1)
        try:
            results[key] = float(match.group(2))
        except ValueError:
            continue
    return results


def _parse_block_mesh(text: str) -> dict[str, object]:
    variables = _parse_scalar_definitions(text)
    scale = _parse_number(text, "convertToMeters")
    if scale is None:
        scale = _parse_number(text, "scale")
    if scale is None:
        scale = 1.0
    dmin = None
    dmax = None
    if all(k in variables for k in ("minX", "minY", "minZ", "maxX", "maxY", "maxZ")):
        dmin = [variables["minX"], variables["minY"], variables["minZ"]]
        dmax = [variables["maxX"], variables["maxY"], variables["maxZ"]]
    if dmin is None or dmax is None:
        vertices_block = _find_paren_block(text, "vertices")
        coords = []
        for match in re.finditer(r"\(\s*([^\)]+?)\s*\)", vertices_block):
            tokens = match.group(1).strip().split()
            if len(tokens) < 3:
                continue
            vals = []
            valid = True
            for token in tokens[:3]:
                val = _resolve_token(token, variables)
                if val is None:
                    valid = False
                    break
                vals.append(val)
            if valid:
                coords.append(vals)
        if coords:
            dmin = [min(v[i] for v in coords) for i in range(3)]
            dmax = [max(v[i] for v in coords) for i in range(3)]
    if dmin is not None and dmax is not None and scale not in (1.0, None):
        dmin = [v * scale for v in dmin]
        dmax = [v * scale for v in dmax]
    blocks_block = _find_paren_block(text, "blocks")
    cells = None
    match = re.search(r"hex\s*\([^\)]*\)\s*\(\s*([^\)]+)\)", blocks_block)
    if match:
        parts = match.group(1).strip().split()
        if len(parts) >= 3:
            try:
                cells = [int(float(parts[0])), int(float(parts[1])), int(float(parts[2]))]
            except ValueError:
                cells = None
    return {"domain_min": dmin, "domain_max": dmax, "base_cells": cells}


def _parse_snappy_hex_mesh(text: str) -> dict[str, object]:
    payload: dict[str, object] = {}
    payload["castellated"] = _parse_bool(text, "castellatedMesh")
    payload["snap"] = _parse_bool(text, "snap")
    payload["layers"] = _parse_bool(text, "addLayers")
    for key, dest in (
        ("maxLocalCells", "max_local_cells"),
        ("maxGlobalCells", "max_global_cells"),
        ("minRefinementCells", "min_refinement_cells"),
        ("maxLoadUnbalance", "max_load_unbalance"),
        ("resolveFeatureAngle", "feature_angle"),
        ("nFeatureSnapIter", "n_feature_snap_iter"),
        ("expansionRatio", "expansion_ratio"),
        ("finalLayerThickness", "final_layer_thickness"),
        ("minThickness", "min_thickness"),
        ("nGrow", "n_grow"),
        ("featureAngle", "layer_feature_angle"),
        ("slipFeatureAngle", "slip_feature_angle"),
        ("nRelaxIter", "layer_n_relax_iter"),
        ("nSmoothSurfaceNormals", "n_smooth_surface_normals"),
        ("nSmoothNormals", "n_smooth_normals"),
        ("nSmoothThickness", "n_smooth_thickness"),
        ("maxFaceThicknessRatio", "max_face_thickness_ratio"),
        ("maxThicknessToMedialRatio", "max_thickness_to_medial_ratio"),
        ("minMedialAxisAngle", "min_medial_axis_angle"),
        ("nBufferCellsNoExtrude", "n_buffer_cells_no_extrude"),
        ("nLayerIter", "n_layer_iter"),
        ("mergeTolerance", "merge_tolerance"),
    ):
        value = _parse_number(text, key)
        if value is not None:
            payload[dest] = value
    payload["location_in_mesh"] = _parse_vector(text, "locationInMesh")
    payload["allow_free_standing_zone_faces"] = _parse_bool(text, "allowFreeStandingZoneFaces")
    payload["implicit_feature_snap"] = _parse_bool(text, "implicitFeatureSnap")
    payload["explicit_feature_snap"] = _parse_bool(text, "explicitFeatureSnap")
    payload["multi_region_feature_snap"] = _parse_bool(text, "multiRegionFeatureSnap")
    n_layers = _parse_number(text, "nSurfaceLayers")
    if n_layers is not None:
        payload["n_surface_layers"] = int(n_layers)

    refinement_surfaces = _find_brace_block(text, "refinementSurfaces")
    if refinement_surfaces:
        match = re.search(rf"\blevel\s*\(\s*({_NUMBER})\s+({_NUMBER})\s*\)", refinement_surfaces)
        if match:
            payload["refinement_min"] = int(float(match.group(1)))
            payload["refinement_max"] = int(float(match.group(2)))

    geometry_block = _find_brace_block(text, "geometry")
    tri_surface_name = None
    stl_file = None
    if geometry_block:
        cursor = 0
        while cursor < len(geometry_block):
            match = re.search(r"([A-Za-z0-9_\.]+)\s*\{", geometry_block[cursor:])
            if not match:
                break
            entry_name = match.group(1).strip()
            start = cursor + match.start()
            entry_block = _find_brace_block(geometry_block[start:], entry_name)
            if entry_block:
                if re.search(r"\btype\s+triSurface", entry_block):
                    tri_surface_name = entry_name
                    file_match = re.search(r'file\s+"([^"]+\.stl)"', entry_block, flags=re.I)
                    if file_match:
                        stl_file = file_match.group(1).strip()
                    name_match = re.search(r"\bname\s+([^;]+);", entry_block)
                    if name_match:
                        tri_surface_name = name_match.group(1).strip()
                    break
            cursor = start + 1
        if stl_file is None:
            file_match = re.search(r'file\s+"([^"]+\.stl)"', geometry_block, flags=re.I)
            if file_match:
                stl_file = file_match.group(1).strip()
        if tri_surface_name is None:
            name_match = re.search(r"\bname\s+([^;]+);", geometry_block)
            if name_match:
                tri_surface_name = name_match.group(1).strip()
    if stl_file is None and tri_surface_name and tri_surface_name.lower().endswith(".stl"):
        stl_file = tri_surface_name
        tri_surface_name = Path(tri_surface_name).stem
    if tri_surface_name is not None:
        payload["tri_surface_name"] = Path(tri_surface_name).stem.replace(" ", "_")
    if stl_file is not None:
        payload["stl_file"] = stl_file

    refinement_box = _find_brace_block(text, "refinementBox")
    rr_min = _parse_vector(refinement_box, "min")
    rr_max = _parse_vector(refinement_box, "max")
    if rr_min and rr_max:
        payload["refinement_region"] = {"enabled": True, "min": rr_min, "max": rr_max}

    refinement_regions = _find_brace_block(text, "refinementRegions")
    if refinement_regions:
        level_match = re.search(rf"levels\s*\(\(\s*{_NUMBER}\s+({_NUMBER})\s*\)\)", refinement_regions)
        if level_match:
            payload.setdefault("refinement_region", {})["level"] = int(float(level_match.group(1)))
    return payload


def _parse_fv_schemes(text: str) -> dict[str, object]:
    schemes: dict[str, object] = {}
    fv: dict[str, object] = {}

    def parse_default(block: str) -> str | None:
        if not block:
            return None
        match = re.search(r"\bdefault\b\s+([^;]+);", block)
        return match.group(1).strip() if match else None

    def parse_entry(block: str, key: str) -> str | None:
        if not block:
            return None
        match = re.search(rf"\b{re.escape(key)}\b\s+([^;]+);", block)
        return match.group(1).strip() if match else None

    ddt_block = _find_brace_block(text, "ddtSchemes")
    val = parse_default(ddt_block)
    if val:
        fv["ddt_default"] = val

    grad_block = _find_brace_block(text, "gradSchemes")
    val = parse_default(grad_block)
    if val:
        fv["grad_default"] = val

    div_block = _find_brace_block(text, "divSchemes")
    div_u = parse_entry(div_block, "div(phi,U)")
    if div_u:
        fv["div_phi_u"] = div_u
        if "linearUpwind" in div_u:
            schemes["fv_schemes_preset"] = "potentialFoam basic"
        else:
            schemes["fv_schemes_preset"] = "bounded steady RANS"
    div_k = parse_entry(div_block, "div(phi,k)")
    div_omega = parse_entry(div_block, "div(phi,omega)")
    div_nu_eff = parse_entry(div_block, "div((nuEff*dev2(T(grad(U)))))")
    if div_k:
        fv["div_phi_turb"] = div_k
    elif div_omega:
        fv["div_phi_turb"] = div_omega
    if div_nu_eff:
        fv["div_nu_eff_dev2"] = div_nu_eff

    lap_block = _find_brace_block(text, "laplacianSchemes")
    val = parse_default(lap_block)
    if val:
        fv["laplacian_default"] = val

    interp_block = _find_brace_block(text, "interpolationSchemes")
    val = parse_default(interp_block)
    if val:
        fv["interpolation_default"] = val

    sn_block = _find_brace_block(text, "snGradSchemes")
    val = parse_default(sn_block)
    if val:
        fv["sn_grad_default"] = val

    wall_block = _find_brace_block(text, "wallDist")
    val = parse_entry(wall_block, "method")
    if val:
        fv["wall_dist_method"] = val

    if fv:
        schemes["fv_schemes"] = fv
    return schemes


def _parse_fv_solution(text: str) -> dict[str, object]:
    results: dict[str, object] = {}
    fv: dict[str, object] = {}

    def parse_word(block: str, key: str) -> str | None:
        if not block:
            return None
        match = re.search(rf"\b{re.escape(key)}\b\s+([A-Za-z0-9_]+)\s*;", block)
        return match.group(1).strip() if match else None

    solvers = _find_brace_block(text, "solvers")
    if solvers:
        p_block = _find_brace_block(solvers, "p")
        if p_block:
            solver = parse_word(p_block, "solver")
            if solver:
                fv["p_solver"] = solver
            smoother = parse_word(p_block, "smoother")
            if smoother:
                fv["p_smoother"] = smoother
            precond = parse_word(p_block, "preconditioner")
            if precond:
                fv["p_preconditioner"] = precond
            tol = _parse_number(p_block, "tolerance")
            if tol is not None:
                results["p_solver_tol"] = tol
            rel = _parse_number(p_block, "relTol")
            if rel is not None:
                fv["p_rel_tol"] = rel
        u_block = _find_brace_block(solvers, "U")
        if u_block:
            solver = parse_word(u_block, "solver")
            if solver:
                fv["u_solver"] = solver
            smoother = parse_word(u_block, "smoother")
            if smoother:
                fv["u_smoother"] = smoother
            precond = parse_word(u_block, "preconditioner")
            if precond:
                fv["u_preconditioner"] = precond
            tol = _parse_number(u_block, "tolerance")
            if tol is not None:
                results["u_solver_tol"] = tol
            rel = _parse_number(u_block, "relTol")
            if rel is not None:
                fv["u_rel_tol"] = rel
    relaxation = _find_brace_block(text, "relaxationFactors")
    if relaxation:
        fields = _find_brace_block(relaxation, "fields")
        if fields:
            p_relax = _parse_number(fields, "p")
            if p_relax is not None:
                results["p_relax"] = p_relax
        equations = _find_brace_block(relaxation, "equations")
        if equations:
            u_relax = _parse_number(equations, "U")
            if u_relax is not None:
                results["u_relax"] = u_relax
    simple = _find_brace_block(text, "SIMPLE")
    if simple:
        n_non_ortho = _parse_number(simple, "nNonOrthogonalCorrectors")
        if n_non_ortho is not None:
            fv["simple_n_non_ortho"] = int(n_non_ortho)
        consistent = _parse_bool(simple, "consistent")
        if consistent is not None:
            fv["simple_consistent"] = consistent
        residual = _find_brace_block(simple, "residualControl")
        if residual:
            res_p = _parse_number(residual, "p")
            if res_p is not None:
                fv["residual_control_p"] = res_p
                results["simple_residual_control"] = res_p
            res_u = _parse_number(residual, "U")
            if res_u is not None:
                fv["residual_control_u"] = res_u
    if fv:
        results["fv_solution"] = fv
    return results


def _parse_mesh_quality(text: str) -> dict[str, object]:
    results: dict[str, object] = {}
    for key, dest in (
        ("maxNonOrtho", "max_non_ortho"),
        ("maxBoundarySkewness", "max_boundary_skewness"),
        ("minVol", "min_vol"),
    ):
        val = _parse_number(text, key)
        if val is not None:
            results[dest] = val
    return results


def _parse_decompose_par(text: str) -> dict[str, object]:
    results: dict[str, object] = {}
    cores = _parse_number(text, "numberOfSubdomains")
    if cores is not None:
        results["mpi_cores"] = int(float(cores))
    return results


def _parse_turbulence_model(text: str) -> str | None:
    ras = _find_brace_block(text, "RAS")
    if ras:
        match = re.search(r"\bmodel\s+([A-Za-z0-9_]+)\s*;", ras)
        if match:
            return match.group(1)
    les = _find_brace_block(text, "LES")
    if les:
        match = re.search(r"\bmodel\s+([A-Za-z0-9_]+)\s*;", les)
        if match:
            return match.group(1)
    return None


def parse_openfoam_case(case_dir: str | Path, base_state: dict | None = None) -> tuple[dict, list[str]]:
    case_path = Path(case_dir)
    if not case_path.is_dir():
        raise FileNotFoundError(f"Case folder not found: {case_path}")
    base = deepcopy(base_state) if base_state is not None else default_openfoam_state()
    aero_state = {"openfoam": base}
    of_state = ensure_openfoam_state(aero_state)
    warnings: list[str] = []

    control_path = case_path / "system" / "controlDict"
    if not control_path.is_file():
        raise FileNotFoundError(f"Missing controlDict: {control_path}")
    control_text = _read_text(control_path)
    app_match = re.search(r"\bapplication\b\s+([A-Za-z0-9_]+)\s*;", control_text)
    if app_match:
        app = app_match.group(1).strip()
        if app in {"simpleFoam", "potentialFoam"}:
            of_state["workflow"] = app
    for key, dest in (
        ("startTime", "start_time"),
        ("endTime", "end_time"),
        ("deltaT", "delta_t"),
        ("writeInterval", "write_interval"),
        ("purgeWrite", "purge_write"),
    ):
        val = _parse_number(control_text, key)
        if val is not None:
            of_state["simulation"][dest] = val if dest != "purge_write" else int(val)

    block_path = case_path / "system" / "blockMeshDict"
    if block_path.is_file():
        block_mesh = _parse_block_mesh(_read_text(block_path))
        if block_mesh.get("domain_min"):
            of_state["mesh"]["domain_min"] = [float(v) for v in block_mesh["domain_min"]]
        if block_mesh.get("domain_max"):
            of_state["mesh"]["domain_max"] = [float(v) for v in block_mesh["domain_max"]]
        if block_mesh.get("base_cells"):
            of_state["mesh"]["base_cells"] = [int(v) for v in block_mesh["base_cells"]]
    else:
        warnings.append("system/blockMeshDict not found.")

    snappy_path = case_path / "system" / "snappyHexMeshDict"
    if snappy_path.is_file():
        snappy = _parse_snappy_hex_mesh(_read_text(snappy_path))
        for key in ("castellated", "snap", "layers"):
            if snappy.get(key) is not None:
                of_state["mesh"][key] = bool(snappy[key])
        for key in (
            "max_local_cells",
            "max_global_cells",
            "min_refinement_cells",
            "max_load_unbalance",
            "feature_angle",
            "n_feature_snap_iter",
            "expansion_ratio",
            "final_layer_thickness",
            "min_thickness",
            "n_grow",
            "layer_feature_angle",
            "slip_feature_angle",
            "layer_n_relax_iter",
            "n_smooth_surface_normals",
            "n_smooth_normals",
            "n_smooth_thickness",
            "max_face_thickness_ratio",
            "max_thickness_to_medial_ratio",
            "min_medial_axis_angle",
            "n_buffer_cells_no_extrude",
            "n_layer_iter",
            "merge_tolerance",
        ):
            if key in snappy:
                of_state["mesh"][key] = snappy[key]
        if snappy.get("location_in_mesh"):
            of_state["mesh"]["location_in_mesh"] = [float(v) for v in snappy["location_in_mesh"]]
        if snappy.get("allow_free_standing_zone_faces") is not None:
            of_state["mesh"]["allow_free_standing_zone_faces"] = bool(snappy["allow_free_standing_zone_faces"])
        if snappy.get("implicit_feature_snap") is not None:
            of_state["mesh"]["implicit_feature_snap"] = bool(snappy["implicit_feature_snap"])
        if snappy.get("explicit_feature_snap") is not None:
            of_state["mesh"]["explicit_feature_snap"] = bool(snappy["explicit_feature_snap"])
        if snappy.get("multi_region_feature_snap") is not None:
            of_state["mesh"]["multi_region_feature_snap"] = bool(snappy["multi_region_feature_snap"])
        if snappy.get("n_surface_layers") is not None:
            of_state["mesh"]["n_surface_layers"] = int(snappy["n_surface_layers"])
        if snappy.get("refinement_min") is not None:
            of_state["mesh"]["refinement_min"] = int(snappy["refinement_min"])
        if snappy.get("refinement_max") is not None:
            of_state["mesh"]["refinement_max"] = int(snappy["refinement_max"])
        if snappy.get("tri_surface_name"):
            of_state["geometry"]["tri_surface_name"] = str(snappy["tri_surface_name"])
        if snappy.get("stl_file"):
            stl_file = str(snappy["stl_file"])
            for subdir in ("constant/geometry", "constant/triSurface"):
                candidate = case_path / subdir / stl_file
                if candidate.is_file():
                    of_state["geometry"]["stl_path"] = str(candidate)
                    break
            else:
                of_state["geometry"]["stl_path"] = str(case_path / stl_file)
        if snappy.get("refinement_region"):
            rr = of_state["mesh"].setdefault("refinement_region", {})
            rr.update(snappy["refinement_region"])
    else:
        warnings.append("system/snappyHexMeshDict not found.")

    fv_schemes_path = case_path / "system" / "fvSchemes"
    if fv_schemes_path.is_file():
        schemes = _parse_fv_schemes(_read_text(fv_schemes_path))
        if schemes.get("fv_schemes_preset"):
            of_state["numerics"]["fv_schemes_preset"] = schemes["fv_schemes_preset"]
        if schemes.get("fv_schemes") and isinstance(schemes.get("fv_schemes"), dict):
            of_state["numerics"]["fv_schemes"].update(schemes["fv_schemes"])
    else:
        warnings.append("system/fvSchemes not found.")

    fv_solution_path = case_path / "system" / "fvSolution"
    if fv_solution_path.is_file():
        solution = _parse_fv_solution(_read_text(fv_solution_path))
        for key, dest in (
            ("p_solver_tol", "p_solver_tol"),
            ("u_solver_tol", "u_solver_tol"),
            ("p_relax", "p_relax"),
            ("u_relax", "u_relax"),
            ("simple_residual_control", "simple_residual_control"),
        ):
            if key in solution:
                of_state["numerics"][dest] = solution[key]
        if solution.get("fv_solution") and isinstance(solution.get("fv_solution"), dict):
            of_state["numerics"]["fv_solution"].update(solution["fv_solution"])
    else:
        warnings.append("system/fvSolution not found.")

    mesh_quality_path = case_path / "system" / "meshQualityDict"
    if mesh_quality_path.is_file():
        quality = _parse_mesh_quality(_read_text(mesh_quality_path))
        for key, dest in (
            ("max_non_ortho", "max_non_ortho"),
            ("max_boundary_skewness", "max_boundary_skewness"),
            ("min_vol", "min_vol"),
        ):
            if key in quality:
                of_state["check_mesh"][dest] = quality[key]
    else:
        warnings.append("system/meshQualityDict not found.")

    decompose_path = case_path / "system" / "decomposeParDict"
    if decompose_path.is_file():
        decomp = _parse_decompose_par(_read_text(decompose_path))
        if decomp.get("mpi_cores") is not None:
            of_state["simulation"]["mpi_cores"] = int(decomp["mpi_cores"])
            of_state["simulation"]["use_parallel"] = int(decomp["mpi_cores"]) > 1

    turb_path = case_path / "constant" / "turbulenceProperties"
    if not turb_path.is_file():
        turb_path = case_path / "constant" / "momentumTransport"
    if turb_path.is_file():
        model = _parse_turbulence_model(_read_text(turb_path))
        if model:
            of_state["numerics"]["turbulence_model"] = model

    of_state["execution"]["case_dir"] = str(case_path)
    of_state["export"]["output_path"] = str(case_path)
    ensure_openfoam_state(aero_state)
    return of_state, warnings


__all__ = ["parse_openfoam_case"]
