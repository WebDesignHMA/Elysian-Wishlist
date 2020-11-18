from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(db_uri='sqlite:///auth.db'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # SECRET_KEY required for session, flash and Flask Sqlalchemy to work
    app.config['SECRET_KEY'] = 'OCML3BRawWEUeaxcuKHLpw'
    db.init_app(app)
    app.app_context().push()
    db.create_all()
  
    return app

app=create_app()
from elysian_wishlist import routes
