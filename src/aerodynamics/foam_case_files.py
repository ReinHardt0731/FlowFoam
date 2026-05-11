from ._controller_common import *

def _build_block_mesh_dict(of_state):
    mesh = of_state["mesh"]
    dmin = mesh["domain_min"]
    dmax = mesh["domain_max"]
    nx, ny, nz = mesh["base_cells"]
    vertices = [
        (dmin[0], dmin[1], dmin[2]),
        (dmax[0], dmin[1], dmin[2]),
        (dmax[0], dmax[1], dmin[2]),
        (dmin[0], dmax[1], dmin[2]),
        (dmin[0], dmin[1], dmax[2]),
        (dmax[0], dmin[1], dmax[2]),
        (dmax[0], dmax[1], dmax[2]),
        (dmin[0], dmax[1], dmax[2]),
    ]
    lines = [_foam_header("dictionary", "blockMeshDict")]
    lines.append("convertToMeters 1;\n")
    lines.append("vertices\n(\n")
    for v in vertices:
        lines.append(f"    ({_fmt_float(v[0])} {_fmt_float(v[1])} {_fmt_float(v[2])})\n")
    lines.append(");\n\n")
    lines.append("blocks\n(\n")
    lines.append(f"    hex (0 1 2 3 4 5 6 7) ({int(nx)} {int(ny)} {int(nz)}) simpleGrading (1 1 1)\n")
    lines.append(");\n\n")
    lines.append("edges\n(\n);\n\n")
    lines.append(
        "boundary\n(\n"
        "    inlet    { type patch; faces ((0 4 7 3)); }\n"
        "    outlet   { type patch; faces ((1 2 6 5)); }\n"
        "    farfield { type patch; faces ((0 1 5 4) (3 7 6 2) (0 3 2 1) (4 5 6 7)); }\n"
        ");\n\n"
        "mergePatchPairs\n(\n);\n"
    )
    return "".join(lines)


