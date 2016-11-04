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

import json
from json import dumps

from django.http import HttpResponse


def json_response(func):
    def wrapper_func(request):
        response = HttpResponse(content_type='application/json')
        response.write(dumps(func(request)))
        response.content_type = ''
        return response

    return wrapper_func


class JsonResponse(HttpResponse):
    def __init__(self, data=None, **kwargs):
        self.status_code = kwargs.get('status_code', 200)
        kwargs.setdefault('content_type', 'application/json')
        if not isinstance(data, dict) and not isinstance(data, list):
            data = {}
        data = json.dumps(data)
        super(JsonResponse, self).__init__(content=data, **kwargs)
