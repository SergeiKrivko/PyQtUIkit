import sys
from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QSizePolicy

from PyQtUIkit.themes import icons
from PyQtUIkit.widgets import *


class MainWindow(KitMainWindow):
    def __init__(self):
        super().__init__()
        self.set_theme('Dark')
        self.resize(640, 480)
        self.__searcher = None

        main_layout = KitHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setCentralWidget(main_layout)

        right_layout = KitVBoxLayout()
        right_layout.setMaximumWidth(300)
        right_layout.setSpacing(10)
        main_layout.addWidget(right_layout, 1)

        top_layout = KitHBoxLayout()
        top_layout.setSpacing(10)
        top_layout.setFixedHeight(24)
        right_layout.addWidget(top_layout)

        self.line_edit = KitLineEdit()
        self.line_edit.setFixedHeight(24)
        self.line_edit.textEdited.connect(self.update_icons)
        top_layout.addWidget(self.line_edit)

        self._spinner = KitSpinner()
        self._spinner.size = 18
        self._spinner.width = 3
        top_layout.addWidget(self._spinner)

        self._icon = KitIconWidget('line-checkmark-circle')
        self._icon.setFixedSize(20, 20)
        top_layout.addWidget(self._icon)

        self.list_widget = KitListWidget()
        self.list_widget.currentItemChanged.connect(self.select_icon)
        right_layout.addWidget(self.list_widget)
        self.update_icons()

        right_layout = KitVBoxLayout()
        main_layout.addWidget(right_layout)

        self.icon_widget = KitIconWidget()
        right_layout.addWidget(self.icon_widget, 1)

        group = KitHGroup()
        group.height = 24
        group.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        right_layout.addWidget(group)

        self.copy_line = KitLineEdit()
        self.copy_line.setReadOnly(True)
        group.addItem(self.copy_line)

        self.copy_button = KitIconButton('line-copy')
        self.copy_button.size = 24
        self.copy_button.clicked.connect(self.copy_icon_name)
        group.addItem(self.copy_button)

    def select_icon(self):
        item = self.list_widget.currentItem()
        if item:
            self.icon_widget.icon = item.text()
            self.copy_line.setText(item.text())
        else:
            self.icon_widget.icon = ''
            self.copy_line.setText("")

    def copy_icon_name(self):
        if self.copy_line.text:
            QApplication.clipboard().setText(self.copy_line.text)

    def _add_icon(self, key):
        item = KitListWidgetItem(key, key)
        self.list_widget.addItem(item)

    def update_icons(self):
        self.list_widget.clear()
        if isinstance(self.__searcher, QThread):
            self.__searcher.terminate()
        search = self.line_edit.text
        self.__searcher = Searcher(search, icons.keys())
        self.__searcher.find.connect(self._add_icon)
        self.__searcher.finished.connect(self._on_search_finished)

        self._spinner.resume()
        self._spinner.show()
        self._icon.hide()

        self.__searcher.start()

    def _on_search_finished(self):
        self._spinner.pause()
        self._spinner.hide()
        self._icon.show()


class Searcher(QThread):
    find = pyqtSignal(str)

    def __init__(self, key, data):
        super().__init__()
        self._key = key
        self._data = data

    def run(self):
        for key in self._data:
            if not self._key or self._key in key:
                self.find.emit(key)
                sleep(0.01)


def main():
    sys.exit(KitApplication(MainWindow).exec())


if __name__ == '__main__':
    main()
