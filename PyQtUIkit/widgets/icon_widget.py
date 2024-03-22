from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget, QSizePolicy

from PyQtUIkit.core.properties import IconProperty, IntProperty, PaletteProperty
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitIconWidget(QWidget, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Transparent')
    border = IntProperty('border', 0)
    radius = IntProperty('radius', 4)
    icon = IconProperty('icon')

    def __init__(self, icon=''):
        super().__init__()
        self.__widgets = []
        self.__painter = QPainter()
        self._icon = icon
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def paintEvent(self, a0) -> None:
        if self._tm and self._tm.active and self.icon:
            self.__painter.begin(self)
            pixmap, width, height = self.icon.resized_pixmap(self.main_palette.text, (self.width(), self.height()))
            self.__painter.drawPixmap((self.width() - width) // 2, (self.height() - height) // 2, width, height, pixmap)
            self.__painter.end()
        super().paintEvent(a0)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {self.main_palette.main};
            border: {self.border}px solid {self._tm.get('Border').main};
            border-radius: {self.radius}px;
        }}
        """)
        self.update()
