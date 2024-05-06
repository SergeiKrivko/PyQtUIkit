from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget

from PyQtUIkit.core.font import KitFont

from PyQtUIkit.core.properties import PaletteProperty, IntProperty, FontProperty, EnumProperty

from PyQtUIkit.widgets._widget import _KitWidget


try:
    from PyQt6.Qsci import QsciScintilla, QsciLexer
except ImportError:
    class KitScintilla(QWidget, _KitWidget):
        def __init__(self, *args, **kwargs):
            super().__init__()
            raise ImportError("QScintilla is not installed. Please install by running 'pip install PyQt6-QScintilla'.")
else:
    from PyQtUIkit.themes import languages

    class KitScintilla(QsciScintilla, _KitWidget):
        main_palette = PaletteProperty('main_palette', 'Main')
        margins_palette = PaletteProperty('margins_palette', 'Bg')
        border = IntProperty('border', 0)
        radius = IntProperty('radius', 0)
        font = FontProperty('font', 'mono')
        font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)

        ARROW_MARKER_NUM = 8

        def __init__(self, language='txt'):
            super().__init__()
            self._lang = languages.language(language)

            self.setCaretLineVisible(True)

            self.setAutoCompletionThreshold(1)
            self.setAutoCompletionCaseSensitivity(True)
            self.setAutoCompletionReplaceWord(True)
            self.setCallTipsStyle(QsciScintilla.CallTipsStyle.CallTipsContext)
            self.setCallTipsPosition(QsciScintilla.CallTipsPosition.CallTipsAboveText)

            self.setIndentationsUseTabs(False)
            self.setTabWidth(4)
            self.setIndentationGuides(True)
            self.setTabIndents(True)
            self.setAutoIndent(True)

            self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
            self.setCallTipsVisible(0)
            self.setMarginWidth(0, 40)

            self.current_row = 0

            self._apply_lexer()

        @property
        def language(self):
            return self._lang

        @language.setter
        def language(self, value):
            self._lang = languages.language(value)
            self._apply_lexer()
            self._apply_theme()

        def _apply_lexer(self):
            if self._lang.lexer is not None:
                self._lexer = self._lang.lexer(self)
                self.setLexer(self._lexer)
            else:
                self._lexer = None

        def _apply_theme(self):
            if self._tm is None or not self._tm.active:
                return
            font = self.font.get(self.font_size)
            self.setFont(font)

            if isinstance(self._lexer, QsciLexer):
                self._lexer.setDefaultFont(font)
                self._lexer.setPaper(QColor(self.main_palette.main))
                for key, item in self._lang.colors.items():
                    self._lexer.setColor(self._tm.code_color(item), key)
                    self._lexer.setFont(font, key)
                self._lexer.setFont(font, 0)

            self.setMarkerBackgroundColor(QColor(self.main_palette.text), self.ARROW_MARKER_NUM)
            self.setMarginsBackgroundColor(QColor(self.margins_palette.main))
            self.setMarginsForegroundColor(QColor(self.margins_palette.text))
            self.setCaretLineBackgroundColor(QColor(self.main_palette.hover))
            self.setMatchedBraceBackgroundColor(QColor(self.main_palette.hover))
            self.setMatchedBraceForegroundColor(self._tm.code_color('Keyword'))
            self.setUnmatchedBraceBackgroundColor(QColor(self.main_palette.hover))
            self.setUnmatchedBraceForegroundColor(self._tm.code_color('Keyword'))
            self.setPaper(QColor(self.main_palette.main))
            self.setColor(QColor(self.main_palette.text))

            self.setStyleSheet(f"""
    QsciScintilla {{
        background-color: {self.main_palette.main};
        border: {self.border}px solid {self.border_palette.main};
    }}
    QsciScintilla QScrollBar:vertical {{
        background: {self.main_palette.main};
        width: 12px;
        margin: 0px;
    }}
    QsciScintilla QScrollBar::handle::vertical {{
        background-color: {self.border_palette.main};
        margin: 2px 2px 2px 6px;
        border-radius: 2px;
        min-height: 20px;
    }}
    QsciScintilla QScrollBar::handle::vertical:hover {{
        margin: 2px;
        border-radius: 4px;
    }}
    QsciScintilla QScrollBar::sub-page, QScrollBar::add-page {{
        background: none;
    }}
    QsciScintilla QScrollBar::sub-line, QScrollBar::add-line {{
        background: none;
        height: 0px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }}""")
