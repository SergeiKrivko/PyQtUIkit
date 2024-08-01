from enum import Enum
from typing import Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QSizePolicy

from core import KitIcon
from core.style_obj import ButtonStyle
from core.styles import style_service
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

    def __apply_width(self):
        style: ButtonStyle = style_service.get_style(self)
        fm = QFontMetrics(self.__label.qt_widget.font())
        width = fm.size(0, self.__label.qt_widget.text()).width() + style.padding[1] + style.padding[3]
        self.qt_widget.setFixedWidth(width)

    def apply_style(self):
        self.__label.classes = self.classes.copy()
        self.__label.classes.add('__PyQtUIkit_Button_Label')
        super().apply_style()
        self.__apply_width()

    def apply_lang(self):
        super().apply_lang()
        self.__apply_width()
