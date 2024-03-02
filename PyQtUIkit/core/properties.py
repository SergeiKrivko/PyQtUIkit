from uuid import uuid4

from PyQt6.QtGui import QColor

from PyQtUIkit.core.icon import KitIcon
from PyQtUIkit.themes import Palette, icons


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
        self._id = '_' + (str(name) or str(uuid4()).replace('-', '_'))

        def getter(obj) -> Palette:
            try:
                res = getattr(obj, self._id)
            except AttributeError:
                res = default
            if isinstance(res, str):
                res = obj.theme_manager.get(res)
            return res

        def setter(obj, value: str | Palette):
            setattr(obj, self._id, value)

        super().__init__(getter, setter)
