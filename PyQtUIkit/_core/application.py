from typing import Type

from PyQt6.QtWidgets import QApplication

from PyQtUIkit._core.q_application import KitQApplication
from PyQtUIkit._core.service import KitService
from PyQtUIkit._core.styles import KitStyleService
from PyQtUIkit._widgets.main_window import KitMainWindow


class KitApplication:
    def __init__(self,
                 name: str,
                 version: str,
                 window: Type[KitMainWindow] | list[Type[KitMainWindow]],
                 url: str | None = None,
                 organization: str | None = None,
                 icons_path: str = 'assets/icons',
                 locale_path: str = 'assets/locale',
                 styles: list[str] = None,
                 ):
        self.__name: str = name
        self.__window: list[Type[KitMainWindow]] = window if isinstance(window, list) else [window]
        self.__icons_path: str = icons_path
        self.__locale_path: str = locale_path
        self.__styles: list[str] = styles if styles is not None else []
        self.__organization: str = organization
        self.__version: str = version
        self.__url: str = url
        self.__app: KitQApplication | None = None
        self.__run()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def window(self) -> list[Type[KitMainWindow]]:
        return self.__window

    @property
    def icons_path(self) -> str:
        return self.__icons_path

    @property
    def styles(self) -> list[str]:
        return self.__styles

    @property
    def locale_path(self) -> str:
        return self.__locale_path

    @property
    def version(self) -> str:
        return self.__version

    @property
    def url(self) -> str:
        return self.__url

    @property
    def organization(self) -> str:
        return self.__organization

    def run(self):
        QApplication.setApplicationName(self.name)
        QApplication.setApplicationVersion(self.version)
        QApplication.setOrganizationName(self.organization)
        QApplication.setOrganizationDomain(self.url)
        self.__app = KitQApplication(self.window)

        style_service: KitStyleService = KitService.inject(KitStyleService)
        for el in self.styles:
            style_service.parse(el)

        self.__app.exec()

    def __run(self):
        self.run()
