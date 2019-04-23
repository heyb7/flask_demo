from flask import Flask, render_template, flash, url_for, redirect, request
from forms import LoginForm, FortyTwoForm, UploadForm

app = Flask(__name__)

app.secret_key = 'secret string'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
    # if request.method == 'POST': # and form.validate():
        username = form.username.data
        print('username:%s' % username)
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    
    return render_template('basic.html', form=form)


@app.route('/coustom-validator', methods=['GET', 'POST'])
def custome_validator():
    form = FortyTwoForm()

    if form.validate_on_submit():
        flash('Bingo')
        return redirect(url_for('index'))
    
    return render_template('custom_validator.html', form=form)


@app.route('/upload', methods=['GET','POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        pass

    return render_template('upload.html', form=form)