from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.diary import DiaryEntry
from app.domain.repositories.diary_repo import AbstractDiaryRepository
from app.infrastructure.models.diary import DiaryEntryModel


class DiaryRepositoryImpl(AbstractDiaryRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_entity(model: DiaryEntryModel) -> DiaryEntry:
        return DiaryEntry(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            date=model.date,
            mood=model.mood,
            note=model.note,
            sleep_hours=model.sleep_hours,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(entity: DiaryEntry) -> DiaryEntryModel:
        return DiaryEntryModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            date=entity.date,
            mood=entity.mood,
            note=entity.note,
            sleep_hours=entity.sleep_hours,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, entry: DiaryEntry) -> DiaryEntry:
        model = self._to_model(entry)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_user_and_date(self, user_id: UUID, day: date) -> DiaryEntry | None:
        result = await self._session.execute(
            select(DiaryEntryModel).where(
                DiaryEntryModel.user_id == str(user_id),
                DiaryEntryModel.date == day,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_range(
        self, user_id: UUID, date_from: date, date_to: date
    ) -> list[DiaryEntry]:
        result = await self._session.execute(
            select(DiaryEntryModel)
            .where(
                DiaryEntryModel.user_id == str(user_id),
                DiaryEntryModel.date >= date_from,
                DiaryEntryModel.date <= date_to,
            )
            .order_by(DiaryEntryModel.date.desc())
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def update(self, entry: DiaryEntry) -> DiaryEntry:
        result = await self._session.execute(
            select(DiaryEntryModel).where(DiaryEntryModel.id == str(entry.id))
        )
        model = result.scalar_one()
        model.mood = entry.mood
        model.note = entry.note
        model.sleep_hours = entry.sleep_hours
        model.updated_at = entry.updated_at
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_entity(model)
