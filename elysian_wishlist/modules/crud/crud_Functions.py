from flask import Flask, render_template, request, url_for, redirect, flash, \
session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from elysian_wishlist import db
from elysian_wishlist.models import *
from elysian_wishlist.modules.third_party_api.ebay import *
from elysian_wishlist.modules.third_party_api.amazon import *
import json


#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)

#route for all my wishlists
def index():
    #creates your wishlist or returns all wishlists created
    db.create_all()
    if request.method == 'POST':
        if session.get("USERNAME", None) is not None:
            username = session.get("USERNAME")
            user = User.query.filter_by(username=username).first()
            user_uid = user.uid
            list_content = request.form['content']
            new_list = Wishlist(content=list_content, user_uid=user_uid)
        else:
            flash("User Must Login to Create Wishlist", "danger")
            return redirect('/login/')

        try:
            db.session.add(new_list)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your wishlist'

    else:
        if session.get("USERNAME", None) is not None:
            username = session.get("USERNAME")
            user = User.query.filter_by(username=username).first()
            user_uid = user.uid
            user_wishlist = Wishlist.query.filter_by(user_uid=user_uid).all()
            images = []
            for list in user_wishlist:
                childList = child.query.filter_by(Wishlist_id=list.id).first()
                if childList is not None:
                    images.append(childList.image_file)
                else:
                    images.append("../static/images/santa.png")
            combined = []
            for i in range(len(user_wishlist)):
                combined.append([user_wishlist[i], images[i]])
            return render_template('index.html', lists=user_wishlist, combined=combined)
        #lists = Wishlist.query.order_by(Wishlist.date_created).all()
        else:
            flash("User Must Login to Create Wishlist", "danger")
            return redirect('/login/')
            #lists=''
            #return render_template('index.html', lists=lists)


#all WISHLISTS everyone made
def api_allWishlists():
    #lists = Wishlist.query.order_by(Wishlist.date_created).all()
    lists = db.session.query(Wishlist, User).join(User).all()
    if lists is not None:
        bubbleSort(lists)
    else:
        lists = ''
    images = []
    for list in lists:
        childList = child.query.filter_by(Wishlist_id=list[0].id).first()
        if childList is not None:
            images.append(childList.image_file)
        else:
            images.append("../static/images/santa.png")
    combined = []
    for i in range(len(lists)):
        combined.append([lists[i], images[i]])

    return render_template('allWishlists.html', lists=lists, combined=combined, has_liked_wishlist = has_liked_wishlist, like_action = like_action_api, displayComments=displayComments)

#bubbleSort to sort the likes
def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j][0].liked.count() < arr[j + 1][0].liked.count():
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


#updates wishlist
def update(id):
    list = Wishlist.query.get_or_404(id)

    if request.method == 'POST':
        list.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your wishlist'

    else:
        result = {'sub': False, 'list': list}
        return render_template('update.html', context=result)

#delete wishlists and all sublists
def delete(id):
    list_to_delete = Wishlist.query.get_or_404(id)


    sub_lists = child.query.filter_by(Wishlist_id=id).all()

    for i in sub_lists:
        db.session.delete(i)

    db.session.delete(list_to_delete)

    db.session.commit()
    return redirect('/')


def apiResult(name, id):
    myList = Wishlist.query.get_or_404(id)
    json_dict = json.loads(ebay_search_catalog(name, 1))
    return render_template('apiResults.html', result = json_dict, wishlistId = id)

def addToWishlistApi(wishlistId, itemId):
    json_dict = json.loads(ebay_search_item(itemId))
    json_content = json_dict['title']
    json_price = json_dict['price']
    json_image = json_dict['image']
    new_list = child(child_content=json_content, Wishlist_id=int(wishlistId), prices=json_price, image_file=json_image, ebay_id=itemId)
    db.session.add(new_list)
    db.session.commit()
    return redirect('/list/'+str(wishlistId))


def displayComments(id):
    if request.method == "POST":
        if session.get("USERNAME", None) is not None:
            username = session.get("USERNAME")
            user = User.query.filter_by(username=username).first()
            user_uid = user.uid
            content = request.form['content']
            parentId = request.form['parentId']
            new_list = WishlistComment(body=content, wishlist_id=parentId, uid=user_uid)
            try:
                db.session.add(new_list)
                db.session.commit()
                print(id)
                return redirect('/comments/'+str(id))
            except:
                return 'There was an issue adding your wishlist'
        else:
            flash("User Must Login to Create Wishlist", "danger")
            return redirect('/login/')

    #User and WishlistComment Table Joined
    myList = db.session.query(WishlistComment).filter(WishlistComment.wishlist_id == id).join(User, WishlistComment.uid==User.uid).add_columns('username').all()
    #Wishlist and User Joined Table
    lists = Wishlist.query.filter_by(id=id).join(User).add_columns('username')
    for list in lists:
        print(list[0].id)
        print(list[1])
    return render_template('displayComments.html', result = myList, lists=lists)


