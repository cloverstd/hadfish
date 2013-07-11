# -*- coding: utf-8 -*-

from flask import Module, render_template, request, flash, url_for, redirect, session, g, abort
from hadfish.utils import check_password_hash, generate_password_hash, allowed_file
from hadfish.extensions import db
from hadfish.databases import User
from hadfish import config
from werkzeug import secure_filename
import os.path

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
                    school=u"上海建桥学院",
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
        
        if not request.form["password[0]"] or not request.form["password[1]"] or not request.form["password[2]"]:
            error = u"密码不能为空"
        elif not check_password_hash(user.password, request.form["password[0]"], config.PASSWORD_KEY):
            error = u"原密码不正确"
        elif request.form["password[1]"] != request.form["password[2]"]:
            error = u"新密码两次不相同"
        
        if error:
            flash(error, category="alert-error")
            return render_template("user/password.html")
        user = g.user
        user.password = generate_password_hash(request.form["password[1]"],config.PASSWORD_KEY)
        db.session.commit()
        flash(u"密码修改成功，请重新登录", category="alert-success")
        return redirect(url_for("account.logout"))
    return render_template("user/password.html")


@account.route("/setting/avatar", methods=["GET", "POST"])
def setting_avatar():
    if not g.user:
        # return redirect(url_for(""))
        return "请先登录"
    error = None
    if request.method == "POST":
        file = request.files["avatar"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # TODO 文件以 ID 保存，转换成 JPG 后
            file.save(os.path.join("/home/action/hadfish/hadfish/static/img", filename))
            flash(u"上传成功", category="alert-success")
            
            g.user.avatar = filename
            db.session.commit()
            return redirect(url_for("account.setting_avatar"))
        else:
            flash(u"文件格式不支持", category="alert-error")
            
    return render_template("user/avatar.html", user=g.user)