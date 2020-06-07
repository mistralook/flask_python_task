import json
from collections import Counter
from sqlite_manager import select, select_for_days
from flask import Flask, make_response, send_file, request
from secrets import token_urlsafe
from utils import country_by_ip, update
from geoip2 import database

app = Flask(__name__)
reader = database.Reader('CountryDB/GeoLite2-Country.mmdb')


@app.route('/counter', methods=['GET'])
def counter():
    current_id = request.args.get('id')
    resp = make_response(send_file('img/1x1.png', cache_timeout=-1))
    cookie = request.cookies.get('some cookie')
    if cookie is None:
        cookie = token_urlsafe(5)
    update("BD.db", current_id, cookie)
    if cookie:
        resp.set_cookie('some cookie', str(cookie), max_age=1296000)
    return resp


@app.route('/get_count', methods=['GET'])
def get_count():
    country_visits = Counter()
    current_id = request.args.get('id')
    is_country_statistic = request.args.get('country')
    if is_country_statistic == '1':
        ip = select("BD.db", 'unique_visits', 'ip',
                    **{'id': current_id})
        for address in ip:
            country = country_by_ip(address[0], reader)
            country_visits[country] += 1
        return country_visits
    elif is_country_statistic == '0' or not is_country_statistic:
        all_count = select("BD.db", 'counter',
                           'count', **{'id   ': current_id})[0][0]
        unique_day = select_for_days("BD.db", '-1 day', current_id)
        unique_week = select_for_days("BD.db", '-6 days', current_id)
        unique_month = select_for_days("BD.db", '-30 days', current_id)
        json_file = json.dumps({'all_visits': all_count,
                                'unique_last_day': len(unique_day),
                                'unique_last_week': len(unique_week),
                                'unique_last_month': len(unique_month)})

        return json_file


if __name__ == '__main__':
    app.run()
