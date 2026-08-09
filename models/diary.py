"""Pydantic models for whole HHYB diaries."""

import datetime as dt

from pydantic import BaseModel, Field

from models.entry import Entry


class Diary(BaseModel):
    """Base diary model for HHYB."""

    started_at: dt.datetime
    entries: list[Entry] = Field(min_length=1)

    @classmethod
    def from_json(cls, json_data: dict):
        """Create a Diary object from a JSON dictionary."""
        return cls(**json_data)

    def to_json(self) -> str:
        """Convert the Diary object to a JSON string."""
        return self.model_dump_json(indent=2)


class CurrentDiary(Diary):
    """Current diary model for HHYB."""

    current_last_entry: dt.date
    last_updated_at: dt.datetime


class BackupDiary(CurrentDiary):
    """Backup diary model for HHYB."""

    last_backup_at: dt.datetime


class ArchivedDiary(Diary):
    """Archived diary model for HHYB."""

    last_entry: dt.date
    archived_at: dt.datetime
