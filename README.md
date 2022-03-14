# 2AD-Tools（Attack and Defense）攻击与防御工具

## 简介
这是一个中介工具, 不提供任何武器或服务,只承担组织和集中调度的功能
如果您需要额外添加别的目录,请严格遵守模板的使用约定,否则后果自负.
系统默认集成了一些脚本.您可以直接改造tools目录中的文件,模块脚本与
平台完全隔离不受任何影响.

> 约定

1. 系统自带攻击和防御两种配置模组，以方便用户后来增加自定义功能
2. 可以有无数个模组但是最多只能有2层目录，毕竟这只是个轻量级脚本

- 模组规范：
    ```xml
      <collection shelf="defense">
        <menu title="防御" cardid="simple_check">
            <title>通用DOS检测</title>
            <func_path>/root/py_tools/hacker/2AD-Tools/tools/universal_dos_detection.py</func_path>
            <description>默认请求量500/s 带宽40mb以下，可自定义</description>
        </menu>
        <menu title="监听" cardid="listen_info">
            <title>ARP监听</title>
            <func_path>/root/py_tools/hacker/2AD-Tools/tools/LAN/monitor_traffic.py</func_path>
            <description>不提供监听功能</description>
        </menu>
      </collection>
    ```
  - 攻击或防御仅需修改父级节点的shelf值即可
    - 攻击:attack
    - 防御为:defense
  - menu可以有多个,每个menu代表一个脚本
    - cardid是唯一的,重复则导致程序无法正常运行
    - func_path标签需要填写脚本的绝对路径!

### 特别说明
1. 程序暂定只有攻防两种功能
2. 如若需要加入自定义脚本,请在启动前修改此处
    - auto_scanner_files的形参是个元组,每个路径用逗号隔开即可;程序会自动将其扫描到内存
```python
#!/usr/bin/python3

from api.sys_init import auto_scanner_files, check_init_config, running_main_gui

if __name__ == '__main__':
    # 加载文件到内存
    auto_scanner_files('/root/py_tools/hacker/2AD-Tools/tools','other')
    # 启动前检查
    check_init_config()
    # 生成目录
    running_main_gui()
```

## 快速开始
1. 运行环境>=python3.6
2. 用你环境的pip工具安装packages.txt
3. linux系统,需要额外安装rpm yum等基本工具.最好是红帽系列的系统
4. 给main.py授权或直接执行python3 main.py"# 2AD-Tools" 
