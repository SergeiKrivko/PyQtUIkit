from PyQt6.QtGui import QPixmap, QImage, QIcon, QFont, QFontDatabase

from PyQtUIkit.core.font import KitFont
from PyQtUIkit.themes.builtin_themes import basic_theme, builtin_themes
from PyQtUIkit.themes.icons import icons
from PyQtUIkit.themes.svg import SVG
from PyQtUIkit.themes.theme import KitTheme, KitPalette


class ThemeManager:
    def __init__(self, on_theme_changed):
        self.__current_theme_name = 'Light'
        self.__current_theme = basic_theme
        self.__themes = builtin_themes
        self.__on_theme_changed = on_theme_changed
        self.__active = False

        from importlib.resources import files
        for file in files('PyQtUIkit.fonts').iterdir():
            QFontDatabase.addApplicationFontFromData(file.read_bytes())

    def add_theme(self, name: str, th: KitTheme):
        self.__themes[name] = th

    def set_theme(self, new_theme):
        self.__current_theme = self.__themes.get(new_theme)
        self.__current_theme_name = new_theme
        self.__on_theme_changed()

    @property
    def current_theme(self):
        return self.__current_theme_name

    @property
    def active(self):
        return self.__active

    def _set_active(self):
        self.__active = KitTheme

    def palette(self, key: str):
        return self.__current_theme.palette(key)

    def font(self, font):
        return self.__current_theme.font(font)

    def border(self):
        return self.__current_theme.border()

    def pixmap(self, name, color, size=None):
        icon = SVG(icons[name])
        icon.change_color(color)
        if size:
            icon.resize(*size)
        return QPixmap.fromImage(QImage.fromData(icon.bytes()))

    def icon(self, name, color=None, size=None):
        return QIcon(self.pixmap(name, color, size))
