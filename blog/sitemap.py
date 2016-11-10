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

from datetime import datetime
from django.contrib.sitemaps import Sitemap
from django.db import connection
from django.urls import reverse

from . import views


class BlogSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        sql = 'SELECT core_article.id, core_article.publish_time ' \
              'FROM core_article AS core_article ' \
              'ORDER BY core_article.publish_time DESC '
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        return rows

    def lastmod(self, obj):
        return obj[1]

    def location(self, obj):
        return '/post/%d' % obj[0]


class StaticSitemap(Sitemap):
    changefreq = 'month'
    priority = 0.5

    def items(self):
        return [views.about]

    def lastmod(self, obj):
        return datetime.now()

    def location(self, item):
        return reverse(item)
