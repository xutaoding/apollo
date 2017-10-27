# -*- coding: utf-8 -*-
from datetime import datetime

import peewee
from playhouse.db_url import connect

import settings

# from peewee import MySQLDatabase
# mysql_db = MySQLDatabase(**flight.settings.MYSQL_CONFIG)
db_url = 'mysql+pool://{user}:{password}@{host}:{port}/{database}?' \
         'charset={charset}&max_connections=20&stale_timeout=600'
mysql_db = connect(db_url.format(**settings.MYSQL_CONFIG))


class BaseModel(peewee.Model):
    crt = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = mysql_db

    @classmethod
    def fields(cls):
        # The following methods could obtain models all fields:
        # 1. Fly._meta.fields.keys()
        # 2. Fly._meta.columns.keys()

        return cls._meta.sorted_field_names

    def create(self):
        self.save(force_insert=True)
        self._prepare_instance()
        return self

    @classmethod
    def query(cls, *dq, **query):
        if not dq and not query:
            return cls.select()

        return cls.filter(*dq, **query)

    @classmethod
    def get(cls, *query, **kwargs):
        try:
            return super(BaseModel, cls).get(*query, **kwargs)
        except cls.DoesNotExist:
            pass

        return None

    def update_self(self):
        return self.save()

    @classmethod
    def update_all(cls, expressions, __data=None, **update):
        """ So far not use """
        q = super(BaseModel, cls).update(__data, **update).where(*expressions)
        return q.execute()

    @classmethod
    def delete(cls, *query):
        q = super(BaseModel, cls).delete().where(*query)
        return q.execute()

    @classmethod
    def execute_raw_sql(cls, sql, *params):
        """ Not work """
        return cls.raw(sql, *params)


class MiddleFile(BaseModel):
    username = peewee.CharField(max_length=20)
    spider_task_id = peewee.UUIDField(unique=True)
    url = peewee.CharField(max_length=256)
    filename = peewee.CharField(unique=True, max_length=128)
    ext = peewee.CharField(max_length=8, default='.html')
    file_utility = peewee.CharField(max_length=2)

    class Meta:
        db_table = 'aegis_middle_file'


if __name__ == '__main__':
    for row in MiddleFile.query():
        print row.username


