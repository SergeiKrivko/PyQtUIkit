from PyQt6.QtWidgets import QLabel

from PyQtUIkit.core.properties import IntProperty, PaletteProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitLabel(QLabel, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Transparent')
    border = IntProperty('border', 0)
    radius = IntProperty('radius', 4)

    def __init__(self, text=''):
        super().__init__(text)

    def _apply_theme(self):
        self.setFont(self._tm.font_small)
        self.setStyleSheet(f"""
        QWidget {{
            color: {self.main_palette.text};
            background-color: {self.main_palette.main};
            border: {self.border}px solid {self._tm.get('Border').main};
            border-radius: {self.radius}px;
        }}""")
