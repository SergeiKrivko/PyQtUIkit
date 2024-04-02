from enum import Enum

from PyQt6.QtGui import QFont


class KitFont:
    class Size(Enum):
        SMALL = 0
        MEDIUM = 1
        BIG = 2
        SUPER_BIG = 3

    def __init__(self,
                 family: str,
                 small: int,
                 medium: int = None,
                 big: int = None,
                 super_big: int = None,
                 italic=False,
                 bold=False,
                 strike=False):
        self.family = family
        self.small = small
        self.medium = medium or small
        self.big = big or medium or small
        self.super_big = super_big or big or medium or small
        
        self._small = QFont(self.family, self.small)
        self._medium = QFont(self.family, self.medium)
        self._big = QFont(self.family, self.big)
        self._super_big = QFont(self.family, self.super_big)

        for el in [self._small, self._medium, self._big, self._super_big]:
            el.setItalic(italic)
            el.setBold(bold)
            el.setStrikeOut(strike)

    def get(self, size: Size):
        match size:
            case KitFont.Size.SMALL:
                return self._small
            case KitFont.Size.MEDIUM:
                return self._medium
            case KitFont.Size.BIG:
                return self._big
            case KitFont.Size.SUPER_BIG:
                return self._super_big
            case _:
                raise KeyError(size)
