import os.path
from typing import Any, Type

import bs4

from PyQtUIkit.core.style_obj import BaseStyle
from PyQtUIkit.core.service import KitService


class KitStyle:
    def __init__(self, *args: 'KitStyle'):
        self.__children: tuple[KitStyle, ...] = args

    @property
    def children(self):
        return self.__children

    def __iter__(self):
        return iter(self.__children)


class KitStyleTheme(KitStyle):
    def __init__(self, names: str | list[str], *args):
        super().__init__(*args)
        if isinstance(names, str):
            self.__names = names.split()
        else:
            self.__names = names

    @property
    def names(self):
        return self.__names


class KitStyleClass(KitStyle):
    def __init__(self, names: str | list[str], *args):
        super().__init__(*args)
        if isinstance(names, str):
            self.__names = set(names.split())
        else:
            self.__names = set(names)

    @property
    def names(self):
        return self.__names


class KitStyleType(KitStyle):
    def __init__(self, names: str | list[str], *args):
        super().__init__(*args)
        if isinstance(names, str):
            self.__names = set(names.split())
        else:
            self.__names = set(names)

    @property
    def names(self):
        return self.__names


class KitStyleProperty:
    def __init__(self, name: str, value: str | None = None, variable: str | None = None):
        self.__name = name
        self.__value = value
        self.__variable = variable
        self.__service: StyleService = KitService.inject(StyleService)

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        if self.__variable:
            return self.__service.get(self.__variable, self.__value)
        return self.__value


class StyleService(KitService):
    def __init__(self):
        super().__init__()
        self.__variables = {'': dict()}
        self.__styles = []
        self.__theme: str = 'dark'
        self.parse(r"C:\Users\sergi\PycharmProjects\UIkit\PyQtUIkit\styles\main.xml")

    @property
    def variables(self):
        return self.__variables

    def get(self, name: str, default=None):
        if name in self.__variables[self.__theme]:
            return self.__variables[self.__theme][name]
        return self.__variables[''].get(name, default)

    def parse(self, file_path: str):
        for el in self.__parse_file(file_path):
            self.__styles.append(el)

    def __parse_file(self, file_path: str, theme=''):
        with open(file_path, 'r') as f:
            document = bs4.BeautifulSoup(f.read(), 'xml')

        root = document.find('uikit-style', recursive=False)
        return self.__parse_elem(file_path, root, theme)

    def __parse_elem(self, path, elem: bs4.element.Tag, theme=''):
        for child in elem.findChildren(recursive=False):
            match child.name:
                case 'theme':
                    if theme:
                        raise Exception("Duplicated theme tag")
                    for th in child['name'].split():
                        if th not in self.__variables:
                            self.__variables[th] = dict()
                    yield KitStyleTheme(child['name'], *self.__parse_elem(path, child, child['name']))
                case 'class':
                    yield KitStyleClass(child['name'], *self.__parse_elem(path, child, theme))
                case 'type':
                    yield KitStyleType(child['name'], *self.__parse_elem(path, child, theme))
                case 'property':
                    yield KitStyleProperty(child['name'], child.attrs.get('value'), child.attrs.get('var'))
                case 'var':
                    for th in theme.split() or ['']:
                        self.__variables[th][child['name']] = child['value']
                case 'include':
                    include_path = child['path']
                    if not os.path.isabs(include_path):
                        include_path = os.path.join(os.path.dirname(path), include_path)
                    for el in self.__parse_file(include_path):
                        yield el

    @staticmethod
    def __check_class(obj_class, classes):
        while obj_class != object:
            if obj_class.__name__ in classes:
                return True
            obj_class = obj_class.__base__
        return False

    def __find(self, obj, style: BaseStyle) -> dict[str: Any]:
        def find_in_elem(elem: KitStyle):
            if isinstance(elem, KitStyleProperty):
                style.set(elem.name, elem.value, if_none=False)
            elif isinstance(elem, KitStyleTheme) and self.__theme in elem.names:
                for el in elem.children:
                    find_in_elem(el)
            elif isinstance(elem, KitStyleType) and self.__check_class(obj.__class__, elem.names):
                for el in elem.children:
                    find_in_elem(el)
            elif isinstance(elem, KitStyleClass) and elem.names & obj.classes:
                for el in elem.children:
                    find_in_elem(el)

        for el in self.__styles:
            find_in_elem(el)

    def get_style(self, obj):
        res: BaseStyle = obj.style.__class__()
        self.__find(obj, res)
        res.apply(obj.style)
        return res


style_service = StyleService()
