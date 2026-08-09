"""Models for diary entries."""

import datetime as dt
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class EntryFieldType(StrEnum):
    """Entry field type."""

    TEXT = "text"
    CHOICE = "choice"
    NUMERICAL = "numerical"
    SCALE = "scale"


FIELD_TYPE_FIELD = "field_type"


class EntryField(BaseModel):
    """Entry field for diary entries."""

    name: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    field_type: EntryFieldType

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EntryField":
        """Create an EntryField from a dictionary."""
        if FIELD_TYPE_FIELD not in data:
            raise ValueError(
                f"Field '{FIELD_TYPE_FIELD}' is required! Only got fields "
                f"{[str(k) for k in data.keys()]} in given dictionary."
            )
        model_cls = FIELD_TYPE_TO_MODEL[EntryFieldType(data[FIELD_TYPE_FIELD])]
        return model_cls(**data)

    @property
    def full_prompt(self) -> str:
        """Get the full prompt for the entry field."""
        return f"{self.prompt}\n{self._generate_type_prompt()}:\n"

    def _generate_type_prompt(self) -> str:
        """Generate a type prompt for the entry field."""
        raise NotImplementedError("This method must be implemented by subclasses!")

    def _process_input(self, input_string: str) -> Any:
        """Process the input string and return valid value if possible."""
        raise NotImplementedError("This method must be implemented by subclasses!")

    def get_value_from_prompt(self) -> Any:
        """Get the value from the prompt."""
        input_string = input(self.full_prompt)
        return self._process_input(input_string)


class TextEntryField(EntryField):
    """Text entry field for diary entries."""

    field_type: EntryFieldType = EntryFieldType.TEXT

    def _generate_type_prompt(self) -> str:
        """Generate a type prompt for the entry field."""
        return "You can use any unicode characters you like"

    def _process_input(self, input_string: str) -> str:
        """Process the input string and return valid value if possible."""
        return input_string.strip()


class ChoiceEntryField(EntryField):
    """Choice entry field for diary entries."""

    field_type: EntryFieldType = EntryFieldType.CHOICE
    choices: dict[str, str] = Field(min_length=2)  # short key: description

    def _generate_type_prompt(self) -> str:
        """Generate a type prompt for the entry field."""
        choice_menu = "\n".join(
            f"  {key}: {description}" for key, description in self.choices.items()
        )
        return f"Please select one of the following options:\n{choice_menu}"

    def _process_input(self, input_string: str) -> str:
        """Process the input string and return valid value if possible."""
        if input_string.strip() not in self.choices:
            raise ValueError(
                f"Invalid choice: {input_string}. "
                f"Valid choices: {list(self.choices.keys())}"
            )
        return input_string.strip()


class NumericalEntryField(EntryField):
    """Numerical entry field for diary entries."""

    field_type: EntryFieldType = EntryFieldType.NUMERICAL
    min_value: float | None = Field(default=None)
    max_value: float | None = Field(default=None)

    def _generate_type_prompt(self) -> str:
        """Generate a type prompt for the entry field."""
        range_prompt = ""
        if self.min_value is not None and self.max_value is not None:
            range_prompt = f"between {self.min_value} and {self.max_value}"
        elif self.min_value is not None:
            range_prompt = f"greater than or equal to {self.min_value}"
        elif self.max_value is not None:
            range_prompt = f"less than or equal to {self.max_value}"
        return f"Please enter a numerical value {range_prompt}"

    def _process_input(self, input_string: str) -> float:
        """Process the input string and return valid value if possible."""
        try:
            value = float(input_string)
        except ValueError:
            raise ValidationError("Please enter a numerical value!")
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(
                f"Please enter a value greater than or equal to {self.min_value}!"
            )
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(
                f"Please enter a value less than or equal to {self.max_value}!"
            )
        return value


class ScaleEntryField(EntryField):
    """Scale entry field for diary entries."""

    field_type: EntryFieldType = EntryFieldType.SCALE
    min_value: int = Field(default=0)
    max_value: int = Field(default=10)

    def _generate_type_prompt(self) -> str:
        """Generate a type prompt for the entry field."""
        return (
            "Please enter an integer value between "
            f"{self.min_value} and {self.max_value}"
        )

    def _process_input(self, input_string: str) -> int:
        """Process the input string and return valid value if possible."""
        try:
            value = int(input_string)
        except ValueError:
            raise ValidationError("Please enter an integer value!")
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(
                f"Please enter an integer value greater than "
                f"or equal to {self.min_value}!"
            )
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(
                f"Please enter an integer value less than or equal to {self.max_value}!"
            )
        return value


FIELD_TYPE_TO_MODEL = {
    EntryFieldType.TEXT: TextEntryField,
    EntryFieldType.CHOICE: ChoiceEntryField,
    EntryFieldType.NUMERICAL: NumericalEntryField,
    EntryFieldType.SCALE: ScaleEntryField,
}


class Entry(BaseModel):
    """One day entry for diary HHYB."""

    date: dt.date
    created_at: dt.datetime
    last_updated_at: dt.datetime
    fields: list[EntryField] = Field(min_length=1)
