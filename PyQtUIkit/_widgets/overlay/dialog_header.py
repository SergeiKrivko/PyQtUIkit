from typing import Iterable

from PyQtUIkit._widgets.layout.base import KitHLayout
from _core.event import KitSignals
from _core.locale import _KitLocaleString, _KitLocaleStringArray
from _widgets.buttons.icon_button import KitIconButton
from _widgets.card import KitCard
from _widgets.label import KitLabel


class KitDialogHeader(KitCard):
    def __init__(self,
                 name: str | _KitLocaleString | _KitLocaleStringArray,
                 classes: Iterable[str] | str = None):
        super().__init__(KitHLayout(), classes=classes)

        self.__label = KitLabel(name, classes='h4')
        self.layout.add(self.__label)

        self.__button = KitIconButton('line-close', classes='text contrast')
        self.__button.size = 24
        self.__button.on_click.add(lambda: self.__reject_events())
        self.layout.add(self.__button)

        self.__reject_events = KitSignals()

    @property
    def on_reject(self):
        return self.__reject_events

    def _apply_style(self):
        super()._apply_style()
