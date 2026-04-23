from abc import ABC
from typing import Generic, TypeVar

EntityT = TypeVar("EntityT")


class AbstractRepository(ABC, Generic[EntityT]):
    """Базовый интерфейс. Конкретные репо наследуются от него."""

    pass
