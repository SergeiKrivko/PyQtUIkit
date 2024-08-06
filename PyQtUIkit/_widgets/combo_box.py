from typing import Iterable

from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QSize, QParallelAnimationGroup
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QSizePolicy, QApplication

from PyQtUIkit._core.button_sequence import ButtonSequence
from PyQtUIkit._core.event import KitSignals
from PyQtUIkit._core.icon import KitIcon
from PyQtUIkit._core.locale import _KitLocaleString, _KitLocaleStringArray
from PyQtUIkit._widgets.base_menu import KitBaseMenu
from PyQtUIkit._widgets.button import KitButton
from PyQtUIkit._widgets.icon_widget import KitIconWidget
from PyQtUIkit._widgets.label import KitLabel
from PyQtUIkit._widgets.layout import KitVLayout, KitVBoxLayout
from PyQtUIkit._widgets.layout_button import KitLayoutButton
from PyQtUIkit._widgets.scroll_area import KitScrollArea
from PyQtUIkit._widgets.widget import KitWidget


class KitComboBox(KitLayoutButton):
    _DEFAULT_H_ICON_SIZE = 20

    def __init__(self,
                 items: Iterable[str] | Iterable[dict] | Iterable[object] = None,
                 name_field='name', value_field='value', icon_field='icon',
                 classes: Iterable[str] | str = None):
        super().__init__(classes=classes)

        self.__items = items
        self.__sequence = ButtonSequence(KitComboBoxItem, items=items, name_field=name_field,
                                         value_field=value_field, icon_field=icon_field)
        self.__sequence.on_reload.add(self.reload)

        self.__value_change_events = KitSignals()
        self.on_value_change.add(print)

        self.__icon_widget = KitIconWidget()
        self.add(self.__icon_widget)

        self.__label = KitLabel('')
        self.add(self.__label)

        self.__arrow_widget = KitIconWidget('line-chevron-down')
        self.__arrow_widget.size = 20
        self.add(self.__arrow_widget)

        self.__menu = KitComboBoxMenu(self.__sequence)

        self.on_click.add(self.__on_clicked)
        self.qt_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.__sequence.on_current_change.add(self.__on_current_change)
        self.__sequence.reload()

    @property
    def children(self) -> Iterable['KitWidget']:
        for el in super().children:
            yield el
        yield self.__menu

    @property
    def text(self) -> str:
        return self.__label.text

    @text.setter
    def text(self, text: str | _KitLocaleString | _KitLocaleStringArray):
        self.__label.text = text

    @property
    def icon(self) -> KitIcon | None:
        return self.__icon_widget.icon

    @icon.setter
    def icon(self, icon: KitIcon | str | None):
        self.__icon_widget.icon = icon

    @property
    def on_value_change(self) -> KitSignals:
        return self.__value_change_events

    @property
    def value(self):
        return self.__sequence.current.value

    @value.setter
    def value(self, value):
        for el in self.__sequence.buttons:
            if el.value == value:
                self.__sequence.current = el
                break
        raise ValueError("Value is not valid")

    def __on_clicked(self):
        pos = QPoint(0, self.height if 1 == 1 else self.height // 2)
        self.__menu.width = self.width
        self.__menu.open(self.qt_widget.mapToGlobal(pos), 1)

    def __apply_size(self):
        style = self.final_style.apply(self.style)
        if style.spacing is None:
            return
        fm = QFontMetrics(self.__label.qt_widget.font())
        size = fm.size(0, self.__label.qt_widget.text())
        width, height = size.width(), size.height()

        height = max(height, self._DEFAULT_H_ICON_SIZE)

        self.__label.qt_widget.setFixedSize(width, height)
        width += 20 + style.spacing
        if self.icon:
            self.__icon_widget.qt_widget.setFixedSize(self._DEFAULT_H_ICON_SIZE, height)
            width += style.spacing + self._DEFAULT_H_ICON_SIZE
        height += style.padding[0] + style.padding[2]
        width += style.padding[1] + style.padding[3]
        self.qt_widget.setMinimumSize(width, height)

    def __on_current_change(self, item: 'KitComboBoxItem'):
        self.text = item.text
        self.icon = item.icon
        self.__value_change_events(item.value)
        self.__apply_size()

    def _apply_style(self):
        if not self.icon:
            self.__icon_widget.hide()

        self.style.align = Qt.AlignmentFlag.AlignCenter
        self.__label.qt_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        super()._apply_style()
        self.__apply_size()
        self.__menu._apply_style()

    def reload(self):
        self.__menu.reload()

    def apply_lang(self):
        super().apply_lang()
        self.__menu.apply_lang()
        self.__apply_size()


class KitComboBoxItem(KitButton):
    def __init__(self,
                 text: str | _KitLocaleString | _KitLocaleStringArray,
                 value=None,
                 icon: str | KitIcon | None = None,):
        super().__init__(text, icon)
        self.__value = value
        self.qt_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.checkable = True

    @property
    def value(self):
        return self.__value


class KitComboBoxMenu(KitBaseMenu):
    def __init__(self, sequence: ButtonSequence):
        super().__init__()
        self.__sequence = sequence
        self.layout = KitVLayout()
        self.__scroll_area = KitScrollArea()
        self.layout.add(self.__scroll_area)
        self.__scroll_layout = KitVBoxLayout()
        self.__scroll_area.widget = self.__scroll_layout

        self._height = 10
        self.__anim = None
        self.__pos = QPoint(0, 0)
        self.__sequence.on_current_change.add(self.qt_widget.close)

    def __resize(self):
        self._height = 26 * min(12, self.__scroll_layout.count) + 8
        self.__scroll_area.qt_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded if
                                                                self.__scroll_layout.count > 12 else
                                                                Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.qt_widget.resize(self.width, self._height)

    def add(self, item):
        self.__scroll_layout.add(item)
        self.__resize()

    def clear(self):
        self.__scroll_layout.clear()
        self.__resize()

    def reload(self):
        self.clear()
        for el in self.__sequence.buttons:
            self.add(el)

    def open(self, pos: QPoint, type=1):
        self.__pos = pos
        screen_size = QApplication.primaryScreen().size()
        target_pos = pos - QPoint(0, 0 if type == 1 else self._height // 2)
        if target_pos.y() < 20:
            target_pos.setY(20)
        elif target_pos.y() + self._height > screen_size.height() - 20:
            target_pos.setY(screen_size.height() - self._height - 20)
        self.qt_widget.move(pos)
        self.qt_widget.resize(self.width, 0)

        pos_anim = QPropertyAnimation(self.qt_widget, b"pos")
        pos_anim.setEndValue(target_pos)
        pos_anim.setDuration(200)
        pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        height_anim = QPropertyAnimation(self.qt_widget, b"size")
        height_anim.setEndValue(QSize(self.width, self._height))
        height_anim.setDuration(200)
        height_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.__anim = QParallelAnimationGroup()
        self.__anim.addAnimation(pos_anim)
        self.__anim.addAnimation(height_anim)
        self.__anim.start()

        self.qt_widget.exec()
