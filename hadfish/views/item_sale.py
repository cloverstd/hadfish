# -*- coding: utf-8 -*-

from flask import Module, render_template, request, flash, url_for, redirect,\
    g, abort
from hadfish import config
from hadfish.extensions import db
from hadfish.databases import ItemSale, Image, Kind, User
from hadfish.utils import get_kind, check_price, qiniu_token


item = Module(__name__)


def get_items(page=None, kind_id=None):
    """全部 items"""
    if page is not None:
        if kind_id:
            rv = ItemSale.query.filter_by(kind_id=kind_id).filter_by(is_visited=True).order_by("id desc").paginate(page, config.PER_PAGE)
        else:
            rv = ItemSale.query.filter_by(is_visited=True).order_by("id desc").paginate(page, config.PER_PAGE)
        items = list()
        for item in rv.items:
            items.append(get_item_by_id(item.id, item=item))
        rv = dict(sales=items,
                  has_next=rv.has_next,
                  has_prev=rv.has_prev,
                  next_num=rv.next_num,
                  prev_num=rv.prev_num,
                  pages=rv.pages,
                  page=rv.page)
        return rv

    rv = ItemSale.query.filter_by(is_visited=True).all()
    items = list()
    for item in rv:
        # images = list(img.name for img in item.images)
        # kind = Kind.query.filter_by(id=item.kind_id).first().name
        # item_dict = dict(id=item.id,
                         # name=item.name,
                         # original_price=item.original_price,
                         # price=item.price,
                         # level=item.level,
                         # valid_date=item.valid_date,
                         # date=item.date,
                         # description=item.description,
                         # kind_id=item.kind_id,
                         # kind=kind,
                         # is_sell=item.is_sell,
                         # images=images,
                         # is_visited=item.is_visited)
        items.append(get_item_by_id(item.id))
    rv = dict(sales=items, count=len(items))
    return rv


