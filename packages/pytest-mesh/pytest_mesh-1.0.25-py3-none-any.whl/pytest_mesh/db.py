#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
数据库相关

@author:zhaojiajun
@file:db.py
@time:2022/07/26
"""
import sqlalchemy
from sqlalchemy.orm import Session
import logging

log = logging.getLogger(__name__)


class MySqlDB:
    """
    通过SQLAlchemy 维护与mysql数据库的连接
    """

    def __init__(self, server: str, port: str, user: str, password: str, db: str):
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.engine = self.__init_engine()

    def __init_engine(self):
        """
        初始化目标数据库的连接

        :return:
        """
        log.info('初始化mysql数据库连接.')
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.server}:{self.port}/{self.db}'
        log.info('mysql连接地址：{}'.format(url))
        engine = sqlalchemy.create_engine(url, echo=True, future=True)
        log.info('mysql数据库连接成功.')
        return engine

    def execute(self, sql: str):
        """
        执行sql语句

        :param sql:语句
        :return:
        """
        with Session(self.engine) as session:
            result = session.execute(sql)
            return result


if __name__ == '__main__':
    pass
