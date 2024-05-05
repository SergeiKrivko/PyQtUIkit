from PyQt6.QtGui import QColor

from PyQtUIkit.core.font import KitFont


class KitPalette:
    def __init__(self, main, hover=None, selected=None, text=None, text_only=None):
        self.main = main
        self.hover = hover or main
        self.selected = selected or hover or main
        self.text = text or selected or hover or main
        self.text_only = text_only or text or selected or hover or main

    def __str__(self):
        return f"KitPalette({self.main}, {self.hover}, {self.selected}, {self.text}, {self.text_only})"


class KitTheme:
    def __init__(self,
                 palettes: dict[str: KitPalette] = None,
                 fonts: dict[str: KitFont] = None,
                 code_colors: dict[str, QColor] = None,
                 inherit: 'KitTheme' = None,
                 is_dark=False):
        self.is_dark = is_dark
        self._palettes = palettes
        self._fonts = fonts
        self._code_colors = code_colors
        self._inherit = inherit

    def palette(self, key: str):
        if self._palettes and key in self._palettes:
            return self._palettes[key]
        if not self._inherit:
            raise KeyError(f"Key '{key}' not found")
        return self._inherit.palette(key)

    def code_color(self, key: str):
        if self._code_colors and key in self._code_colors:
            return self._code_colors[key]
        if not self._inherit:
            raise KeyError(f"Key '{key}' not found")
        return self._inherit.code_color(key)

    def font(self, key='default') -> KitFont:
        if self._fonts and key in self._fonts:
            return self._fonts[key]
        if not self._inherit:
            raise KeyError(f"Key '{key}' not found")
        return self._inherit.font(key)
