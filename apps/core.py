"""Core functionality for apps in HHYB."""

import os
from abc import ABC, abstractmethod

from protocols.apps import AppProtocol
from protocols.menu import MenuHandlerProtocol


class ConsoleApp(ABC):
    """Abstract class for console apps in HHYB."""

    MAIN_APP_NAME = "HHYB - Your Diary"

    def __init__(self, app_name: str) -> None:
        """Initialise the console app."""
        self.app_name = app_name
        self.menu_handler.check_app_has_attrs(self)

    @property
    @abstractmethod
    def menu_handler(self) -> MenuHandlerProtocol:
        """Get the menu handler for the specific console app."""
        ...

    @property
    def _app_greeting(self) -> str:
        """Get the specific app's greeting."""
        return f"WELCOME TO {self.MAIN_APP_NAME.upper()} - {self.app_name.upper()}!"

    def _print_app_title(self) -> None:
        """Print the app title."""
        print(self._app_greeting)
        print("".join(["-"] * len(self._app_greeting)))

    def _reset_terminal(self) -> None:
        """Reset the terminal."""
        if os.name == "nt":  # Windows system
            os.system("cls")
        else:  # Unix-based system
            os.system("clear")
        self._print_app_title()

    @abstractmethod
    def _run(self) -> None:
        """Run the console app (special to every app)."""
        ...

    def run(self) -> None:
        """Run the console app."""
        self._reset_terminal()
        self._run()

    @abstractmethod
    def _prepare_for_final_exit(self) -> None:
        """Prepare the console app for exit (special to every app)."""
        ...

    def exit(self) -> None:
        """Exit the console app."""
        self._prepare_for_final_exit()
        print(f"Thank you for using {self.MAIN_APP_NAME} and goodbye!")
        input()
        exit()


class SubApp(ConsoleApp, ABC):
    """Abstract class for console apps in HHYB."""

    MAIN_APP_NAME = "HHYB - Your Diary"

    def __init__(
        self,
        app_name: str,
        app_handler: AppProtocol | None,
        always_exit_to_handler: bool,
    ) -> None:
        """Initialise the console app."""
        super().__init__(app_name)
        self.app_handler = app_handler
        if self.app_handler is None and always_exit_to_handler:
            raise ValueError(
                "Cannot set always_exit_to_handler to True if no app handler is set!"
            )
        self.always_exit_to_handler = always_exit_to_handler

    @abstractmethod
    def _exit_to_app_handler(self) -> None:
        """Exit the console app to their app handler."""
        ...

    def exit(self) -> None:
        """Exit the console app."""
        if self.always_exit_to_handler:
            self._exit_to_app_handler()
        else:
            self._prepare_for_final_exit()
            print(f"Thank you for using {self.MAIN_APP_NAME} and goodbye!")
            input()
            exit()
