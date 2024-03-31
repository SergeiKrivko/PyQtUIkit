from enum import Enum
from uuid import uuid4

from PyQt6.QtGui import QColor

from PyQtUIkit.core.icon import KitIcon
from PyQtUIkit.themes import KitPalette, icons


class IntProperty(property):
    def __init__(self, name='', default=0):
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))

        def getter(obj) -> int:
            try:
                return getattr(obj, self._id)
            except AttributeError:
                return default

        def setter(obj, value: int | float):
            setattr(obj, self._id, int(value))

        super().__init__(getter, setter)


class BoolProperty(property):
    def __init__(self, name='', default=True):
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))

        def getter(obj) -> bool:
            try:
                return getattr(obj, self._id)
            except AttributeError:
                return default

        def setter(obj, value):
            setattr(obj, self._id, bool(value))

        super().__init__(getter, setter)


class StringProperty(property):
    def __init__(self, name='', default=''):
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))

        def getter(obj) -> str:
            try:
                return getattr(obj, self._id)
            except AttributeError:
                return default

        def setter(obj, value: str):
            setattr(obj, self._id, str(value))

        super().__init__(getter, setter)


class IconProperty(property):
    def __init__(self, name=''):
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))

        def getter(obj) -> KitIcon | None:
            try:
                icon = getattr(obj, self._id)
            except AttributeError:
                return None
            if not icon or icon == 'None':
                return None
            if isinstance(icon, str):
                return KitIcon(data=icons[icon])
            return icon

        def setter(obj, value: str | KitIcon):
            setattr(obj, self._id, value)
            obj._apply_theme()

        super().__init__(getter, setter)


class _Color(QColor):
    def __str__(self):
        return self.name()


class ColorProperty(property):
    def __init__(self, name='', default='#00000000'):
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))

        def getter(obj) -> _Color:
            try:
                res = getattr(obj, self._id)
            except AttributeError:
                res = default
            if isinstance(res, str):
                if res.startswith('#'):
                    res = _Color(res)
                else:
                    res = obj.theme_manager.get(res)
            return res

        def setter(obj, value: str | _Color | QColor):
            if isinstance(value, QColor):
                value = _Color(value.name())
            setattr(obj, self._id, value)

        super().__init__(getter, setter)


class PaletteProperty(property):
    def __init__(self, name='', default='Main'):
        if name == 'Main':
            raise Exception
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))

        def getter(obj) -> KitPalette:
            try:
                res = getattr(obj, self._id)
            except AttributeError:
                res = default
            if isinstance(res, str):
                res = obj.theme_manager.get(res)
            return res

        def setter(obj, value: str | KitPalette):
            setattr(obj, self._id, value)

        super().__init__(getter, setter)


class LiteralProperty(property):
    def __init__(self, name, values: list):
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))
        self._values = values

        def getter(obj) -> str:
            try:
                return getattr(obj, self._id)
            except AttributeError:
                return values[0]

        def setter(obj, value: str):
            if value not in self._values:
                raise ValueError(f"Invalid value: {name} must be one of {repr(values)}")
            setattr(obj, self._id, str(value))

        super().__init__(getter, setter)


class EnumProperty(property):
    def __init__(self, name, enum, default=0):
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))
        self._enum = enum
        self._default = default

        def getter(obj):
            try:
                return getattr(obj, self._id)
            except AttributeError:
                return default

        def setter(obj, value: str):
            if value not in self._enum:
                raise ValueError(f"Invalid value: {name} must be one of {repr(list(self._enum))}")
            setattr(obj, self._id, value)

        super().__init__(getter, setter)