def _build_snappy_hex_mesh_dict(of_state, stl_name):
    mesh = of_state["mesh"]
    geom = of_state["geometry"]
    emesh_name = f"{geom['tri_surface_name']}.eMesh"
    loc = mesh.get("location_in_mesh", [4.0, 4.0, 0.0])
    rr = mesh.get("refinement_region", {})
    rr_enabled = bool(rr.get("enabled", False))
    rr_min = rr.get("min", [])
    rr_max = rr.get("max", [])
    rr_level = rr.get("level", mesh.get("refinement_min", 1))
    rr_valid = False
    try:
        if (
            isinstance(rr_min, (list, tuple))
            and isinstance(rr_max, (list, tuple))
            and len(rr_min) == 3
            and len(rr_max) == 3
        ):
            rr_min = [float(v) for v in rr_min]
            rr_max = [float(v) for v in rr_max]
            rr_valid = all(rr_min[i] < rr_max[i] for i in range(3))
    except (TypeError, ValueError):
        rr_valid = False
    try:
        rr_level = int(float(rr_level))
    except (TypeError, ValueError):
        rr_level = int(mesh.get("refinement_min", 1))
    geometry_lines = [
        "geometry\n{\n",
        f"    {geom['tri_surface_name']}\n",
        "    {\n",
        "        type triSurfaceMesh;\n",
        f'        file "{stl_name}";\n',
        f"        name {geom['tri_surface_name']};\n",
        "    }\n",
    ]
    if rr_enabled and rr_valid:
        geometry_lines.extend(
            [
                "\n    refinementBox\n",
                "    {\n",
                "        type searchableBox;\n",
                f"        min ({_fmt_float(rr_min[0])} {_fmt_float(rr_min[1])} {_fmt_float(rr_min[2])});\n",
                f"        max ({_fmt_float(rr_max[0])} {_fmt_float(rr_max[1])} {_fmt_float(rr_max[2])});\n",
                "    }\n",
            ]
        )
    geometry_lines.append("};\n\n")
    geometry_block = "".join(geometry_lines)
    refinement_regions = ["    refinementRegions\n", "    {\n"]
    if rr_enabled and rr_valid:
        refinement_regions.extend(
            [
                "        refinementBox\n",
                "        {\n",
                "            mode inside;\n",
                f"            levels ((1E15 {int(rr_level)}));\n",
                "        }\n",
            ]
        )
    refinement_regions.append("    }\n")
    refinement_regions_block = "".join(refinement_regions)
    return (
        _foam_header("dictionary", "snappyHexMeshDict")
        + f"castellatedMesh {_bool_text(mesh['castellated'])};\n"
        + f"snap {_bool_text(mesh['snap'])};\n"
        + f"addLayers {_bool_text(mesh['layers'])};\n\n"
        + geometry_block
        + "castellatedMeshControls\n{\n"
        + f"    maxLocalCells {int(mesh.get('max_local_cells', 100000))};\n"
        + f"    maxGlobalCells {int(mesh.get('max_global_cells', 2000000))};\n"
        + f"    minRefinementCells {int(mesh.get('min_refinement_cells', 10))};\n"
        + f"    maxLoadUnbalance {_fmt_float(mesh.get('max_load_unbalance', 0.10))};\n"
        + "    nCellsBetweenLevels 3;\n"
        + "    features\n"
        + "    (\n"
        + "        {\n"
        + f'            file "{emesh_name}";\n'
        + f"            level {int(mesh['refinement_max'])};\n"
        + "        }\n"
        + "    );\n"
        + "    refinementSurfaces\n"
        + "    {\n"
        + f"        {geom['tri_surface_name']}\n"
        + "        {\n"
        + f"            level ({int(mesh['refinement_min'])} {int(mesh['refinement_max'])});\n"
        + "        }\n"
        + "    }\n"
        + refinement_regions_block
        + "    resolveFeatureAngle "
        + _fmt_float(mesh["feature_angle"])
        + ";\n"
        + f"    locationInMesh ({_fmt_float(loc[0])} {_fmt_float(loc[1])} {_fmt_float(loc[2])});\n"
        + f"    allowFreeStandingZoneFaces {_bool_text(mesh.get('allow_free_standing_zone_faces', True))};\n"
        + "}\n\n"
        + "snapControls\n{\n"
        + "    nSmoothPatch 3;\n"
        + "    tolerance 2.0;\n"
        + "    nSolveIter 30;\n"
        + "    nRelaxIter 5;\n"
        + f"    nFeatureSnapIter {int(mesh.get('n_feature_snap_iter', 10))};\n"
        + f"    implicitFeatureSnap {_bool_text(mesh.get('implicit_feature_snap', False))};\n"
        + f"    explicitFeatureSnap {_bool_text(mesh.get('explicit_feature_snap', True))};\n"
        + f"    multiRegionFeatureSnap {_bool_text(mesh.get('multi_region_feature_snap', False))};\n"
        + "}\n\n"
        + "addLayersControls\n{\n"
        + "    relativeSizes true;\n"
        + "    layers\n"
        + "    {\n"
        + f"        \"{geom['tri_surface_name']}.*\"\n"
        + "        {\n"
        + f"            nSurfaceLayers {int(mesh['n_surface_layers'])};\n"
        + "        }\n"
        + "    }\n"
        + f"    expansionRatio {_fmt_float(mesh.get('expansion_ratio', 1.0))};\n"
        + f"    finalLayerThickness {_fmt_float(mesh.get('final_layer_thickness', 0.3))};\n"
        + f"    minThickness {_fmt_float(mesh.get('min_thickness', 0.1))};\n"
        + f"    nGrow {int(mesh.get('n_grow', 0))};\n"
        + f"    featureAngle {_fmt_float(mesh.get('layer_feature_angle', 60.0))};\n"
        + f"    slipFeatureAngle {_fmt_float(mesh.get('slip_feature_angle', 30.0))};\n"
        + f"    nRelaxIter {int(mesh.get('layer_n_relax_iter', 3))};\n"
        + f"    nSmoothSurfaceNormals {int(mesh.get('n_smooth_surface_normals', 1))};\n"
        + f"    nSmoothNormals {int(mesh.get('n_smooth_normals', 3))};\n"
        + f"    nSmoothThickness {int(mesh.get('n_smooth_thickness', 10))};\n"
        + f"    maxFaceThicknessRatio {_fmt_float(mesh.get('max_face_thickness_ratio', 0.5))};\n"
        + f"    maxThicknessToMedialRatio {_fmt_float(mesh.get('max_thickness_to_medial_ratio', 0.3))};\n"
        + f"    minMedialAxisAngle {_fmt_float(mesh.get('min_medial_axis_angle', 90.0))};\n"
        + f"    nBufferCellsNoExtrude {int(mesh.get('n_buffer_cells_no_extrude', 0))};\n"
        + f"    nLayerIter {int(mesh.get('n_layer_iter', 50))};\n"
        + "}\n\n"
        + "meshQualityControls\n{\n"
        + '    #include "meshQualityDict"\n'
        + "}\n\n"
        + "writeFlags\n"
        + "(\n"
        + "    scalarLevels\n"
        + "    layerSets\n"
        + "    layerFields\n"
        + ");\n\n"
        + f"mergeTolerance {_fmt_float(mesh.get('merge_tolerance', 1e-6))};\n"
    )


