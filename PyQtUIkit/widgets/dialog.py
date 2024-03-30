from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

from PyQtUIkit.core.properties import PaletteProperty, BoolProperty, StringProperty, IconProperty
from PyQtUIkit.themes import KitPalette
from PyQtUIkit.widgets import KitIconButton, KitHBoxLayout, KitVBoxLayout, KitButton, KitIconWidget, KitLabel
from PyQtUIkit.widgets._widget import _KitWidget


class KitDialog(QDialog, _KitWidget):
    header_palette = PaletteProperty('header_palette', 'Menu')
    button_close = BoolProperty('button_close', True)
    name = StringProperty('name', '')

    def __init__(self, parent):
        super().__init__()
        self._main_palette = 'Bg'
        self._parent = parent
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        layout = QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(layout)

        self.__top_widget = KitHBoxLayout()
        self.__top_widget.setContentsMargins(10, 2, 2, 2)
        self.__top_widget.setFixedHeight(32)
        layout.addWidget(self.__top_widget)

        self.__label = QLabel()
        self.__label.setFixedHeight(25)
        self.__top_widget.addWidget(self.__label)

        self.__button_close = KitIconButton('solid-xmark')
        self.__button_close.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.__button_close.size = 25
        self.__button_close.border = 0
        self.__button_close.clicked.connect(self.reject)
        self.__top_widget.addWidget(self.__button_close)

        self.__widget = KitVBoxLayout()
        self.__widget.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.__widget)

        self.__moving = False
        self.__last_pos = None

    def setWidget(self, w) -> None:
        self.__widget.addWidget(w)

    def mousePressEvent(self, a0) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.__moving = True
            self.__last_pos = a0.pos()

    def mouseReleaseEvent(self, a0) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.__moving = False
            self.__last_pos = None

    def mouseMoveEvent(self, a0) -> None:
        if self.__moving:
            self.move(self.pos() + a0.pos() - self.__last_pos)

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        self._set_tm(self._parent._tm)

    def _apply_theme(self):
        self.__top_widget.main_palette = self.header_palette
        self.__button_close.main_palette = self.header_palette
        self.__button_close.setHidden(not self.button_close)
        self.__label.setHidden(not self.name)
        self.__top_widget.setHidden(not self.button_close and not self.name)

        self.__label.setText(self.name)
        css = f"""color: {self.main_palette.text};
                  background-color: {self.main_palette.main};
                  border: 1px solid {self._tm['Border'].main};
                  border-radius: 5px;"""
        self.setStyleSheet(css)

        self.__top_widget._set_tm(self._parent._tm)
        self.__widget._set_tm(self._parent._tm)
        super()._apply_theme()

    @staticmethod
    def question(parent, question: str, answers=('No', 'Yes'), default='No'):
        dialog = _KitAskDialog(parent, question, answers, default)
        dialog.exec()
        return dialog.answer

    @staticmethod
    def info(parent, title: str, text: str):
        dialog = _KitMessageBox(parent, title, text, 'solid-circle-info')
        dialog.exec()

    @staticmethod
    def danger(parent, title: str, text: str):
        dialog = _KitMessageBox(parent, title, text, 'solid-circle-exclamation')
        dialog.icon_palette = 'Danger'
        dialog.exec()

    @staticmethod
    def warning(parent, title: str, text: str):
        dialog = _KitMessageBox(parent, title, text, 'solid-triangle-exclamation')
        dialog.icon_palette = 'Warning'
        dialog.exec()

    @staticmethod
    def success(parent, title: str, text: str):
        dialog = _KitMessageBox(parent, title, text, 'solid-circle-check')
        dialog.icon_palette = 'Success'
        dialog.exec()


class _KitAskDialog(KitDialog):
    def __init__(self, parent, question: str, answers=('No', 'Yes'), default=''):
        super().__init__(parent)
        self._answers = answers
        self.button_close = False

        self.setMinimumSize(300, 120)

        main_layout = KitVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setWidget(main_layout)

        layout = KitHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(15)
        main_layout.addWidget(layout)

        self._icon_widget = KitIconWidget()
        self._icon_widget.icon = 'solid-circle-question'
        self._icon_widget.setFixedSize(72, 72)
        layout.addWidget(self._icon_widget)

        self._label = KitLabel(question)
        self._label.setWordWrap(True)
        layout.addWidget(self._label, 100)

        buttons_layout = KitHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(buttons_layout)

        self._buttons = dict()
        self._answer = default

        for el in answers:
            button = KitButton(el)
            button.setMinimumSize(100, 24)
            buttons_layout.addWidget(button)
            button.clicked.connect(lambda f, a=el: self._on_button_clicked(a))
            self._buttons[el] = button

    def _on_button_clicked(self, answer):
        self._answer = answer
        self.accept()

    @property
    def answer(self):
        return self._answer


class _KitMessageBox(KitDialog):
    text = StringProperty('text', '')
    icon = IconProperty('icon')
    icon_palette = PaletteProperty('icon_palette', 'Transparent')

    def __init__(self, parent, title: str, text: str, icon: str):
        super().__init__(parent)
        self._name = title
        self._icon = icon
        self._text = text
        self.button_close = True

        self.setMinimumSize(300, 120)

        main_layout = KitVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setWidget(main_layout)

        layout = KitHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(15)
        main_layout.addWidget(layout)

        self._icon_widget = KitIconWidget()
        self._icon_widget.icon = icon
        self._icon_widget.setFixedSize(72, 72)
        layout.addWidget(self._icon_widget)

        self._label = KitLabel(text)
        self._label.setWordWrap(True)
        layout.addWidget(self._label, 100)

    def _apply_theme(self):
        self._label.setText(self.text)
        self._icon_widget.icon = self._icon
        self._icon_widget.main_palette = self.icon_palette
        super()._apply_theme()
