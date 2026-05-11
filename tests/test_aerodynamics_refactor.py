from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from aerodynamics._controller_common import (
    _parse_convergence_coeffs,
    _parse_convergence_residual,
    _parse_convergence_time,
)
from aerodynamics.execution import ExecutionMixin, execution_stage_names
from aerodynamics.foam_case_files import build_case_files, build_run_scripts
from aerodynamics.foam_case_import import parse_openfoam_case
from aerodynamics.mesh import MeshMixin
from aerodynamics.pressure_io import PressureIOMixin
from aerodynamics.state import default_openfoam_state, ensure_openfoam_state


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_CASE = ROOT / "samples" / "openfoam_case"
CHECK_MESH_LOG = ROOT / "tests" / "fixtures" / "openfoam_case" / "log.check_mesh.txt"


class DummyExecution(ExecutionMixin):
    def __init__(self, case_dir):
        self._case_dir = Path(case_dir)
        self.openfoam = default_openfoam_state()
        self.openfoam["simulation"]["use_parallel"] = True
        self.openfoam["simulation"]["mpi_cores"] = 4
        self.openfoam["mesh"]["snappy_parallel_mode"] = "On"
        self.openfoam["geometry"]["tri_surface_name"] = "aircraft"
        self.export_calls = []
        self.patch_calls = []
        self.logs = []

    def _execution_case_dir(self):
        return self._case_dir

    def _find_mpi_launcher(self):
        return "mpirun", "-np"

    def _append_run_log(self, text):
        self.logs.append(str(text))

    def _queue_create_patch_if_needed(self, case_dir, tri_name, log_path):
        self.patch_calls.append((Path(case_dir), tri_name, Path(log_path)))
        return None

    def export_openfoam_case(self, case_dir):
        self.export_calls.append(Path(case_dir))
        return case_dir

    def _parse_force_coeffs(self, case_dir):
        return {"case_dir": str(case_dir)}


class DummyMesh(MeshMixin):
    def __init__(self):
        self.openfoam = {
            "check_mesh": {
                "max_non_ortho": 70.0,
                "max_boundary_skewness": 20.0,
                "min_vol": 1.0e-13,
            }
        }


class DummyPressure(PressureIOMixin):
    def __init__(self):
        self.state = {"aerodynamics": {}}


class TestStateNormalization(unittest.TestCase):
    def test_ensure_openfoam_state_derives_surface_name_and_solver_defaults(self):
        aero_state = {
            "openfoam": {
                "geometry": {"stl_path": "C:/tmp/My Plane.stl"},
                "numerics": {"fv_solution": {"p_solver": "GAMG", "u_solver": "smoothSolver"}},
            }
        }

        of_state = ensure_openfoam_state(aero_state)

        self.assertEqual(of_state["geometry"]["tri_surface_name"], "My_Plane")
        self.assertEqual(of_state["numerics"]["fv_solution"]["p_smoother"], "GaussSeidel")
        self.assertEqual(of_state["numerics"]["fv_solution"]["u_smoother"], "symGaussSeidel")
        self.assertIn("aircraft", of_state["boundary_conditions"]["fields"]["U"])


class TestCaseImportAndBuilders(unittest.TestCase):
    def test_parse_openfoam_case_reads_sample_case(self):
        of_state, warnings = parse_openfoam_case(SAMPLE_CASE)

        self.assertEqual(warnings, [])
        self.assertEqual(of_state["workflow"], "simpleFoam")
        self.assertEqual(of_state["geometry"]["tri_surface_name"], "aircraft")
        self.assertEqual(Path(of_state["geometry"]["stl_path"]).name, "aircraft.stl")
        self.assertTrue(of_state["simulation"]["use_parallel"])
        self.assertEqual(of_state["simulation"]["mpi_cores"], 4)

    def test_case_file_and_script_builders_emit_expected_outputs(self):
        of_state = default_openfoam_state()
        of_state["geometry"]["stl_path"] = "constant/geometry/aircraft.stl"
        of_state["geometry"]["tri_surface_name"] = "aircraft"
        of_state["simulation"]["use_parallel"] = True
        of_state["simulation"]["mpi_cores"] = 4
        of_state["mesh"]["snappy_parallel_mode"] = "On"

        files = build_case_files(of_state)
        scripts = build_run_scripts(of_state)

        self.assertIn("system/controlDict", files)
        self.assertIn("system/snappyHexMeshDict", files)
        self.assertIn("0/U", files)
        self.assertIn("0/k", files)
        self.assertIn("aircraft.stl", files["system/snappyHexMeshDict"])
        self.assertEqual(sorted(scripts), ["Allclean", "Allclean.bat", "Allrun", "Allrun.bat"])
        self.assertIn("MAX_CORES=4", scripts["Allrun"])
        self.assertIn("SNAPPY_MODE=\"On\"", scripts["Allrun"])
        self.assertIn("simpleFoam", scripts["Allrun"])


