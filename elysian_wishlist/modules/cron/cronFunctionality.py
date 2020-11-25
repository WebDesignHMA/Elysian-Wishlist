from elysian_wishlist import db
from flask_apscheduler import APScheduler
from elysian_wishlist.modules.third_party_api.ebay import *
from elysian_wishlist.models import *
import json



scheduler = APScheduler()

def scheduledTask():
    print("Task initiated...")
    lists = db.session.query(child).all()
    for list in lists:
        json_dict = json.loads(ebay_search_item(list.ebay_id))
        json_price = json_dict['price']
        new_list = cronScheduler(ebay_id=list.ebay_id, prices=json_price)
        db.session.add(new_list)
        db.session.commit()
        updateItemPrices(list.ebay_id, json_price)


def updateItemPrices(id, price):
    cronItem = child.query.filter_by(ebay_id=id).first()
    if not price:
        pass
    else:
        cronItem.prices = price
        try:
            db.session.commit()
        except:
            return 'There was an issue updating your wishlist'
