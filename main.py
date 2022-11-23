from my_first_project import app
from flask import render_template, url_for, request, redirect, flash
from email_validator import validate_email, EmailNotValidError


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
            flash("Enter username")
            is_valid = False

        if not email:
            flash("Enter email address")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("This email format is not valid")
            is_valid = False

        if not description:
            flash("Enter details of enquiry")
            is_valid = False

        if not is_valid:
            return redirect(url_for("form"))

        flash("Your enquiry sent over via email.Thank you for contacting us!")
        return redirect(url_for("form_complete"))

    return render_template("form_complete.html")