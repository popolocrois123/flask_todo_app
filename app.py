from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField, SubmitField, TextAreaField, BooleanField


app = Flask(__name__, template_folder="templates")

# フォームを利用する際に必要。セキュリティ対策に必要。
app.config['SECRET_KEY'] = 'mysecretkey'


"""
継承元のFlaskFormクラスの機能を使えるようになる。
各フィールドを定義する。ここで定義したフィールドを基にHTMLに配置する。
"""
class Todo_Registration(FlaskForm):
    # todoリストの項目入力フィールド
    todo = StringField()
    # todoリストの内容入力フィールド
    todo_detale = TextAreaField()
    # チェックボックスフィールド
    check_box = BooleanField()
    # 送信ボタンフィールド
    submit = SubmitField()




# 空のtodoリスト
# 宿題：detaleの欄を追加　
todos = [{"task": "Sample_todo", "detale": None, "done": False}]

@app.route("/")
def index():
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    todo = request.form.get("todo")
    todo_detale = request.form.get("detale")
    if todo:  # 空でないときだけ追加
        if  not todo_detale:
            todos.append({"task": todo, "detale": None, "done": False})
        else:
            todo.append({"task": todo, "detale": todo_detale, "done": False})

    return redirect(url_for("index"))

# # 宿題：detaleを追加
# @app.route("/detale", methods=["POST"])
# def add_detale():
#     todo_detale = request.form.get("todo_detale")
#     todo_index = int(request.form.get("todo_index"))
#     if todo_detale:  # 空でないときだけ追加
#         todos[todo_index]["detale"] = todo_detale
#     return redirect(url_for("index"))


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    todo = todos[index]
    if request.method == "POST":
        todo["task"] = request.form["todo"]
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo, index=index)
    
@app.route("/check/<int:index>")    
def check(index):
    todos[index]["done"] = not todos[index]["done"]
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete(index):
    del todos[index]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)