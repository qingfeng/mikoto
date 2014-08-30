# -*- coding: utf-8 -*-

import re

RE_CHECKBOX_IN_HTML = re.compile('<li>\[[x\s]\].+</li>')
RE_CHECKBOX_IN_TEXT = re.compile('- (\[[x\s]\]).+')
CHECKED = '[x]'
UNCHECKED = '[ ]'
HTML_CHECKED = '<li>[x]'
HTML_UNCHECKED = '<li>[ ]'


def get_checkbox_count(content):
    m = re.findall(RE_CHECKBOX_IN_TEXT, content)
    if m:
        checked = filter(lambda x: x == CHECKED, m)
        return (len(checked), len(m))


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

