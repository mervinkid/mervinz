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

from django.contrib import admin

from core.models import Article, Tag, Friend, Career


def display_tags(obj):
    if not isinstance(obj, Article):
        return ''
    tags = obj.tags.all().order_by('id')
    return ', '.join([tag.title for tag in tags])


class BaseModelAdmin(admin.ModelAdmin):
    empty_value_display = 'N/A'


class ArticleAdmin(BaseModelAdmin):
    model = Article
    ordering = ['-publish_time']
    list_display = ['title', 'bgm_id', display_tags, 'publish_time']


class TagAdmin(BaseModelAdmin):
    model = Tag
    ordering = ['id']
    list_display = ['id', 'title']


class FriendAdmin(BaseModelAdmin):
    model = Friend


class CareerAdmin(BaseModelAdmin):
    model = Career
    ordering = ['-start']
    list_display = ['company', 'job', 'start', 'end']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(Career, CareerAdmin)
