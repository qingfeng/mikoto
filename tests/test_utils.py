# encoding: utf-8

from __future__ import absolute_import
from unittest import TestCase
from mikoto.libs.text import render_markdown, get_mentions_from_text


class TestUtils(TestCase):

    def test_mentioned_people_from_text(self):
        text1 = "@xingben OK"
        text2 = "OK @xingben"
        text3 = "Done. @xingben check?"
        text4 = "Done. @xingben @qingfeng"
        text5 = "@xingben @qingfeng Done"
        text6 = "@xingben Done @qingfeng @zhangchi Check?"
        text7 = "Hello, World"
        assert ['xingben'] == get_mentions_from_text(text1)
        assert ['xingben'] == get_mentions_from_text(text2)
        assert ['xingben'] == get_mentions_from_text(text3)
        assert ['xingben', 'qingfeng'] == get_mentions_from_text(text4)
        assert ['xingben', 'qingfeng'] == get_mentions_from_text(text5)
        assert ['xingben', 'qingfeng', 'zhangchi'] == get_mentions_from_text(text6)
        assert [] == get_mentions_from_text(text7)

    def test_render_markdown_simple(self):
        t = 'aa'
        r = render_markdown(t).strip()
        assert r == '<p>aa</p>'

    def test_render_markdown_with_xss(self):
        t = '    <script>'
        r = render_markdown(t).strip()
        assert r == '<pre><code>&lt;script&gt;</code></pre>'

    def test_render_markdown_with_chinese(self):
        t = u'     牛B'
        r = render_markdown(t).strip()
        assert r == u'<pre><code>\u725bB</code></pre>'
