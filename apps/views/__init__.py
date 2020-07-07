# -*- coding: utf-8 -*-
import functools

from flask import jsonify


def api_decorator(func):
    setattr(func, 'methods', ('POST', 'GET'))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wf = func
        for f in [][::-1]:
            wf = f(wf)
        data = wf(*args, **kwargs)
        return jsonify(data)

    return wrapper
