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

account = Module(__name__)


def get_user_id(username):
    rv = User.query.filter_by(name=username).first()
    return rv.id if rv else None


def get_user_id_from_email(email):
    rv = User.query.filter_by(email=email).first()
    return rv.id if rv else None


@account.route("/register", methods=["GET", "POST"])
def register():
    if g.user:
        return "已经登录了"
    error = None
    if request.method == "POST":
        if not request.form["username"]:
            error = u"亲，用户名不能为空哟！"
        elif not request.form["password"]:
            error = u"亲，肿么可以没有密码呢!"
        elif request.form["password"] != request.form["password2"]:
            error = u"亲，两次输入的密码不相同哟!"
        elif not request.form["email"] or \
                '@' not in request.form["email"]:
            error = u"亲，邮箱地址不正确哟!"
        elif get_user_id(request.form["username"]):
            error = u"亲，用户名已经存在了哟！"
        elif get_user_id_from_email(request.form["email"]):
            error = u"亲，邮箱已经存在了哟！"

        print request.form

        if error:
            flash(error, category="alert-error")
            return render_template("user/register.html", pre_data=request.form)
        user = User(request.form["username"], request.form["email"],
                    generate_password_hash(request.form["password"],
                                           config.PASSWORD_KEY),
                    tel=request.form["tel"], qq=request.form["QQ"],
                    school=u"上海建桥学院", profile=u"",
                    address=request.form["address"])

        db.session.add(user)
        db.session.commit()
        flash(u"亲，注册成功了，赶紧登录吧！", category="alert-success")
        return redirect(url_for("account.login"))
    return render_template("user/register.html")


@account.route("/login", methods=["GET", "POST"])
def login():
    if g.user:
        return "已经登录了"
    error = None
    if request.method == "POST":
        if '@' in request.form["username"]:
            user = User.query.filter_by(email=request.form["username"]).first()
            if user is None:
                error = u"用户名错误哟！"
            elif not check_password_hash(user.password,
                                         request.form["password"],
                                         config.PASSWORD_KEY):
                error = u"亲，密码错误哟"
            else:
                flash(u"登录成功！", category="alert-success")
                session["user_id"] = user.id
                if request.form.get("login-auto"):
                    session.permanent = True
                # return redirect(url_for(""))
                return "登录成功"
        else:
            user = User.query.filter_by(name=request.form["username"]).first()
            if user is None:
                error = u"用户名错误哟！"
            elif not check_password_hash(user.password,
                                         request.form["password"],
                                         config.PASSWORD_KEY):
                error = u"亲，密码错误哟"
            else:
                flash(u"登录成功！", category="alert-success")
                session["user_id"] = user.id
                if request.form.get("login-auto"):
                    session.permanent = True
                # return redirect(url_for(""))
                return "登录成功"

        flash(error, category="alert-error")
    return render_template("user/login.html")


@account.route("/logout", methods=["GET", "POST"])
def logout():
    if g.user is not None:
        session.pop('user_id', None)
        session.permanent = False
        flash(u"'你已经成功登出！")
    # return redirect(url_for())
    return "已经成功登出"


@account.route("/user/<username>")
def userinfo(username):
    user = User.query.filter_by(name=username).first()
    if not user:
        abort(404)
    return render_template("user/userinfo.html", user=user)


@account.route("/setting/account", methods=["GET", "POST"])
def setting():
    if not g.user:
        # return redirect(url_for(""))
        return "请先登录"
    error = None
    if request.method == "POST":
        if not request.form["username"]:
            error = u"用户名不能为空"
        elif not request.form["email"] or not '@' in request.form["email"]:
            error = u"邮箱不能为空"
        if error:
            flash(error, category="alert-error")
            return redirect(url_for("account.setting"))
        user = g.user
        user.name = request.form["username"]
        # 如果邮箱改变则需要重新验证
        if request.form["email"] != user.email:
            user.is_validate = False
            user.valid_time = ""
            user.valid_value = ""
        user.email = request.form["email"]
        user.qq = request.form["QQ"]
        user.tel = request.form["tel"]
        user.address = request.form["address"]
        user.profile = request.form["profile"]
        db.session.commit()
        flash(u"修改成功", category="alert-success")
        return redirect(url_for("account.setting"))
    return render_template("user/setting.html", user=g.user)


