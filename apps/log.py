# -*- coding: utf-8 -*-

import logging

from flask import request

_logger = logging.getLogger('game_server')


def extra():
    data = {}
    if request and hasattr(request, 'id'):
        data['request_id'] = request.id
    return data


def log(level, msg, *args, **kwargs):
    e = kwargs.get('extra', {})
    e.update(extra())
    kwargs['extra'] = e
    _logger.log(level, msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    e = kwargs.get('extra', {})
    e.update(extra())
    kwargs['extra'] = e
    _logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    e = kwargs.get('extra', {})
    e.update(extra())
    kwargs['extra'] = e
    _logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    e = kwargs.get('extra', {})
    e.update(extra())
    kwargs['extra'] = e
    _logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    e = kwargs.get('extra', {})
    e.update(extra())
    kwargs['extra'] = e
    _logger.error(msg, *args, **kwargs)
