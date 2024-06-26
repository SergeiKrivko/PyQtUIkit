from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QVBoxLayout, QPushButton, QSizePolicy

from PyQtUIkit.core import IntProperty, EnumProperty, KitFont, FontProperty, MethodsProperty, SignalProperty
from PyQtUIkit.widgets._widget import KitGroupItem as _KitGroupItem, KitGroup as _KitGroup


class KitSpinBox(QWidget, _KitGroupItem):
    border = IntProperty('border', 1)
    radius = IntProperty('radius', 4)

    valueChanged = pyqtSignal(object)
    valueEdited = pyqtSignal(object)

    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)

    def __init__(self, func=int):
        super().__init__()
        self._min = 0
        self._max = 100
        self._step = 1
        self._func = func
        self._last_text = '0'
        self._last_pos = 0
        self._value_changed = False
        self.setMaximumHeight(24)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self._line_edit = QLineEdit()
        self._line_edit.setText('0')
        self._line_edit.cursorPositionChanged.connect(self._on_cursor_moved)
        self._line_edit.editingFinished.connect(self._on_editing_finished)
        self._line_edit.textEdited.connect(self._on_text_edited)
        self._line_edit.setFixedHeight(self.height())
        main_layout.addWidget(self._line_edit)

        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(0)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(buttons_layout)

        self._button_up = QPushButton()
        self._button_up.setCursor(Qt.CursorShape.PointingHandCursor)
        # self._button_up.setFixedWidth(20)
        self._button_up.clicked.connect(self._increase)
        self._button_up.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        buttons_layout.addWidget(self._button_up)

        self._button_down = QPushButton()
        self._button_down.setCursor(Qt.CursorShape.PointingHandCursor)
        # self._button_down.setFixedWidth(20)
        self._button_down.clicked.connect(self._decrease)
        self._button_down.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        buttons_layout.addWidget(self._button_down)

    def _on_text_edited(self):
        value = 0 if not self._last_text else self._func(self._last_text)
        self._fix_value()
        if value != self.value:
            self._value_changed = True

    def _fix_value(self):
        text = self._line_edit.text()
        try:
            value = 0 if text in ['', '+', '-'] else self._func(text)
        except ValueError:
            pos = self._last_pos
            self._line_edit.setText(self._last_text)
            self._last_pos = pos
            self._line_edit.setCursorPosition(self._last_pos)
        else:
            if text and value < self._min:
                self._last_text = str(self._min)
                self._line_edit.setText(self._last_text)
            elif text and value > self._max:
                self._last_text = str(self._max)
                self._line_edit.setText(self._last_text)
            else:
                self._last_text = text
            self.valueChanged.emit(value)
            self._last_pos = self._line_edit.cursorPosition()

    def _on_cursor_moved(self):
        self._last_pos = self._line_edit.cursorPosition()

    def _on_editing_finished(self):
        text = self._line_edit.text()
        if not text:
            self._line_edit.setText('0')
            self._on_text_edited()
        if self._value_changed:
            self.valueEdited.emit(self.value)
            self._value_changed = False

    def _decrease(self):
        self.setValue(round(self.value - self._step, 2))
        self.valueEdited.emit(self.value)
        self._value_changed = False

    def _increase(self):
        self.setValue(round(self.value + self._step, 2))
        self.valueEdited.emit(self.value)
        self._value_changed = False

    def setRange(self, minimum, maximum):
        self._min = minimum
        self._max = maximum
        self._fix_value()

    def setMinimum(self, minimum):
        self._min = minimum
        self._fix_value()

    def setMaximum(self, maximum):
        self._max = maximum
        self._fix_value()

    def setValue(self, value):
        self._line_edit.setText(str(value))
        self._fix_value()

    def getValue(self):
        if not self._line_edit.text():
            return 0
        return self._func(self._line_edit.text())

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        orientation, position = self._group()
        self._line_edit.setFixedHeight(self.height())
        self._line_edit.setFont(self.font.get(self.font_size))
        self._line_edit.setStyleSheet(f"""
        QLineEdit {{
            color: {self.main_palette.text};
            background-color: {self.main_palette.main};
            border: {self.border}px solid {self.border_palette.main};
            border-top-left-radius: {self.radius if orientation == _KitGroup.NO_GROUP or position == _KitGroup.FIRST else 0}px;
            border-bottom-left-radius: {self.radius if orientation == _KitGroup.NO_GROUP or
                                                       orientation == _KitGroup.VERTICAL and position == _KitGroup.LAST or
                                                       orientation == _KitGroup.HORIZONTAL and position == _KitGroup.FIRST else 0}px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
        }}
        QLineEdit:hover {{
            border: {self.border}px solid {self.border_palette.hover};
            background-color: {self.main_palette.hover};
        }}
        QLineEdit:focus {{
            border: {self.border}px solid {self.border_palette.selected};
            background-color: {self.main_palette.hover};
        }}""")
        self._button_up.setIcon(self._tm.icon('line-chevron-up', self.main_palette.text))
        self._button_down.setIcon(self._tm.icon('line-chevron-down', self.main_palette.text))
        css = f"""
QPushButton {{
    color: {self.main_palette.text};
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self.border_palette.main};
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px;
}}
QPushButton::hover {{
    background-color: {self.main_palette.hover};
    border: {self.border}px solid {self.border_palette.selected};
}}"""
        radius = self.radius if orientation == _KitGroup.NO_GROUP or \
                                orientation == _KitGroup.VERTICAL and position == _KitGroup.FIRST or \
                                orientation == _KitGroup.HORIZONTAL and position == _KitGroup.LAST else 0
        self._button_up.setStyleSheet(css.replace("top-right-radius: 0px;", f"top-right-radius: {radius}px;"))
        radius = self.radius if orientation == _KitGroup.NO_GROUP or position == _KitGroup.LAST else 0
        self._button_down.setStyleSheet(css.replace("bottom-right-radius: 0px;", f"bottom-right-radius: {radius}px;"))

    value = MethodsProperty(getValue, setValue)
    on_value_changed = SignalProperty('on_value_changed', 'valueChanged')
    on_value_edited = SignalProperty('on_value_edited', 'valueEdited')
