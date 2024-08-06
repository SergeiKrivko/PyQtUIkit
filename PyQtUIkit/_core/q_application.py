import sys
from typing import Type

import qasync

from PyQtUIkit._widgets.main_window import KitMainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class KitQApplication(qasync.QApplication):
    def __init__(self, windows: list[Type[KitMainWindow]]):
        super().__init__([])
        import asyncio

        self.__event_loop = qasync.QEventLoop(super())
        asyncio.set_event_loop(self.__event_loop)

        self.__app_close_event = asyncio.Event()
        self.aboutToQuit.connect(self.__app_close_event.set)

        self._windows = []
        for window in windows:
            w = window()
            w.show()
            self._windows.append(w)
        sys.excepthook = except_hook

    def exec(self):
        with self.__event_loop:
            self.__event_loop.run_until_complete(self.__app_close_event.wait())
