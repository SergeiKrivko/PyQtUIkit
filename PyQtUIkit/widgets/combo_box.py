from PyQt6.QtCore import pyqtSignal, Qt, QPoint, QPropertyAnimation, QEasingCurve, QSize, QParallelAnimationGroup
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QMenu, QHBoxLayout, QApplication

from PyQtUIkit.core import IntProperty, PaletteProperty, IconProperty, EnumProperty, KitFont, FontProperty, \
    MethodsProperty, TextProperty
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget, KitGroupItem as _KitGroupItem
from PyQtUIkit.widgets.icon_widget import KitIconWidget
from PyQtUIkit.widgets.scroll_area import KitScrollArea
from PyQtUIkit.widgets.layout import KitVBoxLayout
from PyQtUIkit.widgets.button import KitLayoutButton


class KitComboBoxItem(QPushButton, _KitWidget):
    selected = pyqtSignal(object)
    icon = IconProperty('icon')
    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)
    text = TextProperty('text')

    def __init__(self, name='', value=None, icon=''):
        super().__init__()
        self._text = name
        self._value = value if value is not None else name
        self._icon = icon
        self.setCheckable(True)
        self.clicked.connect(self._on_clicked)
        self.setFixedHeight(24)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _on_clicked(self, flag):
        if not flag:
            self.setChecked(True)
        self.selected.emit(self)

    @property
    def value(self):
        return self._value

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFont(self.font.get(self.font_size))
        self.setStyleSheet(f"""
QPushButton {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: 0px solid {self.border_palette.main};
    border-radius: 5px;
    padding: 3px 5px 3px 5px;
    text-align: left;
}}
QPushButton::hover {{
    background-color: {self.main_palette.hover};
}}
QPushButton::checked {{
    background-color: {self.main_palette.selected};
}}""")
        if self.icon is not None:
            self.setIcon(self.icon.icon(self.main_palette.text))

    def _apply_lang(self):
        self.setText(self.text)


