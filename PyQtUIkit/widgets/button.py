from PyQt6.QtWidgets import QPushButton

from PyQtUIkit._properties import IntProperty, ColorProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitButton(QPushButton, _KitWidget):
    border = IntProperty(1)
    radius = IntProperty(4)
    text_color = ColorProperty('TextColor')

    def __init__(self, text='', icon=None):
        super().__init__()
        self.__widgets = []
        self.main_palette = 'Main'

        self.setText(text)
        self._icon = icon

    def _apply_theme(self):
        self.setStyleSheet(f"""
QPushButton {{
    color: {self.text_color};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self._tm['Border'].main};
    border-radius: {self.radius}px;
    padding: 3px 8px 3px 8px;
}}
QPushButton::hover {{
    background-color: {self.main_palette.hover};
    border: {self.border}px solid {self._tm['Border'].selected};
}}
QPushButton::disabled {{
    color: {self.main_palette.main};
    border-color: {self._tm['Border'].main};
}}
QPushButton::checked {{
    background-color: {self.main_palette.selected};
    border: {self.border}px solid {self._tm['Border'].selected};
}}
QPushButton::menu-indicator {{
    image: url({1 or self.get_image('buttons/down_arrow')});
    subcontrol-origin: padding;
    padding-right: 5px;
    subcontrol-position: right;
}}""")
        if self._icon is not None:
            self.setIcon(self._tm.icon(self._icon))
