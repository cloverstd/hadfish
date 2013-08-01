# -*- coding: utf-8 -*-
from flask import Module

message = Module(__name__)


# 发送消息
@message.route("/message/send/<int:receiver_id>", methods=["GET", "POST"])
def send(receiver_id):
    return "send to  %r" % receiver_id


# 显示发送的消息
@message.route("/message/send")
def send_box():
    return "发件箱"


# 显示收到的信息
@message.route("/message/reveive")
def reveive_box():
    return "reveive"


# 显示收到和发出的 message
@message.route("/message")
def msg_box():
    return "msg_box"
