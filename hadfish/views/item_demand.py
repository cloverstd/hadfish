# -*- coding: utf-8 -*-

from flask import Module, render_template, request, flash, url_for, redirect,\
    session, g, abort
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from hadfish.extensions import db
from hadfish.databases import Kind, User, ItemDemand
from hadfish import config
from hadfish.images import upload_images, delete_images
from hadfish.utils import get_kind, check_price, qiniu_token

item = Module(__name__)


def get_items(page=None):
    """全部 items"""
    if page is not None:
        rv = ItemDemand.query.order_by("id desc").paginate(page, config.PER_PAGE)
        items = list()
        for item in rv.items:
            items.append(get_item_by_id(item.id))
        rv = dict(demands=items,
                  has_next=rv.has_next,
                  has_prev=rv.has_prev,
                  next_num=rv.next_num,
                  prev_num=rv.prev_num,
                  pages=rv.pages,
                  page=rv.page)
        return rv
    rv = ItemDemand.query.all()
    items = list()
    for item in rv:
        items.append(get_item_by_id(item.id))
    rv = dict(demands=items, count=len(items))
    return rv


def get_item_by_id(item_id):
    item = ItemDemand.query.get(item_id)
    if item is None:
        return None
    kind = Kind.query.get(item.kind_id).name
    user = User.query.get(item.user_id)
    item = dict(id=item.id,
                name=item.name,
                price=item.price,
                valid_date=item.valid_date,
                date=item.date,
                description=item.description,
                kind_id=item.kind_id,
                kind=kind,
                is_sell=item.is_sell,
                is_visited=item.is_visited)
    user = dict(id=user.id,
                name=user.name,
                email=user.email,
                qq=user.qq,
                tel=user.tel,
                school=user.school,
                address=user.address,
                profile=user.profile,
                date=user.date,
                avatar=user.avatar)

    return dict(item=item, user=user)

@item.route("/item/demand/add", methods=["GET", "POST"])
def add_item():
    if not g.user:
        flash(u"请先登录", category="alert-warming")
        return redirect(url_for("account.login"))

    if request.method == "POST":
        error = None

        if request.form["name"] == '':
            error = u"名称不能为空"
        elif not check_price(request.form["price"]):
            error = u"价格应该为数字"
        elif float(request.form["price"]) < 0:
            error = u"价格不能未0"
        elif not check_price(request.form["valid_date"], "int"):
            error = u"有效期应该为数字"
        elif int(request.form["valid_date"]) <= 0 or \
                int(request.form["valid_date"]) > 150:
            error = u"有效日期无效"

        if error:
            flash(error, category="alert-error")
            return render_template("item/demand/add.html",
                                   kinds=get_kind(),
                                   pre_data=request.form)
        item = ItemDemand(name=request.form["name"],
                                 price=float(request.form["price"]),
                                 kind_id=request.form["kind"],
                                 valid_date=request.form["valid_date"],
                                 description=request.form["description"])
        g.user.item_demands.append(item)
        item.user_id = g.user.id
        db.session.add(item)
        db.session.commit()
        flash(u"发步需求成功", category="alert-success")
        return redirect(url_for("item_demand.show_item_by_id", item_id=item.id))
    return render_template("item/demand/add.html", kinds=get_kind())


@item.route("/item/demand/modify/<int:item_id>", methods=["GET", "POST"])
def modify_item(item_id):
    if not g.user:
        flash(u"请先登录", category="alert-warming")
        return redirect(url_for("account.login"))
    item = get_item_by_id(item_id)
    if g.user.id != item["user"]["id"]:
        flash(u"亲，无法修改别人的商品", category="alert-warming")
        return redirect(url_for("item_demand.show_item",
                        item_id=item["item"]["id"]))
    if item is None:
        abort(404)

    if request.method == "POST":
        error = None

        if request.form["name"] == '':
            error = u"名称不能为空"
        elif not check_price(request.form["price"]):
            error = u"价格应该为数字"
        elif float(request.form["price"]) < 0:
            error = u"价格不能未0"
        elif not check_price(request.form["valid_date"], "int"):
            error = u"有效期应该为数字"
        elif int(request.form["valid_date"]) <= 0 or \
                int(request.form["valid_date"]) > 150:
            error = u"有效日期无效"

        if error:
            flash(error, category="alert-error")
            return render_template("item/demand/modify.html",
                                   item=item,
                                   kinds=get_kind(),
                                   pre_data=request.form)
        item_db = ItemDemand.query.get(item_id)
        item_db.name = request.form["name"]
        item_db.price = float(request.form["price"])
        item_db.valid_date = int(request.form["valid_date"])
        item_db.kind_id = int(request.form["kind"])
        item_db.description = request.form["description"]
        db.session.commit()
        flash(u"修改完成", category="alert-success")
        return redirect(url_for("item_demand.show_item_by_id", item_id=item_id))

    return render_template("item/demand/modify.html",
                           item=item,
                           kinds=get_kind())


@item.route("/item/demand/show/<int:item_id>")
def show_item_by_id(item_id):
    item = get_item_by_id(item_id)
    if item is None:
        abort(404)
    return render_template("item/demand/show.html", item=item)


@item.route("/item/demand/", defaults={"page": 1})
@item.route("/item/demand/<int:page>")
def show_item(page):
    items = get_items(page)
    return render_template("item/demand/show_all.html", items=items)
