# -*- coding: utf-8 -*-

from flask import Module, render_template, request, flash, url_for, redirect,\
    session, g, abort
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from hadfish import config
from hadfish.extensions import db
from hadfish.databases import ItemSale, Image, Kind, User
from hadfish.images import upload_images, delete_images
from hadfish.utils import get_kind, check_price, qiniu_token


item = Module(__name__)


def get_items():
    """全部 items"""
    rv = ItemSale.query.all()
    items = list()
    for item in rv:
        images = list(img.name for img in item.images)
        kind = Kind.query.filter_by(id=item.kind_id).first().name
        item_dict = dict(id=item.id,
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
        items.append(item_dict)
    return dict(items=items)


def get_item_by_id(item_id):
    item = ItemSale.query.get(item_id)
    if item is None:
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
        if len(request.form["name"]) == 0:
            error = u"商品名称不能为空！"
        elif not check_price(request.form["original_price"]):
            error = u"原价应该为数字"
        elif not check_price(request.form["price"]):
            error = u"价格应该为数字"
        elif float(request.form["original_price"]) < 0:
            error = u"原价不能未0"
        elif float(request.form["price"]) < 0:
            error = u"价格不能未0"
        elif not check_price(request.form["valid_date"], "int"):
            error = u"有效期应该为数字"
        elif int(request.form["valid_date"]) <= 0 or \
                int (request.form["valid_date"]) > 150:
            error = u"有效日期无效"

        if error:
            flash(error, category="alert-error")
            return render_template("item/sale/add.html", kinds=get_kind(), 
                                   pre_data=request.form, token=qiniu_token())
        # print request.form["original_price"]
        images_name = request.form["img"].split(';')
        images = [Image(img) for img in images_name]
        item = ItemSale(request.form["name"], float(request.form["price"]),
                        request.form["level"], int(request.form["kind"]),
                        valid_date=int(request.form["valid_date"]),
                        original_price=int(request.form["original_price"]),
                        description=request.form["description"])
        item.images = images
        g.user.item_sales.append(item)
        db.session.add(item)
        db.session.commit()
        flash(u"恭喜，添加商品成功！", category="alert-success")
        return redirect(url_for("item_sale.show_item_by_id", item_id=item.id))
    return render_template("item/sale/add.html", kinds=get_kind(), token=qiniu_token())


@item.route("/item/sale/modify/<int:item_id>", methods=["GET", "POST"])
def modify_item(item_id):
    if not g.user:
        flash(u"请先登录", category="alert-warming")
        return redirect(url_for("account.login"))
    item = get_item_by_id(item_id)
    if item is None:
        abort(404)

    if request.method == "POST":
        error = None
        if len(request.form["name"]) == 0:
            error = u"商品名称不能为空！"
        elif not check_price(request.form["original_price"]):
            error = u"原价应该为数字"
        elif not check_price(request.form["price"]):
            error = u"价格应该为数字"
        elif float(request.form["original_price"]) < 0:
            error = u"原价不能未0"
        elif float(request.form["price"]) < 0:
            error = u"价格不能未0"
        elif not check_price(request.form["valid_date"], "int"):
            error = u"有效期应该为数字"
        elif int(request.form["valid_date"]) <= 0 or \
                int (request.form["valid_date"]) > 150:
            error = u"有效日期无效"

        if error:
            flash(error, category="alert-error")
            return render_template("item/sale/modify.html", item=item, kinds=get_kind(), 
                                   pre_data=request.form, token=qiniu_token())

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
        item_db.name = request.form["name"]
        item_db.original_price = float(request.form["original_price"])
        item_db.price = float(request.form["price"])
        item_db.kind = int(request.form["kind"])
        item_db.level = int(request.form["level"])
        item_db.valid_date = int(request.form["valid_date"])
        item_db.description = request.form["description"]
        db.session.commit()
        flash(u"修改完成", category="alert-success")
        return redirect(url_for("item_sale.show_item_by_id", item_id=item_id))
        return "test"

    return render_template("item/sale/modify.html", item=item, kinds=get_kind(),  token=qiniu_token())


@item.route("/item/sale/show/<int:item_id>")
def show_item_by_id(item_id):
    item = get_item_by_id(item_id)
    if item is None:
        abort(404)
    return render_template("item/sale/show.html", item=item, kinds=get_kind())
    

@item.route("/item/sale/show")
@item.route("/item/sale/all")
@item.route("/item/sale/")
@item.route("/item/sale")
def show_item():
    items = get_items()
    return render_template("item/sale/show_all.html", items=items)
