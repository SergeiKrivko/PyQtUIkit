class Theme:
    def __init__(self, theme_data: dict, inherit: 'Theme' = None):
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


class Palette:
    def __init__(self, main, hover=None, selected=None):
        self.main = main
        self.hover = hover or main
        self.selected = selected or hover or main
