from PyQtUIkit.core.properties import PaletteProperty
from PyQtUIkit.themes import ThemeManager


class KitWidget:
    main_palette = PaletteProperty('main_palette')

    def __init__(self):
        self._tm: ThemeManager = None

    def _set_tm(self, tm: ThemeManager):
        self._tm = tm
        if tm and tm.active:
            self._apply_theme()

    @property
    def theme_manager(self):
        return self._tm

    def _apply_theme(self):
        pass

