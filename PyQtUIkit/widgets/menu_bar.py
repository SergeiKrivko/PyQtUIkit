from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QLabel, QMenuBar, QMenu

from PyQtUIkit.core import IntProperty, PaletteProperty, EnumProperty, KitFont, FontProperty, MethodsProperty
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitMenuBar(QMenuBar, _KitWidget):
    class Action(QAction):
        def __init__(self, name, icon, func=None, shortcut=None):
            super().__init__()
            self.setText(name)
            if shortcut:
                self.setShortcut(shortcut)
            self._icon = icon
            self._func = func
            if self._func:
                self.triggered.connect(self._func)

        def _apply_styles(self, tm, main_palette, border_palette):
            if self._icon:
                self.setIcon(tm.icon(self._icon, main_palette.text))

    class Menu(QMenu):
        def __init__(self, name, icon, *args):
            super().__init__()
            self.setTitle(name)
            self._icon = icon
            self.setMinimumWidth(160)
            self._children = []
            for el in args:
                if isinstance(el, QMenu):
                    self.addMenu(el)
                elif isinstance(el, QAction):
                    self.addAction(el)

        def addAction(self, action: QAction, *args):
            super().addAction(action)
            self._children.append(action)

        def addMenu(self, menu: QMenu):
            super().addMenu(menu)
            self._children.append(menu)

        def clear(self) -> None:
            self._children.clear()

        def _apply_styles(self, tm, main_palette, border_palette):
            if self._icon:
                self.setIcon(tm.icon(self._icon, main_palette.text))
            self.setStyleSheet(f"""
QMenu {{
    color: {main_palette.text};
    background-color: {main_palette.main};
    border: 1px solid {border_palette.main};
    border-radius: 6px;
    spacing: 4px;
    padding: 3px;
}}
QMenu::item {{
    border: 0px solid {border_palette.main};
    background-color: transparent;
    border-radius: 8px;
    padding: 4px 20px 4px 6px;
}}
QMenu::icon {{
    padding-left: 10px;
}}
QMenu::item:selected {{
    background-color: {main_palette.hover};
}}
QMenu::separator {{
    height: 1px;
    background: {border_palette.main};
    margin: 4px 10px;
}}""")
            for el in self._children:
                if hasattr(el, '_apply_styles'):
                    el._apply_styles(tm, main_palette, border_palette)

    main_palette = PaletteProperty('main_palette', 'Menu')
    border = IntProperty('border', 0)
    radius = IntProperty('radius', 4)
    spacing = IntProperty('spacing', 3)
    padding = IntProperty('padding', 4)
    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)

    def __init__(self, *args):
        super().__init__()
        self._children = []
        for el in args:
            if isinstance(el, QMenu):
                self.addMenu(el)
            elif isinstance(el, QAction):
                self.addAction(el)

    def addAction(self, action: QAction, *args):
        super().addAction(action)
        self._children.append(action)

    def addMenu(self, menu: QMenu):
        super().addMenu(menu)
        self._children.append(menu)

    def clear(self) -> None:
        self._children.clear()

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setFont(self.font.get(self.font_size))
        self.setStyleSheet(f"""
QMenuBar {{
    background-color: {self.main_palette.main};
    spacing: {self.spacing}px;
    padding: {self.padding}px;
}}
QMenuBar::item {{
    color: {self.main_palette.text};
    padding: 3px 6px;
    background: {self.main_palette.main};
    border-radius: {self.radius}px;
}}
QMenuBar::item:selected {{
    background: {self.main_palette.hover};
}}
QMenuBar::item:pressed {{
    background: {self.main_palette.selected};
}}""")
        for el in self._children:
            if hasattr(el, '_apply_styles'):
                el._apply_styles(self._tm, self.main_palette, self.border_palette)
