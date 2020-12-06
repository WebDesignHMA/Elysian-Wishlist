from flask import Flask, render_template, request, url_for, redirect, flash, \
session, abort, json
import matplotlib.pyplot as plt
from elysian_wishlist.models import *
import re




def makePriceChart(id):
    chartItem = db.session.query(child).filter_by(id=id).first()
    item_content = chartItem.child_content
    lists = db.session.query(cronScheduler).filter_by(ebay_id=chartItem.ebay_id).all()
    xAxis = []
    yAxis = []
    for list in lists:
        xAxis.append(list.date_created.date().isoformat())
        yAxis.append(re.sub(r'[^0-9.]+', '', list.prices).strip())
    labels = json.dumps(xAxis)
    data = json.dumps(yAxis)
    #new = re.sub(r'[^0-9.]+', '', s)

    #plt.figure()
    #plt.plot(xAxis,yAxis)
    #plt.title('Price Tracker')
    #plt.xlabel('Dates')
    #plt.ylabel('Prices')
    #plt.savefig("/elysian_wishlist/static/images/chart.png")
    #plt.close()
    return render_template('displayChart.html', xVal=labels, yVal=data, product=item_content)
    #plt.show()
