from PyQt6.QtGui import QPixmap, QImage, QIcon

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

    def get(self, key: str | tuple):
        return self.__current_theme.get(key)

    def __getitem__(self, item):
        return self.__current_theme.get(item)

    def pixmap(self, name, color=None, size=None):
        if not color:
            color = self.get('TextColor')
        icon = SVG(icons[name])
        icon.change_color(color)
        if size:
            icon.resize(*size)
        return QPixmap.fromImage(QImage.fromData(icon.bytes()))

    def icon(self, name, color=None, size=None):
        return QIcon(self.pixmap(name, color, size))
