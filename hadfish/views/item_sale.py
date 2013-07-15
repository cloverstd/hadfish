# -*- coding: utf-8 -*-

from flask import Module, render_template, request, flash, url_for, redirect,\
    session, g, abort
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from hadfish import config
from hadfish.extensions import db
from hadfish.images import upload_images, delete_images

item = Module(__name__)


def get_items():
    """全部 items"""
    pass

@item.route("/item/sale/add", methods=["GET", "POST"])
def add_item():
    return render_template("item/sale/add.html")


@item.route("/item/sale/modify/<int:item_id>", methods=["GET", "POST"])
def modify_item(item_id):
    return "modify_item sale"


@item.route("/item/sale/show/<int:item_id>")
@item.route("/item/sale/show", defaults={"item_id": None})
@item.route("/item/sale/all", defaults={"item_id": None})
@item.route("/item/sale", defaults={"item_id": None})
def show_item(item_id):
    return "show_item sale"
