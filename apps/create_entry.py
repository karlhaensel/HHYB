"""App to create new diary entries."""

from apps.core import SubApp
from models.menu import MenuHandler, MenuItem
from protocols.apps import AppProtocol

_CREATE_ENTRY_MENU_HANDLER = MenuHandler(
    menu_items=[
        MenuItem(
            menu_id=0,
            description="Create entry for today.",
            call_attr="create_for_today",
        ),
        MenuItem(
            menu_id=1,
            description="Create entry for past date.",
            call_attr="create_for_past_date",
        ),
        MenuItem(menu_id=2, description="Exit to main menu", call_attr="exit"),
    ]
)


class CreateEntryApp(SubApp):
    """App to create diary entries."""

    def __init__(self, app_handler: AppProtocol) -> None:
        """Initialise the app."""
        super().__init__(
            app_name="Create Diary Entry",
            app_handler=app_handler,
            always_exit_to_handler=True,
        )

    @property
    def menu_handler(self) -> MenuHandler:
        """Get the menu handler for the app."""
        return _CREATE_ENTRY_MENU_HANDLER

    def _run(self) -> None:
        """Run the app."""
        self.menu_handler.run(self)

    def _exit_to_app_handler(self) -> None:
        """Exit the app."""
        # Nothing to do as of now, but possibly TODO
        pass

    def _prepare_for_final_exit(self) -> None:
        """Prepare the app for final exit."""
        # Will not happen.
        pass

    def create_for_today(self) -> None:
        """Create an entry for today."""
        # TODO: Implement create_for_today
        print("Creating entry for today...")
        self.menu_handler.run(self)

    def create_for_past_date(self) -> None:
        """Create an entry for past date."""
        # TODO: Implement create_for_past_date
        print("Creating entry for past date...")
        self.menu_handler.run(self)
