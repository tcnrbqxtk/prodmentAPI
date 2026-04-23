from abc import abstractmethod
from datetime import date
from uuid import UUID

from app.domain.entities.diary import DiaryEntry
from app.domain.repositories.base import AbstractRepository


class AbstractDiaryRepository(AbstractRepository[DiaryEntry]):
    @abstractmethod
    async def create(self, entry: DiaryEntry) -> DiaryEntry: ...

    @abstractmethod
    async def get_by_user_and_date(
        self, user_id: UUID, day: date
    ) -> DiaryEntry | None: ...

    @abstractmethod
    async def get_range(
        self, user_id: UUID, date_from: date, date_to: date
    ) -> list[DiaryEntry]: ...

    @abstractmethod
    async def update(self, entry: DiaryEntry) -> DiaryEntry: ...
