from flask import Flask
import click

app = Flask(__name__)

# 最小flask应用
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

# 在试图函数上绑定多个路由
@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'

# 动态路由
@app.route('/greet', defaults={'name':'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name

# 自定义flask命令
@app.cli.command()
def hello():
    click.echo('Hello, Human!')