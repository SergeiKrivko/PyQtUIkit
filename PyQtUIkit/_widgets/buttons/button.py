from enum import Enum
from typing import Iterable, Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QBoxLayout, QSizePolicy

from PyQtUIkit._core.icon import KitIcon
from PyQtUIkit._core.locale import _KitLocaleString, _KitLocaleStringArray
from PyQtUIkit._widgets.icon_widget import KitIconWidget
from PyQtUIkit._widgets.label import KitLabel
from PyQtUIkit._widgets.buttons.layout_button import KitLayoutButton


class KitButton(KitLayoutButton):
    class IconPosition(Enum):
        LEFT = 1
        RIGHT = 2
        TOP = 3
        BOTTOM = 4

    _DEFAULT_V_ICON_SIZE = 32
    _DEFAULT_H_ICON_SIZE = 20

    def __init__(self,
                 text: str | _KitLocaleString | _KitLocaleStringArray = '',
                 icon: KitIcon | str = None,
                 icon_pos=IconPosition.LEFT,
                 on_click: Callable = None,
                 checkable: bool = False,
                 classes: Iterable[str] | str = None):
        super().__init__(
            Qt.Orientation.Horizontal if
            icon_pos == KitButton.IconPosition.LEFT or icon_pos == KitButton.IconPosition.RIGHT
            else Qt.Orientation.Vertical, checkable=checkable, classes=classes, on_click=on_click)

        self.__icon_pos = icon_pos

        self.__label = KitLabel(text)
        self.add(self.__label)

        self.__icon_widget = KitIconWidget(icon)
        self.add(self.__icon_widget)

        self.on_state_change.add(self.__on_checked_change)
        self.qt_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    @property
    def text(self) -> str:
        return self.__label.text

    @text.setter
    def text(self, text: str | _KitLocaleString | _KitLocaleStringArray):
        self.__label.text = text

    @property
    def icon(self) -> KitIcon | None:
        return self.__icon_widget.icon

    @icon.setter
    def icon(self, icon: KitIcon | str | None):
        self.__icon_widget.icon = icon

    @property
    def icon_pos(self) -> IconPosition:
        return self.__icon_pos

    def __on_checked_change(self, status):
        if status:
            self.__label.classes.add('pressed')
            self.__icon_widget.classes.add('pressed')
        else:
            self.__label.classes.discard('pressed')
            self.__icon_widget.classes.discard('pressed')
        self.__label._apply_style()
        self.__icon_widget._apply_style()

    def __apply_size(self):
        style = self.final_style.apply(self.style)
        fm = QFontMetrics(self.__label.qt_widget.font())
        size = fm.size(0, self.__label.qt_widget.text())
        width, height = size.width(), size.height()

        if self.icon:
            if self.icon_pos == KitButton.IconPosition.LEFT or self.icon_pos == KitButton.IconPosition.RIGHT:
                height = max(height, self._DEFAULT_H_ICON_SIZE)
            if self.icon_pos == KitButton.IconPosition.TOP or self.icon_pos == KitButton.IconPosition.BOTTOM:
                width = max(width, self._DEFAULT_V_ICON_SIZE)

        self.__label.qt_widget.setFixedSize(width, height)
        if self.icon:
            if self.icon_pos == KitButton.IconPosition.LEFT or self.icon_pos == KitButton.IconPosition.RIGHT:
                self.__icon_widget.qt_widget.setFixedSize(self._DEFAULT_H_ICON_SIZE, height)
                width += self._DEFAULT_H_ICON_SIZE
                if self.text:
                    width += style.spacing
            elif self.icon_pos == KitButton.IconPosition.TOP or self.icon_pos == KitButton.IconPosition.BOTTOM:
                self.__icon_widget.qt_widget.setFixedSize(width, self._DEFAULT_V_ICON_SIZE)
                height += self._DEFAULT_V_ICON_SIZE
                if self.text:
                    height += style.spacing
        height += style.padding[0] + style.padding[2]
        width += style.padding[1] + style.padding[3]
        self.qt_widget.setMinimumSize(width, height)

    def _apply_style(self):
        self.__label.hidden = not self.text
        self.__icon_widget.hidden = not self.icon
        if self.icon_pos == KitButton.IconPosition.LEFT:
            self._layout.qt_widget.setDirection(QBoxLayout.Direction.RightToLeft)
        elif self.icon_pos == KitButton.IconPosition.TOP:
            self._layout.qt_widget.setDirection(QBoxLayout.Direction.BottomToTop)
        elif self.icon_pos == KitButton.IconPosition.RIGHT:
            self._layout.qt_widget.setDirection(QBoxLayout.Direction.LeftToRight)
        elif self.icon_pos == KitButton.IconPosition.BOTTOM:
            self._layout.qt_widget.setDirection(QBoxLayout.Direction.TopToBottom)

        self.style.align = Qt.AlignmentFlag.AlignCenter
        self.__label.qt_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        super()._apply_style()
        self.__apply_size()

    def apply_lang(self):
        super().apply_lang()
        self.__apply_size()
