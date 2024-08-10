from typing import Iterable

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QPushButton, QWidget, QLayout

from PyQtUIkit._widgets.group import KitGroupWidget
from PyQtUIkit._widgets.layout import KitLayout
from PyQtUIkit._widgets.widget import KitWidget
from PyQtUIkit._widgets.base_popup import KitBasePopup
from PyQtUIkit._core.style_obj import ButtonStyle
from PyQtUIkit._core.event import KitSignals


class KitLayoutButton(KitGroupWidget):
    def __init__(self, orientation: Qt.Orientation = Qt.Orientation.Horizontal,
                 checkable: bool = False,
                 classes: Iterable[str] | str = None):
        button = QPushButton()
        self.__layout = KitLayout(orientation)
        button.setLayout(self.__layout.qt_widget)

        super().__init__(button)

        self.__click_events = KitSignals()
        self.__state_change_events = KitSignals()
        self.qt_widget.clicked.connect(self.__on_click)

        self.__style = ButtonStyle()
        self.__final_style = ButtonStyle()
        if classes:
            self.classes = classes
        self.checkable = checkable

        self.__popup: KitBasePopup | None = None

        self.qt_widget.setCursor(Qt.CursorShape.PointingHandCursor)

    @property
    def qt_widget(self) -> QPushButton:
        return super().qt_widget

    @property
    def style(self) -> ButtonStyle:
        return self.__style

    @property
    def final_style(self) -> ButtonStyle:
        return self.__final_style

    @property
    def children(self) -> Iterable['KitWidget']:
        yield self.__layout

    @property
    def on_click(self):
        return self.__click_events

    @property
    def on_state_change(self):
        return self.__state_change_events

    @property
    def checkable(self) -> bool:
        return self.qt_widget.isCheckable()

    @checkable.setter
    def checkable(self, value: bool):
        self.qt_widget.setCheckable(value)

    @property
    def checked(self) -> bool:
        return self.qt_widget.isChecked()

    @checked.setter
    def checked(self, value: bool):
        old = self.checked
        self.qt_widget.setChecked(value)
        if value != old:
            self.__state_change_events(value)

    @property
    def popup(self):
        return self.__popup

    @popup.setter
    def popup(self, value: KitBasePopup):
        self.__popup = value

    def __on_click(self, value):
        if self.checkable:
            self.__state_change_events(value)
        if self.__popup:
            pos = self.qt_widget.mapToGlobal(QPoint())
            self.__popup.move(pos.x(), pos.y() + self.height + 5)
            self.__popup.exec()
        self.__click_events()

    @property
    def _layout(self) -> KitLayout:
        return self.__layout

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

    def _apply_style(self):
        super()._apply_style()
        style = self.final_style
        self.__layout.style.spacing = style.spacing
        self.__layout.style.align = style.align
        self.__layout._apply_style()
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
            border: {style.hover.border.width}px {style.hover.border.type} rgba{style.hover.border.color.getRgb()};
            border-top-left-radius: {style.hover.radius.top_left};
            border-top-right-radius: {style.hover.radius.top_right};
            border-bottom-left-radius: {style.hover.radius.bottom_left};
            border-bottom-right-radius: {style.hover.radius.bottom_right};
            padding: {style.hover.padding[0]}px {style.hover.padding[1]}px {style.hover.padding[2]}px {style.hover.padding[3]}px;
        }}
        QPushButton::disabled {{
            color: rgba{style.pressed.color.getRgb()};
            background-color: rgba{style.pressed.background.getRgb()};
            border: {style.pressed.border.width}px {style.pressed.border.type} rgba{style.pressed.border.color.getRgb()};
            border-top-left-radius: {style.pressed.radius.top_left};
            border-top-right-radius: {style.pressed.radius.top_right};
            border-bottom-left-radius: {style.pressed.radius.bottom_left};
            border-bottom-right-radius: {style.pressed.radius.bottom_right};
            padding: {style.pressed.padding[0]}px {style.pressed.padding[1]}px {style.pressed.padding[2]}px {style.pressed.padding[3]}px;
        }}
        QPushButton::checked {{
            color: rgba{style.pressed.color.getRgb()};
            background-color: rgba{style.pressed.background.getRgb()};
            border: {style.pressed.border.width}px {style.pressed.border.type} rgba{style.pressed.border.color.getRgb()};
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
        # print(s)
