from elysian_wishlist.modules.third_party_api.amazon import *
from elysian_wishlist.modules.third_party_api.ebay import *
import json
    
def test_ebay_search_catalog():
    items=json.loads(ebay_search_catalog("baseball", 1))
    assert type(items)==type([])
    assert type(items[0])==type({})

def test_ebay_search_item():
    items=json.loads(ebay_search_catalog("baseball", 1))
    id=items[0]['item_id']
    item=json.loads(ebay_search_item(id))
    assert type(item)==type({})

    