@account.route("/setting/password", methods=["GET", "POST"])
def setting_password():
    if not g.user:
        # return redirect(url_for(""))
        return "请先登录"
    error = None
    if request.method == "POST":
        if not request.form["password[0]"] or \
                not request.form["password[1]"] or \
                not request.form["password[2]"]:
            error = u"密码不能为空"
        elif not check_password_hash(g.user.password,
                                     request.form["password[0]"],
                                     config.PASSWORD_KEY):
            error = u"原密码不正确"
        elif request.form["password[1]"] != request.form["password[2]"]:
            error = u"新密码两次不相同"
        if error:
            flash(error, category="alert-error")
            return render_template("user/password.html")
        user = g.user
        user.password = generate_password_hash(request.form["password[1]"],
                                               config.PASSWORD_KEY)
        db.session.commit()
        flash(u"密码修改成功，请重新登录", category="alert-success")
        return redirect(url_for("account.logout"))
    return render_template("user/password.html")


@account.route("/setting/avatar", methods=["GET", "POST"])
def setting_avatar():
    if not g.user:
        # return redirect(url_for(""))
        return "请先登录"
    # error = None
    if request.method == "POST":
        try:
            file = request.files["avatar"]
        except RequestEntityTooLarge:
            flash(u"只允许上传 5MB 以下的图片，谢谢", category="alert-error")
            return redirect(url_for("account.setting_avatar"))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = rename_image(filename, get_avatar_name(g.user.id))
            # file.save(os.path.join("hadfish/hadfish/static/img", filename))
            # 上传二进制流到七牛
            if not delete_images(config.QINIU_BUCKET_AVATAR, g.user.avatar):
                flash(u"修改头像失败，请重试", category="alert-warming")
                return render_template("user/avatar.html", user=g.user)
            if not upload_images(config.QINIU_BUCKET_AVATAR,
                                 filename, file.stream):
                flash(u"修改头像失败，请重试", category="alert-warming")
                return render_template("user/avatar.html", user=g.user)
            flash(u"上传成功", category="alert-success")
            g.user.avatar = filename
            db.session.commit()
            return redirect(url_for("account.setting_avatar"))
        else:
            flash(u"文件格式不支持", category="alert-error")
    return render_template("user/avatar.html", user=g.user)


@account.route("/setting/email", methods=["GET", "POST"])
def email_valid():
    if request.args:
        k = request.args.get("k")
        v = request.args.get("v")
        if not k or not v:
            flash(u"无效的验证链接", category="alert-error")
            return "验证链接无效"
        user = User.query.filter_by(id=k).first()
        if g.user.is_validate:
            flash(u"已经验证过了", category="alert-warming")
            return "已经验证了的邮箱"

        valid_time = user.valid_time
        if (datetime.now() - valid_time).days > 0:
            flash(u"验证链接已经过期", category="alert-warming")
            return "验证链接已经过期"

        if not user or user.valid_value != v:
            flash(u"无效的验证链接", category="alert-error")
            return "验证链接无效"

        if user.valid_value == v:
            user.is_validate = True
            user.valid_time = None
            user.valid_value = None
            db.session.commit()
            flash(u"恭喜验证成功", category="alert-success")
            return "验证成功"

    if not g.user:
        # return redirect(url_for(""))
        return "请先登录"
    if request.method == "POST":
        if g.user.is_validate:
            flash(u"已经验证过了", category="alert-warming")
            return "已经验证了的邮箱"

        valid_time = datetime.now()
        valid_value = md5("%s%s" % (g.user.id,
                                    valid_time.__str__())).hexdigest()
        g.user.valid_time = valid_time
        g.user.valid_value = valid_value
        db.session.commit()
        # Send a validate email
        html = """
        <a href="%s/setting/email?k=%sv&v=%s">点击验证</a></br>
        如果无法点击，请复制下列地址到浏览器中验证
        %s/setting/email?k=%s&v=%s
        """ % ("http://localhost:8080", g.user.id, valid_value,
               "http://localhost:8080", g.user.id, valid_value)
        mail.send_message(subject="有鱼网验证邮件",
                          recipients=[g.user.email],
                          # recipients=["23081991@qq.com"],
                          html=html)
        return "邮件已经发送，请查收"
    return "无效的验证链接"
