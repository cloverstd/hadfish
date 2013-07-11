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
    item = Item("test", 1.2, 1, 0)
    item.images = [image1, image2]
    # 
    user = User("test", "test", "test")
    user.items = [item]
    # 
    db.session.add(user)
    db.session.commit()
    # 
    i = User.query.first()
    print i.items[0]
    # 
    for a in i.items[0].images:
        print a.get_name()
