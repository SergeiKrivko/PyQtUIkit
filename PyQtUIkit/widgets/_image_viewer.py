from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap
from PyQtUIkit.core.properties import FloatProperty

from PyQtUIkit.widgets import KitScrollArea, KitLabel, KitHBoxLayout


class KitImageViewer(KitScrollArea):
    min_zoom = FloatProperty('min_zoom', 1.0)
    max_zoom = FloatProperty('max_zoom', 32.0)

    def __init__(self):
        super().__init__()

        layout = KitHBoxLayout()
        layout.alignment = Qt.AlignmentFlag.AlignCenter
        self.setWidget(layout)

        self._label = KitLabel(self)
        layout.addWidget(self._label)

        self._initial_pixmap = QPixmap()
        self._pixmap = QPixmap()

        self._zoom = 1.0
        self._pos = None

    def _apply_pixmap(self):
        if self.width() / self.height() > self._initial_pixmap.width() / self._initial_pixmap.height():
            height = self.height()
            width = height * self._initial_pixmap.width() / self._initial_pixmap.height()
        else:
            width = self.width()
            height = width * self._initial_pixmap.height() / self._initial_pixmap.width()

        width = int(width * self._zoom)
        height = int(height * self._zoom)

        self._pixmap = self._initial_pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio,
                                                   Qt.TransformationMode.SmoothTransformation)
        self._label.setPixmap(self._pixmap)
        self._label.setFixedSize(self._pixmap.size())

    def zoom_in(self, pos: QPoint = None):
        self._set_zoom(min(self.max_zoom, self._zoom * 1.5), pos)

    def zoom_out(self, pos: QPoint = None):
        self._set_zoom(max(self.min_zoom, self._zoom / 1.5), pos)

    def _set_zoom(self, new_zoom, pos: QPoint = None):
        old_zoom = self._zoom
        self._zoom = new_zoom

        if pos:
            canvass_x = (self.horizontalScrollBar().value() + pos.x()) / old_zoom
            canvass_y = (self.verticalScrollBar().value() + pos.y()) / old_zoom
            self._apply_pixmap()
            self.horizontalScrollBar().setValue(int(canvass_x * new_zoom - pos.x()))
            self.verticalScrollBar().setValue(int(canvass_y * new_zoom - pos.y()))
        else:
            self._apply_pixmap()

    def wheelEvent(self, a0):
        super().wheelEvent(a0)
        if a0.angleDelta().y() > 0:
            self.zoom_in(a0.position())
        else:
            self.zoom_out(a0.position())

    def mousePressEvent(self, a0):
        if a0.button() == Qt.MouseButton.LeftButton:
            self._pos = a0.position()
        else:
            super().mousePressEvent(a0)

    def mouseReleaseEvent(self, a0):
        if a0.button() == Qt.MouseButton.LeftButton:
            self._pos = None
        else:
            super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0):
        if self._pos:
            self.scroll(int(self._pos.x() - a0.position().x()),
                        int(self._pos.y() - a0.position().y()), animation=False)
            self._pos = a0.position()
        else:
            super().mouseMoveEvent(a0)

    def setPixmap(self, pixmap: QPixmap):
        self._initial_pixmap = pixmap
        self._apply_pixmap()

    def pixmap(self) -> QPixmap:
        return self._initial_pixmap
