"""Core functionality for apps in HHYB."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod

from models.menu import MenuHandler


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
