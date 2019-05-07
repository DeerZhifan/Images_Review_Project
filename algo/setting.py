from algo.password import PassWord
import os
import yaml


def get_pyconfig_dict():
    """将pyconfig的内容转化为字典, 根据线上不同环境使用不同配置"""
    online_pyconfig_path = r'/home/apps/bootstrap/current/config/pyconfig.yaml'
    pc_path = r'C:\Users\ABC\IdeaProjects\btr-algorithm\btr-algorithm-publish\src\main\resources\pyconfig.yaml'
    mac_path = r'/users/vita/IdeaProjects/btr-algorithm\btr-algorithm-publish/src/main/resources/pyconfig.yaml'
    if os.path.exists(online_pyconfig_path):
        pyconfig_path = online_pyconfig_path
    elif os.path.exists(pc_path):
        pyconfig_path = pc_path
    else:
        pyconfig_path = mac_path

    pyconfig_dict = yaml.load(open(pyconfig_path, encoding='utf-8'))
    # 解密
    pw = PassWord(pyconfig_dict['algo_mysql']['public_key'])
    pyconfig_dict['algo_mysql']['password'] = pw.decrypt_text(pyconfig_dict['algo_mysql']['encrypted_password'])
    del pyconfig_dict['algo_mysql']['public_key']
    del pyconfig_dict['algo_mysql']['encrypted_password']
    return pyconfig_dict


def get_config(yaml_path):
    """将config.yaml的内容转换为字典"""
    parent_path = os.path.dirname(os.path.dirname(__file__))
    setting_filename = os.path.join(parent_path + yaml_path)
    setting_dict = yaml.load(open(setting_filename, encoding="utf-8"))
    return setting_dict


pyconfig = get_pyconfig_dict()
local_config = get_config("/resources/local_config.yaml")



