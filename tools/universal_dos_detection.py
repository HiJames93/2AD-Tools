import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time
from datetime import datetime


# 操作防火墙
def firewall(ip):
    # 查看该ip是否已被封禁
    firewalld = os.popen("firewall-cmd --list-all").read()
    if ip.strip() not in firewalld:
        # 封禁一小时
        execute = os.popen(f'firewall-cmd --add-rich-rule="rule family=ipv4 source address={ip.strip()} '
                           f'drop" --timeout=3600').read()
        if execute.strip() == "success":
            print(f"{ip.strip()} 已被防火墙封禁1小时。")
            mail(f"发现入侵行为: {ip},防火墙已封禁该IP。")
        else:
            print(f"{ip.strip()} 封禁失败, 请联系管理员。")
            mail(f"发现入侵行为: {ip},防火墙封禁失败，请尽快登录查看。")
            return False
    return True

# 邮件告警
def mail(warn):
    try:
        # 发送邮箱和接收邮箱是同一个
        sender = '2396065191@qq.com'
        # 构建邮件的主体对象
        msg = MIMEMultipart()
        msg['Subject'] = '系统安全警告'
        msg['From'] = sender
        msg['To'] = sender
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        content = MIMEText(warn, 'plain', 'utf-8')
        msg.attach(content)

        # 建立与邮件服务器的连接并发送邮件
        smtp_obj = smtplib.SMTP_SSL('smtp.qq.com', 465)  # 如果基于SSL，则 smtplib.SMTP_SSL
        smtp_obj.login(user=sender, password='stpptxbxuykzecdi')  # 登录发信邮箱
        smtp_obj.sendmail(sender, sender, str(msg))  # 发送邮件
        smtp_obj.quit()  # 退出
    except Exception as e:
        print(f"邮件告警失败，错误信息是: {e}")

# 获取日志信息
def gain_log():
    ip_list = []  # 存放访问用户的ip信息
    today = time.strftime("%d/%b/%Y")  # 获取今天的年月日信息,以这个当检索标志
    data = os.popen(f"tail -n 5000 /opt/lampp/logs/access_log | grep {today} | grep -v ::1").readlines()  # 提取今天的访问日志
    for i in data:
        ip = i.split()[0]  # 获取ip
        """92.168.100.130 - - [09/Mar/2022:11:16:44 +0800] "GET /dash"""
        tim = i.split("[")[1].split(" +")[0]  # 获取访问时间
        tim = str(datetime.strptime(tim, '%d/%b/%Y:%H:%M:%S'))  # 格式转换

        dic = {"ip": ip, "time": []}
        if ip_list:  # 判断列表是否为空
            for j in ip_list:
                if j['ip'] == ip:
                    j["time"].append(tim)  # ip已添加的话添加访问时间
                    break
            else:
                ip_list.append(dic)
        else:
            ip_list.append(dic)

    return ip_list

# 查看日志信息并进行安全操作
def show_log():
    ip_list = gain_log()
    for dic in ip_list:
        start = datetime.strptime(dic['time'][0], "%Y-%m-%d %H:%M:%S")  # (形式要对应)
        end = datetime.strptime(dic['time'][-1], "%Y-%m-%d %H:%M:%S")
        # 相减得到秒数、小时、天数
        seconds = (end - start).seconds
        print(f"IP: {dic['ip']}, 时间段: {dic['time'][0]} ~ {dic['time'][-1]}, 访问次数: {len(dic['time'])}")

        if seconds < 10 and len(dic['time']) > 100:  # 访问时间时间段小于10秒 和 访问次数 大于100的封ip
            print(f"{dic['ip']} 疑似攻击主机，正在封禁该ip。")
            firewall(dic['ip'])

# 获取网络的通信状态
def gain_network():
    # 获取http的半连接数量
    syn_number = int(os.popen("netstat -ant | grep :80 | grep SYN_RECV | wc -l").read().strip())
    # 获取http的正在通信的连接数量
    est_number = int(os.popen("netstat -ant | grep :80 | grep ESTABLISHED | wc -l").read().strip())
    # 获取http接收缓冲区堆积的连接数
    recv = int(os.popen("ss -ltn | grep :80 | awk '{print $2}'").read().strip())
    return syn_number, est_number, recv

# 获取CPU的平均负载百分比
def gain_cpu():
    # cpu负载情况
    cpu_load = os.popen("uptime | awk -F : '{print $NF}'").read().strip()
    cpu_load = cpu_load.split(", ")  # cpu负载列表
    # 获取系统cpu的个数
    cpu_number = int(os.popen("lscpu | grep 'CPU(s):' | awk '{print $2}'").readline()[0])

    cpu_load = [format(float(i) / cpu_number, '.0%') for i in cpu_load]  # 以百分比显示
    return cpu_load

# 获取实时带宽
def bandwidth():
    res = 0
    unit = "Bytes"  # 定义默认单位
    for i in range(5):
        # 获取发送的数据总量
        data_1 = int(os.popen("ifconfig | head -n 7 | tail -n 1 | awk '{print $5}'").read().strip())
        time.sleep(0.5)
        data_2 = int(os.popen("ifconfig | head -n 7 | tail -n 1 | awk '{print $5}'").read().strip())
        # 实时带宽
        bw = data_2 - data_1
        res += bw
    res = res / 5  # 求平均值
    original_bw = res  # 保存原先的bytes大小
    # 判断实时流量大小是否可以转换
    if res > 1024:
        res = res / 1024  # KB
        unit = "KB"
        if res > 1024:
            res = res / 1024  # MB
            unit = "MB"
    return int(res), unit, original_bw

# 主调
def main():
    bw, unit, original_bw = bandwidth()  # 实时带宽
    cpu_load = gain_cpu()  # cpu负载
    syn, est, recv = gain_network()  # 网络通信状态
    print(f"CPU Load: {cpu_load[0]}, Band Width: {bw}{unit}, SYN_connect: {syn}, ESTABLISHED_connect: {est}, Recv-Q: {recv}")

    # 判断是否有安全风险
    cpu_load = int(cpu_load[0].replace("%", ""))
    # CPU负载大于500%并且带宽大于100MB时
    if cpu_load > 500 and original_bw > 104857600:   # 104857600Byes 相当于 100MB
        print("出现安全风险，正在进行访问日志确认。")
        show_log()

    time.sleep(1)
    main()


if __name__ == '__main__':
    main()

