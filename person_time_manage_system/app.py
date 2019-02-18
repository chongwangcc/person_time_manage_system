#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/16 14:02 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : App.py 
# @Software: PyCharm

from flask import Flask, render_template, jsonify, request, redirect
from flask_login.login_manager import LoginManager
from flask_login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from tools.DateTools import calc_week_begin_end_date, calc_month_begin_end_date, calc_year_begin_end_date
import BussinessLogic
import SqlTools

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    return SqlTools.fetch_user_info(user_name)


@app.route("/api/v1/statistics/weekly/all/<date_str>", methods=["GET"])
@login_required
def weekly_statistics1(date_str):
    """
    获得每周相关的统计信息、每周概览的统计信息从这个一个API调用
    :param date_str:
    :return:
    """
    # 1.构造缓存查询任务
    monday, sunday = calc_week_begin_end_date(date_str)
    t_user = SqlTools.fetch_user_info(current_user.user_name)
    task = BussinessLogic.CacheCalcTask(t_user, "week", monday, sunday)
    # 2.查询缓存
    result = BussinessLogic.CachCalcService.fetch_cache(task)
    # 3. 构造返回JSON
    return jsonify(result)


@app.route("/api/v1/statistics/monthly/all/<date_str>", methods=["GET"])
@login_required
def monthly_statistics(date_str):
    """
    获得每月统计数据
    :param date_str 月份字符串，例如：2019-01 :
    :return:
    """
    #  查找缓存，获得每月数据
    first_day, last_day = calc_month_begin_end_date(date_str)
    task = BussinessLogic.CachCalcService.CacheCalcTask(current_user, "month", first_day, last_day)
    # 2.查询缓存
    result = BussinessLogic.CachCalcService.fetch_cache(task)
    # 3. 构造返回JSON
    return jsonify(result)


@app.route("/api/v1/statistics/yearly/all/<date_str>", methods=["GET"])
@login_required
def yearly_statistics(date_str):
    """
    获得每年的统计数据
    :param date_str 月份字符串，例如：2019:
    :return:
    """
    #  查找缓存，获得每年数据

    # 1.构造缓存查询任务
    first_day, last_day = calc_year_begin_end_date(date_str)
    task = BussinessLogic.CacheCalcTask(current_user, "month", first_day, last_day)
    # 2.查询缓存
    result = BussinessLogic.CachCalcService.fetch_cache(task)
    # 3. 构造结果
    return jsonify(result)


@app.route("/weeksum/", methods=["GET"])
@login_required
def timesum():
    return render_template("index.html", user_name=current_user.user_name)


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
    app.run(debug=True, host="0.0.0.0", port=9001)
