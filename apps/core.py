"""Core functionality for apps in HHYB."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod

from pydantic import BaseModel, Field, field_validator


class MenuItem(BaseModel):
    """Menu Item class for console apps."""

    menu_id: int = Field(ge=0)
    description: str
    call_attr: str = Field(pattern="^[a-z_]+$")

    def check_call_attr_for_app_object(self, app: ConsoleApp) -> None:
        """Check if the call_attr is a valid attribute of the app class."""
        if not hasattr(app, self.call_attr):
            raise ValueError(
                f"MenuItem {self} does not have a valid call attribute for class "
                f"{app.__class__.__name__}."
            )

    def run_call(self, app: ConsoleApp) -> None:
        """Run the call_attr method of the app class."""
        self.check_call_attr_for_app_object(app)
        getattr(app, self.call_attr)()


class MenuHandler(BaseModel):
    """Menu handler class for console apps."""

    _EXIT_CHARACTER = "x"

    menu_items: list[MenuItem] = Field(min_length=1)

    @field_validator("menu_items", mode="after")
    @classmethod
    def check_unique_id(cls, items: list[MenuItem]) -> list[MenuItem]:
        """Check the unique id for each item in the menu."""
        duplicates: list[MenuItem] = [
            item
            for item in items
            if sum(1 for i in items if i.menu_id == item.menu_id) > 1
        ]
        if len(duplicates) > 0:
            raise ValueError(
                "MenuItem IDs must be unique! But there are the following duplicates: "
                f"{', '.join([str(item.menu_id) for item in duplicates])}"
            )
        return items

    @field_validator("menu_items", mode="after")
    @classmethod
    def check_unique_call_attr(cls, items: list[MenuItem]) -> list[MenuItem]:
        """Check the unique call_attr for each item in the menu."""
        duplicates: list[MenuItem] = [
            item
            for item in items
            if sum(1 for i in items if i.call_attr == item.call_attr) > 1
        ]
        if len(duplicates) > 0:
            raise ValueError(
                "MenuItem call_attr must be unique! But there are the following "
                f"duplicates: {', '.join([item.call_attr for item in duplicates])}"
            )
        return items

    @property
    def items(self) -> dict[int, MenuItem]:
        """Return the menu items as a dictionary."""
        return {item.menu_id: item for item in self.menu_items}

    def check_app_has_attrs(self, app: ConsoleApp) -> None:
        """Check if given app has all menu items call attributes."""
        for item in self.menu_items:
            item.check_call_attr_for_app_object(app)

    def run(self, app: ConsoleApp) -> None:
        """Run the menu (print and listen for commands)."""
        self._print_menu()
        while True:
            choice = input("Enter menu number: ")
            if choice.lower() == self._EXIT_CHARACTER.lower():
                app.exit()
                break
            item: MenuItem | None = (
                None if not choice.isdigit() else self.items.get(int(choice))
            )
            if item is None:
                print(f"{choice} is an invalid choice. Try again with one of these:")
                self._print_menu(only_choices=True)
                continue
            getattr(app, item.call_attr)()
            break

    def _print_menu(self, only_choices: bool = False) -> None:
        """Print the menu to the console."""
        if not only_choices:
            print("MENU")
            print("What would you like to do? Choose the corresponding number:")
        for item in self.menu_items:
            print(f"({item.menu_id}) : {item.description}")
        print(f"Enter '{self._EXIT_CHARACTER}' to exit.")


class ConsoleApp(ABC):
    """Abstract class for console apps in HHYB."""

    MAIN_APP_NAME = "HHYB - Your Diary"

    def __init__(
        self, app_name: str, calling_app: ConsoleApp | None, exit_to_calling_app: bool
    ) -> None:
        """Initialise the console app."""
        self.app_name = app_name
        self.calling_app = calling_app
        if self.calling_app is None and exit_to_calling_app:
            raise ValueError(
                "Cannot set exit_to_calling_app to True if no calling app is set!"
            )
        self.exit_to_calling_app = exit_to_calling_app
        self.menu_handler.check_app_has_attrs(self)

    @abstractmethod
    @property
    def menu_handler(self) -> MenuHandler:
        """Get the menu handler for the specific console app."""
        ...

    @property
    def _app_greeting(self) -> str:
        """Get the specific app's greeting."""
        return f"WELCOME TO {self.MAIN_APP_NAME.upper()} - {self.app_name.upper()}!"

    def print_app_title(self) -> None:
        """Print the app title."""
        print(self._app_greeting)
        print("".join(["-"] * len(self._app_greeting)))

    def reset_terminal(self) -> None:
        """Reset the terminal."""
        if os.name == "nt":  # Windows system
            os.system("cls")
        else:  # Unix-based system
            os.system("clear")
        self.print_app_title()

    @abstractmethod
    def _run(self) -> None:
        """Run the console app (special to every app)."""
        ...

    def run(self) -> None:
        """Run the console app."""
        self.reset_terminal()
        self.print_app_title()
        self._run()

    @abstractmethod
    def _exit_to_calling_app(self) -> None:
        """Exit the console app to their calling app."""
        ...

    @abstractmethod
    def _prepare_for_final_exit(self) -> None:
        """Prepare the console app for exit (special to every app)."""
        ...

    def exit(self) -> None:
        """Exit the console app."""
        if self.exit_to_calling_app:
            self._exit_to_calling_app()
        else:
            self._prepare_for_final_exit()
            print(f"Thank you for using {self.MAIN_APP_NAME} and goodbye!")
            input()
            exit()
