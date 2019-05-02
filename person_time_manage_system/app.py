#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/16 14:02 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : App.py 
# @Software: PyCharm

from flask import Flask, render_template, jsonify, request, redirect
from flask_login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from tools import BussinessLogic
from tools import SqlTools
from tools.restful import app, socketio
import warnings

warnings.filterwarnings('ignore')

@app.route("/weeksum/", methods=["GET"])
@login_required
def timesum():
    return render_template("weeksum.html", user_name=current_user.user_name)


@app.route("/monthlySum/", methods=["GET"])
@login_required
def monthlySum():
    return render_template("monthly.html", user_name=current_user.user_name)


@app.route("/yearlySum/", methods=["GET"])
@login_required
def yearlySum():
    return render_template("yearly.html", user_name=current_user.user_name)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    打开默认界面
    :return:
    """
    if request.method == 'POST':
        user_name = request.form["username"]
        password = request.form["password"]
        # 判断用户密码是否正确
        m_user = SqlTools.fetch_user_info(user_name)
        if m_user is not None and m_user.password == password:
            # 登陆成功
            login_user(m_user, remember=True)
            # 跳转
            return redirect("/weeksum")
        else:
            # 登陆失败，弹出消息框
            return render_template('login.html')

    # 判断有没有用户登录
    return render_template('login.html')


@app.route("/logout", methods=["POST","GET"])
@login_required
def logout():
    """
    登出界面
    :return:
    """
    logout_user()
    return redirect('/login')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    BussinessLogic.start()
    # app.run(debug=True, host="0.0.0.0", port="9001")
    socketio.run(app, debug=True,host="0.0.0.0", port="9001")
