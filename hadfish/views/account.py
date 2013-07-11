# -*- coding: utf-8 -*-

from flask import Module, render_template, request, flash, url_for, redirect
from hadfish.utils import check_password_hash, generate_password_hash
from hadfish.extensions import db
from hadfish.databases import User
from hadfish import config

account = Module(__name__)


def get_user_id(username):
    rv = User.query.filter_by(name=username).first()
    return rv.id if rv else None


def get_user_id_from_email(email):
    rv = User.query.filter_by(email=email).first()
    return rv.id if rv else None


@account.route("/register", methods=["GET", "POST"])
def register():
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
                # session["user_id"] = user.id
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
                # session["user_id"] = user.id
                # return redirect(url_for(""))
                return "登录成功"

        flash(error, category="alert-error")

    return render_template("user/login.html")
