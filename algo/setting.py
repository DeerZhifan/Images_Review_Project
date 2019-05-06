import os
import yaml


def get_config():
    """将config.yaml的内容转换为字典"""
    parent_path = os.path.dirname(os.path.dirname(__file__))
    setting_filename = parent_path + "/resources/config.yaml"
    setting_dict = yaml.load(open(setting_filename, encoding="utf-8"))
    config = dict()
    for key, values in setting_dict.items():
        config[key] = values
    return config


config = get_config()

