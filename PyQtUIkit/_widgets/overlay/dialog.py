from typing import Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QDialog

from PyQtUIkit._widgets.widget import KitWidget
from PyQtUIkit._core.style_obj import CardStyle
from PyQtUIkit._widgets.layout.base import KitVLayout
from PyQtUIkit._widgets.overlay.dialog_header import KitDialogHeader


class KitDialog(KitWidget):
    def __init__(self,
                 header_or_content: KitDialogHeader | KitWidget = None,
                 content: KitWidget = None,
                 classes: Iterable[str] | str = None, ):
        super().__init__(QDialog())
        self.qt_widget.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        strange_layout = QHBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.qt_widget.setLayout(strange_layout)
        self.__strange_widget = QWidget()
        strange_layout.addWidget(self.__strange_widget)
        self.__layout = KitVLayout()
        self.__strange_widget.setLayout(self.__layout.qt_widget)

        if isinstance(header_or_content, KitDialogHeader):
            self.__header = header_or_content
            self.__content = content
        elif content:
            raise TypeError("Duplicated content")
        else:
            self.__header = None
            self.__content = header_or_content

        if self.__header is not None:
            self.__layout.add(self.__header)
            self.__header.on_reject.add(self.qt_widget.reject)
        if self.__content is not None:
            self.__layout.add(self.__content)

        self.__style = CardStyle()
        self.__final_style = CardStyle()
        if classes:
            self.classes = classes

        self.__moving = False
        self.__last_pos = None
        self.on_mouse_press.add(self.__on_mouse_press)
        self.on_mouse_move.add(self.__on_mouse_move)
        self.on_mouse_release.add(self.__on_mouse_release)

    @property
    def qt_widget(self) -> QDialog:
        return super().qt_widget

    @property
    def style(self) -> CardStyle:
        return self.__style

    @property
    def final_style(self) -> CardStyle:
        return self.__final_style

    @property
    def children(self) -> Iterable['KitWidget']:
        yield self.__layout

    @property
    def header(self) -> KitDialogHeader:
        return self.__header

    @header.setter
    def header(self, value: KitDialogHeader):
        if isinstance(self.__header, KitDialogHeader):
            self.__layout.remove(self.__header)
            self.__header.on_reject.remove(self.qt_widget.reject)
        self.__header = value
        self.__layout.insert(0, self.__header)
        self.__header.on_reject.add(self.qt_widget.reject)

    @property
    def content(self) -> KitWidget:
        return self.__content

    @content.setter
    def content(self, value: KitWidget):
        if self.__content is not None:
            self.__layout.remove(self.__content)
        self.__content = value
        self.__layout.add(self.__content)

    def exec(self):
        self.apply_style()
        self.apply_lang()
        return self.qt_widget.exec()

    def __on_mouse_press(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.__moving = True
            self.__last_pos = a0.pos()

    def __on_mouse_release(self, a0) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.__moving = False
            self.__last_pos = None

    def __on_mouse_move(self, a0) -> None:
        if self.__moving:
            self.move(self.qt_widget.pos() + a0.pos() - self.__last_pos)

    def _apply_style(self):
        super()._apply_style()
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
        self.__layout._apply_style()

    def apply_lang(self):
        self.__layout.apply_lang()
