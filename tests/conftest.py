"""Conftest for global fixtures etc."""

import pytest

from apps.core import SubApp, ConsoleApp
from models.menu import MenuItem, MenuHandler


@pytest.fixture
def test_menu_item_test_method() -> MenuItem:
    """Create a menu item for calling the test method."""
    return MenuItem(menu_id=0, description="Test method.", call_attr="_test_method")


@pytest.fixture
def test_menu_item_other_test_method() -> MenuItem:
    """Create a menu item for calling the other test method."""
    return MenuItem(
        menu_id=1, description="Other test method.", call_attr="other_test_method"
    )


@pytest.fixture
def test_menu_item_exit() -> MenuItem:
    """Create a menu item for calling the exit method."""
    return MenuItem(menu_id=2, description="Exit this app.", call_attr="exit")


@pytest.fixture
def test_menu_handler(
    test_menu_item_test_method: MenuItem,
    test_menu_item_other_test_method: MenuItem,
    test_menu_item_exit: MenuItem,
) -> MenuHandler:
    """Create a test menu handler."""
    return MenuHandler(
        menu_items=[
            test_menu_item_test_method,
            test_menu_item_other_test_method,
            test_menu_item_exit,
        ],
    )


@pytest.fixture
def test_app_cls(test_menu_handler: MenuHandler):
    """Return TestApp class."""

    class TestApp(SubApp):
        """Class for testing console apps."""

        def __init__(
            self, app_handler: ConsoleApp | None, always_exit_to_handler: bool
        ) -> None:
            """Initialise test console app."""
            super().__init__("Test App", app_handler, always_exit_to_handler)

        @property
        def menu_handler(self) -> MenuHandler:
            """Return the menu handler for the test app."""
            return test_menu_handler

        def _run(self) -> None:
            """Run the test console app."""
            self.menu_handler.run(self)

        def _exit_to_app_handler(self) -> None:
            """Exit the calling app."""
            if not self.always_exit_to_handler:
                raise ValueError(
                    "Cannot exit to app handler because always_exit_to_handler==False."
                )
            print("Exit to calling app.")

        def _prepare_for_final_exit(self) -> None:
            """Prepare for final exit."""
            print("Saving everything important and stuff.")

        def _test_method(self) -> None:
            """Just some test method."""
            print(f"Running _test_method for {self.__class__.__name__}.")

        def other_test_method(self) -> None:
            """Just some other test method."""
            print(f"Running other_test_method for {self.__class__.__name__}.")

    return TestApp


@pytest.fixture
def test_calling_app_instance(test_app_cls) -> ConsoleApp:
    """Return instance of TestApp with no calling app."""
    return test_app_cls(None, False)


@pytest.fixture
def test_app_getting_called_returning_to_calling_app(
    test_app_cls,
    test_calling_app_instance,
) -> ConsoleApp:
    """Return instance of TestApp with calling app, existing to calling app."""
    return test_app_cls(test_calling_app_instance, True)


@pytest.fixture
def test_app_getting_called_returning_to_exit(
    test_app_cls,
    test_calling_app_instance,
) -> ConsoleApp:
    """Return instance of TestApp with calling app, not existing to calling app."""
    return test_app_cls(test_calling_app_instance, False)
