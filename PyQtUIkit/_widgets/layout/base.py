from typing import Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QBoxLayout, QHBoxLayout, QVBoxLayout, QWidget, QLayout

from PyQtUIkit._widgets.widget import KitWidget
from PyQtUIkit._core.style_obj import LayoutStyle


class KitLayout(KitWidget):
    def __init__(self, orientation: Qt.Orientation):

        if orientation == Qt.Orientation.Horizontal:
            layout = QHBoxLayout()
        elif orientation == Qt.Orientation.Vertical:
            layout = QVBoxLayout()
        else:
            raise ValueError(f'Invalid orientation: {orientation}')

        super().__init__(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.__children = []
        self.__style = LayoutStyle()
        self.__final_style = LayoutStyle()

    @property
    def qt_widget(self) -> QBoxLayout:
        return super().qt_widget

    @property
    def style(self) -> LayoutStyle:
        return self.__style

    @property
    def final_style(self) -> LayoutStyle:
        return self.__final_style

    @property
    def children(self) -> Iterable['KitWidget']:
        for child in self.__children:
            yield child

    @property
    def count(self):
        return len(self.__children)

    def add(self, widget: KitWidget | QWidget | QLayout):
        self.__children.append(widget)
        if isinstance(widget, KitWidget):
            widget = widget.qt_widget

        if isinstance(widget, QWidget):
            self.qt_widget.addWidget(widget)
        elif isinstance(widget, QLayout):
            self.qt_widget.addLayout(widget)
        else:
            raise TypeError(f'Invalid widget: {widget}')

    def insert(self, index, widget: KitWidget | QWidget | QLayout):
        self.__children.insert(index, widget)
        if isinstance(widget, KitWidget):
            widget = widget.qt_widget

        if isinstance(widget, QWidget):
            self.qt_widget.insertWidget(index, widget)
        elif isinstance(widget, QLayout):
            self.qt_widget.insertLayout(index, widget)
        else:
            raise TypeError(f'Invalid widget: {widget}')

    def remove(self, widget):
        index = self.__children.index(widget)
        return self.pop(index)

    def pop(self, index) -> KitWidget | QWidget | QLayout:
        self.qt_widget.removeWidget(index)
        return self.__children.pop(index)

    def clear(self):
        for widget in self.__children:
            self.qt_widget.removeWidget(widget.qt_widget)
            widget.qt_widget.setParent(None)
        self.__children.clear()

    def apply_lang(self):
        for el in self.__children:
            if isinstance(el, KitWidget):
                el.apply_lang()

    def _apply_style(self):
        super()._apply_style()
        self.qt_widget.setContentsMargins(*self.final_style.padding)
        self.qt_widget.setSpacing(self.final_style.spacing)
        self.qt_widget.setAlignment(self.final_style.align or Qt.AlignmentFlag.AlignJustify)
        for el in self.__children:
            if isinstance(el, KitWidget):
                el._apply_style()


class KitHLayout(KitLayout):
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


class KitVLayout(KitLayout):
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
