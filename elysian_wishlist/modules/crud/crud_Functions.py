from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from elysian_wishlist import db
from elysian_wishlist.models import *


#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)

#route for all wishlists
def index():
    #creates your wishlist or returns all wishlists created
    db.create_all()
    if request.method == 'POST':
        list_content = request.form['content']
        new_list = Wishlist(content=list_content)

        try:
            db.session.add(new_list)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your wishlist'

    else:
        lists = Wishlist.query.order_by(Wishlist.date_created).all()
        return render_template('index.html', lists=lists)

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
        print(content)
        print(parentId)

        new_list = child(child_content=content, Wishlist_id=int(parentId))
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
