from flask import Flask, render_template, flash, url_for, redirect, request, session, \
     send_from_directory
from forms import LoginForm, FortyTwoForm, UploadForm, RichTextForm
from flask_ckeditor import CKEditor, upload_success, upload_fail

import os
import uuid

app = Flask(__name__)

app.secret_key = 'secret string'

# 自定义config
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')

# flask config
# set request body's max length
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024 # 3Mb

app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload_for_ckeditor'


ckeditor = CKEditor(app)

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


@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/upload', methods=['GET','POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'],filename))
        flash('Upload success')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))

    return render_template('upload.html', form=form)


@app.route('/ckeditor', methods=['GET', 'POST'])
def integrate_ckeditor():
    form = RichTextForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        flash('Your post is published')
        return render_template('post.html', title=title, body=body)

    return render_template('ckeditor.html', form=form)    


@app.route('/upload-ck', methods=['POST'])
def upload_for_ckeditor():
    f = request.files.get('upload')
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail('Image only')
    
    f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
    url = url_for('get_file', filename=f.filename)
    return upload_success(url, f.filename)