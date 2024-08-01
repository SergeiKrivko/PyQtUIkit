from typing import Iterable

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy

from PyQtUIkit.widgets._widget import KitWidget
from core._style_obj import CardStyle
from core._styles import style_service
from PyQtUIkit.widgets._layout import KitBoxLayout


class KitCard(KitWidget):
    def __init__(self,
                 layout: KitBoxLayout = None,
                 classes: Iterable[str] | str = None, ):
        super().__init__(QWidget())
        strange_layout = QHBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.qt_widget.setLayout(strange_layout)
        self.__strange_widget = QWidget()
        strange_layout.addWidget(self.__strange_widget)
        self.__layout = None
        self.layout = layout

        self.__style = CardStyle()
        if classes:
            self.classes = classes

    @property
    def qt_widget(self) -> QWidget:
        return super().qt_widget

    @property
    def style(self) -> CardStyle:
        return self.__style

    @property
    def layout(self) -> KitBoxLayout:
        return self.__layout

    @layout.setter
    def layout(self, layout: KitBoxLayout):
        self.__layout = layout
        self.__strange_widget.setLayout(layout.qt_widget)

    def apply_style(self):
        style: CardStyle = style_service.get_style(self)
        self.qt_widget.setStyleSheet(f"""
        QWidget {{
            background-color: rgba{style.background.getRgb()};
            border: {style.border.width}px {style.border.type} rgba{style.border.color.getRgb()};
            border-top-left-radius: {style.radius.top_left};
            border-top-right-radius: {style.radius.top_right};
            border-bottom-left-radius: {style.radius.bottom_left};
            border-bottom-right-radius: {style.radius.bottom_right};
        }}""")
        self.layout.apply_style()

    def apply_lang(self):
        self.layout.apply_lang()
