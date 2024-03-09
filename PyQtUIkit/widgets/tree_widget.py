from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QTreeWidget, QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from PyQtUIkit.core.properties import IntProperty, PaletteProperty, StringProperty, IconProperty
from PyQtUIkit.widgets.vbox_layout import KitVBoxLayout
from PyQtUIkit.widgets.hbox_layout import KitHBoxLayout
from PyQtUIkit.widgets.scroll_area import KitScrollArea
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitTreeWidgetItem(QVBoxLayout, _KitWidget):
    name = StringProperty('name', '')
    radius = IntProperty('radius', 4)

    def __init__(self, name='', icon=''):
        super().__init__()
        self._name = name
        self._icon = icon
        self.__level = 0
        self.__selected = False
        self.__expanded = False
        self.__children: list[KitTreeWidgetItem] = []
        self.__root: KitTreeWidget = None
        self._icon1 = None
        self._icon2 = None

        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.__button = QPushButton()
        self.__button.setFixedHeight(24)
        self.__button.clicked.connect(self._on_clicked)
        self.addWidget(self.__button)

        self.__top_layout = QHBoxLayout()
        self.__top_layout.setContentsMargins(0, 0, 0, 0)
        self.__top_layout.setSpacing(5)
        self.__button.setLayout(self.__top_layout)

        self.__arrow_right = QPushButton()
        self.__arrow_right.setFixedSize(20, 20)
        self.__arrow_right.hide()
        self.__arrow_right.clicked.connect(self.expand)
        self.__top_layout.addWidget(self.__arrow_right)

        self.__arrow_down = QPushButton()
        self.__arrow_down.setFixedSize(20, 20)
        self.__arrow_down.hide()
        self.__arrow_down.clicked.connect(self.collapse)
        self.__top_layout.addWidget(self.__arrow_down)

        self.__label = QLabel(self._name)
        self.__top_layout.addWidget(self.__label)

        self.__widget = QWidget()
        self.addWidget(self.__widget)
        self.__widget.hide()

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__widget.setLayout(self.__layout)

    def addItem(self, item: 'KitTreeWidgetItem') -> None:
        self.insertItem(len(self.__children), item)

    def insertItem(self, index, item: 'KitTreeWidgetItem'):
        item._set_level(self.__level + 1)
        item._set_tm(self._tm)
        item._set_root(self.__root)
        if self._tm and self._tm.active:
            item._apply_theme()

        self.__arrow_down.setHidden(not self.__expanded)
        self.__arrow_right.setHidden(self.__expanded)
        self._update_padding()

        self.__children.insert(index, item)
        self.__layout.insertLayout(index, item)

    def clear(self):
        for _ in range(self.count()):
            self.takeAt(0).widget().setParent(None)
        for el in self.__children:
            if el.selected():
                self.__root._set_current(None)
        self.__children.clear()

    def deleteItem(self, index):
        self.takeAt(index).widget().setParent(None)
        if self.__children.pop(index).selected():
            self.__root._set_current(None)

    def expand(self):
        self.__expanded = True
        self.__widget.show()
        self.__arrow_down.show()
        self.__arrow_right.hide()

    def collapse(self):
        self.__expanded = False
        self.__widget.hide()
        self.__arrow_down.hide()
        self.__arrow_right.show()

    def selected(self):
        return self.__selected

    def _on_clicked(self):
        if self.__selected:
            return
        self.__selected = True
        self._apply_selected_theme()
        self.__root._set_current(self)

    def _deselect(self):
        self.__selected = False
        self._apply_selected_theme()

    def _set_level(self, level):
        self.__level = level
        self._update_padding()
        for item in self.__children:
            item._set_level(self.__level + 1)

    def _update_padding(self):
        self.__top_layout.setContentsMargins((self.__level - 1) * 15 + 3 + (0 if self.__children else 25), 0, 0, 0)

    def _hide_button(self):
        self.__button.hide()

    def _set_tm(self, tm):
        super()._set_tm(tm)
        for el in self.__children:
            el._set_tm(tm)

    def _set_root(self, root):
        self.__root = root
        for el in self.__children:
            el._set_root(root)

    def _apply_theme(self):
        for el in self.__children:
            el.main_palette = self._main_palette
        self.__arrow_right.setIcon(self.__root._icon1)
        self.__arrow_down.setIcon(self.__root._icon2)
        self._apply_selected_theme()
        for el in [self.__arrow_right, self.__arrow_down]:
            el.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 0px solid black;
                border-radius: {self.radius}px;
            }}
            QPushButton:hover {{
                background-color: {self.main_palette.main};
            }}
            """)
        self.__label.setStyleSheet(f"color: {self.main_palette.text}; background-color: transparent;")
        for el in self.__children:
            el._apply_theme()

    def _apply_selected_theme(self):
        self.__button.setStyleSheet(f"""
            QPushButton {{
                color: {self.main_palette.text};
                background-color: {self.main_palette.selected if self.__selected else self.main_palette.main};
                border: 0px solid black;
                border-radius: {self.radius}px;
            }}
            QPushButton:hover {{
                background-color: {self.main_palette.selected if self.__selected else self.main_palette.hover};
            }}
            """)


class KitTreeWidget(KitScrollArea):
    currentItemChanged = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.__children = []
        self._main_palette = 'Main'
        self._border = 1

        self.__current = None

        self.__tree = KitTreeWidgetItem()
        self.__tree._hide_button()
        self.__tree._set_root(self)
        self.__tree.expand()

        self.__widget = QWidget()
        self.__widget.setLayout(self.__tree)

        self.setWidget(self.__widget)

    def addItem(self, item: KitTreeWidgetItem):
        item._main_palette = self._main_palette
        self.__tree.addItem(item)

    def currentItem(self) -> KitTreeWidgetItem | None:
        return self.__current

    def _set_current(self, item):
        if isinstance(self.__current, KitTreeWidgetItem):
            self.__current._deselect()
        self.currentItemChanged.emit(item)
        self.__current = item

    def _set_tm(self, tm):
        super()._set_tm(tm)
        self.__tree._set_tm(tm)

    def _apply_theme(self):
        self.__tree.main_palette = self._main_palette
        self.__widget.setStyleSheet("background-color: transparent;")
        self._icon1 = self._tm.icon('solid-angle-right', self.main_palette.text)
        self._icon2 = self._tm.icon('solid-angle-down', self.main_palette.text)
        self.__tree._apply_theme()
        super()._apply_theme()
