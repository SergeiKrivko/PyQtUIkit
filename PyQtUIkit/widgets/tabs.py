from PyQt6.QtWidgets import QWidget

from PyQtUIkit.widgets import KitHBoxLayout


class TabLayout(KitHBoxLayout):
    def __init__(self):
        super().__init__()
        self.__current = None

    def addWidget(self, widget: QWidget, *args):
        super().addWidget(widget)
