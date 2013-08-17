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


@page.route("/help.html")
def page_help():
    return render_template("page/help.html")
