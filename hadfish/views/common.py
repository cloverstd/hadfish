# -*- coding: utf-8 -*-

from flask import Module, request, flash, g, render_template
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from hadfish import config
from hadfish.images import upload_images, delete_images
from hadfish.utils import rename_image, allowed_file
from time import sleep
from hadfish.extensions import db
from hadfish.databases import ItemSale, Image, Kind, User
from hashlib import md5

common = Module(__name__)

def get_items(page=None, kind_id=None):
    """全部 items"""
    if page is not None:
        if kind_id:
            rv = ItemSale.query.filter_by(kind_id=kind_id).order_by("id desc").paginate(page, config.PER_PAGE)
        else:
            rv = ItemSale.query.order_by("id desc").paginate(page, config.PER_PAGE)
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

    rv = ItemSale.query.all()
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

@common.route("/upload/image", methods=["POST"])
def upload_image():
    # Just for a test
    # sleep(0.5)

    try:
        file = request.files["Filedata"]
    except RequestEntityTooLarge:
        #flash(u"只允许上传 5MB 以下的图片，谢谢", category="alert-error")
        return "ERROR"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = rename_image(filename, md5(file.stream.read()).hexdigest())
        # file.save(os.path.join("hadfish/hadfish/static/img", filename))
        # 上传二进制流到七牛
        if not upload_images(config.QINIU_BUCKET,
                             filename, file.stream):
            # flash(u"修改头像失败，请重试", categoty="alert-warming")
            print "test"
            return "ERROR"
        return "FILENAME:%s" % filename
    else:
        flash(u"文件格式不支持", category="alert-error")
    return "ERROR"


@common.route("/")
def index():
    return render_template("index.html", items=get_items())
