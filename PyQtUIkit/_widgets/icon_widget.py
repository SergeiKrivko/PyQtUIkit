from typing import Iterable

from PyQtUIkit._core.icon import KitIcon
from PyQtUIkit._impl.icon_widget import IconWidget
from PyQtUIkit._widgets.widget import KitWidget
from PyQtUIkit._core.style_obj import CardStyle


class KitIconWidget(KitWidget):
    def __init__(self,
                 icon: KitIcon | str = None,
                 classes: Iterable[str] | str = None,):
        super().__init__(IconWidget(icon))
        self.__style = CardStyle()
        self.__final_style = CardStyle()
        if classes:
            self.classes = classes

    @property
    def qt_widget(self) -> IconWidget:
        return super().qt_widget

    @property
    def style(self) -> CardStyle:
        return self.__style

    @property
    def final_style(self) -> CardStyle:
        return self.__final_style

    @property
    def icon(self):
        return self.qt_widget.icon

    @icon.setter
    def icon(self, icon: KitIcon):
        self.qt_widget.icon = icon

    def _apply_style(self):
        super()._apply_style()
        style = self.final_style
        self.qt_widget.setStyleSheet(f"""
        QIconWidget {{
            background-color: transparent;
            border: none;
        }}""")
        self.qt_widget.color = style.color
        self.qt_widget.update()
