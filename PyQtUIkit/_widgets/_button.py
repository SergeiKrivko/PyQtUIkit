from enum import Enum
from typing import Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics

from _core.icon import KitIcon
from _core.style_obj import ButtonStyle
from _core.styles import style_service
from _core.locale import _KitLocaleString, _KitLocaleStringArray
from _widgets._layout_button import KitLayoutButton
from _widgets._label import KitLabel


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
        self.__label.classes.add('__PyQtUIkit_Button_Label')
        self.on_click.add(self.__on_click)

        self.add(self.__label)

    def __on_click(self, status):
        if status:
            self.__label.classes.add('pressed')
        else:
            self.__label.classes.remove('pressed')
        self.__label.apply_style()

    def __apply_width(self):
        style = self.final_style.apply(self.style)
        fm = QFontMetrics(self.__label.qt_widget.font())
        width = fm.size(0, self.__label.qt_widget.text()).width() + style.padding[1] + style.padding[3]
        self.qt_widget.setFixedWidth(width)

    def apply_style(self):
        super().apply_style()
        self.__apply_width()

    def apply_lang(self):
        super().apply_lang()
        self.__apply_width()
