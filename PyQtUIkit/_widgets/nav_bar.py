from typing import Iterable

from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QSizePolicy

from PyQtUIkit._core.button_sequence import ButtonSequence
from PyQtUIkit._core.style_obj import ButtonStyle
from PyQtUIkit._widgets.button import KitButton
from _core.icon import KitIcon
from _core.locale import _KitLocaleString, _KitLocaleStringArray
from _widgets.card import KitCard
from _widgets.divider import KitHDivider
from _widgets.icon_widget import KitIconWidget
from _widgets.label import KitLabel
from _widgets.layout import KitVLayout, KitVBoxLayout
from _widgets.layout_button import KitLayoutButton


class KitNavBar(KitCard):
    def __init__(self,
                 items: list[str] | list[dict] | list[object] | None = None,
                 name_field='name', value_field='value', icon_field='icon',
                 classes: Iterable[str] | str = None, ):
        super().__init__(KitVLayout(), classes=classes)
        self.__expanded = False
        self.__sequence = ButtonSequence(_KitNavBarItem, items=items, name_field=name_field,
                                         value_field=value_field, icon_field=icon_field)
        self.__sequence.on_reload.add(self.__reload)
        self.__anim: QPropertyAnimation | None = None
        self.__style = ButtonStyle()
        self.__final_style = ButtonStyle()

        self.__expand_button = KitButton(icon='line-menu', classes='text')
        self.__expand_button.on_click.add(self.__on_expand_button_clicked)
        self.layout.add(self.__expand_button)

        self.layout.add(KitHDivider())

        self.__layout = KitVBoxLayout()
        self.layout.add(self.__layout)

        self.layout.style.align = Qt.AlignmentFlag.AlignTop
        self.qt_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.__sequence.reload()

        def apply_buttons_width(width, height):
            for el in self.__sequence.buttons:
                el.set_size(width - self.layout.final_style.padding[1] - self.layout.final_style.padding[3])
        self.qt_widget.sizeChanged.connect(apply_buttons_width)

    @property
    def style(self) -> ButtonStyle:
        return self.__style

    @property
    def final_style(self) -> ButtonStyle:
        return self.__final_style

    def __reload(self):
        self.__layout.clear()
        for el in self.__sequence.buttons:
            self.__layout.add(el)

    def expand(self):
        for el in self.__sequence.buttons:
            el.expand()
        self.__start_animation()

    def collapse(self):
        for el in self.__sequence.buttons:
            el.collapse()
        self.__start_animation()

    def __start_animation(self, on_finish=None):
        width = max(b.calc_width() for b in self.__sequence.buttons)

        if self.__anim:
            self.__anim.stop()
        self.__anim = QPropertyAnimation(self.qt_widget, b'card_width')
        self.__anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.__anim.setEndValue(width + self.layout.final_style.padding[1] + self.layout.final_style.padding[3])
        if on_finish:
            self.__anim.finished.connect(on_finish)
        self.__anim.start()

    @property
    def expanded(self):
        return self.__expanded

    @expanded.setter
    def expanded(self, value):
        if value == self.__expanded:
            return
        self.__expanded = value
        if self.__expanded:
            self.expand()
        else:
            self.collapse()

    def __on_expand_button_clicked(self):
        self.expanded = not self.expanded

    def _apply_style(self):
        for el in self.__sequence.buttons:
            el.classes.add('text')
            for cl in ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'contrast']:
                if cl in self.classes:
                    el.classes.add(cl)
                else:
                    el.classes.discard(cl)
        for cl in ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'contrast']:
            if cl in self.classes:
                self.__expand_button.classes.add(cl)
            else:
                self.__expand_button.classes.discard(cl)
        super()._apply_style()
        self.max_width = max(b.calc_width() for b in self.__sequence.buttons) + self.layout.final_style.padding[1] + \
                         self.layout.final_style.padding[3]


class _KitNavBarItem(KitLayoutButton):
    ICON_SIZE = 28

    def __init__(self,
                 text: str | _KitLocaleString | _KitLocaleStringArray = '',
                 value=None,
                 icon: KitIcon | str = None, ):
        super().__init__(Qt.Orientation.Horizontal)
        self.__value = value
        self.__expanded = False
        self.checkable = True

        self.__icon_widget = KitIconWidget(icon)
        self.__icon_widget.size = _KitNavBarItem.ICON_SIZE
        self.add(self.__icon_widget)

        self.__label = KitLabel(text)
        self.__label.hide()
        self.add(self.__label)

        self.on_state_change.add(self.__on_checked_change)
        self.qt_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    @property
    def text(self) -> str:
        return self.__label.text

    @text.setter
    def text(self, text: str | _KitLocaleString | _KitLocaleStringArray):
        self.__label.text = text

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def icon(self) -> KitIcon | None:
        return self.__icon_widget.icon

    @icon.setter
    def icon(self, icon: KitIcon | str | None):
        self.__icon_widget.icon = icon

    def __on_checked_change(self, status):
        if status:
            self.__label.classes.add('pressed')
            self.__icon_widget.classes.add('pressed')
        else:
            self.__label.classes.discard('pressed')
            self.__icon_widget.classes.discard('pressed')
        self.__label._apply_style()
        self.__icon_widget._apply_style()

    def expand(self):
        self.__expanded = True
        self.__label.show()

    def collapse(self):
        self.__expanded = False
        self.__label.hide()

    def calc_width(self):
        style = self.final_style.apply(self.style)
        if self.__expanded:
            fm = QFontMetrics(self.__label.qt_widget.font())
            size = fm.size(0, self.__label.qt_widget.text())
            width, _ = size.width(), size.height()
            width += style.spacing
        else:
            width = 0
        width += _KitNavBarItem.ICON_SIZE + style.padding[1] + style.padding[3]
        return width

    def set_size(self, width):
        style = self.final_style
        self.__label.width = width - (_KitNavBarItem.ICON_SIZE + style.padding[1] + style.padding[3] + style.spacing)

    def _apply_style(self):
        self.style.align = Qt.AlignmentFlag.AlignCenter
        super()._apply_style()
        self.height = self.ICON_SIZE + self.final_style.padding[0] + self.final_style.padding[2]

    def apply_lang(self):
        super().apply_lang()
