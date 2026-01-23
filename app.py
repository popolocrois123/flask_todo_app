from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from loguru import logger

app = Flask(__name__, template_folder="templates")

# フォームを利用する際に必要。セキュリティ対策に必要
app.config['SECRET_KEY'] = 'mysecretkey'


# logを追加
logger.remove()
# ログファイル
logger.add("log_state.log", level="INFO", encoding="utf-8")



"""
継承元のFlaskFormクラスの機能を使えるようになる。
各フィールドを定義する。ここで定義したフィールドを基にHTMLに配置する。
"""
class Todo_Form(FlaskForm):
    # todoリストの項目入力フィールド
    todo = StringField("Todo", validators=[DataRequired()])
    # todoリストの内容入力フィールド
    todo_detale = StringField("詳細")
    # チェックボックスフィールド
    check_box = BooleanField()
    # 送信ボタンフィールド
    submit = SubmitField("送信")


# 空のtodoリスト
# 宿題：detaleの欄を追加　
todos = [{"task": "Sample_todo", "detale": None, "done": False}]

@app.route("/")
def index():
    form = Todo_Form()
    return render_template("index.html", todos=todos, form=form)


@app.route("/add", methods=["POST"])
def add():
    form = Todo_Form()
    
    if form.validate_on_submit():
        # todo, todo_detaleはこの下に書く
        todo = form.todo.data
        todo_detale = form.todo_detale.data
        if todo:  # 空でないときだけ追加
                todos.append({"task": todo, "detale": todo_detale if todo_detale else None, "done": False})
                logger.info(f"todosの追加: {todos}")
            # if  not todo_detale:
            #     todos.append({"task": todo, "detale": None, "done": False})
            # else:
            #     todos.append({"task": todo, "detale": todo_detale, "done": False})
            # if todo_detale:
            #     todos[todo]["detale"] = todo_detale

    return render_template("index.html", form=form, todos=todos)

# 宿題：detaleを追加
@app.route("/see_todo", methods=["GET"])
def see_todo():
    return render_template("see_todo.html", todos=todos)

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