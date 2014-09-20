# -*- coding: utf-8 -*-

from mikoto.markdown import render_markdown
from mikoto.rst import render_rst
from mikoto.code import render_code, render_highlight_code
from mikoto.text import translate_to_unicode

__all__ = ['Mikoto']

class Mikoto(object):

    def __init__(self, text):
        self.text = text
        self.unicode = translate_to_unicode(text)

    @property
    def markdown(self):
        return render_markdown(self.unicode)

    @property
    def restructuredtext(self):
        return render_rst(self.unicode)

    @property
    def code(self):
        return render_code(self.unicode)

    def highlight_code(self, path):
        return render_highlight_code(self.unicode, path)
