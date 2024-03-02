from PyQt6.QtWidgets import QWidget, QHBoxLayout, QListWidget

from PyQtUIkit.core.properties import IntProperty, StringProperty, ColorProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitListWidget(QListWidget, _KitWidget):
    border = IntProperty('border', )
    radius = IntProperty('radius', )

    def __init__(self):
        super().__init__()
        self.__widgets = []
        self.border = 1
        self.radius = 4

    def _apply_theme(self):
        self.setStyleSheet(f"""
QListWidget {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self._tm.get('Border').main};
    border-radius: {self.radius}px;
}}
QListWidget::item {{
    border-radius: 6px;
}}
QListWidget::item:hover {{
    background-color: {self.main_palette.hover};
}}
QListWidget::item:selected {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.selected};
    border-radius: 6px;
}}
QListWidget QScrollBar:vertical {{
    background: {self.main_palette.main};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    width: 12px;
    margin: 0px;
}}
QListWidget QScrollBar:horizontal {{
    background: {self.main_palette.main};
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    height: 12px;
    margin: 0px;
}}
QListWidget QScrollBar::handle::vertical {{
    background-color: {self._tm['Border'].main};
    margin: 2px 2px 2px 6px;
    border-radius: 2px;
    min-height: 20px;
}}
QListWidget QScrollBar::handle::vertical:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QListWidget QScrollBar::handle::horizontal {{
    background-color: {self._tm['Border'].main};
    margin: 6px 2px 2px 2px;
    border-radius: 2px;
    min-width: 20px;
}}
QListWidget QScrollBar::handle::horizontal:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QListWidget QScrollBar::sub-page, QScrollBar::add-page {{
    background: none;
}}
QListWidget QScrollBar::sub-line, QScrollBar::add-line {{
    background: none;
    height: 0px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}}
""")
