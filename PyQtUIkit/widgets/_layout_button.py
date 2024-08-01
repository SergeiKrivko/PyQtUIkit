from typing import Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QWidget, QLayout

from PyQtUIkit.widgets._layout import KitBoxLayout
from PyQtUIkit.widgets._widget import KitWidget
from core._style_obj import ButtonStyle
from core._styles import style_service
from core.event import KitSignals


class KitLayoutButton(KitWidget):
    def __init__(self, orientation: Qt.Orientation = Qt.Orientation.Horizontal,
                 checkable: bool = False,
                 classes: Iterable[str] | str = None):
        button = QPushButton()
        self.__layout = KitBoxLayout(orientation)
        button.setLayout(self.__layout.qt_widget)

        super().__init__(button)

        self.__click_events = KitSignals()
        self.qt_widget.clicked.connect(self.__click_events)

        self.__style = ButtonStyle()
        if classes:
            self.classes = classes
        self.checkable = checkable

    @property
    def qt_widget(self) -> QPushButton:
        return super().qt_widget

    @property
    def style(self) -> ButtonStyle:
        return self.__style

    @property
    def on_click(self):
        return self.__click_events

    @property
    def checkable(self) -> bool:
        return self.qt_widget.isCheckable()

    @checkable.setter
    def checkable(self, value: bool):
        self.qt_widget.setCheckable(value)

    def add(self, widget: KitWidget | QWidget | QLayout):
        self.__layout.add(widget)

    def insert(self, index, widget: KitWidget | QWidget | QLayout):
        self.__layout.insert(index, widget)

    def remove(self, widget):
        return self.__layout.remove(widget)

    def pop(self, index) -> KitWidget | QWidget | QLayout:
        return self.__layout.pop(index)

    def apply_lang(self):
        self.__layout.apply_lang()

    def apply_style(self):
        self.__layout.apply_style()
        style: ButtonStyle = style_service.get_style(self)
        self.qt_widget.setStyleSheet(s := f"""
        QPushButton {{
            color: rgba{style.color.getRgb()};
            background-color: rgba{style.background.getRgb()};
            border: {style.border.width}px {style.border.type} rgba{style.border.color.getRgb()};
            border-top-left-radius: {style.radius.top_left};
            border-top-right-radius: {style.radius.top_right};
            border-bottom-left-radius: {style.radius.bottom_left};
            border-bottom-right-radius: {style.radius.bottom_right};
            padding: {style.padding[0]}px {style.padding[1]}px {style.padding[2]}px {style.padding[3]}px;
        }}
        QPushButton::hover {{
            color: rgba{style.hover.color.getRgb()};
            background-color: rgba{style.hover.background.getRgb()};
            border: {style.hover.border.width}px {style.border.type} rgba{style.border.color.getRgb()};
            border-top-left-radius: {style.hover.radius.top_left};
            border-top-right-radius: {style.hover.radius.top_right};
            border-bottom-left-radius: {style.hover.radius.bottom_left};
            border-bottom-right-radius: {style.hover.radius.bottom_right};
            padding: {style.hover.padding[0]}px {style.hover.padding[1]}px {style.hover.padding[2]}px {style.hover.padding[3]}px;
        }}
        QPushButton::disabled {{
            color: rgba{style.pressed.color.getRgb()};
            background-color: rgba{style.pressed.background.getRgb()};
            border: {style.pressed.border.width}px {style.border.type} rgba{style.border.color.getRgb()};
            border-top-left-radius: {style.pressed.radius.top_left};
            border-top-right-radius: {style.pressed.radius.top_right};
            border-bottom-left-radius: {style.pressed.radius.bottom_left};
            border-bottom-right-radius: {style.pressed.radius.bottom_right};
            padding: {style.pressed.padding[0]}px {style.pressed.padding[1]}px {style.pressed.padding[2]}px {style.pressed.padding[3]}px;
        }}
        QPushButton::checked {{
            color: rgba{style.pressed.color.getRgb()};
            background-color: rgba{style.pressed.background.getRgb()};
            border: {style.pressed.border.width}px {style.border.type} rgba{style.border.color.getRgb()};
            border-top-left-radius: {style.pressed.radius.top_left};
            border-top-right-radius: {style.pressed.radius.top_right};
            border-bottom-left-radius: {style.pressed.radius.bottom_left};
            border-bottom-right-radius: {style.pressed.radius.bottom_right};
            padding: {style.pressed.padding[0]}px {style.pressed.padding[1]}px {style.pressed.padding[2]}px {style.pressed.padding[3]}px;
        }}
        QPushButton::menu-indicator {{
            image: none;
            subcontrol-origin: padding;
            padding-right: 5px;
            subcontrol-position: right;
        }}""")
        print(s)
