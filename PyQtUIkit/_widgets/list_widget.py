import asyncio
from typing import Iterable
from uuid import uuid4

from PyQt6.QtCore import QPropertyAnimation, QParallelAnimationGroup
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QListWidget, QListWidgetItem

from PyQtUIkit._core.style_obj import ListStyle
from PyQtUIkit._widgets.widget import KitWidget
from PyQtUIkit._core.event import KitSignals
from PyQtUIkit._core.icon import KitIcon
from PyQtUIkit._core.icons import icons


class KitListWidget(KitWidget):
    def __init__(self,
                 items: Iterable[str] | Iterable[object] | Iterable[dict] | None = None,
                 name_field='name', value_field='value', icon_field='icon',
                 classes: Iterable[str] | str = None, ):
        super().__init__(QListWidget())
        self.__items = items
        self.__name_field = name_field
        self.__value_field = value_field
        self.__icon_field = icon_field

        self.__style = ListStyle()
        self.__final_style = ListStyle()
        if classes:
            self.classes = classes

        self.__animations = True
        self.__anim = None
        self.__scroll_x = 0
        self.__scroll_y = 0
        self.__reloading_id = None

        self.__value_change_events = KitSignals()

        self.qt_widget.currentItemChanged.connect(self.__on_current_item_change)

        self.reload()

    @property
    def qt_widget(self) -> QListWidget:
        return super().qt_widget

    @property
    def style(self) -> ListStyle:
        return self.__style

    @property
    def final_style(self) -> ListStyle:
        return self.__final_style

    @property
    def items(self) -> Iterable[str] | Iterable[object] | Iterable[dict] | None:
        return self.__items

    @items.setter
    def items(self, items: Iterable[str] | Iterable[dict] | Iterable[object] | None) -> None:
        self.__items = items

    @property
    def animations(self) -> bool:
        return self.__animations

    @animations.setter
    def animations(self, animations: bool):
        self.__animations = animations

    @property
    def on_current_change(self):
        return self.__value_change_events

    @property
    def horizontal(self):
        return self.qt_widget.horizontalScrollBar().value()

    @horizontal.setter
    def horizontal(self, horizontal):
        self.scroll_to(horizontal, self.__scroll_y)

    @property
    def vertical(self):
        return self.qt_widget.verticalScrollBar().value()

    @vertical.setter
    def vertical(self, vertical):
        self.scroll_to(self.__scroll_x, vertical)

    @property
    def current_value(self):
        item: _KitListWidgetItem = self.qt_widget.currentItem()
        if item is None:
            return None
        return item.value

    def scroll_to(self, x=0, y=0, animation=None):
        if animation is None:
            animation = self.__animations

        if isinstance(self.__anim, QPropertyAnimation) and not self.__anim.finished:
            self.__anim.stop()
        self.__scroll_x = x
        self.__scroll_y = y
        self._scroll(animation)

    def scroll(self, dx=0, dy=0, animation=True):
        if isinstance(self.__anim, QPropertyAnimation) and not self.__anim.finished:
            self.__anim.stop()
        else:
            self.__scroll_x = self.qt_widget.horizontalScrollBar().value()
            self.__scroll_y = self.qt_widget.verticalScrollBar().value()
        self.__scroll_x += dx
        self.__scroll_y += dy
        self._scroll(animation)

    def _scroll(self, animation=False):
        if animation:
            self.__anim = QParallelAnimationGroup()

            anim = QPropertyAnimation(self.qt_widget.horizontalScrollBar(), b'value')
            anim.setEndValue(self.__scroll_x)
            self.__anim.addAnimation(anim)

            anim = QPropertyAnimation(self.qt_widget.verticalScrollBar(), b'value')
            anim.setEndValue(self.__scroll_y)
            self.__anim.addAnimation(anim)

            self.__anim.start()
        else:
            self.qt_widget.horizontalScrollBar().setValue(self.__scroll_x)
            self.qt_widget.verticalScrollBar().setValue(self.__scroll_y)

    def _add(self, item: '_KitListWidgetItem'):
        self.qt_widget.addItem(item)
        return item

    def _insert(self, index: int, item: '_KitListWidgetItem'):
        self.qt_widget.insertItem(index, item)
        return item

    def _pop(self, index: int):
        return self.qt_widget.takeItem(index)

    def _parse(self, item) -> '_KitListWidgetItem':
        if isinstance(item, str):
            return _KitListWidgetItem(item)
        if isinstance(item, dict):
            return _KitListWidgetItem(item.get(self.__name_field),
                                      item.get(self.__value_field, item.get(self.__name_field)),
                                      item.get(self.__icon_field, None))
        return _KitListWidgetItem(getattr(item, self.__name_field),
                                  getattr(item, self.__value_field, getattr(item, self.__name_field)),
                                  getattr(item, self.__icon_field, None))

    def clear(self):
        self.qt_widget.clear()

    def add(self, item):
        if not isinstance(item, _KitListWidgetItem):
            item = self._parse(item)
        return self._add(item)

    def insert(self, index, item):
        if not isinstance(item, _KitListWidgetItem):
            item = self._parse(item)
        return self._insert(index, item)

    def reload(self):
        self.clear()
        if self.items is None:
            return
        for item in self.__items:
            self.add(item)

    async def reload_async(self):
        self.__reloading_id = reloading_id = uuid4()
        self.clear()
        if self.items is None:
            return
        for i, item in enumerate(self.__items):
            self.add(item)
            if i % 10 == 0:
                await asyncio.sleep(0.1)
            if reloading_id != self.__reloading_id:
                return False
        return True

    def __on_current_item_change(self, item):
        if item is None:
            self.__value_change_events(None)
        else:
            self.__value_change_events(item.value)

    def apply_lang(self):
        for i in range(self.qt_widget.count()):
            self.qt_widget.item(i).apply_lang()

    def _apply_style(self):
        super()._apply_style()
        for i in range(self.qt_widget.count()):
            self.qt_widget.item(i).apply_style()

        if 'no-animation' in self.classes:
            self.__anim = False
        elif 'animation' in self.classes:
            self.__anim = True

        style = self.final_style
        print(style.item.color.name())
        self.qt_widget.setStyleSheet(f"""
QListWidget {{
    color: rgba{style.color.getRgb()};
    background-color: rgba{style.background.getRgb()};
    border: {style.border.width}px {style.border.type} rgba{style.border.color.getRgb()};
    border-top-left-radius: {style.radius.top_left};
    border-top-right-radius: {style.radius.top_right};
    border-bottom-left-radius: {style.radius.bottom_left};
    border-bottom-right-radius: {style.radius.bottom_right};
}}
QListWidget::item {{
    color: rgba{style.item.color.getRgb()};
    background-color: rgba{style.item.background.getRgb()};
    border-top-left-radius: {style.item.radius.top_left};
    border-top-right-radius: {style.item.radius.top_right};
    border-bottom-left-radius: {style.item.radius.bottom_left};
    border-bottom-right-radius: {style.item.radius.bottom_right};
    min-height: 24px;
}}
QListWidget::item:hover {{
    color: rgba{style.item.hover.color.getRgb()};
    background-color: rgba{style.item.hover.background.getRgb()};
    border-top-left-radius: {style.item.radius.top_left};
    border-top-right-radius: {style.item.radius.top_right};
    border-bottom-left-radius: {style.item.radius.bottom_left};
    border-bottom-right-radius: {style.item.radius.bottom_right};
}}
QListWidget::item:selected {{
    color: rgba{style.item.pressed.color.getRgb()};
    background-color: rgba{style.item.pressed.background.getRgb()};
    border-top-left-radius: {style.item.radius.top_left};
    border-top-right-radius: {style.item.radius.top_right};
    border-bottom-left-radius: {style.item.radius.bottom_left};
    border-bottom-right-radius: {style.item.radius.bottom_right};
}}
QListWidget QScrollBar:vertical {{
    background: rgba{style.background.getRgb()};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    width: 12px;
    margin: 0px;
}}
QListWidget QScrollBar:horizontal {{
    background: rgba{style.background.getRgb()};
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    height: 12px;
    margin: 0px;
}}
QListWidget QScrollBar::handle::vertical {{
    background-color: rgba{style.border.color.getRgb()};
    margin: 2px 2px 2px 6px;
    border-radius: 2px;
    min-height: 20px;
}}
QListWidget QScrollBar::handle::vertical:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QListWidget QScrollBar::handle::horizontal {{
    background-color: rgba{style.border.color.getRgb()};
    margin: 6px 2px 2px 2px;
    border-radius: 2px;
    min-width: 20px;
}}
QListWidget QScrollBar::handle::horizontal:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QListWidget QScrollBar::sub-page, QScrollBar::add-page {{
    background: none;
}}
QListWidget QScrollBar::sub-line, QScrollBar::add-line {{
    background: none;
    height: 0px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}}
""")


class _KitListWidgetItem(QListWidgetItem):
    def __init__(self, text, value=None, icon=None):
        super().__init__()
        self.__text = text
        self.__value = value or text
        self.__icon = icon
        self.apply_lang()
        self.apply_style()

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value

    @property
    def icon(self) -> KitIcon | None:
        if not self.__icon:
            return None
        if isinstance(self.__icon, str):
            return KitIcon(data=icons[self.__icon])
        if isinstance(self.__icon, KitIcon):
            return self.__icon
        return None

    @icon.setter
    def icon(self, value):
        self.__icon = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def apply_lang(self):
        self.setText(self.text)

    def apply_style(self):
        self.setIcon(QIcon() if not self.icon else self.icon.icon())
