# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2016 Mervin <mofei2816@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from pygments.formatters.html import HtmlFormatter
from mistune import Renderer


class BlogContentRenderer(Renderer):
    """
    Markdown renderer for article rich-text content.
    This renderer improve following features:
    - Syntax highlight for <code> block.
    - Lazy load of vue-lazyload library for <img> tag.
    """

    def __init__(self, **kwargs):
        super(BlogContentRenderer, self).__init__(**kwargs)

    def block_code(self, code, lang=None):
        if not lang:
            return super(BlogContentRenderer, self).block_code(code, lang)
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter(style='xcode')
            return highlight(code, lexer, formatter)
        except ClassNotFound:
            return super(BlogContentRenderer, self).block_code(code, lang)
