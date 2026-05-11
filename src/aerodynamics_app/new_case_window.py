from __future__ import annotations

from pathlib import Path
import re
import shutil

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from project_paths import OPENFOAM_WINDOWS_V2412_DIR, PROJECT_ROOT


CURATED_TUTORIALS = [
    {
        "id": "bundled_aircraft_sample",
        "title": "Bundled Aircraft Sample",
        "description": "The repo sample case used by the current workbench.",
        "solver": "simpleFoam",
        "tags": ["sample", "aircraft", "3D"],
        "source_path": "samples/openfoam_case",
        "source_kind": "repo_sample",
    },
    {
        "id": "airfoil_2d",
        "title": "AirFoil 2D",
        "description": "Bundled simpleFoam tutorial for external aerodynamics around a 2D airfoil.",
        "solver": "simpleFoam",
        "tags": ["airfoil", "2D", "simpleFoam"],
        "source_path": "incompressible/simpleFoam/airFoil2D",
        "source_kind": "bundled_tutorial",
    },
    {
        "id": "cylinder_potential_flow",
        "title": "Cylinder Potential Flow",
        "description": "Bundled potentialFoam tutorial for a simple inviscid cylinder case.",
        "solver": "potentialFoam",
        "tags": ["cylinder", "2D", "potentialFoam"],
        "source_path": "basic/potentialFoam/cylinder",
        "source_kind": "bundled_tutorial",
    },
    {
        "id": "simple_car",
        "title": "Simple Car",
        "description": "Bundled simpleFoam tutorial for an automotive external-flow setup.",
        "solver": "simpleFoam",
        "tags": ["car", "3D", "simpleFoam"],
        "source_path": "incompressible/simpleFoam/simpleCar",
        "source_kind": "bundled_tutorial",
    },
]


def sanitize_case_name(name: str) -> str:
    text = re.sub(r'[<>:"/\\|?*]+', "_", str(name or "").strip())
    text = re.sub(r"\s+", " ", text).strip(" .")
    return text


def bundled_tutorial_root(root: Path | None = None) -> Path:
    project_root = Path(root or PROJECT_ROOT)
    vendor_root = project_root / "vendor" / "openfoam" / "v2412"
    if root is None:
        vendor_root = OPENFOAM_WINDOWS_V2412_DIR
    return (
        vendor_root
        / "msys64"
        / "home"
        / "ofuser"
        / "OpenFOAM"
        / "OpenFOAM-v2412"
        / "tutorials"
    )


def resolve_tutorial_manifest(root: Path | None = None) -> list[dict]:
    project_root = Path(root or PROJECT_ROOT)
    tutorial_root = bundled_tutorial_root(project_root)
    tutorials = []
    for item in CURATED_TUTORIALS:
        resolved = (
            project_root / item["source_path"]
            if item["source_kind"] == "repo_sample"
            else tutorial_root / item["source_path"]
        )
        if not resolved.is_dir():
            continue
        if not (resolved / "system" / "controlDict").is_file():
            continue
        entry = dict(item)
        entry["source_path"] = str(resolved)
        tutorials.append(entry)
    return tutorials


def validate_tutorial_destination(destination_parent: str | Path, case_name: str) -> tuple[Path | None, str | None]:
    parent = Path(destination_parent)
    if not parent.exists() or not parent.is_dir():
        return None, "Choose an existing destination folder."
    safe_name = sanitize_case_name(case_name)
    if not safe_name:
        return None, "Case name is required."
    target = parent / safe_name
    if target.exists():
        if target.is_file():
            return None, f"Target path already exists as a file:\n{target}"
        return None, f"Target folder already exists:\n{target}"
    return target, None


def _is_numeric_time_dir(name: str) -> bool:
    try:
        return float(str(name)) >= 0.0
    except Exception:
        return False


def _ignore_case_entries(directory: str, names: list[str]) -> set[str]:
    ignored = set()
    base = Path(directory)
    for name in names:
        child = base / name
        if child.is_dir():
            if name.startswith("processor") or name in {"postProcessing", ".ad_gui_runtime"}:
                ignored.add(name)
                continue
            if name.startswith("VTK"):
                ignored.add(name)
                continue
            if _is_numeric_time_dir(name) and name != "0":
                ignored.add(name)
                continue
        if child.is_file():
            if name.startswith("log") or child.suffix.lower() == ".foam":
                ignored.add(name)
    return ignored


