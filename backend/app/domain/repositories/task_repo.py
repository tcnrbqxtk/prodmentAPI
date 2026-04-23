from abc import abstractmethod
from datetime import date
from uuid import UUID

from app.domain.entities.task import Task
from app.domain.repositories.base import AbstractRepository


class AbstractTaskRepository(AbstractRepository[Task]):
    @abstractmethod
    async def create(self, task: Task) -> Task: ...

    @abstractmethod
    async def get_by_id(self, task_id: UUID) -> Task | None: ...

    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> list[Task]: ...

    @abstractmethod
    async def get_completed_by_date(self, user_id: UUID, day: date) -> list[Task]: ...

    @abstractmethod
    async def update(self, task: Task) -> Task: ...

    @abstractmethod
    async def delete(self, task_id: UUID) -> None: ...
