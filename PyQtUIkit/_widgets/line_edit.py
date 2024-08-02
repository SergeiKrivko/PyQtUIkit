from typing import Iterable

from PyQt6.QtWidgets import QLineEdit

from PyQtUIkit._core.locale import _KitLocaleString, _KitLocaleStringArray
from _core.event import KitSignals
from _widgets.widget import KitWidget
from _core.style_obj import ButtonStyle
from _core.styles import style_service


class KitLineEdit(KitWidget):
    def __init__(self,
                 placeholder: str | _KitLocaleString | _KitLocaleStringArray,
                 classes: Iterable[str] | str = None,):
        super().__init__(QLineEdit())
        self.__placeholder = placeholder
        self.__style = ButtonStyle()
        self.__final_style = ButtonStyle()
        if classes:
            self.classes = classes

        self.__text_change_events = KitSignals()
        self.__text_edit_events = KitSignals()

        self.qt_widget.textChanged.connect(self.__text_change_events)
        self.qt_widget.textEdited.connect(self.__text_edit_events)

    @property
    def qt_widget(self) -> QLineEdit:
        return super().qt_widget

    @property
    def style(self) -> ButtonStyle:
        return self.__style

    @property
    def final_style(self) -> ButtonStyle:
        return self.__final_style

    @property
    def on_text_change(self):
        return self.__text_change_events

    @property
    def on_text_edit(self):
        return self.__text_edit_events

    @property
    def text(self):
        return self.qt_widget.text()

    @text.setter
    def text(self, text: str):
        self.qt_widget.setText(text)

    @property
    def placeholder(self) -> str:
        if isinstance(self.__placeholder, str):
            return self.__placeholder
        return self.__placeholder.get()

    @placeholder.setter
    def placeholder(self, placeholder: str | _KitLocaleString | _KitLocaleStringArray):
        self.__placeholder = placeholder
        self.apply_lang()

    def apply_lang(self):
        self.qt_widget.setPlaceholderText(self.placeholder)

    def apply_style(self):
        super().apply_style()
        # self.qt_widget.setFont(self.style.font.get())
        style = self.final_style
        self.qt_widget.setStyleSheet(s := f"""
        QLineEdit {{
            color: rgba{style.color.getRgb()};
            background-color: rgba{style.background.getRgb()};
            border: {style.border.width}px {style.border.type} rgba{style.border.color.getRgb()};
            border-top-left-radius: {style.radius.top_left};
            border-top-right-radius: {style.radius.top_right};
            border-bottom-left-radius: {style.radius.bottom_left};
            border-bottom-right-radius: {style.radius.bottom_right};
            padding: {style.padding[0]}px {style.padding[1]}px {style.padding[2]}px {style.padding[3]}px;
        }}
        QLineEdit::hover {{
            color: rgba{style.hover.color.getRgb()};
            background-color: rgba{style.hover.background.getRgb()};
            border: {style.hover.border.width}px {style.hover.border.type} rgba{style.hover.border.color.getRgb()};
            border-top-left-radius: {style.hover.radius.top_left};
            border-top-right-radius: {style.hover.radius.top_right};
            border-bottom-left-radius: {style.hover.radius.bottom_left};
            border-bottom-right-radius: {style.hover.radius.bottom_right};
            padding: {style.hover.padding[0]}px {style.hover.padding[1]}px {style.hover.padding[2]}px {style.hover.padding[3]}px;
        }}
        QLineEdit::disabled {{
            color: rgba{style.pressed.color.getRgb()};
            background-color: rgba{style.pressed.background.getRgb()};
            border: {style.pressed.border.width}px {style.pressed.border.type} rgba{style.pressed.border.color.getRgb()};
            border-top-left-radius: {style.pressed.radius.top_left};
            border-top-right-radius: {style.pressed.radius.top_right};
            border-bottom-left-radius: {style.pressed.radius.bottom_left};
            border-bottom-right-radius: {style.pressed.radius.bottom_right};
            padding: {style.pressed.padding[0]}px {style.pressed.padding[1]}px {style.pressed.padding[2]}px {style.pressed.padding[3]}px;
        }}
        QLineEdit::focus {{
            color: rgba{style.pressed.color.getRgb()};
            background-color: rgba{style.pressed.background.getRgb()};
            border: {style.pressed.border.width}px {style.pressed.border.type} rgba{style.pressed.border.color.getRgb()};
            border-top-left-radius: {style.pressed.radius.top_left};
            border-top-right-radius: {style.pressed.radius.top_right};
            border-bottom-left-radius: {style.pressed.radius.bottom_left};
            border-bottom-right-radius: {style.pressed.radius.bottom_right};
            padding: {style.pressed.padding[0]}px {style.pressed.padding[1]}px {style.pressed.padding[2]}px {style.pressed.padding[3]}px;
        }}""")
        print(s)
