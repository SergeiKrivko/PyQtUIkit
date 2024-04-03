from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy

from PyQtUIkit.core import PaletteProperty, EnumProperty, KitFont, FontProperty, MethodsProperty
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget
from PyQtUIkit.widgets.button import KitIconButton
from core import SignalProperty


class KitCheckBox(QWidget, _KitWidget):
    main_palette = PaletteProperty('main_palette', 'Main')
    font = FontProperty('font')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)

    stateChanged = pyqtSignal(bool)
    stateEdited = pyqtSignal(bool)

    def __init__(self, text=''):
        super().__init__()
        self.__state = False
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self.__button = KitIconButton()
        self.__button.setCheckable(True)
        self.__button.clicked.connect(self._on_clicked)
        self.__button.size = 16
        main_layout.addWidget(self.__button)

        self.__label = QPushButton(text)
        self.__label.clicked.connect(self._on_clicked)
        main_layout.addWidget(self.__label)
        if not text:
            self.__label.hide()

    def _on_clicked(self):
        self.__state = not self.__state
        self.__on_state_changed()
        self.stateEdited.emit(self.__state)

    def __on_state_changed(self):
        self.__button.icon = 'solid-check' if self.__state else ''
        self.__button.setChecked(self.__state)
        self.stateChanged.emit(self.__state)

    def isChecked(self):
        return self.__state

    def setChecked(self, state):
        self.__state = bool(state)
        self.__on_state_changed()

    def setText(self, text):
        self.__label.setText(text)

    def getText(self):
        return self.__label.text()

    def _set_tm(self, tm):
        super()._set_tm(tm)
        self.__button._set_tm(tm)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.__button.main_palette = self.main_palette
        self.__button._apply_theme()
        self.__label.setFont(self.font.get(self.font_size))
        self.__label.setStyleSheet(f"""
        QPushButton {{
            color: {self.main_palette.text};
            background-color: transparent;
            text-align: left;
        }}""")

    state = MethodsProperty(isChecked, setChecked)
    text = MethodsProperty(getText, setText)
    on_state_changed = SignalProperty('on_state_changed', 'stateChanged')
    on_state_edited = SignalProperty('on_state_edited', 'stateEdited')
