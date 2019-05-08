#!/usr/bin/env python
# -*- coding: utf-8 -*

import httplib2
import os
from random import Random

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import configparser

from tools.SqlTools import fetch_user_info


cf = configparser.ConfigParser()
cf.read(r"./data/base.conf")

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = cf.get("google_calender", "CLIENT_SECRET_FILE")
APPLICATION_NAME = cf.get("google_calender", "APPLICATION_NAME")
HOME_DIR = cf.get("google_calender", "TMP_DIR")
REDIRECT_HOST =  cf.get("google_calender", "REDIRECT_HOST")

has_proxy = cf.getboolean("proxy", "user_proxy")
if has_proxy:
    fanqian_proxy = httplib2.ProxyInfo(
                    httplib2.socks.PROXY_TYPE_SOCKS5,
                    cf.get("proxy", "proxy_ip"),
                    cf.getint("proxy", "proxy_port")
                    )
else:
    fanqian_proxy = None

flow_map = {}



def get_calender_id(credential_service, name=u"时间日志"):
    """
    获得 日历 ID
    :param credential_service:  日历服务
    :param name:  日历的名称
    :return: 此名称日历对应ID
    """
    page_token = None
    id = None
    while True:
        calendar_list = credential_service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if name == calendar_list_entry['summary']:
                id = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token or not id:
            break
    return id


def get_calender_content(credential_service, calender_id, min_time, max_time):
    """
    获得 日历 的指定时间段所有的活动
    :param credential_service:
    :param calender_id:
    :param min_time:
    :param max_time:
    :return:
    """
    # calendar = credential_service.calendars().get(calendarId=calender_id).execute()
    calendar_request = credential_service.events().list(calendarId=calender_id,
                                                     timeMin=min_time,
                                                     timeMax=max_time,
                                                     singleEvents=True,
                                                     orderBy='startTime')
    events_response = calendar_request.execute()
    list_result = []
    while events_response is not None:
        # 1. 添加日历结果到list列表
        events = events_response.get('items', [])
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            title = event.setdefault('summary',"")
            listIndex = [start, end, title]
            list_result.append(listIndex)
        # 2. 获得下一页内容
        t_calendar_request = credential_service.events().list_next(calendar_request, events_response)
        if t_calendar_request is None:
            break
        events_response = t_calendar_request.execute()
    # print("final"+str(len(list_result)))
    return list_result


def gen_calender_auth_url_bak(user_name):
    """
    生成google日历获得授权的url
    :return:
    :param redirect_uri
    """
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    flow.redirect_uri = REDIRECT_HOST+"/api/v1/login/calender_oauth"
    url, t_id = flow.authorization_url()
    # url += "&redirect_uri="+REDIRECT_HOST+"/api/v1/login/calender_oauth"
    print(url)
    flow_map[t_id] = {
        "flow": flow,
        "user_name": user_name
    }
    return url,t_id


def random_str(randomlength=16):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def check_user_config(user_name):
    """
    检查用户有没有配置基本信息
    :param user_name:
    :return:
    """
    user_info = fetch_user_info(user_name)
    if user_info is None:
        return False

    if user_info.password is None or len(user_info.password)<1:
        return False

    if user_info.calender_server is None or len(user_info.calender_server)<1:
        return False

    if user_info.calender_name is None or len(user_info.calender_name)<1:
        return False
    return True


def gen_url(uri):
    url = REDIRECT_HOST + uri
    return url



