# -*- coding: utf-8 -*-

engine_kv = None

def init(**kwargs):
    _init_engine(**kwargs['engine'])


def _init_engine(**kwargs):
    from apps.kv.engine import Engine
    global engine_kv
    engine_kv = Engine(**kwargs)
