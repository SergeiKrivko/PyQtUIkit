from time import time

from PyQt6.QtCore import pyqtSignal, Qt, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QSizePolicy, QWidget
from PyQt6.QtGui import QFontMetrics

from PyQtUIkit.core.properties import IntProperty, PaletteProperty, IconProperty
from PyQtUIkit.themes import KitPalette
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget
from PyQtUIkit.widgets.icon_widget import KitIconWidget
from PyQtUIkit.widgets.button import KitIconButton, KitButton
from PyQtUIkit.widgets.scroll_area import KitScrollArea
from PyQtUIkit.widgets.hbox_layout import KitHBoxLayout
from PyQtUIkit.widgets.label import KitLabel


class KitTab(QPushButton, _KitWidget):
    radius_top = IntProperty('radius_top', 5)
    radius_bottom = IntProperty('radius_bottom', 0)

    selected = pyqtSignal(object)
    _mousePress = pyqtSignal(object)
    _mouseRelease = pyqtSignal()
    icon = IconProperty('icon')

    def __init__(self, name, value=None, icon=''):
        super().__init__()
        self._name = name
        self._value = value or name
        self._icon = icon
        self.__click_time = 0
        self.__checked = False

        self.__closable = False

        layout = QHBoxLayout()
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)

        self.__icon_widget = KitIconWidget(icon)
        self.__icon_widget.setFixedSize(18, 18)
        layout.addWidget(self.__icon_widget)

        self.__label = KitLabel(name)
        self.__label.setContentsMargins(4, 0, 4, 0)
        layout.addWidget(self.__label)

        self.__button_close = KitIconButton(icon='solid-xmark')
        self.__button_close.border = 0
        self.__button_close.size = 18
        self.__button_close.hide()
        layout.addWidget(self.__button_close)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _set_checked(self, flag):
        self.__checked = flag
        self._apply_theme()

    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)
        if e.button() == Qt.MouseButton.LeftButton:
            self._mousePress.emit(self.mapToParent(e.pos()))
            self.__click_time = time()

    def mouseReleaseEvent(self, e) -> None:
        super().mouseReleaseEvent(e)
        if e.button() == Qt.MouseButton.LeftButton and time() - self.__click_time < 0.5:
            self.__click_time = 0
            if not self.__checked:
                self._on_clicked()
        self._mouseRelease.emit()

    def _set_closable(self, flag):
        self.__closable = flag
        self.__button_close.setHidden(not flag)

    def _on_clicked(self):
        self.selected.emit(self)

    def _set_tm(self, tm):
        super()._set_tm(tm)
        self.__button_close._set_tm(tm)
        self.__icon_widget._set_tm(tm)
        self.__label._set_tm(tm)

    @property
    def value(self):
        return self._value

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.__button_close.main_palette = KitPalette('#00000000', self.main_palette.main,
                                                      text=self.main_palette.text)
        self.__label.setFont(self._tm.font_small)
        self.setStyleSheet(f"""
QPushButton {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main if not self.__checked else self.main_palette.selected};
    border: 0px solid {self._tm['Border'].main};
    border-top-left-radius: {self.radius_top}px;
    border-top-right-radius: {self.radius_top}px;
    border-bottom-left-radius: {self.radius_bottom}px;
    border-bottom-right-radius: {self.radius_bottom}px;
    padding: 3px 5px 3px 5px;
    text-align: left;
}}
QPushButton::hover {{
    background-color: {self.main_palette.hover if not self.__checked else self.main_palette.selected};
}}""")
        font_metrics = QFontMetrics(self.font())
        width = font_metrics.size(0, self.__label.text()).width() + 10
        if self.icon:
            width += 20
        if self.__closable:
            width += 20
        self.setFixedWidth(width)

        self.__label._apply_theme()
        self.__icon_widget.setHidden(not self.icon)
        self.__icon_widget.icon = self.icon
        self.__button_close._apply_theme()


