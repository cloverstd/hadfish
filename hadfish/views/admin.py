# -*- coding: utf-8 -*-

from flask import Module, render_template, request, flash, url_for, redirect,\
    session, g, abort, jsonify
from hadfish.utils import check_password_hash, generate_password_hash
from hadfish.extensions import db, mail
from hadfish.databases import *
from hadfish import config
from hadfish.images import upload_images, delete_images
from hashlib import md5
from datetime import datetime
# import os.path

admin = Module(__name__)


def error(msg, code):
    return dict(errmsg=msg, errcode=code)


def success(msg, code=1):
    return dict(msg=msg, code=code)


def get_user():
    rv = User.query.filter(User.power < 99).all()
    users = list()
    for user in rv:
        users.append(dict(id=user.id,
                          name=user.name,
                          email=user.email,
                          qq=user.qq,
                          tel=user.tel,
                          school=user.school,
                          address=user.address,
                          profile=user.profile,
                          date=user.date,
                          avatar=user.avatar,
                          is_validate=user.is_validate
                  ))
    return users
    # rv = dict(users=users, count=len(rv))
    # return rv


def get_sale(page):
    rv = ItemSale.query.order_by(ItemSale.id.desc()).pagination(page, config.PEE_PAGE)
    return rv

# 管理界面
@admin.route("/manage")
def index():
    return render_template("manage/index.html")


######################## 用户管理 ##########################
# error code 说明
# 100 没有登录
# 101 缺少必要参数 username, 或者 username 为空
# 102 缺少必要参数 password，或者 password 为空
# 103 缺少必要参数 email，或者 email 为空
# 104 email 已经存在
# 105 username 已经存在
@admin.route("/manage/user")
def user():
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))

    rv = get_user()
    return jsonify(users=rv, count=len(rv))


@admin.route("/manage/user/add", methods=["POST"])
def user_add():
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))

    if request.form.get("username", "") != "":
        username = request.form["username"].strip()
    else:
        return jsonify(error("username is required", 101))

    if request.form.get("password", "") != "":
        password = request.form["password"]
    else:
        return jsonify(error("password is required", 102))

    if request.form.get("email", "") != "":
        email = request.form["email"].strip()
    else:
        return jsonify(error("email is required", 103))

    if User.query.filter_by(name=username).first():
        return jsonify(error("username is existence", 104))

    if User.query.filter_by(email=email).first():
        return jsonify(error("email is existence", 105))

    user = User(request.form["username"], request.form["email"],
                generate_password_hash(request.form["password"],
                                       config.PASSWORD_KEY),
                tel=request.form.get("tel", "").strip(), qq=request.form.get("QQ", "").strip(),
                school=u"上海建桥学院", profile=u"")
                # address=request.form["address"])

    db.session.add(user)
    db.session.commit()
    return jsonify(user=dict(name=user.name,
                        email=user.email,
                        qq=user.qq,
                        tel=user.tel,
                        school=user.school,
                        address=user.address,
                        profile=user.profile,
                        date=user.date,
                        avatar=user.avatar,
                        is_validate=user.is_validate
                        ))


@admin.route("/manage/user/modify")
def user_mod():
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))

    if request.form.get("id", "") != "":
        uid = request.form["id"]
    else:
        return jsonify(error("id is required", 106))

    user = User.query.get(uid)
    if user is None:
        return jsonify(error("id is not existence"), 110)

    if "username" in request.form:
        if request.form["username"] != "":
            user.name = request.form["username"]
        else:
            return jsonify(error("username is null", 107))

    if "password" in request.form:
        if request.form["password"] != "":
            user.password = generate_password_hash(request.form["password"],
                                                   config.PASSWORD_KEY),
        else:
            return jsonify(error("password is null", 108))

    if "email" in request.form:
        if request.form["email"] != "" and "@" in request.form["email"]:
            user.email = request.form["email"]
            user.is_validate = False
        else:
            return jsonify(error("email is null or email is wrong", 109))
    
    if "qq" in request.form:
        user.qq = request.form["qq"]

    if "tel" in request.form:
        user.tel = request.form["tel"]

    if "address" in request.form:
        user.address = request.form["address"]

    if "profile" in request.form:
        user.profile = request.form["profile"]

    if "avatar" in request.form:
        user.avatar = request.form["avatar"]

    db.session.commit()
    return jsonify(user=dict(name=user.name,
                        email=user.email,
                        qq=user.qq,
                        tel=user.tel,
                        school=user.school,
                        address=user.address,
                        profile=user.profile,
                        date=user.date,
                        avatar=user.avatar,
                        is_validate=user.is_validate
                        ))


@admin.route("/manage/user/disable/<int:uid>")
def user_disable(uid):
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))
    
    if request.form.get("id", "") != "":
        uid = request.form["id"]
    else:
        return jsonify(error("id is required", 106))

    user = User.query.get(uid)
    if user is None:
        return jsonify(error("id is not existence"), 110)

    user.disable = True
    db.session.commit()
    return jsonify(success("user had disabled"))


@admin.route("/manage/user/enable/<int:uid>")
def user_enable(uid):
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))
    
    if request.form.get("id", "") != "":
        uid = request.form["id"]
    else:
        return jsonify(error("id is required", 106))

    user = User.query.get(uid)
    if user is None:
        return jsonify(error("id is not existence"), 110)

    user.disable = False
    db.session.commit()
    return jsonify(success("user had enabled"))


@admin.route("/manage/user/delete/<int:uid>")
def user_del(uid):
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))

    if not g.user and g.user.power < 99:
        return jsonify(error("not login", 100))
    
    if request.form.get("id", "") != "":
        uid = request.form["id"]
    else:
        return jsonify(error("id is required", 106))

    user = User.query.get(uid)
    if user is None:
        return jsonify(error("id is not existence"), 110)

    db.session.delete(user)
    db.session.commit()
    return jsonify(success("user had deleted"))


######################## 出售订单管理 ##########################
@admin.route("/manage/item/sale")
def item_sale():
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))
    return "item sale manage"


@admin.route("/manage/item/sale/modify/<int:item_id>")
def item_sale_mod(item_id):
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))
    return "item sale mod manage"


@admin.route("/manage/item/sale/delete/<int:item_id>")
def item_sale_del(item_id):
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))
    return "item sale del manage"


@admin.route("/manage/item/sale/disable/<int:item_id>")
def item_sale_disable(item_id):
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))
    return "item sale disable manage"


@admin.route("/manage/item/sale/enable/<int:item_id>")
def item_sale_enable(item_id):
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))
    return "item sale enable manage"


######################## 求购订单管理 ##########################
@admin.route("/manage/item/demand")
def item_demand():
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))
    return "item demand manage"


@admin.route("/manage/item/demand/modify/<int:item_id>")
def item_demand_mod(item_id):
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))
    return "item demand mod manage"


@admin.route("/manage/item/demand/delete/<int:item_id>")
def item_demand_del(item_id):
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))
    return "item demand del manage"


@admin.route("/manage/item/demand/disable/<int:item_id>")
def item_demand_disable(item_id):
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))
    return "item demand disable manage"


@admin.route("/manage/item/demand/enable/<int:item_id>")
def item_demand_enable(item_id):
    if not g.user:
        return jsonify(error("not login", 100))
    elif g.user.power < 99:
        return jsonify(error("not login", 100))
    return "item demand enable manage"
