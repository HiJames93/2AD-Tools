# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import os
    host = input("请输入主机：")
    info_list = os.popen(f"nmap -sS {host}").readlines()
    for info in info_list[3:-2]:
        if info != "\n":
            print(info[:-1])