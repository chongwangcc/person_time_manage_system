# -*- coding: utf-8 -*
from flask import Flask, request, redirect
import httplib2
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
app = Flask(__name__)
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
credentials_files = r"E:\project\CM\Python\googleCalenderAPI\docs\client_id.json"



@app.route("/login")
def login():
    """
    登陆google界面
    :return:
    """

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials_files, SCOPES,redirect_uri="http://127.0.0.1:48080/oauthcallback")
        # flow = OAuth2WebServerFlow(client_id="366346832077-5ha34bck9556ok2710p7maudmb3vetu5.apps.googleusercontent.com",
        #                            client_secret="WKOdQp_sjjU_h7PcJX0I9i74",
        #                            scope=SCOPES,
        #                            redirect_uri="http://localhost:48080/auth")
        http = httplib2.Http(proxy_info=httplib2.ProxyInfo(
            httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1080))
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
        print(auth_uri)
        # creds = tools.run_flow(flow, store,http=http)
        print(creds)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                       maxResults=10, singleEvents=True,
    #                                       orderBy='startTime').execute()
    # events = events_result.get('items', [])
    #
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

@app.route("/oauthcallback")
def permission_auth():
    """
    授权后的跳转界面
    :return:
    """
    flow = client.flow_from_clientsecrets(credentials_files, SCOPES,
                                          redirect_uri="http://127.0.0.1:48080/oauthcallback")
    code = request.args.get("code")
    scope = request.args.get("scope")
    print(code)
    print(scope)
    http = httplib2.Http(proxy_info=httplib2.ProxyInfo(
        httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1080))
    creds = flow.step2_exchange(code,http=http)
    print(creds)


@app.route("/")
def index():
    """
    打开默认界面
    :return:
    """
    # 判断有没有用户登录
    return app.send_static_file('login.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=48080, debug=True)
