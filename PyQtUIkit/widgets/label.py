from PyQt6.QtWidgets import QLabel

from PyQtUIkit.core import IntProperty, PaletteProperty, EnumProperty, FontSize
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitLabel(QLabel, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Transparent')
    border = IntProperty('border', 0)
    radius = IntProperty('radius', 4)
    font_size = EnumProperty('font_size', FontSize, FontSize.MEDIUM)

    def __init__(self, text=''):
        super().__init__(text)
        self._use_text_only = True

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFont(self._tm.font(self.font_size))
        self.setStyleSheet(f"""
        QWidget {{
            color: {self.main_palette.text_only if self._use_text_only else self.main_palette.text};
            background-color: transparent;
            border: none;
        }}""")
