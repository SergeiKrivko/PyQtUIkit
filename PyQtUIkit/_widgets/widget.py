from typing import Iterable

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLayout

from PyQtUIkit._core.event import KitSignals
from _core.style_obj import BaseStyle
from _core.styles import KitStyle, KitStyleProperty, KitStyleTheme, KitStyleType, KitStyleClass, style_service, \
    KitStyleAny, KitStyleChild


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

        self._style = BaseStyle()
        self._final_style = BaseStyle()
        self.__child_styles: list[KitStyleChild] = []

    @property
    def qt_widget(self):
        return self._qt_widget

    @property
    def style(self):
        return self._style

    @property
    def final_style(self):
        return self._final_style

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

    @property
    def children(self) -> Iterable['KitWidget']:
        return []

    @property
    def size(self):
        return self.qt_widget.size()

    @property
    def width(self):
        return self.qt_widget.width()

    @width.setter
    def width(self, width: int):
        self.qt_widget.setFixedWidth(width)

    @property
    def height(self):
        return self.qt_widget.height()

    @height.setter
    def height(self, height: int):
        self.qt_widget.setFixedHeight(height)

    @size.setter
    def size(self, size: QSize | tuple[int, int] | int):
        if isinstance(size, tuple):
            self.qt_widget.setFixedSize(*size)
        elif isinstance(size, int):
            self.qt_widget.setFixedSize(size, size)
        else:
            self.qt_widget.setFixedSize(size)

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

    def show(self):
        self.qt_widget.show()

    def hide(self):
        self.qt_widget.hide()

    def apply_style(self):
        self.__load_styles()
        self.final_style.apply(self.style)

    def apply_lang(self):
        pass

    def __add_style(self, elem: KitStyle):
        if isinstance(elem, KitStyleProperty):
            self.final_style.set(elem.name, elem.value, if_none=False)
        else:
            if isinstance(elem, KitStyleAny):
                print(f"Adding style {elem} to {self}")
                for el in elem.children:
                    self.__add_style(el)
            if isinstance(elem, KitStyleTheme) and style_service.theme in elem.names:
                print(f"Adding style {elem} to {self}")
                for el in elem.children:
                    self.__add_style(el)
            elif isinstance(elem, KitStyleType) and style_service.check_class(self.__class__, elem.names):
                print(f"Adding style {elem} to {self}")
                for el in elem.children:
                    self.__add_style(el)
            elif isinstance(elem, KitStyleChild):
                for child in self.children:
                    child._add_child_style(elem)
            elif isinstance(elem, KitStyleClass) and elem.names & self.classes:
                print(f"Adding style {elem} to {self}")
                for el in elem.children:
                    self.__add_style(el)

    def __load_styles(self):
        for child in self.children:
            child._clear_child_styles()
        for el in style_service.styles:
            self.__add_style(el)
        for el in self.__child_styles:
            if not el.types:
                for e in el.children:
                    self.__add_style(e)
            elif style_service.check_class(self.__class__, el.types):
                for e in el.children:
                    self.__add_style(e)
            else:
                for child in self.children:
                    child._add_child_style(el)

    def _clear_child_styles(self):
        self.__child_styles.clear()

    def _add_child_style(self, style: KitStyleChild):
        print(f"Adding style {style} to {self}")
        self.__child_styles.append(style)

