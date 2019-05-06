#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/4 17:21 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : restful.py.py 
# @Software: PyCharm


from threading import Lock
import time
import threading
import json

from flask import Flask, render_template, jsonify, request, redirect
from flask_login.login_manager import LoginManager
from flask_login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from tools.DateTools import calc_week_begin_end_date, calc_month_begin_end_date, calc_year_begin_end_date
from flask_socketio import SocketIO, Namespace, emit

from tools import SqlTools
from tools import BussinessLogic
from tools import DateTools
from tools import GoogleAuth


app = Flask(__name__, static_folder='../static', template_folder="../static/html")
app.config['SECRET_KEY'] = '123456'

login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app,engineio_logger=True)
thread = None
thread_lock = Lock()

@login_manager.user_loader
def load_user(user_name):
    m_user = SqlTools.fetch_user_info(user_name)
    return m_user


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
    result = BussinessLogic.CacheCalcService.fetch_cache(task)
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
    result = BussinessLogic.CacheCalcService.fetch_cache(task)
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
    result = BussinessLogic.CacheCalcService.fetch_cache(task)
    # 3. 构造结果
    return jsonify(result)


@app.route("/api/v1/login/google", methods=["post"])
def login_in_with_google():
    """
    使用google登录帐号
    :return:
    """
    token = request.values.get("id")
    email = request.values.get("email")
    name = request.values.get("name")
    if name is None:
        name = str(email).split("@")[0]
    # 1. 检查有没有这个帐号
    code, user_info = SqlTools.check_user_email_token(email,token)
    if code == 1:
        # 1.1 如果没有，创建新帐号
        user_info = SqlTools.add_user({
            "name": name,
            "email": email,
            "token": token
        })
    elif code == 2:
        # 2. 用户授权信息不对
        return jsonify({"code": 4})
    elif code == 0:
        # 3.授权信息正确
        pass

    m_user = SqlTools.fetch_user_info(user_info.user_name)
    login_user(m_user, remember=True)

    # 3. 判断帐号有没有 授权访问google 日历
    # 弹出，授权google日历界面
    if not SqlTools.check_calender_token(user_info):
        url = GoogleAuth.gen_calender_auth_url(user_info.user_name)
        return jsonify({"code": 2,
                        "data": url})

    # 4. 判断帐号有没有配置“日历、密码”等信息
    # 如果没有，弹出配置日历的窗口
    ret = GoogleAuth.check_user_config(user_info.user_name)
    if not ret:
        return jsonify({"code": 3,
                        "data": GoogleAuth.gen_url("/userinfo")})

    # 5. 进入时间日志的统计界面
    return jsonify({"code": 0,
                    "data": GoogleAuth.gen_url("/weeksum")})


@app.route("/api/v1/login/calender_oauth", methods=["GET", "POST"])
def calender_oauth():
    """
    使用google登录帐号
    :return:
    """

    state = request.args.get("state")
    code = request.args.get("code")

    ret = GoogleAuth.gen_calender_auth_2(state, code)
    if ret:
        return redirect('login')
    else:
        return jsonify({"msg":"login failed"})


@app.route("/api/v1/login/baseinfo",  methods=["GET","POST"])
@login_required
def get_base_info():
    """
    获得用户的基本信息
    :return:
    """
    t_user = SqlTools.fetch_user_info(current_user.user_name)
    if request.method == 'POST':
        t_user.user_name = request.form.get("name")
        t_user.password = request.form.get("password")
        t_user.calender_server = request.form.get("calender_server")
        t_user.calender_name = request.form.get("calender_name")
        t_user.save()
        login_user(t_user, remember=True)

        result = {
            "code":0,
            "data":GoogleAuth.gen_url("/login")
        }
    elif request.method == "GET":
        result = {
            "code": 0,
            "data": {
                "user_name": t_user.user_name,
                "password" : t_user.password,
                "calendar_servers": ["google calendar"],
                "calendar_names": {
                    "google calendar": ["时间日志", "主日历"]
                }
            }
        }

    return jsonify(result)



class WebResultFetcher(Namespace):
    """

    """
    def __init__(self, namespace=None):
        super().__init__(namespace)
        BussinessLogic.ConnectionManager.set_emit_cls(self)

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_weeksum(self, data):
        date_str = data.get('date_str')
        monday, sunday = calc_week_begin_end_date(date_str)
        t_user = SqlTools.fetch_user_info(current_user.user_name)
        task = BussinessLogic.CacheCalcTask(t_user, "week", monday, sunday)
        t_dict = BussinessLogic.ConnectionManager.register_task(task)
        while True:
            with t_dict["cond"]:
                t_dict["cond"].wait()
                emit("weeksum", t_dict["json"])

    def on_monthsum(self, data):
        date_str = data.get('date_str')
        first_day, last_day = calc_month_begin_end_date(date_str)
        t_user = SqlTools.fetch_user_info(current_user.user_name)
        task = BussinessLogic.CacheCalcTask(t_user, "month", first_day, last_day)
        t_dict = BussinessLogic.ConnectionManager.register_task(task)
        with t_dict["cond"]:
            while True:
                t_dict["cond"].wait()
                t_dict["callback"](t_dict["task"], t_dict["json"])

    def on_yearsum(self, data):
        date_str = data.get('date_str')
        first_day, last_day = calc_year_begin_end_date(date_str)
        t_user = SqlTools.fetch_user_info(current_user.user_name)
        task = BussinessLogic.CacheCalcTask(t_user, "year", first_day, last_day)
        t_dict = BussinessLogic.ConnectionManager.register_task(task)
        with t_dict["cond"]:
            t_dict["cond"].wait()
            t_dict["callback"](t_dict["task"], t_dict["json"])


socketio.on_namespace(WebResultFetcher('/update'))