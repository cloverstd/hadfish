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
    date = db.Column(db.DateTime)
    avatar = db.Column(db.String(50))

    # Email validate
    is_validate = db.Column(db.Boolean)
    valid_time = db.Column(db.DateTime)
    valid_value = db.Column(db.String(32))

    disable = db.Column(db.Boolean)

    # 权限 99 最大权限，注册用户默认权限为 0
    power = db.Column(db.Integer(2))

    item_sales = db.relationship("ItemSale",
                                 backref="user", lazy="dynamic")
    item_demands = db.relationship("ItemDemand",
                                   backref="user", lazy="dynamic")

    # receive_msgs = db.relationship("Message",
                                   # backref="user", lazy="dynamic")
    # send_msgs = db.relationship("Message",
                                   # backref="user", lazy="dynamic")

    def __init__(self, name, email, password, tel='', qq='', school='',
                 address='', profile='', is_validate=False, avatar=''):
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
        self.power = 0
        self.disable = False

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
    description = db.Column(db.String(140))
    images = db.relationship("Image", backref="itemsales", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    kind_id = db.Column(db.Integer, db.ForeignKey("kind.id"))  # 分类
    is_sell = db.Column(db.Boolean)  # 售出
    is_visited = db.Column(db.Boolean)  # 是否隐藏

    def __init__(self, name, price, level, kind_id, is_sell=False,
                 is_visited=True, original_price='',
                 valid_date=150, description=''):
        self.name = name
        self.price = price
        self.level = level
        if not original_price:
            self.original_price = price
        else:
            self.original_price = original_price
        self.valid_date = valid_date
        self.description = description
        self.date = datetime.now()
        # self.images = images
        self.kind_id = kind_id
        self.is_sell = is_sell
        self.is_visited = is_visited

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
    # images = db.relationship("Image", backref="itemdemands", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    kind_id = db.Column(db.Integer, db.ForeignKey("kind.id"))  # 分类
    is_sell = db.Column(db.Boolean)  # 售出
    is_visited = db.Column(db.Boolean)  # 是否隐藏

    def __init__(self, name, price, kind_id, is_sell=False,
                 is_visited=True, description='', valid_date=150):
        self.name = name
        self.price = price
        self.description = description
        self.date = datetime.now()
        self.kind_id = kind_id
        self.is_sell = is_sell
        self.is_visited = is_visited
        self.valid_date = valid_date

    def __repr__(self):
        return "<ItemDemand %r>" % self.name


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # name 最大应该为 25
    name = db.Column(db.String(40))
    date = db.Column(db.DateTime)  # 文件名以日期保存
    item_sale_id = db.Column(db.Integer, db.ForeignKey("itemsales.id"))
    # item_demand_id = db.Column(db.Integer, db.ForeignKey("itemdemands.id"))

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


class Kind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(6), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Kind %r>" % self.name


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    send_time = db.Column(db.DateTime)
    content = db.Column(db.String(200))
    is_read = db.Column(db.Boolean)
    is_delete = db.Column(db.Boolean)

    def __init__(self, sender_id, receiver_id, content):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.send_time = datetime.now()
        self.is_read = False
        self.is_delete = False

    def __repr__(self):
        return "<Message %r>" % self.id


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    slug = db.Column(db.String(20), unique=True)
    content = db.Column(db.Text)
    content_title = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime)
    visitable = db.Column(db.Boolean)

    def __init__(self, slug, title, content, content_title):
        self.slug = slug
        self.title = title
        self.content_title = content_title
        self.content = content
        self.timestamp = datetime.now()
        self.visitable = True

    def __repr__(self):
        return "<Page %r>" % self.id


class SiteInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(256))
    domain = db.Column(db.String(128))

    # 七牛云储存
    qiniu_access_key = db.Column(db.String(40))
    qiniu_secret_key = db.Column(db.String(40))
    qiniu_bucket_avatar = db.Column(db.String(20))
    qiniu_bucket_img = db.Column(db.String(20))
    qiniu_domain_img = db.Column(db.String(128))
    qiniu_domain_avatar = db.Column(db.String(128))

    # 每页显示商品数目
    per_page = db.Column(db.Integer, default=20)

    def __repr__(self):
        return "<SiteInfo %r>" % self.id


class GroupOrder(db.Model):
    __tablename__ = "grouporder"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    tel = db.Column(db.String(11))
    address = db.Column(db.String(20))
    email = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime)
    num = db.Column(db.Integer(2))
    ok = db.Column(db.Boolean)

    def __init__(self, name, tel, address, email="", num=1):
        self.name = name
        self.tel = tel
        self.address = address
        self.email = email
        self.num = num
        self.timestamp = datetime.now()
        self.ok = False

    def __repr__(self):
        return "<GroupOrder %r>" % self.id
