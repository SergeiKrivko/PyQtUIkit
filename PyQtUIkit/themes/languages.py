from enum import Enum
from typing import Type

from PyQt6.Qsci import QsciLexerCPP, QsciLexerPython, QsciLexerBash, QsciLexerBatch, QsciLexerCSharp, QsciLexerJava, \
    QsciLexerJavaScript, QsciLexerMarkdown, QsciLexerHTML, QsciLexerJSON, QsciLexerXML, QsciLexerMASM, QsciLexerNASM, \
    QsciLexerCSS


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
            QsciLexerPython.Decorator: 'Function',
            QsciLexerPython.FunctionMethodName: 'Preprocessor',
            QsciLexerPython.DoubleQuotedString: 'String',
            QsciLexerPython.SingleQuotedString: 'String',
            QsciLexerPython.DoubleQuotedFString: 'String',
            QsciLexerPython.SingleQuotedFString: 'String',
            QsciLexerPython.TripleDoubleQuotedString: 'String',
            QsciLexerPython.TripleSingleQuotedString: 'String',
            QsciLexerPython.TripleDoubleQuotedFString: 'String',
            QsciLexerPython.TripleSingleQuotedFString: 'String',
            QsciLexerPython.UnclosedString: 'String',
            QsciLexerPython.HighlightedIdentifier: 'Function'
        },
    ),
    'c++': _Language(
        'c++',
        extensions=['.cpp', '.h', '.hpp'],
        lexer=QsciLexerCPP,
        colors={
            QsciLexerCPP.Default: 'Identifier',
            QsciLexerCPP.Number: 'Number',
            QsciLexerCPP.Identifier: 'Identifier',
            QsciLexerCPP.Keyword: 'Keyword',
            QsciLexerCPP.Operator: 'Identifier',
            QsciLexerCPP.PreProcessor: 'Preprocessor',
            QsciLexerCPP.GlobalClass: 'Preprocessor',
            QsciLexerCPP.InactiveGlobalClass: 'Comment',
            QsciLexerCPP.UUID: 'Number',
            QsciLexerCPP.EscapeSequence: 'Preprocessor',
            QsciLexerCPP.InactiveEscapeSequence: 'Preprocessor',

            QsciLexerCPP.Comment: 'Comment',
            QsciLexerCPP.CommentDoc: 'Comment',
            QsciLexerCPP.CommentLine: 'Comment',
            QsciLexerCPP.CommentLineDoc: 'Comment',
            QsciLexerCPP.CommentDocKeyword: 'Comment',
            QsciLexerCPP.CommentDocKeywordError: 'Comment',
            QsciLexerCPP.InactiveComment: 'Comment',
            QsciLexerCPP.InactiveCommentLine: 'Comment',
            QsciLexerCPP.InactiveCommentDoc: 'Comment',
            QsciLexerCPP.InactiveCommentLineDoc: 'Comment',
            QsciLexerCPP.InactiveCommentDocKeyword: 'Comment',
            QsciLexerCPP.InactiveCommentDocKeywordError: 'Comment',
            QsciLexerCPP.PreProcessorComment: 'Comment',
            QsciLexerCPP.PreProcessorCommentLineDoc: 'Comment',
            QsciLexerCPP.InactivePreProcessorComment: 'Comment',
            QsciLexerCPP.InactivePreProcessorCommentLineDoc: 'Comment',

            QsciLexerCPP.SingleQuotedString: 'String',
            QsciLexerCPP.DoubleQuotedString: 'String',
            QsciLexerCPP.UnclosedString: 'String',
            QsciLexerCPP.RawString: 'String',
            QsciLexerCPP.VerbatimString: 'String',
            QsciLexerCPP.HashQuotedString: 'String',
            QsciLexerCPP.TripleQuotedVerbatimString: 'String',
            QsciLexerCPP.InactiveSingleQuotedString: 'String',
            QsciLexerCPP.InactiveDoubleQuotedString: 'String',
            QsciLexerCPP.InactiveUnclosedString: 'String',
            QsciLexerCPP.InactiveRawString: 'String',
            QsciLexerCPP.InactiveVerbatimString: 'String',
            QsciLexerCPP.InactiveHashQuotedString: 'String',
            QsciLexerCPP.InactiveTripleQuotedVerbatimString: 'String',
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
            QsciLexerBash.Error: 'Danger'
        },
    ),
    'batch': _Language(
        'batch',
        extensions=['.cmd', '.bat'],
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
            QsciLexerHTML.UnknownAttribute: 'Danger',
        },
    ),
    'json': _Language(
        'json',
        extensions=['.json'],
        lexer=QsciLexerJSON,
        colors={
            QsciLexerJSON.Default: 'Identifier',
            QsciLexerJSON.Number: 'Number',
            QsciLexerJSON.Keyword: 'Keyword',
            QsciLexerJSON.KeywordLD: 'Keyword',
            QsciLexerJSON.Operator: 'Identifier',
            QsciLexerJSON.CommentBlock: 'Comment',
            QsciLexerJSON.CommentLine: 'Comment',
            QsciLexerJSON.EscapeSequence: 'Identifier',
            QsciLexerJSON.String: 'String',
            QsciLexerJSON.UnclosedString: 'String',
            QsciLexerJSON.Property: 'Preprocessor',
            QsciLexerJSON.Error: 'Danger',
            QsciLexerJSON.IRI: 'Function',
            QsciLexerJSON.IRICompact: 'Function',
        },
    ),
    'c#': _Language(
        'c#',
        extensions=['.cs'],
        lexer=QsciLexerCSharp,
        colors={
            QsciLexerCSharp.Default: 'Identifier',
            QsciLexerCSharp.Number: 'Number',
            QsciLexerCSharp.Identifier: 'Identifier',
            QsciLexerCSharp.Keyword: 'Keyword',
            QsciLexerCSharp.Operator: 'Identifier',
            QsciLexerCSharp.PreProcessor: 'Preprocessor',
            QsciLexerCSharp.GlobalClass: 'Preprocessor',
            QsciLexerCSharp.InactiveGlobalClass: 'Comment',
            QsciLexerCSharp.UUID: 'Number',
            QsciLexerCSharp.EscapeSequence: 'Preprocessor',
            QsciLexerCSharp.InactiveEscapeSequence: 'Preprocessor',

            QsciLexerCSharp.Comment: 'Comment',
            QsciLexerCSharp.CommentDoc: 'Comment',
            QsciLexerCSharp.CommentLine: 'Comment',
            QsciLexerCSharp.CommentLineDoc: 'Comment',
            QsciLexerCSharp.CommentDocKeyword: 'Comment',
            QsciLexerCSharp.CommentDocKeywordError: 'Comment',
            QsciLexerCSharp.InactiveComment: 'Comment',
            QsciLexerCSharp.InactiveCommentLine: 'Comment',
            QsciLexerCSharp.InactiveCommentDoc: 'Comment',
            QsciLexerCSharp.InactiveCommentLineDoc: 'Comment',
            QsciLexerCSharp.InactiveCommentDocKeyword: 'Comment',
            QsciLexerCSharp.InactiveCommentDocKeywordError: 'Comment',
            QsciLexerCSharp.PreProcessorComment: 'Comment',
            QsciLexerCSharp.PreProcessorCommentLineDoc: 'Comment',
            QsciLexerCSharp.InactivePreProcessorComment: 'Comment',
            QsciLexerCSharp.InactivePreProcessorCommentLineDoc: 'Comment',

            QsciLexerCSharp.SingleQuotedString: 'String',
            QsciLexerCSharp.DoubleQuotedString: 'String',
            QsciLexerCSharp.UnclosedString: 'String',
            QsciLexerCSharp.RawString: 'String',
            QsciLexerCSharp.VerbatimString: 'String',
            QsciLexerCSharp.HashQuotedString: 'String',
            QsciLexerCSharp.TripleQuotedVerbatimString: 'String',
            QsciLexerCSharp.InactiveSingleQuotedString: 'String',
            QsciLexerCSharp.InactiveDoubleQuotedString: 'String',
            QsciLexerCSharp.InactiveUnclosedString: 'String',
            QsciLexerCSharp.InactiveRawString: 'String',
            QsciLexerCSharp.InactiveVerbatimString: 'String',
            QsciLexerCSharp.InactiveHashQuotedString: 'String',
            QsciLexerCSharp.InactiveTripleQuotedVerbatimString: 'String',
        }
    ),
    'java': _Language(
        'java',
        extensions=['.java'],
        lexer=QsciLexerJava,
        colors={
            QsciLexerJava.Default: 'Identifier',
            QsciLexerJava.Identifier: 'Identifier',
            QsciLexerJava.Number: 'Number',
            QsciLexerJava.Keyword: 'Keyword',
            QsciLexerJava.Operator: 'Identifier',
            QsciLexerJava.PreProcessor: 'Preprocessor',
            QsciLexerJava.GlobalClass: 'Preprocessor',
            QsciLexerJava.InactiveGlobalClass: 'Comment',
            QsciLexerJava.UUID: 'Number',
            QsciLexerJava.EscapeSequence: 'Preprocessor',
            QsciLexerJava.InactiveEscapeSequence: 'Preprocessor',

            QsciLexerJava.Comment: 'Comment',
            QsciLexerJava.CommentDoc: 'Comment',
            QsciLexerJava.CommentLine: 'Comment',
            QsciLexerJava.CommentLineDoc: 'Comment',
            QsciLexerJava.CommentDocKeyword: 'Comment',
            QsciLexerJava.CommentDocKeywordError: 'Comment',
            QsciLexerJava.InactiveComment: 'Comment',
            QsciLexerJava.InactiveCommentLine: 'Comment',
            QsciLexerJava.InactiveCommentDoc: 'Comment',
            QsciLexerJava.InactiveCommentLineDoc: 'Comment',
            QsciLexerJava.InactiveCommentDocKeyword: 'Comment',
            QsciLexerJava.InactiveCommentDocKeywordError: 'Comment',
            QsciLexerJava.PreProcessorComment: 'Comment',
            QsciLexerJava.PreProcessorCommentLineDoc: 'Comment',
            QsciLexerJava.InactivePreProcessorComment: 'Comment',
            QsciLexerJava.InactivePreProcessorCommentLineDoc: 'Comment',

            QsciLexerJava.SingleQuotedString: 'String',
            QsciLexerJava.DoubleQuotedString: 'String',
            QsciLexerJava.UnclosedString: 'String',
            QsciLexerJava.RawString: 'String',
            QsciLexerJava.VerbatimString: 'String',
            QsciLexerJava.HashQuotedString: 'String',
            QsciLexerJava.TripleQuotedVerbatimString: 'String',
            QsciLexerJava.InactiveSingleQuotedString: 'String',
            QsciLexerJava.InactiveDoubleQuotedString: 'String',
            QsciLexerJava.InactiveUnclosedString: 'String',
            QsciLexerJava.InactiveRawString: 'String',
            QsciLexerJava.InactiveVerbatimString: 'String',
            QsciLexerJava.InactiveHashQuotedString: 'String',
            QsciLexerJava.InactiveTripleQuotedVerbatimString: 'String',
        }
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
        extensions=['.ts'],
        lexer=QsciLexerJavaScript,
        colors=js_colors,
    ),
    'xml': _Language(
        'xml',
        extensions=['.xml', '.svg'],
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
    'masm': _Language(
        'masm',
        extensions=['.asm', '.masm'],
        lexer=QsciLexerMASM,
        colors={
            QsciLexerMASM.Default: 'Identifier',
            QsciLexerMASM.Operator: 'Identifier',
            QsciLexerMASM.Identifier: 'Identifier',
            QsciLexerMASM.Comment: 'Comment',
            QsciLexerMASM.CommentDirective: 'Comment',
            QsciLexerMASM.BlockComment: 'Comment',
            QsciLexerMASM.CPUInstruction: 'Keyword',
            QsciLexerMASM.FPUInstruction: 'Keyword',
            QsciLexerMASM.ExtendedInstruction: 'Keyword',
            QsciLexerMASM.Directive: 'Preprocessor',
            QsciLexerMASM.Number: 'Number',
            QsciLexerMASM.SingleQuotedString: 'String',
            QsciLexerMASM.DoubleQuotedString: 'String',
            QsciLexerMASM.UnclosedString: 'String',
            QsciLexerMASM.Register: 'Function',
        }
    ),
    'nasm': _Language(
        'masm',
        extensions=['.asm', '.nasm'],
        lexer=QsciLexerMASM,
        colors={
            QsciLexerNASM.Default: 'Identifier',
            QsciLexerNASM.Operator: 'Identifier',
            QsciLexerNASM.Identifier: 'Identifier',
            QsciLexerNASM.Comment: 'Comment',
            QsciLexerNASM.CommentDirective: 'Comment',
            QsciLexerNASM.BlockComment: 'Comment',
            QsciLexerNASM.CPUInstruction: 'Keyword',
            QsciLexerNASM.FPUInstruction: 'Keyword',
            QsciLexerNASM.ExtendedInstruction: 'Keyword',
            QsciLexerNASM.Directive: 'Preprocessor',
            QsciLexerNASM.Number: 'Number',
            QsciLexerNASM.SingleQuotedString: 'String',
            QsciLexerNASM.DoubleQuotedString: 'String',
            QsciLexerNASM.UnclosedString: 'String',
            QsciLexerNASM.Register: 'Keyword',
        }
    ),
    'css': _Language(
        'css',
        extensions=['.css', '.scss'],
        lexer=QsciLexerCSS,
        colors={
            QsciLexerCSS.Default: 'Identifier',
            QsciLexerCSS.CSS1Property: 'Preprocessor',
            QsciLexerCSS.CSS2Property: 'Preprocessor',
            QsciLexerCSS.CSS3Property: 'Preprocessor',
            QsciLexerCSS.SingleQuotedString: 'String',
            QsciLexerCSS.DoubleQuotedString: 'String',
            QsciLexerCSS.Comment: 'Comment',
            QsciLexerCSS.Tag: 'Function',
            QsciLexerCSS.Operator: 'Identifier',
            QsciLexerCSS.ClassSelector: 'Function',
            QsciLexerCSS.Attribute: 'Keyword',
            QsciLexerCSS.AtRule: 'Keyword',
            QsciLexerCSS.MediaRule: 'Keyword',
            QsciLexerCSS.ExtendedCSSProperty: 'Keyword',
            QsciLexerCSS.ExtendedPseudoClass: 'Keyword',
            QsciLexerCSS.ExtendedPseudoElement: 'Keyword',
            QsciLexerCSS.Important: 'Keyword',
            QsciLexerCSS.Value: 'Number',
            QsciLexerCSS.Variable: 'Identifier',
            QsciLexerCSS.UnknownProperty: 'Preprocessor',
        }
    ),
}


_names = _languages.copy()
for key, item in _languages.items():
    for ext in item.extensions:
        if ext[1:] not in _names:
            _names[ext.lstrip('.')] = item


def language(name):
    if name not in _names:
        return _names['']
    return _names[name]


def all_languages():
    return _names.values()

