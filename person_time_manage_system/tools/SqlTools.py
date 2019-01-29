#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/29 14:39 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : SqlTools.py 
# @Software: PyCharm

import sqlite3
g_sqlite3_path="./data/sqlit3.db"


def execute_script(sqlite3_file_path, sql_script_path):
    """
    执行sql脚本
    :return:
    :param sqlite3_file_path
    :param sql_script_path
    """
    with open(sql_script_path, mode="r", encoding="utf8") as f:
        create_sql = f.read()
        conn = sqlite3.connect(sqlite3_file_path)
        c = conn.cursor()
        c.executescript(create_sql)
        conn.commit()
        conn.close()
        return True
    return False


def create_table(mode="create"):
    """
    按照条件选择是否创建表格
    :param mode:
    :return:
    """
    global g_sqlite3_path
    if mode in ["create"]:
        create_script = r"./data/create_table.sql"
        execute_script(g_sqlite3_path, create_script)
    elif mode in ["drop"]:
        delete_script = r"./data/drop_table.sql"
        execute_script(g_sqlite3_path, delete_script)
    else:
        print("[ERROR] unkown mode "+mode)


if __name__ == "__main__":
    create_table("drop")
    create_table()


