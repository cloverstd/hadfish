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
    if slug == "help":
        page_title = u"帮助"
        content_title = u"帮助中心"
        content = u"""
<ul>
    <li>
        <h1>如何成为有鱼网的用户</h1>
        <br>  第一，在网站的首页的轮播图上点击注册，也可以点击网站最上方导航栏的注册，进入注册页面后，一次输入用户名，密码，重复密码，注册邮箱即可。</br>
    　　 <br>  第二，注册完成后点击进入个人主页，点击修改资料，上传照片（最好是本人照片，增加可信度），再点击基本信息，输入个人真实信息，以备交易时使用。</br>
    　　 <br>  第三，回到个人主页，点击我要卖，上传需要出售的商品，等待出售。</br>
    　 　<br>  第四，与买家达成协议后，进行交易，交易完成之后下架商品。
    </li>
    <li>
        <h1></h1>
        <p></p>
    </li>
</ul>
        """
    else:
        abort(404)
    return render_template("page/ui.html", page_title=page_title,
                           content_title=content_title,
                           content=content)
