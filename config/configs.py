import os
import traceback
import yaml


def read_yaml_config(file_path: str):
    with open(file_path, 'r') as stream:
        try:
            cfg = yaml.safe_load(stream)
        except yaml.YAMLError:
            print("在读取config时出现异常")
            traceback.print_exc()
            cfg = {}
    return cfg


config = read_yaml_config(os.path.join(os.path.dirname(__file__), "config.yaml"))
