from app.core.security import hash_password, verify_password, create_access_token
from app.domain.entities.user import User
from app.domain.repositories.user_repo import AbstractUserRepository


class AuthService:
    def __init__(self, repo: AbstractUserRepository) -> None:
        self._repo = repo

    async def register(self, email: str, password: str) -> User:
        existing = await self._repo.get_by_email(email)
        if existing:
            raise ValueError("User with this email already exists")
        user = User(
            email=email,
            hashed_password=hash_password(password),
        )

        return await self._repo.create(user)

    async def login(self, email: str, password: str) -> str:
        user = await self._repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")
        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return create_access_token(user.id)
