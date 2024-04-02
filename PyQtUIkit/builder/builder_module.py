from PyQt6.QtCore import Qt

from PyQtUIkit import widgets
from PyQtUIkit.builder import _BuilderClass


class _BuilderModule:
    def __init__(self, module, filename):
        self._filename = filename
        self._file = open(filename)
        self._classes = dict()
        self.imports = {'module': __import__(module), 'Qt': Qt, 'widgets': widgets}
        self.parse_file()

    def parse_file(self):
        res = None
        res_indent = None
        for line in self._file:
            if not line.strip():
                continue
            indent = len(line) - len(line.lstrip())

            if indent and res is not None:
                if res_indent is None:
                    res_indent = indent
                res.add_line(line[res_indent:])
                continue

            if line.startswith('import'):
                module_name = line[6:].strip()
                module = __import__(module_name)
                self.imports[module_name if '.' not in module_name else module_name.split('.')[-1]] = module
            elif line.startswith('class'):
                name = line[5:].strip('\n\t\r :')
                res = _BuilderClass(name, self)
                res_indent = None
                self._classes[name] = res

    def get_class(self, name) -> _BuilderClass:
        return self._classes.get(name)
