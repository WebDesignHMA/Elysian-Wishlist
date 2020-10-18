from flask import Flask, render_template, request, url_for, redirect, flash, \
session, abort
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from modules.user_login.login_app import *

# Change dbname here
#db_name = "auth.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'.format(db=db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# SECRET_KEY required for session, flash and Flask Sqlalchemy to work
app.config['SECRET_KEY'] = 'OCML3BRawWEUeaxcuKHLpw'

db = SQLAlchemy(app)

def create_db():       #run this function if there is no current db created
    db.create_all()

@app.route("/signup/", methods=["GET", "POST"])
def signup():
    return api_signup(db)

@app.route("/", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    return api_login(User)

@app.route("/user/<username>/")
def user_home(username):
    return api_user_home(username)

@app.route("/logout/<username>")
def logout(username):
    return api_logout(username)



if __name__ == "__main__":
    app.run(port=5000, debug=True)
