from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QSizePolicy

from PyQtUIkit.core.icon import KitIcon
from PyQtUIkit.core import IntProperty, PaletteProperty, IconProperty, EnumProperty, KitFont, FontProperty, TextProperty
from PyQtUIkit.widgets import KitVBoxLayout, KitIconButton, KitIconWidget
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitNavigationButton(QPushButton, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Main')
    icon = IconProperty('icon')
    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)
    text = TextProperty('text')

    selected = pyqtSignal()

    def __init__(self, text='', icon=None):
        super().__init__()
        self._text = text
        self._main_palette = 'Main'
        self.__widgets = []
        self._radius = 4
        self._size = 30
        self.setCheckable(True)
        self.clicked.connect(self._on_clicked)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.__layout = QHBoxLayout()
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__layout.setContentsMargins(4, 4, 4, 4)
        self.__layout.setSpacing(4)
        self.setLayout(self.__layout)

        self.__icon = KitIconWidget()
        self.__icon._use_text_only = False
        self.__layout.addWidget(self.__icon)

        self.__label = QLabel()
        self.__layout.addWidget(self.__label)

        self._icon = icon
        self._set_expanded(False)

    def _on_clicked(self, flag):
        if not flag:
            self.setChecked(True)
        else:
            self.selected.emit()

    def _set_expanded(self, expanded):
        self.__label.setHidden(not expanded)
        if expanded:
            self.setMaximumWidth(1000)
        else:
            self.setFixedWidth(self._size)

    def _expanded_width(self):
        fm = QFontMetrics(self.__label.font())
        fm.size(0, self.__label.text())
        return 44 + fm.size(0, self.__label.text()).width()

    def _set_tm(self, tm):
        super()._set_tm(tm)
        self.__icon._set_tm(tm)

    def _apply_theme(self):
        self._set_expanded(not self.__label.isHidden())
        self.setFixedHeight(self._size)
        self.__icon.setFixedSize(self._size - 8, self._size - 8)
        self.__icon._main_palette = self._main_palette
        self.__label.setFont(self.font.get(self.font_size))
        self.setStyleSheet(f"""
QPushButton {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: 0px solid {self.border_palette.main};
    border-radius: {self._radius}px;
    padding: 3px 8px 3px 8px;
}}
QPushButton::hover {{
    background-color: {self.main_palette.hover};
}}
QPushButton::checked {{
    background-color: {self.main_palette.selected};
}}""")
        self.__label.setStyleSheet(f"color: {self.main_palette.text}; border: none; background-color: transparent")
        if self.icon is not None:
            self.__icon.icon = self.icon

    def _apply_lang(self):
        self.__label.setText(self.text)


class KitNavigation(KitVBoxLayout):
    button_size = IntProperty('button_size', 30)
    button_radius = IntProperty('button_radius', 4)
    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)

    currentChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._main_palette = 'Menu'
        self._radius = 0
        self.__tabs = []
        self.__expanded = False
        self.__current = None

        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setContentsMargins(5, 5, 5, 5)
        self.setSpacing(5)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.__button = KitIconButton('line-reorder-three')
        self.__button.border = 0
        self.__button.clicked.connect(self._on_clicked)
        self.addWidget(self.__button)

        self.__anim = None

    def _on_clicked(self):
        if self.__expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self):
        self.__expanded = True
        if isinstance(self.__anim, QPropertyAnimation):
            self.__anim.stop()
        width = max(el._expanded_width() for el in self.__tabs) + \
                self.contentsMargins().left() + self.contentsMargins().right()
        self.__anim = QPropertyAnimation(self, b'maximumWidth')
        self.__anim.setEndValue(width)
        self.__anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.__anim.start()
        for el in self.__tabs:
            el._set_expanded(True)

    def collapse(self):
        self.__expanded = False
        if isinstance(self.__anim, QPropertyAnimation):
            self.__anim.stop()
        width = self.button_size + self.contentsMargins().left() + self.contentsMargins().right()
        self.__anim = QPropertyAnimation(self, b'maximumWidth')
        self.__anim.setEndValue(width)
        self.__anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.__anim.start()
        for el in self.__tabs:
            el._set_expanded(False)

    def setCurrentTab(self, tab: int):
        if isinstance(tab, int):
            tab = self.__tabs[tab]
        self.__current.setChecked(False)
        self.__current = tab
        self.__current.setChecked(True)
        self.currentChanged.emit(self.__tabs.index(tab))

    def _on_tab_selected(self, button: KitNavigationButton):
        if isinstance(self.__current, KitNavigationButton):
            self.__current.setChecked(False)
        self.__current = button
        self.currentChanged.emit(self.__tabs.index(button))

    def addTab(self, name: str, icon: str | KitIcon):
        self.insertTab(len(self.__tabs), name, icon)

    def insertTab(self, index: int, name: str, icon: str | KitIcon):
        button = KitNavigationButton(name, icon)
        button.selected.connect(lambda: self._on_tab_selected(button))
        self.__tabs.insert(index, button)
        if not self.__current:
            self.__current = button
            button.setChecked(True)
        self.insertWidget(index + 1, button)

    def clear(self):
        super().clear()
        self.addWidget(self.__button)
        self.__tabs.clear()
        self.__current = None

    def currentIndex(self):
        if self.__current is None:
            return None
        return self.__tabs.index(self.__current)

    def _apply_theme(self):
        self.setMaximumWidth(self.button_size + self.contentsMargins().left() + self.contentsMargins().right())
        self.__button.main_palette = self._main_palette
        self.__button.size = self.button_size
        for el in self.__tabs:
            el.main_palette = self.main_palette
            el.font = self.font
            el.font_size = self.font_size
            el._size = self.button_size
            el._radius = self.button_radius
        super()._apply_theme()

    def _apply_lang(self):
        for el in self.__tabs:
            el._apply_lang()
        if self.__expanded:
            self.expand()
