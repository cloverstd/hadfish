# -*- coding: utf-8 -*-

from flask import Flask, g, session
from flask.ext.sqlalchemy import SQLAlchemy
from hadfish import config
from hadfish.views import account, item_sale, item_demand, common
from hadfish.extensions import db
# from hadfish.databases import User, ItemSale, Image
from hadfish.databases import *
import os


os.environ["TZ"] = config.DEFAULT_TIMEZONE

app = Flask(__name__)
app.config.from_object("hadfish.config.DevConfig")

app.register_module(account)
app.register_module(item_sale)
app.register_module(item_demand)
app.register_module(common)

# db = SQLAlchemy(app)
db.init_app(app)

@app.before_request
def before_request():
    g.user = None
    if "user_id" in session:
        g.user = User.query.get(session["user_id"])
        
        
# 模版过滤器
@app.template_filter("date_format")
def date_format(date):
    return u"%s年%s月%s日" % (date.year, date.month, date.day)


@app.template_filter("avatar_url")
def get_avatar(avatar):
    return u"%s/%s" % (config.QINIU_DOMAIN_AVATAR, avatar)
