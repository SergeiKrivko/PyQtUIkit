from typing import Iterable, Callable, Type

from _core.event import KitSignals


class ButtonSequence:
    def __init__(self,
                 button_func: Callable[[str, object, str | None], None] | Type,
                 items: list[str] | list[dict] | list[object] | None = None,
                 name_field='name', value_field='value', icon_field=None,):
        super().__init__()
        self.__items = items or []
        self.__buttons = []
        self.__current = None

        self.__name_field = name_field
        self.__value_field = value_field
        self.__icon_field = icon_field
        self.__button_func = button_func

        self.__current_change_events = KitSignals()
        self.__reload_events = KitSignals()

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        self.__items = value
        self.reload()

    @property
    def buttons(self):
        return self.__buttons

    @property
    def on_reload(self):
        return self.__reload_events

    @property
    def on_current_change(self):
        return self.__current_change_events

    def add(self, button):
        self.__buttons.append(button)
        if self.__current is None:
            self.__set_current(button)
        button.on_click.add(lambda: self.__set_current(button))
        return self

    def insert(self, index, button):
        self.__buttons.insert(index, button)
        if self.__current is None:
            self.__set_current(button)
        button.on_click.add(lambda: self.__set_current(button))
        return self

    def remove(self, button):
        self.pop(self.__buttons.index(button))
        return self

    def pop(self, index):
        if self.__current == self.__buttons[index]:
            if index < len(self.__buttons) - 1:
                self.__set_current(self.__buttons[index + 1])
            elif index:
                self.__set_current(self.__buttons[index - 1])
            else:
                self.__set_current(None)
        self.__buttons.pop(index)
        return self

    def clear(self):
        self.__buttons.clear()
        self.__current = None
        return self

    def reload(self):
        self.clear()
        for el in self.__items:
            if isinstance(el, dict):
                name = el.get(self.__name_field)
                value = el.get(self.__value_field)
                icon = el.get(self.__icon_field)
            elif isinstance(el, str):
                name = value = el
                icon = None
            else:
                name = getattr(el, self.__name_field, '')
                value = getattr(el, self.__value_field, None)
                icon = getattr(el, self.__icon_field, None)
            self.add(self.__button_func(name, value, icon))
        self.__reload_events(self.buttons)

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, value):
        self.__set_current(value)

    def __set_current(self, value):
        if self.__current:
            self.__current.checked = False
        self.__current = value
        if self.__current:
            self.__current.checked = True
        self.__current_change_events(value)
