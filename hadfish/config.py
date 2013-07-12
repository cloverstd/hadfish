# -*- coding: utf-8 -*-

import os.path


_CURRENT_PATH = os.path.dirname(__file__)
_DB_SQLITE_PATH = os.path.join(_CURRENT_PATH, 'hadfish.sqlite')

_DBUSER = None # 数据库用户名
_DBPASS = None # 数据库密码
_DBHOST = None # 数据库服务器
_DBNAME = None # 数据库名称
_DBPORT = None # 数据库端口

PER_PAGE = 20 # 每页显示商品数目
RE_PER_PAGE = 20 # 每页显示评论数目
DEFAULT_TIMEZONE = "Asia/Shanghai" # 默认时区

PASSWORD_KEY = "This is a key"
SITE_NAME = u"有鱼网"

# 七牛 key
QINIU_ACCESS_KEY = "WeqOutuF2P9hhB3lEGBQwWXfh1ivcfSBsILdF_U6"
QINIU_SECRET_KEY = "anyM4uKbxl3JCCkrESHcrilPdd23t2OJPDtmbiMB"
QINIU_BUCKET_AVATAR = "hadfish-avatar"
QINIU_BUCKET = "hadfish"
QINIU_DOMAIN = "http://hadfish.qiniudn.com"
QINIU_DOMAIN_AVATAR = "http://hadfish-avatar.qiniudn.com"

# 上传文件格式显示
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png"])


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "This is a key"
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024 # 6MB
    # MAX_CONTENT_LENGTH = 1024 # Just for test
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % _DB_SQLITE_PATH


class DevConfig(BaseConfig):
    DEBUG = True

class ProConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (_DBUSER, _DBPASS, _DBHOST, _DBNAME)
