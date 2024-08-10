from typing import Any, Iterable

from PyQt6.QtWidgets import QWidget, QLayout

from _core.button_sequence import ButtonSequence
from _widgets.buttons.select_button import KitSelectButton
from _widgets.layout.box import KitHBoxLayout
from _widgets.nav_bar import KitNavBar
from _widgets.widget import KitWidget


class KitTabLayout(KitHBoxLayout):
    def __init__(self, tabs: dict[Any: KitWidget],
                 classes: Iterable[str] | str = None):
        super().__init__(classes=classes)
        self.__tabs: dict[Any: KitWidget] = dict()
        self.__current = None
        for key, item in tabs.items():
            self.add(key, item)

    def add(self, value: Any, widget: KitWidget = None):
        if widget is None:
            raise ValueError
        self.__tabs[value] = widget
        widget.hide()
        super().add(widget)
        if self.__current is None:
            self.__set_current(value)

    def clear(self):
        self.__current = None
        self.__tabs.clear()
        super().clear()

    def insert(self, index, widget: KitWidget | QWidget | QLayout):
        raise NotImplementedError

    def pop(self, value: Any):
        res = super().remove(self.__tabs[value])
        self.__tabs.pop(value)
        self.__current = None
        return res

    def remove(self, widget: KitWidget):
        raise NotImplementedError

    def __set_current(self, value: Any):
        if self.__current in self.__tabs:
            self.__tabs[self.__current].hide()
        self.__current = value
        if self.__current in self.__tabs:
            self.__tabs[self.__current].show()

    @property
    def current(self) -> KitWidget:
        return self.__current

    @current.setter
    def current(self, value: Any):
        self.__set_current(value)

    def connect(self, widget: KitSelectButton | KitNavBar):
        sequence: ButtonSequence = widget._sequence
        sequence.on_current_change.add(lambda w: self.__set_current(w.value))



