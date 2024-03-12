from PyQt6.QtWidgets import QLineEdit

from PyQtUIkit.core.properties import PaletteProperty
from PyQtUIkit.widgets._widget import KitGroupItem as _KitGroupItem


class KitLineEdit(QLineEdit, _KitGroupItem):
    main_palette = PaletteProperty('main_palette', 'Main')

    def __init__(self, text=''):
        super().__init__(text)
        self.__widgets = []
        self.border = 1
        self.radius = 4

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFont(self._tm.font_medium)
        self.setStyleSheet(f"""
QLineEdit {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self._tm.get('Border').main};
    {self._border_radius_css()}
}}
QLineEdit:hover {{
    border: {self.border}px solid {self._tm.get('Border').hover};
    background-color: {self.main_palette.hover};
}}
QLineEdit:focus {{
    border: {self.border}px solid {self._tm.get('Border').selected};
    background-color: {self.main_palette.hover};
}}""")
