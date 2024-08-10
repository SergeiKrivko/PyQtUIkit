from typing import Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from PyQtUIkit._widgets.widget import KitWidget
from PyQtUIkit._core.style_obj import CardStyle


class KitDivider(KitWidget):
    def __init__(self,
                 orientation: Qt.Orientation.Horizontal,
                 classes: Iterable[str] | str = None, ):
        super().__init__(QWidget())
        self.__orientation = orientation
        strange_layout = QHBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.qt_widget.setLayout(strange_layout)
        strange_layout.addWidget(QWidget())

        self.__style = CardStyle()
        self.__final_style = CardStyle()
        if classes:
            self.classes = classes

    @property
    def qt_widget(self) -> QWidget:
        return super().qt_widget

    @property
    def style(self) -> CardStyle:
        return self.__style

    @property
    def final_style(self) -> CardStyle:
        return self.__final_style

    def _apply_style(self):
        super()._apply_style()
        style = self.final_style
        if self.__orientation == Qt.Orientation.Horizontal:
            self.height = style.border.width
        else:
            self.width = style.border.width
        self.qt_widget.setStyleSheet(f"""
        QWidget {{
            background-color: rgba{style.border.color.getRgb()};
            border: none;
        }}""")


class KitHDivider(KitDivider):
    def __init__(self, classes: Iterable[str] | str = None):
        super().__init__(Qt.Orientation.Horizontal, classes)


class KitVDivider(KitDivider):
    def __init__(self, classes: Iterable[str] | str = None):
        super().__init__(Qt.Orientation.Vertical, classes)
