#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/16 14:02 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : App.py 
# @Software: PyCharm

from flask import Flask, render_template, json, jsonify, request
from datetime import datetime,timedelta
from tools import TimeSum

app = Flask(__name__)
g_user_name="mm"

def calc_week_begin_end_date(date_str):
    """
    计算某天的周一、周六的日期
    :param date_str:
    :return:
    """
    m_date = datetime.strptime(date_str, '%Y-%m-%d')
    week = m_date.weekday()
    minDate = m_date + timedelta(days=(-1 - week))
    maxDate = m_date + timedelta(days=(6 - week))
    monday = minDate.strftime('%Y-%m-%d')
    sunday = maxDate.strftime('%Y-%m-%d')
    return monday, sunday


@app.route("/api/v1/statistics/weekly/all/<date_str>", methods=["GET"])
def weekly_statistics(date_str):
    """
    获得每周相关的统计信息、每周概览的统计信息从这个一个API调用
    :param date_str:
    :return:
    """

    # TODO 登陆验证函数
    user_name = g_user_name
    monday, sunday = calc_week_begin_end_date(date_str)
    result_list, type_list, date_list = TimeSum.get_sum_list(user_name, "2019-01-13", "2019-01-19")
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
        "actual_hours": [
            {"category": "星期日", "hours": 8},
            {"category": "星期一", "hours": 7.5},
            {"category": "星期二", "hours": 6},
            {"category": "星期三", "hours": 10},
            {"category": "星期四", "hours": 5.5},
            {"category": "星期五", "hours": 7},
            {"category": "星期六", "hours": 6},
        ]
    }

    # 4. 各项每天时间汇总
    result["every_day_category_details"] = {
        "xData":[" 星期1"," 星期2"," 星期3"," 星期4"," 星期5"," 星期6"," 星期日"],
        "legends": ["睡觉", '学习', '杂', " 工作", " 运动", " 娱乐"],
        # 每个类别，每一天的时间，shape==（lengends.长度  *  xData.长度）
        "data":[
            [1,2,3,4,5,6,7],
            [8,9,10,11,12,13,14],
            [15,16,17,18,19,20,21],
            [1, 2, 3, 4, 5, 6, 7],
            [8, 9, 10, 11, 12, 13, 14],
            [15, 16, 17, 18, 19, 20, 21],
        ],
        "sum":[15, 16, 17, 18, 19, 20, 21]
    }

    # 5. 类别 时间汇总
    result["each_category_time_sum"] = [
            {"name": "睡觉", "value": 8},
            {"name": "学习", "value": 7.5},
            {"name": "工作", "value": 6},
            {"name": "娱乐", "value": 10},
            {"name": "运动", "value": 5.5},
            {"name": "杂", "value": 7},
        ]

    # 6. 漏填、充填时段
    result["missing_info"] = [
                {"start_time":"1-12 ","end_time":'1-12 12：00',"during":'1.5',"type":"重叠"},
                {"start_time": "1-12 ", "end_time": '1-12 12：00', "during": '1.5', "type": "重叠"},
                {"start_time": "1-12 ", "end_time": '1-12 12：00', "during": '1.5', "type": "重叠"},
                {"start_time": "1-12 ", "end_time": '1-12 12：00', "during": '1.5', "type": "重叠"},
                {"start_time": "1-12 ", "end_time": '1-12 12：00', "during": '1.5', "type": "重叠"},
                {"start_time": "1-12 ", "end_time": '1-12 12：00', "during": '1.5', "type": "重叠"},
            ]
    return jsonify(result)


@app.route("/<user_name>", methods=["GET"])
def index(user_name):
    global g_user_name
    g_user_name = user_name
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)