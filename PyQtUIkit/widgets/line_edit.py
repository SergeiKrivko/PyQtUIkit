from PyQt6.QtWidgets import QLineEdit

from PyQtUIkit.core import PaletteProperty, EnumProperty, KitFont, FontProperty, MethodsProperty, SignalProperty
from PyQtUIkit.widgets._widget import KitGroupItem as _KitGroupItem


class KitLineEdit(QLineEdit, _KitGroupItem):
    main_palette = PaletteProperty('main_palette', 'Main')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)
    font = FontProperty('font')

    def __init__(self, text=''):
        super().__init__(text)
        self.__widgets = []
        self.border = 1
        self.radius = 4

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFont(self.font.get(self.font_size))
        self.setStyleSheet(f"""
QLineEdit {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self.border_palette.main};
    {self._border_radius_css()}
}}
QLineEdit:hover {{
    border: {self.border}px solid {self.border_palette.hover};
    background-color: {self.main_palette.hover};
}}
QLineEdit:focus {{
    border: {self.border}px solid {self.border_palette.selected};
    background-color: {self.main_palette.hover};
}}""")

    text = MethodsProperty(QLineEdit.text, QLineEdit.setText)
    on_text_changed = SignalProperty('on_text_changed', 'textChanged')
    on_text_edited = SignalProperty('on_text_edited', 'textEdited')
