from typing import Iterable

from PyQt6.QtWidgets import QMenu

from PyQtUIkit._core.style_obj import CardStyle
from PyQtUIkit._widgets.layout import KitLayout
from PyQtUIkit._widgets.widget import KitWidget


class KitBaseMenu(KitWidget):
    def __init__(self):
        super().__init__(QMenu())

        self.__layout = None
        self.__style = CardStyle()
        self.__final_style = CardStyle()

    @property
    def qt_widget(self) -> QMenu:
        return super().qt_widget

    @property
    def style(self) -> CardStyle:
        return self.__style

    @property
    def children(self) -> Iterable['KitWidget']:
        yield self.__layout

    @property
    def final_style(self) -> CardStyle:
        return self.__final_style

    @property
    def layout(self) -> KitLayout:
        return self.__layout

    @layout.setter
    def layout(self, layout: KitLayout):
        self.__layout = layout
        self.qt_widget.setLayout(layout.qt_widget)

    def _apply_style(self):
        super()._apply_style()
        style = self.final_style
        self.qt_widget.setStyleSheet(f"""
QMenu {{
    color: rgba{style.color.getRgb()};
    background-color: rgba{style.background.getRgb()};
    border: {style.border.width}px {style.border.type} rgba{style.border.color.getRgb()};
    border-top-left-radius: {style.radius.top_left};
    border-top-right-radius: {style.radius.top_right};
    border-bottom-left-radius: {style.radius.bottom_left};
    border-bottom-right-radius: {style.radius.bottom_right};
}}""")
        self.__layout._apply_style()

    def apply_lang(self):
        self.__layout.apply_lang()
