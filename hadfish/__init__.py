# -*- coding: utf-8 -*-

from flask import Flask, g, session
# from flask.ext.sqlalchemy import SQLAlchemy
from hadfish import config
from hadfish.views import account, item_sale, item_demand, common, message, admin
from hadfish.extensions import db, mail
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
app.register_module(message)
app.register_module(admin)

# db = SQLAlchemy(app)
db.init_app(app)
mail.init_app(app)

@app.before_request
def before_request():
    g.user = None
    if "user_id" in session:
        g.user = User.query.get(session["user_id"])
        
        
# 模版过滤器
@app.template_filter("date_format")
def filter_date_format(date):
    return u"%s年%s月%s日" % (date.year, date.month, date.day)


@app.template_filter("avatar_url")
def filter_get_avatar(avatar):
    return u"%s/%s" % (config.QINIU_DOMAIN_AVATAR, avatar)


@app.template_filter("level_format")
def filter_level_format(level):
    rv = [u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"全新"]
    return rv[level]
