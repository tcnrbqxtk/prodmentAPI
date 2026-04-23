from datetime import date, datetime, timezone
from uuid import UUID

from app.domain.entities.diary import DiaryEntry
from app.domain.repositories.diary_repo import AbstractDiaryRepository


class DiaryService:

    def __init__(self, repo: AbstractDiaryRepository) -> None:
        self._repo = repo

    async def get_or_create_today(self, user_id: UUID) -> DiaryEntry:
        """Получить запись на сегодня или создать пустую."""
        today = datetime.now(timezone.utc).date()
        entry = await self._repo.get_by_user_and_date(user_id, today)
        if not entry:
            entry = DiaryEntry(user_id=user_id, date=today)
            entry = await self._repo.create(entry)
        return entry

    async def get_by_date(self, user_id: UUID, day: date) -> DiaryEntry | None:
        return await self._repo.get_by_user_and_date(user_id, day)

    async def get_range(
        self, user_id: UUID, date_from: date, date_to: date
    ) -> list[DiaryEntry]:
        return await self._repo.get_range(user_id, date_from, date_to)

    async def update_entry(
        self,
        user_id: UUID,
        day: date,
        mood: int | None = None,
        note: str | None = None,
        sleep_hours: float | None = None,
    ) -> DiaryEntry:
        entry = await self._repo.get_by_user_and_date(user_id, day)
        if not entry:
            # если записи нет — создаём с нуля
            entry = DiaryEntry(user_id=user_id, date=day)
            entry = await self._repo.create(entry)

        if mood is not None:
            entry.set_mood(mood)  # валидация 0-100 внутри сущности
        if note is not None:
            entry.note = note
        if sleep_hours is not None:
            entry.sleep_hours = sleep_hours

        entry.updated_at = datetime.now(timezone.utc)
        return await self._repo.update(entry)
