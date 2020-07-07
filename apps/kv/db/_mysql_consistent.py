# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.dialects.mysql import insert

from . import base


class MySQLConsistent(base.DB):
    _tables = {}

    def __init__(self, **kwargs):
        """
        :param kwargs: {
            'mysql': {
                'url': 'mysql+pymysql://root:@127.0.0.1:3306/project_m_game_master?charset=utf8mb4'
            },
        }
        """
        master_cfg = {}
        master_cfg.update(kwargs.get('default_config', {}))
        master_cfg.update(kwargs.get('mysql', {}))
        self._master_client = sqlalchemy.engine_from_config(master_cfg, prefix='')

    @property
    def master_client(self):
        return self._master_client

    def get_master_connection(self):
        return self._master_client.connect()

    def master_execute(self, sqlobject, *multiparams, **params):
        conn = self.get_master_connection()
        try:
            return conn.execute(sqlobject, *multiparams, **params)
        finally:
            conn.close()

    def master_get_all(self, model_cls):
        conn = self.get_master_connection()
        table = self.get_table(model_cls._meta.table_name)
        try:
            rows = {}
            for row in conn.execute(sqlalchemy.select([table])):
                rows[row[0]] = row[1]
            return rows
        except Exception as e:
            raise e
        finally:
            conn.close()

    @classmethod
    def get_table(cls, name):
        if name not in cls._tables:
            cls._tables[name] = sqlalchemy.Table(
                name, sqlalchemy.MetaData(),
                sqlalchemy.Column('key', sqlalchemy.String(255), primary_key=True),
                sqlalchemy.Column('value', sqlalchemy.JSON)
            )
        return cls._tables[name]

    def get_connection_info(self, model_cls, key):
        table_name = model_cls._meta.table_name
        conn = self.get_master_connection()
        table = self.get_table(table_name)
        return conn, table

    def get(self, model_cls, key):
        return self._select(model_cls, key)

    def put(self, model_cls, key, data, is_new=False):
        self._on_duplicate_key_update(model_cls, key, data)

    def delete(self, model_cls, pkey):
        pass

    def _select(self, model_cls, key):
        conn, table = self.get_connection_info(model_cls, key)
        try:
            result = conn.execute(sqlalchemy.select([table]).where(table.c.key == key))
            rows = [dict(zip(result.keys(), row)) for row in result]
            return rows[0]['value'] if rows else None
        except Exception as e:
            raise e
        finally:
            conn.close()

    def _on_duplicate_key_update(self, model_cls, key, data):
        conn, table = self.get_connection_info(model_cls, key)
        try:
            insert_stmt = insert(table).values(key=key, value=data)
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(value=insert_stmt.inserted.value)
            conn.execute(on_duplicate_key_stmt)
        except Exception as e:
            raise e
        finally:
            conn.close()
