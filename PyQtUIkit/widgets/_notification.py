import asyncio
import subprocess
import sys
from enum import Enum

from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, pyqtSignal
from PyQt6.QtWidgets import QApplication
from PyQtUIkit.core.properties import SignalProperty

from PyQtUIkit.core.font import KitFont
from PyQtUIkit.widgets._button import KitIconButton
from PyQtUIkit.widgets._form import KitForm
from PyQtUIkit.widgets._icon_widget import KitIconWidget
from PyQtUIkit.widgets._label import KitLabel
from PyQtUIkit.widgets._layout import KitHBoxLayout, KitVBoxLayout


class KitSystemNotification:
    class Duration(Enum):
        SHORT = 'short'
        LONG = 'long'

    def __init__(self, title=None, body=None, on_click=print, icon=None, duration=Duration.SHORT):
        self._title = title
        self._body = body
        self._on_click = on_click
        self._icon = icon
        self._duration = duration

    @property
    def time(self):
        match self._duration:
            case self.Duration.LONG:
                return 25
            case self.Duration.SHORT:
                return 7

    async def show(self):
        match sys.platform:
            case 'win32':
                import win11toast
                await win11toast.toast_async(self._title,
                                             self._body,
                                             on_click=self._on_click,
                                             icon=self._icon,
                                             duration=self._duration.value)
            case 'linux':
                args = ['notify-send', '-t', self.time * 1000]
                if self._title:
                    args.append(self._title)
                if self._body:
                    args.append(self._body)
                if self._icon:
                    args.extend(['-i', self._icon])
                subprocess.run(args, shell=True)
                await asyncio.sleep(self.time)
            case 'darwin':
                subprocess.run(['osascript', '-e',
                                f'display notification "{self._body}" with title "{self._title}"'],
                               shell=True)
                await asyncio.sleep(self.time)


class KitBaseNotification(KitVBoxLayout):
    ANIM_DURATION = 300

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.main_palette = 'Menu'
        self.border = 1
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.WindowStaysOnTopHint)
        self.__dismissed = False
        self.__anim = None
        self.__expired = 0

    def _closed_pos(self):
        screen_size = QApplication.primaryScreen().size()
        return QPoint(screen_size.width(), screen_size.height() - self.height() - 75)

    def _opened_pos(self):
        screen_size = QApplication.primaryScreen().size()
        return QPoint(screen_size.width() - self.width() - 20, screen_size.height() - self.height() - 75)

    async def _show(self):
        super().show()
        self._set_tm(self._parent._tm)
        self._start_anim(QPropertyAnimation.Direction.Backward)
        await asyncio.sleep(self.ANIM_DURATION / 1000)

    async def _hide(self):
        self._start_anim(QPropertyAnimation.Direction.Forward)
        await asyncio.sleep(self.ANIM_DURATION / 1000)
        super().hide()

    def _start_anim(self, direction):
        if isinstance(self.__anim, QPropertyAnimation):
            self.__anim.stop()
        self.__anim = QPropertyAnimation(self, b'pos')
        self.__anim.setEasingCurve(QEasingCurve.Type.Linear)
        self.__anim.setStartValue(self._opened_pos())
        self.__anim.setEndValue(self._closed_pos())
        self.__anim.setDirection(direction)
        self.__anim.setDuration(KitBaseNotification.ANIM_DURATION)
        self.__anim.start()

    def _has_focus(self):
        if self.geometry().top() > self.cursor().pos().y():
            return False
        if self.geometry().bottom() < self.cursor().pos().y():
            return False
        if self.geometry().left() > self.cursor().pos().x():
            return False
        if self.geometry().right() < self.cursor().pos().y():
            return False
        return True

    async def exec(self, duration):
        await self._show()
        self.__expired = duration
        while not self.__dismissed and self.__expired > 0:
            await asyncio.sleep(0.1)
            if self._has_focus():
                self.__expired = max(3, self.__expired)
            self.__expired -= 0.1
        await self._hide()

    def dismiss(self):
        self.__dismissed = True


class KitNotification(KitBaseNotification):
    clicked = pyqtSignal()

    on_click = SignalProperty('on_click', 'clicked')

    def __init__(self, parent, title: str, text: str, icon: str = None, form: KitForm = None):
        super().__init__(parent)
        self.padding = 16
        self.spacing = 6

        self.setFixedWidth(350)

        layout = KitHBoxLayout()
        layout.spacing = 6
        self.addWidget(layout)

        if icon:
            self._icon_widget = KitIconWidget(icon)
            self._icon_widget.setFixedSize(72, 72)
            layout.addWidget(self._icon_widget)
        else:
            self._icon_widget = None

        v_layout = KitVBoxLayout()
        v_layout.spacing = 6
        layout.addWidget(v_layout)

        top_layout = KitHBoxLayout()
        top_layout.spacing = 6
        v_layout.addWidget(top_layout)

        self._title_label = KitLabel(title)
        self._title_label.font_size = KitFont.Size.BIG
        top_layout.addWidget(self._title_label)

        self._button_close = KitIconButton('line-close')
        self._button_close.setFixedSize(22, 22)
        self._button_close.radius = 11
        self._button_close.border = 0
        self._button_close.main_palette = 'Menu'
        self._button_close.on_click = self.dismiss
        top_layout.addWidget(self._button_close)

        self._text_label = KitLabel(text)
        self._text_label.setWordWrap(True)
        v_layout.addWidget(self._text_label, 100)

        if form:
            self._form = form
            self.addWidget(self._form)
        else:
            self._form = None

    def _has_focus(self):
        if self._form and self._form.has_focus():
            return True
        return super()._has_focus()

    def mousePressEvent(self, a0):
        super().mousePressEvent(a0)
        if a0.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
