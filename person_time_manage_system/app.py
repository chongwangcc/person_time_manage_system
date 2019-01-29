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
from tools import TimeSum
from tools.UserTools import UserInfoManager
from tools.DateTools import calc_week_begin_end_date

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
login_manager = LoginManager()
login_manager.init_app(app)

userinfomanager = UserInfoManager("./data")

@login_manager.user_loader
def load_user(userid):
    return userinfomanager.get_user_info(userid)


@app.route("/api/v1/statistics/weekly/all/<date_str>", methods=["GET"])
@login_required
def weekly_statistics(date_str):
    """
    获得每周相关的统计信息、每周概览的统计信息从这个一个API调用
    :param date_str:
    :return:
    """

    # 登陆验证函数
    user_name = current_user.user_name
    monday, sunday = calc_week_begin_end_date(date_str)
    result_list, missing_info = TimeSum.get_sum_list(user_name, monday,sunday)
    # 构造返回结果
    result = {}
    # 1.开始结束日期 工作-学习番茄数 锻炼娱乐次数
    result["working_tomato_nums"] = TimeSum.get_tomato_nums(result_list, label="工作")
    result["study_tomato_nums"] = TimeSum.get_tomato_nums(result_list, label="学习")
    result["execise_nums"] = TimeSum.get_nums(result_list, label="运动")
    result["fun_nums"] = TimeSum.get_nums(result_list, label="娱乐")
    result["start_date"] = monday
    result["end_date"] = sunday

    # 2. 番茄时钟达标率
    result["working_and_study_tomato_nums_of_each_day"]=result["working_tomato_nums"]+result["study_tomato_nums"]

    # 3. 睡眠时间
    result["sleep_hours"] = {
        "standard_hours": 7.5,
        "actual_hours": TimeSum.get_every_day_sum_of_category(result_list, label="睡觉")
    }

    # 4. 各项每天时间汇总
    result["every_day_category_details"] = TimeSum.get_every_day_category_details(result_list, day_padding=7)
    print(result["every_day_category_details"])

    # 5. 类别 时间汇总
    result["each_category_time_sum"] = TimeSum.get_all_category_time_sum(result_list)

    # 6. 漏填、充填时段
    result["missing_info"] = missing_info
    return jsonify(result)


@app.route("/api/v1/statistics/monthly/all/<date_str>", methods=["GET"])
@login_required
def monthly_statistics(date_str):
    """
    获得每月统计数据
    :param date_str 月份字符串，例如：2019-01 :
    :return:
    """
    # TODO 查找缓存，获得每月数据

    #构造结果
    result={}
    result["start_date"] = "2019-01-01"
    result["end_date"] = "2019-01-29"
    result["during_percent"] = "93%"
    result["living_percent"] = "30%"
    result["working_tomato_nums"] = "40"
    result["study_tomato_nums"] = "60"

    #1. 本月主题词云
    result["word_cloud"] = [
                        {
                            "name": 'Sam S Club',
                            "value": 10000,
                        }, {
                            "name": 'Macys',
                            "value": 6181
                        }, {
                            "name": 'Amy Schumer',
                            "value": 4386
                        }, {
                            "name": 'Jurassic World',
                            "value": 4055
                        }, {
                            "name": 'Charter Communications',
                            "value": 2467
                        }, {
                            "name": 'Chick Fil A',
                            "value": 2244
                        }, {
                            "name": 'Planet Fitness',
                            "value": 1898
                        }, {
                            "name": 'Pitch Perfect',
                            "value": 1484
                        }, {
                            "name": 'Express',
                            "value": 1112
                        }, {
                            "name": 'Home',
                            "value": 965
                        }, {
                            "name": 'Johnny Depp',
                            "value": 847
                        }, {
                            "name": 'Lena Dunham',
                            "value": 582
                        }, {
                            "name": 'Lewis Hamilton',
                            "value": 555
                        }, {
                            "name": 'KXAN',
                            "value": 550
                        }, {
                            "name": 'Mary Ellen Mark',
                            "value": 462
                        }, {
                            "name": 'Farrah Abraham',
                            "value": 366
                        }, {
                            "name": 'Rita Ora',
                            "value": 360
                        }, {
                            "name": 'Serena Williams',
                            "value": 282
                        }, {
                            "name": 'NCAA baseball tournament',
                            "value": 273
                        }, {
                            "name": 'Point',
                            "value": 273
                        }, {
                            "name": 'Point Break',
                            "value": 265
                        }]

    #2. 各项能力雷达图
    result["ability_redar"] = [
        {
              "value": [5, 7, 1.2, 1.1, 1.5, 1.4],
              "name": '上月',
          },{
              "value": [2.5, 1.2, 8, 8.5, 1.2, 1.2],
              "name": '本月',
          }
    ]

    # 3, 各类环比图
    result["compare"] ={
        "last_month":[209,236,325],
        "this_month":[209,236,325],
        "growth":[1,13,5],
        "type":['工作时长',"学习时长","运动"]
    }

    # 4. 活着时间
    result["living_time"]={
        "last_month_data":[120, 132, 101, 134, 90, 230, 210],
        "this_month_data":[220, 182, 191, 234, 290, 330, 310]
    }

    # 5. 类别分布矩形图
    result["category_rectangle"]={
        "工作":{
            "$count":12,
            "开发":{
                 "$count":34,
            },
            "运维":{
                 "$count":46,
            },
            "开会":{
                 "$count":78,
            },
        },
        "学习":{
            "$count":12,
            "时间日志":{
                 "$count":34,
            },
            "看书":{
                 "$count":780,
            },
            "写笔记":{
                 "$count":100,
            },
        }
    }

    # 6. TODO 活着时长演变图
    result["living_evolution"]={}

    # 7. 工作时段转换率
    result["working_hours_transform_rate"]={
        "legend": ['展现','点击','访问','咨询','订单'],
        "value": [
                    {"value": 20, "name": '访问'},
                    {"value": 10, "name": '咨询'},
                    {"value": 5, "name": '订单'},
                    {"value": 80, "name": '点击'},
                    {"value": 100, "name": '展现'}
                ]
    }

    # 8. 学习时段转换率
    result["learning_hours_transform_rate"]={
        "legend": ['展现','点击','访问','咨询','订单'],
        "value": [
                    {"value": 20, "name": '访问'},
                    {"value": 10, "name": '咨询'},
                    {"value": 5, "name": '订单'},
                    {"value": 80, "name": '点击'},
                    {"value": 100, "name": '展现'}
                ]
    }




@app.route("/weeksum/", methods=["GET"])
@login_required
def timesum():
    return render_template("index.html", user_name=current_user.user_name)


@app.route("/monthlySum/", methods=["GET"])
@login_required
def monthlySum():
    return render_template("monthly.html", user_name=current_user.user_name)


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
        m_user = userinfomanager.get_user_info(user_name)
        if m_user is not None and m_user.password == password:
            # 登陆成功
            login_user(m_user)
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
    app.run(debug=True, host="0.0.0.0", port=9001)
