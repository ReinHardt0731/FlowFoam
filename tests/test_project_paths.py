from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from project_paths import PROJECT_ROOT, WORKSPACE_CASES_DIR, default_workspace_case_dir


class TestProjectPaths(unittest.TestCase):
    def test_project_root_is_stable(self):
        self.assertEqual(PROJECT_ROOT, ROOT)

    def test_default_workspace_case_dir_lives_under_workspace_cases(self):
        case_dir = default_workspace_case_dir("demo_case")
        self.assertEqual(case_dir, WORKSPACE_CASES_DIR / "demo_case")
        self.assertEqual(case_dir.parent, WORKSPACE_CASES_DIR)


if __name__ == "__main__":
    unittest.main()
