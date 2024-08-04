from typing import Callable, Any


class KitSignals:
    def __init__(self):
        self.__handlers = []

    def add(self, handler: Callable[[Any], Any] | Callable[[], Any]):
        self.__handlers.append(handler)
        return self

    def remove(self, handler: Callable[[Any], Any] | Callable[[], Any]):
        self.__handlers.remove(handler)
        return self

    def clear(self):
        self.__handlers.clear()
        return self

    def __iadd__(self, handler: Callable[[Any], Any] | Callable[[], Any]):
        return self.add(handler)

    def __add__(self, handler: Callable[[Any], Any] | Callable[[], Any]):
        return self.add(handler)

    def __isub__(self, handler: Callable[[Any], Any] | Callable[[], Any]):
        return self.remove(handler)

    def __sub__(self, handler: Callable[[Any], Any] | Callable[[], Any]):
        return self.remove(handler)

    @property
    def count(self):
        return len(self.__handlers)

    def call(self, event: Any = None):
        for handler in self.__handlers:
            try:
                handler(event)
            except TypeError as e:
                if 'too many arguments' not in str(e) and 'positional argument' not in str(e):
                    raise e
                handler()

    def __call__(self, event: Any = None):
        self.call(event)
