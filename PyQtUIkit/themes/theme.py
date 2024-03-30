class KitTheme:
    def __init__(self,
                 theme_data: dict,
                 inherit: 'KitTheme' = None,
                 is_dark=False):
        self.is_dark = is_dark
        self._data = theme_data
        self._inherit = inherit

    def get(self, key: str | tuple):
        if isinstance(key, str):
            key = (key,)
        for el in key:
            if el in self._data:
                return self._data[el]
        if not self._inherit:
            raise KeyError(f"Key {key} not found")
        return self._inherit.get(key)

    def __getitem__(self, item):
        return self.get(item)


class KitPalette:
    def __init__(self, main, hover=None, selected=None, text=None, text_only=None):
        self.main = main
        self.hover = hover or main
        self.selected = selected or hover or main
        self.text = text or selected or hover or main
        self.text_only = text_only or text or selected or hover or main

    def __str__(self):
        return f"KitPalette({self.main}, {self.hover}, {self.selected}, {self.text}, {self.text_only})"
