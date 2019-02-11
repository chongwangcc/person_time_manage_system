#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/29 14:39 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : SqlTools.py 
# @Software: PyCharm


from Entity import *

g_sqlite3_path = "./data/sqlit3.db"
set_db_name(g_sqlite3_path)


def execute_script(sqlite3_file_path, sql_script_path):
    """
    执行sql脚本
    :return:
    :param sqlite3_file_path
    :param sql_script_path
    """
    import sqlite3
    with open(sql_script_path, mode="r", encoding="utf8") as f:
        create_sql = f.read()
        conn = sqlite3.connect(sqlite3_file_path)
        c = conn.cursor()
        c.executescript(create_sql)
        conn.commit()
        conn.close()
        return True
    return False


def create_table(mode="create"):
    """
    按照条件选择是否创建表格
    :param mode:
    :return:
    """
    global g_sqlite3_path
    if mode in ["create"]:
        create_script = r"./data/create_table.sql"
        execute_script(g_sqlite3_path, create_script)
    elif mode in ["drop"]:
        delete_script = r"./data/drop_table.sql"
        execute_script(g_sqlite3_path, delete_script)
    else:
        print("[ERROR] unkown mode "+mode)


def fetch_userInfo(user_name):
    """
    获得用户信息类
    :param user_name:
    :return:
    """
    try:
        userinfo = User_Info.get(user_name=user_name)
        return userinfo
    except:
        pass
    return None


def get_time_details(user_id, start_date, end_date):
    """
    获得时间明细的记录
    :param user_id:
    :param start_date: 包含前者，包含后者
    :param end_date:
    :return:
    """
    time_details = Time_Details.query()\
        .filter(user_id=user_id)\
        .filter(date_str=start_date, operator=">=")\
        .filter(date_str=end_date, operator="<=").all()
    return time_details


def save_time_details(user_id, date_str, detail_list):
    """
    保存时间明细记录, 一天的一次性插入，把start_date的删除，然后再插入新纪录
    :param user_id:
    :param date_str 这批记录是哪一天的记录？
    :param detail_list: 列表，每个元素是Time_Details 对象
    :return:
    """
    # 0. 检查detail_list记录是不是全部是user_id + date_str 的记录
    b_list = [detail.user_id==user_id and date_str==detail.date_str for detail in detail_list]
    if not all(b_list) and detail_list is not None and len(detail_list)>0:
        print("detial_list结果不对")
        return False

    # 1.删除旧记录
    old_details = get_time_details(user_id, date_str, date_str)
    [detail.delete() for detail in old_details]

    # 2.插入新纪录
    [detail.save() for detail in detail_list]
    return True


def get_everyday_cache(user_id, start_date, end_date):
    """
    获得每天缓存的统计数据
    :param user_id:
    :param start_date:
    :param end_date:
    :return:
    """
    everyday_cache = Everyday_Cache.query()\
        .filter(user_id=user_id)\
        .filter(date_str=start_date, operator=">=")\
        .filter(date_str=end_date, operator="<=").all()
    return everyday_cache


def save_everyday_cache(user_id, date_str, cache_list):
    """
    保存每天的缓存，先删除记录，后插入记录
    :param user_id:
    :param date_str 这批记录是哪一天的记录？
    :param cache_list: 列表，每个元素是Time_Details 对象
    :return:
    """
    # 0. 检查detail_list记录是不是全部是user_id + date_str 的记录
    b_list = [cache.user_id == user_id and date_str == cache.date_str for cache in cache_list]
    if not all(b_list) and cache_list is not None and len(cache_list)>0:
        print("cache_list 结果不对")
        return False

    # 1.删除旧记录
    old_cache = get_everyday_cache(user_id, date_str, date_str)
    [cache.delete() for cache in old_cache]

    # 2.插入新纪录
    [cache.save() for cache in cache_list]
    return True


def get_everyweek_cache(user_id, start_date, end_date):
    """
    获得每天缓存的统计数据
    :param user_id:
    :param start_date: 每周开始日期
    :param end_date:  每周结束日期
    :return:
    """
    everyweek_cache = Every_week_Cache.query()\
        .filter(user_id=user_id)\
        .filter(start_date_str=start_date, operator=">=")\
        .filter(start_date_str=end_date, operator="<=").all()
    return everyweek_cache


def save_everyweek_cache(user_id, date_str, cache_list):
    """
    保存每周的缓存，先删除记录，后插入记录
    :param user_id:
    :param date_str 这批记录是哪一天的记录？
    :param cache_list: 列表，每个元素是Time_Details 对象
    :return:
    """
    # 0. 检查detail_list记录是不是全部是user_id + date_str 的记录
    b_list = [cache.user_id == user_id and date_str == cache.start_date_str for cache in cache_list]
    if not all(b_list) and cache_list is not None and len(cache_list)>0:
        print("cache_list 结果不对")
        return False

    # 1.删除旧记录
    old_cache = get_everyweek_cache(user_id, date_str, date_str)
    [cache.delete() for cache in old_cache]

    # 2.插入新纪录
    [cache.save() for cache in cache_list]
    return True


def get_everymonth_cache(user_id, start_date, end_date):
    """
    获得每月缓存的统计数据
    :param user_id:
    :param start_date: 每周开始日期
    :param end_date:  每周结束日期
    :return:
    """
    everymonth_cache = Every_month_Cache.query()\
        .filter(user_id=user_id)\
        .filter(month_str=start_date, operator=">=")\
        .filter(month_str=end_date, operator="<=").all()
    return everymonth_cache


def save_everymonth_cache(user_id, date_str, cache_list):
    """
    保存每周的缓存，先删除记录，后插入记录
    :param user_id:
    :param date_str 这批记录是哪一天的记录？
    :param cache_list: 列表，每个元素是Time_Details 对象
    :return:
    """
    # 0. 检查detail_list记录是不是全部是user_id + date_str 的记录
    b_list = [cache.user_id == user_id and date_str == cache.month_str for cache in cache_list]
    if not all(b_list) and cache_list is not None and len(cache_list)>0:
        print("cache_list 结果不对")
        return False

    # 1.删除旧记录
    old_cache = get_everymonth_cache(user_id, date_str, date_str)
    [cache.delete() for cache in old_cache]

    # 2.插入新纪录
    [cache.save() for cache in cache_list]
    return True


if __name__ == "__main__":
    pass
    # create_table("drop")
    # create_table()
    user_info = fetch_userInfo("cc")
    print(user_info)
    detail_list = []
    for i in range(10):
        time_details=Every_week_Cache()
        time_details.user_id = user_info.id
        time_details.start_date_str = "2019-01-02"
        time_details.end_date_str = "2019-01-02"
        time_details.category ="运动"
        time_details.during = 25
        time_details.nums = 12
        detail_list.append(time_details)

    save_everyweek_cache(user_info.id, "2019-01-02", detail_list)

    de = get_time_details(3, start_date="2019-01-01", end_date="2019-01-01")
    print(de)



