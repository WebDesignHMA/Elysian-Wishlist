from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

def create_app(db_uri='postgres://uhfejtnaccuojq:960f111d3b5a84c8b548950c79e5ae6335bb21ab984dad9e5ceb563085fdc414@ec2-35-171-31-33.compute-1.amazonaws.com:5432/dj7uv0tb4n85s'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # SECRET_KEY required for session, flash and Flask Sqlalchemy to work
    app.config['SECRET_KEY'] = 'OCML3BRawWEUeaxcuKHLpw'
    return app

app=create_app()
db = SQLAlchemy(app)
db.create_all()

from elysian_wishlist import routes