def _build_surface_features_dict(stl_name):
    return (
        _foam_header("dictionary", "surfaceFeaturesDict")
        + f'surfaces ("{stl_name}");\n\n'
        + "includedAngle       150;\n\n"
        + "subsetFeatures\n{\n"
        + "    nonManifoldEdges       no;\n"
        + "    openEdges              yes;\n"
        + "}\n"
    )


def _build_surface_feature_extract_dict(stl_name):
    return (
        _foam_header("dictionary", "surfaceFeatureExtractDict")
        + f"{stl_name}\n"
        + "{\n"
        + "    extractionMethod    extractFromSurface;\n"
        + "    includedAngle       150;\n\n"
        + "    subsetFeatures\n"
        + "    {\n"
        + "        nonManifoldEdges       no;\n"
        + "        openEdges              yes;\n"
        + "    }\n\n"
        + "    writeObj                   yes;\n"
        + "}\n"
    )


def _build_control_dict(of_state):
    sim = of_state["simulation"]
    solver = of_state["workflow"]
    return (
        _foam_header("dictionary", "controlDict")
        + f"application     {solver};\n"
        + f"startTime       {_fmt_float(sim['start_time'])};\n"
        + f"endTime         {_fmt_float(sim['end_time'])};\n"
        + f"deltaT          {_fmt_float(sim['delta_t'])};\n"
        + f"writeInterval   {_fmt_float(sim['write_interval'])};\n"
        + f"purgeWrite      {int(sim['purge_write'])};\n"
        + "writeFormat     ascii;\n"
        + "writePrecision  8;\n"
        + "timeFormat      general;\n"
        + "timePrecision   6;\n"
        + "runTimeModifiable true;\n"
    )


def _build_fv_schemes(of_state):
    schemes = _effective_fv_schemes(of_state["numerics"])
    div_line = f"    div(phi,U)      {schemes['div_phi_u']};"
    return (
        _foam_header("dictionary", "fvSchemes")
        + f"ddtSchemes\n{{\n    default         {schemes['ddt_default']};\n}}\n\n"
        + f"gradSchemes\n{{\n    default         {schemes['grad_default']};\n}}\n\n"
        + "divSchemes\n{\n"
        + div_line
        + f"\n    div(phi,k)      {schemes['div_phi_turb']};\n"
        + f"    div(phi,omega)  {schemes['div_phi_turb']};\n"
        + f"    div((nuEff*dev2(T(grad(U))))) {schemes['div_nu_eff_dev2']};\n}}\n\n"
        + f"laplacianSchemes\n{{\n    default         {schemes['laplacian_default']};\n}}\n\n"
        + f"interpolationSchemes\n{{\n    default         {schemes['interpolation_default']};\n}}\n\n"
        + f"snGradSchemes\n{{\n    default         {schemes['sn_grad_default']};\n}}\n"
        + f"\nwallDist\n{{\n    method          {schemes['wall_dist_method']};\n}}\n"
    )


