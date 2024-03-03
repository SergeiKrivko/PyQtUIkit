from PyQt6.QtWidgets import QPushButton, QVBoxLayout

from PyQtUIkit.core.properties import IntProperty, ColorProperty, PaletteProperty

from PyQtUIkit.core.properties import IconProperty
from PyQtUIkit.themes import ThemeManager
from PyQtUIkit.widgets import KitIconWidget
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitButton(QPushButton, _KitWidget):
    main_palette = PaletteProperty('Main')
    border = IntProperty('border', 1)
    radius = IntProperty('radius', 4)
    icon = IconProperty('icon')

    def __init__(self, text='', icon=None):
        super().__init__()
        self.__widgets = []

        self.setText(text)
        self._icon = icon

    def _apply_theme(self):
        self.setStyleSheet(f"""
QPushButton {{
    color: {self.main_palette.text};
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
    image: none;
    subcontrol-origin: padding;
    padding-right: 5px;
    subcontrol-position: right;
}}""")
        if self.icon is not None:
            self.setIcon(self.icon.icon(self.main_palette.text))


class KitIconButton(QPushButton, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Main')
    border = IntProperty('border', 1)
    radius = IntProperty('radius', 4)
    size = IntProperty('size', 24)
    icon = IconProperty('icon')

    def __init__(self, icon=''):
        super().__init__()
        self.__widgets = []
        self._icon = icon

        layout = QVBoxLayout()
        layout.setContentsMargins(*[min(6, self.size // 5)] * 4)
        self.setLayout(layout)

        self._icon_label = KitIconWidget()
        layout.addWidget(self._icon_label)

    def _set_tm(self, tm: ThemeManager):
        super()._set_tm(tm)
        self._icon_label._set_tm(tm)

    def _apply_theme(self):
        self._icon_label.icon = self.icon
        self.setFixedSize(self.size, self.size)
        self.setStyleSheet(f"""
QPushButton {{
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
}}""")
