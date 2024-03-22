from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStyle, QLayout
from PyQt6.QtCore import Qt, QRect, QSize, QPoint
from PyQt6.QtWidgets import QSizePolicy

from PyQtUIkit.core.properties import IntProperty
from PyQtUIkit.widgets._widget import _KitWidget as _KitWidget


class KitFlowLayout(QWidget, _KitWidget):
    border = IntProperty('border', 0)
    radius = IntProperty('radius', 4)

    def __init__(self):
        super().__init__()
        self.__widgets = []
        self.main_palette = 'Main'
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        strange_layout = QHBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)

        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        self.__layout = _FlowLayout()
        strange_widget.setLayout(self.__layout)

    def addWidget(self, widget: QWidget):
        self.__widgets.append(widget)
        self.__layout.addWidget(widget)

    def deleteWidget(self, w: int | QWidget):
        if isinstance(w, int):
            w = self.__layout.takeAt(w).widget()
        w.setParent(None)
        return w

    def clear(self):
        for _ in range(self.__layout.count()):
            self.__layout.takeAt(0).widget().setParent(None)
        self.__widgets.clear()

    def setSpacing(self, spacing):
        self.__layout.setSpacing(spacing)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.__layout.setContentsMargins(left, top, right, bottom)

    def count(self):
        return self.__layout.count()

    def _set_tm(self, tm):
        super()._set_tm(tm)
        for el in self.__widgets:
            if hasattr(el, '_set_tm'):
                el._set_tm(tm)

    def _apply_theme(self):
        for el in self.__widgets:
            if hasattr(el, '_apply_theme'):
                el._apply_theme()
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {self.main_palette.main};
            border: {self.border}px solid {self._tm.get('Border').main};
            border-radius: {self.radius}px;
        }}
        """)


class _FlowLayout(QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super(_FlowLayout, self).__init__(parent)
        self._hspacing = hspacing
        self._vspacing = vspacing
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        else:
            return self.smartSpacing(
                QStyle.PixelMetric.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        else:
            return self.smartSpacing(
                QStyle.PixelMetric.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return Qt.Orientation.Vertical

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(_FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testonly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineheight = 0
        for item in self._items:
            widget = item.widget()
            hspace = self.horizontalSpacing()
            if hspace == -1:
                hspace = widget.style().layoutSpacing(
                    QSizePolicy.Policy.PushButton,
                    QSizePolicy.Policy.PushButton, Qt.Orientation.Horizontal)
            vspace = self.verticalSpacing()
            if vspace == -1:
                vspace = widget.style().layoutSpacing(
                    QSizePolicy.Policy.PushButton,
                    QSizePolicy.Policy.PushButton, Qt.Orientation.Vertical)
            nextX = x + item.sizeHint().width() + hspace
            if nextX - hspace > effective.right() and lineheight > 0:
                x = effective.x()
                y = y + lineheight + vspace
                nextX = x + item.sizeHint().width() + hspace
                lineheight = 0
            if not testonly:
                item.setGeometry(
                    QRect(QPoint(x, y), item.sizeHint()))
            x = nextX
            lineheight = max(lineheight, item.sizeHint().height())
        return y + lineheight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()
