from typing import Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout

from PyQtUIkit._widgets.widget import KitWidget
from PyQtUIkit._core.style_obj import LayoutStyle
from _widgets.layout.base import KitLayout


class KitBoxLayout(KitWidget):
    def __init__(self, orientation: Qt.Orientation):
        super().__init__(QWidget())
        self.__layout = KitLayout(orientation)
        self.qt_widget.setLayout(self.__layout.qt_widget)

        self.__style = LayoutStyle()
        self.__final_style = LayoutStyle()

    @property
    def style(self) -> LayoutStyle:
        return self.__style

    @property
    def final_style(self) -> LayoutStyle:
        return self.__final_style

    @property
    def children(self) -> Iterable['KitWidget']:
        return self.__layout.children

    @property
    def count(self) -> int:
        return self.__layout.count

    @property
    def layout(self):
        return self.__layout

    def add(self, widget: KitWidget | QWidget | QLayout):
        self.__layout.add(widget)

    def insert(self, index, widget: KitWidget | QWidget | QLayout):
        self.__layout.insert(index, widget)

    def remove(self, widget: KitWidget | QWidget | QLayout):
        self.__layout.remove(widget)

    def pop(self, index) -> KitWidget | QWidget | QLayout:
        return self.__layout.pop(index)

    def clear(self):
        self.__layout.clear()

    def apply_lang(self):
        super().apply_lang()
        self.__layout.apply_lang()

    def _apply_style(self):
        super()._apply_style()
        self.qt_widget.setStyleSheet('background-color: transparent;')
        self.__layout.style.padding = self.final_style.padding
        self.__layout.style.spacing = self.final_style.spacing
        self.__layout.style.align = self.final_style.align
        self.__layout._apply_style()


class KitHBoxLayout(KitBoxLayout):
    def __init__(self, *args,
                 padding: int | tuple[int, int, int, int] | tuple[int, int] | str = None,
                 spacing: int | str = None,
                 align: Qt.AlignmentFlag | None = None,
                 classes: Iterable[str] | str = None):
        super().__init__(Qt.Orientation.Horizontal)
        for el in args:
            self.add(el)
        if padding is not None:
            self.style.padding = padding
        if spacing is not None:
            self.style.spacing = spacing
        if align is not None:
            self.style.align = align
        if classes:
            self.classes = classes


class KitVBoxLayout(KitBoxLayout):
    def __init__(self, *args,
                 padding: int | tuple[int, int, int, int] | tuple[int, int] | str = None,
                 spacing: int | str = None,
                 align: Qt.AlignmentFlag | None = None,
                 classes: Iterable[str] | str = None):
        super().__init__(Qt.Orientation.Vertical)
        for el in args:
            self.add(el)
        if padding is not None:
            self.style.padding = padding
        if spacing is not None:
            self.style.spacing = spacing
        if align is not None:
            self.style.align = align
        if classes:
            self.classes = classes
