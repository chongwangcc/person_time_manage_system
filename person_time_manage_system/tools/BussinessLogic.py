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
from datetime import datetime

import SqlTools
import CalenderTools
import DateTools
from Entity import *

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
            weekly_key = DateTools.gen_week_list_in_days(dayly_key)
            month_key = DateTools.gen_month_list_in_days(dayly_key)
            yearly_key = DateTools.gen_year_list_in_days(dayly_key)
            for t_dayly in dayly_key:
                t_cachercalc_task = CacheCalcTask(query_task.user_info,
                                                  "day",
                                                  t_dayly,
                                                  DateTools.calc_next_date(t_date_str))
                StatisticsCalcService.add_cache_calc_task(t_cachercalc_task)
            for t_weekly in weekly_key:
                t_cachercalc_task = CacheCalcTask(query_task.user_info,
                                                  "week",
                                                  t_weekly[0],
                                                  t_weekly[1])
                StatisticsCalcService.add_cache_calc_task(t_cachercalc_task)
            for t_monthly in month_key:
                t_cachercalc_task = CacheCalcTask(query_task.user_info,
                                                  "month",
                                                  t_monthly + "-01",
                                                  t_monthly + "-31")
                StatisticsCalcService.add_cache_calc_task(t_cachercalc_task)
            for t_yearly in yearly_key:
                t_cachercalc_task = CacheCalcTask(query_task.user_info,
                                                  "year",
                                                  t_yearly + "-01-01",
                                                  t_yearly + "-12-31")
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

    def calc_weekly_statistics(self):
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

    def calc_monthly_statistics(self):
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

    def calc_yearly_statistics(self):
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

    def calc_missing_during(self, everyday_details_df):
        """
        计算重叠时段
        :param everyday_details_df:
        :return:
        """
        missing_during = []
        df_sort = everyday_details_df.sort_values(by=["date_str", "start_time"])
        if len(df_sort) <= 1:
            return missing_during

        # 2. 判断有没有漏掉/重叠的时段
        last_one = datetime.strptime(df_sort.iloc[0]["date_str"] + " " + df_sort.iloc[0]["start_time"], '%Y-%m-%d %H:%M:%S')
        for i, t_time in enumerate(df_sort.iterrows()):
            t_time = t_time[1]
            s_time = datetime.strptime(t_time["date_str"] + " " + t_time["start_time"], '%Y-%m-%d %H:%M:%S')
            if (s_time - last_one).total_seconds() < 60 and (last_one - s_time).total_seconds() < 60:
                pass
            elif s_time < last_one:
                # 重叠
                e_time_str = last_one.strftime("%m-%d %H:%M")
                s_time_str = s_time.strftime("%m-%d %H:%M")
                minute = round((last_one - s_time).total_seconds() / 60, 2)
                info = "重叠"
                t_d = {"start_time": s_time_str, "end_time": e_time_str, "during": minute, "type": info}
                missing_during.append(t_d)
            elif last_one > s_time:
                # 漏掉
                e_time_str = s_time.strftime("%m-%d %H:%M")
                s_time_str = last_one.strftime("%m-%d %H:%M")
                minute = round((s_time - last_one).total_seconds() / 60, 2)
                info = "漏掉"
                t_d = {"start_time": s_time_str, "end_time": e_time_str, "during": minute, "type": info}
                missing_during.append(t_d)
            last_one = datetime.strptime(t_time["date_str"] + " " + t_time["start_time"], '%Y-%m-%d %H:%M:%S')
        return missing_during

    def get_every_day_sum_of_category(self, result_list, label="睡觉"):
        """
        获得某类别，每天的时间
        :param result_list:
        :param label:
        :return:
        """
        df_t = result_list[result_list["category"] == label]
        result = []
        for index, row in df_t.iterrows():
            t_dict = {"category": row["date_str"], "hours": round(row["during"]/ 60, 2)}
            result.append(t_dict)
        return result

    def get_every_day_category_details(self, everday_df, day_padding=7):
        """
        获得所有明细
        :param everday_df:
        :param day_padding: 日期不够长时，加长日期
        :return:
        """
        xData = list(set(everday_df["date_str"]))
        xData.sort()
        legends = list(set(everday_df["category"]))
        legends.sort()
        sum = [0 for x in xData]
        every_day_sum = [[0 for x in xData] for l in legends]
        for i, t_day in enumerate(xData):
            t_count = 0
            for j, t_category in enumerate(legends):
                t_df = everday_df[(everday_df["date_str"]==t_day) & (everday_df["category"]==t_category)]
                if len(t_df) == 1:
                    every_day_sum[j][i] = round(t_df.iloc[0]["during"]/60, 2)
                    t_count += t_df.iloc[0]["during"]
            sum[i] = round(t_count/60, 2)

        result = {
            "xData": xData,
            "legends": legends,
            # 每个类别，每一天的时间，shape==（lengends.长度  *  xData.长度）
            "data": every_day_sum,
            "sum": sum  # 每天的总时间数
        }
        print(result)

        return result

    def calc_weekly_cache(self, cache_task):
        """
        计算每周的统计数据
        :param cache_task:
        :return:
        """
        # 1. 读数据库 获得每周的统计数据
        week_cache_list = SqlTools.get_everyweek_cache(cache_task.user_info.id,
                                                        cache_task.start_date_str,
                                                        cache_task.end_date_str)
        day_cache_df = SqlTools.get_everyday_cache_df(cache_task.user_info.id,
                                                        cache_task.start_date_str,
                                                        cache_task.end_date_str)
        day_details_df = SqlTools.get_time_details_df(cache_task.user_info.id,
                                                        cache_task.start_date_str,
                                                        cache_task.end_date_str)
        # print(week_cache_list)
        # print(day_cache_df)
        # 2. 转换为每周统计web需要的字典结构
        result = {}

        # 3.开始结束日期 工作-学习番茄数 锻炼娱乐次数
        result["start_date"] = cache_task.start_date_str
        result["end_date"] = cache_task.end_date_str
        result["each_category_time_sum"] = []
        result["execise_nums"] = 0
        result["fun_nums"] = 0
        result["working_tomato_nums"] = 0
        result["study_tomato_nums"] = 0
        for week_cache in week_cache_list:
            if week_cache.category in ["学习"]:
                result["study_tomato_nums"] = round(week_cache.during / 30, 2)
                pass
            elif week_cache.category in ["工作"]:
                result["working_tomato_nums"] = round(week_cache.during/30, 2)
                pass
            elif week_cache.category in ["运动"]:
                result["execise_nums"] = week_cache.nums
                pass
            elif week_cache.category in ["娱乐"]:
                result["fun_nums"] = week_cache.nums
                pass
            # 5. 类别 时间汇总
            t_dict = {"name": week_cache.category, "value": round(week_cache.during, 2)}
            result["each_category_time_sum"].append(t_dict)

        # 2. 番茄时钟达标率
        result["working_and_study_tomato_nums_of_each_day"] = result["working_tomato_nums"] + result[
            "study_tomato_nums"]

        # 3. 睡眠时间
        result["sleep_hours"] = {
            "standard_hours": 8,
            "actual_hours": self.get_every_day_sum_of_category(day_cache_df, label="睡觉")
        }

        # 4 .各项每天时间汇总
        result["every_day_category_details"] = self.get_every_day_category_details(day_cache_df,day_padding=7)

        # 6.  漏填、重复时段
        result["missing_info"] = self.calc_missing_during(day_details_df)
        return result

    def add_new_cache(self, cache_task):
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
    # # 2. 开启线程
    start()

    # 1.添加一个任务到队列中
    user_info = SqlTools.fetch_user_info("cc")
    query_task = CalenderQueryTask(user_info, "2019-01-01", "2019-02-28")
    QuerayCalenderService.add_calender_query_task(query_task)

    aa = input()
    # user_info = SqlTools.fetch_userInfo("cc")
    # task = CacheCalcTask(user_info, "week", "2018-12-30", "2019-01-05")
    #
    # calc_service = CachCalcService(web_cache)
    # calc_service.add_new_cache(task)