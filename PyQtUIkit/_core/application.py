import sys
from typing import Type

import qasync

from PyQtUIkit._widgets._main_window import KitMainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class KitApplication(qasync.QApplication):
    def __init__(self, window: Type[KitMainWindow]):
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