class KitTabBar(KitHBoxLayout, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Bg')
    tabs_palette = PaletteProperty('tabs_palette', 'Main')
    height = IntProperty('height', 26)
    border = IntProperty('border', 0)
    radius = IntProperty('radius', 4)

    currentChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.__tabs: list[KitTab] = []
        self.__current = None
        self.__tabs_closable = False
        self.__tabs_movable = False
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self._main_palette = 'Bg'

        self.__button_left = KitButton(icon='solid-chevron-left')
        self.__button_left.border = 0
        self.__button_left.setFixedWidth(20)
        self.__button_left.clicked.connect(self._scroll_left)
        self.addWidget(self.__button_left)

        self.__scroll_area = KitScrollArea()
        self.addWidget(self.__scroll_area)
        self.__layout = _TabLayout(self.__tabs)
        self.__scroll_area.setWidget(self.__layout)
        self.__scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.__button_right = KitButton(icon='solid-chevron-right')
        self.__button_right.border = 0
        self.__button_right.setFixedWidth(20)
        self.__button_right.clicked.connect(self._scroll_right)
        self.addWidget(self.__button_right)

    def addTab(self, tab: str | KitTab):
        self.insertTab(len(self.__tabs), tab)

    def insertTab(self, index, tab: str | KitTab):
        if isinstance(tab, str):
            tab = KitTab(tab)
        tab._set_closable(self.__tabs_closable)
        tab._set_tm(self._tm)
        tab.selected.connect(lambda: self.setCurrentTab(tab))
        tab._mousePress.connect(self.__layout.on_mouse_press)
        tab._mouseRelease.connect(self.__layout.on_mouse_release)
        self.__tabs.insert(index, tab)
        self.__layout.update_tabs()
        if self.__current is None:
            self.__current = tab
            tab._set_checked(True)

    def _scroll_left(self):
        self.__scroll_area.scroll(-10)

    def _scroll_right(self):
        self.__scroll_area.scroll(10)

    def setTabsClosable(self, flag):
        self.__tabs_closable = flag
        for el in self.__tabs:
            el._set_closable(flag)

    def setTabsMovable(self, flag):
        self.__tabs_movable = flag
        self.__layout.set_tabs_movable(flag)

    def setCurrentTab(self, tab: int | KitTab):
        if isinstance(tab, int):
            tab = self.__tabs[tab]
        self.__current._set_checked(False)
        self.__current = tab
        self.__current._set_checked(True)
        self.currentChanged.emit(self.__tabs.index(tab))

    def _set_tm(self, tm):
        super()._set_tm(tm)
        for el in self.__tabs:
            el._set_tm(tm)

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self.__button_left.setHidden(self.__layout.width() <= self.width())
        self.__button_right.setHidden(self.__layout.width() <= self.width())

    def _apply_theme(self):
        self.__button_left.setHidden(self.__layout.width() <= self.width())
        self.__button_right.setHidden(self.__layout.width() <= self.width())
        self.__scroll_area.main_palette = self.main_palette
        self.__scroll_area.setFixedHeight(self.height)
        self.__button_left.main_palette = self.main_palette
        self.__button_right.main_palette = self.main_palette
        super()._apply_theme()
        for el in self.__tabs:
            el.main_palette = self.tabs_palette
            el.setFixedHeight(self.height)
            el._apply_theme()
        self.__layout.update_tabs()


class _TabLayout(QWidget):
    def __init__(self, widgets: list[KitTab]):
        super().__init__()
        self.__widgets = widgets
        self.__tabs_movable = False
        self.__widgets_positions = [0 for _ in widgets]
        self.__last_pos = QPoint(0, 0)
        self.__tab_move: KitTab | None = None
        self.__tab_move_index = 0
        self.__animations: dict[int: QPropertyAnimation] = dict()

    def update_tabs(self):
        x = 0
        self.__widgets_positions.clear()
        for el in self.__widgets:
            if el != self.__tab_move:
                el.setParent(self)
                el.move(x, 0)
            self.__widgets_positions.append(x)
            x += el.width()
        self.setFixedWidth(x)

    def on_mouse_press(self, pos: QPoint):
        if not self.__tabs_movable:
            return
        index = -1
        for el in self.__widgets:
            if el.pos().x() > pos.x():
                break
            index += 1
        self.__tab_move = self.__widgets[index]
        self.__tab_move_index = index
        self.__last_pos = pos

    def mouseReleaseEvent(self, a0) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.on_mouse_release()

    def on_mouse_release(self):
        if self.__tab_move is not None:
            self.__move_tab(self.__tab_move_index)
            self.__tab_move = None

    def mouseMoveEvent(self, a0) -> None:
        if self.__tab_move:
            self.__tab_move.move(self.__tab_move.pos() - QPoint(self.__last_pos.x() - a0.pos().x(), 0))
            self.__last_pos = a0.pos()
            i = self.__tab_move_index - 1
            while i >= 0 and self.__tab_move.x() + self.__tab_move.width() // 2 < \
                    self.__widgets_positions[i] + self.__widgets[i].width() // 2:
                self.__move_right(i)
                i -= 1
            i = self.__tab_move_index + 1
            while i < len(self.__widgets) and self.__tab_move.x() + self.__tab_move.width() // 2 > \
                    self.__widgets_positions[i] + self.__widgets[i].width() // 2:
                self.__move_left(i)
                i += 1

    def set_tabs_movable(self, flag):
        self.__tabs_movable = flag

    def __move_right(self, index):
        self.__widgets[index], self.__widgets[index + 1] = self.__widgets[index + 1], self.__widgets[index]
        self.__widgets_positions[index + 1] = self.__widgets_positions[index] + self.__tab_move.width()
        self.__move_tab(index + 1)
        self.__tab_move_index -= 1

    def __move_left(self, index):
        self.__widgets[index], self.__widgets[index - 1] = self.__widgets[index - 1], self.__widgets[index]
        self.__widgets_positions[index] = self.__widgets_positions[index - 1] + self.__widgets[index - 1].width()
        self.__move_tab(index - 1)
        self.__tab_move_index += 1

    def __move_tab(self, index):
        tab = self.__widgets[index]
        if index in self.__animations:
            self.__animations[index].stop()
        anim = QPropertyAnimation(tab, b'pos')
        anim.setEndValue(QPoint(self.__widgets_positions[index], 0))
        anim.setDuration(200)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.__animations[index] = anim
        anim.start()
