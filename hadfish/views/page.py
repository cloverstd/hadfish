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
import re
# import os.path

page = Module(__name__)


@page.route("/<slug>")
def page_ui(slug):
    p = Page.query.filter_by(slug=slug).first()

    if not p:
        abort(404)

    if not p.visitable:
        abort(404)
    return render_template("page/ui.html", page_title=p.title,
                           content_title=p.content_title,
                           content=p.content)
