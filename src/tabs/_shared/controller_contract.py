from typing import Protocol, runtime_checkable


TAB_CONTROLLER_METHODS = (
    "get_model",
    "sync_from_state",
    "on_tree_selection_changed",
    "set_task_controls_visible",
)


@runtime_checkable
class TabControllerProtocol(Protocol):
    def get_model(self):
        ...

    def sync_from_state(self):
        ...

    def on_tree_selection_changed(self, path):
        ...

    def set_task_controls_visible(self, visible):
        ...


def supports_tab_controller_contract(obj) -> bool:
    return all(callable(getattr(obj, name, None)) for name in TAB_CONTROLLER_METHODS)
