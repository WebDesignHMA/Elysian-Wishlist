from flask import Flask, render_template, url_for, request, redirect, flash, \
session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from elysian_wishlist import db
from elysian_wishlist.models import *

def api_forum():
  threads = Thread.query.order_by(Thread.date_created.desc()).all()
  return render_template('forum.html', threads=threads)

def api_new_thread():

  new_thread = None

  if request.method == 'POST' and request.form['content'] != "" and request.form['title'] != "":
    username = session.get("USERNAME")
    user = User.query.filter_by(username=username).first()
    if user:
        uid = user.uid
        thread_content = request.form['content']
        thread_title = request.form['title']
        new_thread = Thread(content=thread_content, title=thread_title, uid=uid)
    else:
        flash("User Must Login to Create Thread", "danger")
        return redirect('/login/')

    try:
      db.session.add(new_thread)
      db.session.commit()
      return redirect('/forum')

    except:
      return 'There was an error while creating the thread'

  elif request.method == 'POST' and request.form['content' or 'title'] == "":
    return 'Please insert a title and content to create a new thread'

  else:
    return render_template('new.html', new_thread=new_thread)

#editing so that only users that created the thread can delete the thread
def api_delete_thread(id):
    username = session.get("USERNAME")
    user = User.query.filter_by(username=username).first()
    if user:
           uid = user.uid
           thread_to_delete = Thread.query.get_or_404(id) #function to return error 404 if object not found
           db.session.delete(thread_to_delete)
           db.session.commit()
           return redirect('/forum')
    else:
        flash("Cannot perform this action", "danger")
        return redirect('/forum')


def api_view(id):
  thread = Thread.query.get_or_404(id)
  new_comment = None
  comment = Comment.query.filter(Comment.thread_id == thread.id).order_by(Comment.date_created).all()

  if request.method == 'POST' and request.form['content'] != "":
    username = session.get("USERNAME")
    user = User.query.filter_by(username=username).first()
    if user:
        uid = user.uid
        comment_content = request.form['content']
        thread_parent = thread
        new_comment = Comment(content=comment_content, thread=thread_parent, uid=uid)
    else:
        flash("User Must Login to Comment", "danger")
        return redirect('/login/')

    try:
      db.session.add(new_comment)
      thread.comments.append(new_comment)
      db.session.commit()
      return redirect(request.url)
    except:
      return 'There was an error while creating the comment'


  else:
    return render_template('view.html', thread=thread, comment=comment)
