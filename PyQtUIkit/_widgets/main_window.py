from typing import Iterable

from PyQt6.QtWidgets import QMainWindow, QWidget

from _widgets.layout import KitVLayout
from _widgets.widget import KitWidget
from _core.style_obj import CardStyle


class KitMainWindow(KitWidget):
    def __init__(self,
                 widget: KitWidget = None):
        super().__init__(QMainWindow())

        self.__central_layout = KitVLayout()
        strange_widget = QWidget()
        strange_widget.setLayout(self.__central_layout.qt_widget)

        self.qt_widget.setCentralWidget(strange_widget)

        self.central_widget = widget

        self.on_show.add(self.apply_all)

        self.__style = CardStyle()
        self.__final_style = CardStyle()

    @property
    def qt_widget(self) -> QMainWindow:
        return super().qt_widget

    @property
    def style(self) -> CardStyle:
        return self.__style

    @property
    def final_style(self) -> CardStyle:
        return self.__final_style

    @property
    def children(self) -> Iterable['KitWidget']:
        yield self.central_widget

    @property
    def central_widget(self) -> KitWidget:
        return self.__central_widget

    def show(self):
        self.qt_widget.show()

    def hide(self):
        self.qt_widget.hide()

    @central_widget.setter
    def central_widget(self, widget: KitWidget):
        self.__central_widget = widget
        self.__central_layout.clear()
        if widget:
            self.__central_layout.add(self.__central_widget)

    def apply_all(self):
        self.apply_style()
        self.apply_lang()

    def _apply_style(self):
        super()._apply_style()
        style = self.final_style
        self.qt_widget.setStyleSheet(f"background: rgba{style.background.getRgb()};")
        self.__central_widget._apply_style()

    def apply_lang(self):
        self.__central_widget.apply_lang()
