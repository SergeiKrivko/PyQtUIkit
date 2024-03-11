from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtWidgets import QProgressBar

from PyQtUIkit.core.properties import IntProperty, PaletteProperty, BoolProperty, StringProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitProgressBar(QProgressBar, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Main')
    border = IntProperty('border', 1)
    radius = IntProperty('radius', 4)
    animations = BoolProperty('animations', True)
    mode = StringProperty('mode', 'l')

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
        if self.mode == 'l':
            super().setTextVisible(visible)
        else:
            super().setTextVisible(False)

    def _apply_theme(self):
        self.setFont(self._tm.font_small)
        if self.mode == 'l':
            self.setFixedHeight(24)
            self.setTextVisible(self.__text_visible)
            self.setStyleSheet(f"""
QProgressBar {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self._tm['Border'].main};
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
