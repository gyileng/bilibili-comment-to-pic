# -*- coding: utf-8 -*-


class Result:
    def __init__(self):
        self._result = {}

    def set_code(self, code):
        self._result['code'] = code

    def set_msg(self, msg):
        self._result['msg'] = msg

    def set_data(self, data):
        self._result['data'] = data

    @property
    def result(self):
        return self._result


def from_exc(exc):
    r = Result()
    r.set_code(exc.code)
    r.set_msg(exc.msg)
    return r.result


def from_data(data):
    r = Result()
    r.set_data(data)
    return r.result
