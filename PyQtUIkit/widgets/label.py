from PyQt6.QtWidgets import QLabel

from PyQtUIkit._properties import IntProperty, ColorProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitLabel(QLabel, _KitWidget):
    border = IntProperty()
    radius = IntProperty()
    text_color = ColorProperty('TextColor')

    def __init__(self, text=''):
        super().__init__(text)
        self.__widgets = []
        self.main_palette = 'Transparent'
        self.border = 0
        self.radius = 4

    def _apply_theme(self):
        self.setStyleSheet(f"""
        QWidget {{
            color: {self._tm.get('TextColor')};
            background-color: {self.main_palette.main};
            border: {self.border}px solid {self._tm.get('Border').main};
            border-radius: {self.radius}px;
        }}""")
