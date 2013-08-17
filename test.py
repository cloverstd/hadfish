#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hadfish import app
from hadfish.extensions import db
from hadfish.databases import *
from datetime import datetime

with app.test_request_context():
    # users = list()
    # for i in range(100):
        # user = User("user%d" % i, "user%d@hadfish.com" % i, "1")
        # users.append(user)

    # db.session.add_all(users)
    # item = ItemSale.query.get(1)
    # items = list()
    # for i in range(8 * 10):
        # rv = ItemDemand(item.name, item.price, item.kind_id)
        # rv.user_id = item.user_id
        # rv.images = item.images
        # items.append(rv)

    # db.session.add_all(items)

    # items = ItemSale.query.all()
    # for item in items:
        # if item.id != 1:
            # db.session.delete(item)

    user = User.query.filter_by(name="cloverstd").first()
    user.power =  99
    page = Page.query.all()
    for p in page:
        db.session.delete(p)
    db.session.commit()


    # print ItemSale.query.filter_by(kind_id=5).all()

