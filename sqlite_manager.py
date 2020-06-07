import sqlite3
import functools


def make_criteria(**kwargs) -> str:
    return " and ".join([f'{key} = {value}'
                         for key, value in kwargs.items()])


def sql_operations(func):
    @functools.wraps(func)
    def wrapper(db_name, table, *args, **kwargs):
        with sqlite3.connect(db_name) as connection:
            cursor = connection.cursor()
            sql = func(db_name, table, *args, **kwargs)
            result = list(cursor.execute(sql))
            cursor.fetchall()
            cursor.close()
        return result

    return wrapper


@sql_operations
def select(db, table, *args, **kwargs):
    criteria = make_criteria(**kwargs)
    return f'SELECT {",".join(args)} FROM {table} WHERE {criteria}'


@sql_operations
def update_value(db, table, setter: tuple, **kwargs):
    cr = make_criteria(**kwargs)
    return f"UPDATE {table} SET {setter[0]}={setter[1]} WHERE {cr}"


@sql_operations
def insert_if_not_exist(db, table, **kwargs):
    cr = make_criteria(**kwargs)
    return f"""INSERT INTO {table} ({', '.join(kwargs.keys())})
    SELECT {', '.join([f'{v} as {k}' for k, v in kwargs.items()])}
    FROM {table} WHERE NOT EXISTS(SELECT * FROM {table} WHERE {cr})
    LIMIT 1;"""


@sql_operations
def select_for_days(db, period, page):
    return f"""SELECT * FROM unique_visits
    WHERE last_visit BETWEEN datetime('now', '{period}')
    AND datetime('now', 'localtime') AND id = '{page}';"""
