#!/usr/bin/python2
# -*- coding: utf-8 -*
from __future__ import print_function
from datetime import datetime
import datetime
import re
from tools import GoogleAuth


def _calc_record(start_date_str, start_time_str, end_data_str, end_time_str, content):
    pass


def standard_content_list(time_min_str,time_max_str,list_result):
    """
    将日历数据标准化，方便下一步计算
    [星期几，类别，开始时间，结束时间]
    :param list_result:
    :return:
    """
    type_set=set()
    date_set=set()
    result_list=[]
    for list_one in list_result:
        start_time=list_one[0]
        end_time=list_one[1]
        content=list_one[2]

        start_date_str=start_time[:10]
        start_time_str=start_time[11:19]
        end_data_str=end_time[0:10]
        end_time_str=end_time[11:19]

        type=re.split(u",| |;|，|；|:|：|～",content)[0]
        type_set.add(type)

        date_s = datetime.datetime.strptime(start_date_str+start_time_str, '%Y-%m-%d%H:%M:%S')
        date_e = datetime.datetime.strptime(end_data_str+end_time_str, '%Y-%m-%d%H:%M:%S')

        days_delta_total = (datetime.datetime.strptime(end_data_str,'%Y-%m-%d')\
                           -datetime.datetime.strptime(start_date_str,'%Y-%m-%d')).days

        for day_delta in range(0,days_delta_total+1):
            t_start_datetime = datetime.datetime(year=(date_s + datetime.timedelta(days=day_delta)).year,
                                                 month=(date_s + datetime.timedelta(days=day_delta)).month,
                                                 day=(date_s + datetime.timedelta(days=day_delta)).day,
                                                 hour=0, minute=0, second=0)
            t_end_datetime = datetime.datetime(year=(date_s + datetime.timedelta(days=day_delta+1)).year,
                                                 month=(date_s + datetime.timedelta(days=day_delta+1)).month,
                                                 day=(date_s + datetime.timedelta(days=day_delta+1)).day,
                                                 hour=0, minute=0, second=0)
            if day_delta == 0 :
                t_start_datetime = date_s

            if day_delta == days_delta_total:
                t_end_datetime = date_e
            start_date_str = datetime.datetime.strftime(t_start_datetime,'%Y-%m-%d')

            if start_date_str < time_min_str or start_date_str >= time_max_str:
                continue

            #记录在同一天
            date_set.add(start_date_str)
            temp_list=[]
            date1=datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            weeknum=date1.weekday() #获得 星期几
            #获得时间差
            delta=t_end_datetime-t_start_datetime
            #保存数据到列表中
            temp_list.append(type)
            temp_list.append(start_date_str)
            temp_list.append(weeknum)
            temp_list.append(start_time_str)
            temp_list.append(end_time_str)
            temp_list.append(delta)
            temp_list.append(str(delta))
            temp_list.append(str(delta + delta))
            #print(repr(temp_list))

            result_list.append(temp_list)

    return result_list,list(type_set),list(date_set)

def gen_sum_list(time_list,type_list,date_list):
    """
    统计时间打印输出
    :param time_list:
    :param type_list:
    :param date_list:
    :return:
    """
    dict_temp={}
    type_list.sort()
    date_list.sort()
    for time_unit in time_list:
        type=time_unit[0]
        date=time_unit[1]
        week=time_unit[2]
        delta=time_unit[5]
        last_delta=dict_temp.get((type,date))
        if last_delta is None:
            dict_temp[(type,date)]=delta
        else:
            dict_temp[(type,date)]=last_delta+delta

    #生成统计列表
    sum_all=datetime.timedelta()
    result_list=[]
    temp_list=[" "]
    temp_list.extend([str1 for str1 in date_list])
    temp_list.append("类别汇总")
    result_list.append(temp_list)
    for type in type_list:
        temp_list=[]
        temp_list.append(type)
        sum_delta=datetime.timedelta()
        for date in date_list:
            delta=dict_temp.get((type,date))
            if delta:
                sum_delta+=delta
            else:
                delta=datetime.timedelta()
            temp_list.append(delta)
        temp_list.append(sum_delta)
        result_list.append(temp_list)
        sum_all+=sum_delta

    temp_list=["日期汇总"]
    for date in date_list:
        sum_delta=datetime.timedelta()
        for type in type_list:
            delta=dict_temp.get((type,date))
            if delta:
                sum_delta+=delta
            else:
                delta=datetime.timedelta()
            pass
        temp_list.append(sum_delta)
    temp_list.append(sum_all)
    result_list.append(temp_list)
    return result_list

def sumListToStr(sum_list):
    """
    将统计列表转换为字符串
    :param sum_list:
    :return:
    """
    for i in range(0,len(sum_list)):
        for j in range(0,len(sum_list[i])):
            if isinstance(sum_list[i][j],datetime.datetime):
                sum_list[i][j]=str(sum_list[i][j])[:-3]
    return sum_list

def getSumList(user_name,time_min_str,time_max_str):
    """
    根据日期，生成 时间的统计结果
    :param time_min_str:
    :param time_max_str:
    :return:
    """
    naive = datetime.datetime.strptime(time_min_str+" 0:0:0", "%Y-%m-%d %H:%M:%S")
    naive=naive-datetime.timedelta(hours=8)
    time_min = naive.isoformat() + 'Z'
    naive = datetime.datetime.strptime(time_max_str+" 0:0:0", "%Y-%m-%d %H:%M:%S")
    naive=naive-datetime.timedelta(hours=8)
    time_max = naive.isoformat() + 'Z'

    #时间日志列表
    service = GoogleAuth.get_service(user_name)
    calendar_id = GoogleAuth.get_calender_ID(service,u"时间日志")
    time_list=GoogleAuth.get_calender_content(service,calendar_id,time_min,time_max)
    time_list,type_list,date_list=standard_content_list(time_min_str,time_max_str,time_list)

    #统计时间
    result_list=gen_sum_list(time_list,type_list,date_list)
    return result_list,type_list,date_list


def print_test():
    print("import testsuccess")

def main():
    #生成要获得数据的时间
    result_list, type_list, date_list = getSumList("2018-11-18","2018-11-25")
    print(result_list)
    pass


if __name__ == '__main__':
    main()
