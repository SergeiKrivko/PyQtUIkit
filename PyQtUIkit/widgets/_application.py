import sys
from typing import Callable

from PyQt6.QtWidgets import QApplication

from PyQtUIkit.widgets import KitMainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class KitApplication(QApplication):
    def __init__(self, window: Callable[[], KitMainWindow]):
        super().__init__([])
        self._window = window()
        self._window.show()
        sys.excepthook = except_hook


try:
    import qasync
except ImportError:
    class KitAsyncApplication:
        def __init__(self, window):
            raise ImportError("Qasync is not installed. Please use \"pip install qasync\"")
else:
    class KitAsyncApplication(qasync.QApplication):
        def __init__(self, window: Callable[[], KitMainWindow]):
            super().__init__([])
            import asyncio

            self.__event_loop = qasync.QEventLoop(super())
            asyncio.set_event_loop(self.__event_loop)

            self.__app_close_event = asyncio.Event()
            self.aboutToQuit.connect(self.__app_close_event.set)

            self._window = window()
            self._window.show()
            sys.excepthook = except_hook

        def exec(self):
            with self.__event_loop:
                self.__event_loop.run_until_complete(self.__app_close_event.wait())
