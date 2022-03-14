"""系统初始化

"""
from services.cfg import attack_scripts, defense_scripts

"""
加载配置文件

:param *args 目录写绝对路径
"""


def auto_scanner_files(*args):
    import os
    # 装进内存
    for file_path in args:
        # 导入所有目录的模板
        if os.path.exists(file_path) is True:
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if file[-3:] == "xml":
                        load_file_to_obj(os.path.join(root, file))


# 读取文件并转为对象
def load_file_to_obj(absolute_path):
    from services.file_utls import xml2obj
    xml2obj(absolute_path)


# 检查初始化配置
def check_init_config():
    # 模组是不是空的
    if attack_scripts["scripts_number"] == 0 and defense_scripts["scripts_number"] == 0:
        import sys
        print("加载失败~即将退出程序")
        sys.exit(-1)
    else:
        print("文件加载成功")
        print("生成目录中。。")


# 生成目录
def running_main_gui():
    from api.run_script import execute_model_by_id
    while True:
        opt = input(">> 这里有红色（攻击, 1）和蓝色（防御, 2）两种糖，你要哪个？【退出按d】<<\n")
        if opt == "d":
            import sys
            sys.exit(-1)

        if opt in ["红", "red", "红色", "1", "hong"]:
            while True:
                print("\tid\t\t【名称：简介】\t".center(50, "="))
                for index in range(0, len(attack_scripts["scripts_list"])):
                    payload = attack_scripts["scripts_list"][index]
                    print(f"{payload['menu_id']}\t\t【{payload['menu_title']}：{payload['menu_desc']}】")
                user_opt = input("请选择ID（回到上一级按q）：")
                if user_opt == "q":
                    break
                execute_model_by_id(user_opt)

        else:
            while True:
                print("\tid\t\t【名称：简介】\t".center(50, "="))
                for index in range(0, len(defense_scripts["scripts_list"])):
                    payload = defense_scripts["scripts_list"][index]
                    print(f"{payload['menu_id']}\t\t【{payload['menu_title']}：{payload['menu_desc']}】")
                user_opt = input("请选择ID（回到上一级按q）：")
                if user_opt == "q":
                    break
                execute_model_by_id(user_opt)

