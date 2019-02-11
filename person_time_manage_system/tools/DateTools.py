#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/22 7:19 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : DateTools.py 
# @Software: PyCharm

from datetime import datetime, timedelta


def calc_week_begin_end_date(date_str):
    """
    计算某天的周一、周六的日期
    :param date_str: 格式例如 2019-01-01
    :return:
    """
    m_date = datetime.strptime(date_str, '%Y-%m-%d')
    week = m_date.weekday()
    minDate = m_date + timedelta(days=(-1 - week))
    maxDate = m_date + timedelta(days=(6 - week))
    monday = minDate.strftime('%Y-%m-%d')
    sunday = maxDate.strftime('%Y-%m-%d')
    return monday, sunday


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
    weeknum = cacl_week_num(date_start)
    during = calc_delta_seconds(date_start + " " + time_start,
                                end_date_str + " " + time_end)
    during = round(during/60)
    if during <= 0:
        return None

    return [ date_start, weeknum, time_start, time_end, during]


def cacl_week_num(date_str):
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


if __name__ == "__main__":
    dd = gen_day_list_between("2019-01-01", "2019-01-02")
    print(dd)




