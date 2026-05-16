from flask_wtf import FlaskForm
from wtforms import DateField, ValidationError, StringField, PasswordField, SubmitField, TextAreaField, BooleanField, RadioField
from wtforms.validators import DataRequired, Optional
import enum
from flask_sqlalchemy import SQLAlchemy




# --------------------------------
# ---- State定義 
# --------------------------------
# TODO: タスクが未着手の状態
# DOING: タスクが進行中の状態
# DONE: タスクが完了した状態
class State(enum.Enum):
    TODO = "TODO"
    DOING = "DOING"
    # DONE = "DONE"
    @property
    def label(self):
        return {
            "TODO": "未着手",
            "DOING": "作業中",
            # "DONE": "完了"
        }[self.value]


# --------------------------------
# --- Flaskフォーム（WTF）
# --------------------------------


class Todo_Form(FlaskForm):
    # todoリストの項目入力フィールド
    todo = StringField("Todo", validators=[DataRequired()])
    # todoリストの内容入力フィールド
    todo_detail = StringField("詳細")
    # 完了チェックボックスフィールド
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


# ----------------------------
# --- todoテーブルの定義
# ----------------------------
db = SQLAlchemy()

class Todo_info(db.Model):
    # データベースの保存先の引き出しを作る
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.String(255), nullable=True)
    done = db.Column(db.Boolean, default=False)
    limit = db.Column(db.Date, nullable=True)
    state = db.Column(db.Enum(State))

    # 追加、削除、編集の為のデコレーター
    @classmethod
    def add_todo(cls, request, session):
        if request.form.get("id"):
            # データベースから該当のタスクを取得
            todo = cls.query.get(request.form.get("id"))
            # タスクの内容を更新
            todo.task = request.form.get("todo")
            todo.detail = request.form.get("todo_detail")
            todo.limit = request.form.get("limit_date")
            todo.state = State(request.form.get("select_state"))
            print(f"上書き保存check")
        else:
            new_todo = cls(
                task=request.form.get("todo"),
                detail=request.form.get("todo_detail", None),
                done=request.form.get("check_box") == "y",
                limit=request.form.get("limit_date", None),
                state=State(request.form.get("select_state", "TODO"))
            )
            print("★中身の確認:", request.form.get("id"))
            print(f"新規登録check")
            session.add(new_todo)
        session.commit()
        