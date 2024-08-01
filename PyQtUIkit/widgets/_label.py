from typing import Iterable

from PyQt6.QtWidgets import QLabel

from PyQtUIkit.core.locale import _KitLocaleString, _KitLocaleStringArray
from PyQtUIkit.widgets._widget import KitWidget
from core.style_obj import CardStyle
from core.styles import style_service


class KitLabel(KitWidget):
    def __init__(self,
                 text: str | _KitLocaleString | _KitLocaleStringArray,
                 classes: Iterable[str] | str = None,):
        super().__init__(QLabel())
        self.__text = text
        self.__style = CardStyle()
        if classes:
            self.classes = classes

    @property
    def qt_widget(self) -> QLabel:
        return super().qt_widget

    @property
    def style(self) -> CardStyle:
        return self.__style

    @property
    def text(self) -> str:
        if isinstance(self.__text, str):
            return self.__text
        return self.__text.get()

    @text.setter
    def text(self, text: str | _KitLocaleString | _KitLocaleStringArray):
        self.__text = text
        self.apply_lang()

    def apply_lang(self):
        self.qt_widget.setText(self.text)

    def apply_style(self):
        # self.qt_widget.setFont(self.style.font.get())
        style: CardStyle = style_service.get_style(self)
        self.qt_widget.setStyleSheet(f"""
        QLabel {{
            color: rgba{style.color.getRgb()};
            background-color: rgba{style.background.getRgb()};
            border: {style.border.width}px {style.border.type} rgba{style.border.color.getRgb()};
            border-top-left-radius: {style.radius.top_left};
            border-top-right-radius: {style.radius.top_right};
            border-bottom-left-radius: {style.radius.bottom_left};
            border-bottom-right-radius: {style.radius.bottom_right};
        }}""")
