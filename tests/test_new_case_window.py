from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from aerodynamics_app.new_case_window import (
    copy_tutorial_case,
    resolve_tutorial_manifest,
    validate_tutorial_destination,
)
from aerodynamics_app.workspace_state import load_workspace_payload, record_recent_case, save_workspace_payload


def _write_case_stub(case_dir: Path):
    (case_dir / "system").mkdir(parents=True, exist_ok=True)
    (case_dir / "system" / "controlDict").write_text("application simpleFoam;\n", encoding="utf-8")


class TestNewCaseWindowHelpers(unittest.TestCase):
    def test_resolve_tutorial_manifest_filters_missing_entries(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_case_stub(root / "samples" / "openfoam_case")
            _write_case_stub(
                root
                / "vendor"
                / "openfoam"
                / "v2412"
                / "msys64"
                / "home"
                / "ofuser"
                / "OpenFOAM"
                / "OpenFOAM-v2412"
                / "tutorials"
                / "incompressible"
                / "simpleFoam"
                / "airFoil2D"
            )

            entries = resolve_tutorial_manifest(root)

        ids = [entry["id"] for entry in entries]
        self.assertEqual(ids, ["bundled_aircraft_sample", "airfoil_2d"])

    def test_recent_case_persistence_prunes_missing_paths(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prefs_path = root / ".ad_gui_preferences.json"
            case_a = root / "case_a"
            case_b = root / "case_b"
            case_a.mkdir()
            case_b.mkdir()

            recent = []
            recent = record_recent_case(recent, case_a, label="Case A")
            recent = record_recent_case(recent, case_b, label="Case B", source_kind="tutorial", template_id="airfoil_2d")
            recent.append({"path": str(root / "missing_case"), "label": "Missing"})

            save_workspace_payload(
                prefs_path,
                settings={"general": {"dark_mode": True}},
                workspace={"recent_cases": recent},
            )
            payload = load_workspace_payload(prefs_path)

        self.assertEqual(payload["settings"]["general"]["dark_mode"], True)
        self.assertEqual(len(payload["workspace"]["recent_cases"]), 2)
        self.assertEqual(payload["workspace"]["recent_cases"][0]["label"], "Case B")
        self.assertEqual(payload["workspace"]["recent_cases"][0]["template_id"], "airfoil_2d")

    def test_copy_tutorial_case_sanitizes_generated_artifacts(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "source_case"
            target = root / "copied_case"
            _write_case_stub(source)
            (source / "0").mkdir()
            (source / "50").mkdir()
            (source / "constant").mkdir()
            (source / "processor0").mkdir()
            (source / "postProcessing").mkdir()
            (source / "VTK").mkdir()
            (source / ".ad_gui_runtime").mkdir()
            (source / "Allrun").write_text("#!/bin/sh\n", encoding="utf-8")
            (source / "Allclean").write_text("#!/bin/sh\n", encoding="utf-8")
            (source / "log.solve.txt").write_text("solver log\n", encoding="utf-8")
            (source / "result.foam").write_text("foam\n", encoding="utf-8")

            copy_tutorial_case(source, target)

            self.assertTrue((target / "system" / "controlDict").is_file())
            self.assertTrue((target / "0").is_dir())
            self.assertTrue((target / "constant").is_dir())
            self.assertTrue((target / "Allrun").is_file())
            self.assertTrue((target / "Allclean").is_file())
            self.assertFalse((target / "50").exists())
            self.assertFalse((target / "processor0").exists())
            self.assertFalse((target / "postProcessing").exists())
            self.assertFalse((target / "VTK").exists())
            self.assertFalse((target / ".ad_gui_runtime").exists())
            self.assertFalse((target / "log.solve.txt").exists())
            self.assertFalse((target / "result.foam").exists())

    def test_validate_tutorial_destination_rejects_existing_nonempty_target(self):
        with TemporaryDirectory() as tmpdir:
            parent = Path(tmpdir)
            target = parent / "Simple Car"
            target.mkdir()
            (target / "placeholder.txt").write_text("x", encoding="utf-8")

            resolved, error = validate_tutorial_destination(parent, "Simple Car")

        self.assertIsNone(resolved)
        self.assertIn("already exists", error)


if __name__ == "__main__":
    unittest.main()
