from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.task import Task, TaskStatus, TaskPriority
from app.domain.repositories.task_repo import AbstractTaskRepository
from app.infrastructure.models.task import TaskModel


class TaskRepositoryImpl(AbstractTaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ── маппинг ORM → domain ──────────────────────────────
    @staticmethod
    def _to_entity(model: TaskModel) -> Task:
        return Task(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            title=model.title,
            description=model.description,
            status=TaskStatus(model.status),
            priority=TaskPriority(model.priority),
            position=model.position,
            due_date=model.due_date,
            completed_at=model.completed_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(entity: Task) -> TaskModel:
        return TaskModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            title=entity.title,
            description=entity.description,
            status=entity.status.value,
            priority=entity.priority.value,
            position=entity.position,
            due_date=entity.due_date,
            completed_at=entity.completed_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    # ── CRUD ─────────────────────────────────────────────
    async def create(self, task: Task) -> Task:
        model = self._to_model(task)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, task_id: UUID) -> Task | None:
        result = await self._session.execute(
            select(TaskModel).where(TaskModel.id == str(task_id))
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_user(self, user_id: UUID) -> list[Task]:
        result = await self._session.execute(
            select(TaskModel)
            .where(TaskModel.user_id == str(user_id))
            .order_by(TaskModel.position)
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def get_completed_by_date(self, user_id: UUID, day: date) -> list[Task]:
        result = await self._session.execute(
            select(TaskModel).where(
                TaskModel.user_id == str(user_id),
                TaskModel.status == TaskStatus.DONE,
                TaskModel.completed_at >= day,  # фильтр по дню нужен для стриков
            )
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def update(self, task: Task) -> Task:
        result = await self._session.execute(
            select(TaskModel).where(TaskModel.id == str(task.id))
        )
        model = result.scalar_one()
        model.title = task.title
        model.description = task.description
        model.status = task.status.value
        model.priority = task.priority.value
        model.position = task.position
        model.due_date = task.due_date
        model.completed_at = task.completed_at
        model.updated_at = task.updated_at
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, task_id: UUID) -> None:
        result = await self._session.execute(
            select(TaskModel).where(TaskModel.id == str(task_id))
        )
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.commit()
