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
from tools.DateTools import calc_week_begin_end_date
import BussinessLogic
import SqlTools

calc_service = BussinessLogic.CachCalcService(BussinessLogic.web_cache)
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
    task = BussinessLogic.CacheCalcTask(current_user, "week", monday, sunday)
    calc_service.add_new_cache(task)
    # 构造返回结果
    result = BussinessLogic.web_cache.setdefault(task.get_key(),{})
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
    print(date_str)

    #构造结果
    result={}
    result["start_date"] = "2018-01-01"
    result["end_date"] = "2018-01-29"
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
    result["living_time"] = {
        "last_month_data": [120, 132, 101, 134, 90, 230, 210],
        "this_month_data": [220, 182, 191, 234, 290, 330, 310]
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
    result["living_evolution"]={
    "counties": ["学习", "工作", "娱乐", "运动", "整理"],
    "timeline": [i for i in range(1, 32)],
    "series": [[[815, 34.05, 351014, "学习", 1],[1314, 39, 645526, "工作", 1],  [985, 32, 321675013, "娱乐", 1], [864, 32.2, 345043, "运动", 1], [1244, 36.5731262, 977662, "整理", 1]],
                [[834, 34.05, 342440, "学习", 2], [1400, 39.01496774, 727603, "工作", 2], [985, 32, 350542958, "娱乐", 2], [970, 33.64, 470176, "运动", 2], [1267, 36.9473378, 1070625, "整理", 2]],
               [[853, 34.05, 334002, "学习", 3], [1491, 39.02993548, 879432, "工作", 3], [985, 32, 380055273, "娱乐", 3], [1090, 35.04, 607664, "运动", 3], [1290, 37.29122269, 1190807, "整理", 3]], 
               [[1399, 34.05, 348143, "学习", 4], [1651, 39.04490323, 1202146, "工作", 4], [986, 32, 402373519, "娱乐", 4], [1224, 35.74, 772812, "运动", 4], [1360, 36.29644969, 1327905, "整理", 4]], 
               [[2269, 34.05, 434095, "学习", 5], [1922, 40.19012, 1745604, "工作", 5], [986, 32, 411213424, "娱乐", 5], [1374, 36.48, 975565, "运动", 5], [1434, 41.46900965, 1467238, "整理", 5]], 
               [[3267, 34.05, 742619, "学习", 6], [2202, 40.985432, 2487811, "工作", 6], [985, 32, 402711280, "娱乐", 6], [1543, 36.26, 1181650, "运动", 6], [1512, 37.35415172, 1607810, "整理", 6]], 
               [[4795, 34.05, 1256048, "学习", 7], [2406, 41.541504, 3231465, "工作", 7], [1023, 28.85, 380047548, "娱乐", 7], [1733, 36.24, 1324000, "运动", 7], [1594, 38.15099864, 1734254, "整理", 7]], 
               [[5431, 34.05, 1724213, "学习", 8], [2815, 42.460624, 3817167, "工作", 8], [1099, 31.95714286, 363661158, "娱乐", 8], [1946, 29.66, 1424672, "运动", 8], [1897, 45.66140699, 1847468, "整理", 8]]]
    }

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
    return jsonify(result)


@app.route("/api/v1/statistics/yearly/all/<date_str>", methods=["GET"])
@login_required
def yearly_statistics(date_str):
    """
    获得每年的统计数据
    :param date_str 月份字符串，例如：2019:
    :return:
    """
    # TODO 查找缓存，获得每月数据
    print(date_str)

    #构造结果
    result={}
    result["year"] = "2019"
    result["end_date"] = "01-29"
    result["working_tomato_nums"] = "40"
    result["study_tomato_nums"] = "60"
    result["workout_nums"] = "10"
    result["workout_hours"] = "45"

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

    #2. 每周时间走势图
    result["every_week_category_details"] = {'xData': ['2019-02-03'], 'legends': ['杂', '睡觉'], 'data': [[2.25], [7.5]], 'sum': [9.75]}

    # 3. 类别分布矩形图
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
        },
        "运动": {
            "$count": 12,
            "健身房": {
                "$count": 34,
            },
            "跑步": {
                "$count": 780,
            },
            "遛弯": {
                "$count": 100,
            },
        }
    }

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
