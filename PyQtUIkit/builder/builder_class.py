class _BuilderClass:
    def __init__(self, name, module):
        self.name = name
        self.lines: list[str] = []
        self.properties = dict()
        self.children = []
        self.module = module

    def add_line(self, line):
        self.lines.append(line)

    def parse(self, variables):
        self.properties.clear()
        self.children.clear()
        child = None
        child_indent = None
        for line in self.lines:
            s_line = line.strip()
            if not s_line:
                continue
            indent = len(line) - len(line.lstrip())

            if indent and child is not None:
                if child_indent is None:
                    child_indent = indent
                child.add_line(line[child_indent:])
                continue
            else:
                child = None

            if s_line.endswith(':'):
                name = s_line[:-1].strip()
                if not name.endswith(')'):
                    name += '()'

                child = _BuilderClass(name, self.module)
                child_indent = None
                self.children.append(child)
            elif ':' in s_line:
                index = s_line.index(':')
                self.properties[s_line[:index]] = eval(s_line[index + 1:].strip(), variables)

    def build(self, obj, add_child, vars=None):
        if vars is None:
            vars = {'self': obj, **self.module.imports}
        self.parse(vars)
        for key, item in self.properties.items():
            setattr(obj, key, item)
        for child in self.children:
            print(child.name, eval(child.name, vars))
            child_obj = eval(child.name, vars)
            child_obj._build_from_kui_as_child(child, vars)
            add_child(child_obj)
