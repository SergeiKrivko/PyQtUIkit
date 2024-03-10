from PyQt6.QtCore import QMargins
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from PyQtUIkit.core.properties import IntProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitHBoxLayout(QWidget, _KitWidget):
    border = IntProperty('border', 0)
    radius = IntProperty('radius', 4)

    def __init__(self):
        super().__init__()
        self.__widgets = []
        self.main_palette = 'Transparent'

        strange_layout = QHBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)

        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        self.__layout = QHBoxLayout()
        strange_widget.setLayout(self.__layout)

    def addWidget(self, widget: QWidget, stretch: int = None, alignment=None):
        if alignment is not None:
            self.__layout.addWidget(widget, stretch, alignment)
        elif stretch is not None:
            self.__layout.addWidget(widget, stretch)
        else:
            self.__layout.addWidget(widget)
        self.__widgets.append(widget)
        if hasattr(widget, '_set_tm'):
            widget._set_tm(self._tm)

    def insertWidget(self, index: int, widget: QWidget, stretch: int = None, alignment=None):
        if alignment is not None:
            self.__layout.insertWidget(index, widget, stretch, alignment)
        elif stretch is not None:
            self.__layout.insertWidget(index, widget, stretch)
        else:
            self.__layout.insertWidget(index, widget)
        self.__widgets.insert(index, widget)
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
        self.__widgets.clear()

    def setAlignment(self, a) -> bool:
        return self.__layout.setAlignment(a)

    def setSpacing(self, spacing):
        self.__layout.setSpacing(spacing)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.__layout.setContentsMargins(left, top, right, bottom)

    def contentsMargins(self) -> QMargins:
        return self.__layout.contentsMargins()

    def count(self):
        return self.__layout.count()

    def _set_tm(self, tm):
        super()._set_tm(tm)
        for el in self.__widgets:
            if hasattr(el, '_set_tm'):
                el._set_tm(tm)

    def _apply_theme(self):
        for el in self.__widgets:
            if hasattr(el, '_apply_theme'):
                el._apply_theme()
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {self.main_palette.main};
            border: {self.border}px solid {self._tm.get('Border').main};
            border-radius: {self.radius}px;
        }}
        """)
