from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout

from PyQtUIkit.core import *
from PyQtUIkit.widgets._layout import KitBoxLayout
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitRadioButton(QPushButton, _KitWidget):
    main_palette = PaletteProperty('Bg')
    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)

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
        self.__button.setChecked(True)
        if not self.__selected:
            self._set_selected(True)

    def _set_selected(self, flag):
        self.__selected = flag
        self.__button.setChecked(flag)
        if flag:
            self.selected.emit()

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return 
        self.__label.setFont(self.font.get(self.font_size))
        fm = QFontMetrics(self.__label.font())
        fm.size(0, self.__label.text())
        self.setFixedWidth(34 + fm.size(0, self.__label.text()).width())

        self.setFixedHeight(self._size)
        self.__button.setFixedSize(self._size - 8, self._size - 8)
        self.__button.setStyleSheet(f"""
QPushButton {{
    background-color: {self.main_palette.main};
    border: 1px solid {self.border_palette.main};
    border-radius: {(self._size - 8) // 2}px;
    padding: 3px 8px 3px 8px;
}}
QPushButton::hover {{
    background-color: {self.main_palette.hover};
    border: 1px solid {self.border_palette.selected};
}}
QPushButton::checked {{
    background-color: {self.main_palette.main};
    border: {(self._size - 8) // 4}px solid {self.border_palette.selected};
}}""")
        self.__label.setStyleSheet(f"color: {self.main_palette.text}; border: none; background-color: transparent")


class KitRadio(KitBoxLayout):
    button_height = IntProperty('button_size', 24)
    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)

    currentChanged = pyqtSignal(int)
    on_current_changed = SignalProperty('on_current_changed', 'currentChanged')

    def __init__(self, orientation=Qt.Orientation.Vertical):
        super().__init__(orientation)
        self._main_palette = 'Bg'
        self.__items = []
        self.__current = None

        if orientation == Qt.Orientation.Vertical:
            self.setAlignment(Qt.AlignmentFlag.AlignTop)
        else:
            self.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.padding = 5
        self.spacing = 5

    def setCurrentItem(self, index: int):
        tab: KitRadioButton = self.__items[index]
        if self.__current:
            self.__current._set_selected(False)
        self.__current = tab
        self.__current._set_selected(True)
        self.currentChanged.emit(index)

    def _on_item_selected(self, button: KitRadioButton):
        if isinstance(self.__current, KitRadioButton) and self.__current != button:
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
        if self.__current is None:
            return None
        return self.__items.index(self.__current)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        for el in self.__items:
            el.main_palette = self.main_palette
            el.font = self.font
            el.font_size = self.font_size
            el._size = self.button_height
        super()._apply_theme()


class KitHRadio(KitRadio):
    def __init__(self):
        super().__init__(orientation=Qt.Orientation.Horizontal)


class KitVRadio(KitRadio):
    def __init__(self):
        super().__init__(orientation=Qt.Orientation.Vertical)
