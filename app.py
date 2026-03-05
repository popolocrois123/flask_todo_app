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

# ベースクラス
class Base(DeclarativeBase):
    pass

# モデル定義
class TODO_DB(Base):
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(primary_key=True)  # 自動採番
    task: Mapped[str] = mapped_column(String) 
    detail: Mapped[str] = mapped_column(String)
    done: Mapped[str] = mapped_column(Boolean)
    limit: Mapped[datetime.date] = mapped_column(Date)

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
    # # [WTF]POSTデータを自動ｄフォームに紐付け
    # form = Todo_Form()
    # return render_template("index.html", todos=todos, form=form)

    form = Todo_Form()
    # POSTか同化の確認とセキュリティ
    if form.validate_on_submit():
        # print("test")
        # form の中のtodoからデータを入手
        todo = form.todo.data
        # print(f"{form}")
        todo_detail = form.todo_detail.data
        limit_date = form.limit_date.data
        if todo:  # 空でないときだけ追加
            # 追加するtodoの辞書
            todo_add_dict = {"task": todo, 
                        "detail": todo_detail if todo_detail else None, 
                        "done": False, 
                        "limit": limit_date if limit_date else None}
            todos.append(todo_add_dict)
            logger.info(f"todosの追加: {todos}")


            # 宿題
            # データベースへの追加
            for t in todo_add_dict:
                print(f"{todo_add_dict[t]}: {type(todo_add_dict[t])}")
            session.add(TODO_DB(**todo_add_dict))
            session.commit()

            

            # if  not todo_detale:
        # データベースからデータの呼び出し
        all_data = session.query(TODO_DB).all()
        for task_data in all_data:
            todos.append({"id": task_data.id,
                            "task": task_data.task,
                            "detail": task_data.detail,
                            "done": task_data.done,
                            "limit": task_data.limit})
        return render_template("see_todo.html", todos=todos, form=form)
    else:
        print(form.errors)
    return render_template("index.html",  form=form)




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

    




# # 宿題：detaleを追加
# @app.route("/see_todo", methods=["GET"])
# def see_todo():
#     return render_template("see_todo.html", todos=todos)


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