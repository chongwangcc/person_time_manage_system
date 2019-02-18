#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/22 7:19 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : DateTools.py 
# @Software: PyCharm

from datetime import datetime, timedelta
import calendar


def calc_week_begin_end_date(date_str):
    """
    计算某天的所在星期的 周一、周日的日期
    :param date_str: 格式例如 2019-01-01
    :return:
    """
    m_date = datetime.strptime(date_str, '%Y-%m-%d')
    week = (m_date.weekday()+1) % 7
    minDate = m_date + timedelta(days=- week)
    maxDate = m_date + timedelta(days=6 - week)
    monday = minDate.strftime('%Y-%m-%d')
    sunday = maxDate.strftime('%Y-%m-%d')
    return monday, sunday


def calc_month_begin_end_date(date_str):
    """
    计算某天所在月份的第一天，最后一天的日期
    :param date_str:
    :return:
    """
    minDate = date_str[:7]+"-01"
    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, lastday = calendar.monthrange(int(date_str[:4]), int(date_str[5:7]))
    maxDate = date_str[:7]+"-"+str(lastday)
    return minDate, maxDate


def calc_month_total_days(date_str):
    """
    计算所在月份的天数
    :param date_str:
    :return:
    """
    _,lastDate = calc_month_begin_end_date(date_str)
    nums = int(lastDate[-2:])
    return nums


def calc_last_month_begin_end_date(date_str):
    """
    获得上月份的开始结束日期
    :param date_str:
    :return:
    """
    m_date = datetime.strptime(date_str, '%Y-%m-%d')
    first = m_date.replace(day=1)
    lastMonth = first - timedelta(days=1)
    last_month_str = lastMonth.strftime('%Y-%m-%d')
    return calc_month_begin_end_date(last_month_str)


def calc_year_begin_end_date(date_str):
    minxDate = date_str[:4]+"-01-01"
    maxDate = date_str[:4]+"-12-31"
    return minxDate,maxDate


def calc_next_date(date_str):
    """
    计算明天的日期
    :param date_str:
    :return:
    """
    m_date = datetime.strptime(date_str, '%Y-%m-%d')
    tomorrow = m_date + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')
    return tomorrow_str


def calc_delta_seconds(date_start, date_end):
    """
    计算两个字符串的时间差, date_end-date_start, 精确到多少秒
    :param date_start: 格式例如 2019-01-01 05:05:05
    :param date_end:格式例如 2019-01-01 05:05:05
    :return:
    """
    d_1 = datetime.strptime(date_end, '%Y-%m-%d %H:%M:%S')
    d_2 = datetime.strptime(date_start, '%Y-%m-%d %H:%M:%S')
    total_seconds = (d_1-d_2).total_seconds()
    return int(total_seconds)


def calc_deta_days(date_start, date_end):
    """

    :param date1: 格式例如 2019-01-01
    :param date2: 格式例如 2019-01-01
    :return: 相等返回0， 不相等返回整数
    """
    days_delta_total = (datetime.strptime(date_end, '%Y-%m-%d') \
                        - datetime.strptime(date_start, '%Y-%m-%d')).days
    return days_delta_total


def calc_same_days_delta(date_start, time_start,end_date_str,  time_end):
    """
    计算同一天的时间计算值，返回：
    [ 日期字符串, 星期几，开始时间，结束时间, 持续分钟数]
    :param date_start:
    :param time_start:
    :param time_end:
    :return:
    """
    weeknum = calc_week_num(date_start)
    during = calc_delta_seconds(date_start + " " + time_start,
                                end_date_str + " " + time_end)
    during = round(during/60)
    if during <= 0:
        return None

    return [ date_start, weeknum, time_start, time_end, during]


def calc_week_num(date_str):
    """
    计算日期字符串 是星期几
    :param date_str: 格式例如 2019-01-01
    :return: 0,1,2,3,4,5,6 ， 星期一返回0，....，星期日返回6

    """
    weeknum = datetime.strptime(date_str, '%Y-%m-%d').weekday()
    return weeknum


def gen_day_list_between(date1, date2):
    """
    返回两个日期中的每天日期，包含前后两个日期
    :param date1: 格式例如 2019-01-01
    :param date2: 格式例如 2019-01-02
    :return: ["2019-01-01", "2019-01-02"]
    """

    def gen_dates(b_date, days):
        day = timedelta(days=1)
        for i in range(days):
            yield b_date + day * i

    start =  datetime.strptime(date1, '%Y-%m-%d')
    end = datetime.strptime(date2, '%Y-%m-%d')

    date_list = []
    for d in gen_dates(start, (end - start).days+1):
        date_list.append(d.strftime('%Y-%m-%d'))
    return date_list


def gen_week_list_in_days(date_list):
    """
    计算一串日期中，包含的周日期
    :param date_list: ["2019-01-01", "2019-01-03","2019-01-03",]
    :return: 周的起始日期 ["2019-01-01"]
    """
    r_weekly = set()
    for t_day in date_list:
        t_dd = calc_week_begin_end_date(t_day)
        r_weekly.add(t_dd)
    l_result = list(r_weekly)
    l_result.sort()
    # l_result = [t[0] for t in l_result]
    return l_result


def gen_month_list_in_days(date_list):
    """
    计算一串日期中，包含的月份列表
    :param date_list:  ["2019-01-01", "2019-01-03","2019-01-03",]
    :return: 月份 ["2019-01"]
    """
    l_result = [t[:7] for t in date_list]
    l_result = list(set(l_result))
    l_result.sort()
    return l_result


def gen_year_list_in_days(date_list):
    """
    计算一串日期中，包含的年份列表
    :param date_list: ["2019-01-01", "2019-01-03","2019-01-03",]
    :return: 年份 ["2019-01"]
    """
    l_result = [t[:4] for t in date_list]
    l_result = list(set(l_result))
    l_result.sort()
    return l_result


def calc_intersection_minutes(start_time1, end_time1, start_time2, end_time2):
    """
    计算两个时间段交集的分钟数，不想交返回0
    :param start_time1:
    :param end_time1:
    :param start_time2:
    :param end_time2:
    :return:
    """
    min_time_str = None
    max_time_str = None
    minutes = 0

    if start_time2 >= start_time1 and start_time2 <= end_time1:
        # 相交
        min_time_str = start_time2
        max_time_str = min(end_time1, end_time2)
    if start_time1 >= start_time2 and start_time1 <= end_time2:
        # 相交
        min_time_str = max(start_time1,start_time2)
        max_time_str = start_time1
    if min_time_str is not None:
        time_min = datetime.strptime(min_time_str, '%H:%M:%S')
        time_max = datetime.strptime(max_time_str, '%H:%M:%S')
        minutes = (time_max - time_min).total_seconds()/60
    return minutes





if __name__ == "__main__":
    # dd = gen_week_list_in_days( ["2019-01-01", "2019-01-03","2019-01-03"])
    # print(dd)
    # dd = gen_month_list_in_days(["2019-01-01", "2019-01-03", "2019-01-03"])
    # print(dd)
    # dd = gen_year_list_in_days(["2019-01-01", "2019-01-03", "2019-01-03"])
    # print(dd)
    dd = calc_week_num("2019-02-19")
    print(dd)




