import json
import os.path

import folder_paths  # noqa
from folder_paths import models_dir  # noqa
import comfy.sd  # noqa
import comfy.utils  # noqa
from nodes import LoraLoader  # noqa
from .utils.lora_enc_map import FELoraEmpFinder, read_emp
from .utils.any_hack import any
from .utils.model_info import get_metadata


class FEEncLoraLoader(LoraLoader, FELoraEmpFinder):
    def __init__(self):
        super().__init__()
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
        s.EMP_CACHE = read_emp("loras")
        out_loras = [s.find_real_lora(lora) for lora in folder_paths.get_filename_list("loras")]
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_name": (out_loras,),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", any)
    RETURN_NAMES = ("MODEL", "CLIP", "EXTRA")
    FUNCTION = "load_lora"

    CATEGORY = "loaders"

    def load_lora(self, model, clip, lora_name, strength_model, strength_clip):
        lora_name = self.find_current_lora(lora_name)
        try:
            result = get_metadata(lora_name) or {}
        except:
            result = {}
        if not lora_name:
            return (model, clip, result,)
        try:
            m, c = super().load_lora(model, clip, lora_name, strength_model, strength_clip)
        except:
            print("Failed to load lora", lora_name)
            raise
        return (m, c, result,)
