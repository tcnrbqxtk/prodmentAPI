from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from pydantic import BaseModel, Field

from app.api.deps import get_current_user_id
from app.domain.entities.diary import DiaryEntry
from app.services.diary_service import DiaryService

router = APIRouter(
    prefix="/diary",
    tags=["diary"],
    route_class=DishkaRoute,
)


# ── Схемы ─────────────────────────────────────────────────────────────────────


class DiaryUpdate(BaseModel):
    mood: int | None = Field(None, ge=0, le=100)  # валидация прямо в схеме
    note: str | None = None
    sleep_hours: float | None = Field(None, ge=0, le=24)


class DiaryResponse(BaseModel):
    id: UUID
    user_id: UUID
    date: date
    mood: int | None
    mood_color: str | None  # red / yellow / green
    note: str | None
    sleep_hours: float | None

    model_config = {"from_attributes": True}


def _to_response(entry: DiaryEntry) -> DiaryResponse:
    return DiaryResponse(
        id=entry.id,
        user_id=entry.user_id,
        date=entry.date,
        mood=entry.mood,
        mood_color=entry.mood_color,  # property из сущности
        note=entry.note,
        sleep_hours=entry.sleep_hours,
    )


# ── Роуты ─────────────────────────────────────────────────────────────────────


@router.get("/today", response_model=DiaryResponse)
async def get_today(
    service: FromDishka[DiaryService],
    user_id: UUID = Depends(get_current_user_id),
) -> DiaryResponse:
    entry = await service.get_or_create_today(user_id)
    return _to_response(entry)


@router.get("/{day}", response_model=DiaryResponse)
async def get_by_date(
    day: date,
    service: FromDishka[DiaryService],
    user_id: UUID = Depends(get_current_user_id),
) -> DiaryResponse:
    entry = await service.get_by_date(user_id, day)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No entry for this date"
        )
    return _to_response(entry)


@router.get("/", response_model=list[DiaryResponse])
async def get_range(
    date_from: date,
    date_to: date,
    service: FromDishka[DiaryService],
    user_id: UUID = Depends(get_current_user_id),
) -> list[DiaryResponse]:
    if date_from > date_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="date_from must be before date_to",
        )
    entries = await service.get_range(user_id, date_from, date_to)
    return [_to_response(e) for e in entries]


@router.patch("/today", response_model=DiaryResponse)
async def update_today(
    body: DiaryUpdate,
    service: FromDishka[DiaryService],
    user_id: UUID = Depends(get_current_user_id),
) -> DiaryResponse:
    from datetime import datetime, timezone

    today = datetime.now(timezone.utc).date()
    entry = await service.update_entry(
        user_id=user_id,
        day=today,
        mood=body.mood,
        note=body.note,
        sleep_hours=body.sleep_hours,
    )
    return _to_response(entry)


@router.patch("/{day}", response_model=DiaryResponse)
async def update_by_date(
    day: date,
    body: DiaryUpdate,
    service: FromDishka[DiaryService],
    user_id: UUID = Depends(get_current_user_id),
) -> DiaryResponse:
    entry = await service.update_entry(
        user_id=user_id,
        day=day,
        mood=body.mood,
        note=body.note,
        sleep_hours=body.sleep_hours,
    )
    return _to_response(entry)
