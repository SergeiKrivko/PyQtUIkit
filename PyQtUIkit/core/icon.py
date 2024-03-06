from PyQt6.QtGui import QPixmap, QImage, QIcon

from PyQtUIkit.themes import SVG


class KitIcon:
    def __init__(self, file='', data=''):
        if not data and not file:
            raise TypeError("need file or data")
        self._file = file
        self._data = data

    def _get_data(self):
        if self._data:
            return self._data
        with open(self._file, encoding='utf-8') as f:
            return f.read()

    def pixmap(self, color, size=None):
        icon = SVG(self._get_data())
        icon.change_color(color)
        if size:
            icon.resize(*size)
        return QPixmap.fromImage(QImage.fromData(icon.bytes()))

    def resized_pixmap(self, color, size):
        icon = SVG(self._get_data())
        icon.change_color(color)
        width, height = icon.resize(*size)
        return QPixmap.fromImage(QImage.fromData(icon.bytes())), width, height

    def icon(self, color=None, size=None):
        return QIcon(self.pixmap(color, size))
