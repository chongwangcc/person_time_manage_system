#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/2/11 15:52 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : BussinessLogic.py 
# @Software: PyCharm
# 业务逻辑代码
import queue
import threading
import time

import SqlTools
import CalenderTools
import DateTools
from Entity import Time_Details,Everyday_Cache,Every_week_Cache,Every_month_Cache
# 0. pd 打印调试开关
import pandas as pd
pd.set_option('display.max_columns', None)

# 一些全局队列
network_calender_query_queue = queue.Queue()    # 网络查询日历的任务队列
cache_calc_queue = queue.Queue()  # 计算缓存任务的队列
statistics_cache = {}  # 缓存对象


class CalenderQueryTask:
    """
    日历查询的任务，一个对象是一个任务
    """
    def __init__(self, user_info, start_date, end_date):
        self.user_info = user_info
        self.start_date = start_date
        self.end_date = end_date


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
        key = str(self.user_info.id)+"_"+self.freq+"_"+self.start_date_str
        return key

    def __str__(self):
        return self.get_key()


class CacherCalcService:
    """
    计算缓存对象的服务类
    """

    def __init__(self, cache_task):
        """

        :param cache_task:  CacheCalcTask对象
        """
        self.cache_task = cache_task
        self.details_df = None
        self.dayly_cache_str_map = None
        self.dayly_cache_df = None
        self.weekly_cache_df = None
        self.weekly_cache_str_map = None
        self.monthly_cache_str_map = None
        self.monthly_cache_df = None

    def load_date_details(self, force=False):
        """
        加载数据明细，从数据库中读数据明细
        # 计算缓存时，假设数据都已经同步到缓存中了
        :return:
        """
        if self.details_df is None or force:
            details_df = SqlTools.get_time_details_df(self.cache_task.user_info.id,
                                      self.cache_task.start_date_str,
                                      self.cache_task.end_date_str)
            self.details_df = details_df

    def calc_dayly_cache(self):
        """
        计算某一天的缓存数据
        前提条件：每天的明细数据已经入库了
        :return:
        """
        # 1. 分组统计结果
        group_day = self.details_df.groupby(by=["date_str", "category"])
        during_sum_df = group_day["during"].sum().reset_index()
        description_df = group_day["description"].aggregate(lambda x: ",".join(x)).reset_index()
        count_df = group_day["during"].count().reset_index()
        df_final = during_sum_df
        df_final["word_cloud"] = description_df["description"]
        df_final["nums"] = count_df["during"]
        df_final["user_id"] = self.cache_task.user_info.id
        self.dayly_cache_df = df_final

        # 2. 保存缓存到数据库中
        self.dayly_cache_str_map = {}
        for index, row in df_final.iterrows():
            day_cache = Everyday_Cache()
            day_cache.user_id = row["user_id"]
            day_cache.date_str = row["date_str"]
            day_cache.category = row["category"]
            day_cache.during = row["during"]
            day_cache.nums = row["nums"]
            day_cache.word_cloud = row["word_cloud"]
            m_ll = self.dayly_cache_str_map.setdefault(row["date_str"], [])
            m_ll.append(day_cache)
        return self.dayly_cache_str_map


    def calc_weekly_cache(self):
        """
        计算某一周的cache
        前提条件：每天的缓存数据已经入库了，并且是最新的
        :return: 返回json串
        """
        # 1. 判断要不要从数据库中读数据
        if self.dayly_cache_df is None:
            dayly_cache_df = SqlTools.get_everyday_cache_df(self.cache_task.user_info.id,
                                                      self.cache_task.start_date_str,
                                                      self.cache_task.end_date_str)
            self.dayly_cache_df = dayly_cache_df
        if len(self.dayly_cache_df) == 0:
            return None

        # 2. 计算每周的缓存
        self.dayly_cache_df["start_date_str"] = self.dayly_cache_df["date_str"]\
                                                        .map(lambda x: DateTools.calc_week_begin_end_date(x)[0])
        self.dayly_cache_df["end_date_str"] = self.dayly_cache_df["date_str"]\
                                                        .map(lambda x: DateTools.calc_week_begin_end_date(x)[1])
        group_week = self.dayly_cache_df.groupby(by=["user_id", "start_date_str", "end_date_str", "category"])
        during_sum_df = group_week.sum().reset_index()
        description_df = group_week["word_cloud"].aggregate(lambda x: ",".join(x)).reset_index()
        df_final = during_sum_df
        df_final["word_cloud"] = description_df["word_cloud"]
        self.weekly_cache_df = df_final

        # 2. 保存缓存到数据库中
        self.weekly_cache_str_map = {}
        for index, row in df_final.iterrows():
            week_cache = Every_week_Cache()
            week_cache.user_id = row["user_id"]
            week_cache.start_date_str = row["start_date_str"]
            week_cache.end_date_str = row["end_date_str"]
            week_cache.category = row["category"]
            week_cache.during = row["during"]
            week_cache.nums = row["nums"]
            week_cache.word_cloud = row["word_cloud"]
            m_ll = self.weekly_cache_str_map.setdefault(row["start_date_str"], [])
            m_ll.append(week_cache)
        return self.weekly_cache_str_map


        print(self.weekly_cache_df)
        return []

    def calc_monthly_cache(self):
        """
        TODO 计算某一月的cache
        前提条件：每天的缓存数据已经入库了，并且是最新的
        :return: 返回json串
        """
        # 1. 判断要不要从数据库中读数据
        if self.dayly_cache_df is None:
            dayly_cache_df = SqlTools.get_everyday_cache_df(self.cache_task.user_info.id,
                                                            self.cache_task.start_date_str,
                                                            self.cache_task.end_date_str)
            self.dayly_cache_df = dayly_cache_df
        if len(self.dayly_cache_df) == 0:
            return None

        # 2. 计算每月的缓存
        self.dayly_cache_df["month_str"] = self.dayly_cache_df["date_str"].map(lambda x: x[:7])
        group_month = self.dayly_cache_df.groupby(by=["user_id", "month_str", "category"])
        during_sum_df = group_month.sum().reset_index()
        description_df = group_month["word_cloud"].aggregate(lambda x: ",".join(x)).reset_index()
        df_final = during_sum_df
        df_final["word_cloud"] = description_df["word_cloud"]
        self.monthly_cache_df = df_final

        # 2. 保存缓存到数据库中
        self.monthly_cache_str_map = {}
        for index, row in df_final.iterrows():
            month_cache = Every_month_Cache()
            month_cache.user_id = row["user_id"]
            month_cache.month_str = row["month_str"]
            month_cache.category = row["category"]
            month_cache.during = row["during"]
            month_cache.nums = row["nums"]
            month_cache.word_cloud = row["word_cloud"]
            m_ll = self.monthly_cache_str_map.setdefault(row["month_str"], [])
            m_ll.append(month_cache)
        return self.monthly_cache_str_map

    def calc_yearly_cache(self):
        """
        TODO 计算某一年的cache
        :return:
        """
        return []

    def calc(self):
        """
        计算，返回值
        :return:
        """
        self.load_date_details()
        result = None
        if self.cache_task.freq in ["day"]:
            result = self.calc_dayly_cache()
        elif self.cache_task.freq in ["week"]:
            result = self.calc_weekly_cache()
        elif self.cache_task.freq in ["month"]:
            result = self.calc_monthly_cache()
        elif self.cache_task.freq in ["year"]:
            result = self.calc_yearly_cache()
        return result

    def save(self):
        """
        TODO 将缓存结果保存到 数据库中
        :return:
        """
        if self.dayly_cache_str_map is not None:
            for key, value in self.dayly_cache_str_map.items():
                SqlTools.save_everyday_cache(self.cache_task.user_info.id,
                                             key,
                                             value)
        if self.weekly_cache_str_map is not None:
            for key, value in self.weekly_cache_str_map.items():
                SqlTools.save_everyweek_cache(self.cache_task.user_info.id,
                                             key,
                                             value)

        if self.monthly_cache_str_map is not None:
            for key, value in self.monthly_cache_str_map.items():
                SqlTools.save_everymonth_cache(self.cache_task.user_info.id,
                                             key,
                                             value)


