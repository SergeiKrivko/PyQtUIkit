from PyQt6.QtCore import QPropertyAnimation, QParallelAnimationGroup
from PyQt6.QtWidgets import QScrollArea

from PyQtUIkit.core.properties import IntProperty, PaletteProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitScrollArea(QScrollArea, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Main')
    border = IntProperty('border', 0)
    radius = IntProperty('radius', 4)

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.__anim = None
        self.__scroll_x = 0
        self.__scroll_y = 0

    def setWidget(self, w) -> None:
        super().setWidget(w)
        if hasattr(w, '_set_tm'):
            w._set_tm(self._tm)

    def scrollTo(self, x=0, y=0, anim=False):
        self.horizontalScrollBar().setValue(x)
        self.verticalScrollBar().setValue(y)

    def scroll(self, dx=0, dy=0, animation=True):
        if isinstance(self.__anim, QPropertyAnimation) and not self.__anim.finished:
            self.__anim.stop()
        else:
            self.__scroll_x = self.horizontalScrollBar().value()
            self.__scroll_y = self.verticalScrollBar().value()
        self.__scroll_x += dx
        self.__scroll_y += dy
        if animation:
            self.__anim = QParallelAnimationGroup()
            if dx:
                anim = QPropertyAnimation(self.horizontalScrollBar(), b'value')
                anim.setEndValue(self.__scroll_x + dx)
                self.__anim.addAnimation(anim)
            if dy:
                anim = QPropertyAnimation(self.verticalScrollBar(), b'value')
                anim.setEndValue(self.__scroll_y + dy)
                self.__anim.addAnimation(anim)
            self.__anim.start()
        else:
            self.horizontalScrollBar().setValue(self.__scroll_x + dx)
            self.verticalScrollBar().setValue(self.__scroll_y + dy)

    def _set_tm(self, tm):
        super()._set_tm(tm)
        widget = self.widget()
        if hasattr(widget, '_set_tm'):
            widget._set_tm(tm)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setStyleSheet(f"""
QScrollArea {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self._tm.get('Border').main};
    border-radius: {self.radius}px;
}}
QScrollArea QScrollBar:vertical {{
    background: {self.main_palette.main};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    width: 12px;
    margin: 0px;
}}
QScrollArea QScrollBar:horizontal {{
    background: {self.main_palette.main};
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    height: 12px;
    margin: 0px;
}}
QScrollArea QScrollBar::handle::vertical {{
    background-color: {self._tm['Border'].main};
    margin: 2px 2px 2px 6px;
    border-radius: 2px;
    min-height: 20px;
}}
QScrollArea QScrollBar::handle::vertical:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QScrollArea QScrollBar::handle::horizontal {{
    background-color: {self._tm['Border'].main};
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
        widget = self.widget()
        if hasattr(widget, '_apply_theme'):
            widget._apply_theme()
