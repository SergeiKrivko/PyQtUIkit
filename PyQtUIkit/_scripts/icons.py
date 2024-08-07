import sys

from PyQt6.QtWidgets import QApplication
from qasync import asyncSlot

from PyQtUIkit._core.icons import icons
from PyQtUIkit._core.q_application import KitQApplication
from PyQtUIkit.widgets import *


class MainWindow(KitMainWindow):
    def __init__(self):
        super().__init__(
            KitHBoxLayout(
                KitVBoxLayout(
                    KitHLayout(
                        line_edit := KitLineEdit(),
                        spinner := KitSpinner(classes='primary'),
                        checkmark := KitIconWidget('line-checkmark', classes='success'),
                        spacing=5,
                    ),
                    list_widget := KitListWidget(),
                    classes='spacing-small'
                ),
                KitVLayout(
                    icon_widget := KitIconWidget(),
                    KitHGroup(
                        name_label := KitLineEdit(),
                        button_copy := KitButton(icon='solid-copy'),
                    ),
                ),
                classes='padding-medium spacing-medium'
            )
        )
        self.qt_widget.resize(640, 480)

        self.line_edit = line_edit
        self.spinner = spinner
        self.checkmark = checkmark
        self.icon_widget = icon_widget
        self.name_label = name_label
        self.name_label.read_only = True
        self.checkmark.hide()

        self.spinner.size = 26
        self.spinner.style.padding = 2
        self.checkmark.size = 26

        self.list_widget = list_widget
        self.line_edit.on_text_edit.add(self.reload)
        self.list_widget.on_current_change.add(self.__on_select)
        button_copy.on_click.add(self.__copy_icon)

        self.reload()

    @asyncSlot()
    async def reload(self):
        self.checkmark.hide()
        self.spinner.show()

        search = self.line_edit.text
        self.list_widget.items = [{
            'name': el, 'value': el, 'icon': el,
        } for el in (icons if not search else filter(lambda name: search in name, icons))]
        status = await self.list_widget.reload_async()

        if status:
            self.checkmark.show()
            self.spinner.hide()

    def __on_select(self, icon):
        self.icon_widget.icon = icon
        self.icon_widget.apply_style()
        self.name_label.text = icon

    def __copy_icon(self):
        QApplication.clipboard().setText(self.name_label.text)


def main(args=None):
    sys.exit(KitQApplication([MainWindow]).exec())


if __name__ == '__main__':
    main()
