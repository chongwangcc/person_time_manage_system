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


class CalenderServer:

    def format_date_str_for_calender_server(self,date_str, service="google"):
        """
        将日期字符串，格式化 日历服务需要的字符串格式
        :param date_str:
        :return:
        """
        if service in ["google"]:
            naive = datetime.strptime(date_str + " 0:0:0", "%Y-%m-%d %H:%M:%S")
            naive=naive-timedelta(hours=8)
            time_min = naive.isoformat() + 'Z'
            return time_min
        else:
            return None

    def standard_content_list(self, user_id, list_result):
        """
        将日历数据标准化，方便下一步计算
        [user_id, date_str, 星期几，开始时间，结束时间, 类别, 持续分钟数, 描述字符串]
        :param user_id:
        :param list_result: [['2019-01-01T00:00:00+08:00', '2019-01-01T05:30:00+08:00', '睡觉'], ...]
        :return:
        """
        result = []
        for list_one in list_result:
            start_date_str = list_one[0][:10]
            start_time_str = list_one[0][11:19]
            end_date_str = list_one[1][:10]
            end_time_str = list_one[1][11:19]

            ss = re.split(u",| |;|，|；|:|：|～", list_one[2])
            if ss is None or len(ss) == 0:
                continue

            category = ss[0]
            description = "".join(ss[1:])

            if start_date_str == end_date_str:
                # 记录没有跨天，在同一天
                weeknum = datetime.strptime(start_date_str, '%Y-%m-%d').weekday()
                during = 1
                app_list = [user_id, start_date_str, weeknum, start_time_str, end_time_str, category, during ,description]
                result.append(app_list)
            else:
                # 记录跨天，要拆分

                pass





    def get_time_details(self, userinfo, start_date, end_date):
        """
        获得时间的明细，
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
            proxy = httplib2.ProxyInfo( httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1080)
            # 2. 创建 日历 服务
            service = GoogleAuth.get_service(userinfo.user_name,
                                             userinfo.auth_token_file,
                                             proxy=proxy)
            calendar_id = GoogleAuth.get_calender_id(service, userinfo.calender_name)

            # 3. 连接日历 获得结果
            time_list = GoogleAuth.get_calender_content(service, calendar_id, time_min, time_max)

            # 4. 格式化字符串


            print(time_list)

            pass
        else:
            print("calender server ["+userinfo.calender_server+"] not support yet" )


if __name__ == "__main__":
    # user_info = fetch_userInfo("cc")
    # calender_server = CalenderServer()
    # calender_server.get_time_details(user_info, start_date="2019-01-01", end_date="2019-01-02")

    ss = ["睡觉"]
    description = "".join(ss[2:])
    print(ss[2:])

    pass