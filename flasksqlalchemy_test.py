import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# ----------------------
# 基本
# ----------------------

# app = Flask(__name__)

# # 2. 最初に `basedir` を定義する
# basedir = os.path.abspath(os.path.dirname(__file__))

# # データベースの設定
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "f_sqltest.db")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# # SQLAlchemyインスタンスの作成
# db = SQLAlchemy(app)

# # モデルの定義
# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return f"<User {self.username}>"


# # データベースとテーブルの作成
# with app.app_context():
#     db.create_all()

# データの操作
# データの作成
# with app.app_context():
#     # インスタンスの作成
#     new_user = User(username="masamigmail", email="masami@example.com")

#     # セッションに追加してコミット（保存）
#     db.session.add(new_user)
#     db.session.commit()

# # データの取得
# with app.app_context():
#     # 全件取得
#     all_users = User.query.all()

#     # 主キー（id）で一件取得
#     user = User.query.get(1) # 現在は非推奨
#     user = db.session.get(User, 2)

#     # 条件を指定して取得
#     taro = User.query.filter_by(username="tarogmail").first()

#     # あいまい検索など、より複雑な条件
#     gmail_users = User.query.filter(User.email.like("%@gmail.com")).all()

#     # 太郎のメールアドレスを取得
#     taro_mail = user.email

#     print(all_users)
#     print(user)
#     print(taro)
#     print(gmail_users)
#     print(taro_mail)


# # データの更新
# with app.app_context():
#     # 更新したいユーザーを取得
#     user = db.session.get(User, 1)

#     # 属性を書き換えてコミット
#     if user:
#         user.email = "taro_new@example.com"
#         db.session.commit()


# # データの削除
# with app.app_context():
#     # 削除したいユーザーを取得
#     user = db.session.get(User, 2)

#     # セッションから削除してコミット
#     if user:
#         db.session.delete(user)
#         db.session.commit()

# # データの取得
# with app.app_context():
#     # 全件取得
#     all_users = User.query.all()

#     # 主キー（id）で一件取得
#     user = User.query.get(1) # 現在は非推奨
#     user = db.session.get(User, 2)

#     # 条件を指定して取得
#     user_filter = User.query.filter_by(username="masamigmail").first()

#     # あいまい検索など、より複雑な条件
#     gmail_users = User.query.filter(User.email.like("%@gmail.com")).all()

#     # 太郎のメールアドレスを取得
#     user_mail = user.email

#     print(all_users)
#     print(user)
#     print(user_filter)
#     print(gmail_users)
#     print(user_mail)

# -----------------
# デコレータの利用
# -----------------

# app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "f_sqltest.db")
# db = SQLAlchemy(app)

# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return f"<User {self.username}>"

#     @classmethod
#     def create_user(cls, username, email):
#         """新しいユーザーを作成して保存するメソッド"""
#         new_user = cls(username=username, email=email)
#         db.session.add(new_user)
#         db.session.commit()
#         return new_user

#     @classmethod
#     def update_email(cls, user_id, new_email):
#         """指定したIDのユーザーのメールアドレスを更新するメソッド"""
#         user = db.session.get(cls, user_id)
#         if user:
#             user.email = new_email
#             db.session.commit()
#             return user
#         return None

#     @classmethod
#     def delete_user(cls, user_id):
#         """指定したIDのユーザーを削除するメソッド"""
#         user = db.session.get(cls, user_id)
#         if user:
#             db.session.delete(user)
#             db.session.commit()
#             return True
#         return False


# # 別のクラスを定義
# class UserService:
#     def __init__(self):
#         # 必要なら初期化処理
#         pass

#     def register_new_customer(self, name, email):
#         """お客様を新規登録し、付随する処理を行うメソッド"""
#         print("[Service] ユーザー登録処理を開始します...")
        
#         # ★ ここで別のクラスである「User」のクラスメソッドを呼び出す！
#         new_user = User.create_user(username=name, email=email)
        
#         print(f"[Service] データベースへの保存完了: {new_user.username}")
#         print(f"[Service] {email} 宛にウェルカムメールを送信しました（模擬）")
#         return new_user

# # 呼び出し
# with app.app_context():
#     # UserServiceクラスのインスタンスを作って呼び出す
#     service = UserService()
#     service.register_new_customer(name="hinatagmail", email="hinata@example.com")



# ----------------------------
# デコレータの利用　request, sessionを引数に取る
# ----------------------------

import os
from flask import Flask, request, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "f_sqltest.db")
db = SQLAlchemy(app)

# -----------------
# 1. モデル定義
# -----------------
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    @classmethod
    def create_user(cls, request_obj, db_session):
        """引数のrequestからデータを抜き、引数のsessionで保存する"""
        # フォーム送信されたデータを取得
        username = request_obj.form.get("username")
        email = request_obj.form.get("email")

        if not username or not email:
            return None
        
        new_user = cls(username=username, email=email)

        # 引数でもらったセッションを使う
        db_session.add(new_user)
        db_session.commit()
        return new_user


# -----------------
# 2. サービス（ビジネスロジック）クラス
# -----------------
class UserService:
    def register_new_customer(self, req, sess):
        """引数で受け取ったreqとsessをそのままモデルへバケツリレーする"""
        print("[Service] ユーザー登録処理を開始します...")
        new_user = User.create_user(request_obj=req, db_session=sess)
        return new_user


# データベースの初期化
with app.app_context():
    db.create_all()


# -----------------
# 3. Flask ページ（ルーティング）の定義
# -----------------

# 簡易的な画面用のHTMLテンプレート（今回は1ファイルで動くように文字列で定義しています）
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>ユーザー登録テスト</title></head>
<body>
    <h1>ユーザー登録フォーム</h1>
    <form method="POST" action="/">
        <label>ユーザー名: <input type="text" name="username" required></label><br><br>
        <label>メールアドレス: <input type="email" name="email" required></label><br><br>
        <button type="submit">登録する</button>
    </form>

    <h2>登録済みユーザー一覧</h2>
    <ul>
    {% for user in users %}
        <li>{{ user.username }} ({{ user.email }})</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    # ページ上でボタンが押されて「POST」でデータが送られてきた場合
    if request.method == "POST":
        # 本物の「request」と「db.session」をその場で取得
        current_request = request
        current_session = db.session

        # サービスに引数として叩き込む！
        service = UserService()
        service.register_new_customer(req=current_request, sess=current_session)

        # 登録が終わったら、画面をリフレッシュ（二重送信防止）
        return redirect(url_for("index"))

    # 普通にページを開いた（GET）場合は、全ユーザーを並べて画面を表示する
    all_users = User.query.all()
    return render_template_string(HTML_TEMPLATE, users=all_users)


# アプリの起動
if __name__ == "__main__":
    app.run(debug=True)