# coding=utf8
import os
import json
from flask_login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUserMixin,
                            confirm_login, fresh_login_required)


class UserInfo(UserMixin):
    """
    用户信息类
    """

    def __init__(self, user_name, id,
                 email=None,
                 password=None,
                 active=True,
                 calender_server="google",
                 calender_name = "时间日历",
                 auth_token_file="",
                 data_root=""
                 ):
        self.email = email
        self.password = password
        self.active = active
        self.id = id
        self.user_name=user_name
        self.auth_token_file =auth_token_file
        self.calender_server = calender_server
        self.calender_name = calender_name
        self.data_root = data_root

    def __init__(self, info_dict):
        self.email = info_dict.setdefault("email", "")
        self.password = info_dict.setdefault("password", "")
        self.active = info_dict.setdefault("active", "")
        self.id = info_dict.setdefault("id", "")
        self.user_name = info_dict.setdefault("user_name", "")
        self.auth_token_file = info_dict.setdefault("auth_token_file", "")
        self.calender_server = info_dict.setdefault("calender_server", "")
        self.calender_name = info_dict.setdefault("calender_name", "")
        self.data_root = info_dict.setdefault("data_root", "")

    def get_by_id(self, id):
        dbUser = UserInfoManager.get_user_info(id)
        return dbUser

    def to_map(self):
        """
        转变为字典
        :return:
        """
        dict_t = {}
        dict_t["email"] = self.email
        dict_t["password"] = self.password
        dict_t["active"] = self.active
        dict_t["id"] = self.id
        dict_t["user_name"] = self.user_name
        dict_t["email"] = self.email
        dict_t["auth_token_file"] = self.auth_token_file
        dict_t["calender_server"] = self.calender_server
        dict_t["calender_name"] = self.calender_name
        dict_t["data_root"] = self.data_root
        return dict_t


class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"


class UserInfoManager:
    """
    管理已登录用户的工具类
    """
    userinfo_filename = "users_info.json"

    def __init__(self, root_dir):
        # 检查文件夹是否存在
        if not os.path.isdir(root_dir) :
            raise Exception("root_dir should be a EXIST dir, not a file")

        self.json_path = os.path.join(root_dir, UserInfoManager.userinfo_filename)
        self.root_dir = root_dir
        if not os.path.isfile(self.json_path):
            # 文件不存在，创建空文件
            with open(self.json_path,mode="w", encoding="utf8") as f:
                f.write("{}")
        # 读文件到json串中，构造map
        self.map = json.load(open(self.json_path,encoding="utf8"))

    def add_user_info(self, user_info):
        """
        添加一条用户信息
        :param user_info:
        :return:
        """
        username = user_info.user_name
        if username in ["default"]:
            raise Exception("user name can't be DEFAULT, choose another one ")

        # 将最后添加的设置为default用户
        self.map[username] = user_info.to_map()
        self.map["default"] = username
        # 保存到文件中
        json.dump(self.map,
                  open(self.json_path, encoding="utf8",mode="w"),
                  sort_keys=True,
                  indent=4,
                  separators=(',', ':'),
                  ensure_ascii=False)

    def rm_user_info(self, username):
        """
        删除一个用户信息
        :param username:
        :return:
        """
        self.map.pop(username)
        if username in [self.map.get("default")]:
            self.map.pop("default")

        # 保存到文件中
        json.dump(self.map,
                  open(self.json_path, encoding="utf8",mode="w"),
                  sort_keys=True,
                  indent=4,
                  separators=(',', ':'),
                  ensure_ascii=False)

    def get_user_info(self, username):
        """
        获得用户信息
        :param username:
        :return:
        """
        try:
            if username in ["default"]:
                username = self.map.get("default")
            m_dict = self.map.get(username)
            user_info = UserInfo(m_dict)
            return user_info
        except:
            return None

    def set_default_user(self, username):
        """
        设置用户名
        :param username:
        :return:
        """
        self.map["default"]=username

    def get_default_user(self):
        return userinfo.get_user_info(self.map.get("default"))


if __name__ == "__main__":
    userinfo = UserInfoManager(r".\data")
    t_map = {
        "email": "chongwangcc@gmail.com",
        "password": "123456",
        "active": True,
        "id": "cc",
        "user_name": "cc",
        "auth_token_file": r".\data\.credentials\cc_calendar.json",
        "calender_server": "google",
        "calender_name": "时间日志",
        "data_root": r".\data\cache\cc",
    }
    info = UserInfo(t_map)
    t_map = userinfo.add_user_info(info)
    t_path = userinfo.get_user_info("cc")
    print(t_path.to_map())

    t_map = {
        "email": "mmzhangwh@gmail.com",
        "password": "123456",
        "active": True,
        "id": "mm",
        "user_name": "mm",
        "auth_token_file": r".\data\.credentials\mm_calendar.json",
        "calender_server": "google",
        "calender_name": "时间日志",
        "data_root": r".\data\cache\mm",
    }
    info = UserInfo(t_map)
    t_map = userinfo.add_user_info(info)
    t_path = userinfo.get_user_info("mm")
    print(t_path.to_map())