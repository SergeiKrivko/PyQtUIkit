from enum import Enum

from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from PyQtUIkit.core import KitFont
from PyQtUIkit.core.properties import IntProperty, StringProperty, IconProperty, BoolProperty, EnumProperty, \
    PaletteProperty, FontProperty
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget
from PyQtUIkit.widgets.dialog import KitDialog
from PyQtUIkit.widgets.hbox_layout import KitHBoxLayout
from PyQtUIkit.widgets.icon_widget import KitIconWidget
from PyQtUIkit.widgets.label import KitLabel
from PyQtUIkit.widgets.scroll_area import KitScrollArea


class KitTreeWidgetItem(QVBoxLayout, _KitWidget):
    name = StringProperty('name', '')
    radius = IntProperty('radius', 4)
    icon = IconProperty('icon')
    text_palette = PaletteProperty('text_palette', 'Main')
    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)

    def __init__(self, name='', icon=''):
        super().__init__()
        self._name = name
        self._icon = icon
        self._main_palette = 'Main'
        self._text_palette = 'Main'
        self.__level = 0
        self._height = 24
        self.__selected = False
        self.__expanded = False
        self.__children: list[KitTreeWidgetItem] = []
        self.__root: KitTreeWidget = None
        self.__parent: KitTreeWidgetItem = None
        self._icon1 = None
        self._icon2 = None
        self.__never_expanded = True
        self.__move_widget = None
        self.__last_pos = None

        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.__button = QPushButton()
        self.__button.mousePressEvent = self._on_clicked
        self.__button.mouseMoveEvent = self._on_move
        self.__button.mouseReleaseEvent = self._on_released
        self.__button.mouseDoubleClickEvent = self._on_double_clicked
        self.addWidget(self.__button)

        self.__top_layout = QHBoxLayout()
        self.__top_layout.setContentsMargins(0, 0, 0, 0)
        self.__top_layout.setSpacing(3)
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

        self.__icon_widget = KitIconWidget()
        self.__top_layout.addWidget(self.__icon_widget)

        self.__label = QLabel(self._name)
        self.__top_layout.addWidget(self.__label)

        self.__widget = QWidget()
        self.addWidget(self.__widget)
        self.__widget.hide()

        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(0)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__widget.setLayout(self.__layout)

    def parent(self):
        return self.__parent

    def level(self):
        return self.__level

    def children(self) -> list['KitTreeWidgetItem']:
        return self.__children

    def addItem(self, item: 'KitTreeWidgetItem') -> None:
        self.insertItem(len(self.__children), item)

    def insertItem(self, index, item: 'KitTreeWidgetItem'):
        item._set_level(self.__level + 1)
        item._set_root(self.__root, self)
        item._set_tm(self._tm)

        self.__children.insert(index, item)
        self.__layout.insertLayout(index, item)

        self.__arrow_down.setHidden(not self.__expanded)
        self.__arrow_right.setHidden(self.__expanded)
        self._update_padding()

    def childrenCount(self):
        return len(self.__children)

    def child(self, index):
        return self.__children[index]

    def clear(self):
        for _ in range(self.count()):
            self.takeAt(0).widget().setParent(None)
        for el in self.__children:
            if el.selected():
                self.__root._set_current(None)
        self.__children.clear()

    def deleteItem(self, item):
        if isinstance(item, KitTreeWidgetItem):
            item = self.__children.index(item)
        self.takeAt(item).widget().setParent(None)
        if self.__children.pop(item).selected():
            self.__root._set_current(None)

    def deleteSelf(self):
        self.__parent.deleteItem(self)

    def expand(self):
        self.__expanded = True
        self.__widget.show()
        self.__arrow_down.show()
        self.__arrow_right.hide()
        if self.__never_expanded:
            self.firstExpand()
            self.__never_expanded = False

    def collapse(self):
        self.__expanded = False
        self.__widget.hide()
        self.__arrow_down.hide()
        self.__arrow_right.show()

    def selected(self):
        return self.__selected

    def firstExpand(self):
        pass

    def _on_clicked(self, a0):
        QPushButton.mousePressEvent(self.__button, a0)
        self.__last_pos = a0.pos()
        self.__root._item_click(self, right=a0.button() == Qt.MouseButton.RightButton)

    def _on_double_clicked(self, a0):
        QPushButton.mouseDoubleClickEvent(self.__button, a0)
        self.__root._item_double_click(self)

    def _select(self, multi=False):
        self.__selected = True
        self._apply_selected_theme()
        if multi:
            for el in self.__children:
                el._select(True)

    def _on_move(self, a0):
        QPushButton.mouseMoveEvent(self.__button, a0)
        if self.__last_pos is None:
            return
        if not self.__root.movable:
            return 
        if self.__move_widget is None:
            self.__move_widget = _MoveItem(self, (self.__button.width(), self._height), self.name, self._icon,
                                           self._text_palette)
            self.__move_widget.main_palette = self.main_palette
            self.__move_widget.move(self.__button.mapToGlobal(a0.pos()))
            self.__move_widget.show()
        else:
            self.__move_widget.move(self.__move_widget.pos() + a0.pos() - self.__last_pos)
        self.__last_pos = a0.pos()

    def _on_released(self, a0):
        QPushButton.mouseReleaseEvent(self.__button, a0)
        if isinstance(self.__move_widget, _MoveItem):
            self.__move_widget.close()
            self.__root._request_move(self, self.__move_widget.pos())
            self.__move_widget = None
        self.__last_pos = None

    def _deselect(self, multi=False):
        self.__selected = False
        self._apply_selected_theme()
        if multi:
            for el in self.__children:
                el._deselect(True)

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
        self.__icon_widget._set_tm(tm)
        for el in self.__children:
            el._set_tm(tm)

    def _set_root(self, root, parent):
        self.__root = root
        self.__parent = parent
        for el in self.__children:
            el._set_root(root, self)

    def _find_by_pos(self, pos: QPoint):
        if not self.__button.isHidden() and pos.x() < self.__button.width() and pos.y() < self.__button.height():
            return self, 0
        height = 0 if self.__button.isHidden() else self._height
        if self.__expanded:
            for i, el in enumerate(self.__children):
                res, h = el._find_by_pos(pos - QPoint(0, height))
                if res:
                    return res, 0
                height += h
        return None, height

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        for el in self.__children:
            el._height = self._height
            el.main_palette = self._main_palette
            el.text_palette = self._text_palette
        if self._icon:
            self.__icon_widget._icon = self._icon
            self.__icon_widget.show()
            self.__icon_widget._main_palette = self._text_palette
            self.__icon_widget.setFixedSize(self._height - 6, self._height - 6)
            self.__icon_widget._apply_theme()
        else:
            self.__icon_widget.hide()
        self.__button.setFixedHeight(self._height)
        self.__arrow_right.setIcon(self.__root._icon1)
        self.__arrow_down.setIcon(self.__root._icon2)
        self._apply_selected_theme()
        self.__label.setFont(self.font.get(self.font_size))
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
        self.__label.setStyleSheet(f"color: {self.text_palette.text_only}; background-color: transparent;")
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