def _build_fv_solution(of_state):
    num = of_state["numerics"]
    sol = _effective_fv_solution(num)
    p_solver = sol["p_solver"]
    u_solver = sol["u_solver"]
    p_smoother = sol.get("p_smoother") or "GaussSeidel"
    u_smoother = sol.get("u_smoother") or "symGaussSeidel"
    u_preconditioner = sol.get("u_preconditioner") or "DILU"
    workflow = str(of_state.get("workflow", "simpleFoam"))
    return (
        _foam_header("dictionary", "fvSolution")
        + "solvers\n{\n"
        + "    p\n    {\n"
        + f"        solver          {p_solver};\n"
        + f"        tolerance       {_fmt_float(num['p_solver_tol'])};\n"
        + f"        relTol          {_fmt_float(sol['p_rel_tol'])};\n"
        + (f"        smoother        {p_smoother};\n" if p_solver in ("GAMG", "smoothSolver") else "")
        + (f"        preconditioner  {sol['p_preconditioner']};\n" if p_solver in ("PCG", "PBiCGStab") else "")
        + "    }\n"
        + "    U\n    {\n"
        + f"        solver          {u_solver};\n"
        + (f"        smoother        {u_smoother};\n" if u_solver == "smoothSolver" else "")
        + (f"        preconditioner  {u_preconditioner};\n" if u_solver in ("PCG", "PBiCGStab") else "")
        + f"        tolerance       {_fmt_float(num['u_solver_tol'])};\n"
        + f"        relTol          {_fmt_float(sol['u_rel_tol'])};\n"
        + "    }\n"
        + (
            "    k\n    {\n"
            + f"        solver          {u_solver};\n"
            + (f"        smoother        {u_smoother};\n" if u_solver == "smoothSolver" else "")
            + (f"        preconditioner  {u_preconditioner};\n" if u_solver in ("PCG", "PBiCGStab") else "")
            + f"        tolerance       {_fmt_float(num['u_solver_tol'])};\n"
            + f"        relTol          {_fmt_float(sol['u_rel_tol'])};\n"
            + "    }\n"
            + "    omega\n    {\n"
            + f"        solver          {u_solver};\n"
            + (f"        smoother        {u_smoother};\n" if u_solver == "smoothSolver" else "")
            + (f"        preconditioner  {u_preconditioner};\n" if u_solver in ("PCG", "PBiCGStab") else "")
            + f"        tolerance       {_fmt_float(num['u_solver_tol'])};\n"
            + f"        relTol          {_fmt_float(sol['u_rel_tol'])};\n"
            + "    }\n"
            if workflow == "simpleFoam"
            else ""
        )
        + "}\n\n"
        + "SIMPLE\n{\n"
        + f"    nNonOrthogonalCorrectors {int(sol['simple_n_non_ortho'])};\n"
        + f"    consistent      {_bool_text(sol['simple_consistent'])};\n"
        + "    residualControl\n    {\n"
        + f"        p               {_fmt_float(sol['residual_control_p'])};\n"
        + f"        U               {_fmt_float(sol['residual_control_u'])};\n"
        + "    }\n"
        + "}\n\n"
        + "relaxationFactors\n{\n"
        + "    fields\n    {\n"
        + f"        p               {_fmt_float(num['p_relax'])};\n"
        + "    }\n"
        + "    equations\n    {\n"
        + f"        U               {_fmt_float(num['u_relax'])};\n"
        + "    }\n"
        + "}\n"
    )


def _build_decompose_par_dict(of_state):
    sim = of_state.get("simulation", {})
    cores = int(sim.get("mpi_cores", 1) or 1)
    if cores < 1:
        cores = 1
    best = (cores, 1, 1)
    best_score = float("inf")
    for nx in range(1, cores + 1):
        if cores % nx != 0:
            continue
        rem = cores // nx
        for ny in range(1, rem + 1):
            if rem % ny != 0:
                continue
            nz = rem // ny
            dims = sorted([nx, ny, nz])
            score = (dims[2] - dims[0]) + (dims[2] - dims[1])
            if score < best_score:
                best_score = score
                best = (nx, ny, nz)
    nx, ny, nz = best
    return (
        _foam_header("dictionary", "decomposeParDict")
        + f"numberOfSubdomains  {cores};\n\n"
        + "method      hierarchical;\n"
        + "distributor     ptscotch;\n"
        + "// distributor     zoltan;\n"
        + '// libs            ("libzoltanDecomp.so");\n\n'
        + "hierarchicalCoeffs\n"
        + "{\n"
        + f"    n               ({nx} {ny} {nz});\n"
        + "    order           xyz;\n"
        + "}\n\n"
        + "zoltanCoeffs\n"
        + "{\n"
        + "    lb_method       hypergraph;\n"
        + "    lb_approach     partition;\n"
        + "}\n"
    )


def _build_mesh_quality_dict(of_state):
    cm = of_state["check_mesh"]
    max_non_ortho = int(float(cm.get("max_non_ortho", 70.0)))
    max_bnd_skew = int(float(cm.get("max_boundary_skewness", 20.0)))
    min_vol = float(cm.get("min_vol", 1.0e-13))
    return (
        _foam_header("dictionary", "meshQualityDict")
        + f"maxNonOrtho {max_non_ortho};\n\n"
        + f"maxBoundarySkewness {max_bnd_skew};\n\n"
        + "maxInternalSkewness 4;\n\n"
        + "maxConcave 80;\n\n"
        + f"minVol {_fmt_float(min_vol)};\n\n"
        + "minTetQuality 1e-15;\n\n"
        + "minArea -1;\n\n"
        + "minTwist 0.02;\n\n"
        + "minDeterminant 0.001;\n\n"
        + "minFaceWeight 0.05;\n\n"
        + "minVolRatio 0.01;\n\n"
        + "minTriangleTwist -1;\n\n"
        + "nSmoothScale 4;\n\n"
        + "errorReduction 0.75;\n\n"
        + "relaxed\n"
        + "{\n"
        + f"    maxNonOrtho {max(75, max_non_ortho)};\n"
        + "}\n"
    )


