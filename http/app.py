import json
import os

from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import abort
from flask import make_response
from flask import jsonify
from flask import session

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'secret string')

@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Flask')
        response = '<h1>Hello, %s!</h1>' % name
        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
    return response

@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to %d!</p>' % (2018 - year)

@app.route('/colors/<any(blue, white, red):color>')
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'

@app.route('/hi')
def hi():
    return redirect(url_for('hello'))

@app.route('/404')
def no_found():
    abort(404)

@app.route('/note', defaults={'content_type':'text'})
@app.route('/note/<content_type>')
def note(content_type):
    content_type = content_type.lower()

    if content_type == 'text':
        body = ''' 
            Note
            to: Peter
            from: Jane
            heading: Reminder
            body: Don't forget the party!
        '''

        response = make_response(body)
        response.mimetype = 'text/plain'
    
    elif content_type == 'html':
        body = '''
            <!DOCTYPE html>
            <html>
            <head></head>
            <body>
                <h1>Note</h1>
                <p>to: Peter</p>
                <p>from: Jane</p>
                <p>heading: Reminder</p>
                <p>body: <strong>Don't forget the party!</strong></p>
            </body>
            </html>
        '''

        response = make_response(body)
        response.mimetype = 'text/html'

    elif content_type == 'xml':
        body = '''<?xml version="1.0" encoding="UTF-8"?>
            <note>
                <to>Peter</to>
                <from>Jane</from>
                <heading>Reminder</heading>
                <body>Don't forget the party!</body>
            </note> 
        '''

        response = make_response(body)
        response.mimetype = 'application/xml'

    elif content_type == 'json':
        body = {
            "note":{
                "to": "Peter",
                "from": "Jane",
                "heading": "Reminder",
                "body": "Don't forget the party!"
            },
        }

        response = jsonify(body)
        # equal to:
        # response = make_response(json.dumps(body))
        # response.mimetype = 'application/json'

    else:
        abort(400)

    return response

@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response

@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page'

@app.route('/login')
def login():
    session['logged_in'] = True # 写入session，并使用secret_key加密
    return redirect(url_for('hello'))

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))

@app.route('/foo')
def foo():
    return '<h1>Foo page</h1> <a href="%s">Do something</a>' % url_for('do_something', next=request.full_path)

@app.route('/bar')
def bar():
    return '<h1>Bar page</h1> <a href="%s">Do something</a>' % url_for('do_something', next=request.full_path)

@app.route('/do_something')
def do_something():
    return redirect_back()


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if target:
            return redirect(target)
    return redirect(url_for(default, **kwargs))