def add_calender_query_task(query_task):
    """
    添加一个 日历查询的任务
    :param query_task: CalenderQueryTask 对象
    :return:
    """
    if query_task is None:
        return False
    network_calender_query_queue.put(query_task)
    return True


def add_cache_calc_task(calc_task):
    """
    添加calc 任务
    :param calc_task:
    :return:
    """
    if query_task is None:
        return False
    cache_calc_queue.put(calc_task)
    return True


def calder_query_func():
    """
    查询日历查询队列，网络读取数据
    :return:
    """
    while True:
        # 1. 阻塞获取  远程查询任务
        query_task = network_calender_query_queue.get(block=True)  # CalenderQueryTask 对象
        if query_task is None:
            time.sleep(1)
            continue
        # 2. 调用网络层，获得数据
        calender_server = CalenderTools.CalenderServer()
        final_result, missing_during = calender_server.get_time_details(query_task.user_info,
                                         start_date=query_task.start_date,
                                         end_date=query_task.end_date)
        # print(final_result)
        # print(missing_during)
        # 3. 保存到 数据库中
        t_date_str_map = {}
        for res in final_result:
            t_date_str = res[3]
            time_detail_model = Time_Details()
            time_detail_model.user_id = res[0]
            time_detail_model.category = res[1]
            time_detail_model.description = res[2]
            time_detail_model.date_str = res[3]
            time_detail_model.week_nums = res[4]
            time_detail_model.start_time = res[5]
            time_detail_model.end_time = res[6]
            time_detail_model.during = res[7]
            m_ll = t_date_str_map.setdefault(t_date_str, [])
            m_ll.append(time_detail_model)
        for key, value in t_date_str_map.items():
            SqlTools.save_time_details(query_task.user_info.id,
                                       key,
                                       value)
        # 4. 创建 cache计算任务,加入cache计算队列
        # 计算 又影响的 dayly, weekly,monthly, yearly 缓存数据
        dayly_key = list(t_date_str_map.keys())
        weekly_key = DateTools.gen_week_list_in_days(dayly_key)
        month_key = DateTools.gen_month_list_in_days(dayly_key)
        yearly_key = DateTools.gen_year_list_in_days(dayly_key)
        for t_dayly in dayly_key:
            t_cachercalc_task = CacheCalcTask(query_task.user_info,
                                              "day",
                                              t_dayly,
                                              t_dayly)
            add_cache_calc_task(t_cachercalc_task)
        for t_weekly in weekly_key:
            t_cachercalc_task = CacheCalcTask(query_task.user_info,
                                              "week",
                                              t_weekly[0],
                                              t_weekly[1])
            add_cache_calc_task(t_cachercalc_task)
        for t_monthly in month_key:
            t_cachercalc_task = CacheCalcTask(query_task.user_info,
                                              "month",
                                              t_monthly+"-01",
                                              t_monthly+"-31")
            add_cache_calc_task(t_cachercalc_task)
        for t_yearly in yearly_key:
            t_cachercalc_task = CacheCalcTask(query_task.user_info,
                                              "year",
                                              t_yearly+"-01-01",
                                              t_yearly+"-12-31")
            add_cache_calc_task(t_cachercalc_task)

        # 5. 休眠一下
        time.sleep(1)


