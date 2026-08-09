"""Pydantic models for menus in HHYB."""

from pydantic import BaseModel, Field, field_validator

from protocols.apps import AppProtocol


class MenuItem(BaseModel):
    """Menu Item class for console apps."""

    menu_id: int = Field(ge=0)
    description: str = Field(min_length=1)
    call_attr: str = Field(pattern="^[a-z_]+$")

    def check_call_attr_for_app_object(self, app: AppProtocol) -> None:
        """Check if the call_attr is a valid attribute of the app class."""
        if not hasattr(app, self.call_attr):
            raise ValueError(
                f"MenuItem {self} does not have a valid call attribute for class "
                f"{app.__class__.__name__}."
            )

    def run_call(self, app: AppProtocol) -> None:
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

    def check_app_has_attrs(self, app: AppProtocol) -> None:
        """Check if given app has all menu items call attributes."""
        for item in self.menu_items:
            item.check_call_attr_for_app_object(app)

    def run(self, app: AppProtocol) -> None:
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
