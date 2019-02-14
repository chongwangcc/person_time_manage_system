#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/30 15:05 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : CalenderTools.py 
# @Software: PyCharm
from datetime import datetime, timedelta, time
from SqlTools import *
import re
import DateTools


class CalenderServer:

    @staticmethod
    def format_date_str_for_calender_server(date_str, service="google"):
        """
        将日期字符串，格式化 日历服务需要的字符串格式
        :param date_str:
        :return:
        """
        if service in ["google"]:
            naive = datetime.strptime(date_str + " 0:0:0", "%Y-%m-%d %H:%M:%S")
            naive = naive-timedelta(hours=8)
            time_min = naive.isoformat() + 'Z'
            return time_min
        else:
            return None

    @staticmethod
    def standard_content_list(user_id, list_result):
        """
        将日历数据标准化，方便下一步计算
        [user_id, 类别, 描述字符串, date_str, 星期几，开始时间，结束时间, 持续分钟数]
        :param user_id:
        :param list_result: [['2019-01-01T00:00:00+08:00', '2019-01-01T05:30:00+08:00', '睡觉'], ...]
        :return:
        """
        result = []
        for list_one in list_result:
            start_date_str = list_one[0][:10]    # 开始日期，例如 2019-01-01
            start_time_str = list_one[0][11:19]  # 开始时间， 例如 05:30:00
            end_date_str = list_one[1][:10]      # 结束日期， 例如 2019-01-01
            end_time_str = list_one[1][11:19]    # 结束日期， 例如 06:00:00

            # 检查 标题是否为空
            ss = re.split(u",| |;|，|；|:|：|～", list_one[2])
            if ss is None or len(ss) == 0:
                continue

            category = ss[0]                   # 类别
            description = "".join(ss[1:])     # 描述

            if start_date_str == end_date_str:
                # 记录没有跨天，在同一天
                t_time = DateTools.calc_same_days_delta(start_date_str, start_time_str, end_date_str, end_time_str)
                if t_time is None or len(t_time) == 0:
                    continue
                app_list = [user_id,category,description]
                app_list.extend(t_time)
                result.append(app_list)
            else:
                #  记录跨天，要拆分
                t_date_list = DateTools.gen_day_list_between(start_date_str, end_date_str)
                t_date_list.append(t_date_list[-1])
                if len(t_date_list) < 2:
                    continue
                t_start_time = ["00:00:00" for i in range(len(t_date_list))]
                t_end_time = ["23:59:59" for i in range(len(t_date_list))]
                t_start_time[0] = start_time_str
                t_end_time[-2] = end_time_str
                for i in range(len(t_date_list)-1):
                    t_time = DateTools.calc_same_days_delta(t_date_list[i], t_start_time[i], t_date_list[i], t_end_time[i])
                    if t_time is None:
                        continue
                    app_list = [user_id, category, description]
                    app_list.extend(t_time)
                    result.append(app_list)
        return result

    @staticmethod
    def calc_missing_during(list_result, start_date_str, end_date_str):
        """
        计算 遗漏/重叠 时段, 筛选不在指定日期范围内的结果
        :param list_result: standard_content_list()函数返回的结果格式
        :return:
        """
        missing_during = []
        valid_result_list = []

        # 1. 判断日期是不是在指定范围内
        for t_time in list_result:
            t_date_str = t_time[3]
            if t_date_str < start_date_str or t_date_str > end_date_str:
                continue
            valid_result_list.append(t_time)
        if len(valid_result_list) <= 1:
            return valid_result_list, missing_during

        # 2. 判断有没有漏掉/重叠的时段
        last_one = datetime.strptime(valid_result_list[0][3] + " " + valid_result_list[0][6], '%Y-%m-%d %H:%M:%S')
        for t_time in valid_result_list[1:]:
            s_time = datetime.strptime(t_time[3] + " " + t_time[5], '%Y-%m-%d %H:%M:%S')
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
            else:
                # 漏掉
                e_time_str = s_time.strftime("%m-%d %H:%M")
                s_time_str = last_one.strftime("%m-%d %H:%M")
                minute = round((s_time - last_one).total_seconds() / 60, 2)
                info = "漏掉"
                t_d = {"start_time": s_time_str, "end_time": e_time_str, "during": minute, "type": info}
                missing_during.append(t_d)
            last_one = datetime.strptime(t_time[3] + " " + t_time[6], '%Y-%m-%d %H:%M:%S')
        return valid_result_list, missing_during

    def get_time_details(self, userinfo, start_date, end_date):
        """
        获得时间的明细，包含开始日期，不包含结束日期
        :param userinfo: 用户信息
        :param start_date:  开始日期
        :param end_date:  结束日期
        :return:
        """
        if userinfo is None:
            return None

        if userinfo.calender_server in ["google"]:
            from tools import GoogleAuth
            import httplib2
            # 1.准备参数
            time_min = self.format_date_str_for_calender_server(start_date, "google")
            time_max = self.format_date_str_for_calender_server(end_date, "google")
            # TODO 网络代理，写到配置文件中
            proxy = httplib2.ProxyInfo( httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1080)
            # 2. 创建 日历 服务
            service = GoogleAuth.get_service(userinfo.user_name,
                                             userinfo.auth_token_file,
                                             proxy=proxy)
            calendar_id = GoogleAuth.get_calender_id(service, userinfo.calender_name)

            # 3. 连接日历 获得结果
            time_list = GoogleAuth.get_calender_content(service, calendar_id, time_min, time_max)

            # 4. 格式化字符串
            time_list_format = self.standard_content_list(userinfo.id, time_list)

            # 5. 过滤筛选 结果，日期不在指定范围内的不要
            final_result, missing_during = self.calc_missing_during(time_list_format, start_date, end_date)
            return final_result, missing_during
        else:
            print("calender server ["+userinfo.calender_server+"] not support yet" )


if __name__ == "__main__":
    user_info = fetch_user_info("cc")
    calender_server = CalenderServer()
    calender_server.get_time_details(user_info, start_date="2019-02-11", end_date="2019-02-12")