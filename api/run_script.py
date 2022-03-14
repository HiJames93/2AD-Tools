# -*- coding: utf-8 -*-


from services.cfg import attack_scripts, defense_scripts


# 根据ID执行脚本
def execute_model_by_id(model_id):
    import os
    mode_info = {}
    # 查找对应脚本
    for mode in attack_scripts["scripts_list"]:
        if mode["menu_id"] == model_id:
            mode_info = mode
    for mode in defense_scripts["scripts_list"]:
        if mode["menu_id"] == model_id:
            mode_info = mode
    # 加载并执行脚本
    if len(mode_info) > 0:
        print(f"运行脚本{mode_info['menu_title']}")
        os.system(f"python3 {mode_info['script_path']}")
    # with open(mode_info["script_path"], mode='r', encoding='utf-8') as script:
    #     codes = script.read()
    #     exec(codes)