# -*- coding: utf-8 -*-
import traceback

import flask
import werkzeug.utils

from apps import core
from apps import log


def error_handler(exc):
    log.error(''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
    raise exc


def register_blueprints(new_app, path):
    for name in werkzeug.utils.find_modules(path):
        m = werkzeug.utils.import_string(name)
        new_app.register_blueprint(m.bp)
        # m.bp.errorhandler(common.CodeException)(exception.handler)
        # m.bp.errorhandler(Exception)(error_handler)
    # new_app.errorhandler(common.CodeException)(exception.handler)
    # new_app.errorhandler(Exception)(error_handler)
    return new_app


def register_middlewares(new_app, path, middlewares):
    for name in middlewares:
        m = werkzeug.utils.import_string('%s.%s' % (path, name))
        before_request = getattr(m, 'before_request', None)
        after_request = getattr(m, 'after_request', None)
        teardown_request = getattr(m, 'teardown_request', None)
        if before_request:
            new_app.before_request(before_request)
        if after_request:
            new_app.after_request(after_request)
        if teardown_request:
            new_app.teardown_request(teardown_request)
    return new_app


def create_app():
    # 初始化app
    new_app = flask.Flask(__name__)
    # 加载配置文件
    new_app.config.from_pyfile('config/settings.py')
    # 注册蓝图
    register_blueprints(new_app, 'apps.views')
    # 注册中间件
    register_middlewares(new_app, 'apps.middlewares', [])
    cfg = new_app.config
    core.init(**cfg['CORE'])
    return new_app


app = create_app()
