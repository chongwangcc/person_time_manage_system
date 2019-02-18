#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/2/15 15:27 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : CacheTools.py 
# @Software: PyCharm

from datetime import datetime, date

import DateTools
import SqlTools


class WeeklyCacheCalcService:
    """
    计算每周 web缓存 需要 工具类
    """
    def __init__(self, user_id, monday_str, sunday_str):
        """
        注意：用调用者决定monday_str,sunday_str的范围，必须是7天内
        :param user_id:
        :param monday_str:
        :param sunday_str:
        """
        self.first_day_str = monday_str
        self.last_day_str = sunday_str
        self.user_id = user_id
        self.day_statics_df = None
        self.day_details_df = None
        self.week_statics_df = None
        self.week_cache = {}

    def load_day_details(self, is_force=False):

        if self.day_statics_df is None or is_force:
            self.day_statics_df = SqlTools.get_everyday_cache_df(self.user_id,
                                                        self.first_day_str,
                                                        self.last_day_str)
            #  按照周聚合，保存 按周聚合的结果
            group_week = self.day_statics_df.groupby(by=["user_id", "week_start_str", "week_end_str", "category"])
            during_sum_df = group_week.sum().reset_index()
            description_df = group_week["word_cloud"].aggregate(lambda x: ",".join(x)).reset_index()
            df_final = during_sum_df
            df_final["word_cloud"] = description_df["word_cloud"]
            # 保存 按周聚合的结果
            self.week_statics_df = df_final
            # print(self.week_statics_df)

        if self.day_details_df is None or is_force:
            self.day_details_df = SqlTools.get_time_details_df(self.user_id,
                                                        self.first_day_str,
                                                        self.last_day_str)
            # print(self.day_details_df)

    def calc_missing_during(self):
        """
        计算重叠时段
        :param everyday_details_df:
        :return:
        """
        missing_during = []
        # 1. 检查有没有判断的必要
        if self.day_details_df is None:
            self.week_cache["missing_info"] = missing_during
        df_sort = self.day_details_df.sort_values(by=["date_str", "start_time"])
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
        self.week_cache["missing_info"] = missing_during

    def calc_basis_nums(self):
        """
        计算各种基本的统计数据
        :return:
        """
        self.week_cache["start_date"] = self.first_day_str
        self.week_cache["end_date"] = self.last_day_str
        self.week_cache["each_category_time_sum"] = []
        self.week_cache["execise_nums"] = 0
        self.week_cache["fun_nums"] = 0
        self.week_cache["working_tomato_nums"] = 0
        self.week_cache["study_tomato_nums"] = 0
        for index, rows in self.week_statics_df.iterrows():
            if rows["category"] in ["学习"]:
                t_tomato_nums = round(rows["during"]/30, 2)
                self.week_cache["study_tomato_nums"] = t_tomato_nums
            elif rows["category"] in ["工作"]:
                t_tomato_nums = round(rows["during"] / 30, 2)
                self.week_cache["working_tomato_nums"] = t_tomato_nums
            elif rows["category"] in ["运动"]:
                self.week_cache["execise_nums"] = rows["nums"]
            elif rows["category"] in ["娱乐"]:
                self.week_cache["fun_nums"] = rows["nums"]
            # 5. 类别 时间汇总
            t_dict = {"name": rows["category"], "value": round(rows["during"], 2)}
            self.week_cache["each_category_time_sum"].append(t_dict)

        # 2. 番茄时钟达标率
            self.week_cache["working_and_study_tomato_nums_of_each_day"] = \
                self.week_cache["working_tomato_nums"] + self.week_cache["study_tomato_nums"]

    def calc_sleep_trends(self):
        """
        计算睡眠时间走势图
        :return:
        """
        df_t = self.day_statics_df[self.day_statics_df["category"] == "睡觉"]
        sleep_hours = []
        for index, row in df_t.iterrows():
            t_dict = {"category": row["date_str"], "hours": round(row["during"] / 60, 2)}
            sleep_hours.append(t_dict)
        self.week_cache["sleep_hours"] = {
            "standard_hours": 8,
            "actual_hours": sleep_hours
        }

    def calc_everyday_category_details(self, day_padding=7):
        """
        获得所有明细
        :param everday_df:
        :param day_padding: 日期不够长时，加长日期
        :return:
        """
        everday_df = self.day_statics_df

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
        self.week_cache["every_day_category_details"] = result

    def get_cache_result(self):
        """
        获得每周缓存的结果
        :return:
        """
        # 1. 加载 本周 的每天统计数据
        self.load_day_details()

        # 2. 计算需要的缓存数据
        self.calc_basis_nums()
        self.calc_sleep_trends()
        self.calc_everyday_category_details()

        # 3.返回结果
        return self.week_cache


