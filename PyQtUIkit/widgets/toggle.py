from enum import Enum

from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QWidget, QPushButton

from PyQtUIkit.core import *
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget
from PyQtUIkit.widgets.button import KitButton


class KitToggle(QWidget, _KitWidget):
    class Mode(Enum):
        SMALL = 0
        MEDIUM = 1
        LARGE = 2

    main_palette = PaletteProperty('main_palette', 'Menu')
    rail_palette = PaletteProperty('rail_palette', 'Main')
    mode = EnumProperty('mode', Mode, Mode.SMALL)

    stateChanged = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.__state = False
        self.__anim = None

        self.__sizes = {
            KitToggle.Mode.MEDIUM: {
                'size': (44, 26),
                'rail_size': (34, 16),
                'button_size': 24,
            },
            KitToggle.Mode.SMALL: {
                'size': (40, 20),
                'rail_size': (40, 20),
                'button_size': 14,
            },
            KitToggle.Mode.LARGE: {
                'size': (46, 28),
                'rail_size': (46, 28),
                'button_size': 24,
            }
        }
        self.__button_y = 0
        self.__button_x = 0

        self.__rail = QPushButton(self)
        self.__rail.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__rail.clicked.connect(self._on_clicked)

        self.__button = KitButton()
        self.__button.setParent(self)
        self.__button.setCheckable(True)
        self.__button.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        self.__state = not self.__state
        self.__on_state_changed()

    def __on_state_changed(self):
        self.__button.setChecked(self.__state)
        self.stateChanged.emit(self.__state)

        if not self._tm or not self._tm.active:
            return

        if self.__anim:
            self.__anim.stop()

        self.__anim = QPropertyAnimation(self.__button, b"pos")
        self.__anim.setStartValue(QPoint(self.__button_x, self.__button_y) if self.__state else
                                  QPoint(self.__button_x_r, self.__button_y))
        self.__anim.setEndValue(QPoint(self.__button_x_r, self.__button_y) if self.__state else
                                QPoint(self.__button_x, self.__button_y))
        self.__anim.setDuration(200)
        self.__anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.__anim.start()

        self._apply_theme()

    def isChecked(self):
        return self.__state

    def setChecked(self, state):
        self.__state = bool(state)
        self.__on_state_changed()

    def _set_tm(self, tm):
        super()._set_tm(tm)
        self.__button._set_tm(tm)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        sizes = self.__sizes[self.mode]
        self.setFixedSize(*sizes['size'])

        self.__button_x = (sizes['size'][0] - sizes['rail_size'][0]) // 2 + \
                          (sizes['rail_size'][1] - sizes['button_size']) // 2
        self.__button_y = (sizes['size'][1] - sizes['button_size']) // 2
        self.__button_x_r = sizes['size'][0] - sizes['button_size'] - self.__button_y

        self.__rail.setGeometry((sizes['size'][0] - sizes['rail_size'][0]) // 2,
                                (sizes['size'][1] - sizes['rail_size'][1]) // 2,
                                *sizes['rail_size'])
        self.__button.setGeometry(self.__button_x, self.__button_y,
                                  sizes['button_size'], sizes['button_size'])
        self.__button.radius = sizes['button_size'] // 2
        self.__button.move(self.__button_x_r if self.__state else self.__button_x, self.__button_y)

        self.__button.main_palette = self.main_palette
        self.__button._apply_theme()
        self.__rail.setStyleSheet(f"""
        QWidget {{
            color: {self.main_palette.text};
            background-color: {self.rail_palette.selected if self.__state else self.rail_palette.main};
            border: 0px solid black;
            border-radius: {sizes['rail_size'][1] // 2}px;
        }}""")

    state = MethodsProperty(isChecked, setChecked)
    on_state_changed = SignalProperty('on_state_changed', 'stateChanged')
