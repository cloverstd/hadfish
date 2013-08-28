# -*- coding: utf-8 -*-

from flask import Module, render_template, request, flash, url_for, redirect,\
    session, g, abort
from hadfish.databases import GroupOrder
from hadfish.extensions import db
import re

group = Module(__name__) 

def is_int(value):
    try:
        return int(value)
    except:
        return False

@group.route("/group", methods=["GET", "POST"])
@group.route("/group/add", methods=["GET", "POST"])
def order_add():
    error = None
    if request.method == "POST":

        if request.form.get("name", '') == '':
            error = u"姓名不能为空"
        elif request.form.get("tel", '') == '':
            error = u"手机号码不能为空"
        elif not re.match("1[0-9]{10}", request.form["tel"]):
            error = u"请填写正确的手机号码"
        elif GroupOrder.query.filter_by(tel=request.form["tel"]).first():
            error = u"手机号已经存在"
        elif request.form.get("address", '') == '':
            error = u"寝室号不能为空"
        elif request.form.get("num", '') == '':
            error = u"购买数量不能不正确"
        elif not is_int(request.form["num"]):
            error = u"购买数量不能不正确"
        elif int(request.form["num"]) < 0 \
                    or int(request.form["num"]) > 3:
            error = u"购买数量不正确"

        if error is None:
        
            order = GroupOrder(request.form["name"].strip(),
                               request.form["tel"],
                               request.form["address"].strip(),
                               num=request.form["num"],
                       )
            if request.form.get("email"):
                order.email = request.form["email"]
            db.session.add(order)
            db.session.commit()
            return render_template("order/success.html",
                                   name=request.form["name"])
            
    return render_template("order/add.html", error=error)
