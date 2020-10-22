from flask import render_template, url_for, redirect, flash
from elysian_wishlist import app, db
from modules.crud.crud_Functions import *
from modules.user_login.login_app import *

# Change dbname here
#db_name = "auth.db"

#def create_db():       #run this function if there is no current db created
#    db.create_all()

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
