from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import DateField, ValidationError, StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from loguru import logger
from flask_bootstrap import Bootstrap
# 自作クラス
from form_list import Todo_Form
# SQLAlchemy
from sqlalchemy import Boolean, Date, String, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
import datetime


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
def index():
    form = Todo_Form()
    # POSTか同化の確認とセキュリティ
    if form.validate_on_submit():
        new_todo = TODO_DB(
            task=form.todo.data,
            detail=form.todo_detail.data,
            done=False,
            limit=form.limit_date.data
        )
        # データベースへの追加
        session.add(new_todo)
        session.commit()

        return redirect(url_for("see_todo"))
    # todos = session.query(TODO_DB).all()
    return render_template("index.html", form=form)



# 宿題：detaleを追加
@app.route("/test", methods=["GET"])
def see_todo():
    todos = session.query(TODO_DB).all()
    return render_template("see_todo.html", todos=todos)

# @app.route("/add", methods=["POST"])
# def add():
#     form = Todo_Form()
#     # [WTF]POSTかどうか自動で判別
#     if form.validate_on_submit():
#         # todo, todo_detaleはこの下に書く
#         todo = form.todo.data
#         todo_detale = form.todo_detale.data
#         if todo:  # 空でないときだけ追加
#                 todos.append({"task": todo, "detale": todo_detale if todo_detale else None, "done": False})
#                 logger.info(f"todosの追加: {todos}")
#             # if  not todo_detale:
#             #     todos.append({"task": todo, "detale": None, "done": False})
#             # else:
#             #     todos.append({"task": todo, "detale": todo_detale, "done": False})
#             # if todo_detale:
#             #     todos[todo]["detale"] = todo_detale

#     return render_template("index.html", form=form, todos=todos)

    






# @app.route("/submit", methods=["POST"])
# def submit():
#     if request.method == "POST":
#         username = request.form["username"]
#         detail = request.form["detail"]
#         print(username)
#         print(detail)
#     return [username, detail], 200
#     # return render_template(".html", todos=todos)

# def add_detale():
#     todo_detale = request.form.get("todo_detale")
#     todo_index = int(request.form.get("todo_index"))
#     if todo_detale:  # 空でないときだけ追加
#         todos[todo_index]["detale"] = todo_detale
#     return redirect(url_for("index"))


# @app.route("/edit/<int:index>", methods=["GET", "POST"])
# def edit(index):
#     todo = todos[index]
#     if request.method == "POST":
#         todo["task"] = request.form["todo"]
#         return redirect(url_for("index"))
#     else:
#         return render_template("edit.html", todo=todo, index=index)
    
# @app.route("/check/<int:index>")    
# def check(index):
#     todos[index]["done"] = not todos[index]["done"]
#     return redirect(url_for("index"))

# @app.route("/delete/<int:index>")
# def delete(index):
#     del todos[index]
#     return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)