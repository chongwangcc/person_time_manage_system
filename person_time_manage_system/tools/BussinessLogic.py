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
    def calender_query_func():
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
            print("[INFO] start handling query_task [" + str(query_task) + "]")
            # 2. 调用网络层，获得数据
            calender_server = CalenderTools.CalenderServer()
            final_result, missing_during = calender_server.get_time_details(query_task.user_info,
                                                                            start_date=query_task.start_date,
                                                                            end_date=query_task.end_date)

            # 4. 转换为 Dataframe 方便后续处理
            columns = ["user_id", "category", "description", "date_str", "week_nums",
                       "start_time", "end_time", "during", "second_category", "md5"]
            time_detail_df = pd.DataFrame(final_result, columns=columns)
            time_detail_df["only_key"] = time_detail_df["user_id"].map(str) \
                                             + time_detail_df["date_str"].map(str) \
                                             + time_detail_df["start_time"].map(str) \
                                             + time_detail_df["end_time"].map(str)
            time_detail_df = time_detail_df.drop_duplicates(keep="first")
            # 3. 保存到 数据库中
            is_update, update_date_list = SqlTools.update_time_detials_df(query_task.user_info.id,
                                          query_task.start_date,
                                          query_task.end_date,
                                          time_detail_df)
            # 4. 如果更新了，重新计算每日缓存
            if is_update:

                print(update_date_list)
                t_task = CacheCalcTask(query_task.user_info, "day", query_task.start_date, query_task.end_date)
                StatisticsCalcService.add_cache_calc_task(t_task)
                print("[INFO] add  Statistics_task [" + str(t_task) + "]")

            print("[INFO] end handling query_task [" + str(query_task) + "]")


class StatisticsCalcService:
    """
    计算每天、每月、每年的统计数据服务类
    """

    def __init__(self, cache_task):
        """

        :param cache_task:  CacheCalcTask对象
        """
        self.cache_task = cache_task

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
            print("[INFO] start handling Statistics_task [" + str(cache_task) + "]")
            # 2. 计算缓存
            cache_service = StatisticsCalcService(cache_task)
            cache_service.calc_daily_statistics()

            # 3. TODO 将JSON添加到缓存内存中
            print("[INFO] end handling Statistics_task [" + str(cache_task) + "]")

    @staticmethod
    def md5_my(row):
        import hashlib
        t_md5 = hashlib.md5()
        [t_md5.update(str(t).encode("utf8")) for t in row.tolist()]
        return t_md5.hexdigest()

    def calc_daily_statistics(self):
        """
        计算某一天的缓存数据
        前提条件：每天的明细数据已经入库了
        :return:
        """

        details_df = SqlTools.get_time_details_df(self.cache_task.user_info.id,
                                  self.cache_task.start_date_str,
                                  self.cache_task.end_date_str)

        # 1. 分组统计结果
        group_day = details_df.groupby(by=["date_str", "category"])
        during_sum_df = group_day["during"].sum().reset_index()
        description_df = group_day["description"].aggregate(lambda x: ",".join(x)).reset_index()
        count_df = group_day["during"].count().reset_index()
        df_final = during_sum_df
        df_final["word_cloud"] = description_df["description"]
        df_final["nums"] = count_df["during"]
        df_final["user_id"] = self.cache_task.user_info.id
        df_final["year_str"] = df_final["date_str"].map(lambda  x : str(x)[:4])
        df_final["month_str"] = df_final["date_str"].map(lambda x: str(x)[:7])
        df_final["week_start_str"] = df_final["date_str"].map(lambda x: DateTools.calc_week_begin_end_date(x)[0])
        df_final["week_end_str"] = df_final["date_str"].map(lambda x: DateTools.calc_week_begin_end_date(x)[1])
        df_final["only_key"] = df_final["user_id"].map(str)\
                                   + df_final["date_str"].map(str) \
                                   + df_final["category"].map(str)

        df_final["md5"] = df_final.apply(StatisticsCalcService.md5_my, axis=1)
        self.dayly_cache_df = df_final

        # 2. 保存缓存到数据库中
        is_update, update_date_list = SqlTools.update_everyday_cache_df(self.cache_task.user_info.id,
                                          self.cache_task.start_date_str,
                                          self.cache_task.end_date_str,
                                          df_final)

        # 3.判断要不要重新计算web需要的json数据
        if is_update:
            CachCalcService.scan_and_update(self.cache_task.user_info.id, update_date_list)
        return


class CachCalcService:
    """
    计算 缓存数据 对象
    """
    @staticmethod
    def scan_and_update(user_id, update_date_list):
        """
        TODO 扫描计算缓存key, 计算json数据
        :return:
        """
        for key, value in web_cache.items():
            # 1. 判断数据有没有更新
            user_name, freq, start_date_str, end_date_str = key.split("_")
            if freq in ["day"]:
                pass
            elif freq in ["week"]:
                start_time_list = [DateTools.calc_week_begin_end_date(t_data)[0] for t_data in update_date_list]
                if start_date_str in start_time_list:
                    user_info = SqlTools.fetch_user_info(user_name)
                    calc_task = CacheCalcTask(user_info, freq, start_date_str, end_date_str)
                    CachCalcService.add_new_cache_calc_task(calc_task)
            elif freq in ["month"]:
                pass
            elif freq in ["year"]:
                pass

            # 2. 对于更新后的数据，重新计算缓存

            pass

    @staticmethod
    def calc_weekly_cache(cache_task):
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

    @staticmethod
    def calc_monthly_cache(cache_task):
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

    @staticmethod
    def calc_yearly_cache(cache_task):
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

    @staticmethod
    def add_new_cache_calc_task(cache_task):
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
            result = CachCalcService.calc_weekly_cache(cache_task)
        elif cache_task.freq in ["month"]:
            result = CachCalcService.calc_monthly_cache(cache_task)
        elif cache_task.freq in ["year"]:
            result = CachCalcService.calc_yearly_cache(cache_task)

        # 3.保存到缓存对象中
        if result is not None and len(result)>0:
            web_cache[cache_task.get_key()] = result
        return result

    @staticmethod
    def fetch_cache(cache_task):
        """
        查缓存获得任务，同时新建任务查询
        :param cache_task:
        :return:
        """
        # 0. 检查参数
        if cache_task is None:
            return {}
        # 1. 新建一条查询任务
        query_task = CalenderQueryTask(cache_task.user_info,
                                       cache_task.start_date_str,
                                       cache_task.end_date_str)
        QuerayCalenderService.add_calender_query_task(query_task)
        # 2. 查询缓存队列中是否有结果
        cache_result = web_cache.setdefault(cache_task.get_key(), None)
        if cache_result is None:
            # 2. 缓存队列为空，新建缓存队列计算任务
            CachCalcService.add_new_cache_calc_task(cache_task)
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
    th1 = threading.Thread(target=QuerayCalenderService.calender_query_func)  # 查询calendar 线程
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
    # user_info = SqlTools.fetch_user_info("cc")
    # query_task = CalenderQueryTask(user_info, "2019-01-01", "2019-02-28")
    # QuerayCalenderService.add_calender_query_task(query_task)

    # user_info = SqlTools.fetch_user_info("cc")
    # calc_task = CacheCalcTask(user_info, "day", "2018-01-01", "2019-02-28")
    # StatisticsCalcService.add_cache_calc_task(calc_task)


    aa = input()
    # user_info = SqlTools.fetch_userInfo("cc")
    # task = CacheCalcTask(user_info, "week", "2018-12-30", "2019-01-05")
    #
    # calc_service = CachCalcService(web_cache)
    # calc_service.add_new_cache(task)