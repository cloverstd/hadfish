# -*- coding: utf-8 -*-
from hadfish.extensions import db
from datetime import datetime


# MySQL 中 一个汉字是一个位
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

    tel = db.Column(db.String(12))
    qq = db.Column(db.String(15))
    school = db.Column(db.String(20))
    address = db.Column(db.String(140))
    profile = db.Column(db.String(140))
    is_validate = db.Column(db.Boolean)
    date = db.Column(db.DateTime)
    avatar = db.Column(db.String(50))

    items = db.relationship("Item", backref="user", lazy="dynamic")

    def __init__(self, name, email, password, tel=None, qq=None, school=None,
                 address=None, profile=None, is_validate=False, avatar=None):
        self.name = name
        self.email = email
        self.password = password
        self.tel = tel
        self.qq = qq
        self.address = address
        self.profile = profile
        self.school = school
        self.is_validate = is_validate
        self.avatar = avatar
        self.date = datetime.now()

    def __repr__(self):
        return "<User %r>" % (self.name)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    original_price = db.Column(db.Float)
    price = db.Column(db.Float)
    level = db.Column(db.Integer(1))    # 新旧程度，0-9成新, 0 表示1，9 表示10
    date = db.Column(db.DateTime)  # 上架时间
    valid_date = db.Column(db.Integer(3))  # 最长时间 150 天
    description = db.Column(db.Integer(140))
    type = db.Column(db.Integer(1))  # 0 表示出售，1 表示求购
    # classify 外键
    images = db.relationship("Image", backref="item", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, name, price, level, type, original_price=None,
                 valid_date=150, description=None):
        self.name = name
        self.price = price
        self.level = level
        self.type = type
        if not original_price:
            self.original_price = price
        self.valid_date = valid_date
        self.description = description
        self.date = datetime.now()
        # self.images = images

    def __repr__(self):
        return "<Item %r>" % (self.name)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    date = db.Column(db.DateTime)  # 文件名以日期保存
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))

    def __init__(self, name):
        self.name = name
        self.date = datetime.now()

    def get_name(self, suffix="jpg"):
        return "%s.%s" % (self.date.strftime("%Y%m%d%H%M%S%s"), suffix)

    def __repr__(self):
        return "<Image %r>" % (self.date)
