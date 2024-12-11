import functools
import time

from folder_paths import models_dir  # noqa
import json
import os


def cache_with_timeout(timeout):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in wrapper.cache and time.time() - wrapper.cache[key][1] < timeout:
                return wrapper.cache[key][0]
            result = func(*args, **kwargs)
            wrapper.cache[key] = (result, time.time())
            return result

        wrapper.cache = {}
        return wrapper

    return decorator


@cache_with_timeout(60)
def read_emp(folders="loras"):
    emp_fp = os.path.join(models_dir, folders, "exist_map.json")
    if os.path.exists(emp_fp):
        with open(emp_fp, "r") as f:
            emp = json.load(f)
    else:
        emp = {}
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


@cache_with_timeout(60)
def read_automap(folders="loras"):
    amp_fp = os.path.join(models_dir, folders, "lora_autoinit_map.json")
    if os.path.exists(amp_fp):
        with open(amp_fp, "r") as f:
            amp = json.load(f)
    else:
        amp = {}
    return amp


read_automap("loras")
