from PyQt6.QtGui import QPixmap, QImage, QIcon

from PyQtUIkit.themes.icons import icons
from PyQtUIkit.themes.svg import SVG
from PyQtUIkit.themes.theme import Theme, Palette

basic_theme = Theme({
    'Transparent': Palette('#00000000', '#00000030', '#00000060', '#222222'),

    'Main': Palette('#FFFFFF', '#DFE1E5', '#CFDEFC', '#222222'),
    'Bg': Palette('#ECF5F9', '#CBCDCF', '#5283C9', '#222222'),
    'Menu': Palette('#F7F8FA', '#DFE1E5', '#3573F0', '#222222'),
    'Border': Palette('#BFC0C2', '#A6A7A8', '#52AFDE', '#222222'),
})


class ThemeManager:
    def __init__(self, on_theme_changed):
        self.__current_theme_name = 'Basic'
        self.__current_theme = basic_theme
        self.__themes = {'Basic': basic_theme}
        self.__on_theme_changed = on_theme_changed
        self.__active = False

        self.add_theme('Dark', Theme({
            'Transparent': Palette('#00000000', '#00000030', '#00000060', '#F0F0F0'),
            'Main': Palette('#2B2D30', '#3E4145', '#2E436E', '#F0F0F0'),
            'Bg': Palette('#141517', '#222345', '#323466', '#F0F0F0'),
            'Menu': Palette('#1F2024', '#4E5157', '#3573F0', '#F0F0F0'),
            'Border': Palette('#474747', '#595959', '#2D63CC', '#F0F0F0'),
        }, basic_theme))

    def add_theme(self, name: str, th: Theme):
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
        self.__active = Theme

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
