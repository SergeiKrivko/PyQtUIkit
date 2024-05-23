from functools import lru_cache

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

    def __eq__(self, other):
        if not isinstance(other, KitIcon):
            return False
        if self._data:
            return self._data == other._data
        return self._file == other._file

    def pixmap(self, color, size=None):
        return KitIcon._pixmap(self._get_data(), color, size)[0]

    def resized_pixmap(self, color, size):
        return KitIcon._pixmap(self._get_data(), color, size)

    @staticmethod
    @lru_cache
    def _pixmap(data, color, size=None):
        icon = SVG(data)
        icon.change_color(color)
        if size:
            width, height = icon.resize(*size)
        else:
            width, height = None, None
        return QPixmap.fromImage(QImage.fromData(icon.bytes())), width, height

    def icon(self, color=None, size=None):
        return QIcon(self.pixmap(color, size))
