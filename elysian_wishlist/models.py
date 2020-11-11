from datetime import datetime
from elysian_wishlist import db

#db model for each wishlist
class Wishlist(db.Model):
    __tablename__ = "Wishlist"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_uid = db.Column(db.Integer, db.ForeignKey('User.uid'), nullable=False)
    wishlist_sub = db.relationship('child', backref='wishlist')
    liked = db.relationship('LikedWishlist', backref='wishlist', lazy='dynamic')


    def __repr__(self):
        return f"User('{self.id}', '{self.content}', '{self.user_uid}')"

#db model for each sub wishlist
class child(db.Model):
    __tablename__ = "sub"
    id = db.Column(db.Integer, primary_key=True)
    child_content = db.Column(db.String(200), nullable=False)
    Wishlist_id = db.Column(db.Integer, db.ForeignKey('Wishlist.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    prices = db.Column(db.String(200), nullable=True)
    image_file = db.Column(db.String(200), nullable=False)


class User(db.Model):
    __tablename__ = "User"                               #creating a user model using flask sqlalchemy
    uid = db.Column(db.Integer, primary_key=True)       #the id created when adding a session to the user
    firstname = db.Column(db.String(100), nullable=False) #the information that will be stored in each corresponding column in the db
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pass_hash = db.Column(db.String(100), nullable=False)
    user_wishlist = db.relationship('Wishlist', backref='user')
    liked = db.relationship('LikedWishlist', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.uid}', '{self.firstname}', '{self.lastname}', '{self.email}', '{self.username}')"

class LikedWishlist(db.Model):
    __tablename__ = 'LikedWishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.Integer, db.ForeignKey('User.uid'))
    Wishlist_id = db.Column(db.Integer, db.ForeignKey('Wishlist.id'))

    
