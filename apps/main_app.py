"""Main menu for HHYB."""

from apps.core import ConsoleApp
from apps.create_entry import CreateEntryApp
from models.menu import MenuHandler, MenuItem

_MAIN_MENU_HANDLER = MenuHandler(
    menu_items=[
        MenuItem(
            menu_id=0, description="Create Diary Entry.", call_attr="create_entry"
        ),
        MenuItem(menu_id=1, description="Exit HHYB.", call_attr="exit"),
    ]
)


class MainApp(ConsoleApp):
    """Main menu for HHYB."""

    _MENU_METHODS_WITHOUT_EXIT = ("create_entry",)

    def __init__(self) -> None:
        """Initialise the main menu app."""
        super().__init__(app_name="Main Menu")
        self.create_entry_app = CreateEntryApp(app_handler=self)

    @property
    def menu_handler(self) -> MenuHandler:
        """Return the menu handler for the main menu app."""
        return _MAIN_MENU_HANDLER

    def _run(self) -> None:
        """Run the main menu app."""
        self.menu_handler.run(self)

    def _prepare_for_final_exit(self) -> None:
        """Prepare the main menu app for final exit."""
        # TODO: add DataHandler.save() or sth similar
        pass

    def create_entry(self):
        """Call the app to create an entry for the diary."""
        self.create_entry_app.run()
