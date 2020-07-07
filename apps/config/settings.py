# -*- coding: utf-8 -*-

DEBUG = False
SECRET_KEY = '2342'

CORE = {
    'tzone': 'Asia/Shanghai',
    'engine': {
        'db': {
            'class': 'apps.kv.db.MySQLConsistent',
            'config': {
                'default_config': {
                    'pool_size': 32,
                    'echo': True,
                    'pool_recycle': 3600,
                    # 'echo_pool': True,
                },
                'mysql': {
                    'url': 'mysql+pymysql://root:123456@127.0.0.1:3306/zhijian?charset=utf8mb4'
                },
            }
        },
        'cache': {
            'class': 'apps.kv.db.Redis',
            'config': {
                'url': 'redis://127.0.0.1:6379',
                'prefix': 'caffe-web',
            }
        },
    },
}