class TestExecutionPlanning(unittest.TestCase):
    def test_execution_stage_names_are_stable(self):
        self.assertEqual(
            execution_stage_names(),
            ["surfaceFeatureExtract", "blockMesh", "snappyHexMesh", "checkMesh", "simpleFoam"],
        )

    def test_parallel_snappy_stage_keeps_callable_patch_step(self):
        with TemporaryDirectory() as tmpdir:
            runner = DummyExecution(tmpdir)

            commands = runner._build_stage_commands("snappy_mesh", Path(tmpdir))

        self.assertEqual(commands[0]["cmd"], ["decomposePar", "-force"])
        self.assertEqual(commands[1]["cmd"], ["mpirun", "-np", "4", "snappyHexMesh", "-overwrite", "-parallel"])
        self.assertEqual(commands[2]["cmd"], ["reconstructParMesh", "-constant"])
        self.assertEqual(commands[3]["kind"], "callable")
        commands[3]["fn"]()
        self.assertEqual(len(runner.patch_calls), 1)
        self.assertEqual(runner.patch_calls[0][1], "aircraft")

    def test_execution_plan_inserts_generate_and_preserves_callable_entries(self):
        with TemporaryDirectory() as tmpdir:
            runner = DummyExecution(tmpdir)

            case_dir, plan = runner._build_execution_plan(["snappy_mesh", "post"])

        self.assertEqual(case_dir, Path(tmpdir))
        self.assertEqual(plan[0]["stage"], "generate")
        self.assertEqual(plan[0]["kind"], "callable")
        self.assertTrue(any(entry["stage"] == "snappy_mesh" and entry["kind"] == "callable" for entry in plan))
        self.assertEqual(plan[-1]["stage"], "post")
        self.assertEqual(plan[-1]["kind"], "callable")


class TestMeshAndPressureParsing(unittest.TestCase):
    def test_check_mesh_report_parser_reads_sample_log(self):
        mesh = DummyMesh()

        report = mesh._parse_check_mesh_report(CHECK_MESH_LOG)

        self.assertIsNotNone(report)
        self.assertTrue(report["has_violations"])
        self.assertEqual(report["failed_checks"], 2)
        self.assertAlmostEqual(report["metrics"]["max_non_ortho"], 0.0)
        self.assertAlmostEqual(report["metrics"]["min_volume"], 0.29296875)

    def test_convergence_parsers_extract_time_residuals_and_coefficients(self):
        self.assertEqual(_parse_convergence_time("Time = 42"), 42.0)
        self.assertEqual(
            _parse_convergence_residual(
                "smoothSolver: Solving for Ux, Initial residual = 0.00123, Final residual = 1e-06, No Iterations 2"
            ),
            ("Ux", 0.00123),
        )
        self.assertEqual(_parse_convergence_coeffs("Cd = 0.12 Cl = 0.34 Cm = -0.01"), (0.12, 0.34, -0.01))

    def test_pressure_csv_parser_and_state_persistence(self):
        pressure = DummyPressure()
        csv_text = (
            "Points:0,Points:1,Points:2,Cp,U:0,U:1,U:2,wallShearStress:0,wallShearStress:1,wallShearStress:2\n"
            "0.0,1.0,2.0,0.5,3.0,4.0,0.0,1.0,2.0,2.0\n"
        )

        with TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "pressure.csv"
            csv_path.write_text(csv_text, encoding="utf-8")
            data = pressure._parse_pressure_csv(csv_path)

        self.assertEqual(data["point_count"], 1)
        self.assertEqual(data["field_order"][0], "cp")
        self.assertAlmostEqual(data["fields"]["u_mag"][0], 5.0)
        self.assertAlmostEqual(data["fields"]["wall_shear_mag"][0], 3.0)

        pressure._save_pressure_state(data, "cp")

        aero_state = pressure.state["aerodynamics"]
        self.assertEqual(aero_state["pressure_meta"]["selected_field"], "cp")
        self.assertEqual(aero_state["pressure_meta"]["point_count"], 1)
        self.assertEqual(aero_state["pressure_data"]["fields"]["cp"], [0.5])
        self.assertEqual(aero_state["pressure_data"]["fields"]["u_mag"], [5.0])


if __name__ == "__main__":
    unittest.main()
