# -*- coding: utf-8 -*-

from flask import Module, render_template, request, flash, url_for, redirect,\
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from hadfish.extensions import db
from hadfish import config
from hadfish.images import upload_images, delete_images

item = Module(__name__)


def get_items():
    """全部 items"""
    pass

@item.route("/item/sale/add", methods=["GET", "POST"])
def add_item():
    return "add_item"


@item.route("/item/modify/<int:item_id>", methods=["GET", "POST"])
def modify_item(item_id):
    return "modify_item"


@item.route("/item/show/<int:item_id>")
@item.route("/item/show", defaults={"item_id": None})
@item.route("/item/all", defaults={"item_id": None})
@item.route("/item/", defaults={"item_id": None})
def show_item(item_id):
    return "show_item"
