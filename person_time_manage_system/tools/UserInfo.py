# coding=utf8
import os
import json
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUserMixin,
                            confirm_login, fresh_login_required)


class UserInfo(UserMixin):
    """
    用户信息类
    """
    def __init__(self, email=None, password=None, active=True, id=None):
        self.email = email
        self.password = password
        self.active = active
        self.isAdmin = False
        self.id = None

    def get_by_id(self, id):
    	dbUser = UserInfoManager.get_user_info(id)
    	if dbUser:
    		self.email = dbUser.email
    		self.active = dbUser.active
    		self.id = dbUser.id

    		return self
    	else:
    		return None


class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"


class UserInfoManager:
    """
    管理已登录用户的工具类
    """
    userinfo_filename = "users_info.json"
    token_json = "token.json"

    def __init__(self, root_dir):
        # 检查文件夹是否存在
        if not os.path.isdir(root_dir) :
            raise Exception("root_dir should be a EXIST dir, not a file")

        self.json_path = os.path.join(root_dir, UserInfo.userinfo_filename)
        self.root_dir = root_dir
        if not os.path.isfile(self.json_path):
            # 文件不存在，创建空文件
            with open(self.json_path,mode="w",encoding="utf8") as f:
                f.write("{}")
        # 读文件到json串中，构造map
        self.map = json.load(open(self.json_path,encoding="utf8"))

    def add_user_info(self, username, calender_name):
        """
        添加一条用户信息
        :param username:
        :param calender_name:
        :return:
        """
        if username in ["default"]:
            raise Exception("user name can't be DEFAULT, choose another one ")
        t_map = {username:{"calender_name":calender_name,}}
        self.map[username] = {"calender_name": calender_name,
                              "data_root": os.path.join(self.root_dir,username)
                              }

        # 将最后添加的设置为default用户
        self.map["default"] = username
        # 保存到文件中
        json.dump(self.map, open(self.json_path,encoding="utf8", mode="w"), ensure_ascii=False)

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
        json.dump(self.map, open(self.json_path, encoding="utf8",mode="w"), ensure_ascii=False)

    def get_user_info(self, username):
        """
        获得用户信息
        :param username:
        :return:
        """
        if username in ["default"]:
            username = self.map.get(username)
        return self.map.get(username)

    def set_default_user(self, username):
        """
        设置用户名
        :param username:
        :return:
        """
        self.map["default"]=username

    def get_default_user(self):
        return userinfo.get_user_info(self.map.get("default"))

    def get_token_path(self, username):
        """
        获得用户授权文件路径
        :param username:
        :return:
        """
        t_user_info = self.get_user_info(username)
        t_path = os.path.join(t_user_info["data_root"], UserInfo.token_json)
        return t_path


if __name__ == "__main__":
    userinfo = UserInfo(r"E:\project\CM\Python\googleCalenderAPI\docs\data")
    t_map = userinfo.add_user_info("chongwangcc", "时间日历")
    t_path = userinfo.get_token_path("chongwangcc")
    print(t_path)