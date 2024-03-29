from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QVBoxLayout

from PyQtUIkit.core.properties import IconProperty, LiteralProperty
from PyQtUIkit.core.properties import IntProperty, PaletteProperty
from PyQtUIkit.themes import ThemeManager
from PyQtUIkit.widgets import KitIconWidget
from PyQtUIkit.widgets._widget import KitGroupItem as _KitGroupItem


class KitButton(QPushButton, _KitGroupItem):
    main_palette = PaletteProperty('main_palette', 'Main')
    icon = IconProperty('icon')
    font_size = LiteralProperty('font_size', ['medium', 'small', 'big'])

    def __init__(self, text='', icon=None):
        super().__init__()
        self.__widgets = []
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setText(text)
        self._icon = icon

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFont(self._tm.font(self.font_size))
        self.setStyleSheet(f"""
QPushButton {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self._tm['Border'].main};
    {self._border_radius_css()}
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


class KitIconButton(QPushButton, _KitGroupItem):
    main_palette = PaletteProperty('main_palette', 'Main')
    size = IntProperty('size', 24)
    icon = IconProperty('icon')

    def __init__(self, icon=''):
        super().__init__()
        self.__widgets = []
        self._icon = icon
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        self._icon_label = KitIconWidget()
        self.__layout.addWidget(self._icon_label)

    def _set_tm(self, tm: ThemeManager):
        super()._set_tm(tm)
        self._icon_label._set_tm(tm)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self._icon_label.icon = self.icon
        self.setFixedSize(self.size, self.size)
        self.__layout.setContentsMargins(*[self.size // 5] * 4)
        self.setStyleSheet(f"""
QPushButton {{
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self._tm['Border'].main};
    {self._border_radius_css()}
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
    subcontrol-position: right;
}}""")
