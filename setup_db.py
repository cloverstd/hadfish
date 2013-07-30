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

    # image1 = Image("1")
    # image2 = Image("2")
    # image3 = Image("3")
    # image4 = Image("4")
    kind1 = Kind(u"日用品")
    kind2 = Kind(u"其他")
    kind3 = Kind(u"书籍")
    kind4 = Kind(u"3C")
    # item_sale = ItemSale("test", 1.2, 1, kind1.id)
    # item_demand = ItemDemand("test", 1, kind2.id)
    # item_sale.images = [image1, image3]
    # item_demand.images = [image2, image4]
    # 
    # user = User("cloverstd", "cloverstd@gmail.com", "")
    # user.item_sales = [item_sale]
    # user.item_demands = [item_demand]
    # 
    # db.session.add(user)
    db.session.add_all([kind1, kind2, kind3, kind4])
    db.session.commit()
    # 
    # i = User.query.first()
    # print i.item_sales[0]
    # 
    # for a in i.item_sales[0].images:
        # print a
    # for a in i.item_demands[0].images:
        # print a
