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

from django.db import models
from markdown import markdown

from core.utils import format_publish_time
from .misc import Tag


class Article(models.Model):
    """Article model
    """
    # article id
    id = models.AutoField(
        db_column='id',
        primary_key=True,
        unique=True,
        verbose_name='ID'
    )
    # article title
    title = models.CharField(
        db_column='title',
        max_length=256,
        verbose_name='Title'
    )
    # markdown content
    md_content = models.TextField(
        db_column='md_content',
        null=False,
        blank=False,
        default=str(),
        verbose_name='Markdown Content'
    )
    # html content
    html_content = models.TextField(
        db_column='html_content',
        null=False,
        blank=False,
        default=str(),
        verbose_name='HTML Content',
        editable=False
    )
    # publish time
    publish_time = models.DateTimeField(
        db_column='publish_time',
        verbose_name='Publish Time'
    )
    # background music id of 163 music service
    bgm_id = models.CharField(
        db_column='bgm_id',
        null=True,
        blank=True,
        max_length=16,
        verbose_name='163 Music ID'
    )
    # tags
    tags = models.ManyToManyField(Tag, db_table='core_article_tag_relation', verbose_name='Tags')

    class Meta(object):
        db_table = 'core_article'

    def save(self, *args, **kwargs):
        self.html_content = markdown(self.md_content)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def to_dict(self, md_content=True, html_content=True, short_publish_time=False):
        md_content = md_content if isinstance(md_content, bool) else False
        html_content = html_content if isinstance(html_content, bool) else False
        data = {
            'content_type': 'article',
            'id': self.id,
            'title': self.title,
            'publish_time': self.publish_time.strftime('%Y-%m-%d %H:%M:%S'),
            'publish_time_display': format_publish_time(self.publish_time, short_publish_time),
            'bgm_id': self.bgm_id,
            'tags': [tag.to_dict() for tag in self.tags.all()]
        }
        if md_content:
            data['md_content'] = self.md_content
        if html_content:
            data['html_content'] = self.html_content
        return data
