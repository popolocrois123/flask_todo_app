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
    Todo_info,
    db
    )
# SQLAlchemy
from sqlalchemy import Boolean, Date, String, Integer, create_engine, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
import datetime
import enum
import os

app = Flask(__name__, template_folder="templates")


# フォームを利用する際に必要。セキュリティ対策に必要
app.config['SECRET_KEY'] = 'mysecretkey'

# ----------------------------
# logの設定
# ----------------------------
# logを追加
logger.remove()
# ログファイル
logger.add("log_state.log", level="DEBUG", 
            filter=lambda record: record["level"].name in ["INFO", "DEBUG"],
            encoding="utf-8")


# ----------------------------
# Flask-SQLAlchemyのデータベースの設定
# ----------------------------
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'todo.db')}"
)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db.init_app(app)
with app.app_context():
    db.create_all()




# ----------------------------
# メイン処理
# ----------------------------

# 空のtodoリスト
todos = []

@app.route("/regist", methods=["GET", "POST"])
def regist():
    form = Todo_Form()
    
    # POSTか同化の確認とセキュリティ
    if form.validate_on_submit():
        # print("validate通過")
        # Todo_info.add_todo(request, session)

        return redirect(url_for("index"))

    else:
        print("新規登録画面に移行")

    return render_template("regist.html", form=form)


@app.route("/", methods=["GET", "POST"])
def index():
    # form = Todo_Form()
    # todos = Todo_info.query.all()
    # # デバッグ
    # print(f"todosの件数： {len(todos)}")
    # return render_template("index.html", form=form, todos=todos, State=State)

    form = Todo_Form()
    
    # 【デバッグ】どんなリクエストが来たか確認
    print(f"--- リクエストメソッド: {request.method} ---")
    
    if request.method == "POST":
        print("--- POSTリクエストを感知しました ---")
        
        if form.validate_on_submit():
            print("--- フォームのバリデーション成功！ add_todoを実行します ---")
            Todo_info.add_todo(request, db.session)
            return redirect(url_for("index"))
        else:
            # もしフォームの入力値に問題（エラー）があればここを通る
            print("--- フォームのバリデーションに失敗しました ---")
            print(f"フォームのエラー内容: {form.errors}") # ← 何が原因で弾かれたか出力

    # データ取得
    todos = Todo_info.query.all()
    # print(todos) # ← 取得したデータを確認
    # print(db.engine.url)
    return render_template("index.html", form=form, todos=todos, State=State)


@app.route("/todo_main", methods=["GET", "POST"])
def see_todo():
    form = Todo_Form()
    todos = Todo_info.query.all()

    if form.validate_on_submit():
        Todo_info.add_todo(request, db.session)
        return redirect(url_for("index"))

    return render_template("index.html", form=form, todos=todos, State=State)


    
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_todo(id):
    print(f"id:{id}")
    form = Todo_Form()
    # todos = session.query(TODO_DB).all()
    # フォームの値をデータベースの値で表示
    todo = Todo_info.query.get(id)
    form.todo.id = id
    form.todo.data = todo.task
    form.todo_detail.data = todo.detail
    form.limit_date.data = todo.limit

    logger.info(f"{request.method} /edit 編集画面")

    return render_template("regist.html", form=form, id=id)




# 完了処理
@app.route("/complete/<int:id>", methods=["POST"])
def complete_todo(id):
    todo = Todo_info.query.get(id)
    todo.done = True
    todo.state = State.DONE

    db.session.commit()

    return redirect(url_for("see_todo"))



if __name__ == "__main__":
    app.run(debug=True, port=5002)