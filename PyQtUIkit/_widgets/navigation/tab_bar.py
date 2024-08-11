from typing import Iterable

from PyQt6.QtCore import QPropertyAnimation, QParallelAnimationGroup, QPoint, QSize

from PyQtUIkit._core.button_sequence import ButtonSequence
from PyQtUIkit._core.style_obj import ButtonStyle
from PyQtUIkit._widgets.buttons.button import KitButton
from PyQtUIkit._widgets.layout.box import KitHBoxLayout, KitVBoxLayout
from PyQtUIkit._widgets.card import KitCard


class KitTabBar(KitVBoxLayout):
    def __init__(self,
                 items: list[str] | list[dict] | list[object] | None = None,
                 name_field='name', value_field='value', icon_field=None,
                 classes: Iterable[str] | str = None, ):
        super().__init__(classes=classes)
        self.__sequence = ButtonSequence(_KitTabBarTab, items=items, name_field=name_field,
                                         value_field=value_field, icon_field=icon_field)
        self.__sequence.on_reload.add(self.__reload)
        self.__style = ButtonStyle()
        self.__final_style = ButtonStyle()

        self.__layout = KitHBoxLayout()
        self.__layout.height = 28
        self.add(self.__layout)

        rail = KitHBoxLayout()
        rail.height = 8
        self.add(rail)

        self.__line = KitCard()
        self.__line.qt_widget.setParent(rail.qt_widget)
        self.__line.show()

        self.height = 36

        self.__anim = None

        self.__sequence.on_current_change.add(self.__move_line)
        self.on_show.add(self.__move_line)
        self.__sequence.reload()

    @property
    def style(self) -> ButtonStyle:
        return self.__style

    @property
    def final_style(self) -> ButtonStyle:
        return self.__final_style

    @property
    def children(self) -> Iterable['KitWidget']:
        for el in super().children:
            yield el
        yield self.__line

    def __reload(self):
        self.__layout.clear()
        for el in self.__sequence.buttons:
            self.__layout.add(el)

    def __move_line(self):
        if isinstance(self.__anim, QPropertyAnimation):
            self.__anim.stop()

        item = self.__sequence.current
        if isinstance(item, _KitTabBarTab):
            self.__line.show()

            self.__anim = QParallelAnimationGroup()

            anim = QPropertyAnimation(self.__line.qt_widget, b'pos')
            anim.setEndValue(QPoint(item.qt_widget.x(), 2))
            self.__anim.addAnimation(anim)

            anim = QPropertyAnimation(self.__line.qt_widget, b'size')
            anim.setEndValue(QSize(item.width, 4))
            self.__anim.addAnimation(anim)

            self.__anim.start()
        else:
            self.__line.hide()

    def _apply_style(self):
        for el in self.__sequence.buttons:
            for cl in ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'contrast']:
                if cl in self.classes:
                    el.classes.add(cl)
                else:
                    el.classes.discard(cl)
        super()._apply_style()
        self.__line._apply_style()
        self.__move_line()


class _KitTabBarTab(KitButton):
    def __init__(self, name, value, icon):
        super().__init__(name, icon)
        self.__value = value
        self.checkable = True

    @property
    def value(self):
        return self.__value
