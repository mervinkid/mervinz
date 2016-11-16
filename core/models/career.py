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


class Career(models.Model):
    id = models.AutoField(
        db_column='id',
        primary_key=True,
        unique=True,
        verbose_name='ID'
    )

    start = models.DateField(
        db_column='start',
        blank=False,
        null=False,
        verbose_name='Start'
    )

    end = models.DateField(
        db_column='end',
        blank=True,
        null=True,
        verbose_name='End'
    )

    company = models.CharField(
        db_column='company',
        max_length=128,
        null=False,
        blank=False,
        verbose_name='Company'
    )

    desc = models.TextField(
        db_column='desc',
        null=False,
        blank=False,
        verbose_name='Desc'
    )

    job = models.CharField(
        db_column='job',
        max_length=128,
        blank=False,
        null=False,
        verbose_name='Job'
    )

    class Meta:
        db_table = 'core_career'
        verbose_name_plural = 'Career'

    def to_dict(self):
        start = '%s.%s' % \
                (self.start.year, str(self.start.month) if self.start.month >= 10 else '0%d' % self.start.month)
        end = '%s.%s' % \
              (self.start.year, str(self.start.month) if self.start.month >= 10 else '0%d' % self.start.month) \
            if self.end is not None else 'Now'
        return {
            'content_type': 'career',
            'id': self.id,
            'company': self.company,
            'jobs': [job.strip() for job in str(self.job).split(',')],
            'start': start,
            'end': end,
            'desc': self.desc
        }

    def __str__(self):
        return self.company
