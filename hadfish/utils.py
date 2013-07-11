#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hashlib import md5


def generate_password_hash(password, key=None):
    return md5("%s%s" % (password, key)).hexdigest()


def check_password_hash(hash_password, password, key=None):
    if hash_password == generate_password_hash(password, key):
        return True
    return False
