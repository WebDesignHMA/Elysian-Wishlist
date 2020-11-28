from flask import Flask, render_template, request, url_for, redirect, flash, \
session, abort
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from elysian_wishlist import db
from elysian_wishlist.models import *

#signup
def api_signup(db):
    db.create_all()
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if not (firstname and lastname and email and username and password):
            flash("Fields cannot be empty")
            return redirect(url_for('signup'))
        else:
            firstname = firstname.strip()       #strip() removing all whitespaces
            lastname = lastname.strip()
            email = email.strip()
            username = username.strip()
            password = password.strip()

        # Returns salted pwd hash in format : method$salt$hashedvalue
        hashed_pwd = generate_password_hash(password, 'sha256')

        new_user = User(firstname = firstname, lastname = lastname, email = email, username=username, pass_hash=hashed_pwd)  #creating new_user object
        db.session.add(new_user)  #storing the object 'new_user' into the session, this allows for users to be authenticated to certain pages when requiring                         session[]=true
                                  #for exampe, if session[amrit, singh, ...] = true, it will allow that user to login and access the homepage from there
        try:
            db.session.commit()   #transaction is committed and user is given an id, new_user.id
        except sqlalchemy.exc.IntegrityError:
            flash("Email {e} is already in use.".format(e=email))
            flash("Username {u} is not available.".format(u=username))
            return redirect(url_for('signup'))

        flash("User account has been created.")
        return redirect(url_for("login"))

    return render_template("signup.html")

def api_login(User):
    if request.method == "POST":
        username = request.form['username']  #session variable username and password are found and user can login
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.pass_hash, password):   #the check_password_hash function will check plaintext password with hashed value stored in database to see if they match
            session["USERNAME"] = username        #will store session cookie with true if username and password is valid
            return redirect(url_for("user_home"))
        else:
            flash("Invalid username or password.")

    return render_template("login_form.html")


def api_user_home():
    if session.get("USERNAME", None) is not None:   #if session cookie value is not true, it will redirect to login.
        username = session.get("USERNAME")
        user = User.query.filter_by(username=username).first()
        if user:
            #myList = db.session.query(LikedWishlist).filter(LikedWishlist.user_uid == user.uid).join(Wishlist).all()
            #myList = db.session.query(Wishlist, LikedWishlist).join(LikedWishlist, LikedWishlist.Wishlist_id == Wishlist.id).filter_by(LikedWishlist.user_uid==user.uid).all()
            #myList = Wishlist.query.join(LikedWishlist, LikedWishlist.user_uid==user.uid).all()
            likedList = db.session.query(Wishlist).join(LikedWishlist).filter(LikedWishlist.user_uid==user.uid).all()
            listCreated = db.session.query(Wishlist).join(User).filter(User.uid==user.uid).all()

            #print(myList)
            return render_template("user_home.html", likedList=likedList, listCreated=listCreated)
        else:
            print("session not found")
            return redirect(url_for('login'))
    else:
        print("session not found")
        return redirect(url_for('login'))


def api_logout():
    """ Logout user and redirect to login page with success message."""
    session.pop("USERNAME", None)     #removes the current users session cookie when logging out, this pops out 'username' session variable
    flash("successfully logged out.")
    return redirect(url_for('login'))
