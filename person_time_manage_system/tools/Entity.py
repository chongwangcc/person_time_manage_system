#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/30 10:18 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : Entity.py 
# @Software: PyCharm
from nanorm import *
from flask_login import UserMixin, AnonymousUserMixin


# 内存中的 实体结果 ---------------------
class CalenderQueryTask:
    """
    日历查询的任务，一个对象是一个任务
    """
    def __init__(self, user_info, start_date, end_date):
        self.user_info = user_info
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        info = ""
        info += " user_info="+str(self.user_info.user_name)
        info += " start_date="+str(self.start_date)
        info += " end_date=" + str(self.end_date)
        return info


class CacheCalcTask:
    """
    计算统计数据缓存的任务
    """
    def __init__(self, user_info, freq, start_date_str, end_date_str):
        """

        :param user_info:
        :param freq: 统计周期，只能是 [日，周，月，年] 中的一个
        :param date_str:
        """
        self.user_info = user_info
        self.freq = freq
        self.start_date_str = start_date_str
        self.end_date_str = end_date_str

    def get_key(self):
        key = str(self.user_info.user_name)+"_"+self.freq+"_"+self.start_date_str+"_"+self.end_date_str
        return key

    def __str__(self):
        return self.get_key()


# SQLite 数据库中 实体结构定义---------------------------

class User_Info(Model, UserMixin):
    """
    用户信息表
    """
    user_name = CharField(128)
    password = CharField(128)
    active = IntegerField()
    auth_token_file = CharField(256)
    calender_server = CharField(128)
    calender_name = CharField(128)
    email = CharField(128)

    def get_id(self):
        return self.user_name

    def get_by_id(self, user_name):
        try:
            userinfo = User_Info.get(user_name=user_name)
            return userinfo
        except:
            pass
        return None

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my

    @staticmethod
    def is_user_exist():
        """
        判断user_info表是否为空
        :return:
        """
        try:
            sql = "select * from %s limit 1" \
                  % (__class__.__name__.lower())
            cu = get_cursor()
            execute_sql(cu, sql)
            rows = cu.fetchall()
            if len(rows) >= 1 :
                return True
        except:
            lock.release()
            pass
        return False


class Time_Details(Model):
    """
    时间明细表
    """
    user_id = ForeignKey(User_Info)
    date_str = CharField(10)
    week_nums = IntegerField(1)
    category = CharField(16)
    second_category = CharField(16)
    start_time = CharField(10)
    end_time = CharField(10)
    during = IntegerField()
    description = CharField()
    only_key = CharField()
    md5 = CharField(128)

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my

    @staticmethod
    def get_table_name():
        return __class__.__name__.lower()

    @staticmethod
    def is_table_exist():
        """
        判断user_info表是否为空
        :return:
        """
        try:
            sql = "select * from %s limit 1" \
                  % (__class__.__name__.lower())
            cu = get_cursor()
            execute_sql(cu, sql)
            rows = cu.fetchall()
            if len(rows) >= 1 :
                return True
        except:
            lock.release()
            pass
        return False


class Everyday_Cache(Model):
    """
    每日缓存表
    """
    user_id = ForeignKey(User_Info)
    date_str = CharField(10)
    week_start_str = CharField(10)
    week_end_str = CharField(10)
    year_str = CharField(4)
    month_str = CharField(7)
    category = CharField(16)
    during = IntegerField()
    nums = IntegerField()
    word_cloud = CharField()
    only_key = CharField()
    md5 = CharField()

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_my = {}
        for key, value in zip(self.field_names,self.field_values):
            dict_my[key.replace("`", "")] = value.replace("'", "")
        return dict_my

    @staticmethod
    def get_table_name():
        return __class__.__name__.lower()


if __name__ == "__main__":
    print(Time_Details.get_table_name())

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

