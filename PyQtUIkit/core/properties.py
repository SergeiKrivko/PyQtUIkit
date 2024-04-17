from enum import Enum
from uuid import uuid4

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor

from PyQtUIkit.core.font import KitFont
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


class TextProperty(property):
    def __init__(self, name='', default=''):
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))

        def getter(obj) -> str:
            try:
                res = getattr(obj, self._id)
                if isinstance(res, str):
                    return res
                return res.get(obj._tm)
            except AttributeError:
                return default

        def setter(obj, value: str):
            setattr(obj, self._id, value)
            obj._apply_lang()

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


class PaletteProperty(property):
    def __init__(self, name='', default='Main'):
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))

        def getter(obj) -> KitPalette:
            try:
                res = getattr(obj, self._id)
            except AttributeError:
                res = default
            if isinstance(res, str):
                res = obj.theme_manager.palette(res)
            return res

        def setter(obj, value: str | KitPalette):
            setattr(obj, self._id, value)

        super().__init__(getter, setter)


class FontProperty(property):
    def __init__(self, name='', default='default'):
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))

        def getter(obj) -> KitFont:
            try:
                res = getattr(obj, self._id)
            except AttributeError:
                res = default
            if isinstance(res, str):
                res = obj.theme_manager.font(res)
            return res

        def setter(obj, value: str | KitFont):
            setattr(obj, self._id, value)

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


class SignalProperty(property):
    def __init__(self, name, signal: str):
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))
        self._signal = signal

        def getter(obj):
            return None

        def setter(obj, value: str):
            getattr(obj, self._signal).connect(value)

        super().__init__(getter, setter)
        
        
class MethodsProperty(property):
    def __init__(self, getter, setter):
        super().__init__(lambda obj: getter(obj), lambda obj, x: setter(obj, x))
