#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hadfish import app
from hadfish.extensions import db
from hadfish.databases import *
from random import randint
from datetime import datetime
from random import randint
from hashlib import md5
import json
# import MySQLdb


# con = MySQLdb.connect("localhost", "root", "xws2931336", "hadfish2", charset='utf8')

# cur = con.cursor(MySQLdb.cursors.DictCursor)

# cur.execute("SELECT userName, userPassword, userEmail, userFace, userQQ, userAddress, userCellphone, userRegtime FROM yy_user;")

# rows = cur.fetchall()

# con.close()
users_json = None
with open("hadfish.json") as fp:
    users_json = json.load(fp)

def import_user():
    users = list()
    for user in users_json:
        users.append(User(name=user["name"],
                          email=user["email"],
                          password=user["password"],
                          tel=user["tel"],
                          qq=user["qq"],
                          address=user["address"],
                          avatar=user["avatar"]))
    db.session.add_all(users)


with app.test_request_context():
    # import_user()
    u = User.query.filter_by(name="cloverstd").first()
    print u
    u.power = 99

    # me = User.query.filter_by(name="cloverstd").first()
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
    db.session.commit()


    # print ItemSale.query.filter_by(kind_id=5).all()

