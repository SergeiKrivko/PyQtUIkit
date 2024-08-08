from typing import Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from PyQtUIkit._core.locale import _KitLocaleString, _KitLocaleStringArray
from PyQtUIkit._widgets.widget import KitWidget
from PyQtUIkit._core.style_obj import LayoutCardStyle
from _core.event import KitSignals
from _widgets.button import KitButton
from _widgets.icon_button import KitIconButton
from _widgets.layout import KitHLayout


class KitCheckbox(KitHLayout):
    def __init__(self,
                 text: str | _KitLocaleString | _KitLocaleStringArray = '',
                 classes: Iterable[str] | str = None,):
        super().__init__(QLabel())
        self.__style = LayoutCardStyle()
        self.__final_style = LayoutCardStyle()
        if classes:
            self.classes = classes
        self.__state = False

        self.__button = KitIconButton()
        self.__button.size = 16
        self.__button.checkable = True
        self.__button.on_click.add(self.__on_clicked)
        self.__button.qt_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.add(self.__button)

        self.__label = KitButton(text, classes='CheckboxLabel')
        self.__label.on_click.add(self.__on_clicked)
        self.__label.qt_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.add(self.__label)

        self.__click_events = KitSignals()
        self.__state_change_events = KitSignals()

    @property
    def on_click(self) -> KitSignals:
        return self.__click_events

    @property
    def on_state_change(self) -> KitSignals:
        return self.__state_change_events

    @property
    def children(self) -> Iterable['KitWidget']:
        yield self.__button
        yield self.__label

    @property
    def style(self) -> LayoutCardStyle:
        return self.__style

    @property
    def final_style(self) -> LayoutCardStyle:
        return self.__final_style

    @property
    def text(self) -> str:
        return self.__label.text

    @text.setter
    def text(self, text: str | _KitLocaleString | _KitLocaleStringArray):
        self.__label.text = text

    @property
    def state(self) -> bool:
        return self.__state

    @state.setter
    def state(self, state: bool):
        self.__state = state
        self.__on_state_changed()

    def __on_clicked(self):
        self.__state = not self.__state
        self.__on_state_changed()
        self.__click_events(self.__state)

    def __on_state_changed(self):
        self.__button.icon = 'line-checkmark' if self.__state else ''
        self.__button.checked = self.__state
        self.__button.apply_style()
        self.__state_change_events(self.__state)

    def apply_lang(self):
        if not self.text:
            self.__label.hide()
        else:
            self.__label.show()
        self.__label.apply_lang()

    def _apply_style(self):
        super()._apply_style()
        self.__label.apply_style()
        self.__button.apply_style()
