# -*- coding: utf-8 -*-

from flask import Module, render_template, request, flash, url_for, redirect,\
    session, g, abort
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from hadfish.utils import check_password_hash, generate_password_hash,\
    allowed_file, rename_image, get_avatar_name
from hadfish.extensions import db, mail
from hadfish.databases import User
from hadfish import config
from hadfish.images import upload_images, delete_images
from hashlib import md5
from datetime import datetime
# import os.path

admin = Module(__name__)
