import typing

from PyQt6 import QtGui
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu

from PyQtUIkit.core import IntProperty, PaletteProperty, IconProperty, EnumProperty, FontSize
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class _KitMenuAction:
    def __init__(self, action, icon):
        self.__action = action
        self.__icon = icon

    def _apply_icon(self, tm, palette):
        if self.__icon:
            self.__action.setIcon(tm.icon(self.__icon, palette.text))


class _KitMenu:
    def __init__(self, menu: QMenu, icon):
        self.__menu = menu
        self.triggered = menu.triggered
        self.__icon = icon
        self.__actions = []

    def addAction(self, text, icon=''):
        action = self.__menu.addAction(text)
        self.__actions.append(_KitMenuAction(action, icon))
        return action

    def addMenu(self, text, icon='') -> '_KitMenu':
        menu = self.__menu.addMenu(text)
        menu = _KitMenu(menu, icon)
        self.__actions.append(menu)
        return menu

    def _apply_icon(self, tm, palette):
        if self.__icon:
            self.__menu.setIcon(tm.icon(self.__icon, palette.text))
        for el in self.__actions:
            el._apply_icon(tm, palette)


class KitMenu(QMenu, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Main')
    border = IntProperty('border', 0)
    radius = IntProperty('radius', 4)
    icon = IconProperty('icon')
    font_size = EnumProperty('font_size', FontSize, FontSize.MEDIUM)

    def __init__(self, parent):
        super().__init__()
        self.__parent = parent
        self.__actions = []

    def showEvent(self, a0: typing.Optional[QtGui.QShowEvent]) -> None:
        super().showEvent(a0)
        self._set_tm(self.__parent._tm)
        self._apply_theme()

    def addAction(self, text: str, icon='') -> QAction:
        action = super().addAction(text)
        self.__actions.append(_KitMenuAction(action, icon))
        return action

    def addMenu(self, text, icon='') -> _KitMenu:
        menu = super().addMenu(text)
        menu = _KitMenu(menu, icon)
        self.__actions.append(menu)
        return menu

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFont(self._tm.font(self.font_size))
        self.setStyleSheet(f"""
QMenu {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: 1px solid {self._tm['Border'].main};
    border-radius: 6px;
    spacing: 4px;
    padding: 3px;
}}

QMenu::item {{
    border: 0px solid {self._tm['Border'].main};
    background-color: transparent;
    border-radius: 8px;
    padding: 4px 16px;
}}

QMenu::icon {{
    padding-left: 6px;
}}

QMenu::item:selected {{
    background-color: {self.main_palette.hover};
}}
QMenu::separator {{
    height: 1px;
    background: {self._tm['Border'].main};
    margin: 4px 10px;
}}""")
        if self.icon:
            self.setIcon(self._tm.icon(self.icon, self.main_palette.text))
        for el in self.__actions:
            el._apply_icon(self._tm, self.main_palette)
