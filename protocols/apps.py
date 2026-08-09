"""Protocols for apps in HHYB."""

from typing import Protocol


class AppProtocol(Protocol):
    """Protocol for apps in HHYB."""

    def run(self) -> None:
        """Run the app."""
        ...

    def exit(self) -> None:
        """Exit the app."""
        ...
