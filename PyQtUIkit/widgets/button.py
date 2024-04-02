from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QVBoxLayout

from PyQtUIkit.core import IconProperty, EnumProperty, IntProperty, PaletteProperty, KitFont, FontProperty, \
    SignalProperty, MethodsProperty
from PyQtUIkit.themes import ThemeManager
from PyQtUIkit.widgets import KitIconWidget
from PyQtUIkit.widgets._widget import KitGroupItem as _KitGroupItem


class KitButton(QPushButton, _KitGroupItem):
    main_palette = PaletteProperty('main_palette', 'Main')
    icon = IconProperty('icon')
    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)
    on_click = SignalProperty('on_click', 'clicked')

    def __init__(self, text='', icon=None):
        super().__init__()
        self.__widgets = []
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setText(text)
        self._icon = icon

        self._build_from_kui()

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFont(self.font.get(self.font_size))
        self.setStyleSheet(f"""
QPushButton {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self.border_palette.main};
    {self._border_radius_css()}
    padding: 3px 8px 3px 8px;
}}
QPushButton::hover {{
    background-color: {self.main_palette.hover};
    border: {self.border}px solid {self.border_palette.selected};
}}
QPushButton::disabled {{
    color: {self.main_palette.main};
    border-color: {self.border_palette.main};
}}
QPushButton::checked {{
    background-color: {self.main_palette.selected};
    border: {self.border}px solid {self.border_palette.selected};
}}
QPushButton::menu-indicator {{
    image: none;
    subcontrol-origin: padding;
    padding-right: 5px;
    subcontrol-position: right;
}}""")
        if self.icon is not None:
            self.setIcon(self.icon.icon(self.main_palette.text))

    text = MethodsProperty(QPushButton.text, QPushButton.setText)


class KitIconButton(QPushButton, _KitGroupItem):
    main_palette = PaletteProperty('main_palette', 'Main')
    icon = IconProperty('icon')

    def __init__(self, icon=''):
        super().__init__()
        self.__widgets = []
        self._icon = icon
        self._main_palette = 'Main'
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        self._icon_label = KitIconWidget()
        self._icon_label._use_text_only = False
        self.__layout.addWidget(self._icon_label)

    def _set_tm(self, tm: ThemeManager):
        super()._set_tm(tm)
        self._icon_label._set_tm(tm)

    def _set_size(self, x, y=None):
        if isinstance(x, int) and isinstance(y, int):
            self.setFixedSize(x, y)
        elif y is None:
            self.setFixedSize(x, x)
        else:
            self.setFixedSize(x)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self._icon_label.icon = self.icon
        self._icon_label._main_palette = self._main_palette
        self.__layout.setContentsMargins(*[min(self.width(), self.height()) // 5] * 4)
        self.setStyleSheet(f"""
QPushButton {{
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self.border_palette.main};
    {self._border_radius_css()}
    padding: 3px 8px 3px 8px;
}}
QPushButton::hover {{
    background-color: {self.main_palette.hover};
    border: {self.border}px solid {self.border_palette.selected};
}}
QPushButton::disabled {{
    color: {self.main_palette.main};
    border-color: {self.border_palette.main};
}}
QPushButton::checked {{
    background-color: {self.main_palette.selected};
    border: {self.border}px solid {self.border_palette.selected};
}}
QPushButton::menu-indicator {{
    image: none;
    subcontrol-position: right;
}}""")

    size = MethodsProperty(QPushButton.size, _set_size)
