from PyQt6.QtWidgets import QWidget

from PyQtUIkit.widgets import KitHBoxLayout, KitTabBar, KitNavigation, KitHRadio, KitVRadio


class KitTabLayout(KitHBoxLayout):
    def __init__(self):
        super().__init__()
        self.__current = None
        self.__connected_widget = None
        self.setContentsMargins(0, 0, 0, 0)

    def insertWidget(self, index: int, widget: QWidget, *args):
        super().insertWidget(index, widget)
        if self.__current is None:
            self.__current = index
        else:
            widget.hide()

    def addWidget(self, widget: QWidget, *args):
        self.insertWidget(len(self.__widgets), widget)

    def setCurrent(self, index):
        if self.__current is not None and self.__current < len(self.__widgets):
            self.__widgets[self.__current].hide()
        self.__current = index
        self.__widgets[self.__current].show()

    def connect(self, widget: KitTabBar | KitNavigation | KitVRadio | KitHRadio):
        if self.__connected_widget is not None:
            raise Exception("can connect only one widget")
        self.__connected_widget = widget
        widget.currentChanged.connect(self.setCurrent)
        if widget.currentIndex():
            self.setCurrent(widget.currentIndex())