class KitComboBox(QPushButton, _KitGroupItem):
    main_palette = PaletteProperty('main_palette', 'Main')
    type = IntProperty('type', 1)
    icon = IconProperty('icon')
    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)

    currentIndexChanged = pyqtSignal(object)
    currentValueChanged = pyqtSignal(object)

    def __init__(self, *values: str | tuple | KitComboBoxItem):
        super().__init__()
        self.__widgets: list[KitComboBoxItem] = []
        self.__current = None
        self.__menu = _ComboBoxMenu()
        self.__menu.setFixedWidth(self.width())
        self.clicked.connect(self._show_menu)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.setContentsMargins(0, 0, 6, 0)
        self.setLayout(layout)
        self._arrow = KitIconWidget('line-chevron-down')
        self._arrow._use_text_only = False
        self._arrow.setFixedSize(16, 12)
        layout.addWidget(self._arrow)

        for el in values:
            self.addItem(el)

        self._add_child_func = self.addItem

    def addItem(self, item: str | KitComboBoxItem, value=None):
        if not isinstance(item, KitComboBoxItem):
            item = KitComboBoxItem(item, value)
        item.selected.connect(self._on_item_selected)
        self.__widgets.append(item)
        self.__menu.add_item(item)
        if len(self.__widgets) == 1:
            self.setCurrentIndex(0)

    def deleteItem(self, index):
        self.__widgets.pop(index)
        self.__menu.delete_item(index)
        if index == self.__current:
            self.__current = min(self.__current, len(self.__widgets) - 1)
            if not self.__widgets:
                self.__current = None
                self.setIcon(QIcon())
                self.setText('')

    def clear(self):
        self.__widgets.clear()
        self.__menu.clear()
        self.__current = None
        self.setIcon(QIcon())
        self.setText('')

    def currentItem(self):
        if not self.__widgets:
            return None
        return self.__widgets[self.__current]

    def count(self):
        return len(self.__widgets)

    def currentValue(self):
        if not self.__widgets:
            return None
        return self.__widgets[self.__current].value

    def setCurrentIndex(self, index):
        if self.__current is not None:
            self.__widgets[self.__current].setChecked(False)
        self.__current = index
        self.__widgets[self.__current].setChecked(True)

        if self.__current is not None:
            self.setText(self.__widgets[self.__current].text)
            if self.__widgets[self.__current].icon is not None and self._tm and self._tm.active:
                self.setIcon(self.__widgets[self.__current].icon.icon(self.main_palette.text))
        self.currentValueChanged.emit(self.currentValue())
        self.currentIndexChanged.emit(self.__current)

    def _show_menu(self):
        pos = QPoint(0, self.height() if self.type == 1 else self.height() // 2)
        self.__menu.open(self.mapToGlobal(pos), self.type)

    def _on_item_selected(self, item: KitComboBoxItem):
        self.setCurrentIndex(self.__widgets.index(item))
        self.__menu.close()

    def _set_tm(self, tm):
        super()._set_tm(tm)
        self.__menu._set_tm(tm)
        self._arrow._set_tm(tm)

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self.__menu.setFixedWidth(self.width())

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
    text-align: left;
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
}}""")
        if self.__current is not None and self.__widgets[self.__current].icon is not None:
            self.setIcon(self.__widgets[self.__current].icon.icon(self.main_palette.text))
        self.__menu._apply_theme()
        self._arrow._apply_theme()

    def _apply_lang(self):
        if not self._tm:
            return
        item = self.currentItem()
        self.setText('' if not item else item.text)
        for el in self.__widgets:
            el._apply_lang()


class _ComboBoxMenu(QMenu, _KitWidget):
    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)

    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(2, 2, 1, 2)
        self.setLayout(main_layout)

        self._scroll_area = KitScrollArea()
        main_layout.addWidget(self._scroll_area)

        self._scroll_layout = KitVBoxLayout()
        self._scroll_layout.setContentsMargins(3, 3, 3, 3)
        self._scroll_layout.setSpacing(2)
        self._scroll_area.setWidget(self._scroll_layout)

        self._height = 10
        self.__anim = None
        self.__pos = QPoint(0, 0)

    def _resize(self):
        self._height = 26 * min(12, self._scroll_layout.count()) + 8
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded if
                                                     self._scroll_layout.count() > 12 else
                                                     Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.resize(self.width(), self._height)

    def _set_tm(self, tm):
        super()._set_tm(tm)
        self._scroll_area._set_tm(tm)

    def add_item(self, item: KitComboBoxItem):
        self._scroll_layout.addWidget(item)
        self._resize()

    def delete_item(self, index):
        self._scroll_layout.deleteWidget(index)

    def clear(self) -> None:
        self._scroll_layout.clear()

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setStyleSheet(f"""
QMenu {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: 1px solid {self.border_palette.main};
    border-radius: 5px;
    spacing: 4px;
    padding: 3px;
}}""")
        self._scroll_area._apply_theme()

    def open(self, pos: QPoint, type=1):
        self.__pos = pos
        screen_size = QApplication.primaryScreen().size()
        target_pos = pos - QPoint(0, 0 if type == 1 else self._height // 2)
        if target_pos.y() < 20:
            target_pos.setY(20)
        elif target_pos.y() + self._height > screen_size.height() - 20:
            target_pos.setY(screen_size.height() - self._height - 20)
        self.move(pos)
        self.resize(self.width(), 0)

        pos_anim = QPropertyAnimation(self, b"pos")
        pos_anim.setEndValue(target_pos)
        pos_anim.setDuration(200)
        pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        height_anim = QPropertyAnimation(self, b"size")
        height_anim.setEndValue(QSize(self.width(), self._height))
        height_anim.setDuration(200)
        height_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.__anim = QParallelAnimationGroup()
        self.__anim.addAnimation(pos_anim)
        self.__anim.addAnimation(height_anim)
        self.__anim.start()

        self.exec()


class KitLanguageBox(KitComboBox):
    langChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__loading = False
        self.currentValueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, value):
        if self.__loading:
            return
        self.theme_manager.set_lang(value)
        self.langChanged.emit(value)

    def _apply_lang(self):
        if not self._tm:
            return
        self.__loading = True
        self.clear()
        for lang, name in self.theme_manager.get_languages():
            self.addItem(KitComboBoxItem(name, lang))
            if lang == self.theme_manager.lang:
                self.setCurrentIndex(self.count() - 1)
        self.__loading = False
