from PyQtUIkit.core.properties import PaletteProperty, IntProperty
from PyQtUIkit.themes import ThemeManager


class _KitWidget:
    main_palette = PaletteProperty('main_palette')
    border_palette = PaletteProperty('border_palette', 'Border')

    def __init__(self):
        self._tm: ThemeManager = None
        self._add_child_func = lambda x: None

    def _set_tm(self, tm: ThemeManager):
        self._tm = tm
        if tm and tm.active:
            self._apply_theme()
            self._apply_lang()

    @property
    def theme_manager(self):
        return self._tm

    def _apply_theme(self):
        pass

    def _apply_lang(self):
        pass


class KitGroup:
    NO_GROUP = 0
    HORIZONTAL = 1
    VERTICAL = 2
    FIRST = 3
    MIDDLE = 4
    LAST = 5

    def __init__(self, orientation):
        self.__orientation = orientation
        self.__items = []

    def add_item(self, item: 'KitGroupItem'):
        self.__items.append(item)
        item._set_group(self)

    def insert_item(self, index, item: 'KitGroupItem'):
        self.__items.insert(index, item)
        item._set_group(self)

    def remove_item(self, index):
        self.__items.pop(index)._set_group(None)

    def clear(self):
        for item in self.__items:
            item._set_group(None)
        self.__items.clear()

    def __iter__(self):
        for el in self.__items:
            yield el

    def orientation(self):
        return self.__orientation

    def index(self, item):
        return self.__items.index(item)

    def count(self):
        return len(self.__items)


class KitGroupItem(_KitWidget):
    radius = IntProperty('radius', 4)
    border = IntProperty('border', 1)

    def __init__(self):
        super().__init__()
        self.__group: KitGroup | None = None

    def _set_group(self, group: KitGroup | None):
        self.__group = group

    def _group(self) -> tuple[int, int]:
        if not self.__group:
            return KitGroup.NO_GROUP, KitGroup.MIDDLE
        index = self.__group.index(self)
        return self.__group.orientation(), \
            KitGroup.FIRST if index == 0 else KitGroup.LAST if index == self.__group.count() - 1 else KitGroup.MIDDLE

    def _border_radius_css(self):
        orientation, position = self._group()
        return f"""border-top-left-radius: {self.radius if orientation == KitGroup.NO_GROUP or 
                                                           position == KitGroup.FIRST else 0}px;
border-top-right-radius: {self.radius if orientation == KitGroup.NO_GROUP or
                                         orientation == KitGroup.VERTICAL and position == KitGroup.FIRST or
                                         orientation == KitGroup.HORIZONTAL and position == KitGroup.LAST else 0}px;
border-bottom-left-radius: {self.radius if orientation == KitGroup.NO_GROUP or
                                           orientation == KitGroup.HORIZONTAL and position == KitGroup.FIRST or
                                           orientation == KitGroup.VERTICAL and position == KitGroup.LAST else 0}px;
border-bottom-right-radius: {self.radius if orientation == KitGroup.NO_GROUP or position == KitGroup.LAST else 0}px;"""
