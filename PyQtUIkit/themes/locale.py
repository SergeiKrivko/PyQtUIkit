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


class _KitLocalString:
    def __init__(self, key: str):
        self.__key = key

    def __add__(self, other):
        return _KitLocalStringArray(self, other)
    
    def __radd__(self, other):
        return _KitLocalStringArray(other, self)
    
    def get(self, tm):
        return tm.get_text(self.__key)
    
    
class _KitLocalStringArray:
    def __init__(self, *args):
        self.__args = args
        
    def get(self, tm):
        lst = []
        for el in self.__args:
            if isinstance(el, _KitLocalString):
                lst.append(el.get(tm))
            elif callable(el):
                lst.append(el(tm))
            else:
                lst.append(str(el))
        return ''.join(lst)

    def __add__(self, other):
        if isinstance(other, _KitLocalStringArray):
            return _KitLocalStringArray(*self.__args, *other.__args)
        return _KitLocalStringArray(*self.__args, other)
    
    def __radd__(self, other):
        if isinstance(other, _KitLocalStringArray):
            return _KitLocalStringArray(*other.__args, *self.__args)
        return _KitLocalStringArray(other, *self.__args)


class _KitLocalStringClass:
    def __getattr__(self, item):
        return _KitLocalString(item)

    def get(self, item):
        return _KitLocalString(item)


KitLocaleString = _KitLocalStringClass()
