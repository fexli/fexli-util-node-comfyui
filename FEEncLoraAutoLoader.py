import json
import os.path
import re
from typing import List
import folder_paths  # noqa
from folder_paths import models_dir  # noqa
import comfy.sd  # noqa
import comfy.utils  # noqa
from nodes import LoraLoader  # noqa
from .utils.lora_enc_map import FELoraEmpFinder, read_automap, read_emp
from .utils.any_hack import any
from .utils.model_info import get_metadata


class LoraRef:
    def __init__(self, name: str, model_s: float, clip_s: float):
        self.name = name
        self.model_s = model_s
        self.clip_s = clip_s


def find_model(text, model_name):
    pattern = r'<lora:' + re.escape(model_name) + r':(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)>'
    match = re.search(pattern, text)

    if match:
        model_s = float(match.group(1))
        clip_s = float(match.group(2))
        return match.start(), model_s, clip_s, match.end()
    else:
        return None


class FEEncLoraAutoLoader(LoraLoader, FELoraEmpFinder):
    def __init__(self):
        super().__init__()
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
        s.EMP_CACHE = read_emp("loras")
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "model_type": (["sd1.5", "sdxl", "sd3", "sd3.5", 'pony', 'il', 'noob', 'flux'],),
                "prompt": ("STRING", {"default": "", 'forceInput': True}),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", 'STRING', any)
    RETURN_NAMES = ("MODEL", "CLIP", "prompt", "EXTRA")
    FUNCTION = "load_lora"

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

    def load_lora(self, model, clip, model_type, prompt, strength_model, strength_clip):
        auto_loras = read_automap("loras")
        lora_need_load = []  # type:List[LoraRef]
        pe = str(prompt)
        pe_lower = pe  # .lower()
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

        m = model
        c = clip
        # result = []
        lcnt = 0

        for lora_ref in lora_need_load:
            lora_name = self.find_current_lora(lora_ref.name)
            # try:
            #     result = get_metadata(lora_name) or {}
            # except:
            #     result = {}
            if not lora_name:
                print("Failed to load lora with empty name", lora_ref.name)
                continue
            try:
                m, c = super().load_lora(m, c, lora_name, lora_ref.model_s, lora_ref.clip_s)
                lcnt += 1
            except:
                print("Failed to load lora with error occur", lora_ref.name)
                raise
        print("Auto Load", lcnt, "LLor ClipData")
        return (m, c, pe, {},)
