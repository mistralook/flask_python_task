import sqlite3
import functools


def make_criteria(**kwargs) -> str:
    return " and ".join([f'{key} = {value}'
                         for key, value in kwargs.items()])


def sql_operations(func):
    @functools.wraps(func)
    def wrapper(table, *args, **kwargs):
        with sqlite3.connect("BD.db") as connection:
            cursor = connection.cursor()
            sql = func(table, *args, **kwargs)
            result = list(cursor.execute(sql))
            cursor.fetchall()
            cursor.close()
        return result

    return wrapper


@sql_operations
def select(table, *args, **kwargs):
    criteria = make_criteria(**kwargs)
    return f'SELECT {",".join(args)} FROM {table} WHERE {criteria}'


@sql_operations
def insert(table, **kwargs):
    insert_values = ','.join(map(str, kwargs.values()))
    return f"INSERT INTO {table} VALUES ({insert_values})"


@sql_operations
def update_value(table, setter: tuple, **kwargs):
    cr = make_criteria(**kwargs)
    return f"UPDATE {table} SET {setter[0]}={setter[1]} WHERE {cr}"


@sql_operations
def insert_if_not_exist(table, **kwargs):
    cr = make_criteria(**kwargs)
    return f"""INSERT INTO {table} ({', '.join(kwargs.keys())})
            SELECT {', '.join([f'{v} as {k}' for k,  v in kwargs.items()])}
            FROM {table} WHERE NOT EXISTS(SELECT * FROM {table} 
            WHERE {cr}) LIMIT 1;"""