def copy_tutorial_case(source_dir: str | Path, target_dir: str | Path) -> Path:
    source = Path(source_dir)
    target = Path(target_dir)
    if not source.is_dir():
        raise FileNotFoundError(f"Tutorial source not found:\n{source}")
    if target.exists():
        if target.is_file():
            raise FileExistsError(f"Target already exists as a file:\n{target}")
        if any(target.iterdir()):
            raise FileExistsError(f"Target folder already exists and is not empty:\n{target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, ignore=_ignore_case_entries)
    return target


class NewCaseWindow(QDialog):
    open_existing_requested = Signal()
    open_recent_requested = Signal(str)
    create_tutorial_requested = Signal(str, str, str)

    def __init__(
        self,
        parent=None,
        *,
        tutorials: list[dict] | None = None,
        recent_cases: list[dict] | None = None,
        default_parent: str | Path = "",
        required_root: str | Path = "",
    ):
        super().__init__(parent)
        self.setWindowTitle("New File")
        self.setMinimumSize(900, 580)
        self.setModal(True)
        self._tutorials = list(tutorials or [])
        self._recent_cases = list(recent_cases or [])
        self._default_parent = str(default_parent or "")
        self._required_root = str(required_root or "")
        self._build_ui()
        self.set_tutorials(self._tutorials)
        self.set_recent_cases(self._recent_cases)

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(14)

        nav_frame = QFrame(self)
        nav_frame.setFrameShape(QFrame.StyledPanel)
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(10, 10, 10, 10)
        nav_layout.setSpacing(8)

        title = QLabel("Case Launcher", nav_frame)
        title.setStyleSheet("font-size: 16px; font-weight: 600;")
        nav_layout.addWidget(title)

        self.nav_list = QListWidget(nav_frame)
        for label in ("Home", "New", "Open"):
            self.nav_list.addItem(label)
        self.nav_list.currentRowChanged.connect(self._on_nav_changed)
        nav_layout.addWidget(self.nav_list, 1)
        root.addWidget(nav_frame, 0)

        self.pages = QStackedWidget(self)
        root.addWidget(self.pages, 1)

        self.pages.addWidget(self._build_home_page())
        self.pages.addWidget(self._build_new_page())
        self.pages.addWidget(self._build_open_page())
        self.nav_list.setCurrentRow(0)

    def _build_home_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        heading = QLabel("Recent Cases", page)
        heading.setStyleSheet("font-size: 15px; font-weight: 600;")
        layout.addWidget(heading)

        self.home_recent_list = QListWidget(page)
        self.home_recent_list.itemDoubleClicked.connect(self._open_selected_recent_from_home)
        layout.addWidget(self.home_recent_list, 1)

        home_buttons = QHBoxLayout()
        btn_open_recent = QPushButton("Open Selected", page)
        btn_open_recent.clicked.connect(self._open_selected_recent_from_home)
        btn_go_open = QPushButton("Open Existing...", page)
        btn_go_open.clicked.connect(lambda: self.nav_list.setCurrentRow(2))
        home_buttons.addWidget(btn_open_recent)
        home_buttons.addWidget(btn_go_open)
        home_buttons.addStretch(1)
        layout.addLayout(home_buttons)

        tutorial_heading = QLabel("Tutorial Cases", page)
        tutorial_heading.setStyleSheet("font-size: 15px; font-weight: 600;")
        layout.addWidget(tutorial_heading)

        self.home_tutorial_list = QListWidget(page)
        self.home_tutorial_list.itemDoubleClicked.connect(self._use_selected_home_tutorial)
        layout.addWidget(self.home_tutorial_list, 1)

        btn_use_tutorial = QPushButton("Use Selected Tutorial", page)
        btn_use_tutorial.clicked.connect(self._use_selected_home_tutorial)
        layout.addWidget(btn_use_tutorial, 0, Qt.AlignLeft)
        return page

    def _build_new_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        heading = QLabel("Tutorial Cases", page)
        heading.setStyleSheet("font-size: 15px; font-weight: 600;")
        layout.addWidget(heading)

        self.new_tutorial_list = QListWidget(page)
        self.new_tutorial_list.currentRowChanged.connect(self._on_tutorial_selection_changed)
        layout.addWidget(self.new_tutorial_list, 1)

        self.lbl_tutorial_title = QLabel("", page)
        self.lbl_tutorial_title.setStyleSheet("font-size: 14px; font-weight: 600;")
        self.lbl_tutorial_description = QLabel("", page)
        self.lbl_tutorial_description.setWordWrap(True)
        self.lbl_tutorial_meta = QLabel("", page)
        self.lbl_tutorial_meta.setWordWrap(True)
        layout.addWidget(self.lbl_tutorial_title)
        layout.addWidget(self.lbl_tutorial_description)
        layout.addWidget(self.lbl_tutorial_meta)

        form = QFormLayout()
        self.input_case_name = QLineEdit(page)
        form.addRow("Case Name", self.input_case_name)

        dest_row = QHBoxLayout()
        self.input_destination = QLineEdit(page)
        btn_browse = QPushButton("Browse...", page)
        btn_browse.clicked.connect(self._browse_destination)
        dest_row.addWidget(self.input_destination, 1)
        dest_row.addWidget(btn_browse)
        form.addRow("Destination Folder", dest_row)
        layout.addLayout(form)

        self.lbl_required_root = QLabel("", page)
        self.lbl_required_root.setWordWrap(True)
        layout.addWidget(self.lbl_required_root)

        btn_create = QPushButton("Create Tutorial Case", page)
        btn_create.clicked.connect(self._emit_create_tutorial)
        layout.addWidget(btn_create, 0, Qt.AlignLeft)
        return page

    def _build_open_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        heading = QLabel("Open Existing Case Folder", page)
        heading.setStyleSheet("font-size: 15px; font-weight: 600;")
        layout.addWidget(heading)

        btn_open_existing = QPushButton("Open Existing Case Folder...", page)
        btn_open_existing.clicked.connect(self.open_existing_requested.emit)
        layout.addWidget(btn_open_existing, 0, Qt.AlignLeft)

        recent_heading = QLabel("Recent Cases", page)
        recent_heading.setStyleSheet("font-size: 15px; font-weight: 600;")
        layout.addWidget(recent_heading)

        self.open_recent_list = QListWidget(page)
        self.open_recent_list.itemDoubleClicked.connect(self._open_selected_recent_from_open)
        layout.addWidget(self.open_recent_list, 1)

        btn_open_recent = QPushButton("Open Selected Recent Case", page)
        btn_open_recent.clicked.connect(self._open_selected_recent_from_open)
        layout.addWidget(btn_open_recent, 0, Qt.AlignLeft)
        return page

    def set_tutorials(self, tutorials: list[dict]):
        self._tutorials = list(tutorials or [])
        self.home_tutorial_list.clear()
        self.new_tutorial_list.clear()
        for entry in self._tutorials[:4]:
            item = QListWidgetItem(f"{entry['title']}  [{entry['solver']}]", self.home_tutorial_list)
            item.setData(Qt.UserRole, entry["id"])
            item.setToolTip(entry["description"])
        for entry in self._tutorials:
            tags = ", ".join(entry.get("tags", []))
            text = f"{entry['title']}  [{entry['solver']}]"
            if tags:
                text += f"\n{tags}"
            item = QListWidgetItem(text, self.new_tutorial_list)
            item.setData(Qt.UserRole, entry["id"])
            item.setToolTip(entry["description"])
        if self._tutorials:
            self.new_tutorial_list.setCurrentRow(0)
        else:
            self.lbl_tutorial_title.setText("No tutorial templates were found.")
            self.lbl_tutorial_description.setText("")
            self.lbl_tutorial_meta.setText("")
        self._sync_required_root_text()

    def set_recent_cases(self, recent_cases: list[dict]):
        self._recent_cases = list(recent_cases or [])
        self.home_recent_list.clear()
        self.open_recent_list.clear()
        if not self._recent_cases:
            home_item = QListWidgetItem("No recent cases yet.")
            home_item.setFlags(Qt.NoItemFlags)
            open_item = QListWidgetItem("No recent cases yet.")
            open_item.setFlags(Qt.NoItemFlags)
            self.home_recent_list.addItem(home_item)
            self.open_recent_list.addItem(open_item)
            return
        for entry in self._recent_cases:
            label = entry.get("label", Path(entry["path"]).name)
            source_kind = entry.get("source_kind", "opened")
            text = f"{label}\n{entry['path']}  [{source_kind}]"
            home_item = QListWidgetItem(text, self.home_recent_list)
            home_item.setData(Qt.UserRole, entry["path"])
            open_item = QListWidgetItem(text, self.open_recent_list)
            open_item.setData(Qt.UserRole, entry["path"])

    def set_default_parent(self, default_parent: str | Path):
        self._default_parent = str(default_parent or "")
        if not self.input_destination.text().strip():
            self.input_destination.setText(self._default_parent)

    def _sync_required_root_text(self):
        root_text = str(self._required_root or "").strip()
        if root_text:
            self.lbl_required_root.setText(f"Working copies must be created under:\n{root_text}")
        else:
            self.lbl_required_root.setText("")
        if not self.input_destination.text().strip():
            self.input_destination.setText(self._default_parent or root_text)

    def _on_nav_changed(self, row: int):
        self.pages.setCurrentIndex(max(0, min(row, self.pages.count() - 1)))

    def _tutorial_by_id(self, tutorial_id: str) -> dict | None:
        for entry in self._tutorials:
            if entry["id"] == tutorial_id:
                return entry
        return None

    def _current_selected_tutorial(self) -> dict | None:
        item = self.new_tutorial_list.currentItem()
        if item is None:
            return None
        return self._tutorial_by_id(str(item.data(Qt.UserRole)))

    def _on_tutorial_selection_changed(self, _row: int):
        entry = self._current_selected_tutorial()
        if entry is None:
            return
        self.lbl_tutorial_title.setText(entry["title"])
        self.lbl_tutorial_description.setText(entry["description"])
        tags = ", ".join(entry.get("tags", []))
        meta = [f"Solver: {entry['solver']}"]
        if tags:
            meta.append(f"Tags: {tags}")
        meta.append(f"Template Path: {entry['source_path']}")
        self.lbl_tutorial_meta.setText("\n".join(meta))
        if not self.input_case_name.text().strip():
            self.input_case_name.setText(sanitize_case_name(entry["title"]))
        if not self.input_destination.text().strip():
            self.input_destination.setText(self._default_parent or self._required_root)

    def _browse_destination(self):
        start_dir = self.input_destination.text().strip() or self._default_parent or self._required_root
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder", start_dir)
        if folder:
            self.input_destination.setText(folder)

    def _emit_create_tutorial(self):
        entry = self._current_selected_tutorial()
        if entry is None:
            QMessageBox.warning(self, "New File", "Select a tutorial case first.")
            return
        case_name = self.input_case_name.text().strip()
        destination_parent = self.input_destination.text().strip()
        self.create_tutorial_requested.emit(entry["id"], case_name, destination_parent)

    def _use_selected_home_tutorial(self):
        item = self.home_tutorial_list.currentItem()
        if item is None:
            return
        tutorial_id = str(item.data(Qt.UserRole))
        for idx in range(self.new_tutorial_list.count()):
            row_item = self.new_tutorial_list.item(idx)
            if str(row_item.data(Qt.UserRole)) == tutorial_id:
                self.new_tutorial_list.setCurrentRow(idx)
                break
        self.nav_list.setCurrentRow(1)

    def _emit_recent_open(self, widget: QListWidget):
        item = widget.currentItem()
        if item is None:
            return
        path = str(item.data(Qt.UserRole) or "").strip()
        if not path:
            return
        self.open_recent_requested.emit(path)

    def _open_selected_recent_from_home(self, *_args):
        self._emit_recent_open(self.home_recent_list)

    def _open_selected_recent_from_open(self, *_args):
        self._emit_recent_open(self.open_recent_list)
