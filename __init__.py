from flask import Flask
app = Flask(__name__)

app.config["config_key"] = config_value
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"

from my_first_project import main
