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
from datetime import datetime,date

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

    def get_every_month_category_during(self, month_df, category, month_str):
        """
        获得 每月缓存中，某类型的 持续时间,单位分钟
        :param month_df:
        :param category:
        :return:
        """
        during = 0
        if month_df is None or category is None:
            return during
        t_df = month_df[month_df["month_str"] == month_str & month_df["category"] == category]
        if len(t_df) == 1:
            during = t_df["during"]
        return during

    def get_every_month_category_nums(self, month_df, category, month_str):
        """
        获得 每月缓存中，某类型的 持续时间,单位分钟
        :param month_df:
        :param category:
        :return:
        """
        during = 0
        if month_df is None or category is None:
            return during
        t_df = month_df[month_df["month_str"] == month_str & month_df["category"] == category]
        if len(t_df) == 1:
            during = t_df["nums"]
        return during

    def get_month_during_percent(self, start_date_str):
        """
        计算每月过了多久了
        :param start_date_str:
        :return:
        """
        during_percent = 0
        today_str = date.today().strftime('%Y-%m-%d')
        if today_str[:7] == start_date_str[:7]:
            minDate, maxDate = DateTools.calc_month_begin_end_date(start_date_str)
            now_int = int(today_str[-2:])
            all_int = int(maxDate[-2:])
            during_percent = round(now_int/all_int, 2)
        elif today_str[:7] < start_date_str[:7]:
            during_percent = 0
        else:
            during_percent = 1
        return during_percent

    def get_month_living_percent(self, month_cache_df):
        """
        计算活着时间的总数：活着时间定义---除去睡觉和杂的时间
        :param month_cache_df:
        :return:
        """
        total_minuts = month_cache_df["during"].sum()
        living_df = month_cache_df[month_cache_df["category"] != "睡觉" & month_cache_df["category"] != "杂"]
        living_minuts = living_df["during"].sum()

        return round(living_minuts/total_minuts, 2)

    def get_month_word_cloud(self, month_cache_df):
        """
        计算 词云图频率
        :param month_cache_df:
        :return:
        """
        # 1.所有描述合并到一个字符串上
        description = ""
        words_series = month_cache_df["word_cloud"]
        for index, value in words_series.iteritems():
            description += (","+value["word_cloud"])

        # 2. 拆分字符串
        import re
        ss = re.split(u",| |;|，|；|:|：|～", description)

        # 3. 统计词频
        freq_dict = {}
        for s in ss:
            if len(s) <= 1:
                continue
            freq = freq_dict.setdefault(s,0)
            freq += 1
            freq_dict[s] = freq

        #4. 生成需要的格式
        words = []
        for key,value in freq_dict.items():
            t_dict = {"name": key, "value": value}
            words.append(t_dict)

        return words

    def get_month_ablity_randar(self, month_df, month_str):
        """
        计算每月的各项内容雷达值,0--10之间的一个数值
        :param month_df:
        :return:
        """
        result = [0, 0, 0, 0, 0, 0]  # ？？？、睡眠力、工作力、娱乐力、运动力、学习力
        month_pass = self.get_month_during_percent(month_str + "-01")
        month_total_days = DateTools.calc_month_total_days(month_str+"-01")
        # 1.工作力 得分计算规则
        work_minutes = self.get_every_month_category_during(month_df, "工作", month_str)
        stand_work_hours = 40*5/7*month_pass*month_total_days
        work_score = round(work_minutes/60/stand_work_hours*10, 0)
        if work_score > 10:
            work_score = 10

        # 2. 学习力 得分计算规则
        study_minutes = self.get_every_month_category_during(month_df, "学习", month_str)
        stand_study_hours = (3+8/7)*month_total_days*month_pass
        study_score = round(study_minutes/60/stand_study_hours*10, 0)
        if study_score > 10:
            study_score = 10

        # 3. 娱乐力 得分计算规则
        fun_num = self.get_every_month_category_nums(month_df, "娱乐", month_str)
        stand_fun_nums = int(8/7*month_pass*month_total_days)
        fun_score = round(fun_num/stand_fun_nums, 0)
        if fun_score > 10 :
            fun_score = 10

        # 4. 运动力 得分计算规则
        workoutnum = self.get_every_month_category_nums(month_df, "运动", month_str)
        stand_workout_nums = int(5/7*month_total_days*month_pass)
        workout_score = round(workoutnum/stand_workout_nums, 0)
        if workout_score > 10:
            workout_score = 10

        # 5. 睡眠力 得分计算规则
        sleep_minutes = self.get_every_month_category_during(month_df, "睡觉", month_str)
        stand_sleep_hours = 8*month_pass*month_total_days
        sleep_score = abs(round((sleep_minutes/60-8)/(month_total_days*24), 2))
        if sleep_score > 10:
            sleep_score = 10

        result = [0, sleep_score, work_score, fun_score,sleep_score, workout_score, study_score]
        return result

    def get_month_ring_map(self, this_month_df,
                           last_month_df,
                           this_month_str,
                           last_month_str,
                           categolry=["工作", "学习", "运动"]):
        """
        计算month 各类别的环比图
        :param this_month_df:
        :param last_month_df:
        :param categolry:
        :return:
        """
        month_pass = self.get_month_during_percent(this_month_str + "-01")
        result = {}
        result["last_month"] = []
        result["this_month"] = []
        result["growth"] = []
        result["type"] = []

        for cat_t in categolry:
            last_month_hours = self.get_every_month_category_nums(last_month_df, cat_t,last_month_str)
            last_month_hours = round(last_month_hours/60, 2)
            last_month_hours = last_month_hours*month_pass

            this_month_hours = self.get_every_month_category_nums(this_month_df, cat_t, this_month_str)
            this_month_hours = round(this_month_hours/60, 2)

            result["last_month"].append(last_month_hours)
            result["this_month"].append(this_month_hours)
            result["type"].append(cat_t)
            t_grouth = 0
            if result["last_month"] !=0:
                t_grouth = (result["this_month"]-result["last_month"])/result["last_month"]
            result["growth"].append(t_grouth)

        return result


    def get_month_living_trend(self, day_cache_df):
        """
        获得时间的走势图，按照日期排序
        :param day_cache_df:
        :return:
        """
        living_df = day_cache_df[day_cache_df["category"] != "睡觉" & day_cache_df["category"] != "杂"]
        living_df.groupby(by=["date_str"]).sum()
        living_df = living_df[["date_str", "during"]].sort_values(by='date_str')
        int_day = 0
        result = []
        for index, row in living_df.iterrows():
            t_int_day = int(row["date_str"][-2:])
            if t_int_day == (int_day+1):
                result.append(round(row["during"]/60, 2))
            elif t_int_day > (int_day+1):
                result.extend([0 for i in range(t_int_day-int_day-1)])
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

    def calc_monthly_cache(self, cache_task):
        """

        :param cache_task:
        :return:
        """
        # 1. 读数据库 获得每月的统计数据
        last_month_start, last_month_end = DateTools.calc_last_mont_begin_end_date()

        month_cache_df = SqlTools.get_everymonth_cache_df(cache_task.user_info.id,
                                                      cache_task.start_date_str,
                                                      cache_task.end_date_str)
        last_month_cache_df = SqlTools.get_everymonth_cache_df(cache_task.user_info.id,
                                                               last_month_start,
                                                               last_month_end)

        day_cache_df = SqlTools.get_everyday_cache_df(cache_task.user_info.id,
                                                      cache_task.start_date_str,
                                                      cache_task.end_date_str)
        last_day_cache_df = SqlTools.get_everyday_cache_df(cache_task.user_info.id,
                                                               last_month_start,
                                                               last_month_end)

        month_str = cache_task.start_date_str[:7]
        last_month_str = last_month_start[:7]
        print(month_cache_df)
        # 构造结果
        result = {}
        result["start_date"] = cache_task.start_date_str
        result["end_date"] = cache_task.end_date_str
        result["working_tomato_nums"] = round(self.get_every_month_category_during(month_cache_df,
                                                                             "工作",
                                                                             month_str)/60, 2)
        result["study_tomato_nums"] = round(self.get_every_month_category_during(month_cache_df,
                                                                             "学习",
                                                                             month_str)/60, 2)
        result["during_percent"] = "%.2f%%" % self.get_month_during_percent(cache_task.start_date_str)
        result["living_percent"] = "%.2f%%" % self.get_month_living_percent(month_cache_df)

        # 1. 本月主题词云
        result["word_cloud"] = self.get_month_word_cloud(month_cache_df)
        # 2. 各项能力雷达图
        result["ability_redar"] = [
            {
                "value": self.get_month_ablity_randar(last_month_cache_df, last_month_str),
                "name": '上月',
            }, {
                "value": self.get_month_ablity_randar(month_cache_df, month_str),
                "name": '本月',
            }
        ]

        # 3, 各类环比图
        result["compare"] = self.get_month_ring_map(month_cache_df,
                                                    last_month_start,
                                                    month_str,
                                                    last_month_str)

        # 4. 活着时间
        result["living_time"] = {
            "last_month_data":self.get_month_living_trend(last_day_cache_df),
            "this_month_data": self.get_month_living_trend(day_cache_df)
        }

        # 5. 类别分布矩形图
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
            }
        }

        # 6. TODO 活着时长演变图
        result["living_evolution"] = {
            "counties": ["学习", "工作", "娱乐", "运动", "整理"],
            "timeline": [i for i in range(1, 32)],
            "series": [[[815, 34.05, 351014, "学习", 1], [1314, 39, 645526, "工作", 1], [985, 32, 321675013, "娱乐", 1],
                        [864, 32.2, 345043, "运动", 1], [1244, 36.5731262, 977662, "整理", 1]],
                       [[834, 34.05, 342440, "学习", 2], [1400, 39.01496774, 727603, "工作", 2],
                        [985, 32, 350542958, "娱乐", 2], [970, 33.64, 470176, "运动", 2],
                        [1267, 36.9473378, 1070625, "整理", 2]],
                       [[853, 34.05, 334002, "学习", 3], [1491, 39.02993548, 879432, "工作", 3],
                        [985, 32, 380055273, "娱乐", 3], [1090, 35.04, 607664, "运动", 3],
                        [1290, 37.29122269, 1190807, "整理", 3]],
                       [[1399, 34.05, 348143, "学习", 4], [1651, 39.04490323, 1202146, "工作", 4],
                        [986, 32, 402373519, "娱乐", 4], [1224, 35.74, 772812, "运动", 4],
                        [1360, 36.29644969, 1327905, "整理", 4]],
                       [[2269, 34.05, 434095, "学习", 5], [1922, 40.19012, 1745604, "工作", 5],
                        [986, 32, 411213424, "娱乐", 5], [1374, 36.48, 975565, "运动", 5],
                        [1434, 41.46900965, 1467238, "整理", 5]],
                       [[3267, 34.05, 742619, "学习", 6], [2202, 40.985432, 2487811, "工作", 6],
                        [985, 32, 402711280, "娱乐", 6], [1543, 36.26, 1181650, "运动", 6],
                        [1512, 37.35415172, 1607810, "整理", 6]],
                       [[4795, 34.05, 1256048, "学习", 7], [2406, 41.541504, 3231465, "工作", 7],
                        [1023, 28.85, 380047548, "娱乐", 7], [1733, 36.24, 1324000, "运动", 7],
                        [1594, 38.15099864, 1734254, "整理", 7]],
                       [[5431, 34.05, 1724213, "学习", 8], [2815, 42.460624, 3817167, "工作", 8],
                        [1099, 31.95714286, 363661158, "娱乐", 8], [1946, 29.66, 1424672, "运动", 8],
                        [1897, 45.66140699, 1847468, "整理", 8]]]
        }

        # 7. 工作时段利用率
        result["working_hours_transform_rate"] = {
            "legend": ['全部', '-睡觉', '-杂', '工作+学习', '工作'],
            "value": [
                {"value": 20, "name": '访问'},
                {"value": 10, "name": '咨询'},
                {"value": 5, "name": '订单'},
                {"value": 80, "name": '点击'},
                {"value": 100, "name": '展现'}
            ]
        }

        # 8. 学习时段转换率
        result["learning_hours_transform_rate"] = {
            "legend": ['全部', '-睡觉', '-杂', '工作+学习', '工作'],
            "value": [
                {"value": 20, "name": '访问'},
                {"value": 10, "name": '咨询'},
                {"value": 5, "name": '订单'},
                {"value": 80, "name": '点击'},
                {"value": 100, "name": '展现'}
            ]
        }
        return result

    def calc_yearly_cache(self,cache_task):
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