from flask import Flask, render_template, flash, url_for, redirect, request
from forms import LoginForm

app = Flask(__name__)

app.secret_key = 'secret string'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    # if form.validate_on_submit():
    if request.method == 'POST': # and form.validate():
        username = form.username.data
        print('username:%s' % username)
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    print('xxxx')
    return render_template('basic.html', form=form)