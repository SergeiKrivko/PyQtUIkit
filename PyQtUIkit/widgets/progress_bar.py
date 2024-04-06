from enum import Enum

from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtWidgets import QProgressBar

from PyQtUIkit.core import IntProperty, PaletteProperty, BoolProperty, EnumProperty, KitFont, FontProperty
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitProgressBar(QProgressBar, _KitWidget):
    class Mode(Enum):
        SMALL = 0
        LARGE = 1

    main_palette = PaletteProperty('main_palette', 'Main')
    border = IntProperty('border', 1)
    radius = IntProperty('radius', 4)
    animations = BoolProperty('animations', True)
    mode = EnumProperty('mode', Mode, Mode.LARGE)
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)
    font = FontProperty('font')

    def __init__(self):
        super().__init__()
        self.__anim = None
        self.__text_visible = True

    def setValue(self, value: int) -> None:
        if isinstance(self.__anim, QPropertyAnimation):
            self.__anim.stop()
        if self.animations:
            self.__anim = QPropertyAnimation(self, b'value')
            self.__anim.setEndValue(value)
            self.__anim.setDuration(400)
            self.__anim.start()
        else:
            self.setValue(value)
            
    def setTextVisible(self, visible: bool) -> None:
        self.__text_visible = visible
        if self.mode == KitProgressBar.Mode.LARGE:
            super().setTextVisible(visible)
        else:
            super().setTextVisible(False)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFont(self.font.get(self.font_size))
        if self.mode == KitProgressBar.Mode.LARGE:
            self.setFixedHeight(24)
            self.setTextVisible(self.__text_visible)
            self.setStyleSheet(f"""
QProgressBar {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self.border_palette.main};
    border-radius: {self.radius}px;
    text-align: center;
}}
QProgressBar::chunk {{
    background-color: {self.main_palette.selected};
    border-radius: {self.radius}px;
}}
""")
        else:
            self.setFixedHeight(4)
            self.setTextVisible(False)
            self.setStyleSheet(f"""
QProgressBar {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: 0px solid black;
    border-radius: 2px;
    text-align: center;
}}
QProgressBar::chunk {{
    background-color: {self.main_palette.selected};
    border-radius: 2px;
}}
""")
