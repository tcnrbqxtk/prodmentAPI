from abc import abstractmethod
from uuid import UUID

from app.domain.entities.user import User
from app.domain.repositories.base import AbstractRepository


class AbstractUserRepository(AbstractRepository[User]):
    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...
