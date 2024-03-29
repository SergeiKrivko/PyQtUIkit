from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QSizePolicy

from PyQtUIkit.core.properties import IntProperty, PaletteProperty, LiteralProperty
from PyQtUIkit.widgets import KitVBoxLayout, KitHBoxLayout
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitRadioButton(QPushButton, _KitWidget):
    main_palette = PaletteProperty('Bg')
    font_size = LiteralProperty('font_size', ['medium', 'small', 'big'])

    selected = pyqtSignal()

    def __init__(self, text=''):
        super().__init__()
        self.__widgets = []
        self._size = 30
        self.__selected = False
        self.clicked.connect(self._on_clicked)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.__layout = QHBoxLayout()
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__layout.setContentsMargins(4, 4, 4, 4)
        self.__layout.setSpacing(4)
        self.setLayout(self.__layout)

        self.__button = QPushButton()
        self.__button.setCheckable(True)
        self.__button.clicked.connect(self._on_clicked)
        self.__layout.addWidget(self.__button)

        self.__label = QLabel(text)
        self.__layout.addWidget(self.__label)

    def _on_clicked(self):
        if not self.__selected:
            self._set_selected(True)

    def _set_selected(self, flag):
        self.__selected = flag
        self.__button.setChecked(flag)
        if flag:
            self.selected.emit()

    def _apply_theme(self):
        self.__label.setFont(self._tm.font(self.font_size))
        fm = QFontMetrics(self.__label.font())
        fm.size(0, self.__label.text())
        self.setFixedWidth(34 + fm.size(0, self.__label.text()).width())

        self.setFixedHeight(self._size)
        self.__button.setFixedSize(self._size - 8, self._size - 8)
        self.__button.setStyleSheet(f"""
QPushButton {{
    background-color: {self.main_palette.main};
    border: 1px solid {self._tm['Border'].main};
    border-radius: {(self._size - 8) // 2}px;
    padding: 3px 8px 3px 8px;
}}
QPushButton::hover {{
    background-color: {self.main_palette.hover};
    border: 1px solid {self._tm['Border'].selected};
}}
QPushButton::checked {{
    background-color: {self.main_palette.main};
    border: {(self._size - 8) // 4}px solid {self._tm['Border'].selected};
}}""")
        self.__label.setStyleSheet(f"color: {self.main_palette.text}; border: none; background-color: transparent")


class KitVRadio(KitVBoxLayout):
    button_height = IntProperty('button_size', 24)
    font_size = LiteralProperty('font_size', ['medium', 'small', 'big'])

    currentChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._main_palette = 'Bg'
        self.__items = []
        self.__current = None

        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setContentsMargins(5, 5, 5, 5)
        self.setSpacing(5)

    def setCurrentItem(self, tab: int):
        if isinstance(tab, int):
            tab = self.__items[tab]
        self.__current.setChecked(False)
        self.__current = tab
        self.__current.setChecked(True)
        self.currentChanged.emit(self.__items.index(tab))

    def _on_item_selected(self, button: KitRadioButton):
        if isinstance(self.__current, KitRadioButton):
            self.__current._set_selected(False)
        self.__current = button
        self.currentChanged.emit(self.__items.index(button))

    def addItem(self, name: str):
        self.insertItem(len(self.__items), name)

    def insertItem(self, index: int, name: str):
        button = KitRadioButton(name)
        if not self.__current:
            self.__current = button
            button._set_selected(True)
        button.selected.connect(lambda: self._on_item_selected(button))
        self.__items.insert(index, button)
        self.insertWidget(index, button)

    def clear(self):
        super().clear()
        self.__items.clear()
        self.__current = None

    def currentIndex(self):
        return self.__items.index(self.__current)

    def _apply_theme(self):
        for el in self.__items:
            el.main_palette = self.main_palette
            el.font_size = self.font_size
            el._size = self.button_height
        super()._apply_theme()


class KitHRadio(KitHBoxLayout):
    button_height = IntProperty('button_size', 24)
    font_size = LiteralProperty('font_size', ['medium', 'small', 'big'])

    currentChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._main_palette = 'Bg'
        self.__items = []
        self.__current = None

        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setContentsMargins(5, 5, 5, 5)
        self.setSpacing(5)

    def setCurrentItem(self, tab: int):
        if isinstance(tab, int):
            tab = self.__items[tab]
        self.__current.setChecked(False)
        self.__current = tab
        self.__current.setChecked(True)
        self.currentChanged.emit(self.__items.index(tab))

    def _on_item_selected(self, button: KitRadioButton):
        if isinstance(self.__current, KitRadioButton):
            self.__current._set_selected(False)
        self.__current = button
        self.currentChanged.emit(self.__items.index(button))

    def addItem(self, name: str):
        self.insertItem(len(self.__items), name)

    def insertItem(self, index: int, name: str):
        button = KitRadioButton(name)
        if not self.__current:
            self.__current = button
            button._set_selected(True)
        button.selected.connect(lambda: self._on_item_selected(button))
        self.__items.insert(index, button)
        self.insertWidget(index, button)

    def clear(self):
        super().clear()
        self.__items.clear()
        self.__current = None

    def currentIndex(self):
        return self.__items.index(self.__current)

    def _apply_theme(self):
        for el in self.__items:
            el.main_palette = self.main_palette
            el.font_size = self.font_size
            el._size = self.button_height
        super()._apply_theme()
