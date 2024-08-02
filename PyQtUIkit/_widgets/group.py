from typing import Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout

from _widgets.layout import KitBoxLayout
from _widgets.widget import KitWidget


class KitGroupWidget(KitWidget):
    pass


class KitGroup(KitBoxLayout):
    def __init__(self,
                 orientation: Qt.Orientation = Qt.Orientation.Horizontal,
                 classes: Iterable[str] | str = None, ):
        super().__init__(orientation)
        self.__orientation = orientation
        if classes:
            self.classes = classes

    def add(self, widget: KitGroupWidget):
        if not isinstance(widget, KitGroupWidget):
            raise TypeError
        super().add(widget)

    def insert(self, index, widget: KitWidget | QWidget | QLayout):
        if not isinstance(widget, KitGroupWidget):
            raise TypeError
        super().insert(index, widget)

    def apply_style(self):
        orientation = 'H' if self.__orientation == Qt.Orientation.Horizontal else 'V'
        for i, child in enumerate(self.children):
            if i == 0:
                child.classes.add(f'__PyQtUIkit_{orientation}Group_first')
            else:
                child.classes.discard(f'__PyQtUIkit_{orientation}Group_first')
            if i == self.count - 1:
                child.classes.add(f'__PyQtUIkit_{orientation}Group_last')
            else:
                child.classes.discard(f'__PyQtUIkit_{orientation}Group_last')
            child.classes.add(f'__PyQtUIkit_Group')
        super().apply_style()


class KitHGroup(KitGroup):
    def __init__(self, *args: KitGroupWidget,
                 classes: Iterable[str] | str = None, ):
        super().__init__(Qt.Orientation.Horizontal, classes)
        for el in args:
            self.add(el)


class KitVGroup(KitGroup):
    def __init__(self, *args: KitGroupWidget,
                 classes: Iterable[str] | str = None, ):
        super().__init__(Qt.Orientation.Vertical, classes)
        for el in args:
            self.add(el)
