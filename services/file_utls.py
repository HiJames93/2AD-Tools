"""启动时调用
"""
from services.cfg import attack_scripts, defense_scripts
import xml.dom.minidom

# 扫描模组
def scanner_models():
    pass

# 载入模组
def load_models():
    pass

"""xml转对象
主要在启动时调用，一次性读取所有文件暂不考虑性能问题
"""

# xml转对象
def xml2obj(absolute_path):
    DOMTree = xml.dom.minidom.parse(absolute_path)
    collection = DOMTree.documentElement
    if collection.hasAttribute("shelf"):
        # 功能集合
        func_list = collection.getElementsByTagName("menu")

        for func in func_list:
            if func.hasAttribute("title") != "":

                menu_id = func.getAttribute("cardid")
                menu_title = func.getElementsByTagName('title')[0].childNodes[0].data
                script_path = func.getElementsByTagName('func_path')[0].childNodes[0].data
                menu_desc = func.getElementsByTagName('description')[0].childNodes[0].data

                # 划分目录
                if collection.getAttribute("shelf") == "attack":
                    attack_scripts["scripts_number"] += 1
                    attack_scripts["scripts_list"].append({
                        "menu_id": menu_id,
                        "menu_title": menu_title,
                        "script_path": script_path,
                        "menu_desc": menu_desc
                    })
                elif collection.getAttribute("shelf") == "defense":
                    defense_scripts["scripts_number"] += 1
                    defense_scripts["scripts_list"].append({
                        "menu_id": menu_id,
                        "menu_title": menu_title,
                        "script_path": script_path,
                        "menu_desc": menu_desc
                    })


"""运行时调用
"""

"""异常时调用
"""