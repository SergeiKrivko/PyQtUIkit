from PyQt6.QtWidgets import QLabel

from PyQtUIkit.core.properties import IntProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitLabel(QLabel, _KitWidget):
    border = IntProperty('border', )
    radius = IntProperty('radius', )

    def __init__(self, text=''):
        super().__init__(text)
        self.main_palette = 'Transparent'
        self.border = 0
        self.radius = 4

    def _apply_theme(self):
        self.setStyleSheet(f"""
        QWidget {{
            color: {self.main_palette.text};
            background-color: {self.main_palette.main};
            border: {self.border}px solid {self._tm.get('Border').main};
            border-radius: {self.radius}px;
        }}""")
