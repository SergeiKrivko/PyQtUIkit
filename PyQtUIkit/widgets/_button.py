from enum import Enum
from typing import Iterable

from PyQt6.QtCore import Qt

from core import KitIcon
from core.locale import _KitLocaleString, _KitLocaleStringArray
from PyQtUIkit.widgets._layout_button import KitLayoutButton
from PyQtUIkit.widgets._label import KitLabel


class KitButton(KitLayoutButton):
    class IconPosition(Enum):
        LEFT = 1
        RIGHT = 2
        TOP = 3
        BOTTOM = 4

    def __init__(self,
                 text: str | _KitLocaleString | _KitLocaleStringArray,
                 icon: KitIcon | str = None,
                 icon_pos=IconPosition.LEFT,
                 checkable: bool = False,
                 classes: Iterable[str] | str = None):
        super().__init__(
            Qt.Orientation.Horizontal if
            icon_pos == KitButton.IconPosition.LEFT or icon_pos == KitButton.IconPosition.RIGHT
            else Qt.Orientation.Vertical, checkable=checkable, classes=classes)

        self.__text = text
        self.__label = KitLabel(self.__text)
        self.on_click.add(self.__on_click)

        self.add(self.__label)

    def __on_click(self, status):
        if status:
            self.__label.classes.add('pressed')
        else:
            self.__label.classes.remove('pressed')
        self.__label.apply_style()

    def apply_style(self):
        self.__label.classes = self.classes.copy()
        self.__label.classes.add('__PyQtUIkit_Button_Label')
        super().apply_style()
