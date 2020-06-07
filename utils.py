from flask import request
from sqlite_manager import insert_if_not_exist, select, update_value
from datetime import datetime


def update(db, current_id, user_id):
    ip = request.remote_addr
    update_format = "'{}'".format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cookie = "'{}'".format(user_id)
    ip_format = "'{}'".format(ip)
    insert_if_not_exist(db, 'counter', id=current_id)
    count = select(db, 'counter', 'count', id=current_id)[0][0]
    update_value(db, 'counter', ('count', count + 1), id=current_id)
    insert_if_not_exist(db, 'unique_visits', user=cookie,
                        id=current_id, ip=ip_format)
    update_value(db, 'unique_visits', ('last_visit', update_format),
                 user=cookie, id=current_id, ip=ip_format)


def country_by_ip(ip, reader):
    try:
        response = reader.country(f'{ip}')
    except Exception:
        return 'Unknown'
    country = response.country.name
    return country