def _build_create_patch_dict(tri_surface_name):
    name = str(tri_surface_name or "").strip() or "aircraft"
    return (
        _foam_header("dictionary", "createPatchDict")
        + "pointSync false;\n\n"
        + "patches\n"
        + "(\n"
        + "    {\n"
        + f"        name {name};\n"
        + "        patchInfo\n"
        + "        {\n"
        + "            type wall;\n"
        + "            inGroups (wall);\n"
        + "        }\n"
        + "        constructFrom patches;\n"
        + f'        patches ("{name}_.*");\n'
        + "    }\n"
        + ");\n"
    )


def _build_transport_properties():
    return _foam_header("dictionary", "transportProperties") + "transportModel  Newtonian;\nnu [0 2 -1 0 0 0 0] 1.5e-05;\n"


def _build_turbulence_properties(of_state):
    if of_state["workflow"] == "potentialFoam":
        return _foam_header("dictionary", "turbulenceProperties") + "simulationType  laminar;\n"
    model = of_state["numerics"]["turbulence_model"]
    return (
        _foam_header("dictionary", "turbulenceProperties")
        + "simulationType  RAS;\n\n"
        + "RAS\n{\n"
        + f"    RASModel        {model};\n"
        + "    turbulence      on;\n"
        + "    printCoeffs     on;\n"
        + "}\n"
    )


def _field_bc_block(of_state, field):
    bc = of_state["boundary_conditions"]
    dims = FIELD_DIMENSIONS.get(field, "[0 0 0 0 0 0 0]")
    internal = FIELD_INTERNAL_VALUES.get(field, "uniform 0")
    tri_name = str(of_state.get("geometry", {}).get("tri_surface_name", "aircraft")).strip() or "aircraft"
    lines = [f"dimensions      {dims};\n", f"internalField   {internal};\n", "boundaryField\n{\n"]
    for patch in FLOW_PATCHES:
        patch_info = bc["patches"].get(patch, {})
        if not patch_info.get("enabled", True):
            continue
        entry = bc["fields"][field][patch]
        bc_type = str(entry.get("type", "zeroGradient"))
        patch_name = tri_name if patch == "aircraft" else patch
        lines.append(f"    {patch_name}\n")
        lines.append("    {\n")
        lines.append(f"        type            {bc_type};\n")
        value = str(entry.get("value", "")).strip()
        if bc_type == "inletOutlet":
            inlet_value = str(entry.get("inlet_value", "")).strip() or (value if value else internal)
            lines.append(f"        inletValue      {inlet_value};\n")
            outlet_value = value if value else "$internalField"
            lines.append(f"        value           {outlet_value};\n")
        elif value:
            value_key = "freestreamValue" if bc_type in ("freestream", "freestreamPressure") else "value"
            lines.append(f"        {value_key}           {value};\n")
        lines.append("    }\n")
    # Fallback for multi-region STL where snappy names patches aircraft_*.
    if "aircraft" in FLOW_PATCHES and bc["patches"].get("aircraft", {}).get("enabled", True):
        entry = bc["fields"][field]["aircraft"]
        bc_type = str(entry.get("type", "zeroGradient"))
        lines.append(f'    "{tri_name}.*"\n')
        lines.append("    {\n")
        lines.append(f"        type            {bc_type};\n")
        value = str(entry.get("value", "")).strip()
        if bc_type == "inletOutlet":
            inlet_value = str(entry.get("inlet_value", "")).strip() or (value if value else internal)
            lines.append(f"        inletValue      {inlet_value};\n")
            outlet_value = value if value else "$internalField"
            lines.append(f"        value           {outlet_value};\n")
        elif value:
            value_key = "freestreamValue" if bc_type in ("freestream", "freestreamPressure") else "value"
            lines.append(f"        {value_key}           {value};\n")
        lines.append("    }\n")
    lines.append("}\n")
    return "".join(lines)


