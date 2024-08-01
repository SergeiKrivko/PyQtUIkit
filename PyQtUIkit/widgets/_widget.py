from typing import Iterable

from PyQt6.QtWidgets import QWidget, QLayout

from PyQtUIkit.core.event import KitSignals


class KitWidget:
    def __init__(self, qt_widget: QWidget | QLayout):
        self._qt_widget = qt_widget
        self.__classes = set()

        self.__show_events = KitSignals()
        self.__hide_events = KitSignals()
        self.__mouse_move_events = KitSignals()
        self.__mouse_press_events = KitSignals()
        self.__mouse_release_events = KitSignals()
        self.__key_press_events = KitSignals()
        self.__key_release_events = KitSignals()

        self._qt_widget.showEvent = self.__qt_show_event
        self._qt_widget.hideEvent = self.__qt_hide_event
        self._qt_widget.mouseMoveEvent = self.__qt_mouse_move_event
        self._qt_widget.mousePressEvent = self.__qt_mouse_press_event
        self._qt_widget.mouseReleaseEvent = self.__qt_mouse_release_event
        self._qt_widget.keyPressEvent = self.__qt_key_press_event
        self._qt_widget.keyReleaseEvent = self.__qt_key_release_event

    @property
    def qt_widget(self):
        return self._qt_widget

    @property
    def classes(self) -> set[str]:
        return self.__classes

    @classes.setter
    def classes(self, classes: set[str] | Iterable[str] | str):
        if isinstance(classes, str):
            self.__classes = set(classes.split())
        elif isinstance(classes, set):
            self.__classes = classes
        else:
            self.__classes = set(classes)

    @property
    def on_show(self):
        return self.__show_events

    @property
    def on_hide(self):
        return self.__hide_events

    @property
    def on_mouse_move(self):
        return self.__mouse_move_events

    @property
    def on_mouse_press(self):
        return self.__mouse_press_events

    @property
    def on_mouse_release(self):
        return self.__mouse_release_events

    @property
    def on_key_press(self):
        return self.__key_press_events

    @property
    def on_key_release(self):
        return self.__key_release_events

    def __qt_show_event(self, event):
        self.__show_events(event)
        self.qt_widget.__class__.showEvent(self.qt_widget, event)

    def __qt_hide_event(self, event):
        self.__hide_events(event)
        self.qt_widget.__class__.hideEvent(self.qt_widget, event)

    def __qt_mouse_move_event(self, event):
        self.__mouse_move_events(event)
        self.qt_widget.__class__.mouseMoveEvent(self.qt_widget, event)

    def __qt_mouse_press_event(self, event):
        self.__mouse_press_events(event)
        self.qt_widget.__class__.mousePressEvent(self.qt_widget, event)

    def __qt_mouse_release_event(self, event):
        self.__mouse_release_events(event)
        self.qt_widget.__class__.mouseReleaseEvent(self.qt_widget, event)

    def __qt_key_press_event(self, event):
        self.__key_press_events(event)
        self.qt_widget.__class__.keyPressEvent(self.qt_widget, event)

    def __qt_key_release_event(self, event):
        self.__key_release_events(event)
        self.qt_widget.__class__.keyReleaseEvent(self.qt_widget, event)

    def apply_style(self):
        pass

    def apply_lang(self):
        pass
