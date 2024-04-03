from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QListWidget, QListWidgetItem

from PyQtUIkit.core.properties import IntProperty, IconProperty
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitListWidget(QListWidget, _KitWidget):
    border = IntProperty('border', 1)
    radius = IntProperty('radius', 4)

    def __init__(self):
        super().__init__()
        self.__widgets = []

    def _set_tm(self, tm):
        super()._set_tm(tm)
        for i in range(self.count()):
            item = self.item(i)
            if isinstance(item, KitListWidgetItem):
                item._set_tm(tm)

    def addItem(self, aitem) -> None:
        super().addItem(aitem)
        if isinstance(aitem, _KitWidget):
            aitem._set_tm(self._tm)

    def insertItem(self, row: int, item) -> None:
        super().insertItem(row, item)
        if isinstance(item, KitListWidgetItem):
            item._set_tm(self._tm)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setStyleSheet(f"""
QListWidget {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self.border_palette.main};
    border-radius: {self.radius}px;
}}
QListWidget::item {{
    border-radius: 6px;
}}
QListWidget::item:hover {{
    background-color: {self.main_palette.hover};
}}
QListWidget::item:selected {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.selected};
    border-radius: 6px;
}}
QListWidget QScrollBar:vertical {{
    background: {self.main_palette.main};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    width: 12px;
    margin: 0px;
}}
QListWidget QScrollBar:horizontal {{
    background: {self.main_palette.main};
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    height: 12px;
    margin: 0px;
}}
QListWidget QScrollBar::handle::vertical {{
    background-color: {self.border_palette.main};
    margin: 2px 2px 2px 6px;
    border-radius: 2px;
    min-height: 20px;
}}
QListWidget QScrollBar::handle::vertical:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QListWidget QScrollBar::handle::horizontal {{
    background-color: {self.border_palette.main};
    margin: 6px 2px 2px 2px;
    border-radius: 2px;
    min-width: 20px;
}}
QListWidget QScrollBar::handle::horizontal:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QListWidget QScrollBar::sub-page, QScrollBar::add-page {{
    background: none;
}}
QListWidget QScrollBar::sub-line, QScrollBar::add-line {{
    background: none;
    height: 0px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}}
""")
        for i in range(self.count()):
            item = self.item(i)
            if isinstance(item, KitListWidgetItem):
                item._apply_theme()


class KitListWidgetItem(QListWidgetItem, _KitWidget):
    icon = IconProperty('icon')

    def __init__(self, text, icon=''):
        super().__init__()
        self.setText(text)
        self._icon = icon

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setForeground(QColor(self.main_palette.text_only))
        if self.icon:
            self.setIcon(self.icon.icon(self.main_palette.text_only))
