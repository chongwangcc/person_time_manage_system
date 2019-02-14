#!/usr/bin/python2
# -*- coding: utf-8 -*
from __future__ import print_function
from datetime import datetime
import datetime
import re
from tools import GoogleAuth


def calc_missing_during(list_result):
    """
    计算 遗漏/重叠 时段
    :param list_result:
    :return:
    """
    if list_result is None or len(list_result) < 2:
        return []
    missing_during = []
    last_one = datetime.datetime.strptime(list_result[0][1]+" "+list_result[0][4], '%Y-%m-%d %H:%M:%S')
    for t_time in list_result[1:]:
        s_time = datetime.datetime.strptime(t_time[7] + " " + t_time[3], '%Y-%m-%d %H:%M:%S')
        if (t_time[7] + " " + t_time[3]) in ["2019-01-18 09:15:00"]:
            print()
        if (s_time - last_one).total_seconds() < 60 and (last_one - s_time).total_seconds() < 60:
            pass
        elif s_time < last_one:
            # 重叠
            e_time_str = last_one.strftime("%m-%d %H:%M")
            s_time_str = s_time.strftime("%m-%d %H:%M")
            minute = round((last_one-s_time).total_seconds()/60, 2)
            info = "重叠"
            t_d = {"start_time": s_time_str, "end_time": e_time_str, "during": minute, "type": info}
            missing_during.append(t_d)
        else:
            # 漏掉
            e_time_str = s_time.strftime("%m-%d %H:%M")
            s_time_str = last_one.strftime("%m-%d %H:%M")
            minute = round((s_time - last_one).total_seconds() / 60, 2)
            info = "漏掉"
            t_d = {"start_time": s_time_str, "end_time": e_time_str, "during": minute, "type": info}
            missing_during.append(t_d)

        last_one = datetime.datetime.strptime(t_time[8] + " " + t_time[4], '%Y-%m-%d %H:%M:%S')
        pass
    return missing_during


def standard_content_list(min_time_str, max_time_str, list_result):
    """
    将日历数据标准化，方便下一步计算
    [星期几，类别，开始时间，结束时间]
    :param min_time_str:
    :param max_time_str:
    :param list_result:
    :return:
    """
    type_set=set()
    date_set=set()
    result_list=[]
    for list_one in list_result:
        start_time = list_one[0]
        end_time = list_one[1]
        content = list_one[2]

        start_date_str = start_time[:10]
        org_start_date_str = start_date_str
        start_time_str = start_time[11:19]
        end_data_str = end_time[0:10]
        end_time_str = end_time[11:19]
        if content is None or len(content)==0:
            continue
        type=re.split(u",| |;|，|；|:|：|～", content)[0]
        type_set.add(type)

        date_s = datetime.datetime.strptime(start_date_str+start_time_str, '%Y-%m-%d%H:%M:%S')
        date_e = datetime.datetime.strptime(end_data_str+end_time_str, '%Y-%m-%d%H:%M:%S')

        days_delta_total = (datetime.datetime.strptime(end_data_str,'%Y-%m-%d')\
                           -datetime.datetime.strptime(start_date_str,'%Y-%m-%d')).days

        for day_delta in range(0, days_delta_total+1):
            t_start_datetime = datetime.datetime(year=(date_s + datetime.timedelta(days=day_delta)).year,
                                                 month=(date_s + datetime.timedelta(days=day_delta)).month,
                                                 day=(date_s + datetime.timedelta(days=day_delta)).day,
                                                 hour=0, minute=0, second=0)
            t_end_datetime = datetime.datetime(year=(date_s + datetime.timedelta(days=day_delta+1)).year,
                                                 month=(date_s + datetime.timedelta(days=day_delta+1)).month,
                                                 day=(date_s + datetime.timedelta(days=day_delta+1)).day,
                                                 hour=0, minute=0, second=0)
            if day_delta == 0:
                t_start_datetime = date_s

            if day_delta == days_delta_total:
                t_end_datetime = date_e
            t_start_date_str = datetime.datetime.strftime(t_start_datetime, '%Y-%m-%d')

            if t_start_date_str < min_time_str or t_start_date_str >= max_time_str:
                continue

            #记录在同一天
            date_set.add(t_start_date_str)
            temp_list=[]
            date1=datetime.datetime.strptime(t_start_date_str, '%Y-%m-%d')
            weeknum=date1.weekday() #获得 星期几
            #获得时间差
            delta=t_end_datetime-t_start_datetime
            #保存数据到列表中
            temp_list.append(type)
            temp_list.append(t_start_date_str)
            temp_list.append(weeknum)
            temp_list.append(t_start_datetime.strftime("%H:%M:%S"))
            temp_list.append(t_end_datetime.strftime("%H:%M:%S"))
            temp_list.append(delta)
            temp_list.append(str(delta))
            temp_list.append(t_start_datetime.strftime("%Y-%m-%d"))
            temp_list.append(t_end_datetime.strftime("%Y-%m-%d"))
            # temp_list.append(str(delta + delta))
            #print(repr(temp_list))

            result_list.append(temp_list)

    return result_list, list(type_set),list(date_set)


