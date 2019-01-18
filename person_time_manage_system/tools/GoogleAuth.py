#!/usr/bin/python
# -*- coding: utf-8 -*
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    args=argparse.ArgumentParser(parents=[tools.argparser])
    #flags =args.parse_args("")
    flags = args.parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API'


def get_credentials(user_name):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   user_name+'_calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        http = httplib2.Http(proxy_info=httplib2.ProxyInfo(
            httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1080))
        if flags:
            credentials = tools.run_flow(flow, store, flags,http)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_service(user_name):
    """
    获得日历的server
    :return:
    """
    credentials = get_credentials(user_name)
    http = httplib2.Http(proxy_info=httplib2.ProxyInfo(
        httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1080))
    http = credentials.authorize(http)
    service = discovery.build('calendar', 'v3', http=http)
    return service

def get_calender_ID(service,name):
    """
    获得 日历 ID
    :param server:  日历服务
    :param name:  日历的名称
    :return: 此名称日历对应ID
    """
    page_token = None
    ID= None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            #print([calendar_list_entry['summary']],[name])
            if name == calendar_list_entry['summary']:
                ID = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token or not ID:
            break
    return ID

def get_calender_content(service,id,timeMin,timeMax):
    """
    获得 日历 的指定时间段所有的活动
    :param service:
    :param id:
    :param start_date:
    :param end_date:
    :return:
    """
    calendar = service.calendars().get(calendarId=id).execute()
    #print(calendar)
    eventsResult = service.events().list(
        calendarId=id, timeMin=timeMin,timeMax=timeMax , singleEvents=True,
        orderBy='startTime').execute()
    list_result=[]
    events = eventsResult.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end=event['end'].get('dateTime', event['end'].get('date'))
        title=event['summary']
        #print(start, end,title)
        listIndex=[start,end,title]
        list_result.append(listIndex)
    return list_result

if __name__ == '__main__':
    get_service("mm")
