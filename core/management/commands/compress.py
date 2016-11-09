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

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
from css_html_js_minify.minify import prepare, process_single_css_file, process_single_js_file


class Command(BaseCommand):
    help = 'Compress .js and .css files in %s.' % settings.STATIC_ROOT

    def handle(self, *args, **options):
        prepare()
        self.scan_dir(path=settings.STATIC_ROOT, compress=True)

    def scan_dir(self, path, compress=False):
        if not isinstance(path, str) or not os.path.exists(path):
            return
        compress = compress if isinstance(compress, bool) else False
        dir_items = os.listdir(path=path)
        for dir_item in dir_items:
            item_path = os.path.join(path, dir_item)
            if os.path.isdir(item_path):
                self.scan_dir(item_path, compress)
                continue
            item_name_blocks = dir_item.split('.')
            if len(item_name_blocks) < 2:
                continue
            typename = str(item_name_blocks[-1]).lower()
            if typename == 'js':
                process_single_js_file(item_path, overwrite=True)
                print('compressed js : %s' % item_path)
            if typename == 'css':
                process_single_css_file(item_path, overwrite=True)
                print('compressed css: %s' % item_path)
