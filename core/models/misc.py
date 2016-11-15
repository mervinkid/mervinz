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


class Tag(models.Model):
    id = models.AutoField(
        db_column='id',
        primary_key=True,
        unique=True,
        verbose_name='ID'
    )
    title = models.CharField(
        db_column='title',
        max_length=64,
        verbose_name='Title'
    )

    class Meta:
        db_table = 'core_tag'
        verbose_name_plural = 'Tag'

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'content_type': 'tag',
            'id': self.id,
            'title': self.title,
        }
