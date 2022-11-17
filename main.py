import os

from flask import Flask, render_template, request, redirect, url_for, make_response
from sqla_wrapper import SQLAlchemy
from sqlalchemy_pagination import paginate

app = Flask(__name__)
db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///db.sqlite"))
# this connects to a database either on Heroku or on localhost
db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, primary_key=True)
    email = db.Column(db.String, unique=True, primary_key=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, primary_key=False)
    text = db.Column(db.String, primary_key=False)


@app.route("/", methods=["GET"])
def index():
    email_address = request.cookies.get("email")
    # get user from the database based on email address
    if email_address:
        user = db.query(User).filter_by(email=email_address).first()
    else:
        user = None

    page = request.args.get("page")
    if not page:
        page = 1
    messages_query = db.query(Message).order_by(Message.id.desc())
    messages = paginate(query=messages_query, page=int(page), page_size=5)

    return render_template("index.html", messages=messages, user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    # create a User object
    user = User(name=name, email=email)
    user.save()  # save user into the database

    # save user's email into a cookie
    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", email)
    response.set_cookie("name", name)

    return response


@app.route("/add-message", methods=["POST"])
def add_message():
    username = request.cookies.get("name")
    text = request.form.get("text")

    message = Message(author=username, text=text)
    message.save()

    print(f"{username}: {message}")

    return redirect("/")


@app.route("/logout", methods=["GET"])
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", expires=0)
    response.set_cookie("name", expires=0)

    return response


if __name__ == '__main__':
    app.run(use_reloader=True)
