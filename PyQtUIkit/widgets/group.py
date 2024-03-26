from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy

from PyQtUIkit.core.properties import IntProperty, PaletteProperty
from PyQtUIkit.widgets import KitHBoxLayout, KitIconButton, KitVBoxLayout
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget, KitGroup as _KitGroup, KitGroupItem as _KitGroupItem


class KitHGroup(KitHBoxLayout):
    height = IntProperty('height', 24)

    def __init__(self):
        super().__init__()
        self._main_palette = 'Main'
        self._border = 1
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(self.height)
        self.setSpacing(0)
        self.__group = _KitGroup(_KitGroup.HORIZONTAL)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def addItem(self, item: (QWidget, _KitGroupItem)):
        super().addWidget(item)
        self.__group.add_item(item)

    def insertItem(self, index, item: (QWidget, _KitGroupItem)):
        super().insertWidget(index, item)
        self.__group.insert_item(index, item)

    def clear(self):
        super().clear()
        self.__group.clear()

    def _apply_theme(self):
        self.setFixedHeight(self.height + self.contentsMargins().top() + self.contentsMargins().bottom())
        for item in self.__group:
            if isinstance(item, KitIconButton):
                item.size = self.height
            else:
                item.setFixedHeight(self.height)
            item.border = self.border
            item.radius = self.radius
        super()._apply_theme()


class KitVGroup(KitVBoxLayout):
    width = IntProperty('width', 150)

    def __init__(self):
        super().__init__()
        self._main_palette = 'Main'
        self._border = 1
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(self.width)
        self.setSpacing(0)
        self.__group = _KitGroup(_KitGroup.VERTICAL)

    def addItem(self, item: (QWidget, _KitGroupItem)):
        super().addWidget(item)
        self.__group.add_item(item)

    def _apply_theme(self):
        self.setFixedWidth(self.width + self.contentsMargins().left() + self.contentsMargins().right())
        for item in self.__group:
            if isinstance(item, KitIconButton):
                item.size = self.width
            else:
                item.setFixedWidth(self.width)
            item.border = self.border
            item.radius = self.radius
        super()._apply_theme()