class MonthlyCacheCalcSerive:
    """
    计算每月 cache 缓存 需要 的工具类
    """
    working_period_dict = {
        ("05:00:00", "08:00:00"): [0,1,2,3,4,5,6,7],
        ("09:00:00", "12:00:00"): [0,1,2,3,4,7],
        ("13:00:00", "18:00:00"): [0,1,2,3,4,7],
    }
    @staticmethod
    def _high_efficient_period_minues(weeknums, start_time, end_time):
        """
        计算时间和高效时段的交集
        :param weeknums:
        :param start_time:
        :param end_time:
        :return:
        """
        total_minutes = 0
        for t_times, t_weeknums in MonthlyCacheCalcSerive.working_period_dict.items():
            if weeknums in t_weeknums:
                total_minutes += DateTools.calc_intersection_minutes(t_times[0],
                                                                     t_times[1],
                                                                     start_time,
                                                                     end_time)
        return total_minutes

    def __init__(self, user_id, month_str):
        self.user_id = user_id
        self.month_str = month_str
        t_date_str = month_str+"-01"
        # 1.计算本月的第一天、最后一天日期
        self.first_day_str, self.last_day_str = DateTools.calc_month_begin_end_date(t_date_str)

        # 4. 一些数据结构
        self.day_statics_df = None
        self.day_details_df = None
        self.month_statics_df = None
        self.month_cache = {}

    def load_day_details(self, is_force=False):
        """
        从数据库中加载需要的
        :param is_force:
        :return:
        """
        if self.day_statics_df is None or is_force:
            self.day_statics_df = SqlTools.get_everyday_cache_df(self.user_id,
                                                        self.first_day_str,
                                                        self.last_day_str)
            #  按照月聚合，保存 按周月聚合的结果
            self.day_statics_df["month_str"] = self.day_statics_df["date_str"].map(lambda x: x[:7])
            group_month = self.day_statics_df.groupby(by=["user_id", "month_str", "category"])
            during_sum_df = group_month.sum().reset_index()
            description_df = group_month["word_cloud"].aggregate(lambda x: ",".join(x)).reset_index()
            df_final = during_sum_df
            df_final["word_cloud"] = description_df["word_cloud"]
            # 保存 按月聚合的结果
            self.month_statics_df = df_final

        if self.day_details_df is None or is_force:
            self.day_details_df = SqlTools.get_time_details_df(self.user_id,
                                                        self.first_day_str,
                                                        self.last_day_str)

    def get_month_category_minutes(self, category):
        """
        获得 每月缓存中，某类型的 持续时间,单位分钟
        :param month_df:
        :param category:
        :return:
        """
        during = 0
        month_df = self.month_statics_df
        if month_df is None or category is None or month_df.empty:
            return during
        t_df = month_df[(month_df["month_str"] == self.month_str) & (month_df["category"] == category)]
        if len(t_df) == 1:
            during = t_df["during"].tolist()[0]
        return during

    def get_month_category_nums(self, category):
        """
        获得 每月缓存中，某类型的 持续时间,单位分钟
        :param month_df:
        :param category:
        :return:
        """
        during = 0
        month_df = self.month_statics_df
        if month_df is None or category is None or month_df.empty:
            return during
        t_df = month_df[(month_df["month_str"] == self.month_str) & (month_df["category"] == category)]
        if len(t_df) == 1:
            during = t_df["nums"].tolist()[0]
        return during

    def calc_month_pass_percent(self):
        """
        计算每月过了多久了
        :param start_date_str:
        :return:
        """
        during_percent = 0
        today_str = date.today().strftime('%Y-%m-%d')
        if today_str[:7] == self.first_day_str[:7]:
            minDate, maxDate = self.first_day_str,self.last_day_str
            now_int = int(today_str[-2:])
            all_int = int(maxDate[-2:])
            during_percent = round(now_int/all_int, 2)
        elif today_str[:7] < self.first_day_str[:7]:
            during_percent = 0
        else:
            during_percent = 1
        self.pass_percent = during_percent
        return during_percent

    def calc_month_living_percent(self):
        """
        计算活着时间的总数：活着时间定义---除去睡觉和杂的时间
        :param month_cache_df:
        :return:
        """
        month_cache_df = self.month_statics_df
        total_minuts = month_cache_df["during"].sum()
        living_df = month_cache_df[(month_cache_df["category"] != "睡觉") & (month_cache_df["category"] != "杂")]
        living_minuts = living_df["during"].sum()
        return round(living_minuts/total_minuts, 2)

    def calc_basis_nums(self):
        """
        计算一些基本的统计数据
        :return:
        """
        self.month_cache["start_date"] = self.first_day_str
        self.month_cache["end_date"] = self.last_day_str
        self.month_cache["working_tomato_nums"] = round(self.get_month_category_minutes("工作")/30, 2)
        self.month_cache["study_tomato_nums"] = round(self.get_month_category_minutes("学习") / 30, 2)
        self.month_cache["during_percent"] = "%.0f%%" % (self.calc_month_pass_percent()*100)
        self.month_cache["living_percent"] = "%.0f%%" % (self.calc_month_living_percent()*100)

    def calc_words_cloud(self):
        """
        计算 词云图频率
        :return:
        """
        month_cache_df = self.month_statics_df
        # 1.所有描述合并到一个字符串上
        description = ""
        words_series = month_cache_df["word_cloud"]
        for index, value in words_series.iteritems():
            description += ","
            description += value

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
        self.month_cache["word_cloud"] = words

    def calc_ability_radar(self):
        """
        计算各项能力的雷达图
        :return:
        """
        month_str = self.month_str
        month_pass = self.calc_month_pass_percent()
        month_total_days = DateTools.calc_month_total_days(month_str + "-01")
        # 1.工作力 得分计算规则
        work_minutes = self.get_month_category_minutes("工作")
        work_minutes /= 60
        stand_work_hours = 40 * month_pass * month_total_days * 1/ 7
        work_score = round(work_minutes / stand_work_hours * 10, 0)
        if work_score > 10:
            work_score = 10

        # 2. 学习力 得分计算规则
        study_minutes = self.get_month_category_minutes("学习")
        stand_study_hours = (3 + 8 / 7) * month_total_days * month_pass
        study_score = round(study_minutes / 60 / stand_study_hours * 10, 0)
        if study_score > 10:
            study_score = 10

        # 3. 娱乐力 得分计算规则
        fun_num = self.get_month_category_nums("娱乐")
        stand_fun_nums = 1 / 3 * month_pass * month_total_days
        fun_score = round(fun_num / stand_fun_nums, 0)
        if fun_score > 10:
            fun_score = 10

        # 4. 运动力 得分计算规则
        workoutnum = self.get_month_category_minutes("运动")
        stand_workout_nums = int(5 / 7 * month_total_days * month_pass)
        workout_score = round(workoutnum / stand_workout_nums, 0)
        if workout_score > 10:
            workout_score = 10

        # 5. 睡眠力 得分计算规则
        sleep_minutes = self.get_month_category_minutes("睡觉")
        sleep_minutes /= 60
        stand_sleep_hours = 8 * month_pass * month_total_days
        stand_sleep_hours /= month_total_days
        sleep_score = abs(10-abs(8-round((sleep_minutes - stand_sleep_hours), 2)))
        if sleep_score > 10:
            sleep_score = 10
        # result = [0, 0, 0, 0, 0, 0]  # ？？？、睡眠力、工作力、娱乐力、运动力、学习力
        result = [sleep_score, work_score, fun_score, workout_score, study_score]
        self.month_cache["ability_redar"] = [
            {
                "value": result,
                "name": month_str
            }
        ]

    def calc_living_trends(self):
        """
        计算 活着时间走势 图
        活着定义：除去[睡觉，杂]的时间
        :return:
        """
        living_df = self.day_statics_df[(self.day_statics_df["category"] != "睡觉")
                                        & (self.day_statics_df["category"] != "杂")]
        living_df = living_df.sort_values(by=['date_str'])

        living_hours = []
        for index, row in living_df.iterrows():
            t_dict = {"category": row["date_str"], "hours": round(row["during"] / 60, 2)}
            living_hours.append(t_dict)
        self.month_cache["living_time"] = {
            "standard_hours": 12,
            "actual_hours": living_hours
        }

    def calc_using_rate(self):
        """
        TODO 计算学习-工作时段的利用率
        工作时段定义：周一到周五，上午9:00--12:00， 下午 13:00--18:00
        学习时段定义：每天，早上 5:00--8:00,和 周日：9:00-12:00，13:00--18:00
        被利用定义：类别属于-- 学习 或 工作
        :return:
        """
        working_df = self.day_details_df[(self.day_details_df["category"] == "学习")
                                        |(self.day_details_df["category"] == "工作")]
        working_df["effiect_minutes"] = working_df.apply(lambda row:
                                                         MonthlyCacheCalcSerive._high_efficient_period_minues(
                                                             row["week_nums"],
                                                             row["start_time"],
                                                             row["end_time"]
                                                         ), axis=1)
        t_df_sum = working_df.groupby(["date_str","week_nums"])["effiect_minutes"].sum().reset_index()


        t_df_sum["using_rate"] = t_df_sum.apply(axis = 1,func = (lambda row : round(row["effiect_minutes"] /3, 2)
                                                                                if row["week_nums"]==5
                                                                                else round(row["effiect_minutes"]/11,2)
                                                                 )
                                                )
        using_rate = [0 for i in range(31)]
        for index, row in t_df_sum.iterrows():
            days = row["date_str"][-2:]
            using_rate[int(days)-1] = row["using_rate"]
        self.month_cache["efficient_period_using_rate"] = {
            "name":self.month_str,
            "data":using_rate
        }

    def get_cache_result(self):
        # 1. 加载 本月 的每天统计数据
        self.load_day_details()
        if self.month_statics_df is None or self.month_statics_df.empty:
            return {}

        # 2. 计算需要的缓存数据
        self.calc_basis_nums()
        self.calc_words_cloud()
        self.calc_ability_radar()
        self.calc_living_trends()
        self.calc_using_rate()

        # 3.返回结果
        return self.month_cache


