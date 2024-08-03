from typing import Iterable

from PyQt6.QtCore import QPropertyAnimation, QParallelAnimationGroup
from PyQt6.QtWidgets import QScrollArea

from _core.style_obj import CardStyle
from _widgets.widget import KitWidget


class KitScrollArea(KitWidget):
    def __init__(self,
                 widget: KitWidget = None,
                 classes: Iterable[str] | str = None, ):
        super().__init__(QScrollArea())
        self.__widget = widget
        if widget:
            self.qt_widget.setWidget(widget.qt_widget)
        self.qt_widget.setWidgetResizable(True)

        self.__style = CardStyle()
        self.__final_style = CardStyle()
        if classes:
            self.classes = classes

        self.__animations = True
        self.__anim = None
        self.__scroll_x = 0
        self.__scroll_y = 0

    @property
    def qt_widget(self) -> QScrollArea:
        return super().qt_widget

    @property
    def style(self) -> CardStyle:
        return self.__style

    @property
    def final_style(self) -> CardStyle:
        return self.__final_style

    @property
    def widget(self) -> KitWidget:
        return self.__widget

    @widget.setter
    def widget(self, widget: KitWidget):
        self.__widget = widget
        self.qt_widget.setWidget(widget.qt_widget)

    @property
    def animations(self) -> bool:
        return self.__animations

    @animations.setter
    def animations(self, animations: bool):
        self.__animations = animations

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

    def apply_lang(self):
        self.__widget.apply_lang()

    def apply_style(self):
        super().apply_style()

        if 'no-animation' in self.classes:
            self.__anim = False
        elif 'animation' in self.classes:
            self.__anim = True

        style = self.final_style
        self.qt_widget.setStyleSheet(f"""
QScrollArea {{
    color: rgba{style.color.getRgb()};
    background-color: rgba{style.background.getRgb()};
    border: {style.border.width}px {style.border.type} rgba{style.border.color.getRgb()};
    border-top-left-radius: {style.radius.top_left};
    border-top-right-radius: {style.radius.top_right};
    border-bottom-left-radius: {style.radius.bottom_left};
    border-bottom-right-radius: {style.radius.bottom_right};
}}
QScrollArea QScrollBar:vertical {{
    background: rgba{style.background.getRgb()};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    width: 12px;
    margin: 0px;
}}
QScrollArea QScrollBar:horizontal {{
    background: rgba{style.background.getRgb()};
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    height: 12px;
    margin: 0px;
}}
QScrollArea QScrollBar::handle::vertical {{
    background-color: rgba{style.border.color.getRgb()};
    margin: 2px 2px 2px 6px;
    border-radius: 2px;
    min-height: 20px;
}}
QScrollArea QScrollBar::handle::vertical:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QScrollArea QScrollBar::handle::horizontal {{
    background-color: rgba{style.border.color.getRgb()};
    margin: 6px 2px 2px 2px;
    border-radius: 2px;
    min-width: 20px;
}}
QScrollArea QScrollBar::handle::horizontal:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QScrollArea QScrollBar::sub-page, QScrollBar::add-page {{
    background: none;
}}
QScrollArea QScrollBar::sub-line, QScrollBar::add-line {{
    background: none;
    height: 0px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}}
""")
        if self.__widget:
            self.__widget.apply_style()
