from PyQt6.QtWidgets import QLineEdit

from PyQtUIkit.core.properties import IntProperty, StringProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitLineEdit(QLineEdit, _KitWidget):
    border = IntProperty('border', )
    radius = IntProperty('radius', )

    def __init__(self, text=''):
        super().__init__(text)
        self.__widgets = []
        self.border = 1
        self.radius = 4

    def _apply_theme(self):
        self.setStyleSheet(f"""
QLineEdit {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self._tm.get('Border').main};
    border-radius: {self.radius}px;
}}
QLineEdit:hover {{
    border: {self.border}px solid {self._tm.get('Border').hover};
    background-color: {self.main_palette.hover};
}}
QLineEdit:focus {{
    border: {self.border}px solid {self._tm.get('Border').selected};
    background-color: {self.main_palette.hover};
}}""")
