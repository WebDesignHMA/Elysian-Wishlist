from elysian_wishlist.modules.third_party_api.amazon import *
from elysian_wishlist.modules.third_party_api.ebay import *
import json
    
def test_ebay_search_item():
    item=json.loads(ebay_search_item("283986156272"))
    assert type(item)==type({})
    
def test_amazon_search_item():
    item=json.loads(amazon_search_item("B08CB1FXFW"))
    assert type(item)==type({})
    
def test_ebay_search_catalog():
    items=json.loads(ebay_search_catalog("item", 1))
    assert type(items)==type([])
    assert type(items[0])==type({})
    
def test_amazon_search_catalog():
    items=json.loads(amazon_search_catalog("item", 1))
    assert type(items)==type([])
    assert type(items[0])==type({})
    
