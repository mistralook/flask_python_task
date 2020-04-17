import json, sqlite3
from sqlite_manager import insert, select, update_value
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/counter')
def counter():
    id = request.args.get('id')
    update(id)


@app.route('/get_count')
def get_count():
    return True


def update(id):
    try:
        count = select(id)[0][0]
        update_value(id, count)
    except:
        insert(id, 1)
