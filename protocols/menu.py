"""Protocol for menu handling in HHYB."""

from typing import Protocol

from protocols.apps import AppProtocol


class MenuItemProtocol(Protocol):
    """Protocol for menu items in HHYB."""

    menu_id: int
    description: str
    call_attr: str

    def check_call_attr_for_app_object(self, app: AppProtocol) -> None:
        """Check if the call_attr is a valid attribute of the app class."""
        ...

    def run_call(self, app: AppProtocol) -> None:
        """Run the call_attr method of the app class."""
        ...


class MenuHandlerProtocol(Protocol):
    """Protocol for menu handling in HHYB."""

    menu_items: list[MenuItemProtocol]

    @property
    def items(self) -> dict[int, MenuItemProtocol]:
        """Return the menu items as a dictionary."""
        ...

    def check_app_has_attrs(self, app: AppProtocol) -> None:
        """Check if given app has all menu items call attributes."""
        ...

    def run(self, app: AppProtocol) -> None:
        """Run the menu (print and listen for commands)."""
        ...
