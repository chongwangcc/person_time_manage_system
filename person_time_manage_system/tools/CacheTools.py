#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/2/15 15:27 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : CacheTools.py 
# @Software: PyCharm
import DateTools


class WeeklyCacheCalcService:
    """
    计算每周 web缓存 需要 工具类
    """

    def __init__(self, user_id, monday_str, sunday_str):
        self.monday_str = monday_str
        self.sunday_str = sunday_str
        self.user_id = user_id

    def get_cache_result(self):
        """
        获得每周缓存的结果
        :return:
        """


class MonthlyCacheCalcSerive:
    """
    计算每月 cache 缓存 需要 的工具类
    """
    def __init__(self, user_id, month_str):
        self.user_id = user_id
        self.first_month_day_str, self.last_month_day_str = DateTools.calc_month_begin_end_date(month_str+"-01")


class YearlyCacheCalcService:
    """
    计算每年 cache 缓存需要的 工具类
    """