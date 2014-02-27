# -*- coding: utf-8 -*-

from __future__ import absolute_import
import re
import misaka
import chardet

from cgi import escape
from pygments.formatters import HtmlFormatter
from pygments.lexers import (TextLexer, get_lexer_by_name,
                             guess_lexer_for_filename, MakoHtmlLexer,
                             PythonLexer, RstLexer)
from pygments.util import ClassNotFound
from pygments import highlight

from mikoto.libs.consts import (SOURCE_FILE, NOT_GENERATED,
                                IGNORE_FILE_EXTS, IS_GENERATED)
from mikoto.libs.emoji import parse_emoji


RST_RE = re.compile(r'.*\.re?st(\.txt)?$')
RE_TICKET = re.compile(r'(?:^|\s)#(\d+)')
RE_ISSUE = re.compile(r'(?:^|\s)#issue(\d+)')
RE_USER_MENTION = re.compile(r'(^|\W)@([a-zA-Z0-9_]+)')
RE_COMMIT = re.compile(r'(^|\s)([0-9a-f]{7,40})')
RE_IMAGE_FILENAME = re.compile(
    r'^.+\.(?:jpg|png|gif|jpeg|mobileprovision|svg|ico)$', flags=re.IGNORECASE)
RE_CHECKBOX_IN_HTML = re.compile('<li>\[[x\s]\].+</li>')
RE_CHECKBOX_IN_TEXT = re.compile('- (\[[x\s]\]).+')

CHECKED = '[x]'
UNCHECKED = '[ ]'
HTML_CHECKED = '<li>[x]'
HTML_UNCHECKED = '<li>[ ]'
RE_PR_IN_MESSAGE = re.compile(r'(?:^|\s)#(\d+)(?:\s|$)')
RE_ISSUE_IN_MESSAGE = re.compile(r'(?:^|\s)#issue(\d+)(?:\s|$)')

TICKET_LINK_TEXT = r'<a href="/%s/pull/\1/" class="issue-link">#\1</a>'
ISSUE_LINK_TEXT = r'<a href="/%s/issues/\1/" class="issue-link">#\1</a>'
COMMIT_LINK_TEXT = r' <a href="/%s/commit/\2">\2</a>'
USER_LINK_TEXT = r'\1<a href="/people/\2/" class="user-mention">@\2</a>'


class _CodeHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_div(self._wrap_pre(self._wrap_a_line(source)))

    def _wrap_a_line(self, source):
        for i, t in source:
            if i == 1:
                # it's a line of formatted code
                t = '<div>' + t + '</div>'
            yield i, t


class _CodeRenderer(misaka.HtmlRenderer):
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

_generic_renderer = _CodeRenderer(misaka.HTML_HARD_WRAP |
                                  misaka.HTML_SAFELINK |
                                  misaka.HTML_SKIP_STYLE |
                                  misaka.HTML_SKIP_SCRIPT |
                                  misaka.HTML_ESCAPE)
_markdown_renderer = misaka.Markdown(_generic_renderer,
                                     extensions=misaka.EXT_FENCED_CODE |
                                     misaka.EXT_NO_INTRA_EMPHASIS |
                                     misaka.EXT_AUTOLINK |
                                     misaka.EXT_TABLES |
                                     misaka.EXT_STRIKETHROUGH)


def decode_charset_to_unicode(charset, default='utf-8'):
    try:
        return charset.decode(default)
    except UnicodeDecodeError:
        charset_encoding = chardet.detect(charset).get('encoding') or default
        return charset.decode(charset_encoding, 'ignore')


def highlight_code(path, src, div=False, **kwargs):
    src = decode_charset_to_unicode(src)
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


def render_checklist(content):
    i = 0
    while 1:
        m = re.search(RE_CHECKBOX_IN_HTML, content)
        if not m:
            break
        t = m.group(0).replace('<li>', '').replace('</li>', '')
        source = '<li><label><input type="checkbox" data-item-index="%d"' % i
        end = lambda type, idx: '> ' + t.lstrip(type).strip() + \
              '</label></li>' + content[idx + len(t) + len('<li></li>'):]

        if t.startswith(CHECKED):
            checked_idx = content.find(HTML_CHECKED)
            content = content[:checked_idx] + source + ' checked' + \
                      end(CHECKED, checked_idx)
        else:
            unchecked_idx = content.find(HTML_UNCHECKED)
            content = content[:unchecked_idx] + source + \
                      end(UNCHECKED, unchecked_idx)
        i += 1
    return content


def get_checkbox_count(content):
    m = re.findall(RE_CHECKBOX_IN_TEXT, content)
    if m:
        checked = filter(lambda x: x == CHECKED, m)
        return (len(checked), len(m))


def is_binary(fname):
    ext = fname.split('.')
    if ext is None:
        return False
    if len(ext) == 1:
        return ext[0] not in SOURCE_FILE
    ext = '.' + ext[-1]
    if ext in IS_GENERATED:
        return False
    if ext in IGNORE_FILE_EXTS or ext not in (SOURCE_FILE + NOT_GENERATED):
        return True
    return False


def get_mentions_from_text(text):
    try:
        from models.team import Team
    except ImportError:
        from mikoto.libs.mock import Team
    recipients = RE_USER_MENTION.findall(text)
    users = set()
    for _, r in recipients:
        t = Team.get_by_uid(r)
        if t:
            users.update(t.all_members)
        else:
            users.add(r)
    return list(users)


# TODO: move out, not recommended
def render_markdown_with_team(content, team):
    text = render_markdown(content)
    text = re.sub(RE_TICKET, r'<a href="' + team.url +
                  r'issues/\1/" class="issue-link">#\1</a>', text)
    return parse_emoji(text, is_escape=False)


def render_commit_message(message, project):
    text = parse_emoji(message)
    text = re.sub(RE_PR_IN_MESSAGE,
                  r' <a href="/%s/newpull/\1">#\1</a> ' % project.name,
                  text)
    text = re.sub(RE_ISSUE_IN_MESSAGE,
                  r' <a href="/%s/issues/\1">#\1</a> ' % project.name,
                  text)
    text = text.decode('utf8')
    return text


def render_markdown(content):
    if not content:
        content = ''
    return _markdown_renderer.render(content)


def render_markdown_with_project(content, project_name):
    text = render_markdown(content)
    text = re.sub(RE_TICKET,
                  TICKET_LINK_TEXT % project_name,
                  text)
    text = re.sub(RE_ISSUE,
                  ISSUE_LINK_TEXT % project_name,
                  text)
    text = re.sub(RE_COMMIT,
                  COMMIT_LINK_TEXT % project_name,
                  text)
    text = text.replace("[PROJECT]", "/%s/raw/master/" % project_name)
    return text


def render(content, project_name=None):
    if project_name:
        return render_markdown_with_project(content, project_name)
    return render_markdown(content)