class YearlyCacheCalcService:
    """
    TODO 计算每年 cache 缓存需要的 工具类
    """
    def __init__(self, user_id, year_str):
        """

        :param user_id:
        :param year_str:
        """
        self.user_id = user_id
        self.year_str = year_str
        self.first_day_str, self.last_day_str = DateTools.calc_year_begin_end_date(year_str+"-01-01")
        # 4. 一些数据结构
        self.day_statics_df = None
        self.day_details_df = None
        self.year_statics_df = None
        self.year_cache = {}

    def load_day_details(self):
        """
        加载dataframe
        :return:
        """

    def calc_basic_nums(self):
        """
        计算一些基本数据
        :return:
        """

    def calc_words_cloud(self):
        """
        计算词云
        :return:
        """

    def calc_weekly_time_trends(self):
        """
        计算每周的时间走势
        :return:
        """

    def calc_rect(self):
        """
        计算矩形图
        :return:
        """

    def get_cache_result(self):
        """

        :return:
        """
        # 1. 加载 本月 的每天统计数据
        self.load_day_details()

        # 2. 计算需要的缓存数据
        self.calc_basic_nums()
        self.calc_words_cloud()
        self.calc_weekly_time_trends()
        self.calc_rect()

        # 3.返回结果
        return self.year_cache
