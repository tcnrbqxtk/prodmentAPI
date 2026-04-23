from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from pydantic import BaseModel

from app.domain.entities.task import Task, TaskStatus, TaskPriority
from app.services.task_service import TaskService
from app.api.deps import get_current_user_id


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    route_class=DishkaRoute,
)


# ── Схемы запросов/ответов ────────────────────────────────────────────────────


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: TaskPriority | None = None


class TaskMove(BaseModel):
    status: TaskStatus


class TaskReorder(BaseModel):
    position: int


class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    position: int

    model_config = {"from_attributes": True}


# ── Роуты ─────────────────────────────────────────────────────────────────────


@router.get("/", response_model=list[TaskResponse])
async def get_tasks(
    service: FromDishka[TaskService],
    user_id: UUID = Depends(get_current_user_id),  # ← из токена
) -> list[Task]:
    return await service.get_user_tasks(user_id=user_id)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    body: TaskCreate,
    service: FromDishka[TaskService],
    user_id: UUID = Depends(get_current_user_id),  # ← из токена
) -> Task:
    return await service.create_task(
        user_id=user_id,
        title=body.title,
        description=body.description,
        priority=body.priority,
        status=body.status,
    )


@router.patch("/{task_id}/move", response_model=TaskResponse)
async def move_task(
    task_id: UUID,
    body: TaskMove,
    service: FromDishka[TaskService],
) -> Task:
    task = await service.move_task(task_id=task_id, status=body.status)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.patch("/{task_id}/reorder", response_model=TaskResponse)
async def reorder_task(
    task_id: UUID,
    body: TaskReorder,
    service: FromDishka[TaskService],
) -> Task:
    task = await service.reorder_task(task_id=task_id, position=body.position)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    service: FromDishka[TaskService],
) -> None:
    await service.delete_task(task_id=task_id)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: UUID,
    service: FromDishka[TaskService],
) -> Task:
    task = await service.complete_task(task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task
