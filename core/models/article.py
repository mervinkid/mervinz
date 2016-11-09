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
from mistune import markdown
from bs4 import BeautifulSoup

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
        default='',
        verbose_name='Markdown'
    )
    # html content
    html_content = models.TextField(
        db_column='html_content',
        null=False,
        blank=False,
        default='',
        verbose_name='HTML',
        editable=False
    )
    # preview content
    preview_content = models.CharField(
        db_column='preview_content',
        max_length=1024,
        null=False,
        blank=False,
        default='',
        verbose_name='Preview',
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
    tags = models.ManyToManyField(
        Tag,
        db_table='core_article_tag_relation',
        verbose_name='Tags'
    )

    class Meta(object):
        db_table = 'core_article'

    def save(self, *args, **kwargs):
        # markdown to html
        self.html_content = markdown(self.md_content)
        # preview content
        bs = BeautifulSoup(self.html_content, 'html.parser')
        p_list = bs.find_all('p')
        preview = ''
        preview_len = 0
        preview_paragraph = 0
        for p_item in p_list:
            p_item_string_len = len(p_item.string.strip()) if isinstance(p_item.string, str) else 0
            if p_item_string_len > 0:
                preview += str(p_item)
                preview_len += p_item_string_len
                preview_paragraph += 1
            if preview_len > 200 or preview_paragraph >= 5:
                break
        self.preview_content = preview
        super(Article, self).save(*args, **kwargs)
        # process images
        # clear old image data
        article_images = ArticleImage.objects.filter(article=self)
        for article_image in article_images:
            article_image.delete()
        # write new data
        img_list = bs.find_all('img')
        for img_item in img_list:
            src = img_item.get('src')
            if not isinstance(src, str) or len(src.strip()) == 0:
                continue
            article_image = ArticleImage(url=src, publish_time=self.publish_time, article=self)
            article_image.save()

    def __str__(self):
        return self.title

    def to_dict(self, preview_content=True, md_content=True, html_content=True, short_publish_time=False,
                with_images=False, max_images=3):
        preview_content = preview_content if isinstance(preview_content, bool) else False
        md_content = md_content if isinstance(md_content, bool) else False
        html_content = html_content if isinstance(html_content, bool) else False
        with_images = with_images if isinstance(with_images, bool) else False
        max_images = max_images if isinstance(max_images, int) else 3
        data = {
            'content_type': 'article',
            'id': self.id,
            'title': self.title,
            'publish_time': self.publish_time.strftime('%Y-%m-%d %H:%M:%S'),
            'publish_time_display': format_publish_time(self.publish_time, short_publish_time),
            'bgm_id': self.bgm_id,
            'tags': [tag.to_dict() for tag in self.tags.all()]
        }
        if preview_content:
            data['preview_content'] = self.preview_content
        if md_content:
            data['md_content'] = self.md_content
        if html_content:
            data['html_content'] = self.html_content
        if with_images:
            data['images'] = [image.to_dict() for image in list(self.images.all().order_by('id')[0:max_images])]
        return data


class ArticleImage(models.Model):
    # id
    id = models.AutoField(
        db_column='id',
        primary_key=True,
        unique=True
    )
    # article
    article = models.ForeignKey(
        Article,
        db_column='article_id',
        related_name='images'
    )
    # url
    url = models.CharField(
        db_column='url',
        max_length=256
    )
    # publish time
    publish_time = models.DateTimeField(
        db_column='publish_time'
    )

    class Meta:
        db_table = 'core_article_image'

    def to_dict(self):
        return {
            'content_type': 'image',
            'id': self.id,
            'url': self.url
        }
