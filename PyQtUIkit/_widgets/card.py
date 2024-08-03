from typing import Iterable

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy

from _widgets.widget import KitWidget
from _core.style_obj import CardStyle
from _core.styles import style_service, KitStyle
from _widgets.layout import KitLayout


class KitCard(KitWidget):
    def __init__(self,
                 layout: KitLayout = None,
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

    @property
    def children(self) -> Iterable['KitWidget']:
        yield self.layout

    @property
    def layout(self) -> KitLayout:
        return self.__layout

    @layout.setter
    def layout(self, layout: KitLayout):
        self.__layout = layout
        self.__strange_widget.setLayout(layout.qt_widget)

    def apply_style(self):
        super().apply_style()
        style = self.final_style
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
