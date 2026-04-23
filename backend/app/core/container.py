from typing import AsyncGenerator

from dishka import Provider, Scope, provide, make_async_container  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession


from app.infrastructure.database import AsyncSessionFactory
from app.infrastructure.repositories.task_repo import TaskRepositoryImpl
from app.domain.repositories.task_repo import AbstractTaskRepository
from app.services.task_service import TaskService
from app.infrastructure.repositories.user_repo import UserRepositoryImpl
from app.domain.repositories.user_repo import AbstractUserRepository
from app.services.auth_service import AuthService

from app.infrastructure.repositories.diary_repo import DiaryRepositoryImpl
from app.domain.repositories.diary_repo import AbstractDiaryRepository
from app.services.diary_service import DiaryService


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide  # type: ignore[misc]
    def get_task_repo(self, session: AsyncSession) -> AbstractTaskRepository:
        return TaskRepositoryImpl(session)

    @provide  # type: ignore[misc]
    def get_user_repo(self, session: AsyncSession) -> AbstractUserRepository:
        return UserRepositoryImpl(session)

    @provide  # type: ignore[misc]
    def get_diary_repo(self, session: AsyncSession) -> AbstractDiaryRepository:
        return DiaryRepositoryImpl(session)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide  # type: ignore[misc]
    def get_task_service(self, repo: AbstractTaskRepository) -> TaskService:
        return TaskService(repo)

    @provide  # type: ignore[misc]
    def get_auth_service(self, repo: AbstractUserRepository) -> AuthService:
        return AuthService(repo)

    @provide  # type: ignore[misc]
    def get_diary_service(self, repo: AbstractDiaryRepository) -> DiaryService:
        return DiaryService(repo)


class DatabaseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSessionFactory() as session:
            yield session


def create_container():
    return make_async_container(
        DatabaseProvider(),
        RepositoryProvider(),
        ServiceProvider(),
    )
