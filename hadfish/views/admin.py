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
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)

    return render_template("manage/index.html")


#### 页面管理 ####
@admin.route("/manage/page")
def page_show():
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)

    pages = Page.query.all()


    return render_template("manage/page_show.html", pages=pages)


@admin.route("/manage/page/disable/<int:pid>", methods=["POST"])
def disable(pid):
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)
    p = Page.query.get(pid)
    p.visitable = False
    db.session.commit()
    return redirect(url_for("admin.page_show"))


@admin.route("/manage/page/enable/<int:pid>", methods=["POST"])
def enable(pid):
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)
    p = Page.query.get(pid)
    p.visitable = True
    db.session.commit()
    return redirect(url_for("admin.page_show"))

@admin.route("/manage/page/add", methods=["GET", "POST"])
def page_add():
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)

    if request.method == "POST":
        page = Page(title=request.form["page-title"].strip(),
                    slug=request.form["page-slug"],
                    content=request.form["content"],
                    content_title=request.form["content-title"])

        db.session.add(page)
        db.session.commit()

        return redirect(url_for("page.page_ui", slug=page.slug))
    return render_template("manage/page_add.html")


# @admin.route("/manage/page/del", methods=["POST"])
# def page_del():
    # return "page del"


@admin.route("/manage/page/mod/<int:pid>", methods=["GET", "POST"])
def page_mod(pid):
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)

    page = Page.query.get(pid)
    if not page:
        abort(404)

    print "test"
    if request.method == "POST":
        page.title = request.form["page-title"].strip()
        page.content = request.form["content"]
        page.content_title = request.form["content-title"]
        db.session.commit()
        return redirect(url_for("page.page_ui", slug=page.slug))
    return render_template("manage/page_mod.html", page=page)




#### 用户管理 ####

@admin.route("/manage/user", defaults={"page": 1})
@admin.route("/manage/user/page/<int:page>")
def user_show(page):
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)
    users = User.query.paginate(page, 50, False)

    return render_template("manage/user_show.html", users=users.items,
                           page=users)



#### 团购管理 ####
@admin.route("/manage/group")
def group_show():
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)
    orders = GroupOrder.query.all()

    return render_template("manage/group_order.html", orders=orders)



@admin.route("/manage/group/ok/<int:oid>", methods=["POST"])
def group_ok(oid):
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)
    order = GroupOrder.query.get(oid)
    order.ok = True

    db.session.commit()

    return redirect(url_for("admin.group_show"))


#### 出售商品管理 ####
@admin.route("/manage/item/sale", defaults={"page":1})
@admin.route("/manage/item/sale/page/<int:page>")
def sale_show(page):
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)

    sales = ItemSale.query.paginate(page, 50, False)
    return render_template("manage/item_sale.html", items=sales.items,
                           page=sales)

@admin.route("/manage/item/sale/<int:item_id>/disable", methods=["POST"])
def sale_disable(item_id):
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)

    sale = ItemSale.query.get(item_id)
    sale.is_visited = False
    db.session.commit()

    return redirect(url_for("admin.sale_show"))


@admin.route("/manage/item/sale/<int:item_id>/enable", methods=["POST"])
def sale_enable(item_id):
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)

    sale = ItemSale.query.get(item_id)
    sale.is_visited = True
    db.session.commit()

    return redirect(url_for("admin.sale_show"))



#### 出售商品管理 ####
@admin.route("/manage/item/demand", defaults={"page":1})
@admin.route("/manage/item/demand/page/<int:page>")
def demand_show(page):
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)

    demands = ItemDemand.query.paginate(page, 50, False)
    return render_template("manage/item_demand.html", items=demands.items,
                           page=demands)

@admin.route("/manage/item/demand/<int:item_id>/disable", methods=["POST"])
def demand_disable(item_id):
    if not g.user:
        abort(404)
    elif g.user.power != 99:
        abort(404)

    demand = ItemDemand.query.get(item_id)
    demand.is_visited = False
    db.session.commit()

    return redirect(url_for("admin.demand_show"))


@admin.route("/manage/item/demand/<int:item_id>/enable", methods=["POST"])
def demand_enable(item_id):
    if not g.user:
        ort(404)
    if g.user.power != 99:
        abort(404)

    demand = ItemDemand.query.get(item_id)
    demand.is_visited = True
    db.session.commit()

    return redirect(url_for("admin.demand_show"))
