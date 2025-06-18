import os
import traceback
import yaml
import shutil


def read_yaml_config(file_path: str):
    try:
        with open(file_path, 'r') as stream:
            cfg = yaml.safe_load(stream)
    except yaml.YAMLError:
        print("在读取config时出现异常")
        traceback.print_exc()
        cfg = {}
    return cfg


if not os.path.isfile(os.path.join(os.path.dirname(__file__), "config.yaml")):
    if os.path.isfile(os.path.join(os.path.dirname(__file__), "config_example.yaml")):
        # copy example to config
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "config_example.yaml"),
                        os.path.join(os.path.dirname(__file__), "config.yaml"))
    else:
        with open(os.path.join(os.path.dirname(__file__), "config.yaml"), 'w') as f:
            f.write('''bc_docker_api: "http://127.0.0.1:8009/generate"
openai_key: "sk-xxx"
openai_host:
  - "https://api.openai.com/v1/chat/completions"''')
config = read_yaml_config(os.path.join(os.path.dirname(__file__), "config.yaml"))