def gen_sum_list(time_list, type_list, date_list):
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
        sum_all += sum_delta

    temp_list = ["日期汇总"]
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


def sum_list_to_str(sum_list):
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


def get_sum_list(user_name, min_date_str, max_date_str):
    """
    根据日期，生成 时间的统计结果
    :param user_name:
    :param min_date_str:
    :param max_date_str:
    :return:
    """
    naive = datetime.datetime.strptime(min_date_str + " 0:0:0", "%Y-%m-%d %H:%M:%S")
    naive=naive-datetime.timedelta(hours=8)
    time_min = naive.isoformat() + 'Z'
    naive = datetime.datetime.strptime(max_date_str + " 0:0:0", "%Y-%m-%d %H:%M:%S")
    naive=naive-datetime.timedelta(hours=8)
    time_max = naive.isoformat() + 'Z'

    #时间日志列表
    service = GoogleAuth.get_service(user_name)
    calendar_id = GoogleAuth.get_calender_id(service, u"时间日志")
    time_list = GoogleAuth.get_calender_content(service, calendar_id, time_min, time_max)
    time_list, type_list, date_list = standard_content_list(min_date_str, max_date_str, time_list)

    # 计算重叠、遗漏时段
    missing_info = calc_missing_during(time_list)

    #统计时间
    result_list = gen_sum_list(time_list, type_list, date_list)
    return result_list, missing_info


def get_tomato_nums(result_list, label="工作", each_tomato_minutes=30):
    """
    获得 番茄始时钟数
    :param result_list:
    :param each_tomato_minutes:
    :param label:
    :return:
    """
    tomato_nums = 0
    for t_list in result_list:
        m_type = t_list[0]
        m_sum_delta = t_list[-1]
        if m_type == label:
            # 找到了指定的类型
            tomato_nums = round(m_sum_delta.total_seconds()/60/each_tomato_minutes, 2)

    return tomato_nums


def get_nums(result_list, label="工作"):
    """
    获得某类获得 的次数
    :param result_list:
    :param label:
    :return:
    """
    nums = 0
    for t_list in result_list:
        m_type = t_list[0]
        m_sum_delta = t_list[-1]
        if m_type == label:
            # 找到了指定的类型
            for t_time in t_list[1:-1]:
                if (t_time.total_seconds()/60)>1:
                    nums += 1
    return nums


def get_all_category_time_sum(result_list):
    """
    获得每个类别的汇总时间
    :param result_list:
    :return:
    """
    result = []
    for t_list in result_list[1:-1]:
        m_type = t_list[0]
        m_sum_delta = t_list[-1]
        # if m_type == "睡觉":
        #     continue
        t_dict = {"name":m_type, "value":round(m_sum_delta.total_seconds()/60,2)}
        result.append(t_dict)
    return result


def get_every_day_sum_of_category(result_list, label="睡觉"):
    """
    获得某类别，每天的时间
    :param result_list:
    :param label:
    :return:
    """
    result = []
    day_list=result_list[0][1:]
    for t_list in result_list:
        m_type = t_list[0]
        m_sum_delta = t_list[-1]
        if m_type == label:
            # 找到了指定的类型
            # {"category": "星期日", "hours": 8},
            for index, t_time in enumerate(t_list[1:-1]):
                t_dict = {"category": day_list[index], "hours": round(t_time.total_seconds()/3600,2)}
                result.append(t_dict)
    return result


def get_every_day_category_details(result_list, day_padding=7):
    """
    获得所有明细
    :param result_list:
    :param day_padding: 日期不够长时，加长日期
    :return:
    """
    # TODO 按照day_padding 补充日期
    xData = result_list[0][1:-1]
    sum = [round(x.total_seconds()/3600, 2) for x in result_list[-1][1:-1]]
    data = []
    legends = []
    for t_list in result_list[1:-1]:
        legends.append( t_list[0])

    every_day_sum=[]
    for t_list in result_list[1:-1]:
        every_day_sum.append([round(t.total_seconds()/3600,2) for t in t_list[1:-1]])

    result = {
        "xData": xData,
        "legends": legends,
        # 每个类别，每一天的时间，shape==（lengends.长度  *  xData.长度）
        "data": every_day_sum,
        "sum": sum
    }

    return result


if __name__ == "__main__":
    result_list, missing_info = get_sum_list("mm", "2019-01-13", "2019-01-19")




