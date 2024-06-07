import psycopg
import os
import inspect

from .types import Column


class DBPostgreSQL:

    def __init__(self, host: str,  dbname: str, user: str, password: str):
        self.__host = host
        self.__dbname = dbname
        self.__user = user
        self.__password = password
        self.__conninfo = psycopg.conninfo.make_conninfo(
            host=self.__host,
            dbname=self.__dbname,
            user=self.__user,
            password=self.__password
        )

    def execute(self, query: str):
        with psycopg.connect(self.__conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

    def create_table(self, table_name: str, **columns: Column):
        with psycopg.connect(self.__conninfo) as conn:
            with conn.cursor() as cur:
                query = (
                    f'CREATE TABLE IF NOT EXISTS {table_name} '
                    f'({", ".join([
                        f"{name} {column.type} {column.constraint.value}" for name, column in columns.items()
                    ])})'
                )
                cur.execute(query)

    def add_row(self, table_name: str, **kwargs):

        with psycopg.connect(self.__conninfo) as conn:
            with conn.cursor() as cur:

                if existing := self.get_row(table_name, **kwargs):
                    return existing[0]

                query = (
                    f'INSERT INTO {table_name} ({", ".join(kwargs.keys())}) VALUES '
                    f'({", ".join([
                        f"'{value}'" for value in kwargs.values()
                    ])}) '
                )
                query += 'RETURNING *'
                cur.execute(query)
                return cur.fetchone()[0]

    def get_all(self, table_name: str):
        with psycopg.connect(self.__conninfo) as conn:
            with conn.cursor() as cur:
                query = f'SELECT * FROM {table_name}'
                cur.execute(query)
                return cur.fetchall()

    def get_row(self, table_name: str, **kwargs):
        with psycopg.connect(self.__conninfo) as conn:
            with conn.cursor() as cur:
                query = (
                    f'SELECT * FROM {table_name} WHERE '
                    f'{" AND ".join([f"{key} = '{value}'" for key, value in kwargs.items()])}'
                )
                cur.execute(query)
                return cur.fetchone()

    def get_rows(self, table_name: str, **kwargs):
        with psycopg.connect(self.__conninfo) as conn:
            with conn.cursor() as cur:
                query = (
                    f'SELECT * FROM {table_name} WHERE '
                    f'{" AND ".join([f"{key} = '{value}'" for key, value in kwargs.items()])}'
                )
                cur.execute(query)
                return cur.fetchall()

    def delete_rows(self, table_name: str, **kwargs):
        with psycopg.connect(self.__conninfo) as conn:
            with conn.cursor() as cur:
                query = (
                    f'DELETE FROM {table_name} CASCADE WHERE '
                    f'{" AND ".join([f"{key} = '{value}'" for key, value in kwargs.items()])}'
                )
                cur.execute(query)

    def delete_all(self, table_name: str):
        with psycopg.connect(self.__conninfo) as conn:
            with conn.cursor() as cur:
                query = f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE '
                cur.execute(query)


def get_db():
    return DBPostgreSQL(
        host=os.getenv('HOST'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('USER_NAME'),
        password=os.getenv('PASSWORD')
    )


def init_db():
    import models
    db = get_db()

    for name, obj in inspect.getmembers(models):
        if inspect.isclass(obj):
            attrs = {
                attr: value for attr, value in obj.__dict__.items() if not attr.startswith('_')
            }
            db.create_table(name, **attrs)

    return db
