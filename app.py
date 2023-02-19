#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2023/02/17
@Author  :   HDUZN
@Version :   1.0
@Contact :   hduzn@vip.qq.com
@License :   (C)Copyright 2022-2023
@Desc    :   pip install flask, gevent
'''

from flask import Flask, render_template, request, redirect, url_for
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

# MQTT broker 配置
mqtt_account = {
    'MQTT_BROKER':"192.168.31.181",
    'MQTT_PORT':8083
}

# 首页
@app.route("/")
def index():
    return "请输入机房编号，如：/room1 进行登录"

# 登录
@app.route("/<room>")
def login(room):
    return render_template("login.html", room=room)

@app.route('/user', methods=['POST'])
def submit_pc_id():
    computer_id = request.form.get('computer_id')
    room = request.form.get('room')
    return redirect(url_for('user_msg', room=room, computer_id=computer_id)) # 重定向

# 用户页
@app.route('/user/<room>/<computer_id>')
def user_msg(room, computer_id):
    return render_template("message.html", room=room, pc_id=computer_id, mqtt_account=mqtt_account)

# 管理页
@app.route("/admin/<room>")
def admin(room):
    return render_template("admin.html", room=room, mqtt_account=mqtt_account)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, port=5012)
    http_server = WSGIServer(('0.0.0.0', 5012), app)
    http_server.serve_forever()
