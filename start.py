import json
from sqlite_manager import insert, select, update_value
from flask import Flask, request, send_file

app = Flask(__name__)


@app.route('/counter')
def counter():
    current_id = request.args.get('id')
    update(current_id)
    return send_file('static/img/dot.png', attachment_filename='dot.png')


@app.route('/get_count')
def get_count():
    current_id = request.args.get('id')
    count = select(current_id)[0][0]
    json_file = json.dumps({current_id: count})
    with open('package.json', 'w') as file:
        file.write(json_file)
    return send_file('package.json')


def update(current_id):
    try:
        count = select(current_id)[0][0]
        update_value(current_id, count)
    except:
        insert(current_id, 1)
