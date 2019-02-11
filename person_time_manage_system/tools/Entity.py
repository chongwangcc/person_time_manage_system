#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/30 10:18 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : Entity.py 
# @Software: PyCharm
from nanorm import *


class User_Info(Model):
    """
    用户信息表
    """
    user_name = CharField(128)
    password = CharField(128)
    active = IntegerField()
    auth_token_file = CharField(256)
    calender_server = CharField(128)
    calender_name = CharField(128)

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my


class Time_Details(Model):
    """
    时间明细表
    """
    user_id = ForeignKey(User_Info)
    date_str = CharField(10)
    week_nums = IntegerField(1)
    category = CharField(16)
    start_time = CharField(10)
    end_time = CharField(10)
    during = IntegerField()
    descrition = CharField()

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my


class Everyday_Cache(Model):
    """
    每日缓存表
    """
    user_id = ForeignKey(User_Info)
    date_str = CharField(10)
    category = CharField(16)
    during = IntegerField()
    nums = IntegerField()
    word_cloud = CharField()

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my


class Every_week_Cache(Model):
    """
    每周缓存表
    """
    user_id = ForeignKey(User_Info)
    start_date_str = CharField(10)
    end_date_str = CharField(10)
    category = CharField(10)
    during = IntegerField()
    nums = IntegerField()
    word_cloud = CharField()

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my


class Every_month_Cache(Model):
    """
    每月缓存表
    """
    user_id = ForeignKey(User_Info)
    month_str = CharField(7)
    category = CharField(16)
    during = IntegerField()
    nums = IntegerField()
    word_cloud = CharField()

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my


if __name__ == "__main__":
    g_sqlite3_path = "./data/sqlit3.db"
    set_db_name(g_sqlite3_path)
    userinfo = User_Info()
    userinfo.user_name="cc"
    userinfo.password="123456"
    userinfo.active=1
    userinfo.auth_token_file = r".\data\.credentials\cc_calendar.json"
    userinfo.calender_server = "google"
    userinfo.calender_name = "时间日志"
    userinfo.save()

    userinfo = User_Info()
    userinfo.user_name="mm"
    userinfo.password="123456"
    userinfo.active=1
    userinfo.auth_token_file = r".\data\.credentials\mm_calendar.json"
    userinfo.calender_server = "google"
    userinfo.calender_name = "时间日志"
    userinfo.save()


    # userinfo = User_Info.get(user_name="cc")
    # userinfo.delete()
    # userinfo = User_Info.get(user_name="mm")
    # userinfo.delete()
    # print(userinfo)

    userinfo = User_Info.get(user_name="cc")
    print(userinfo.to_dict())
    print(userinfo)

