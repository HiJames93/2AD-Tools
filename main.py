#!/usr/bin/python3

from api.sys_init import auto_scanner_files, check_init_config, running_main_gui

if __name__ == '__main__':
    # 加载文件到内存
    auto_scanner_files('/root/py_tools/hacker/2AD-Tools/tools','other')
    # 启动前检查
    check_init_config()
    # 生成目录
    running_main_gui()