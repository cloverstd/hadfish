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


def get_items(page=None, kind_id=None):
    """全部 items"""
    if page is not None:
        if kind_id:
            rv = ItemDemand.query.filter_by(is_visited=True).filter_by(kind_id=kind_id).order_by("id desc").paginate(page, config.PER_PAGE)
        else:
            rv = ItemDemand.query.filter_by(is_visited=True).order_by("id desc").paginate(page, config.PER_PAGE)
        items = list()
        for item in rv.items:
            items.append(get_item_by_id(item.id, item))
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


def get_item_by_id(item_id, item=None):
    if item is None:
        item = ItemDemand.query.get(item_id)
    else:
        item = item

    if item is None:
        return None
    elif not item.is_visited:
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

        if request.form["name"].strip() == '':
            error = u"名称不能为空"
        elif len(request.form["name"]) >= 140:
            error = u"名称不能大于 80 个字"
        elif not check_price(request.form["price"]):
            error = u"价格应该为数字"
        elif float(request.form["price"]) < 0:
            error = u"价格不能未0"
        elif not check_price(request.form["valid_date"], "int"):
            error = u"有效期应该为数字"
        elif int(request.form["valid_date"]) <= 0 or \
                int(request.form["valid_date"]) > 150:
            error = u"有效日期无效"
        elif len(request.form["description"]) >= 140:
            error = u"描述不能超过 140 个字"

        if error:
            flash(error, category="alert-error")
            return render_template("item/demand/add.html",
                                   kinds=get_kind(),
                                   pre_data=request.form)
        item = ItemDemand(name=request.form["name"].strip(),
                                 price=float(request.form["price"]),
                                 kind_id=int(request.form["kind"]),
                                 valid_date=int(request.form["valid_date"]),
                                 description=request.form["description"].strip())
        g.user.item_demands.append(item)
        item.user_id = g.user.id
        db.session.add(item)
        db.session.commit()
        flash(u"发步需求成功", category="alert-success")
        return redirect(url_for("item_demand.show_item_by_id", item_id=item.id))
    return render_template("item/demand/add.html", kinds=get_kind())


@item.route("/item/demand/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    if not g.user:
        flash(u"请先登录", category="alert-warming")
        return redirect(url_for("account.login"))
    item = get_item_by_id(item_id)
    if item is None:
        abort(404)        
    if g.user.id != item["user"]["id"]:
        flash(u"亲，无法删除别人的商品", category="alert-warming")
        return redirect(url_for("item_demand.show_item_by_id",
                        item_id=item["item"]["id"]))

    if request.method == "POST":
        db.session.delete(ItemDemand.query.get(item_id))
        db.session.commit()
        flash(u"亲，删除成功", category="alert-success")
        return redirect(url_for("item_demand.show_item"))


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

        if request.form["name"].strip() == '':
            error = u"名称不能为空"
        elif len(request.form["name"]) > 80:
            error = u"名称不能超过 80 个字"
        elif not check_price(request.form["price"]):
            error = u"价格应该为数字"
        elif float(request.form["price"]) < 0:
            error = u"价格不能未0"
        elif not check_price(request.form["valid_date"], "int"):
            error = u"有效期应该为数字"
        elif int(request.form["valid_date"]) <= 0 or \
                int(request.form["valid_date"]) > 150:
            error = u"有效日期无效"
        elif len(request.form["description"]) >= 140:
            error = u"描述不能超过 140 个字"

        if error:
            flash(error, category="alert-error")
            return render_template("item/demand/modify.html",
                                   item=item,
                                   kinds=get_kind(),
                                   pre_data=request.form)
        item_db = ItemDemand.query.get(item_id)
        item_db.name = request.form["name"].strip()
        item_db.price = float(request.form["price"])
        item_db.valid_date = int(request.form["valid_date"])
        item_db.kind_id = int(request.form["kind"])
        item_db.description = request.form["description"].strip()
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
    kind_id = None
    if "kind_id" in request.args:
        kind_id = int(request.args["kind_id"])
        items = get_items(page, kind_id)
    else:
        items = get_items(page)
    return render_template("item/demand/show_all.html", items=items, kinds=get_kind(), kind_id=kind_id)
