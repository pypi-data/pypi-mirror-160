from dataclasses import dataclass
from typing import Tuple, List

from rolling_dice.models.Dice import Dice


@dataclass
class Result:
    raw: str
    total: int = None
    dices: List[Tuple[str, Dice]] = None

    @property
    def total_formula(self) -> str:
        result = self.raw
        for dice, cls in self.dices:
            result = result.replace(dice, cls.to_str(view_retains=True, ), 1)
        return result + f"={self.total}"

    @property
    def replaced_dices(self) -> str:
        result = self.raw
        for dice, cls in self.dices:
            result = result.replace(dice, str(cls.total), 1)
        return result