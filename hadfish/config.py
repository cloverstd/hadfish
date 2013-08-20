# -*- coding: utf-8 -*-

import os.path


_CURRENT_PATH = os.path.dirname(__file__)
_DB_SQLITE_PATH = os.path.join(_CURRENT_PATH, 'hadfish.sqlite')

_DBUSER = "hadfish" # 数据库用户名
_DBPASS = "aGFkZmlzaHhXczI3MzA1NTguCg==" # 数据库密码
_DBHOST = "localhost" # 数据库服务器
_DBNAME = "hadfish" # 数据库名称
_DBPORT = 3306 # 数据库端口

PER_PAGE = 20 # 每页显示商品数目
RE_PER_PAGE = 20 # 每页显示评论数目
DEFAULT_TIMEZONE = "Asia/Shanghai" # 默认时区

PASSWORD_KEY = "This is a key"
SITE_NAME = u"有鱼网"

# 七牛 key
QINIU_ACCESS_KEY = "mTjx-jhzEBaeRpY60t--XLCVdKWDopZK4TqIRPDj"
QINIU_SECRET_KEY = "93nRC4uy98qJSCsadtz7-HLPCiF95-qyZDmajtGC"
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

    # Flask-Mail configuration
    MAIL_SERVER = "smtp.exmail.qq.com"
    # MAIL_PORT = 25
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = False
    # MAIL_DEBUG = True
    MAIL_USERNAME = "test@cloverstd.com"
    MAIL_PASSWORD = "xws2931336"
    MAIL_DEFAULT_SENDER = "test@cloverstd.com"
    # MAIL_MAX_EMAILS = None
    # MAIL_SUPPRESS_SEND = False


class DevConfig(BaseConfig):
    DEBUG = True

class ProConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s:%d?charset=utf8"' % (_DBUSER, _DBPASS, _DBHOST, _DBNAME, _DBPORT)
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%d/%s?charset=utf8' % (_DBUSER, _DBPASS, _DBHOST, _DBPORT, _DBNAME)
