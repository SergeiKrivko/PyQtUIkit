from PyQt6.QtWidgets import QMainWindow, QWidget

from PyQtUIkit.widgets._layout import KitVBoxLayout
from PyQtUIkit.widgets._widget import KitWidget
from core.style_obj import CardStyle
from core.styles import style_service


class KitMainWindow(KitWidget):
    def __init__(self,
                 widget: KitWidget = None):
        super().__init__(QMainWindow())

        self.__central_layout = KitVBoxLayout()
        strange_widget = QWidget()
        strange_widget.setLayout(self.__central_layout.qt_widget)

        self.qt_widget.setCentralWidget(strange_widget)

        self.central_widget = widget

        self.on_show.add(self.apply_style)
        self.on_show.add(self.apply_lang)

        self.__style = CardStyle()

    @property
    def qt_widget(self) -> QMainWindow:
        return super().qt_widget

    @property
    def style(self) -> CardStyle:
        return self.__style

    @property
    def central_widget(self) -> KitWidget:
        return self.__central_widget

    def show(self):
        self.qt_widget.show()

    def hide(self):
        self.qt_widget.hide()

    @central_widget.setter
    def central_widget(self, widget: KitWidget):
        self.__central_widget = widget
        self.__central_layout.clear()
        if widget:
            self.__central_layout.add(self.__central_widget)

    def apply_style(self):
        self.__central_widget.apply_style()
        style: CardStyle = style_service.get_style(self)
        print(style.background.name())
        self.qt_widget.setStyleSheet(f"background: {style.background.name()};")

    def apply_lang(self):
        self.__central_widget.apply_lang()
