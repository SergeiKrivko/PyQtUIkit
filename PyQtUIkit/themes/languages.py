from enum import Enum
from typing import Type

from PyQt6.Qsci import QsciLexerCPP, QsciLexerPython, QsciLexerBash, QsciLexerBatch, QsciLexerCSharp, QsciLexerJava, \
    QsciLexerJavaScript, QsciLexerMarkdown, QsciLexerHTML, QsciLexerJSON, QsciLexerXML


class _Language:
    class PreviewType(Enum):
        NONE = 0
        SIMPLE = 1
        ACTIVE = 2
        ONLY = 3

    def __init__(self,
                 name: str,
                 extensions: list,
                 lexer: Type = None,
                 colors: dict = None,):
        self.name = name
        self.extensions = extensions
        self.lexer = lexer
        self.colors = colors or dict()


_languages = {
    '': _Language('txt', ['.txt']),
    'c': _Language(
        'c',
        extensions=['.c', '.h'],
        lexer=QsciLexerCPP,
        colors={
            QsciLexerCPP.Identifier: 'Identifier',
            QsciLexerCPP.PreProcessor: 'Preprocessor',
            QsciLexerCPP.Comment: 'Comment',
            QsciLexerCPP.CommentLine: 'Comment',
            QsciLexerCPP.CommentDoc: 'Comment',
            QsciLexerCPP.Keyword: 'Keyword',
            QsciLexerCPP.Number: 'Number',
            QsciLexerCPP.Operator: 'Identifier',
            QsciLexerCPP.DoubleQuotedString: 'String',
            QsciLexerCPP.SingleQuotedString: 'String',
            QsciLexerCPP.UnclosedString: 'String'
        },
    ),
    'python': _Language(
        'python',
        extensions=['.py'],
        lexer=QsciLexerPython,
        colors={
            QsciLexerPython.Identifier: 'Identifier',
            QsciLexerPython.Comment: 'Comment',
            QsciLexerPython.CommentBlock: 'Comment',
            QsciLexerPython.Keyword: 'Keyword',
            QsciLexerPython.Number: 'Number',
            QsciLexerPython.Operator: 'Identifier',
            QsciLexerPython.ClassName: 'Preprocessor',
            QsciLexerPython.Decorator: 'Preprocessor',
            QsciLexerPython.FunctionMethodName: 'Preprocessor',
            QsciLexerPython.DoubleQuotedString: 'String',
            QsciLexerPython.SingleQuotedString: 'String',
            QsciLexerPython.DoubleQuotedFString: 'String',
            QsciLexerPython.SingleQuotedFString: 'String',
            QsciLexerPython.TripleDoubleQuotedString: 'String',
            QsciLexerPython.TripleSingleQuotedString: 'String',
            QsciLexerPython.TripleDoubleQuotedFString: 'String',
            QsciLexerPython.TripleSingleQuotedFString: 'String',
        },
    ),
    'c++': _Language(
        'c++',
        extensions=['.cpp', '.h'],
        lexer=QsciLexerCPP,
        colors={
            QsciLexerCPP.Identifier: 'Identifier',
            QsciLexerCPP.PreProcessor: 'Preprocessor',
            QsciLexerCPP.Comment: 'Comment',
            QsciLexerCPP.CommentLine: 'Comment',
            QsciLexerCPP.CommentDoc: 'Comment',
            QsciLexerCPP.Keyword: 'Keyword',
            QsciLexerCPP.Number: 'Number',
            QsciLexerCPP.Operator: 'Identifier',
            QsciLexerCPP.DoubleQuotedString: 'String',
            QsciLexerCPP.SingleQuotedString: 'String',
            QsciLexerCPP.UnclosedString: 'String'
        }
    ),
    'bash': _Language(
        'bash',
        extensions=['.sh'],
        lexer=QsciLexerBash,
        colors={
            QsciLexerBash.Identifier: 'Identifier',
            QsciLexerBash.Operator: 'Identifier',
            QsciLexerBash.Number: 'Number',
            QsciLexerBash.Comment: 'Comment',
            QsciLexerBash.Keyword: 'Keyword',
            QsciLexerBash.DoubleQuotedString: 'String',
            QsciLexerBash.SingleQuotedString: 'String',
            QsciLexerBash.ParameterExpansion: 'Preprocessor',
            QsciLexerBash.Backticks: 'Preprocessor',
            QsciLexerBash.Error: 'Preprocessor'
        },
    ),
    'batch': _Language(
        'batch',
        extensions=['.cmd', '.bat', '.ps1'],
        lexer=QsciLexerBatch,
        colors={
            QsciLexerBatch.Keyword: 'Keyword',
            QsciLexerBatch.Comment: 'Comment',
            QsciLexerBatch.ExternalCommand: 'Preprocessor',
            QsciLexerBatch.Operator: 'Identifier',
            QsciLexerBatch.HideCommandChar: 'String',
            QsciLexerBatch.Variable: 'Number',
            QsciLexerBatch.Default: 'Identifier'
        },
    ),
    'markdown': _Language(
        'markdown',
        extensions=['.md'],
        lexer=QsciLexerMarkdown,
        colors={
            QsciLexerMarkdown.BlockQuote: 'Keyword',
            QsciLexerMarkdown.CodeBlock: 'Preprocessor',
            QsciLexerMarkdown.CodeBackticks: 'Preprocessor',
            QsciLexerMarkdown.CodeDoubleBackticks: 'Preprocessor',
            QsciLexerMarkdown.Header1: 'Keyword',
            QsciLexerMarkdown.Header2: 'Keyword',
            QsciLexerMarkdown.Header3: 'Keyword',
            QsciLexerMarkdown.Header4: 'Keyword',
            QsciLexerMarkdown.Header5: 'Keyword',
            QsciLexerMarkdown.Header6: 'Keyword',
            QsciLexerMarkdown.OrderedListItem: 'Keyword',
            QsciLexerMarkdown.UnorderedListItem: 'Keyword',
            QsciLexerMarkdown.Link: 'String',
            QsciLexerMarkdown.Default: 'Identifier'
        },
    ),
    'html': _Language(
        'html',
        extensions=['.html'],
        lexer=QsciLexerHTML,
        colors={
            QsciLexerHTML.Default: 'Identifier',
            QsciLexerHTML.Entity: 'Keyword',
            QsciLexerHTML.HTMLValue: 'Preprocessor',
            QsciLexerHTML.HTMLNumber: 'Number',
            QsciLexerHTML.HTMLComment: 'Comment',
            QsciLexerHTML.HTMLDoubleQuotedString: 'String',
            QsciLexerHTML.HTMLSingleQuotedString: 'String',
            QsciLexerHTML.Attribute: 'Preprocessor',
            QsciLexerHTML.Tag: 'Keyword',
            QsciLexerHTML.OtherInTag: 'Identifier',
            QsciLexerHTML.UnknownTag: 'Keyword',
            QsciLexerHTML.UnknownAttribute: 'Preprocessor',
        },
    ),
    'svg': _Language(
        'svg',
        extensions=['.svg'],
        lexer=QsciLexerXML,
        colors={
            QsciLexerXML.Default: 'Identifier',
            QsciLexerXML.Entity: 'Keyword',
            QsciLexerXML.HTMLValue: 'Preprocessor',
            QsciLexerXML.HTMLNumber: 'Number',
            QsciLexerXML.HTMLComment: 'Comment',
            QsciLexerXML.HTMLDoubleQuotedString: 'String',
            QsciLexerXML.HTMLSingleQuotedString: 'String',
            QsciLexerXML.Attribute: 'Preprocessor',
            QsciLexerXML.Tag: 'Keyword',
            QsciLexerXML.XMLTagEnd: 'Keyword',
            QsciLexerXML.OtherInTag: 'Identifier',
            QsciLexerXML.UnknownTag: 'Keyword',
            QsciLexerXML.UnknownAttribute: 'Preprocessor',
        },
    ),
    'json': _Language(
        'json',
        extensions=['.json', '.dg'],
        lexer=QsciLexerJSON,
        colors={
            QsciLexerJSON.Default: 'Identifier',
            QsciLexerJSON.Number: 'Number',
            QsciLexerJSON.Keyword: 'Keyword',
            QsciLexerJSON.Operator: 'Identifier',
            QsciLexerJSON.CommentBlock: 'Comment',
            QsciLexerJSON.CommentLine: 'Comment',
            QsciLexerJSON.EscapeSequence: 'Identifier',
            QsciLexerJSON.String: 'String',
            QsciLexerJSON.Property: 'Preprocessor',
            QsciLexerJSON.UnclosedString: 'String',
        },
    ),
    'c#': _Language(
        'c#',
        extensions=['.cs'],
        lexer=QsciLexerCSharp,
    ),
    'java': _Language(
        'java',
        extensions=['.java'],
        lexer=QsciLexerJava,
    ),
    'javascript': _Language(
        'javascript',
        extensions=['.js'],
        lexer=QsciLexerJavaScript,
        colors=(js_colors := {
            QsciLexerJavaScript.Default: 'Identifier',
            QsciLexerJavaScript.Number: 'Number',
            QsciLexerJavaScript.Keyword: 'Keyword',
            QsciLexerJavaScript.KeywordSet2: 'Keyword',
            QsciLexerJavaScript.Comment: 'Comment',
            QsciLexerJavaScript.CommentLine: 'Comment',
            QsciLexerJavaScript.CommentDoc: 'Comment',
            QsciLexerJavaScript.CommentLineDoc: 'Comment',
            QsciLexerJavaScript.InactiveComment: 'Comment',
            QsciLexerJavaScript.SingleQuotedString: 'String',
            QsciLexerJavaScript.UnclosedString: 'String',
            QsciLexerJavaScript.DoubleQuotedString: 'String',
            QsciLexerJavaScript.RawString: 'String',
            QsciLexerJavaScript.HashQuotedString: 'String',
            QsciLexerJavaScript.VerbatimString: 'String',
            QsciLexerJavaScript.Identifier: 'Identifier',
            QsciLexerJavaScript.Operator: 'Identifier',
            QsciLexerJavaScript.PreProcessor: 'Preprocessor',
        })
    ),
    'typescript': _Language(
        'typescript',
        extensions=['.js'],
        lexer=QsciLexerJavaScript,
        colors=js_colors,
    ),
    'xml': _Language(
        'xml',
        extensions=['.xml'],
        lexer=QsciLexerXML,
        colors={
            QsciLexerXML.Default: 'Identifier',
            QsciLexerXML.Entity: 'Keyword',
            QsciLexerXML.HTMLValue: 'Preprocessor',
            QsciLexerXML.HTMLNumber: 'Number',
            QsciLexerXML.HTMLComment: 'Comment',
            QsciLexerXML.HTMLDoubleQuotedString: 'String',
            QsciLexerXML.HTMLSingleQuotedString: 'String',
            QsciLexerXML.Attribute: 'Preprocessor',
            QsciLexerXML.Tag: 'Keyword',
            QsciLexerXML.XMLTagEnd: 'Keyword',
            QsciLexerXML.OtherInTag: 'Identifier',
            QsciLexerXML.UnknownTag: 'Keyword',
            QsciLexerXML.UnknownAttribute: 'Preprocessor',
        }
    ),
}


_names = _languages.copy()
for key, item in _languages.items():
    for ext in item.extensions:
        _names[ext[1:]] = item


def language(name):
    if name not in _names:
        return _names['']
    return _names[name]


def all_languages():
    return _names.values()

