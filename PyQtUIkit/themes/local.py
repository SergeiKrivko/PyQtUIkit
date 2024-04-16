class KitLocal:
    def __init__(self, lang: str, name: str, dct: dict[str: str]):
        self.__lang = lang
        self.__name = name
        self.__dict = dct

    def get(self, item):
        return self.__dict[item]

    @property
    def lang(self):
        return self.__lang

    @property
    def name(self):
        return self.__name


class _KitLocalString:
    def __init__(self, key: str):
        self.key = key


class _KitLocalStringClass:
    def __getattr__(self, item):
        return _KitLocalString(item)


KitLocalString = _KitLocalStringClass()
