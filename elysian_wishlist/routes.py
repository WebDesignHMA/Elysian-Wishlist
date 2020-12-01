from flask import render_template, url_for, redirect, flash
from elysian_wishlist import app, db
from elysian_wishlist.modules.crud.crud_Functions import *
from elysian_wishlist.modules.user_login.login_app import *
from elysian_wishlist.modules.third_party_api.ebay import *
from elysian_wishlist.modules.third_party_api.amazon import *
from elysian_wishlist.modules.cronChart.priceChart import *
from elysian_wishlist.modules.forum.forum import *
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

@app.route("/profile/")
def user_home():
    return api_user_home()

@app.route("/logout/")
def logout():
    return api_logout()

#route for all wishlists
@app.route('/', methods=['POST', 'GET'])
def myWishlists():
    return index()

@app.route("/wishlists/")
def allWishlists():
    return api_allWishlists()

#route for charts
@app.route("/charts/")
def displayChartApi():
    return makePriceChart()

#like/unlike wishlists
@app.route('/like/<int:wishlist_id>/<action>')
def like_action(wishlist_id, action):
    return like_action_api(wishlist_id, action)

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

@app.route('/apiResult/<string:name>/<int:id>', methods=['GET'])
def ebayApiResult(name,id):
    return apiResult(name,id)

#routes for showing the wishlist COMMENTS
@app.route('/comments/<int:id>', methods=['POST', 'GET'])
def displayCommentsApi(id):
    return displayComments(id)

@app.route('/postComments/', methods=['POST', 'GET'])
def postCommentsApi(id):
    return postComments(id)



#HELPER FUNCTION: selected items for EBAY are added to db
@app.route('/addToWishlist/<int:wishlistId>/<itemId>')
def addToWishlist(wishlistId, itemId):
    return addToWishlistApi(wishlistId, itemId)


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

#search amazon item
@app.route('/amazon/item/<string:id>', methods=['GET'])
def amazonSearchItem(id):
    item=json.loads(amazon_search_item(id))
    return render_template('item.html', item=item)

#Splash page
@app.route("/home/")
def home():
    return render_template('splash_page.html')

@app.route('/forum')
def forum():
    return api_forum()

@app.route('/new', methods=['GET', 'POST'])
def new_thread():
    return api_new_thread()

@app.route('/deletethread/<int:id>')
def delete_thread(id):
    return api_delete_thread(id)

@app.route('/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    return api_view(id)
