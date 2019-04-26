import os
import yaml


def get_config():
    """将config.yaml的内容转换为字典"""
    parent_path = os.path.dirname(os.path.dirname(__file__))
    print(parent_path)
    setting_filename = os.path.join(parent_path, "config.yaml")
    print(setting_filename)
    setting_dict = yaml.load(open(setting_filename, encoding="utf-8"))
    config = dict()
    for key, values in setting_dict.items():
        config[key] = values
    return config


config = get_config()

