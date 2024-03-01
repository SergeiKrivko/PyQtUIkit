from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QVBoxLayout, QPushButton

from PyQtUIkit._properties import IntProperty, ColorProperty
from PyQtUIkit.widgets._widget import KitWidget as _KitWidget


class KitSpinBox(QWidget, _KitWidget):
    border = IntProperty(1)
    radius = IntProperty(4)
    text_color = ColorProperty('TextColor')

    def __init__(self, func=int):
        super().__init__()
        self._min = 0
        self._max = 100
        self._step = 1
        self._func = func
        self._last_text = '0'
        self.setMaximumHeight(24)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self._line_edit = QLineEdit()
        self._line_edit.setText('0')
        self._line_edit.editingFinished.connect(self._on_editing_finished)
        self._line_edit.textEdited.connect(self._on_text_edited)
        self._line_edit.setFixedHeight(self.height())
        main_layout.addWidget(self._line_edit)

        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(0)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(buttons_layout)

        self._button_up = QPushButton()
        self._button_up.setFixedWidth(20)
        self._button_up.clicked.connect(self._increase)
        buttons_layout.addWidget(self._button_up)

        self._button_down = QPushButton()
        self._button_down.setFixedWidth(20)
        self._button_down.clicked.connect(self._decrease)
        buttons_layout.addWidget(self._button_down)

    def _on_text_edited(self):
        text = self._line_edit.text()
        try:
            value = 0 if text in ['', '+', '-'] else self._func(text)
        except ValueError:
            self._line_edit.setText(self._last_text)
        else:
            if value < self._min:
                self._last_text = str(self._min)
                self._line_edit.setText(self._last_text)
            elif value > self._max:
                self._last_text = str(self._max)
                self._line_edit.setText(self._last_text)
            else:
                self._last_text = text

    def _on_editing_finished(self):
        text = self._line_edit.text()
        if not text:
            self._line_edit.setText('0')
            self._on_text_edited()

    def _decrease(self):
        self.setValue(round(self.value() - self._step, 2))
        # self._line_edit.selectAll()
        # self._line_edit.setFocus()

    def _increase(self):
        self.setValue(round(self.value() + self._step, 2))
        # self._line_edit.selectAll()
        # self._line_edit.setFocus()

    def setRange(self, minimum, maximum):
        self._min = minimum
        self._max = maximum
        self._on_text_edited()

    def setMinimum(self, minimum):
        self._min = minimum
        self._on_text_edited()

    def setMaximum(self, maximum):
        self._max = maximum
        self._on_text_edited()

    def setValue(self, value):
        self._line_edit.setText(str(value))
        self._on_text_edited()

    def value(self):
        if not self._line_edit.text():
            return 0
        return self._func(self._line_edit.text())

    def _apply_theme(self):
        self._line_edit.setStyleSheet(f"""
        QLineEdit {{
            color: {self._tm.get('TextColor')};
            background-color: {self.main_palette.main};
            border: {self.border}px solid {self._tm.get('Border').main};
            border-top-left-radius: {self.radius}px;
            border-bottom-left-radius: {self.radius}px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
        }}
        QLineEdit:hover {{
            border: {self.border}px solid {self._tm.get('Border').hover};
            background-color: {self.main_palette.hover};
        }}
        QLineEdit:focus {{
            border: {self.border}px solid {self._tm.get('Border').selected};
            background-color: {self.main_palette.hover};
        }}""")
        self._button_up.setIcon(self._tm.icon('chevron-up'))
        self._button_down.setIcon(self._tm.icon('chevron-down'))
        css = f"""
QPushButton {{
    color: {self.text_color};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self._tm['Border'].main};
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px;
}}
QPushButton::hover {{
    background-color: {self.main_palette.hover};
    border: {self.border}px solid {self._tm['Border'].selected};
}}"""
        self._button_up.setStyleSheet(css.replace("top-right-radius: 0px;", f"top-right-radius: {self.radius}px;"))
        self._button_down.setStyleSheet(css.replace("bottom-right-radius: 0px;", f"bottom-right-radius: {self.radius}px;"))
