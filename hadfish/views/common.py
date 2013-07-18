# -*- coding: utf-8 -*-

from flask import Module, request, flash, g
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from hadfish import config
from hadfish.images import upload_images, delete_images
from hadfish.utils import rename_image, allowed_file
from time import sleep
from hashlib import md5

common = Module(__name__)


@common.route("/upload/image", methods=["POST"])
def upload_image():
    # Just for a test
    # sleep(0.5)

    try:
        file = request.files["Filedata"]
    except RequestEntityTooLarge:
        #flash(u"只允许上传 5MB 以下的图片，谢谢", category="alert-error")
        return "ERROR"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = rename_image(filename, md5(file.stream.read()).hexdigest())
        # file.save(os.path.join("hadfish/hadfish/static/img", filename))
        # 上传二进制流到七牛
        if not upload_images(config.QINIU_BUCKET,
                             filename, file.stream):
            # flash(u"修改头像失败，请重试", categoty="alert-warming")
            print "test"
            return "ERROR"
        return "FILENAME:%s" % filename
    else:
        flash(u"文件格式不支持", category="alert-error")
    return "ERROR"
