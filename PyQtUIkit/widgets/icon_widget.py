from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget

from PyQtUIkit.core.properties import IconProperty, IntProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitIconWidget(QWidget, _KitWidget):
    border = IntProperty('border', 0)
    radius = IntProperty('radius', 4)
    icon = IconProperty('icon')

    def __init__(self, icon=''):
        super().__init__()
        self.__widgets = []
        self.main_palette = 'Transparent'
        self.__painter = QPainter()
        self._icon = icon

    def paintEvent(self, a0) -> None:
        if self.icon:
            self.__painter.begin(self)
            self.__painter.drawPixmap(0, 0, self.width(), self.height(),
                                      self.icon.pixmap(self.main_palette.text, size=(self.width(), self.height())))
            self.__painter.end()
        super().paintEvent(a0)

    def _apply_theme(self):
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {self.main_palette.main};
            border: {self.border}px solid {self._tm.get('Border').main};
            border-radius: {self.radius}px;
        }}
        """)
        self.update()
