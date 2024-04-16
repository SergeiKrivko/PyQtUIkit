import typing

from PyQt6.QtWidgets import QMainWindow, QWidget, QMenuBar

from PyQtUIkit.themes import ThemeManager


class KitMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._tm = ThemeManager(self._apply_theme, self._apply_lang)
        self.__menu_bar = None

    @property
    def theme_manager(self):
        return self._tm

    def _apply_theme(self):
        if not self._tm.active:
            return
        cw = self.centralWidget()
        if hasattr(cw, '_apply_theme'):
            cw._apply_theme()
        if hasattr(self.__menu_bar, '_apply_theme'):
            self.__menu_bar._apply_theme()

    def _apply_lang(self):
        if not self._tm.active:
            return
        cw = self.centralWidget()
        if hasattr(cw, '_apply_lang'):
            cw._apply_lang()
        if hasattr(self.__menu_bar, '_apply_lang'):
            self.__menu_bar._apply_lang()

    def setCentralWidget(self, widget: typing.Optional[QWidget]) -> None:
        super().setCentralWidget(widget)
        if hasattr(widget, '_set_tm'):
            widget._set_tm(self._tm)
            widget.main_palette = 'Bg'
            widget.radius = 0

    def setMenuBar(self, menubar: QMenuBar) -> None:
        self.__menu_bar = menubar
        super().setMenuBar(menubar)
        if hasattr(menubar, '_set_tm'):
            menubar._set_tm(self._tm)

    def show(self) -> None:
        super().show()
        if not self._tm.active:
            self._tm._set_active()
            self._apply_theme()
            self._apply_lang()

    def set_theme(self, theme):
        self._tm.set_theme(theme)
        if self._tm.active:
            self._apply_theme()
