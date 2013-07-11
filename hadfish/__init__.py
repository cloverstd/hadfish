# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from hadfish import config
from hadfish.views import account
from hadfish.extensions import db
from hadfish.databases import User, Item, Image
import os


os.environ["TZ"] = config.DEFAULT_TIMEZONE

app = Flask(__name__)
app.config.from_object("hadfish.config.DevConfig")

app.register_module(account)

# db = SQLAlchemy(app)
db.init_app(app)
