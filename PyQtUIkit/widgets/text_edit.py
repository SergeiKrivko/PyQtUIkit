from PyQt6.QtWidgets import QTextEdit

from PyQtUIkit.core.properties import IntProperty, PaletteProperty
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitTextEdit(QTextEdit, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Main')
    border = IntProperty('border', 1)
    radius = IntProperty('radius', 4)

    def __init__(self):
        super().__init__()

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFont(self._tm.font_medium)
        self.setStyleSheet(f"""
QTextEdit {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self._tm.get('Border').main};
    border-radius: {self.radius}px;
}}
QTextEdit QScrollBar:vertical {{
    background: {self.main_palette.main};
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    width: 12px;
    margin: 0px;
}}
QTextEdit QScrollBar:horizontal {{
    background: {self.main_palette.main};
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    height: 12px;
    margin: 0px;
}}
QTextEdit QScrollBar::handle::horizontal {{
    background-color: {self._tm.get('Border').main};
    margin: 6px 2px 2px 2px;
    border-radius: 2px;
    min-width: 20px;
}}
QTextEdit QScrollBar::handle::horizontal:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QTextEdit QScrollBar::handle::vertical {{
    background-color: {self._tm.get('Border').main};
    margin: 2px 2px 2px 6px;
    border-radius: 2px;
    min-height: 20px;
}}
QTextEdit QScrollBar::handle::vertical:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QTextEdit QScrollBar::sub-page, QScrollBar::add-page {{
    background: none;
}}
QTextEdit QScrollBar::sub-line, QScrollBar::add-line {{
    background: none;
    height: 0px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}}
""")
