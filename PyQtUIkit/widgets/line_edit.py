from PyQt6.QtWidgets import QLineEdit

from PyQtUIkit._properties import IntProperty, StringProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitLineEdit(QLineEdit, _KitWidget):
    border = IntProperty()
    radius = IntProperty()
    text_color = StringProperty()

    def __init__(self, text=''):
        super().__init__(text)
        self.__widgets = []
        self.text_color = 'TextColor'
        self.border = 1
        self.radius = 4

    def _apply_theme(self):
        self.setStyleSheet(f"""
QLineEdit {{
    color: {self._tm.get('TextColor')};
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
