# -*- coding: utf-8 -*-

from pygments import highlight
from pygments.lexers import (TextLexer,
                             RstLexer,
                             MakoHtmlLexer,
                             PythonLexer,
                             guess_lexer_for_filename)
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

IGNORE_FILE_EXTS = (
    # compress
    '.tar', '.zip', '.rar', '.gz', '.bz', '.bz2', '.dmg', '.jar',
    # image
    '.bmp', '.jpeg', '.jpg', '.png', '.gif', '.svg', '.ico',
    # font
    '.ttf',
    # media
    '.mp3', '.swf', '.fla', '.flash', '.wmv', '.asf', '.asx', '.rm',
    '.rmvb', '.mpg', '.mpeg', '.mpe', '.3gp', '.mov', '.mp4', '.m4v',
    '.avi', '.dat', '.mkv', '.flv', '.vob',
    # min
    '.min.js', '.min.css',
    # binary
    '.pdf', '.svn-base', '.pcap',
)


def render_code(text):
    lexer = TextLexer(encoding='utf-8')
    # the output of highlight is string
    output = highlight(text,
                       lexer,
                       HtmlFormatter(linenos=True,
                                     lineanchors='L',
                                     anchorlinenos=True,
                                     encoding='utf-8'))
    return output.decode('utf-8')


def render_highlight_code(text, path, **kwargs):
    try:
        if path.endswith(('.html', '.mako')):
            lexer = MakoHtmlLexer(encoding='utf-8')
        elif path.endswith('.ptl'):
            lexer = PythonLexer(encoding='utf-8')
        elif path.endswith('.md'):
            lexer = RstLexer(encoding='utf-8')
        else:
            if path.endswith(IGNORE_FILE_EXTS):
                text = 'Hmm.., this is binary file.'
            lexer = guess_lexer_for_filename(path, text)
        lexer.encoding = 'utf-8'
        lexer.stripnl = False
    except ClassNotFound:
        # no code highlight
        lexer = TextLexer(encoding='utf-8')

    formatter = CodeHtmlFormatter

    return highlight(text, lexer, formatter(linenos='inline',
                                            lineanchors='L',
                                            anchorlinenos=True,
                                            encoding='utf-8',
                                            **kwargs))


class CodeHtmlFormatter(HtmlFormatter):

    def wrap(self, source, outfile):
        return self._wrap_code(source)

    def _wrap_code(self, source):
        yield 0, '<table>'
        for i, t in source:
            if i == 1:
                # it's a line of formatted code
                t = '<tr><td class="blob-num">%s</td></tr>' % t
            yield i, t
        yield 0, '</table>'

    def _wrap_num(self, source):
        for i, t in source:
            if i == 1:
                t = '</td><td class="blob-code">%s' % t
            yield i, t

    def _format_lines(self, tokensource):
        return self._wrap_num(super(CodeHtmlFormatter, self)._format_lines(tokensource))
