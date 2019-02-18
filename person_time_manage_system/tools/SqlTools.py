#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/29 14:39 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : SqlTools.py 
# @Software: PyCharm


from tools.Entity import *
import pandas as pd

g_sqlite3_path = "./data/sqlit3.db"
set_db_name(g_sqlite3_path)


def fetch_user_info(user_name):
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


def insert_default_user():
    """
    插入默认的用户，只有当表内容为空时，才执行这个
    :return:
    """
    if not User_Info.is_user_exist():
        print("insert default user cc, mm")
        global g_sqlite3_path
        set_db_name(g_sqlite3_path)

        userinfo = User_Info()
        userinfo.user_name = "cc"
        userinfo.password = "123456"
        userinfo.active = 1
        userinfo.auth_token_file = r"./data/.credentials/cc_calendar.json"
        userinfo.calender_server = "google"
        userinfo.calender_name = "时间日志"
        userinfo.save()

        userinfo = User_Info()
        userinfo.user_name="mm"
        userinfo.password="123456"
        userinfo.active=1
        userinfo.auth_token_file = r"./data/.credentials/mm_calendar.json"
        userinfo.calender_server = "google"
        userinfo.calender_name = "时间日志"
        userinfo.save()


def get_time_details_df(user_id, start_date, end_date):
    """
    获得时间明细的记录
    :param user_id:
    :param start_date: 包含前者，包含后者
    :param end_date:
    :return: Dataframe
    """
    conn = sqlite3.connect(g_sqlite3_path)
    sql = "select * from "+Time_Details.get_table_name()
    sql += " where "
    sql += " user_id == " +str(user_id) +" and "
    sql += " date_str >= '" + start_date + "' "+" and "
    sql += " date_str <= '" + end_date + "' "
    time_details_df = pd.read_sql_query(sql, conn)
    return time_details_df


def update_time_detials_df(user_id, start_date_str, end_date_str, df_new):
    """
    保存dataframe 到数据库中，先删除，后插入
    :param usid_id:
    :param start_date_str:
    :param end_date_str:
    :param df_new:
    :return:
    """
    # 创建表
    is_update = False
    update_date_list = []
    Time_Details.try_create_table()
    df_new["id"] = 0
    # 从数据库中读旧内容
    conn = sqlite3.connect(g_sqlite3_path)
    sql = "select * from " + Time_Details.get_table_name()
    sql += " where "
    sql += " user_id == " + str(user_id) + " and "
    sql += " date_str >= '" + start_date_str + "' " + " and "
    sql += " date_str <= '" + end_date_str + "' "
    df_old = pd.read_sql_query(sql, conn)
    print("time_detials old_df :"+ str(len(df_old)))
    print("time_detials df_new :" + str(len(df_new)))

    # 比较两批dataframe 的不同之处
    delete_df = df_old.append(df_new, sort=True)\
                        .append(df_new, sort=True)\
                        .drop_duplicates(subset=["only_key","md5"], keep=False)
    update_df = df_new.append(df_old, sort=True)\
                        .append(df_old, sort=True)\
                        .drop_duplicates(subset=["only_key", "md5"], keep=False)\
                        .drop_duplicates(subset=["only_key"], keep="first")
    print("time_detials delete_df :" + str(len(delete_df)))
    print("time_detials update_df :" + str(len(update_df)))
    if len(delete_df)>0 or len(update_df)>0:
        is_update = True
    # 先删除，后更新  # 保存dataframe
    [Time_Details.get(id=rows["id"]).delete() for index, rows in delete_df.iterrows()]

    update_df = update_df.drop(columns=["id"])
    update_df.to_sql(Time_Details.get_table_name(), conn, if_exists="append", chunksize=500, index=False)

    # 构造返回结果：是否更新，变动的日期
    update_date_list.extend(update_df["date_str"].tolist())
    update_date_list.extend(delete_df["date_str"].tolist())
    update_date_list = list(set(update_date_list))
    update_date_list.sort()
    return is_update, update_date_list


def get_everyday_cache_df(user_id, start_date, end_date):
    """
    获得每天缓存的统计数据
    :param user_id:
    :param start_date:
    :param end_date:
    :return:Dataframe
    """
    conn = sqlite3.connect(g_sqlite3_path)
    sql = "select * from "+Everyday_Cache.get_table_name()
    sql += " where "
    sql += " user_id == " +str(user_id) +" and "
    sql += " date_str >= '" + start_date + "' "+" and "
    sql += " date_str <= '" + end_date + "' "
    df = pd.read_sql_query(sql, conn)
    return df


def update_everyday_cache_df(user_id, start_date_str, end_date_str, df_new):
    """

    :param user_id:
    :param start_date_str:
    :param end_date_str:
    :param df_new:
    :return:
    """
    is_update = False
    update_date_list = []
    Everyday_Cache.try_create_table()
    # 从数据库中读旧内容
    conn = sqlite3.connect(g_sqlite3_path)
    sql = "select * from " + Everyday_Cache.get_table_name()
    sql += " where "
    sql += " user_id == " + str(user_id) + " and "
    sql += " date_str >= '" + start_date_str + "' " + " and "
    sql += " date_str <= '" + end_date_str + "' "
    df_old = pd.read_sql_query(sql, conn)
    print("everyday_cache df_old :" + str(len(df_old)))
    print("everyday_cache df_new :" + str(len(df_new)))
    # 比较两批dataframe 的不同之处
    delete_df = df_old.append(df_new, sort=True) \
        .append(df_new, sort=True) \
        .drop_duplicates(subset=["only_key", "md5"], keep=False)
    update_df = df_new.append(df_old, sort=True) \
        .append(df_old, sort=True) \
        .drop_duplicates(subset=["only_key", "md5"], keep=False) \
        .drop_duplicates(subset=["only_key"], keep="first")
    print("everyday_cache delete_df :" + str(len(delete_df)))
    print("everyday_cache update_df :" + str(len(update_df)))
    if len(delete_df) > 0 or len(update_df) > 0:
        is_update = True
    # 先删除，后更新  # 保存dataframe
    [Everyday_Cache.get(id=rows["id"]).delete() for index, rows in delete_df.iterrows()]
    update_df.to_sql(Everyday_Cache.get_table_name(), conn, if_exists="append", chunksize=500, index=False)

    #构造返回结果：是否更新，变动的日期
    update_date_list.extend(update_df["date_str"].tolist())
    update_date_list.extend(delete_df["date_str"].tolist())
    update_date_list = list(set(update_date_list))
    update_date_list.sort()
    return is_update, update_date_list


if __name__ == "__main__":
    pass
    # create_table("drop")
    # create_table()
    # user_info = fetch_userInfo("cc")
    # print(user_info)
    # detail_list = []
    # for i in range(10):
    #     time_details=Every_week_Cache()
    #     time_details.user_id = user_info.id
    #     time_details.start_date_str = "2019-01-02"
    #     time_details.end_date_str = "2019-01-02"
    #     time_details.category ="运动"
    #     time_details.during = 25
    #     time_details.nums = 12
    #     detail_list.append(time_details)
    #
    # save_everyweek_cache(user_info.id, "2019-01-02", detail_list)
    #
    # de = get_time_details(3, start_date="2019-01-01", end_date="2019-01-01")
    # print(de)
    insert_default_user()

    print(User_Info.is_user_exist())



