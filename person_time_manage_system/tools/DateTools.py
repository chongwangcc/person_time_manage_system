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
    :param date_str:
    :return:
    """
    m_date = datetime.strptime(date_str, '%Y-%m-%d')
    week = m_date.weekday()
    minDate = m_date + timedelta(days=(-1 - week))
    maxDate = m_date + timedelta(days=(6 - week))
    monday = minDate.strftime('%Y-%m-%d')
    sunday = maxDate.strftime('%Y-%m-%d')
    return monday, sunday