def build_case_files(of_state):
    stl_path = Path(of_state["geometry"]["stl_path"])
    stl_name = stl_path.name
    files = {
        "system/blockMeshDict": _build_block_mesh_dict(of_state),
        "system/snappyHexMeshDict": _build_snappy_hex_mesh_dict(of_state, stl_name),
        "system/surfaceFeaturesDict": _build_surface_features_dict(stl_name),
        "system/surfaceFeatureExtractDict": _build_surface_feature_extract_dict(stl_name),
        "system/controlDict": _build_control_dict(of_state),
        "system/fvSchemes": _build_fv_schemes(of_state),
        "system/fvSolution": _build_fv_solution(of_state),
        "system/decomposeParDict": _build_decompose_par_dict(of_state),
        "system/meshQualityDict": _build_mesh_quality_dict(of_state),
        "system/createPatchDict": _build_create_patch_dict(of_state["geometry"].get("tri_surface_name", "aircraft")),
        "constant/transportProperties": _build_transport_properties(),
        "constant/turbulenceProperties": _build_turbulence_properties(of_state),
        "0/U": _foam_header("volVectorField", "U") + _field_bc_block(of_state, "U"),
        "0/p": _foam_header("volScalarField", "p") + _field_bc_block(of_state, "p"),
    }
    if of_state["workflow"] == "simpleFoam":
        for field in ("k", "omega", "nut"):
            files[f"0/{field}"] = _foam_header("volScalarField", field) + _field_bc_block(of_state, field)
    return files


