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

import CalenderTools
from Entity import *
from CacheCalcTools import *

# 0. pd 打印调试开关
import pandas as pd
pd.set_option('display.max_columns', None)

# 一些全局队列
network_calender_query_queue = queue.Queue()    # 网络查询日历的任务队列
cache_calc_queue = queue.Queue()  # 计算缓存任务的队列
web_cache = {}


class QuerayCalenderService:
    """
    处理查询日历的服务类
    """
    @staticmethod
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

    @staticmethod
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
                print(key)
                SqlTools.save_time_details(query_task.user_info.id,
                                           key,
                                           value)
            # 4. 创建 cache计算任务,加入cache计算队列
            # 计算 又影响的 dayly, weekly,monthly, yearly 缓存数据
            dayly_key = list(t_date_str_map.keys())
            for t_dayly in dayly_key:
                t_cachercalc_task = CacheCalcTask(query_task.user_info,
                                                  "day",
                                                  t_dayly,
                                                  DateTools.calc_next_date(t_date_str))
                StatisticsCalcService.add_cache_calc_task(t_cachercalc_task)

            # 5. 休眠一下
            time.sleep(1)


class StatisticsCalcService:
    """
    计算每天、每月、每年的统计数据服务类
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

    @staticmethod
    def add_cache_calc_task(calc_task):
        """
        添加calc 任务
        :param calc_task:
        :return:
        """
        if calc_task is None:
            return False
        cache_calc_queue.put(calc_task)
        return True

    @staticmethod
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
            cache_service = StatisticsCalcService(cache_task)
            json_result = cache_service.calc()
            cache_service.save()  # 保存到mysql数据库中

            # 3. TODO 将JSON添加到缓存内存中

    def calc_daily_statistics(self):
        """
        计算某一天的缓存数据
        前提条件：每天的明细数据已经入库了
        :return:
        """

        if self.details_df is None:
            details_df = SqlTools.get_time_details_df(self.cache_task.user_info.id,
                                      self.cache_task.start_date_str,
                                      self.cache_task.end_date_str)
            self.details_df = details_df

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


    def calc(self):
        """
        计算，返回值
        :return:
        """
        result = None
        if self.cache_task.freq in ["day"]:
            result = self.calc_daily_statistics()
        elif self.cache_task.freq in ["week"]:
            result = self.calc_weekly_statistics()
        elif self.cache_task.freq in ["month"]:
            result = self.calc_monthly_statistics()
        elif self.cache_task.freq in ["year"]:
            result = self.calc_yearly_statistics()
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


class CachCalcService:
    """
    计算 缓存数据 对象
    """
    def __init__(self, web_cache):
        """
        缓存对象所在列
        :param web_cache:
        """
        self.web_cache = web_cache

    def scan_and_update(self):
        """
        TODO 扫描计算缓存key, 计算json数据
        :return:
        """
        for key, value in self.web_cache.items():
            # 1. 判断数据有没有更新

            # 2. 对于更新后的数据，重新计算缓存

            pass

    def calc_weekly_cache(self, cache_task):
        """
        计算每周的统计数据
        :param cache_task:
        :return:
        """
        week_service = WeeklyCacheCalcService(cache_task.user_info.id,
                                                        cache_task.start_date_str,
                                                        cache_task.end_date_str)
        result = week_service.get_cache_result()
        return result

    def calc_monthly_cache(self, cache_task):
        """

        :param cache_task:
        :return:
        """
        # 1. 读数据库 获得每月的统计数据
        result = {}
        last_month_1, last_month_2 = DateTools.calc_last_month_begin_end_date(cache_task.start_date_str)
        this_month_service = MonthlyCacheCalcSerive(cache_task.user_info.id,
                                              cache_task.start_date_str,
                                              cache_task.end_date_str)
        last_month_service = MonthlyCacheCalcSerive(cache_task.user_info.id,
                                                    last_month_1,
                                                    last_month_2)
        result["this_month"] = this_month_service.get_cache_result()
        result["last_month"] = last_month_service.get_cache_result()
        return result

    def calc_yearly_cache(self, cache_task):
        """

        :param cache_task:
        :return:
        """
        result = {}
        result["year"] = "2019"
        result["end_date"] = "01-29"
        result["working_tomato_nums"] = "40"
        result["study_tomato_nums"] = "60"
        result["workout_nums"] = "10"
        result["workout_hours"] = "45"

        # 1. 本月主题词云
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

        # 2. 每周时间走势图
        result["every_week_category_details"] = {'xData': ['2019-02-03'], 'legends': ['杂', '睡觉'],
                                                 'data': [[2.25], [7.5]], 'sum': [9.75]}

        # 3. 类别分布矩形图
        result["category_rectangle"] = {
            "工作": {
                "$count": 12,
                "开发": {
                    "$count": 34,
                },
                "运维": {
                    "$count": 46,
                },
                "开会": {
                    "$count": 78,
                },
            },
            "学习": {
                "$count": 12,
                "时间日志": {
                    "$count": 34,
                },
                "看书": {
                    "$count": 780,
                },
                "写笔记": {
                    "$count": 100,
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
        return result

    def add_new_cache_calc_task(self, cache_task):
        """
        添加一条新的 统计缓存任务到队列中
        :param cache_task:
        :return:
        """
        if cache_task is None:
            return False

        if cache_task.freq in ["day"]:
            # 不计算每天的 统计数据 json
            return False
        elif cache_task.freq in ["week"]:
            result = self.calc_weekly_cache(cache_task)
        elif cache_task.freq in ["month"]:
            result = self.calc_monthly_cache(cache_task)
        elif cache_task.freq in ["year"]:
            result = self.calc_yearly_cache(cache_task)

        # 3.保存到缓存对象中
        if result is not None and len(result)>0:
            self.web_cache[cache_task.get_key()] = result
        return result

    def fetch_cache(self, cache_task):
        """
        查缓存获得任务，同时新建任务查询
        :param cache_task:
        :return:
        """
        # 0. 检查参数
        if cache_task is None:
            return {}
        # 1. 查询缓存队列中是否有结果
        cache_result = web_cache.setdefault(cache_task.get_key(), None)
        if cache_result is None:
            # 2. 缓存队列为空，新建缓存队列计算任务
            self.add_new_cache_calc_task(cache_task)
            cache_result = web_cache.setdefault(cache_task.get_key(), None)
        if cache_result is None:
            cache_result = {}
        # 3.返回
        return cache_result


def start():
    """
    开启后台线程
    :return:
    """
    # 1.创建数据库，插入默认用户信息
    SqlTools.insert_default_user()
    # 2. 开启线程
    th1 = threading.Thread(target=QuerayCalenderService.calder_query_func)  # 查询calendar 线程
    th2 = threading.Thread(target=StatisticsCalcService.cache_calc_func)  # 查询calendar 线程
    threads = [th1, th2]
    for t in threads:
        t.setDaemon(True)
        t.start()
    # 3.等待线程结束，阻塞状态
    # t.join()


if __name__ == "__main__":
    #  2. 开启线程
    start()

    # 1.添加一个任务到队列中
    user_info = SqlTools.fetch_user_info("cc")
    query_task = CalenderQueryTask(user_info, "2018-01-01", "2019-02-28")
    QuerayCalenderService.add_calender_query_task(query_task)

    aa = input()
    # user_info = SqlTools.fetch_userInfo("cc")
    # task = CacheCalcTask(user_info, "week", "2018-12-30", "2019-01-05")
    #
    # calc_service = CachCalcService(web_cache)
    # calc_service.add_new_cache(task)