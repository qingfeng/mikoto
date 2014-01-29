from unittest import TestCase
from mikoto.libs.text import render


class TestMarkdown(TestCase):
    def test_tasklist(self):
        md = '''
- [x] this is a complete item
- [ ] this is an incomplete item
'''
        html = '''
<ul>
<li><label><input type="checkbox" data-item-index="0" checked> this is a complete item</label></li>
<li><label><input type="checkbox" data-item-index="1"> this is an incomplete item</label></li>
</ul>
'''
        result = render(md)

        result = result.replace('\n', '')
        html = html.replace('\n', '')
        assert result == html

        # test markdown text without newline at end
        md_wo_n = '''
- [x] this is a complete item
- [ ] this is an incomplete item'''
        result = render(md_wo_n)
        result = result.replace('\n', '')
        html = html.replace('\n', '')
        assert result == html

    def test_linebreak(self):
        text = 'hello\nworld'
        html = u'<p>hello<br>\nworld</p>'
        result = render(text).strip()
        assert result == html

    def test_autolink(self):
        text = 'this a link: http://code.dapps.douban.com/'
        html = u'<p>this a link: <a href="http://code.dapps.douban.com/">http://code.dapps.douban.com/</a></p>'
        result = render(text).strip()
        assert result == html

    def test_image_link(self):
        text = '![](http://p.dapps.douban.com/i/800482eec53311e2ac7e24b6fdf6fbfc.png)'
        html = u'<p><img src="http://p.dapps.douban.com/i/800482eec53311e2ac7e24b6fdf6fbfc.png" alt=""></p>'
        result = render(text).strip()
        assert result == html

    def test_html_escape(self):
        text = "this a script: \n<script>alert('hi')</script>\n<style>body{color:red}</style>"
        html = u'''<p>this a script: <br>
&lt;script&gt;alert(&#39;hi&#39;)&lt;/script&gt;<br>
&lt;style&gt;body{color:red}&lt;/style&gt;</p>'''
        result = render(text).strip()
        assert result == html

    def test_html_table(self):
        text = '''
<table>
<tr>
<td>cell1</td>
<td>cell2</td>
</tr>
</table>
'''
        html = u'''
<p>&lt;table&gt;<br>
&lt;tr&gt;<br>
&lt;td&gt;cell1&lt;/td&gt;<br>
&lt;td&gt;cell2&lt;/td&gt;<br>
&lt;/tr&gt;<br>
&lt;/table&gt;</p>
'''.strip()
        result = render(text).strip()
        assert result == html

    def test_markdown_table(self):
        text = '''
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
'''
        html = u'''
<table><thead>
<tr>
<th>First Header</th>
<th>Second Header</th>
</tr>
</thead><tbody>
<tr>
<td>Content Cell</td>
<td>Content Cell</td>
</tr>
<tr>
<td>Content Cell</td>
<td>Content Cell</td>
</tr>
</tbody></table>
'''.strip()
        result = render(text).strip()
        assert result == html

    def test_script_escape(self):
        text = "<script>alert('hi')</script>"
        html = u"<p>&lt;script&gt;alert(&#39;hi&#39;)&lt;/script&gt;</p>"
        result = render(text).strip()
        assert result == html

    def test_fix_h2_bug(self):
        text = '''## H2
## H2_2
'''
        html = u"<h2>H2</h2><h2>H2_2</h2>"
        result = render(text).strip()
        assert result == html

    def test_fix_email(self):
        text = '''
to sa@douban.com send email @abc
@abc hello
'''
        # TODO have problems
        html = u'''<p>to <a href="mailto:sa@douban.com">sa@douban.com</a> send email \
<a href="/people/abc/" class="user-mention">@abc</a><br>
<a href="/people/abc/" class="user-mention">@abc</a> hello</p>'''
        result = render(text).strip()
        assert result == html

    def test_commit_url(self):
        text = 'commit 9ebcb3c a6ac123 traceback'
        html = u'<p>commit <a href="/code/commit/9ebcb3c">9ebcb3c</a> \
<a href="/code/commit/a6ac123">a6ac123</a> traceback</p>'
        result = render(text, project_name='code').strip()
        assert result == html

    def test_image_url(self):
        text = '![](http://p.dapps.douban.com/i/800482eec53311e2ac7e24b6fdf6fbfc.png)'
        html = u'<p><img src="http://p.dapps.douban.com/i/800482eec53311e2ac7e24b6fdf6fbfc.png" alt=""></p>'
        result = render(text, project_name='code').strip()
        assert result == html

    def test_render_user_links(self):
        t = '@qingfeng pls, review cc @hongqn & @huanghuang'
        r = render(t).strip()
        assert r == u'<p><a href="/people/qingfeng/" class="user-mention">@qingfeng</a> \
pls, review cc <a href="/people/hongqn/" class="user-mention">@hongqn</a> &amp; \
<a href="/people/huanghuang/" class="user-mention">@huanghuang</a></p>'

    def test_render_user_and_image(self):
        t = '@qingfeng ![ScreenShot](http://p.dapps.douban.com/i/800482eec53311e2ac7e24b6fdf6fbfc.png)'
        html = u'<p><a href="/people/qingfeng/" class="user-mention">@qingfeng</a> \
<img src="http://p.dapps.douban.com/i/800482eec53311e2ac7e24b6fdf6fbfc.png" alt="ScreenShot"></p>'
        r = render(t).strip()
        assert r == html

    def test_render_code_format(self):
        text = '''@qingfeng `hello @xutao`

    import this
    @qingfeng
'''
        html = u'''<p><a href="/people/qingfeng/" class="user-mention">@qingfeng</a> <code>hello &#64;xutao</code></p>

<pre><code>import this
&#64;qingfeng</code></pre>'''
        result = render(text).strip()
        assert result == html

    def test_render_local_image(self):
        text = '![](Images/screenshot_004.png)'
        html = u'<p><img src="/code/raw/master/Images/screenshot_004.png" alt=""></p>'
        r = render(text, project_name="code").strip()
        assert r == html

    def test_link_and_image(self):
        text = '[![](Images/screenshot_004.png)](Images/screenshot_004.png)'
        html = u'<p><a href="/code/raw/master/Images/screenshot_004.png" title="">\
<img src="/code/raw/master/Images/screenshot_004.png" alt=""></a></p>'
        r = render(text, project_name="code").strip()
        assert r == html
