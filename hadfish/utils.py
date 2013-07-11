#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hashlib import md5


def generate_password_hash(password, key=None):
    return md5("%s%s" % (password, key)).hexdigest()


def check_password_hash(hash_password, password, key=None):
    if hash_password == generate_password_hash(password, key):
        return True
    return False

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])
def allowed_file(filename):
    """检查上传的文件名是否符合要求"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    

# def exchange_img_name(original_name, name):
#     """转换 original_name 为 name，保持后缀不变
    