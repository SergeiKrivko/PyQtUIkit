import typing

from PyQt6.QtWidgets import QMainWindow, QWidget

from PyQtUIkit.themes import ThemeManager


class KitMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__tm = ThemeManager(self._apply_theme)

    @property
    def theme_manager(self):
        return self.__tm

    def _apply_theme(self):
        cw = self.centralWidget()
        if hasattr(cw, '_apply_theme'):
            cw._apply_theme()

    def setCentralWidget(self, widget: typing.Optional[QWidget]) -> None:
        super().setCentralWidget(widget)
        if hasattr(widget, '_set_tm'):
            widget._set_tm(self.__tm)
            widget.main_palette = 'Bg'
            widget.radius = 0

    def show(self) -> None:
        super().show()
        if not self.__tm.active:
            self.__tm._set_active()
            self._apply_theme()

    def set_theme(self, theme):
        self.__tm.set_theme(theme)
        if self.__tm.active:
            self._apply_theme()
