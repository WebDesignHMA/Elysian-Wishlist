from flask import Flask, render_template, request, url_for, redirect, flash, \
session, abort, json
import matplotlib.pyplot as plt
from elysian_wishlist.models import *
import re




def makePriceChart():

    lists = db.session.query(cronScheduler).filter_by(ebay_id='173727095451').all()
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
    return render_template('displayChart.html', xVal=labels, yVal=data)
    #plt.show()
