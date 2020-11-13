from elysian_wishlist.modules.third_party_api.amazon import *
from elysian_wishlist.modules.third_party_api.ebay import *
from flask_sqlalchemy import SQLAlchemy
from elysian_wishlist import create_app, db
import json
import pytest
   
@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.app_context():
        db.create_all()
        print(db.engine.table_names())
        return app
    
def test_app(app):
    assert app.config['SQLALCHEMY_DATABASE_URI']=='sqlite:///test.db'
   
def test_ebay_search_catalog():
    items=json.loads(ebay_search_catalog("baseball", 1))
    assert type(items)==type([])
    assert type(items[0])==type({})

def test_ebay_search_item():
    items=json.loads(ebay_search_catalog("baseball", 1))
    id=items[0]['item_id']
    item=json.loads(ebay_search_item(id))
    assert type(item)==type({})

def test_signup(app):
    with app.test_client() as client:
        response = client.post('/signup/')
        print(response)
