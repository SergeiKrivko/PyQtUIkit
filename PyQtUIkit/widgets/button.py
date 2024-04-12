from enum import Enum

from PyQt6.QtCore import Qt, QMargins
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from PyQtUIkit.core import IconProperty, EnumProperty, PaletteProperty, KitFont, FontProperty, \
    SignalProperty, MethodsProperty
from PyQtUIkit.themes import ThemeManager
from PyQtUIkit.widgets import KitIconWidget
from PyQtUIkit.widgets._widget import KitGroupItem as _KitGroupItem


class KitButton(QPushButton, _KitGroupItem):
    main_palette = PaletteProperty('main_palette', 'Main')
    icon = IconProperty('icon')
    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)
    on_click = SignalProperty('on_click', 'clicked')

    def __init__(self, text='', icon=None):
        super().__init__()
        self.__widgets = []
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setText(text)
        self._icon = icon

        self._build_from_kui()

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFont(self.font.get(self.font_size))
        self.setStyleSheet(f"""
QPushButton {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self.border_palette.main};
    {self._border_radius_css()}
    padding: 3px 8px 3px 8px;
}}
QPushButton::hover {{
    background-color: {self.main_palette.hover};
    border: {self.border}px solid {self.border_palette.selected};
}}
QPushButton::disabled {{
    color: {self.main_palette.main};
    border-color: {self.border_palette.main};
}}
QPushButton::checked {{
    background-color: {self.main_palette.selected};
    border: {self.border}px solid {self.border_palette.selected};
}}
QPushButton::menu-indicator {{
    image: none;
    subcontrol-origin: padding;
    padding-right: 5px;
    subcontrol-position: right;
}}""")
        if self.icon is not None:
            self.setIcon(self.icon.icon(self.main_palette.text))

    text = MethodsProperty(QPushButton.text, QPushButton.setText)


class KitIconButton(QPushButton, _KitGroupItem):
    main_palette = PaletteProperty('main_palette', 'Main')
    icon = IconProperty('icon')
    on_click = SignalProperty('on_click', 'clicked')

    def __init__(self, icon=''):
        super().__init__()
        self.__widgets = []
        self._icon = icon
        self._main_palette = 'Main'
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        self._icon_label = KitIconWidget()
        self._icon_label._use_text_only = False
        self.__layout.addWidget(self._icon_label)

    def _set_tm(self, tm: ThemeManager):
        super()._set_tm(tm)
        self._icon_label._set_tm(tm)

    def _set_size(self, x, y=None):
        if isinstance(x, int) and isinstance(y, int):
            self.setFixedSize(x, y)
        elif y is None:
            self.setFixedSize(x, x)
        else:
            self.setFixedSize(x)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self._icon_label.icon = self.icon
        self._icon_label._main_palette = self._main_palette
        self.__layout.setContentsMargins(*[min(self.width(), self.height()) // 6] * 4)
        self.setStyleSheet(f"""
QPushButton {{
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self.border_palette.main};
    {self._border_radius_css()}
    padding: 3px 8px 3px 8px;
}}
QPushButton::hover {{
    background-color: {self.main_palette.hover};
    border: {self.border}px solid {self.border_palette.selected};
}}
QPushButton::disabled {{
    color: {self.main_palette.main};
    border-color: {self.border_palette.main};
}}
QPushButton::checked {{
    background-color: {self.main_palette.selected};
    border: {self.border}px solid {self.border_palette.selected};
}}
QPushButton::menu-indicator {{
    image: none;
    subcontrol-position: right;
}}""")

    size = MethodsProperty(QPushButton.size, _set_size)


class KitLayoutButton(KitButton):
    class Orientation(Enum):
        HORIZONTAL = 0
        VERTICAL = 1

    def __init__(self, orientation: Orientation = Orientation.HORIZONTAL):
        super().__init__()
        self.__orientation = orientation
        self.__layout = QHBoxLayout() if orientation == KitLayoutButton.Orientation.HORIZONTAL else QVBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__layout)
        self._widgets = []

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
        super()._apply_theme()
        for el in self._widgets:
            if hasattr(el, '_apply_theme'):
                el._apply_theme()

    padding = MethodsProperty(getContentsMargins, _set_margins)
    spacing = MethodsProperty(getSpacing, setSpacing)
    alignment = MethodsProperty(getAlignment, setAlignment)