def get_item_by_id(item_id, item=None):
    if item is None:
        item = ItemSale.query.get(item_id)
    else:
        item = item
    if item is None:
        return None
    elif not item.is_visited:
        return None
    images = list(img.name for img in item.images)
    kind = Kind.query.filter_by(id=item.kind_id).first().name
    user = User.query.get(item.user_id)
    item = dict(id=item.id,
                name=item.name,
                original_price=item.original_price,
                price=item.price,
                level=item.level,
                valid_date=item.valid_date,
                date=item.date,
                description=item.description,
                kind_id=item.kind_id,
                kind=kind,
                is_sell=item.is_sell,
                images=images,
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


@item.route("/item/sale/add", methods=["GET", "POST"])
def add_item():
    if not g.user:
        flash(u"请先登录", category="alert-warming")
        return redirect(url_for("account.login"))
    if request.method == "POST":
        error = None
        original_price = None
        if request.form["original_price"] == '':
            original_price = request.form["price"]

        if len(request.form["name"].strip()) == 0:
            error = u"商品名称不能为空！"
        elif len(request.form["name"]) > 80:
            error = u"商品名称需小于 80 个字"
        elif not check_price(request.form["price"]):
            error = u"价格应该为数字"
        elif float(request.form["price"]) < 0:
            error = u"价格不能未0"
        elif original_price is None and\
                not check_price(request.form["original_price"]):
            error = u"原价应该为数字"
        elif original_price is None and\
                float(request.form["original_price"]) < 0:
            error = u"原价不能未0"
        elif not check_price(request.form["valid_date"], "int"):
            error = u"有效期应该为数字"
        elif int(request.form["valid_date"]) <= 0 or \
                int(request.form["valid_date"]) > 150:
            error = u"有效日期无效"
        elif len(request.form["description"]) >= 140:
            error = u"描述不能超过 140 个字"

        if error:
            flash(error, category="alert-error")
            return render_template("item/sale/add.html", kinds=get_kind(),
                                   pre_data=request.form, token=qiniu_token())
        # print request.form["original_price"]
        item = ItemSale(request.form["name"].strip(), float(request.form["price"]),
                        request.form["level"], int(request.form["kind"]),
                        valid_date=int(request.form["valid_date"]),
                        original_price=float(request.form["original_price"])
                        if original_price is None else original_price,
                        description=request.form["description"].strip())
        if request.form["img"] != '':
            images_name = request.form["img"].split(';')
            images = [Image(img) for img in images_name]
            item.images = images
        g.user.item_sales.append(item)
        item.user_id = g.user.id
        db.session.add(item)
        db.session.commit()
        flash(u"恭喜，添加商品成功！", category="alert-success")
        return redirect(url_for("item_sale.show_item_by_id", item_id=item.id))
    return render_template("item/sale/add.html",
                           kinds=get_kind(),
                           token=qiniu_token())


@item.route("/item/sale/modify/<int:item_id>", methods=["GET", "POST"])
def modify_item(item_id):
    if not g.user:
        flash(u"请先登录", category="alert-warming")
        return redirect(url_for("account.login"))
    item = get_item_by_id(item_id)
    if item is None:
        abort(404)
    if g.user.id != item["user"]["id"]:
        flash(u"亲，无法修改别人的商品", category="alert-warming")
        return redirect(url_for("item_sale.show_item_by_id",
                        item_id=item["item"]["id"]))
    if item is None:
        abort(404)

    if request.method == "POST":
        error = None
        original_price = None
        if request.form["original_price"] == '':
            original_price = request.form["price"]

        if len(request.form["name"].strip()) == 0:
            error = u"商品名称不能为空！"
        elif len(request.form["name"]) > 80:
            error = u"商品名称需小于 80 个字"
        elif not check_price(request.form["price"]):
            error = u"价格应该为数字"
        elif float(request.form["price"]) < 0:
            error = u"价格不能未0"
        elif original_price is None and\
                not check_price(request.form["original_price"]):
            error = u"原价应该为数字"
        elif original_price is None and\
                float(request.form["original_price"]) < 0:
            error = u"原价不能未0"
        elif not check_price(request.form["valid_date"], "int"):
            error = u"有效期应该为数字"
        elif int(request.form["valid_date"]) <= 0 or \
                int(request.form["valid_date"]) > 150:
            error = u"有效日期无效"
        elif len(request.form["description"]) >= 140:
            error = u"描述不能超过 140 个字"

        if error:
            flash(error, category="alert-error")
            return render_template("item/sale/modify.html",
                                   item=item,
                                   kinds=get_kind(),
                                   pre_data=request.form,
                                   token=qiniu_token())

        item_db = ItemSale.query.get(item_id)
        images_name = request.form["img"].split(';')
        # images = [Image(img) for img in images_name]
        images = list()
        for img in images_name:
            img_db = Image.query.filter_by(name=img).first()
            if img_db is None:
                images.append(Image(img))
            else:
                images.append(img_db)

        item_db.images = images
        item_db.name = request.form["name"].strip()
        item_db.original_price = float(request.form["original_price"])\
            if original_price is None else original_price
        item_db.price = float(request.form["price"])
        item_db.kind = int(request.form["kind"])
        item_db.level = int(request.form["level"])
        item_db.valid_date = int(request.form["valid_date"])
        item_db.description = request.form["description"].strip()
        db.session.commit()
        flash(u"修改完成", category="alert-success")
        return redirect(url_for("item_sale.show_item_by_id", item_id=item_id))

    return render_template("item/sale/modify.html",
                           item=item,
                           kinds=get_kind(),
                           token=qiniu_token())


@item.route("/item/sale/show/<int:item_id>")
def show_item_by_id(item_id):
    item = get_item_by_id(item_id)
    if item is None:
        abort(404)
    return render_template("item/sale/show.html", item=item, kinds=get_kind())


# @item.route("/item/sale/show")
# @item.route("/item/sale/all")
@item.route("/item/sale/", defaults={"page": 1})
@item.route("/item/sale/<int:page>")
def show_item(page):
    kind_id = None
    if "kind_id" in request.args:
        kind_id = int(request.args["kind_id"])
        items = get_items(page, kind_id)
    else:
        items = get_items(page)
    # items = ItemSale.query.paginate(page, 2)
    return render_template("item/sale/show_all.html", items=items, kinds=get_kind(), kind_id=kind_id)


@item.route("/item/sale/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    if not g.user:
        flash(u"请先登录", category="alert-warming")
        return redirect(url_for("account.login"))
    item = get_item_by_id(item_id)
    if item is None:
        abort(404)        
    if g.user.id != item["user"]["id"]:
        flash(u"亲，无法删除别人的商品", category="alert-warming")
        return redirect(url_for("item_sale.show_item_by_id",
                        item_id=item["item"]["id"]))

    if request.method == "POST":
        db.session.delete(ItemSale.query.get(item_id))
        db.session.commit()
        flash(u"亲，删除成功", category="alert-success")
        return redirect(url_for("item_sale.show_item"))

