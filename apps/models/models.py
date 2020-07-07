# -*- coding: utf-8 -*-

import hashlib

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    token = Column(String(255))
    token_expire = Column(DateTime)
    created = Column(DateTime, server_default=text('NOW()'))
    authorization = Column(Text)

    @staticmethod
    def generate_password(password):
        return hashlib.md5(('sI+#!-ml%se' % password).encode()).hexdigest()
