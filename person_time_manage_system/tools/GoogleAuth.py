#!/usr/bin/env python
# -*- coding: utf-8 -*

import httplib2
import os
from random import Random

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from google_auth_oauthlib.flow import InstalledAppFlow
import configparser

from tools.SqlTools import fetch_user_info

try:
    import argparse
    args=argparse.ArgumentParser(parents=[tools.argparser])
    flags = args.parse_args()
except ImportError:
    flags = None
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


def get_credentials(user_name):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # TODO 从网络中获得授权文件，保存到数据库中

    # 0.创建临时文件
    credential_dir = os.path.join(HOME_DIR, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   user_name+'_calendar.json')

    store = Storage(credential_path)
    credentials = store.get()
    # 1.从网络中获取
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        http = httplib2.Http(proxy_info=fanqian_proxy)
        credentials = tools.run_flow(flow, store, flags, http)


        print('Storing credentials to ' + credential_path)

    # 2.保存到sql数据库中
    # TODO 待测试
    user_info = fetch_user_info(user_name)
    with open(credential_path, encoding="utf8") as f:
        user_info.auth_code = f.read()
    user_info.save()
    return credentials


def get_credentials_from_db(user_name):
    """
    从数据库中获得授权文件
    """
    credentials = None
    try:
        user_info = fetch_user_info(user_name)
        credentials = client.Credentials.new_from_json(user_info.auth_code)
    except:
        pass
    return credentials


def get_service(user_name):
    """
    获得日历的server
    :return:
    """
    # 获得授权文件
    credentials = get_credentials_from_db(user_name)
    if credentials is None:
        credentials = get_credentials(user_name)

    # 设置代理
    http = httplib2.Http(proxy_info=fanqian_proxy)
    http = credentials.authorize(http)

    # 3. 获得日历服务
    service = discovery.build('calendar', 'v3', http=http)
    return service


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


def gen_calender_auth_url(user_name):
    """
    生成google日历获得授权的url
    :return:
    :param redirect_uri
    """
    redirect_uri = REDIRECT_HOST+"/api/v1/login/calender_oauth"
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES,redirect_uri=redirect_uri)
    state = random_str()
    url = flow.step1_get_authorize_url()
    url += "&state="+state
    flow_map[state] = {
        "flow": flow,
        "user_name": user_name
    }

    return url


def gen_calender_auth_2(state, code):
    try:
        # 1. 获得credons_json串
        http = httplib2.Http(proxy_info=fanqian_proxy)
        flow = flow_map.get(state)["flow"]
        cred = flow.step2_exchange(code, http=http)
        user_name =  flow_map.get(state)["user_name"]

        # 2.  保存授权json到数据库中
        user_info = fetch_user_info(user_name)
        user_info.auth_code = cred.to_json()
        user_info.save()

        return True
    except:
        return False


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


def gen_userinfo_url(uri):
    url = REDIRECT_HOST + "/userinfo"
    return url



if __name__ == '__main__':
    url = gen_calender_auth_url()
    print(url)
