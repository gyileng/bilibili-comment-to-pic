# -*- coding: utf-8 -*-

import json

import redis

from . import base


class Redis(base.DB):
    def __init__(self, **kwargs):
        """
        :param kwargs: {
            'url': '127.0.0.1:6379',
        }
        """
        self._client = redis.Redis.from_url(kwargs.get('url'))
        self._prefix = kwargs.get('prefix', None)

    @property
    def client(self):
        return self._client

    def get_prefix_key(self, key):
        if not self._prefix:
            return key
        return "|".join([self._prefix, key])

    def get(self, model_cls, key):
        prefix_key = self.get_prefix_key(model_cls.get_prefix_key(key))
        data = self._client.get(prefix_key)
        return json.loads(data) if data else None

    def put(self, model_cls, key, data, is_new=False):
        expire = model_cls._meta.cache_expire
        prefix_key = self.get_prefix_key(model_cls.get_prefix_key(key))
        self._client.set(prefix_key, json.dumps(data), expire)

    def delete(self, model_cls, key):
        prefix_key = self.get_prefix_key(model_cls.get_prefix_key(key))
        self._client.delete(prefix_key)
