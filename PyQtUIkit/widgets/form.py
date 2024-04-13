from PyQt6.QtCore import Qt

from PyQtUIkit.widgets import KitVBoxLayout, KitHBoxLayout, KitLabel, KitLineEdit, KitSpinBox, KitComboBox, KitCheckBox


class KitForm(KitVBoxLayout):
    class Label(KitLabel):
        pass

    class StrField(KitHBoxLayout):
        def __init__(self, name=''):
            super().__init__()
            self.name = name
            self.spacing = 6
            self.alignment = Qt.AlignmentFlag.AlignLeft

            if name:
                self.addWidget(KitLabel(name))

            self._line_edit = KitLineEdit()
            self.addWidget(self._line_edit)

        def value(self):
            return self._line_edit.text

    class IntField(KitHBoxLayout):
        def __init__(self, name='', min=0, max=100):
            super().__init__()
            self.name = name
            self.spacing = 6
            self.alignment = Qt.AlignmentFlag.AlignLeft

            if name:
                self.addWidget(KitLabel(name))

            self._spin_box = KitSpinBox()
            self._spin_box.setMaximumWidth(120)
            self._spin_box.setRange(min, max)
            self.addWidget(self._spin_box)

        def value(self):
            return self._spin_box.value

    class ComboField(KitHBoxLayout):
        def __init__(self, name='', values: list = tuple()):
            super().__init__()
            self.name = name
            self.spacing = 6
            self.alignment = Qt.AlignmentFlag.AlignLeft

            if name:
                self.addWidget(KitLabel(name))

            self._combo_box = KitComboBox(*values)
            self._combo_box.setMaximumWidth(120)
            self.addWidget(self._combo_box)

        def value(self):
            return self._combo_box.currentValue()

    class BoolField(KitCheckBox):
        def __init__(self, name):
            super().__init__(name)

        def value(self):
            return self.state

    def __init__(self, *args):
        super().__init__()
        self.__fields = []
        self.spacing = 6
        for arg in args:
            if not isinstance(arg, KitForm.Label):
                self.__fields.append(arg)
            self.addWidget(arg)

    def res(self):
        return [el.value() for el in self.__fields]
