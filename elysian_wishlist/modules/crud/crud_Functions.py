from flask import Flask, render_template, request, url_for, redirect, flash, \
session, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from elysian_wishlist import db
from elysian_wishlist.models import *
from elysian_wishlist.modules.third_party_api.ebay import *
from elysian_wishlist.modules.third_party_api.amazon import *
import json


#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)

#route for all wishlists
def index():
    #creates your wishlist or returns all wishlists created
    db.create_all()
    if request.method == 'POST':
        username = session.get("USERNAME")
        user = User.query.filter_by(username=username).first()
        if user:
            user_uid = user.uid
            list_content = request.form['content']
            new_list = Wishlist(content=list_content, user_uid=user_uid)
        else:
            flash("User Must Login to Create Wishlist")
            return redirect('/')

        try:
            db.session.add(new_list)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your wishlist'

    else:
        username = session.get("USERNAME")
        user = User.query.filter_by(username=username).first()
        if user:
            user_uid = user.uid
            user_wishlist = Wishlist.query.filter_by(user_uid=user_uid).all()
            return render_template('index.html', lists=user_wishlist)
        #lists = Wishlist.query.order_by(Wishlist.date_created).all()
        else:
            lists=''
            return render_template('index.html', lists=lists)


#all WISHLISTS everyone made
def api_allWishlists():
    #lists = Wishlist.query.order_by(Wishlist.date_created).all()
    lists = db.session.query(Wishlist, User).join(User, Wishlist.user_uid == User.uid).all()
    #print(lists)
    return render_template('allWishlists.html', lists=lists)

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

#routes to their appropriate items for the wishlist
def list(id):
    #creates items for each wishlist
    myList = Wishlist.query.get_or_404(id)

    if request.method == "POST":
        content = request.form['content']
        parentId = request.form['parentId']
        json_dict = json.loads(ebay_search_catalog(content, 1))[0]
        json_content = json_dict['title']
        json_price = json_dict['price']
        json_image = json_dict['image']
        print(json_content)
        print(parentId)

        new_list = child(child_content=json_content, Wishlist_id=int(parentId), prices=json_price, image_file=json_image)
        db.session.add(new_list)
        db.session.commit()

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
    try:
        db.session.delete(sublist_to_delete)
        db.session.commit()
        return redirect('/list/{}'.format(str(parent_id)))
    except:
        return 'There was a problem deleting that list'

#update items from each wishlist
def updatesub(id):
    sublist = child.query.get_or_404(id)
    parent_id = sublist.Wishlist_id

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
