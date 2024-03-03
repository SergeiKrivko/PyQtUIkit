from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

from PyQtUIkit.core.properties import PaletteProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget
from PyQtUIkit.widgets.button import KitIconButton, KitButton


class KitCheckItem(QWidget, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Menu')
    rail_palette = PaletteProperty('rail_palette', 'Main')

    stateChanged = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.__state = False
        self.setFixedSize(44, 30)
        self.__anim = None

        self.__rail = QWidget(self)
        self.__rail.setGeometry(5, 5, 34, 16)

        self.__button = KitButton()
        self.__button.radius = 12
        self.__button.setParent(self)
        self.__button.setCheckable(True)
        self.__button.clicked.connect(self._on_clicked)
        self.__button.setGeometry(1, 1, 24, 24)

    def _on_clicked(self):
        self.__state = not self.__state
        self.__on_state_changed()

    def __on_state_changed(self):
        self.__button.setChecked(self.__state)
        self.stateChanged.emit(self.__state)

        if self.__anim:
            self.__anim.stop()

        self.__anim = QPropertyAnimation(self.__button, b"pos")
        self.__anim.setStartValue(QPoint(1, 1) if self.__state else QPoint(18, 1))
        self.__anim.setEndValue(QPoint(18, 1) if self.__state else QPoint(1, 1))
        self.__anim.setDuration(200)
        self.__anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.__anim.start()

        self._apply_theme()

    def state(self):
        return self.__state

    def setState(self, state):
        self.__state = bool(state)
        self.__on_state_changed()

    def _set_tm(self, tm):
        super()._set_tm(tm)
        self.__button._set_tm(tm)

    def _apply_theme(self):
        self.__button.main_palette = self.main_palette
        self.__button._apply_theme()
        self.__rail.setStyleSheet(f"""
        QWidget {{
            color: {self.main_palette.text};
            background-color: {self.rail_palette.selected if self.__state else self.main_palette.main};
            border: 0px solid black;
            border-radius: 7px;
        }}""")
