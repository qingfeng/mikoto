# -*- coding: utf-8 -*-

import docutils
from docutils.core import publish_parts


def render_rst(text):
    html = publish_parts(text, writer_name='html')
    return html['html_body']
