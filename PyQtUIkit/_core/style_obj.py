from functools import lru_cache

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class _SubStyle:
    pass


class _FontSubStyle(_SubStyle):
    def __init__(self):
        self.__family: str | None = None
        self.__size: int | None = None
        self.__bold = None
        self.__italic = None
        self.__underline = None
        self.__strike = None

    @property
    def family(self) -> str:
        return self.__family

    @family.setter
    def family(self, family: str):
        self.__family = family

    @property
    def size(self) -> int:
        return self.__size

    @size.setter
    def size(self, size: int | str):
        self.__size = int(size)

    @property
    def bold(self) -> bool:
        return self.__bold

    @bold.setter
    def bold(self, b: bool | str):
        if b in ['True', 'true']:
            b = True
        elif isinstance(b, str):
            b = False
        self.__bold = bool(b)

    @property
    def italic(self) -> bool:
        return self.__italic

    @italic.setter
    def italic(self, b: bool | str):
        if b in ['True', 'true']:
            b = True
        elif isinstance(b, str):
            b = False
        self.__italic = bool(b)

    @property
    def underline(self) -> bool:
        return self.__underline

    @underline.setter
    def underline(self, b: bool | str):
        if b in ['True', 'true']:
            b = True
        elif isinstance(b, str):
            b = False
        self.__underline = bool(b)

    @property
    def strike(self) -> bool:
        return self.__strike

    @strike.setter
    def strike(self, b: bool | str):
        if b in ['True', 'true']:
            b = True
        elif isinstance(b, str):
            b = False
        self.__strike = bool(b)

    def get(self) -> QFont:
        return self.__font(self.family, self.size, self.bold, self.italic, self.underline, self.strike)

    @staticmethod
    @lru_cache
    def __font(family, size, bold, italic, underline, strike):
        res = QFont()

        res.setFamily(family)
        res.setPointSize(size)
        res.setBold(bold)
        res.setItalic(italic)
        res.setUnderline(underline)
        res.setStrikeOut(strike)

        return res


class _RadiusSubStyle(_SubStyle):
    def __init__(self):
        self.__top_left: int | None = None
        self.__top_right: int | None = None
        self.__bottom_left: int | None = None
        self.__bottom_right: int | None = None

    @property
    def top_left(self) -> int | None:
        return self.__top_left

    @top_left.setter
    def top_left(self, top_left: int | str):
        self.__top_left = int(top_left)

    @property
    def top_right(self) -> int | None:
        return self.__top_right

    @top_right.setter
    def top_right(self, top_right: int | str):
        self.__top_right = int(top_right)

    @property
    def bottom_left(self) -> int | None:
        return self.__bottom_left

    @bottom_left.setter
    def bottom_left(self, bottom_left: int | str):
        self.__bottom_left = int(bottom_left)

    @property
    def bottom_right(self) -> int | None:
        return self.__bottom_right

    @bottom_right.setter
    def bottom_right(self, bottom_right: int | str):
        self.__bottom_right = int(bottom_right)

    @staticmethod
    def _from_tuple(t: tuple[int, ...]) -> '_RadiusSubStyle':
        res = _RadiusSubStyle()
        if len(t) == 1:
            res.top_left = t[0]
            res.top_right = t[0]
            res.bottom_left = t[0]
            res.bottom_right = t[0]
        elif len(t) == 2:
            res.top_left = t[0]
            res.top_right = t[0]
            res.bottom_left = t[1]
            res.bottom_right = t[1]
        elif len(t) == 4:
            res.top_left = t[0]
            res.top_right = t[1]
            res.bottom_left = t[2]
            res.bottom_right = t[3]
        else:
            raise ValueError

        return res

    @staticmethod
    def _from_str(s: str) -> '_RadiusSubStyle':
        return _RadiusSubStyle._from_tuple(tuple(map(int, s.split())))


class _BorderSubStyle(_SubStyle):
    def __init__(self):
        self.__width: int | None = None
        self.__type: str | None = None
        self.__color: QColor | None = None

    @property
    def width(self) -> int | None:
        return self.__width

    @width.setter
    def width(self, width: int | str):
        self.__width = int(width)

    @property
    def type(self) -> str | None:
        return self.__type

    @type.setter
    def type(self, t: str):
        self.__type = t

    @property
    def color(self) -> QColor | None:
        return self.__color

    @color.setter
    def color(self, color: QColor | str):
        self.__color = QColor(color)

    @staticmethod
    def _from_str(s: str):
        res = _BorderSubStyle()
        res.width, res.type, res.color = s.split()
        return res


