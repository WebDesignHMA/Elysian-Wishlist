from elysian_wishlist.tests import app, db
from elysian_wishlist.modules.third_party_api.ebay import ebay_search_catalog, ebay_search_item
import json

def test_app():
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

def test_home():
    with app.test_client() as client:
        response = client.get('/home/')
        assert response.status == "200 OK"
        
def test_signup():
    with app.test_client() as client:
        response = client.get('/signup/')
        assert response.status == "200 OK"

def test_login():
    with app.test_client() as client:
        response = client.get('/login/')
        assert response.status == "200 OK"

def test_profile():
    with app.test_client() as client:
        response = client.get('/profile/')
        assert response.status == "302 FOUND"
        
def test_logout():
    with app.test_client() as client:
        response = client.get('/profile/')
        assert response.status == "302 FOUND"

def test_index():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status == "200 OK"

def test_allWishlist():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status == "200 OK"
        
