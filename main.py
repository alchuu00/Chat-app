import os

from flask import Flask, render_template, request, redirect
from sqla_wrapper import SQLAlchemy

app = Flask(__name__)
db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, primary_key=False)
    text = db.Column(db.String, primary_key=False)


db.create_all()


@app.route("/")
def index():
    messages = db.query(Message).all()
    for message in messages:
        print(message.id, message.author, message.text)

    return render_template("index.html", messages=messages)


@app.route("/add-message", methods=["POST"])
def add_message():
    username = request.form.get("username")
    text = request.form.get("text")

    message = Message(author=username, text=text)
    message.save()

    print(f"{username}: {message}")

    return redirect("/")


if __name__ == '__main__':
    app.run(use_reloader=True)
