import sys

if sys.version_info < (3, 7):
    raise ImportError('Your Python version {0} is not supported by aiogram, please install '
                      'Python 3.7+'.format('.'.join(map(str, sys.version_info[:3]))))

from rolling_dice.models import Dice, Result, DiceError, NotFoundMethod, ParseError
from rolling_dice.parser import get_result, open_lark
from rolling_dice.resources import GRAMMAR_CALCULATOR, GRAMMAR_DICE

__all__ = (
    "Dice",
    "Result",
    "DiceError",
    "NotFoundMethod",
    "ParseError",
    "get_result",
    "open_lark",
    "GRAMMAR_CALCULATOR",
    "GRAMMAR_DICE"
)

__version__ = '1.1'
