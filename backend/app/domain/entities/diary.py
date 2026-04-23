from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import UUID, uuid4


@dataclass
class DiaryEntry:
    user_id: UUID
    date: date
    id: UUID = field(default_factory=uuid4)
    mood: int | None = None  # 0–100
    note: str | None = None
    sleep_hours: float | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if self.mood is not None:
            self._validate_mood(self.mood)

    def set_mood(self, value: int) -> None:
        self._validate_mood(value)
        self.mood = value
        self.updated_at = datetime.now(timezone.utc)

    @staticmethod
    def _validate_mood(value: int) -> None:
        if not (0 <= value <= 100):
            raise ValueError(f"Mood must be between 0 and 100, got {value}")

    @property
    def mood_color(self) -> str | None:
        if self.mood is None:
            return None
        if self.mood < 33:
            return "red"
        if self.mood < 66:
            return "yellow"
        return "green"
