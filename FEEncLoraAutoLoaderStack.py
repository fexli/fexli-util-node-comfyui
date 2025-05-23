import json
import os.path
import re
from typing import List
import folder_paths  # noqa
from folder_paths import models_dir  # noqa
import comfy.sd  # noqa
import comfy.utils  # noqa
from nodes import LoraLoader  # noqa
from .utils.lora_enc_map import read_automap, read_emp
from .utils.any_hack import any
from .utils.model_info import get_metadata


class LoraRef:
    def __init__(self, name: str, model_s: float, clip_s: float):
        self.name = name
        self.model_s = model_s
        self.clip_s = clip_s


def find_model(text, model_name):
    pattern = r'<lora:' + re.escape(model_name) + r'(:)?(\d+(?:\.\d+)?)?(:)?(\d+(?:\.\d+)?)?>'
    match = re.search(pattern, text)

    if match:
        model_s = float(match.group(2) or 1)
        clip_s = float(match.group(4) or model_s)
        return match.start(), model_s, clip_s, match.end()
    else:
        return None


def replaceStrFunc(nom_str):
    original_str = nom_str
    lora_patterns = re.findall(r"<lora:[^<>]*>", original_str)
    modified_str = ""
    last_index = 0
    for pattern in lora_patterns:
        modified_str += original_str[last_index:original_str.find(pattern)]
        last_index = original_str.find(pattern) + len(pattern)
        if last_index < len(original_str) and original_str[last_index] == ',':
            last_index += 1
    modified_str += original_str[last_index:]
    if modified_str.endswith(','):
        modified_str = modified_str[:-1]
    return lora_patterns, modified_str


def getStrLoraName(str):
    str_input = str
    match = re.search(r"<lora:([^>]*)>", str_input)
    if match:
        lora_content = match.group(1)
        if ':' in lora_content:
            parts = lora_content.split(':')
            main_part = parts[0]
            numbers = []
            for part in parts[1:]:
                num_match = re.search(r'(-?\d+(\.\d+)?)', part)
                if num_match:
                    numbers.append(num_match.group(0))
            return main_part, numbers
        else:
            return lora_content, []
    else:
        return None, []


class FEEncLoraAutoLoaderStack(LoraLoader):
    LORADIR_CACHE = folder_paths.get_filename_list("loras")

    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(s):
        s.LORADIR_CACHE = folder_paths.get_filename_list("loras")

        return {
            "required": {
                "model_type": (["sd1.5", "sdxl", "sd3", "sd3.5", 'pony', 'il', 'noob', 'flux'],),
                "prompt": ("STRING", {"default": "", 'forceInput': True}),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LORA_STACK", 'STRING', any)
    RETURN_NAMES = ("lora_stack", "prompt", "EXTRA")
    FUNCTION = "load_lora_stack"

    CATEGORY = "loaders"

    @staticmethod
    def get_replace(lora_setting, trigger_wd):
        replace = lora_setting.get("replace", None)
        if replace is None:
            return trigger_wd
        if isinstance(replace, dict):
            replace = replace.get(trigger_wd, trigger_wd)
        if isinstance(replace, list):
            return replace[0]
        return str(replace)

    def load_lora_stack(self, model_type, prompt, strength_model, strength_clip):
        lora_need_load = []  # type:List[LoraRef]
        pe = str(prompt)
        pe_lower = pe  # .lower()

        # auto lora maps
        auto_loras = read_automap("loras")
        for lora_name, lora_setting in auto_loras.items():
            if lora_setting.get("model", "?") != model_type:
                continue
            tw = lora_setting.get("trigger_word", "")
            if tw == "" or tw not in pe_lower:
                continue
            # 存在，检查是否为<xx:f:f>
            lora_find_rs = find_model(pe_lower, tw)
            if lora_find_rs is None:
                continue
            pe = pe[:lora_find_rs[0]] + pe[lora_find_rs[3]:]
            pe_lower = pe
            model_s = lora_find_rs[1]
            clip_s = lora_find_rs[2]
            lora_need_load.append(LoraRef(lora_name, model_s, clip_s))

        arr, rel_str = replaceStrFunc(pe)
        # find unique loranames
        for str_lora_item in arr:
            loar_sim_path, str_n_arr = getStrLoraName(str_lora_item)
            model_s = strength_model
            model_c = strength_clip
            if len(str_n_arr) > 0:
                if len(str_n_arr) == 1:
                    model_s = model_c = float(str_n_arr[0])
                if len(str_n_arr) > 1:
                    model_s, model_c = float(str_n_arr[0]), float(str_n_arr[1])
            lora_name = loar_sim_path if loar_sim_path in self.LORADIR_CACHE else None
            if lora_name is None:
                next_lora_name = loar_sim_path + ".safetensors"
                if next_lora_name in self.LORADIR_CACHE:
                    lora_name = next_lora_name
            if lora_name is None:
                rel_str += f', !{str_lora_item}'
                continue
            lora_need_load.append(LoraRef(lora_name, model_s, model_c))
        result = list()

        for lora_ref in lora_need_load:
            if lora_ref.name not in self.LORADIR_CACHE:
                print("Failed to load lora with empty name", lora_ref.name)
                continue
            result.extend([(lora_ref.name, lora_ref.model_s, lora_ref.clip_s)]),
        print("Auto Load", len(result), "LLor ClipData")
        return (result, rel_str, {},)
