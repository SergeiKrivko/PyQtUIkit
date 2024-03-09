import typing

from PyQt6 import QtGui
from PyQt6.QtWidgets import QMenu

from PyQtUIkit.core.properties import IntProperty, PaletteProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitMenu(QMenu, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Main')
    border = IntProperty('border', 0)
    radius = IntProperty('radius', 4)

    def __init__(self, parent):
        super().__init__()
        self.__parent = parent

    def showEvent(self, a0: typing.Optional[QtGui.QShowEvent]) -> None:
        super().showEvent(a0)
        self._set_tm(self.__parent._tm)
        self._apply_theme()

    # def exec(self) -> typing.Optional[QtGui.QAction]:
    #     self._set_tm(self.__parent._tm)
    #     self._apply_theme()
    #     return super().exec()

    def _apply_theme(self):
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
