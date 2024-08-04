from typing import Iterable

from PyQt6.QtCore import QSize

from _core.icon import KitIcon
from _widgets.icon_widget import KitIconWidget
from _widgets.layout_button import KitLayoutButton


class KitIconButton(KitLayoutButton):

    def __init__(self,
                 icon: KitIcon | str = None,
                 checkable: bool = False,
                 size: QSize | tuple[int, int] | int = None,
                 classes: Iterable[str] | str = None):
        super().__init__(checkable=checkable, classes=classes)
        self.qt_widget.setMinimumSize(12, 12)

        self.__icon_widget = KitIconWidget(icon)
        self.add(self.__icon_widget)

        self.on_click.add(self.__on_click)
        if size is not None:
            self.size = size

    @property
    def icon(self) -> KitIcon | None:
        return self.__icon_widget.icon

    @icon.setter
    def icon(self, icon: KitIcon | str | None):
        self.__icon_widget.icon = icon

    def __on_click(self, status):
        if status:
            self.__icon_widget.classes.add('pressed')
        else:
            self.__icon_widget.classes.discard('pressed')
        self.__icon_widget._apply_style()

    def _apply_style(self):
        if 'auto-padding' in self.classes:
            self._layout.style.padding = min(self.width, self.height) // 6
        super()._apply_style()
