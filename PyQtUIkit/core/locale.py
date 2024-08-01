


class KitLocale:
    def __init__(self, lang: str, name: str, dct: dict[str: str]):
        self.__lang = lang
        self.__name = name
        self.__dict = dct

    def get(self, item):
        return self.__dict[item]

    def items(self):
        return self.__dict.items()

    @property
    def lang(self):
        return self.__lang

    @property
    def name(self):
        return self.__name


class _KitLocaleString:
    def __init__(self, key: str):
        self.__key = key

    def __add__(self, other):
        return _KitLocaleStringArray(self, other)
    
    def __radd__(self, other):
        return _KitLocaleStringArray(other, self)
    
    def get(self):
        return theme_manager.get_text(self.__key)
    
    
class _KitLocaleStringArray:
    def __init__(self, *args):
        self.__args = args
        
    def get(self):
        lst = []
        for el in self.__args:
            if isinstance(el, _KitLocaleString):
                lst.append(el.get())
            elif callable(el):
                lst.append(el(theme_manager))
            else:
                lst.append(str(el))
        return ''.join(lst)

    def __add__(self, other):
        if isinstance(other, _KitLocaleStringArray):
            return _KitLocaleStringArray(*self.__args, *other.__args)
        return _KitLocaleStringArray(*self.__args, other)
    
    def __radd__(self, other):
        if isinstance(other, _KitLocaleStringArray):
            return _KitLocaleStringArray(*other.__args, *self.__args)
        return _KitLocaleStringArray(other, *self.__args)


class _KitLocalStringClass:
    def __getattr__(self, item):
        return _KitLocaleString(item)

    def get(self, item):
        return _KitLocaleString(item)


KitLocaleString = _KitLocalStringClass()
