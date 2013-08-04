#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hadfish import app
from hadfish.extensions import db
from hadfish.databases import *
from datetime import datetime

with app.test_request_context():
    rv = ItemSale.query.get(2)
    user_id = rv.user_id
    items = ItemSale.query.all()
    for item in items:
        if not item.user_id:
            item.user_id = user_id
    db.session.commit()
