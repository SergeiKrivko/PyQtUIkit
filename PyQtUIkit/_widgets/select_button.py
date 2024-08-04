from typing import Iterable

from _core.button_sequence import ButtonSequence
from _core.style_obj import ButtonStyle
from _widgets.button import KitButton
from _widgets.group import KitHGroup


class KitSelectButton(KitHGroup):
    def __init__(self,
                 items: list[str] | list[dict] | list[object] | None = None,
                 name_field='name', value_field='value', icon_field=None,
                 classes: Iterable[str] | str = None, ):
        super().__init__(classes=classes)
        self.__sequence = ButtonSequence(_KitSelectButtonItem, items=items, name_field=name_field,
                                         value_field=value_field, icon_field=icon_field)
        self.__sequence.on_reload.add(self.__reload)
        self.__style = ButtonStyle()
        self.__final_style = ButtonStyle()

        self.__sequence.reload()

    @property
    def style(self) -> ButtonStyle:
        return self.__style

    @property
    def final_style(self) -> ButtonStyle:
        return self.__final_style

    def __reload(self):
        self.clear()
        for el in self.__sequence.buttons:
            self.add(el)

    def _apply_style(self):
        for el in self.__sequence.buttons:
            for cl in ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'contrast', 'fill', 'text',
                       'outline']:
                if cl in self.classes:
                    el.classes.add(cl)
                else:
                    el.classes.discard(cl)
        super()._apply_style()


class _KitSelectButtonItem(KitButton):
    def __init__(self, name, value, icon):
        super().__init__(name, icon)
        self.__value = value
        self.checkable = True

    @property
    def value(self):
        return self.__value
