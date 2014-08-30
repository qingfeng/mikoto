# -*- coding: utf-8 -*-

from pygments import highlight
from pygments.lexers import TextLexer
from pygments.formatters import HtmlFormatter
from mikoto.text import translate_to_unicode


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


def highlight_code(path, src, div=False, **kwargs):
    src = translate_to_unicode(src)
    try:
        if path.endswith(('.html', '.mako')):
            lexer = MakoHtmlLexer(encoding='utf-8')
        elif path.endswith('.ptl'):
            lexer = PythonLexer(encoding='utf-8')
        elif path.endswith('.md'):
            lexer = RstLexer(encoding='utf-8')
        else:
            if path.endswith(IGNORE_FILE_EXTS):
                src = 'Hmm.., this is binary file.'
            lexer = guess_lexer_for_filename(path, src)
        lexer.encoding = 'utf-8'
        lexer.stripnl = False
    except ClassNotFound:
        # no code highlight
        lexer = TextLexer(encoding='utf-8')
    if div:
        formatter = _CodeHtmlFormatter
    else:
        formatter = HtmlFormatter

    src = highlight(src, lexer, formatter(linenos=True,
                                          lineanchors='L',
                                          anchorlinenos=True,
                                          encoding='utf-8',
                                          **kwargs))
    return src


