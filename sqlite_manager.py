import sqlite3


def select(id):
    with sqlite3.connect('BD.db') as connection:
        sql = f'SELECT count FROM counter WHERE id={id}'
        print(sql)
        cursor = connection.cursor()
        result = list(cursor.execute(sql))
        cursor.fetchall()
        cursor.close()
    return result


def insert(id=None, counter=None):
    if not id and not counter:
        sql = f'INSERT INTO counter DEFAULT VALUES'
    else:
        sql = f'INSERT INTO counter VALUES ({id}, {counter})'
    with sqlite3.connect('BD.db') as connection:
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.fetchall()
        cursor.close()


def update_value(id=None, count=None):
    with sqlite3.connect('BD.db') as connection:
        update = f'UPDATE counter SET count = {count + 1} WHERE id = {id}'
        cursor = connection.cursor()
        cursor.execute(update)
        cursor.fetchall()
        cursor.close()