class _MoveItem(KitDialog):
    def __init__(self, parent, size: tuple, name, icon='', palette='Main'):
        super().__init__(parent)
        self.button_close = False
        self.setFixedSize(*size)

        main_layout = KitHBoxLayout()
        self.setWidget(main_layout)

        if icon:
            self._icon_widget = KitIconWidget(icon)
            main_layout.addWidget(self._icon_widget)
            self._icon_widget.setFixedSize(size[1] - 6, size[1] - 6)
            self._icon_widget.main_palette = palette

        self._label = KitLabel(name)
        self._label.main_palette = palette
        main_layout.addWidget(self._label)


class KitTreeWidget(KitScrollArea):
    class SelectionType(Enum):
        NO = 0
        SINGLE = 1
        MULTI = 2

    item_height = IntProperty('item_height', 24)
    movable = BoolProperty('movable', False)
    selection_type = EnumProperty('selection_type', SelectionType, SelectionType.SINGLE)
    items_palette = PaletteProperty('items_palette', 'Main')

    currentItemChanged = pyqtSignal(object)
    moveRequested = pyqtSignal(object, object)
    doubleClicked = pyqtSignal(object)
    contextMenuRequested = pyqtSignal(QPoint, KitTreeWidgetItem)

    def __init__(self):
        super().__init__()
        self.__children = []
        self._main_palette = 'Main'
        self._items_palette = 'Main'
        self._border = 1
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

        self.__shift = False
        self.__control = False
        self.__current = None
        self.__selected = []
        self.__selected_level = 0

        self.__tree = KitTreeWidgetItem()
        self.__tree._hide_button()
        self.__tree._set_root(self, None)
        self.__tree.expand()

        self.__widget = QWidget()
        self.__widget.setLayout(self.__tree)
        self.setWidget(self.__widget)

    def addItem(self, item: KitTreeWidgetItem):
        item._main_palette = self._main_palette
        self.__tree.addItem(item)

    def currentItem(self) -> KitTreeWidgetItem | None:
        return self.__current

    def selectedItems(self):
        return self.__selected

    def _set_current(self, item):
        self.currentItemChanged.emit(item)
        self.__current = item

    def _request_move(self, item, pos):
        dest, _ = self.__tree._find_by_pos(pos - self.__widget.mapToGlobal(QPoint(0, 0)))
        if dest:
            self.moveRequested.emit(item, dest)

    def _item_click(self, item: KitTreeWidgetItem, right=False):
        if self.selection_type == KitTreeWidget.SelectionType.MULTI:
            if self.__control:
                if not item.selected():
                    self._add_to_selected(item)
                else:
                    self._remove_from_selected(item)
            elif self.__shift:
                self._shift_select(item)
            else:
                item._select(multi=False)
                for el in self.__selected:
                    el._deselect(multi=True)
                self.__selected.clear()
                self.__selected_level = item.level()
                self.__selected.append(item)
        elif self.selection_type == KitTreeWidget.SelectionType.SINGLE:
            self.__selected.clear()
            self.__selected.append(item)
            item._select()
            if isinstance(self.__current, KitTreeWidgetItem):
                self.__current._deselect()
        self._set_current(item)

    def _item_double_click(self, item: KitTreeWidgetItem):
        self.doubleClicked.emit(item)

    def _on_context_menu(self, pos):
        item, _ = self.__tree._find_by_pos(pos)
        self.contextMenuRequested.emit(pos, item)

    def _add_to_selected(self, item: KitTreeWidgetItem):
        if not self.__selected:
            self.__selected.append(item)
            self.__selected_level = item.level()
            item._select(multi=False)
        else:
            while self.__selected_level > item.level():
                it = self.__selected[0].parent()
                self.__selected.clear()
                self.__selected.append(it)
                self.__selected_level -= 1
            while self.__selected_level < item.level():
                item = item.parent()
            self.__selected.append(item)
            for el in self.__selected:
                el._select(multi=True)

    def _remove_from_selected(self, item: KitTreeWidgetItem):
        while self.__selected_level < item.level():
            item = item.parent()
        self.__selected.remove(item)
        item._deselect(multi=True)

    def _shift_select(self, item):
        for el in self.__selected:
            el._deselect(multi=True)
        self.__selected.clear()
        if isinstance(self.__current, KitTreeWidgetItem):
            while self.__current.level() < item.level():
                item = item.parent()
            while self.__current.level() > item.level():
                self.__current = self.__current.parent()
            while self.__current.parent() != item.parent():
                self.__current = self.__current.parent()
                item = item.parent()
            ind1, ind2 = item.parent().children().index(item), item.parent().children().index(self.__current)
            for i in range(min(ind1, ind2), max(ind1, ind2) + 1):
                it = item.parent().children()[i]
                self.__selected.append(it)
                it._select(multi=True)
        else:
            self.__selected.append(item)
            item._select()

    def keyPressEvent(self, a0) -> None:
        super().keyPressEvent(a0)
        if a0.key() == Qt.Key.Key_Shift:
            self.__shift = True
        elif a0.key() == Qt.Key.Key_Control:
            self.__control = True

    def keyReleaseEvent(self, a0) -> None:
        super().keyReleaseEvent(a0)
        if a0.key() == Qt.Key.Key_Shift:
            self.__shift = False
        elif a0.key() == Qt.Key.Key_Control:
            self.__control = False

    def _set_tm(self, tm):
        super()._set_tm(tm)
        self.__tree._set_tm(tm)

    def _apply_theme(self):
        self.__tree.main_palette = self._main_palette
        self.__widget.setStyleSheet("background-color: transparent;")
        self._icon1 = self._tm.icon('solid-angle-right', self.main_palette.text)
        self._icon2 = self._tm.icon('solid-angle-down', self.main_palette.text)
        self.__tree._main_palette = self._main_palette
        self.__tree._text_palette = self._items_palette
        self.__tree._apply_theme()
        super()._apply_theme()
