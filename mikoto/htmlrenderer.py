# -*- coding: utf-8 -*-

import re
from cgi import escape
import misaka
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from mikoto.libs.emoji import parse_emoji
from mikoto.checklist import render_checklist

RE_USER_MENTION = re.compile(r'(^|\W)@([a-zA-Z0-9_]+)')
USER_LINK_TEXT = r'\1<a href="/people/\2/" class="user-mention">@\2</a>'


class HtmlRenderer(misaka.HtmlRenderer):

    def postprocess(self, text):
        if not text:
            return text
        text = render_checklist(text)
        text = parse_emoji(text, is_escape=False)
        return RE_USER_MENTION.sub(USER_LINK_TEXT, text)

    def block_code(self, text, lang):
        if not lang:
            text = escape(text.strip())
            text = self.__text_to_unichr(text)
            return '\n<pre><code>%s</code></pre>\n' % text
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

    def codespan(self, text):
        text = self.__text_to_unichr(text)
        return '<code>%s</code>' % text

    def header(self, text, level):
        if level == 1 and re.match(r'\d+', text):
            return '#' + text
        return '<h%s>%s</h%s>' % (level, text, level)

    def __text_to_unichr(self, text):
        text = text.replace("@", "&#64;")
        return text

    def __link_to_local_project(self, link):
        if not (link.startswith("http://")
                or link.startswith("https://")):
            link = "[PROJECT]%s" % link
        return link

    def image(self, link, title, alt_text):
        alt_text = alt_text or ""
        link = self.__link_to_local_project(link)
        return '<img src="%s" alt="%s">' % (link, alt_text)

    def link(self, link, title, content):
        title = title or ""
        link = self.__link_to_local_project(link)
        return '<a href="%s" title="%s">%s</a>' % (link, title, content)
