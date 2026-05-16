from flask import (
    Flask, 
    render_template, 
    request,
    session, 
    redirect, 
    url_for
    )
from flask_wtf import FlaskForm
from wtforms import (
    DateField, 
    ValidationError, 
    StringField, 
    PasswordField, 
    SubmitField, 
    TextAreaField, 
    BooleanField
    )
from wtforms.validators import DataRequired
from loguru import logger
from flask_bootstrap import Bootstrap
# 自作クラス
from form_list import (
    Todo_Form, 
    State, 
    Todo_info
    )
# SQLAlchemy
from sqlalchemy import Boolean, Date, String, Integer, create_engine, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
import datetime
import enum

app = Flask(__name__, template_folder="templates")


# フォームを利用する際に必要。セキュリティ対策に必要
app.config['SECRET_KEY'] = 'mysecretkey'

# ----------------------------
# logの設定
# ----------------------------
# logを追加
logger.remove()
# ログファイル
logger.add("log_state.log", level="INFO", encoding="utf-8")


# ----------------------------
# SQLAlchemyのデータベースの設定
# ----------------------------

# --- ベースクラス ---
class Base(DeclarativeBase):
    pass

# # --- State定義 ---
# # TODO: タスクが未着手の状態
# # DOING: タスクが進行中の状態
# # DONE: タスクが完了した状態
# class State(enum.Enum):
#     TODO = "TODO"
#     DOING = "DOING"
#     DONE = "DONE"
#     @property
#     def label(self):
#         return {
#             "TODO": "未着手",
#             "DOING": "作業中",
#             "DONE": "完了"
#         }[self.value]

# --- モデル定義 ---
# TODO_DB: todoテーブル に対応。
# id 主キー、連番自動採番。
# task: タスク名。
# detail: 詳細（任意）。
# done: 完了状態（True/False）。
# limit: 期限日（任意）。
class TODO_DB(Base):
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(primary_key=True)  # 自動採番
    task: Mapped[str] = mapped_column(String) 
    detail: Mapped[str] = mapped_column(String, nullable=True)
    done: Mapped[str] = mapped_column(Boolean)
    limit: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    state: Mapped[State] = mapped_column(Enum(State), default=State.TODO)  # デフォルトはTODO

# DB接続とセッション作成
engine = create_engine("sqlite:///todo.db")
Session = sessionmaker(bind=engine)
session = Session()

# テーブル作成
Base.metadata.create_all(engine)

# ----------------------------
# メイン処理
# ----------------------------

# 空のtodoリスト
# detaleの欄を追加　
# todos = [{"task": "Sample_todo", "detail": None, "done": False, "limit": None}]
todos = []

@app.route("/", methods=["GET", "POST"])
def index(id=None):
    form = Todo_Form()
    # POSTか同化の確認とセキュリティ
    if form.validate_on_submit():

        # if id:
        #         # データベースから該当のタスクを取得
        #         todo = session.get(TODO_DB, id)
        #         # タスクの内容を更新
        #         todo.task = form.todo.data
        #         todo.detail = form.todo_detail.data
        #         todo.limit = form.limit_date.data
        #         todo.state = State.TODO  # 編集したタスクはTODO状態にリセット
        #         print(f"上書き保存check")

        # else:
        #     new_todo = TODO_DB(
        #         task=form.todo.data,
        #         detail=form.todo_detail.data,
        #         done=False,
        #         state=State.TODO,  # 新規タスクはTODO状態
        #         limit=form.limit_date.data,
        #     )
        #     # データベースへの追加
        #     session.add(new_todo)
        #     print(f"新規登録check")
        # session.commit()
        Todo_info.add_todo(request, session)

        return redirect(url_for("see_todo"))
    # todos = session.query(TODO_DB).all()
    return render_template("index.html", form=form)



@app.route("/test", methods=["GET"])
def see_todo():
    form = Todo_Form()
    todos = session.query(TODO_DB).all()
    return render_template("see_todo.html", form=form, todos=todos, State=State)


@app.route("/edit/<int:id>", methods=["GET"])
def edit_todo(id):
    form = Todo_Form()
    # todos = session.query(TODO_DB).all()
    # フォームの値をデータベースの値で表示
    todo = session.get(TODO_DB, id)
    form.todo.id = id
    form.todo.data = todo.task
    form.todo_detail.data = todo.detail
    form.limit_date.data = todo.limit

    return render_template("index.html", form=form, id=id)




# 完了処理
@app.route("/complete/<int:id>", methods=["POST"])
def complete_todo(id):
    # データベースから該当のタスクを取得
    todo = session.get(TODO_DB, id)
    # タスクの状態を完了に更新
    todo.done = True
    todo.state = State.DONE  # 状態をDONEに更新

    # 変更をコミット
    session.commit()

    return redirect(url_for("see_todo"))



if __name__ == "__main__":
    app.run(debug=True, port=5001)