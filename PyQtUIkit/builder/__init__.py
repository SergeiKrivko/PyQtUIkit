import os.path
from typing import Callable, Any

from PyQtUIkit.builder.builder_class import _BuilderClass
from PyQtUIkit.builder.builder_module import _BuilderModule


class Builder:
    def __init__(self):
        import __main__
        self._main_path = os.path.dirname(__main__.__file__)
        self._modules = dict()
        self._ext = '.kui'

    def build(self, _class, obj, add_child: Callable = lambda x: None, vars=None):
        _class.build(obj, add_child, vars)

    def build_from_file(self, obj, add_child: Callable = lambda x: None):
        filename = os.path.join(self._main_path, obj.__class__.__module__.replace('.', os.path.sep) + self._ext)
        if not os.path.isfile(filename):
            return
        if filename in self._modules:
            module = self._modules.get(filename)
        else:
            module = _BuilderModule(obj.__class__.__module__, filename)
            self._modules[filename] = module
        _class = module.get_class(obj.__class__.__name__)
        if _class:
            _class.build(obj, add_child)


BUILDER = Builder()
