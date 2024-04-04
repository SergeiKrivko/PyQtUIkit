from PyQt6.QtWidgets import QWidget

from PyQtUIkit.core import IntProperty
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitHSeparator(QWidget, _KitWidget):
    border = IntProperty('border', 1)

    def __init__(self):
        super().__init__()
        self._use_text_only = True
        self.setFixedHeight(self.border)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFixedHeight(self.border)
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {self.border_palette.main};
            border: none;
        }}""")


class KitVSeparator(QWidget, _KitWidget):
    border = IntProperty('border', 1)

    def __init__(self):
        super().__init__()
        self._use_text_only = True
        self.setFixedWidth(self.border)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFixedWidth(self.border)
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {self.border_palette.main};
            border: none;
        }}""")
