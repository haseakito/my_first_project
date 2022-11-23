import sqlite3

from flask import Flask
from flask import render_template, url_for, request, redirect, flash, make_response, session
from email_validator import validate_email, EmailNotValidError
from flask_mail import Mail, Message
import logging
import os

import database

app = Flask(__name__)

app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"

app.logger.setLevel(logging.DEBUG)

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)

db = database.create_table()
DATABASE = 'database.db'
@app.route('/')
def index():

    connect = sqlite3.connect(DATABASE)
    db_table = connect.execute("SELECT * FROM games").fetchall()
    connect.close()

    games = []
    for row in db_table:
        games.append({'title' : row[0],
                      'price' : row[1],
                      'description' : row[2],
                      'link' : row[3]})

    return render_template(
        'index.html',
        games = games
    )

@app.route('/register')
def register():
    response = make_response(render_template('register_game.html'))

    response.set_cookie("flaskbook key", "flaskbook value")

    session["username"] = "who cares?"

    return response
@app.route('/register', methods = ['POST'])
def register_game():
    title = request.form['title']
    price = request.form['price']
    description = request.form['description']
    link = request.form['link']

    connect = sqlite3.connect(DATABASE)
    connect.execute('INSERT INTO games VALUES (?, ?, ?, ?)',
                    [title, price, description, link])
    connect.commit()
    connect.close()

    return redirect(url_for("index"))

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/form/complete', methods = ["GET", "POST"])
def form_complete():
    if request.method == "POST":

        #form属性を使って、フォームの値を取得
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        is_valid = True

        if not username:
            flash("Enter username!")
            is_valid = False

        if not email:
            flash("Enter email address!")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("This email format is not valid!")
            is_valid = False

        if not description:
            flash("Enter details of enquiry!")
            is_valid = False

        if not is_valid:
            return redirect(url_for("form"))

        send_mail(
            email,
            "Thanks for contacting us",
            "contact_mail",
            username=username,
            description=description
        )

        flash("Your enquiry sent over via the email! Thanks you for your opinion!")
        return redirect(url_for("form_complete"))

    return render_template("form_complete.html")

app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")

def send_mail(to, subject, template, **kwargs):
    message = Message(subject, recipients=[to])
    message.body = render_template(template + ".txt", **kwargs)
    message.html = render_template(template + ".html", **kwargs)

    mail.send(message)