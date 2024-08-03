from enum import Enum
from typing import Iterable

from PyQt6.QtCore import QPropertyAnimation, QPoint, QEasingCurve
from PyQt6.QtWidgets import QWidget

from _core.event import KitSignals
from _widgets.layout_button import KitLayoutButton
from _widgets.widget import KitWidget


class KitToggle(KitWidget):
    class __Mode(Enum):
        SMALL = 0
        MEDIUM = 1
        LARGE = 2

    __SIZES = {
        __Mode.MEDIUM: {
            'size': (44, 26),
            'rail_size': (34, 16),
            'button_size': 24,
        },
        __Mode.SMALL: {
            'size': (40, 20),
            'rail_size': (40, 20),
            'button_size': 14,
        },
        __Mode.LARGE: {
            'size': (46, 28),
            'rail_size': (46, 28),
            'button_size': 24,
        }
    }

    def __init__(self, classes: Iterable[str] | str | None = None):
        super().__init__(QWidget())
        if classes is not None:
            self.classes = classes

        self.__state = False
        self.__anim = None

        self.__button_y = 0
        self.__button_x = 0

        self.__rail = KitLayoutButton()
        self.__rail.classes = "__PyQtUIkit_Toggle_rail"
        self.__rail.qt_widget.setParent(self.qt_widget)
        self.__rail.checkable = True
        self.__rail.on_click.add(self.__on_clicked)

        self.__button = KitLayoutButton()
        self.__button.classes = "__PyQtUIkit_Toggle_button"
        self.__button.qt_widget.setParent(self.qt_widget)
        self.__button.checkable = True
        self.__button.on_click.add(self.__on_clicked)

        self.__state_events = KitSignals()

    @property
    def children(self) -> Iterable['KitWidget']:
        yield self.__rail
        yield self.__button

    def __on_clicked(self):
        self.__state = not self.__state
        self.__on_state_changed()

    def __on_state_changed(self):
        self.__rail.checked = self.__state
        self.__button.checked = self.__state
        self.__state_events(self.__state)

        if self.__anim:
            self.__anim.stop()

        self.__anim = QPropertyAnimation(self.__button.qt_widget, b"pos")
        self.__anim.setStartValue(QPoint(self.__button_x, self.__button_y) if self.__state else
                                  QPoint(self.__button_x_r, self.__button_y))
        self.__anim.setEndValue(QPoint(self.__button_x_r, self.__button_y) if self.__state else
                                QPoint(self.__button_x, self.__button_y))
        self.__anim.setDuration(200)
        self.__anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.__anim.start()

        # self.apply_style()

    @property
    def checked(self) -> bool:
        return self.__state

    @checked.setter
    def checked(self, value: bool):
        self.__state = bool(value)
        self.__on_state_changed()

    def apply_style(self):
        super().apply_style()

        mode = KitToggle.__Mode.LARGE if 'large' in self.classes else (
            KitToggle.__Mode.MEDIUM) if 'medium' in self.classes else KitToggle.__Mode.SMALL
        sizes = self.__SIZES[mode]
        self.qt_widget.setFixedSize(*sizes['size'])

        self.__button_x = (sizes['size'][0] - sizes['rail_size'][0]) // 2 + \
                          (sizes['rail_size'][1] - sizes['button_size']) // 2
        self.__button_y = (sizes['size'][1] - sizes['button_size']) // 2
        self.__button_x_r = sizes['size'][0] - sizes['button_size'] - self.__button_y

        self.__rail.qt_widget.setGeometry((sizes['size'][0] - sizes['rail_size'][0]) // 2,
                                          (sizes['size'][1] - sizes['rail_size'][1]) // 2,
                                          *sizes['rail_size'])
        self.__button.qt_widget.setGeometry(self.__button_x, self.__button_y,
                                            sizes['button_size'], sizes['button_size'])
        self.__button.qt_widget.move(self.__button_x_r if self.__state else self.__button_x, self.__button_y)

        self.__button.apply_style()
        self.__rail.apply_style()
