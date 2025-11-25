from dataclasses import dataclass
from typing import Optional, Tuple
from Actions.Action import Action


@dataclass
class Collect(Action):
    item_id: Optional[int] = None

    def to_tuple(self) -> Optional[Tuple[int, int]]:
        # Collect is not a movement; return None to signal that.
        return None

    def __repr__(self) -> str:
        return f"Collect(item_id={self.item_id})"
