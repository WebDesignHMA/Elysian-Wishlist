from flask import render_template, url_for, redirect, flash
from elysian_wishlist import app, db
from modules.crud.crud_Functions import *
from modules.user_login.login_app import *
from modules.third_party_api.ebay import *
from modules.third_party_api.amazon import *
import json

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
    
#search ebay catalog
@app.route('/ebay/search/<string:query>/<int:page>', methods=['GET'])
def ebaySearchCatalog(query, page):
    items=json.loads(ebay_search_catalog(query, page))
    return render_template('items.html', items=items)

#search ebay item
@app.route('/ebay/item/<string:id>', methods=['GET'])
def ebaySearchItem(id):
    item=json.loads(ebay_search_item(id))
    return render_template('item.html', item=item)
    
#search amazon catalog
@app.route('/amazon/search/<string:query>/<int:page>')
def amazonSearchCatalog(query, page):
    items=json.loads(amazon_search_catalog(query, page))
    return render_template('items.html', items=items)
    
#search ebay item
@app.route('/amazon/item/<string:id>', methods=['GET'])
def amazonSearchItem(id):
    item=json.loads(amazon_search_item(id))
    return render_template('item.html', item=item)
