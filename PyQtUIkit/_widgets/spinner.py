from enum import Enum
from typing import Iterable

from PyQt6.QtCore import QPropertyAnimation, QPoint, QEasingCurve
from PyQt6.QtWidgets import QWidget

from PyQtUIkit._core.event import KitSignals
from PyQtUIkit._widgets.layout_button import KitLayoutButton
from PyQtUIkit._widgets.widget import KitWidget
from _core.style_obj import LayoutCardStyle
from _impl._spinner import Spinner


class KitSpinner(KitWidget):

    def __init__(self, classes: Iterable[str] | str | None = None):
        super().__init__(Spinner())
        if classes is not None:
            self.classes = classes

        self.__style = LayoutCardStyle()
        self.__final_style = LayoutCardStyle()

    @property
    def qt_widget(self) -> Spinner:
        return super().qt_widget

    @property
    def style(self) -> LayoutCardStyle:
        return self.__style

    @property
    def final_style(self) -> LayoutCardStyle:
        return self.__final_style

    def _apply_style(self):
        self.size = 40
        super()._apply_style()
        style = self.final_style
        width = self.width - style.padding[1] - style.padding[3]
        height = self.height - style.padding[0] - style.padding[2]
        size = min(width, height)
        self.qt_widget.spinner_size = size
        self.qt_widget.color = style.color
        self.qt_widget.spinner_width = 2
