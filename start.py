import json
from datetime import datetime

from flask import Flask, send_file, render_template, request, redirect

from sqlite_manager import insert, select, update_value, \
    insert_if_not_exist

app = Flask(__name__)


@app.route('/counter', methods=['GET', 'POST'])
def counter():
    current_id = request.args.get('id')
    user_id = request.remote_addr
    update(current_id, user_id)
    return send_file('static/img/dot.png', attachment_filename='dot.png')


@app.route('/get_count', methods=['GET', 'POST'])
def get_count():
    current_id = request.args.get('id')
    all_count = select('counter', 'count', **{'id': current_id})[0][0]
    # unique_count = select('unique_visits', '*', **{})[0][0]
    json_file = json.dumps({'all_visits': all_count})
    #                        'unique_visits': unique_count})
    return json_file


def update(current_id, user_id):
    update_format = "\'{}\'".format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ip_format = "\'{}\'".format(user_id)
    insert_if_not_exist('counter', id=current_id)
    count = select('counter', 'count', id=current_id)[0][0]
    update_value('counter', ('count', count + 1), id=current_id)
    insert_if_not_exist('unique_visits', user=ip_format,
                        page_id=current_id)
    update_value('unique_visits', ('last_visit', update_format),
                 user=ip_format, page_id=current_id)


@app.route('/period', methods=['POST'])
def period():
    user_id = request.form['id']
    if user_id:
        return redirect(f'/get_count?id={user_id}')
    else:
        raise Exception('Incomplete input')


@app.route('/form', methods=['GET', 'POST'])
def my_form():
    return render_template('form.html')


@app.route('/first', methods=['POST'])
def first_test():
    return render_template('first.html')


@app.route('/second', methods=['POST'])
def second_test():
    return render_template('second.html')


if __name__ == 'main':
    app.run()
