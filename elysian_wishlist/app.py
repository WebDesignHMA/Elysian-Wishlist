from flask import Flask, render_template, request, url_for, redirect, flash, \
session, abort
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from modules.user_login.login_app import *
from modules.crud.crud_Functions import *

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

@app.route("/login/", methods=["GET", "POST"])
def login():
    return api_login(User)

@app.route("/user/<username>/")
def user_home(username):
    return api_user_home(username)

@app.route("/logout/<username>")
def logout(username):
    return api_logout(username)

#route for all wishlists
@app.route('/', methods=['POST', 'GET'])
def allWishlists():
    return index()

#updates wishlist
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def updateWishlist(id):
    return update(id)

#delete wishlists and all sublists
@app.route('/delete/<int:id>')
def deleteWishlist(id):
    return delete(id)

#routes to their appropriate items for the wishlist
@app.route('/list/<int:id>', methods=['POST', 'GET'])
def wishlistItems(id):
    return list(id)

#deletes items from each wishlist
@app.route('/deletesub/<int:id>')
def deleteWishlistItems(id):
    return deletesub(id)

#update items from each wishlist
@app.route('/updatesub/<int:id>', methods=['GET', 'POST'])
def updateWishlistItems(id):
    return updatesub(id)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
