from datetime import datetime
from elysian_wishlist import db

#db model for each wishlist
class Wishlist(db.Model):
    __tablename__ = "Wishlist"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<List %r>' % self.id

#db model for each sub wishlist
class child(db.Model):
    __tablename__ = "sub"
    id = db.Column(db.Integer, primary_key=True)
    child_content = db.Column(db.String(200), nullable=False)
    Wishlist_id = db.Column(db.Integer, db.ForeignKey('Wishlist.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):                                   #creating a user model using flask sqlalchemy
    uid = db.Column(db.Integer, primary_key=True)       #the id created when adding a session to the user
    firstname = db.Column(db.String(100), nullable=False) #the information that will be stored in each corresponding column in the db
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pass_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '' % self.username
