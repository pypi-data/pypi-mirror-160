from re import search, findall
from typing import List

from rolling_dice.models.Dice import Dice
from rolling_dice.models.Result import Result
from rolling_dice.models.errors.ParseError import ParseError
from rolling_dice.parser.lark_laboers import open_lark
from rolling_dice.resources import GRAMMAR_DICE, GRAMMAR_CALCULATOR


def get_result(text,
               grammar_dice=GRAMMAR_DICE,
               grammar_calc=GRAMMAR_CALCULATOR) -> List:
    results = []
    repeats_math = search(r"(^\d+)[хx]|[хx](\d+$)", text)
    repeats = repeats_math.group(1) or repeats_math.group(2) if repeats_math else 1
    for _ in range(int(repeats) if int(repeats) < 10 else 10):
        t = text.replace(repeats_math.group(0), "") if repeats_math else text
        result = Result(raw=t)
        result.dices = []
        for dice in findall(r"(\d*[dkдк]\d+[hlвнd]?\d*)", t):
            value: Dice = open_lark(text=dice, grammar=grammar_dice)
            result.dices.append((dice, value))
        result.total = open_lark(text=result.replaced_dices, grammar=grammar_calc)
        if str(result.total) == t:
            raise ParseError
        results.append(result)
    return results
