# -*- coding: utf-8 -*-

import werkzeug.utils


class Engine:
    def __init__(self, **kwargs):
        self._db = None
        self._cache = None

        db_cls = werkzeug.utils.import_string(kwargs['db']['class'])
        self._db = db_cls(**kwargs['db']['config'])

        cache_cls = werkzeug.utils.import_string(kwargs['cache']['class'])
        self._cache = cache_cls(**kwargs['cache']['config'])

    @property
    def db(self):
        return self._db

    @property
    def cache(self):
        return self._cache