def postComments(id):
    #myList = Wishlist.query.get_or_404(id)
    if request.method == "POST":
        content = request.form['content']
        parentId = request.form['parentId']
        author = request.form['authorId']
        new_list = WishlistComment(body=content, wishlist_id=parentId, uid=author)
        try:
            db.session.add(new_list)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your wishlist'

    return redirect('/comments/'+str(id))



#routes to their appropriate items for the wishlist
def list(id):
    #creates items for each wishlist
    myList = Wishlist.query.get_or_404(id)
    user = User.query.filter_by(uid=myList.user_uid).first()


    if request.method == "POST":
        if session.get("USERNAME", None) is not None and user.username == session.get("USERNAME"):
            content = request.form['content']
            parentId = request.form['parentId']
            return redirect(url_for('ebayApiResult', name=content, id=id))
        else:
            myList = Wishlist.query.get_or_404(id)
            sub_list = child.query.filter_by(Wishlist_id=id).all()
            result_list = [
                           myList,
                           sub_list
                           ]
            flash("Only wishlist authors can edit this item!", "danger")
            return render_template('list.html', result = result_list)
    else:
        context = {
            'myList': myList
        }

        sub_list = child.query.filter_by(Wishlist_id=id).all()
        # print(sub_list)
        result_list = [
                    myList,
                    sub_list
                    ]

        print(result_list)
        return render_template('list.html', result = result_list)


#deletes items from each wishlist
def deletesub(id):
    sublist_to_delete = child.query.get_or_404(id)
    parent_id = sublist_to_delete.Wishlist_id
    WishList = Wishlist.query.get_or_404(parent_id)
    user = User.query.filter_by(uid=WishList.user_uid).first()

    if session.get("USERNAME", None) is not None and user.username == session.get("USERNAME"):
        try:
            db.session.delete(sublist_to_delete)
            db.session.commit()
            return redirect('/list/{}'.format(str(parent_id)))
        except:
            return 'There was a problem deleting that list'
    else:
        flash("Only wishlist authors can delete this item!", "danger")
        return redirect('/list/'+str(parent_id))

#update items from each wishlist
def updatesub(id):
    sublist = child.query.get_or_404(id)
    parent_id = sublist.Wishlist_id
    WishList = Wishlist.query.get_or_404(parent_id)
    user = User.query.filter_by(uid=WishList.user_uid).first()

    if session.get("USERNAME", None) is not None and user.username == session.get("USERNAME"):
        if request.method == 'POST':
            sublist.child_content = request.form['content']

            try:
                db.session.commit()
                return redirect('/list/{}'.format(str(parent_id)))
            except:
                return 'There was an issue updating your list'

        else:
            result = {'sub':True, 'sublist':sublist}
            return render_template('update.html', context = result)
    else:
        flash("Only wishlist authors can update this item!", "danger")
        return redirect('/list/'+str(parent_id))


#to like a wishlist (HELPER)
def like_wishlist(Wishlist):
    username = session.get("USERNAME")
    user = User.query.filter_by(username=username).first()
    if session.get("USERNAME", None) is not None:
        if not has_liked_wishlist(Wishlist):
            like = LikedWishlist(user_uid=user.uid, Wishlist_id=Wishlist.id)
            db.session.add(like)
            #return redirect('/wishlists/')
    else:
        return redirect('/login/')

#to unlike a wishlist (HELPER)
def unlike_wishlist(Wishlist):
    username = session.get("USERNAME")
    user = User.query.filter_by(username=username).first()
    if session.get("USERNAME", None) is not None:
        if has_liked_wishlist(Wishlist):
            LikedWishlist.query.filter(LikedWishlist.user_uid == user.uid).filter(LikedWishlist.Wishlist_id == Wishlist.id).delete()
            #return redirect('/wishlists/')
    else:
        return redirect('/login/')


#check if user has liked wishlist ALREADY (HELPER)
def has_liked_wishlist(Wishlist):
    username = session.get("USERNAME")
    user = User.query.filter_by(username=username).first()
    if session.get("USERNAME", None) is not None:
        return LikedWishlist.query.filter(LikedWishlist.user_uid == user.uid, LikedWishlist.Wishlist_id == Wishlist.id).count() > 0
    else:
        return False


#action to like wishlists (MAIN)
def like_action_api(wishlist_id, action):
    if session.get("USERNAME", None) is not None:
        wishlist = Wishlist.query.filter_by(id=wishlist_id).first_or_404()
        if action == 'like':
            like_wishlist(wishlist)
            db.session.commit()
        if action == 'unlike':
            unlike_wishlist(wishlist)
            db.session.commit()
        return redirect('/wishlists/')
    else:
        flash("User Must Login to Like/Dislike a Wishlist", "danger")
        return redirect('/login/')
