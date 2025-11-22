from dataclasses import dataclass
from typing import Optional, Tuple
from Action import Action

@dataclass
class Deposit(Action):
    nest_id: Optional[int] = None

    def to_tuple(self) -> Optional[Tuple[int, int]]:
        # Deposit is not a movement; return None to signal that.
        return None

    def __repr__(self) -> str:
        return f"Deposit(nest_id={self.nest_id})"