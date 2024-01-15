from folder_paths import models_dir  # noqa
import json
import os

emp_datas = {}


def read_emp(folders="loras"):
    global emp_datas
    if folders in emp_datas:
        return emp_datas[folders]
    emp_fp = os.path.join(models_dir, folders, "exist_map.json")
    if os.path.exists(emp_fp):
        with open(emp_fp, "r") as f:
            emp = json.load(f)
    else:
        emp = {}
    emp_datas[folders] = emp
    return emp


read_emp("loras")


class FELoraEmpFinder:
    EMP_CACHE = read_emp("loras")

    @classmethod
    def find_current_lora(c, name):
        while name in c.EMP_CACHE.keys():
            name = c.EMP_CACHE[name]
        return name

    @classmethod
    def find_real_lora(c, name):
        while name in c.EMP_CACHE.values():
            name = list(c.EMP_CACHE.keys())[list(c.EMP_CACHE.values()).index(name)]
        return name
