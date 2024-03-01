from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from PyQtUIkit._properties import IntProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitIcon(QLabel, _KitWidget):
    border = IntProperty(0)
    radius = IntProperty(4)

    def __init__(self, icon=''):
        super().__init__()
        self.__widgets = []
        self.main_palette = 'Transparent'
        self._icon = icon
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon):
        self._icon = icon
        if self._tm.active:
            self._apply_theme()

    def _apply_theme(self):
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {self.main_palette.main};
            border: {self.border}px solid {self._tm.get('Border').main};
            border-radius: {self.radius}px;
        }}
        """)
        if self._icon:
            self.setPixmap(self._tm.pixmap(self._icon))
