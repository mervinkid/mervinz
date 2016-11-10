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

from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from core.services import get_articles, get_article, get_tags
from core.utils import JsonResponse, require_method


@cache_page(60 * 5)
@require_method('GET')
def home(request):
    return render(request, 'home.html', {
        'current': 'home',
        'tags': [tag.to_dict() for tag in get_tags()]
    })


@cache_page(60 * 5)
@require_method('GET')
def post(request):
    page_num = int(request.GET.get('page_num', 1))
    page_num = page_num if page_num > 0 else 1
    page_size = int(request.GET.get('page_size', 5))
    page_size = page_size if page_size > 0 else 5
    tag_id = int(request.GET.get('tag_id', 0))

    articles = get_articles(page_num, page_size, tag_id=(tag_id if tag_id != 0 else None))

    return JsonResponse(data={
        'success': True,
        'articles': [
            article.to_dict(
                md_content=False,
                html_content=False,
                preview_content=True,
                with_images=True,
                short_publish_time=True
            ) for article in articles
            ],
        'page_num': page_num if len(articles) != 0 else page_num - 1,
        'page_size': page_size
    })


@cache_page(60 * 15)
@require_method('GET')
def post_detail(request, article_id):
    article = get_article(article_id=int(article_id))

    if article is None:
        raise Http404()

    return render(request, 'post.html', {
        'current': 'home',
        'article': article.to_dict(md_content=False, preview_content=False, html_content=True)
    })


@cache_page(60 * 15)
@require_method('GET')
def about(request):
    return render(request, 'about.html', {
        'current': 'about'
    })


@cache_page(60 * 5)
@require_method('GET')
def search(request):
    keyword = request.GET.get('keyword', '')
    if not isinstance(keyword, str) or len(keyword.strip()) < 2:
        return JsonResponse(data={
            'success': True,
            'articles': []
        })

    articles = get_articles(1, 20, keyword=keyword)
    return JsonResponse(data={
        'success': True,
        'articles': [
            article.to_dict(
                md_content=False,
                html_content=False,
                preview_content=False,
                short_publish_time=True
            ) for article in articles
            ]
    })


@cache_page(60 * 15)
def handler404(request):
    response = render(request, 'error.html', {
        'error_title': 'Not Found',
        'error_message': 'It seems the page you are looking for have been taken away by aliens.'
    })
    response.status_code = 404
    return response


@cache_page(60 * 15)
def handler500(request):
    response = render(request, 'error.html', {
        'error_title': 'Error',
        'error_message': 'Is there any problem with my code? No, I do not admit! Never!'
    })
    response.status_code = 500
    return response


@cache_page(60 * 15)
def robots_txt(request):
    content = 'User-agent: *\n' \
              'Disallow: /admin/*\n' \
              'Sitemap: https://mervinz.me/sitemap.xml\n'
    response = HttpResponse()
    response.status_code = 200
    response.charset = 'utf-8'
    response['Content-Type'] = 'text/plain; charset=UTF-8'
    response.write(content.encode(encoding='utf-8'))
    return response
