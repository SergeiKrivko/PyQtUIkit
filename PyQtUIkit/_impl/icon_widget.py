from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget, QSizePolicy

from _core.icon import KitIcon
from _core.icons import icons


class IconWidget(QWidget):
    def __init__(self, icon=''):
        super().__init__()
        self.__painter = QPainter()
        self.__icon = icon
        self.__color = QColor(0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    @property
    def icon(self) -> KitIcon | None:
        if not self.__icon:
            return None
        if isinstance(self.__icon, str):
            return KitIcon(data=icons[self.__icon])
        if isinstance(self.__icon, KitIcon):
            return self.__icon
        return None

    @icon.setter
    def icon(self, icon: str | KitIcon):
        self.__icon = icon

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color: QColor | str):
        self.__color = QColor(color)

    def paintEvent(self, a0) -> None:
        if self.icon:
            self.__painter.begin(self)
            pixmap, width, height = self.icon.resized_pixmap(self.color.name(), (self.width(), self.height()))
            self.__painter.drawPixmap((self.width() - width) // 2, (self.height() - height) // 2, width, height, pixmap)
            self.__painter.end()
        super().paintEvent(a0)
