from flask import Flask
from flask import render_template, url_for, request, redirect, flash
from email_validator import validate_email, EmailNotValidError
from flask_mail import Mail, Message
import logging
import os

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

@app.route('/')
def index():
    game = [
        {
            "title" : "COD BO2",
            "price" : 8000,
            "description" : "This game is soo fun"
        },
        {
            "title": "OverWatch2",
            "price": 5000,
            "description": "This game is way better than COD"
        }
    ]
    return render_template(
        'index.html',
        games = game
    )

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