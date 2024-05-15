from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/gagankumar/Documents/dendrite_2/login_app/api/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False