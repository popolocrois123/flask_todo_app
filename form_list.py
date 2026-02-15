from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class Todo_Form(FlaskForm):
    # todoリストの項目入力フィールド
    todo = StringField("Todo", validators=[DataRequired()])
    # todoリストの内容入力フィールド
    todo_detail = StringField("詳細")
    # チェックボックスフィールド
    check_box = BooleanField()
    # 登録ボタンフィールド
    submit = SubmitField("登録")