from flask_wtf import FlaskForm
from wtforms import DateField, ValidationError, StringField, PasswordField, SubmitField, TextAreaField, BooleanField, RadioField
from wtforms.validators import DataRequired, Optional
import enum

# --------------------------------
# ---- State定義 
# --------------------------------
# TODO: タスクが未着手の状態
# DOING: タスクが進行中の状態
# DONE: タスクが完了した状態
class State(enum.Enum):
    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"
    @property
    def label(self):
        return {
            "TODO": "未着手",
            "DOING": "作業中",
            "DONE": "完了"
        }[self.value]


# --------------------------------
# --- Flaskフォーム（WTF）
# --------------------------------


class Todo_Form(FlaskForm):
    # todoリストの項目入力フィールド
    todo = StringField("Todo", validators=[DataRequired()])
    # todoリストの内容入力フィールド
    todo_detail = StringField("詳細")
    # チェックボックスフィールド
    check_box = BooleanField()
    # 登録ボタンフィールド
    submit = SubmitField("登録")
    # 期限の日付選択フィールド
    limit_date = DateField("期限日付を入力：", format="%Y-%m-%d"
                            ,validators=[Optional()])
    # 編集ボタンフィールド
    edit = SubmitField("編集")
    # 進行チェックボックスフィールド
    select_state = RadioField(
        "状態",
        choices=[(s.name, s.label) for s in State], default="TODO"
    )

