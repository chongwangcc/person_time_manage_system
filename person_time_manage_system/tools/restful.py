#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/4 17:21 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : restful.py.py 
# @Software: PyCharm

from flask import Flask, render_template, jsonify, request, redirect
from flask_login.login_manager import LoginManager
from flask_login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from tools.DateTools import calc_week_begin_end_date, calc_month_begin_end_date, calc_year_begin_end_date
from flask_socketio import SocketIO, emit
from tools import SqlTools
from tools import BussinessLogic
from threading import Lock


app = Flask(__name__, static_folder='../static', template_folder="../templates")
app.config['SECRET_KEY'] = '123456'

login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app)
thread = None
thread_lock = Lock()

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
    # 1. 查找缓存，获得每月数据
    first_day, last_day = calc_month_begin_end_date(date_str)
    t_user = SqlTools.fetch_user_info(current_user.user_name)
    task = BussinessLogic.CacheCalcTask(t_user, "month", first_day, last_day)
    # 2.查询缓存
    result = BussinessLogic.CachCalcService.fetch_cache(task)
    # 3. 构造返回JSON
    # import json
    # js = json.dumps(result, sort_keys=True, indent=4, separators=(',', ':'))
    # print(js)
    return jsonify(result)


@app.route("/api/v1/statistics/yearly/all/<date_str>", methods=["GET"])
@login_required
def yearly_statistics(date_str):
    """
    获得每年的统计数据
    :param date_str 月份字符串，例如：2019:
    :return:
    """
    # 1.构造缓存查询任务
    first_day, last_day = calc_year_begin_end_date(date_str)
    t_user = SqlTools.fetch_user_info(current_user.user_name)
    task = BussinessLogic.CacheCalcTask(t_user, "year", first_day, last_day)
    # 2.查询缓存
    result = BussinessLogic.CachCalcService.fetch_cache(task)
    # 3. 构造结果
    return jsonify(result)
