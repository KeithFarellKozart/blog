from pydoc import text
from sqlite3 import IntegrityError
from flask import Flask, redirect, render_template, request, flash, url_for, session, g
from utils.database import db_session
from werkzeug.security import check_password_hash, generate_password_hash
from utils.models import User, Post

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route("/register/", methods=["GET", "POST"])
def register():
     if request.method == "POST":
          username = request.form.get("username")
          email = request.form.get("username")
          password = request.form.get("username")
          password2 = request.form.get("username")
          error = ""

          if not username:
               error = "Username is required"
          elif not password:
               error = "Password is required"
          elif not email:
               error = "Email is required"
          elif password != password2:
               error = "Password don't match"

          if error == "":
               user = User(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
               )
               try:
                    db_session.add(user)
                    db_session.commit()
               except IntegrityError:
                    error = "Такой пользователь уже существует"
               else:
                    return redirect(url_for("login"))
          flash(error)
     return render_template("auth/register.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
     if request.method == "POST":
          username = request.form.get("username")
          password = request.form.get("password")
          print(password)
          error = None

          user = User.query.filter(User.username == username).first()
          if User is None:
               error = "Не существует такого пользователя"
          elif not check_password_hash(user.password, password):
               error ="Неправильный пароль"

          if error is None:
               session.clear()
               session["user_id"] = user.id
               return redirect(url_for("index"))
          flash(error)
          print(error)
     return render_template("auth/login.html")

@app.route("/", methods=["GET", "POST"])
def index():
     posts=Post.query.all()
     return render_template("index.html", posts=posts)


@app.before_request
def load_user() -> None:
     user_id = session.get("user_id")
     if user_id is None:
          g.user = None
     else:
          g.user = User.query.filter(User.id == session["user_id"]).first()

@app.route("/user/<string:name>")
def user(name):
     user = User.query.filter(User.name == name).first()
     return f"<h1>Username is {user.name}"


@app.teardown_appcontext
def shutdown_session(exception=None):
     db_session.remove()

@app.post("/create/")
def create():
     title = request.form.get("title")
     text = request.form.get("text")
     user = g.user
     post = Post(title, text, user.id)
     print(title)
     print(text)
     print(user)
     if text != "" or text is not None:
          db_session.add(post)
          try:
               db_session.commit()
          except:
               print("help me")
     return redirect(url_for("index"))

@app.route("/edit/<int:id>/", methods=["GET", "POST"])
def edit(id: int):
     post = Post.query.filter(Post.id == id).first()
     if request.method == "POST":
          title = request.form.get("title")
          text = request.form.get("text")

          post.title = title
          post.text = text
          db_session.commit()
          return redirect(url_for("index"))    
     return render_template("edit.html", post=post)
@app.post("/delete/<int:id>/")
def delete(id):
     post = Post.query.get(id)
     db_session.delete(post)
     db_session.commit()
     return redirect(url_for("index"))


