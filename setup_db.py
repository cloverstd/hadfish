#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hadfish import app
from hadfish.extensions import db
from hadfish.databases import *
from datetime import datetime
from time import sleep

with app.test_request_context():
    db.init_app(app)
    db.create_all()

    image1 = Image("1")
    image2 = Image("2")
    image3 = Image("3")
    image4 = Image("4")
    item_sale = ItemSale("test", 1.2, 1)
    item_demand = ItemDemand("test", 1, "test")
    item_sale.images = [image1, image3]
    item_demand.images = [image2, image4]
    # 
    user = User("test", "test", "test")
    user.item_sales = [item_sale]
    user.item_demands = [item_demand]
    # 
    db.session.add(user)
    db.session.commit()
    # 
    i = User.query.first()
    print i.item_sales[0]
    # 
    for a in i.item_sales[0].images:
        print a
    for a in i.item_demands[0].images:
        print a
