from datetime import date
from uuid import UUID

from app.domain.entities.task import Task, TaskStatus, TaskPriority
from app.domain.repositories.task_repo import AbstractTaskRepository


class TaskService:
    def __init__(self, repo: AbstractTaskRepository) -> None:
        self._repo = repo

    async def create_task(
        self,
        user_id: UUID,
        title: str,
        description: str | None = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        status: TaskStatus = TaskStatus.TODO,
    ) -> Task:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            status=status,
        )
        return await self._repo.create(task)

    async def get_user_tasks(self, user_id: UUID) -> list[Task]:
        return await self._repo.get_by_user(user_id)

    async def get_task(self, task_id: UUID) -> Task | None:
        return await self._repo.get_by_id(task_id)

    async def move_task(self, task_id: UUID, status: TaskStatus) -> Task | None:
        task = await self._repo.get_by_id(task_id)
        if not task:
            return None
        task.move_to(status)  # бизнес-логика на сущности
        return await self._repo.update(task)

    async def reorder_task(self, task_id: UUID, position: int) -> Task | None:
        task = await self._repo.get_by_id(task_id)
        if not task:
            return None
        task.move_position(position)  # бизнес-логика на сущности
        return await self._repo.update(task)

    async def complete_task(self, task_id: UUID) -> Task | None:
        task = await self._repo.get_by_id(task_id)
        if not task:
            return None
        task.complete()  # выставляет completed_at и статус DONE
        return await self._repo.update(task)

    async def delete_task(self, task_id: UUID) -> None:
        task = await self._repo.get_by_id(task_id)
        if not task:
            return
        await self._repo.delete(task_id)

    async def get_completed_by_date(self, user_id: UUID, day: date) -> list[Task]:
        return await self._repo.get_completed_by_date(user_id, day)
