from PyQt6.QtCore import pyqtProperty, QPropertyAnimation, QRect, QParallelAnimationGroup, QSequentialAnimationGroup
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QPainter, QPen, QColor

from PyQtUIkit.core.properties import IntProperty, PaletteProperty
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitSpinner(QWidget, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Main')
    size = IntProperty('size', 30)
    width = IntProperty('width', 4)
    speed = IntProperty('speed', 1000)

    def __init__(self):
        super().__init__()
        self.__angle_start = 0
        self.__angle_delta = 0
        self.__anim = None
        self.__paused = False
        self.__painter = QPainter()
        self.setFixedSize(self.size, self.size)

    def start(self):
        if self.__anim:
            self.__anim.stop()

        angle_anim = QPropertyAnimation(self, b'_angle_start')
        angle_anim.setStartValue(0)
        angle_anim.setEndValue(360 * 16 * 2)
        angle_anim.setDuration(self.speed * 3)

        delta_anim = QPropertyAnimation(self, b'_angle_delta')
        delta_anim.setEndValue(360 * 16)
        delta_anim.setDuration(self.speed * 3)

        group1 = QParallelAnimationGroup()
        group1.addAnimation(angle_anim)
        group1.addAnimation(delta_anim)

        angle_anim = QPropertyAnimation(self, b'_angle_start')
        angle_anim.setStartValue(0)
        angle_anim.setEndValue(360 * 16 * 3)
        angle_anim.setDuration(self.speed * 3)

        delta_anim = QPropertyAnimation(self, b'_angle_delta')
        delta_anim.setEndValue(0)
        delta_anim.setDuration(self.speed * 3)

        group2 = QParallelAnimationGroup()
        group2.addAnimation(angle_anim)
        group2.addAnimation(delta_anim)

        self.__anim = QSequentialAnimationGroup()
        self.__anim.addAnimation(group1)
        self.__anim.addAnimation(group2)
        self.__anim.finished.connect(self.__anim.start)
        self.__anim.start()
        if self.__paused:
            self.__anim.pause()

    def paintEvent(self, a0) -> None:
        super().paintEvent(a0)
        self.__painter.begin(self)
        pen = QPen()
        pen.setColor(QColor(self.main_palette.selected))
        pen.setWidth(self.width)
        self.__painter.setPen(pen)
        self.__painter.drawArc(QRect(self.width // 2, self.width // 2, self.size - self.width, self.size - self.width),
                               self.__angle_start,
                               self.__angle_delta)
        self.__painter.end()

    @pyqtProperty(int)
    def _angle_start(self):
        return self.__angle_start

    @_angle_start.setter
    def _angle_start(self, value):
        self.__angle_start = value % (360 * 16)
        self.update()

    @pyqtProperty(int)
    def _angle_delta(self):
        return self.__angle_delta

    @_angle_delta.setter
    def _angle_delta(self, value):
        self.__angle_delta = value

    def pause(self):
        if self.__paused:
            return
        self.__paused = True
        if isinstance(self.__anim, QSequentialAnimationGroup):
            self.__anim.pause()

    def resume(self):
        if not self.__paused:
            return
        self.__paused = False
        if isinstance(self.__anim, QSequentialAnimationGroup):
            self.__anim.resume()

    def _apply_theme(self):
        self.setFixedSize(self.size, self.size)
        self.start()
