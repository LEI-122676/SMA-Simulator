from abc import ABC, abstractmethod
from typing import Optional, Tuple


class Action(ABC):
    @abstractmethod
    def to_tuple(self) -> Optional[Tuple[int, int]]:
        """Return a (dx, dy) tuple for movement actions, or None for non-move actions."""

