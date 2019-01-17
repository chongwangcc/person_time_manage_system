#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/16 14:02 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : App.py 
# @Software: PyCharm

from flask import Flask, render_template, json, jsonify, request
app = Flask(__name__)


@app.route("/fanqie_shu/<my_date>", methods=["GET"])
def fanqie_shu(my_date):
    import random
    nums = random.randint(1,100)
    return jsonify({"study_tomato_nums":nums})


@app.route("/sleep_hours/<my_date>", methods=["GET"])
def sleep_hours(my_date):
    result = {
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
    return jsonify(result)


@app.route("/each_category_hours/<my_date>", methods=["GET"])
def each_category_hours(my_date):
    result = [
            {"name": "睡觉", "value": 8},
            {"name": "学习", "value": 7.5},
            {"name": "工作", "value": 6},
            {"name": "娱乐", "value": 10},
            {"name": "运动", "value": 5.5},
            {"name": "杂", "value": 7},
        ]
    return jsonify(result)




@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)