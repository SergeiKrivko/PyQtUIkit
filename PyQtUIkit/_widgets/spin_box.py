from typing import Iterable

from PyQtUIkit._core.locale import _KitLocaleString, _KitLocaleStringArray
from PyQtUIkit._core.event import KitSignals
from PyQtUIkit._core.style_obj import ButtonStyle
from PyQtUIkit._widgets.group import KitHGroup, KitVGroup
from PyQtUIkit._widgets.icon_button import KitIconButton
from PyQtUIkit._widgets.line_edit import KitLineEdit


class KitSpinBox(KitHGroup):
    def __init__(self,
                 placeholder: str | _KitLocaleString | _KitLocaleStringArray = None,
                 classes: Iterable[str] | str = None, ):
        super().__init__(classes=classes)
        self.__placeholder = placeholder
        self.__style = ButtonStyle()
        self.__final_style = ButtonStyle()

        self.__line_edit = KitLineEdit()
        self.add(self.__line_edit)

        self.__group = KitVGroup()
        self.add(self.__group)

        self.__button_up = KitIconButton('line-chevron-up')
        self.__button_up.width = 24
        self.__group.add(self.__button_up)

        self.__button_down = KitIconButton('line-chevron-down')
        self.__button_down.width = 24
        self.__group.add(self.__button_down)
        
        self.__func = int
        self.__min = 0
        self.__max = 100
        self.__step = 1
        
        self.__last_text = '0'
        self._last_pos = 0
        self._value_changed = False

        self.__value_change_events = KitSignals()
        self.__value_edit_events = KitSignals()
        self.__editing_finished_events = KitSignals()
        self.__return_pressed_events = KitSignals()
        self.__cursor_pos_events = KitSignals()

        self.__line_edit.on_cursor_position_changed.add(self.__on_cursor_moved)
        self.__line_edit.on_editing_finished.add(self.__on_editing_finished)
        self.__line_edit.on_editing_finished.add(self.__editing_finished_events)
        self.__line_edit.on_text_edit.add(self.__on_text_edited)
        self.__line_edit.on_return_pressed.add(self.__return_pressed_events)
        self.__line_edit.on_cursor_position_changed.add(self.__cursor_pos_events)
        self.__button_up.on_click.add(self.__increase)
        self.__button_down.on_click.add(self.__decrease)

    @property
    def style(self) -> ButtonStyle:
        return self.__style

    @property
    def final_style(self) -> ButtonStyle:
        return self.__final_style

    @property
    def placeholder(self) -> str:
        if self.__placeholder is None:
            return ''
        if isinstance(self.__placeholder, str):
            return self.__placeholder
        return self.__placeholder.get()

    @placeholder.setter
    def placeholder(self, placeholder: str | _KitLocaleString | _KitLocaleStringArray):
        self.__placeholder = placeholder
        self.apply_lang()
        
    @property
    def min(self) -> int | float:
        return self.__min
    
    @min.setter
    def min(self, min: int | float):
        self.__min = min
        
    @property
    def max(self) -> int | float:
        return self.__max
    
    @max.setter
    def max(self, max: int | float):
        self.__max = max
    
    @property
    def step(self) -> int | float:
        return self.__step
    
    @step.setter
    def step(self, step: int | float):
        self.__step = step
        
    @property
    def value(self) -> int | float:
        if not self.__line_edit.text:
            return 0
        return self.__func(self.__line_edit.text)
    
    @value.setter
    def value(self, value: int | float):
        self.__line_edit.text = str(value)
        self.__fix_value()

    @property
    def on_value_changed(self):
        return self.__value_change_events

    @property
    def on_value_edited(self):
        return self.__value_edit_events

    def __on_text_edited(self):
        value = 0 if not self.__last_text else self.__func(self.__last_text)
        self.__fix_value()
        if value != self.value:
            self._value_changed = True

    def __fix_value(self):
        text = self.__line_edit.text
        try:
            value = 0 if text in ['', '+', '-'] else self.__func(text)
        except ValueError:
            pos = self._last_pos
            self.__line_edit.text = self.__last_text
            self._last_pos = pos
            self.__line_edit.qt_widget.setCursorPosition(self._last_pos)
        else:
            if text and value < self.min:
                self.__last_text = str(self.min)
                self.__line_edit.text = self.__last_text
            elif text and value > self.max:
                self.__last_text = str(self.max)
                self.__line_edit.text = self.__last_text
            else:
                self.__last_text = text
            self.__value_change_events(value)
            self._last_pos = self.__line_edit.qt_widget.cursorPosition()

    def __on_cursor_moved(self):
        self._last_pos = self.__line_edit.qt_widget.cursorPosition()

    def __on_editing_finished(self):
        text = self.__line_edit.text
        if not text:
            self.__line_edit.text = '0'
            self.__on_text_edited()
        if self._value_changed:
            self.__value_edit_events(self.value)
            self._value_changed = False

    def __decrease(self):
        self.value = round(self.value - self.step, 2)
        self.__value_edit_events(self.value)
        self._value_changed = False

    def __increase(self):
        self.value = round(self.value + self.step, 2)
        self.__value_edit_events(self.value)
        self._value_changed = False

    def apply_lang(self):
        self.__line_edit.qt_widget.setPlaceholderText(self.placeholder)

    def _apply_style(self):
        for child in [self.__line_edit, self.__button_up, self.__button_down]:
            child.classes.clear()
            for el in ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'contrast']:
                if el in self.classes:
                    child.classes.add(el)
        self.__button_up.classes.add('outline')
        self.__button_down.classes.add('outline')
        super()._apply_style()

