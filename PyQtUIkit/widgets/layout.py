from PyQt6.QtCore import QMargins, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from PyQtUIkit.core.properties import IntProperty, MethodsProperty
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitBoxLayout(QWidget, _KitWidget):
    border = IntProperty('border', 0)
    radius = IntProperty('radius', 4)

    def __init__(self, orientation=Qt.Orientation.Horizontal):
        super().__init__()
        self._widgets = []
        self._main_palette = 'Transparent'

        strange_layout = QVBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)

        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        self.__layout = QVBoxLayout() if orientation == Qt.Orientation.Vertical else QHBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        strange_widget.setLayout(self.__layout)

        self._add_child_func = self.addWidget

    def addWidget(self, widget: QWidget, stretch: int = None, alignment=None):
        if alignment is not None:
            self.__layout.addWidget(widget, stretch, alignment)
        elif stretch is not None:
            self.__layout.addWidget(widget, stretch)
        else:
            self.__layout.addWidget(widget)
        self._widgets.append(widget)
        if hasattr(widget, '_set_tm'):
            widget._set_tm(self._tm)

    def insertWidget(self, index: int, widget: QWidget, stretch: int = None, alignment=None):
        if alignment is not None:
            self.__layout.insertWidget(index, widget, stretch, alignment)
        elif stretch is not None:
            self.__layout.insertWidget(index, widget, stretch)
        else:
            self.__layout.insertWidget(index, widget)
        self._widgets.insert(index, widget)
        if hasattr(widget, '_set_tm'):
            widget._set_tm(self._tm)

    def deleteWidget(self, w: int | QWidget):
        if isinstance(w, int):
            w = self.__layout.takeAt(w).widget()
        w.setParent(None)
        return w

    def clear(self):
        for _ in range(self.__layout.count()):
            self.__layout.takeAt(0).widget().setParent(None)
        self._widgets.clear()

    def setAlignment(self, a):
        self.__layout.setAlignment(a)

    def getAlignment(self):
        return self.__layout.alignment()

    def setSpacing(self, spacing):
        self.__layout.setSpacing(spacing)

    def getSpacing(self):
        return self.__layout.spacing()

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.__layout.setContentsMargins(left, top, right, bottom)

    def getContentsMargins(self):
        return self.__layout.contentsMargins()

    def _set_margins(self, margins):
        if isinstance(margins, int):
            self.setContentsMargins(margins, margins, margins, margins)
        elif len(margins) == 1:
            self.__layout.setContentsMargins(margins[0], margins[0], margins[0], margins[0])
        elif len(margins) == 2:
            self.__layout.setContentsMargins(margins[0], margins[1], margins[0], margins[1])
        elif len(margins) == 4:
            self.__layout.setContentsMargins(*margins)
        else:
            raise ValueError

    def contentsMargins(self) -> QMargins:
        return self.__layout.contentsMargins()

    def count(self):
        return self.__layout.count()

    def _set_tm(self, tm):
        super()._set_tm(tm)
        for el in self._widgets:
            if hasattr(el, '_set_tm'):
                el._set_tm(tm)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        for el in self._widgets:
            if hasattr(el, '_apply_theme'):
                el._apply_theme()
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {self.main_palette.main};
            border: {self.border}px solid {self.border_palette.main};
            border-radius: {self.radius}px;
        }}
        """)

    def _apply_lang(self):
        if not self._tm or not self._tm.active:
            return
        for el in self._widgets:
            if hasattr(el, '_apply_theme'):
                el._apply_lang()

    padding = MethodsProperty(getContentsMargins, _set_margins)
    spacing = MethodsProperty(getSpacing, setSpacing)
    alignment = MethodsProperty(getAlignment, setAlignment)
    max_width = MethodsProperty(QWidget.maximumWidth, QWidget.setMaximumWidth)
    min_width = MethodsProperty(QWidget.minimumWidth, QWidget.setMinimumWidth)
    max_height = MethodsProperty(QWidget.maximumHeight, QWidget.setMaximumHeight)
    min_height = MethodsProperty(QWidget.minimumHeight, QWidget.setMinimumHeight)


class KitVBoxLayout(KitBoxLayout):
    def __init__(self):
        super().__init__(orientation=Qt.Orientation.Vertical)


class KitHBoxLayout(KitBoxLayout):
    def __init__(self):
        super().__init__(orientation=Qt.Orientation.Horizontal)
