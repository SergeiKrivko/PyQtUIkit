from typing import Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy

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

    def add(self, widget: KitWidget):
        if not isinstance(widget, (KitGroupWidget, KitGroup)):
            raise TypeError
        super().add(widget)

    def insert(self, index, widget: KitWidget):
        if not isinstance(widget, KitGroupWidget):
            raise TypeError
        super().insert(index, widget)

    def apply_style(self):
        def check_attribute(c, attribute):
            if '__PyQtUIkit_Group' not in self.classes or f'__PyQtUIkit_Group_{attribute}' in self.classes:
                c.classes.add(f'__PyQtUIkit_Group_{attribute}')

        for i, child in enumerate(self.children):
            for el in ['top_left', 'top_right', 'bottom_left', 'bottom_right']:
                child.classes.discard(f'__PyQtUIkit_Group_{el}')

            if i == 0:
                check_attribute(child, 'top_left')
                if self.__orientation == Qt.Orientation.Horizontal:
                    check_attribute(child, 'bottom_left')
                else:
                    check_attribute(child, 'top_right')

            if i == self.count - 1:
                check_attribute(child, 'bottom_right')
                if self.__orientation == Qt.Orientation.Horizontal:
                    check_attribute(child, 'top_right')
                else:
                    check_attribute(child, 'bottom_left')

            child.classes.add('__PyQtUIkit_Group')

        super().apply_style()

        if self.__orientation == Qt.Orientation.Horizontal:
            for el in self.children:
                el.qt_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        else:
            for el in self.children:
                el.qt_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.qt_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)


class KitHGroup(KitGroup):
    def __init__(self, *args: KitGroupWidget | KitGroup,
                 classes: Iterable[str] | str = None, ):
        super().__init__(Qt.Orientation.Horizontal, classes)
        for el in args:
            self.add(el)


class KitVGroup(KitGroup):
    def __init__(self, *args: KitGroupWidget | KitGroup,
                 classes: Iterable[str] | str = None, ):
        super().__init__(Qt.Orientation.Vertical, classes)
        for el in args:
            self.add(el)
