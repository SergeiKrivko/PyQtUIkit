import random

from PyQt6.QtCore import pyqtProperty, QPropertyAnimation, QRect, QParallelAnimationGroup, QSequentialAnimationGroup, \
    QEasingCurve
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QWidget


class Spinner(QWidget):
    def __init__(self):
        super().__init__()

        self.__size = 30
        self.__width = 2
        self.__speed = 1200
        self.__color = QColor('#FFFFFF')

        self.__angle_start = random.randint(0, 360) * 16
        self.__angle_delta = 0
        self.__angle_speed = 0
        self.__anim = None
        self.__paused = False
        self.__painter = QPainter()
        self.setMinimumSize(self.spinner_size, self.spinner_size)

    @property
    def spinner_size(self):
        return self.__size

    @spinner_size.setter
    def spinner_size(self, size):
        self.__size = size
        self.setMinimumSize(size, size)

    @property
    def spinner_width(self):
        return self.__width

    @spinner_width.setter
    def spinner_width(self, width):
        self.__width = width

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        self.__speed = speed

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    def start(self):
        if self.__anim:
            self.__anim.stop()

        self.__anim = QSequentialAnimationGroup()

        speed_anim_1 = QPropertyAnimation(self, b'_angle_speed')
        speed_anim_1.setStartValue(50)
        speed_anim_1.setEndValue(250)
        speed_anim_1.setEasingCurve(QEasingCurve.Type.InCubic)
        speed_anim_1.setDuration(self.speed // 2)

        speed_anim_2 = QPropertyAnimation(self, b'_angle_speed')
        speed_anim_2.setStartValue(250)
        speed_anim_2.setEndValue(50)
        speed_anim_2.setEasingCurve(QEasingCurve.Type.OutCubic)
        speed_anim_2.setDuration(self.speed // 2)

        speed_anim = QSequentialAnimationGroup()
        speed_anim.addAnimation(speed_anim_1)
        speed_anim.addAnimation(speed_anim_2)

        delta_anim = QPropertyAnimation(self, b'_angle_delta')
        delta_anim.setStartValue(15 * 16)
        delta_anim.setEndValue(240 * 16)
        delta_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        delta_anim.setDuration(self.speed)

        group = QParallelAnimationGroup()
        group.addAnimation(speed_anim)
        group.addAnimation(delta_anim)
        self.__anim.addAnimation(group)

        delta_anim = QPropertyAnimation(self, b'_angle_delta')
        delta_anim.setStartValue(240 * 16)
        delta_anim.setEndValue(15 * 16)
        delta_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        delta_anim.setDuration(self.speed)
        self.__anim.addAnimation(delta_anim)

        self.__anim.finished.connect(self.__anim.start)
        self.__anim.start()
        if self.__paused:
            self.__anim.pause()

    def paintEvent(self, a0) -> None:
        super().paintEvent(a0)
        self.__painter.begin(self)
        pen = QPen()
        pen.setColor(self.color)
        pen.setWidth(self.spinner_width)
        self.__angle_start += self.__angle_speed
        self.__angle_start %= 360 * 16
        self.__painter.setPen(pen)
        self.__painter.drawArc(
            QRect((self.width() - self.spinner_size + self.spinner_width) // 2,
                  (self.height() - self.spinner_size + self.spinner_width) // 2,
                  self.spinner_size - self.spinner_width, self.spinner_size - self.spinner_width),
            # self.__angle_start - 5,
            # 10,
            self.__angle_start - self.__angle_delta,
            self.__angle_delta
        )
        self.__painter.end()

    @pyqtProperty(int)
    def _angle_start(self):
        return self.__angle_start

    @_angle_start.setter
    def _angle_start(self, value):
        self.__angle_start = value % (360 * 16)
        self.update()

    @pyqtProperty(int)
    def _angle_speed(self):
        return self.__angle_speed

    @_angle_speed.setter
    def _angle_speed(self, value):
        self.__angle_speed = value

    @pyqtProperty(int)
    def _angle_delta(self):
        return self.__angle_delta

    @_angle_delta.setter
    def _angle_delta(self, value):
        self.__angle_delta = value
        self.update()

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

    def showEvent(self, a0):
        if not self.__anim:
            self.start()
        else:
            self.resume()

    def hideEvent(self, a0):
        self.pause()