def cache_calc_func():
    """
    读 缓存任务队列，计算数据的统计缓存
    :return:
    """
    while True:
        # 1. 阻塞获取  cache计算任务
        cache_task = cache_calc_queue.get(block=True)  # CacheCalcTask 对象
        print(cache_task)

        # 2. 计算缓存
        cache_service = CacherCalcService(cache_task)
        json_result = cache_service.calc()
        cache_service.save()  # 保存到mysql数据库中

        # 3. TODO 将JSON添加到缓存内存中


def start():
    """
    开启后台线程
    :return:
    """
    # 1.创建数据库，插入默认用户信息
    SqlTools.insert_default_user()
    # 2. 开启线程
    th1 = threading.Thread(target=calder_query_func)  # 查询calendar 线程
    th2 = threading.Thread(target=cache_calc_func)  # 查询calendar 线程
    threads = [th1, th2]
    for t in threads:
        t.setDaemon(True)
        t.start()
    # 3.等待线程结束，阻塞状态
    # t.join()

if __name__ == "__main__":
    # 2. 开启线程
    start()

    # 1.添加一个任务到队列中
    user_info = SqlTools.fetch_userInfo("cc")
    query_task = CalenderQueryTask(user_info, "2019-01-01", "2019-02-28")
    add_calender_query_task(query_task)

    aa = input()






