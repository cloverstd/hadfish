# -*- coding: utf-8 -*-
from hadfish.extensions import db
from datetime import datetime


# MySQL 中 一个汉字是一个位
class User(db.Model):
    # TODO 用户收藏，用户浏览记录
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

    item_sales = db.relationship("ItemSale",
                                 backref="user", lazy="dynamic")
    item_demands = db.relationship("ItemDemand",
                                   backref="user", lazy="dynamic")

    def __init__(self, name, password, email, tel=None, qq=None, school=None,
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


class ItemSale(db.Model):
    __tablename__ = "itemsales"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    original_price = db.Column(db.Float)
    price = db.Column(db.Float)
    level = db.Column(db.Integer(1))    # 新旧程度，0-9成新, 0 表示1，9 表示10
    date = db.Column(db.DateTime)  # 上架时间
    valid_date = db.Column(db.Integer(3))  # 最长时间 150 天
    description = db.Column(db.Integer(140))
    # TODO classify 外键 类型
    # TODO 相关链接
    images = db.relationship("Image", backref="itemsales", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, name, price, level, original_price=None,
                 valid_date=150, description=None):
        self.name = name
        self.price = price
        self.level = level
        if not original_price:
            self.original_price = price
        self.valid_date = valid_date
        self.description = description
        self.date = datetime.now()
        # self.images = images

    def __repr__(self):
        return "<Item %r>" % (self.name)


class ItemDemand(db.Model):
    __tablename__ = "itemdemands"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    description = db.Column(db.String(140))
    date = db.Column(db.DateTime)
    valid_date = db.Column(db.Integer(3))
    # TODO classify 外键 类型
    images = db.relationship("Image", backref="itemdemands", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, name, price=0, description=None, valid_date=150):
        self.name = name
        self.price = price
        self.description = description
        self.date = datetime.now()

    def __repr__(self):
        return "<ItemDemand %r>" % self.name


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    date = db.Column(db.DateTime)  # 文件名以日期保存
    item_sale_id = db.Column(db.Integer, db.ForeignKey("itemsales.id"))
    item_demand_id = db.Column(db.Integer, db.ForeignKey("itemdemands.id"))

    def __init__(self, name):
        self.name = name
        self.date = datetime.now()

    def get_name(self, suffix="jpg"):
        return "%s.%s" % (self.date.strftime("%Y%m%d%H%M%S%s"), suffix)

    def __repr__(self):
        return "<Image %r>" % (self.date)


# class Setting(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # allow_register = db.Column(db.Boolean, default=False)  # 允许注册
    # allow_email_validate = db.Column(db.Boolean, default=False)  # 允许邮箱验证
    # # 七牛 key
    # qiniu_access_key = db.Column(db.String(100))
    # qiniu_access_key = db.Column(db.String(100))
