#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hadfish import app
from hadfish.extensions import db
from hadfish.databases import *
from random import randint
from datetime import datetime
from random import randint

with app.test_request_context():
    # users = list()
    # for i in range(100):
        # user = User("user%d" % i, "user%d@hadfish.com" % i, "1")
        # users.append(user)

    # db.session.add_all(users)
    # item = ItemSale.query.first()
    # items = list()
    # for i in range(8 * 10):
        # rv = ItemSale(item.name, item.price, item.original_price, randint(1, 4))
        # rv.user_id = item.user_id
        # rv.images = item.images
        # items.append(rv)

    # db.session.add_all(items)

    # items = ItemSale.query.all()
    # for item in items:
        # item.level = randint(0, 9)

    # user = User.query.filter_by(name="cloverstd").first()
    # user.power =  99
    # page = Page.query.all()
    # for p in page:
        # db.session.delete(p)
    # kinds = Kind.query.all()
    # for k in kinds:
        # print k.name, k.id
    users = User.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()


    # print ItemSale.query.filter_by(kind_id=5).all()

