# ---------------
# とにかく最小：Hello Flask（GETだけ）
# ---------------

# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello Flask!"

# if __name__ == "__main__":
#     app.run(debug=True)

# ---------------
# URLパラメータ（/user/3 みたいなやつ）
# ---------------
# from flask import Flask

# app = Flask(__name__)

# @app.route("/user/<name>")
# def user(name):
#     return f"Hello {name}"

# if __name__ == "__main__":
#     app.run(debug=True)


# ---------------
# GET + フォーム（入力→表示）
# ---------------

# from flask import Flask, request

# app = Flask(__name__)

# @app.route("/", methods=["GET"])
# def index():
#     return """
#     <form action="/result" method="get">
#         <input name="msg">
#         <button type="submit">送信</button>
#     </form>
#     """

# @app.route("/result", methods=["GET"])
# def result():
#     msg = request.args.get("msg")
#     return f"入力された値： {msg}"

# if __name__ == "__main__":
#     app.run(debug=True)


# ---------------
# GET + POST（超重要パターン）
# ---------------
# from flask import Flask, request

# app = Flask(__name__)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         msg = request.form.get("msg")
#         return f"POSTで受け取った： {msg}"

#     return """
#     <form method="post">
#         <input name="msg">
#         <button type="submit">送信</button>
#     </form>
#     """

# if __name__ == "__main__":
#     app.run(debug=True)


# ---------------
# ちょい実戦：リダイレクト（重要）
# ---------------
from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for("hello"))

@app.route("/hello")
def hello():
    return "リダイレクトされたページ"

if __name__ == "__main__":
    app.run(debug=True)