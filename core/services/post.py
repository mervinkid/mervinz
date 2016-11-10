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

from django.db.models import Q

from core.models import Article, Tag


def get_articles(page=1, count=5, keyword=None, tag_id=None):
    """Get articles
    :param page:
    :param count:
    :param keyword:
    :param tag_id:
    :return:
    """
    # validate arguments
    if not isinstance(page, int):
        raise TypeError('page must be an int value.')
    if not isinstance(count, int):
        raise TypeError('count must be an int value.')
    if keyword is not None and not isinstance(keyword, str):
        keyword = None
    if tag_id is not None and not isinstance(tag_id, int):
        tag_id = None

    page = 1 if page < 1 else page
    count = 5 if count < 1 else count

    q = Article.objects.all()
    if keyword is not None:
        # split keyword
        for word in keyword.split(' '):
            q = q.filter(Q(title__icontains=word) | Q(html_content__icontains=word))
    if tag_id is not None:
        q = q.filter(Q(tags=tag_id))
    q = q.order_by('-publish_time')
    q = q[(page - 1) * count:(page - 1) * count + count]

    return list(q)


def get_article(article_id):
    """Get specified article data
    :param article_id:
    :return:
    """
    # validate arguments
    if not isinstance(article_id, int):
        raise TypeError('article_id must be an int value.')

    # load article data
    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        return None

    return article


def get_tags(count=2):
    """Get all tags
    :return:
    """
    if not isinstance(count, int):
        count = 2
    tags = Tag.objects.all().order_by('id')[0:count]
    return list(tags)
