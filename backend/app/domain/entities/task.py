from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    user_id: UUID
    title: str
    id: UUID = field(default_factory=uuid4)
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    position: int = 0  # порядок в колонке канбана
    due_date: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def complete(self) -> None:
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def move_to(self, status: TaskStatus) -> None:
        self.status = status
        if status != TaskStatus.DONE:
            self.completed_at = None
        self.updated_at = datetime.now(timezone.utc)

    def move_position(self, position: int) -> None:
        if position < 0:
            raise ValueError("Position cannot be negative")
        self.position = position
        self.updated_at = datetime.now(timezone.utc)
