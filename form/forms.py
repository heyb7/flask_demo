from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField

from wtforms.validators import DataRequired, Length, ValidationError

from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), Length(8,128,"password is short(8-128)")])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


# 自定义表单验证器
class FortyTwoForm(FlaskForm):
    answer = IntegerField('The number')
    submit = SubmitField()

    def validate_answer(form, field):
        if field.data != 42:
            raise ValidationError('Must be 42.')


# 上传文件表单
class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png','gif'])])
    submit = SubmitField()


# 富文本编辑器表单
class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1,50)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Publish')