class BaseStyle:
    _MAIN = []
    _SUB = []

    def __init__(self):
        pass

    def get(self, key: str):
        obj = self
        keys = key.split('.')
        for el in keys[:-1]:
            obj = getattr(obj, el)
        return getattr(obj, keys[-1])

    def set(self, key: str, value: str, if_none=True):
        if value is None:
            return
        obj = self
        keys = key.split('.')
        try:
            for el in keys[:-1]:
                obj = getattr(obj, el)
        except AttributeError:
            return
        if not if_none or getattr(obj, keys[-1]) is None:
            setattr(obj, keys[-1], value)

    def apply(self, other: 'BaseStyle', if_none=False):
        for el in self._MAIN + self._SUB:
            try:
                val = other.get(el)
            except AttributeError as e:
                pass
            else:
                if isinstance(val, BaseStyle):
                    self.get(el).apply(val, if_none=False)
                elif val is not None:
                    self.set(el, val, if_none=if_none)

        for sub_name in self._SUB:
            sub: BaseStyle = self.get(sub_name)
            sub.apply(self, if_none=True)
        return self


class LayoutStyle(BaseStyle):
    _MAIN = ['padding', 'spacing', 'align']

    def __init__(self):
        super().__init__()
        self.__padding: tuple[int, int, int, int] | None = None
        self.__spacing: int | None = None
        self.__align: Qt.AlignmentFlag | None = None

    @property
    def padding(self) -> tuple[int, int, int, int] | None:
        return self.__padding

    @padding.setter
    def padding(self, padding: tuple[int, int, int, int] | tuple[int, int] | int | str | None):
        if isinstance(padding, str):
            padding = tuple(map(int, padding.split()))
        if isinstance(padding, tuple):
            if len(padding) == 1:
                self.__padding = *padding, *padding, *padding, *padding
            elif len(padding) == 2:
                self.__padding = *padding, *padding
            elif len(padding) == 4:
                self.__padding = padding
            else:
                raise ValueError
        elif isinstance(padding, int):
            self.__padding = padding, padding, padding, padding
        else:
            raise TypeError

    @property
    def spacing(self) -> int | None:
        return self.__spacing

    @spacing.setter
    def spacing(self, spacing: int | str):
        self.__spacing = int(spacing)

    @property
    def align(self) -> Qt.AlignmentFlag | None:
        return self.__align

    @align.setter
    def align(self, align: Qt.AlignmentFlag | None):
        self.__align = align


class CardStyle(BaseStyle):
    _MAIN = ['background', 'color',
             'font.family', 'font.size', 'font.bold', 'font.italic', 'font.underline', 'font.strike',
             'radius.top_left', 'radius.top_right', 'radius.bottom_left', 'radius.bottom_right',
             'border.width', 'border.type', 'border.color']

    def __init__(self):
        super().__init__()
        self.__background: QColor | None = None
        self.__color: QColor | None = None
        self.__font = _FontSubStyle()
        self.__radius = _RadiusSubStyle()
        self.__border = _BorderSubStyle()

    @property
    def background(self) -> QColor | None:
        return self.__background

    @background.setter
    def background(self, color: QColor | str | None):
        if isinstance(color, str):
            color = QColor(color)
        self.__background = color

    @property
    def color(self) -> QColor | None:
        return self.__color

    @color.setter
    def color(self, color: QColor | str | None):
        if isinstance(color, str):
            color = QColor(color)
        self.__color = color

    @property
    def radius(self) -> _RadiusSubStyle:
        return self.__radius

    @property
    def font(self) -> _FontSubStyle:
        return self.__font

    @radius.setter
    def radius(self, radius: _RadiusSubStyle | str | tuple):
        if isinstance(radius, str):
            radius = _RadiusSubStyle._from_str(radius)
        elif isinstance(radius, tuple):
            radius = _RadiusSubStyle._from_tuple(radius)
        self.__radius = radius

    @property
    def border(self) -> _BorderSubStyle:
        return self.__border

    @border.setter
    def border(self, border: _RadiusSubStyle | str):
        if isinstance(border, str):
            border = _BorderSubStyle._from_str(border)
        self.__border = border


class LayoutCardStyle(LayoutStyle, CardStyle):
    _MAIN = ['padding', 'spacing', 'align', 'background', 'color',
             'font.family', 'font.size', 'font.bold', 'font.italic', 'font.underline', 'font.strike',
             'radius.top_left', 'radius.top_right', 'radius.bottom_left', 'radius.bottom_right',
             'border.width', 'border.type', 'border.color']

    def __init__(self):
        super().__init__()


class ButtonStyle(LayoutCardStyle):
    _SUB = ['hover', 'pressed']

    def __init__(self):
        super().__init__()
        self.__hover = LayoutCardStyle()
        self.__pressed = LayoutCardStyle()

    @property
    def hover(self) -> LayoutCardStyle:
        return self.__hover

    @property
    def pressed(self) -> LayoutCardStyle:
        return self.__pressed


class ListStyle(LayoutCardStyle):
    _SUB = ['item']

    def __init__(self):
        super().__init__()
        self.__item = ButtonStyle()

    @property
    def item(self) -> ButtonStyle:
        return self.__item
