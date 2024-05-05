import importlib
import os.path
from importlib.resources import files

from PyQt6.QtCore import QLocale
from PyQt6.QtGui import QPixmap, QImage, QIcon, QFontDatabase

from PyQtUIkit.themes.builtin_themes import basic_theme, builtin_themes
from PyQtUIkit.themes.icons import icons
from PyQtUIkit.themes.svg import SVG
from PyQtUIkit.themes.theme import KitTheme, KitPalette


class ThemeManager:
    def __init__(self, on_theme_changed, on_lang_changed):
        self.__current_theme_name = 'Light'
        self.__current_theme = basic_theme
        self.__themes = builtin_themes
        self.__on_theme_changed = on_theme_changed
        self.__on_lang_changed = on_lang_changed
        self.__active = False

        self.__lang = None
        self.__lang_data = None
        self.__lang_path = None

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

    def code_color(self, key: str):
        return self.__current_theme.code_color(key)

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

    @staticmethod
    def add_icons(path: str, prefix=None):
        if prefix is None:
            prefix = os.path.basename(path)
        for file in files(path).iterdir():
            if file.name.endswith('.svg'):
                icons[f'{prefix}-{file.name[:-4]}'] = file.read_text()

    @staticmethod
    def add_icon(icon: str, name: str):
        """
        Add icon (from .svg file or from data)
        :param icon: path to file or data
        :param name: icon name, str
        :return:
        """
        if icon.endswith('.svg'):
            with open(icon, encoding='utf-8') as f:
                icon = f.read()
        icons[name] = icon

    def set_locales_path(self, path):
        self.__lang_path = path

    def get_languages(self):
        for file in files(self.__lang_path).iterdir():
            try:
                locale = importlib.import_module(self.__lang_path + '.' + file.name[:-3]).locale
                yield locale.lang, locale.name
            except ModuleNotFoundError:
                pass
            except AttributeError:
                pass
            except ImportError:
                pass

    def set_locale(self, lang=None, default=None):
        if lang is None:
            lang = QLocale.languageToCode(QLocale.system().language())
        if default is None:
            default = QLocale.languageToCode(QLocale.system().language())

        self.__lang = lang
        try:
            self.__lang_data = importlib.import_module(f'{self.__lang_path}.{lang}').locale
        except ImportError:
            try:
                self.__lang_data = importlib.import_module(f'{self.__lang_path}.{default}').locale
            except ImportError:
                for el, _ in self.get_languages():
                    self.__lang_data = importlib.import_module(f'{self.__lang_path}.{el}').locale
                    break
                else:
                    raise ModuleNotFoundError("no locales found")
        self.__on_lang_changed()

    def get_text(self, key):
        return self.__lang_data.get(key)

    @property
    def locale(self):
        return self.__lang
