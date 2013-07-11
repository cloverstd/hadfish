#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hadfish import db
from hadfish.databases import *
from datetime import datetime
from time import sleep

db.create_all()

# image1 = Image(datetime.now())
# image2 = Image(datetime.now())
# item = Item("test", 1.2, 1, 0)
# item.images = [image1, image2]
# 
# user = User("test", "test", "test")
# user.items = [item]
# 
# db.session.add(user)
# db.session.commit()
# 
# i = User.query.first()
# print i.items[0]
# 
# for a in i.items[0].images:
    # print a.get_name()
