import sys
from typing import Callable

from PyQt6.QtWidgets import QApplication

from PyQtUIkit.widgets import KitMainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class KitApplication(QApplication):
    def __init__(self, window: Callable[[], KitMainWindow]):
        print(0)
        super().__init__([])
        print(1)
        self._window = window()
        self._window.show()
        sys.excepthook = except_hook
        print(2)


try:
    import qasync
except ImportError:
    class KitAsyncApplication:
        def __init__(self):
            raise ImportError("Qasync is not installed. Please use \"pip install qasync\"")
else:
    class KitAsyncApplication(qasync.QApplication):
        def __init__(self, window: Callable[[], KitMainWindow]):
            super().__init__([])
            import asyncio

            event_loop = qasync.QEventLoop(self)
            asyncio.set_event_loop(event_loop)

            app_close_event = asyncio.Event()
            self.aboutToQuit.connect(app_close_event.set)

            self._window = window()
            self._window.show()
            sys.excepthook = except_hook

            with event_loop:
                event_loop.run_until_complete(app_close_event.wait())