def build_run_scripts(of_state):
    scripts = of_state["scripts"]
    solver = of_state["workflow"]
    sim = of_state.get("simulation", {})
    mesh = of_state.get("mesh", {})
    tri_name = str(of_state.get("geometry", {}).get("tri_surface_name", "aircraft")).strip() or "aircraft"
    max_cores = max(1, int(sim.get("mpi_cores", 1) or 1))
    use_parallel = bool(sim.get("use_parallel", False)) and max_cores > 1
    snappy_mode = str(mesh.get("snappy_parallel_mode", "Off")).strip()
    if snappy_mode not in ("Off", "Auto", "On"):
        snappy_mode = "Off"
    include_surface = bool(scripts.get("include_surface_feature_extract", True))
    run_checkmesh = bool(of_state["check_mesh"].get("enabled", True))
    win_bootstrap = _find_windows_openfoam_bootstrap(of_state.get("execution", {}).get("windows_bootstrap", ""))

    unix_lines = [
        "#!/bin/sh",
        "set -e",
        f"MAX_CORES={max_cores}",
        f'SNAPPY_MODE="{snappy_mode}"',
        "MIN_CELLS_PER_CORE=50000",
        "",
        "MPI_LAUNCHER=\"\"",
        "MPI_NP_FLAG=\"-np\"",
        "if command -v mpirun >/dev/null 2>&1; then",
        "    MPI_LAUNCHER=mpirun",
        "elif command -v mpiexec >/dev/null 2>&1; then",
        "    MPI_LAUNCHER=mpiexec",
        "    MPI_NP_FLAG=\"-n\"",
        "fi",
        "",
        "recommend_cores() {",
        "    n_cells=$1",
        "    cores=$(( n_cells / MIN_CELLS_PER_CORE ))",
        "    if [ \"$cores\" -lt 2 ]; then",
        "        echo 1",
        "        return",
        "    fi",
        "    if [ \"$cores\" -gt \"$MAX_CORES\" ]; then",
        "        cores=$MAX_CORES",
        "    fi",
        "    echo \"$cores\"",
        "}",
        "",
        "extract_cells() {",
        "    if [ ! -f \"$1\" ]; then",
        "        echo 0",
        "        return",
        "    fi",
        "    cells=$(grep -E \"cells:[[:space:]]*[0-9]+\" \"$1\" | tail -1 | sed -E 's/.*cells:[[:space:]]*([0-9]+).*/\\1/')",
        "    if [ -z \"$cells\" ]; then",
        "        echo 0",
        "        return",
        "    fi",
        "    echo \"$cells\"",
        "}",
        "",
        "blockMesh",
    ]
    if use_parallel and snappy_mode == "Auto":
        unix_lines.extend(
            [
                "checkMesh -constant | tee log.checkMesh.blockMesh",
                "BCELLS=$(extract_cells log.checkMesh.blockMesh)",
                "SNAPPY_CORES=$(recommend_cores \"$BCELLS\")",
                "echo \"Base mesh cells: $BCELLS | snappy cores (auto): $SNAPPY_CORES\"",
            ]
        )
    elif use_parallel and snappy_mode == "On":
        unix_lines.append("SNAPPY_CORES=$MAX_CORES")
    else:
        unix_lines.append("SNAPPY_CORES=1")
    unix_lines.extend(
        [
            "if [ \"$SNAPPY_CORES\" -ge 2 ] && [ -z \"$MPI_LAUNCHER\" ]; then",
            "    echo \"MPI launcher not found (mpirun/mpiexec). Running snappyHexMesh in serial.\"",
            "    SNAPPY_CORES=1",
            "fi",
        ]
    )
    if include_surface:
        unix_lines.append("surfaceFeatureExtract")
    unix_lines.extend(
        [
            "if [ \"$SNAPPY_CORES\" -ge 2 ]; then",
            "    sed -i -E \"s/^(numberOfSubdomains[[:space:]]+)[0-9]+;/\\1${SNAPPY_CORES};/\" system/decomposeParDict",
            "    decomposePar -force",
            "    $MPI_LAUNCHER $MPI_NP_FLAG \"$SNAPPY_CORES\" snappyHexMesh -overwrite -parallel",
            "    reconstructParMesh -constant",
            "    rm -rf processor*",
            "else",
            "    snappyHexMesh -overwrite",
            "fi",
            f"if grep -q \"{tri_name}_\" constant/polyMesh/boundary; then",
            f"    echo \"Merging {tri_name}_* patches into {tri_name} via createPatch\"",
            "    createPatch -overwrite",
            "fi",
        ]
    )
    if run_checkmesh:
        unix_lines.append("checkMesh -meshQuality | tee log.checkMesh")
    else:
        unix_lines.append("checkMesh | tee log.checkMesh")
    if use_parallel:
        unix_lines.extend(
            [
                "NCELLS=$(extract_cells log.checkMesh)",
                "CORES=$(recommend_cores \"$NCELLS\")",
                "echo \"Mesh cells: $NCELLS | recommended cores: $CORES (max $MAX_CORES)\"",
                "if [ \"$CORES\" -ge 2 ] && [ -z \"$MPI_LAUNCHER\" ]; then",
                "    echo \"MPI launcher not found (mpirun/mpiexec). Running solver in serial.\"",
                "    CORES=1",
                "fi",
                "if [ \"$CORES\" -ge 2 ]; then",
                "    sed -i -E \"s/^(numberOfSubdomains[[:space:]]+)[0-9]+;/\\1${CORES};/\" system/decomposeParDict",
                "    decomposePar -force",
                f"    $MPI_LAUNCHER $MPI_NP_FLAG \"$CORES\" {solver} -parallel",
                "    reconstructPar -latestTime",
                "    rm -rf processor*",
                "else",
                f"    {solver}",
                "fi",
            ]
        )
    else:
        unix_lines.append(solver)

    win_lines = [
        "@echo off",
        "setlocal enabledelayedexpansion",
        'set "SCRIPT_DIR=%~dp0"',
    ]
    if win_bootstrap is not None:
        win_lines.extend(
            [
                f'call "{win_bootstrap}"',
                "if errorlevel 1 exit /b %errorlevel%",
            ]
        )
    win_lines.extend(
        [
            'cd /d "%SCRIPT_DIR%"',
            "if errorlevel 1 exit /b %errorlevel%",
            f"set MAX_CORES={max_cores}",
            f"set SNAPPY_MODE={snappy_mode}",
            "set MPI_LAUNCHER=",
            "set MPI_NP_FLAG=-np",
            "where mpirun >nul 2>&1 && set MPI_LAUNCHER=mpirun",
            "if not defined MPI_LAUNCHER (",
            "  where mpiexec >nul 2>&1 && set MPI_LAUNCHER=mpiexec",
            "  if defined MPI_LAUNCHER set MPI_NP_FLAG=-n",
            ")",
            "blockMesh",
        ]
    )
    if use_parallel and snappy_mode == "Auto":
        win_lines.extend(
            [
                "checkMesh -constant > log.checkMesh.blockMesh 2>&1",
                "for /f \"tokens=2 delims=: \" %%a in ('findstr /R /C:\"cells:[ ]*[0-9][0-9]*\" log.checkMesh.blockMesh') do set BCELLS=%%a",
                "if not defined BCELLS set BCELLS=0",
                "set /a SNAPPY_CORES=BCELLS/50000",
                "if !SNAPPY_CORES! LSS 2 set SNAPPY_CORES=1",
                "if !SNAPPY_CORES! GTR %MAX_CORES% set SNAPPY_CORES=%MAX_CORES%",
                "echo Base mesh cells: !BCELLS! ^| snappy cores (auto): !SNAPPY_CORES!",
            ]
        )
    elif use_parallel and snappy_mode == "On":
        win_lines.append("set SNAPPY_CORES=%MAX_CORES%")
    else:
        win_lines.append("set SNAPPY_CORES=1")
    win_lines.extend(
        [
            "if !SNAPPY_CORES! GEQ 2 if not defined MPI_LAUNCHER (",
            "  echo MPI launcher not found (mpirun/mpiexec). Running snappyHexMesh in serial.",
            "  set SNAPPY_CORES=1",
            ")",
        ]
    )
    if include_surface:
        win_lines.append("surfaceFeatureExtract")
    win_lines.extend(
        [
            "if !SNAPPY_CORES! GEQ 2 (",
            "  powershell -Command \"(Get-Content system/decomposeParDict) -replace '^(numberOfSubdomains\\s+)\\d+;','$1'+$env:SNAPPY_CORES+';' | Set-Content system/decomposeParDict\"",
            "  decomposePar -force",
            "  %MPI_LAUNCHER% %MPI_NP_FLAG% !SNAPPY_CORES! snappyHexMesh -overwrite -parallel",
            "  reconstructParMesh -constant",
            "  for /D %%d in (processor*) do rmdir /S /Q %%d",
            ") else (",
            "  snappyHexMesh -overwrite",
            ")",
        ]
    )
    win_lines.extend(
        [
            f"findstr /R /C:\"{tri_name}_\" constant\\polyMesh\\boundary >nul",
            "if %ERRORLEVEL% EQU 0 (",
            f"  echo Merging {tri_name}_* patches into {tri_name} via createPatch",
            "  createPatch -overwrite",
            ")",
        ]
    )
    if run_checkmesh:
        win_lines.append("checkMesh -meshQuality > log.checkMesh 2>&1")
    else:
        win_lines.append("checkMesh > log.checkMesh 2>&1")
    if use_parallel:
        win_lines.extend(
            [
                "for /f \"tokens=2 delims=: \" %%a in ('findstr /R /C:\"cells:[ ]*[0-9][0-9]*\" log.checkMesh') do set NCELLS=%%a",
                "if not defined NCELLS set NCELLS=0",
                "set /a CORES=NCELLS/50000",
                "if !CORES! LSS 2 set CORES=1",
                "if !CORES! GTR %MAX_CORES% set CORES=%MAX_CORES%",
                "echo Mesh cells: !NCELLS! ^| recommended cores: !CORES! (max %MAX_CORES%)",
                "if !CORES! GEQ 2 if not defined MPI_LAUNCHER (",
                "  echo MPI launcher not found (mpirun/mpiexec). Running solver in serial.",
                "  set CORES=1",
                ")",
                "if !CORES! GEQ 2 (",
                "  powershell -Command \"(Get-Content system/decomposeParDict) -replace '^(numberOfSubdomains\\s+)\\d+;','$1'+$env:CORES+';' | Set-Content system/decomposeParDict\"",
                "  decomposePar -force",
                f"  %MPI_LAUNCHER% %MPI_NP_FLAG% !CORES! {solver} -parallel",
                "  reconstructPar -latestTime",
                "  for /D %%d in (processor*) do rmdir /S /Q %%d",
                ") else (",
                f"  {solver}",
                ")",
            ]
        )
    else:
        win_lines.append(solver)
    unix = "\n".join(unix_lines) + "\n"
    win = "\r\n".join(win_lines) + "\r\n"
    clean_unix = "#!/bin/sh\nrm -rf 0.*/ constant/polyMesh processor*\n"
    clean_win = (
        "@echo off\r\n"
        "cd /d \"%~dp0\"\r\n"
        "if errorlevel 1 exit /b %errorlevel%\r\n"
        "rmdir /S /Q constant\\polyMesh 2>nul\r\n"
        "for /D %%d in (processor*) do rmdir /S /Q %%d\r\n"
    )
    return {
        scripts.get("allrun", "Allrun"): unix,
        scripts.get("allrun_bat", "Allrun.bat"): win,
        scripts.get("allclean", "Allclean"): clean_unix,
        scripts.get("allclean_bat", "Allclean.bat"): clean_win,
    }



__all__ = ["build_case_files", "build_run_scripts"]
