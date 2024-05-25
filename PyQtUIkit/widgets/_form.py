from typing import Callable

from PyQt6.QtCore import Qt, pyqtSignal

from PyQtUIkit.widgets import KitVBoxLayout, KitHBoxLayout, KitLabel, KitLineEdit, KitSpinBox, KitComboBox, \
    KitCheckBox, KitButton


class KitForm(KitVBoxLayout):
    class Label(KitLabel):
        pass

    class StrField(KitHBoxLayout):
        def __init__(self, name='', default=''):
            super().__init__()
            self.name = name
            self.spacing = 6
            self.alignment = Qt.AlignmentFlag.AlignLeft

            if name:
                self.addWidget(KitLabel(name))

            self._line_edit = KitLineEdit()
            self._line_edit.text = default
            self.addWidget(self._line_edit)

        def value(self):
            return self._line_edit.text

        def has_focus(self):
            return self._line_edit.hasFocus()

    class IntField(KitHBoxLayout):
        def __init__(self, name='', min=0, max=100, default=0):
            super().__init__()
            self.name = name
            self.spacing = 6
            self.alignment = Qt.AlignmentFlag.AlignLeft

            if name:
                self.addWidget(KitLabel(name))

            self._spin_box = KitSpinBox()
            self._spin_box.value = default
            self._spin_box.setMaximumWidth(120)
            self._spin_box.setRange(min, max)
            self.addWidget(self._spin_box)

        def value(self):
            return self._spin_box.value

        def has_focus(self):
            return self._spin_box.hasFocus()

    class ComboField(KitHBoxLayout):
        def __init__(self, name='', values: list = tuple(), default=0):
            super().__init__()
            self.name = name
            self.spacing = 6
            self.alignment = Qt.AlignmentFlag.AlignLeft

            if name:
                self.addWidget(KitLabel(name))

            self._combo_box = KitComboBox(*values)
            self._combo_box.setMaximumWidth(120)
            self._combo_box.setCurrentIndex(default)
            self.addWidget(self._combo_box)

        def value(self):
            return self._combo_box.currentValue()

        def has_focus(self):
            return self._combo_box.hasFocus()

    class BoolField(KitCheckBox):
        def __init__(self, name, default=False):
            super().__init__(name)
            self.state = default

        def value(self):
            return self.state

        def has_focus(self):
            return self.hasFocus()

    class Button(KitButton):
        def __init__(self, name, icon='', on_click: Callable = None):
            super().__init__(name, icon)
            if on_click:
                self.clicked.connect(on_click)

        def has_focus(self):
            return self.hasFocus()

    returnPressed = pyqtSignal()

    def __init__(self, *args):
        super().__init__()
        self.__fields = []
        self.spacing = 6
        for arg in args:
            if not isinstance(arg, KitForm.Label):
                self.__fields.append(arg)
            self.addWidget(arg)

    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key.Key_Return:
            self.returnPressed.emit()
        else:
            super().keyPressEvent(a0)

    @property
    def fields(self):
        return self.__fields

    def has_focus(self):
        for el in self.__fields:
            if el.has_focus():
                return True
        return False

    def res(self):
        return [el.value() for el in self.__fields]

    def value(self):
        return self.res()
