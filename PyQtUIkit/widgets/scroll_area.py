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

    def setWidget(self, w) -> None:
        super().setWidget(w)
        if hasattr(w, '_set_tm'):
            w._set_tm(self._tm)

    def _set_tm(self, tm):
        super()._set_tm(tm)
        widget = self.widget()
        if hasattr(widget, '_set_tm'):
            widget._set_tm(tm)

    def _apply_theme(self):
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
