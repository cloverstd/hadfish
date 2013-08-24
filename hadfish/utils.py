#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hashlib import md5
from hadfish import config
from datetime import datetime
from hadfish.databases import *
import json
import hmac
from hashlib import sha1
from hadfish import config
from time import time
from base64 import urlsafe_b64encode
from hadfish.extensions import mail


def generate_password_hash(password, key=None):
    return md5("%s%s" % (password, key)).hexdigest()


def check_password_hash(hash_password, password, key=None):
    if hash_password == generate_password_hash(password, key):
        return True
    return False


def allowed_file(filename, file_extensions=None):
    """检查上传的文件名是否符合要求"""
    file_extensions = config.ALLOWED_EXTENSIONS \
        if not file_extensions else set(file_extensions)
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in file_extensions

# def exchange_img_name(original_name, name):
#     """转换 original_name 为 name，保持后缀不变


def rename_image(before, after):
    """例如，rename_images("test.jpg", "123")"""
    after = str(after)
    if before[-3:] == "jpg" or before[-3:] == "png":
        after += before[-4:]
    else:
        after += before[-5:]
    return after


def get_avatar_name(uid):
    """uid + microsecond 转换成 16 进制，去掉 0x"""
    # 此处用 BUG，用户量超过 100w 可能出现 BUG， 为了上传头像即时刷新所做的处理
    name = "%.6d%.6d" % (uid, datetime.now().microsecond)
    return hex(int(name))[2:]


def get_kind():
    kinds = Kind.query.all()
    rv = list()
    for k in kinds:
        rv.append(dict(id=k.id, name=k.name))

    return dict(kinds=rv)


def date_string():
    return "%s" % (datetime.now().strftime("%Y%m%d%H%M%S%s"))


def check_price(value, check_type="float"):
    """检查 value 是否为数字"""
    try:
        if check_type == "float":
            float(value)
        else:
            int(value)
        return True
    except ValueError:
        return False


def qiniu_token(scope=config.QINIU_BUCKET):
    auth_info = {"scope": scope,
                 "deadline": int(time() + 600),
                 # "callbackUrl": "http://pi.hui.lu:8080/upload",
                 "callbackBodyType": "application/json",
                 # "customer": "customer",
                 # "escape": 1,
                 # "asyncOps": "",
                 # "returnBody": '{"name": $(fname)}',
                 }
    auth_info_encoded = urlsafe_b64encode(json.dumps(auth_info))
    mac = hmac.new(config.QINIU_SECRET_KEY, auth_info_encoded, sha1)
    auth_digest = mac.digest()
    auth_digest_encoded = urlsafe_b64encode(auth_digest)
    return "%s:%s:%s" % (config.QINIU_ACCESS_KEY,
                         auth_digest_encoded, auth_info_encoded)


# 注册邮件
def send_mail(recipients, **args):
    subject = None
    html = None
    if "subject" in args:
        subject = args["subject"]

    if "body" in args:
        html = args["body"]

    return mail.send_message(subject=subject,
                             recipients=[recipients],
                             html=html)
