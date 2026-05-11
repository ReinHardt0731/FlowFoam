from .boundary_conditions import BoundaryConditionMixin
from .case_management import CaseManagementMixin
from .controller_core import AerodynamicsTabCoreMixin
from .execution import ExecutionMixin
from .mesh import MeshMixin
from .post_process import PostProcessMixin
from .pressure_io import PressureIOMixin
from .ui_panels import UIPanelMixin
from .viewer import ViewerMixin


class AerodynamicsTab(
    AerodynamicsTabCoreMixin,
    UIPanelMixin,
    PressureIOMixin,
    CaseManagementMixin,
    PostProcessMixin,
    ExecutionMixin,
    MeshMixin,
    BoundaryConditionMixin,
    ViewerMixin,
):
    pass


__all__ = ["AerodynamicsTab"]
